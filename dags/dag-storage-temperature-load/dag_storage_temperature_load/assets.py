import pandas as pd
import os
import json
import jwt
import requests

from cryptography.fernet import Fernet

from office365.sharepoint.client_context import ClientContext, UserCredential

from dagster import (
    AssetExecutionContext,
    MetadataValue,
    multi_asset,
    AssetIn,
    AssetOut,
    asset,
    Config,
    get_dagster_logger
)

# DataFrames Storage Class
class MyDataFrames():
    df_plant : pd.DataFrame = None
    df_desvio : pd.DataFrame = None
    df_armazem : pd.DataFrame = None
    df_montemp : pd.DataFrame = None

# Functions
def __getSPList(office_context : ClientContext, name = None, columns = None) -> list:
  lines = []
  if name is not None:
    if columns is not None:

      tb = office_context.web.lists.get_by_title(name)
      items = tb.items.get().select(["*"]).execute_query()
      for item in items:  # type:ListItem
        line = []
        for col in columns:
          line.append(item.properties.get(col))
        lines.append(line)

    else:
      print("ERRO: List columns is [NONE] or [NULL]")
    
  else:
    print("ERRO: List name is [NONE] or [NULL]")

  return lines

def __getDataFrameFromSPList(office_context : ClientContext, name = None, columns = None) -> pd.DataFrame:
  lst = __getSPList(office_context, name, columns)
  df = pd.DataFrame(lst, columns = columns)
  return df


@asset( group_name="storage_temperature", required_resource_keys={"url_site","user_credentials"} )
def get_sharepoint_data(context: AssetExecutionContext) -> MyDataFrames:
    """
    Retorna os dados das Listas de Temperaturas registradas do Site no Sharepoint em formato DataFrame Pandas.
    """
    logger = get_dagster_logger()

    logger.info(f">> Conectando com URL: {context.resources.url_site}")
    user_credentials : UserCredential = context.resources.user_credentials
    ctx = ClientContext(context.resources.url_site).with_credentials(user_credentials)
    logger.info(">> Conexão realizada com SUCESSO!") 

    dfs = MyDataFrames()

    # TBPLANT
    logger.info(">> Loading: TBPLANT")
    dfs.df_plant = __getDataFrameFromSPList(office_context=ctx, name="TBPLANT", columns=['Title','CDPLANT','DSPLANT'])
    dfs.df_plant.rename(columns={'Title': 'IDPLANT'}, inplace=True)

    # TBDESVIO
    logger.info(">> Loading: TBDESVIO")
    dfs.df_desvio = __getDataFrameFromSPList(office_context=ctx, name="TBDESVIO", columns=['Title','DSDESVIO'])
    dfs.df_desvio.rename(columns={'Title': 'IDDESVIO'}, inplace=True)

    # TBARMAZEM
    logger.info(">> Loading: TBARMAZEM")
    dfs.df_armazem = __getDataFrameFromSPList(office_context=ctx, name="TBARMAZEM", columns=['Title','IDPLANT','CDARMAZ','DSARMAZ','SETPOINTMIN','SETPOINTMAX'])
    dfs.df_armazem.rename(columns={'Title': 'IDARMAZ'}, inplace=True)

    # TBMONTEMP
    logger.info(">> Loading: TBMONTEMP")
    dfs.df_montemp = __getDataFrameFromSPList(office_context=ctx, name="TBMONTEMP", columns=['Title','IDARMAZ','DTTEMP','TEMPMIN','TEMPAVG','TEMPMAX','IDDESVIO'])
    dfs.df_montemp.rename(columns={'Title': 'IDMONTEMP'}, inplace=True)
    dfs.df_montemp['DTTEMP'] = pd.to_datetime(dfs.df_montemp['DTTEMP'], format=('%Y-%m-%dT%H:%M:%SZ'))    

    context.add_output_metadata(
        metadata={
            "sharepoind_site": context.resources.url_site,
            "count_df_plant" : dfs.df_plant.shape[0],
            "count_df_desvio" : dfs.df_desvio.shape[0],
            "count_df_armazem" : dfs.df_armazem.shape[0],
            "count_df_montemp" : dfs.df_montemp.shape[0]
        }
    )

    logger.info(f">> Dados carregados das Listas do Sharepoint com Sucesso!!!")

    return dfs


@asset(
  group_name="storage_temperature",
  ins={"dfs_lists": AssetIn("get_sharepoint_data")},
  required_resource_keys={"data_path","file_name"}
)
def join_all_dataframes(context: AssetExecutionContext, dfs_lists: MyDataFrames) -> pd.DataFrame:
    """
    Retorna o JOIN de todos DataFrames populados pelas listas do Sharepoint.
    """

    logger = get_dagster_logger()

    logger.info(f"Verifica se o diretório existe: {context.resources.data_path}")
    if not os.path.isdir(context.resources.data_path):
        logger.info(f">> Diretório criado: {context.resources.data_path}")
        os.makedirs(context.resources.data_path)

    path_file = f'{context.resources.data_path}/{context.resources.file_name}'

    join1 = pd.merge(dfs_lists.df_montemp, dfs_lists.df_armazem, on='IDARMAZ')
    join2 = pd.merge(join1, dfs_lists.df_plant, on='IDPLANT')
    join_all = pd.merge(join2, dfs_lists.df_desvio, on='IDDESVIO')

    join_all.to_csv(path_file)

    context.add_output_metadata(
        metadata={
            "data_path": context.resources.data_path,
            "file_name" : context.resources.file_name,
            "count_join" : join_all.shape[0]
        }
    )

    logger.info(f">> Dataframe unificado com sucesso!!!")

    return join_all

@asset(
  group_name="storage_temperature",
  ins={"df": AssetIn("join_all_dataframes")},
  required_resource_keys={"supabase_url","supabase_key","supabase_token"}
)
def supabase_tb_upsert(context: AssetExecutionContext, df: pd.DataFrame) -> None:
    """
    Atualiza a Tabela POWERAPPS_MONTEMP no ambiente do SUPABASE.
    """
    logger = get_dagster_logger()

    supabase_url = 'https://localhost:8080'

    # Ajusdando o formado de data para gravação no banco de dados
    logger.info(">> Convertendo o formado de _'datetime64'_ para _'timestamp'_ no padrão da base de dados.")
    df['DTTEMP']=df['DTTEMP'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    # Atualizando os dados na base
    logger.info(">> Atutalizando a Tabela 'POWERAPPS_MONTEMP' no Supabase (sm-apps/storage-apps).")
    regs = df.to_json(orient="records")
    regs = json.loads(regs)
    
    # preparando URL REST-API
    url = f"{context.resources.supabase_url}/rest/v1/POWERAPPS_MONTEMP"

    # Chamada da API
    logger.info(">> POST - UPSERT.")

    encoded_jwt = jwt.encode({}, context.resources.supabase_token, algorithm="HS256")
    headers = {
      'Authorization': f'Bearer {encoded_jwt}',
      'apikey': context.resources.supabase_key,
      'Content-Type': 'application/json',
      'Prefer': 'resolution=merge-duplicates'
      }   
    response = requests.post(url, json=regs, headers=headers)

    # Fechando a conexão
    logger.info(f">> Response Status: {response.status_code} {response.text}")
  