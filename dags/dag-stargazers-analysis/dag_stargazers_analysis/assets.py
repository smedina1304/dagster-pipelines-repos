import os
import base64
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from io import BytesIO
from github import Github
from datetime import datetime, timedelta
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

class MyAssetConfig(Config):
    github_repos: list
    data_path = 'data/dags/stargazers'
    dataset_name = 'df_github_stargazers.csv'  

@asset( group_name="stargazers", required_resource_keys={"github_api"} )
def get_github_stargazers(context: AssetExecutionContext, config: MyAssetConfig) -> MyAssetConfig:
    """
    Busca os dados das ESTRELAS de cada repositório git informado na Lista de configuração.
    """
    logger = get_dagster_logger()

    logger.info(f"Verifica se o diretório existe: {config.data_path}")
    if not os.path.isdir(config.data_path):
        logger.info(f">> Diretório criado: {config.data_path}")
        os.makedirs(config.data_path)

    path_file = f'{config.data_path}/{config.dataset_name}'

    try:
        dtfile = datetime.fromtimestamp(os.path.getmtime(path_file))
        if datetime.now().date() == dtfile.date():
            logger.info(f"Dataframe já foi baixado em: {dtfile.date()}")
            logger.info(f"Dataframe disponível em: {path_file}")
    except OSError as e:
        logger.info(f"Arquivo não encontrado: {path_file}")
        logger.info(f">> Exception: {e.strerror}")

        # Baixando os dados
        logger.info(f"Iniciando o Downloading de dados!")
        df = None

        for repo in config.github_repos:
            print(repo)
            logger.info(f"Request -> get_stargazers_with_dates(): {repo}")
            repo_stargazers = list(
                context.resources.github_api.get_repo(repo).get_stargazers_with_dates()
            )

            dfrepo = pd.DataFrame(
                [
                    {
                        "users": stargazer.user.login,
                        "date": stargazer.starred_at.date(),
                        "week": stargazer.starred_at.date()
                        + timedelta(days=6 - stargazer.starred_at.weekday()),
                    }
                    for stargazer in repo_stargazers
                ]
            )

            dfrepo['repo'] = repo

            if df is None:
                df = dfrepo.copy()
            else:
                df = pd.concat([df, dfrepo], ignore_index=True)

            del dfrepo

        df.to_csv(path_file)

    context.add_output_metadata(
        metadata={
            "github_repos": str(config.github_repos),
            "data_path" : config.data_path,
            "dataset_name" : config.dataset_name  
        }
    )

    return config


@multi_asset(
        group_name="stargazers",
        ins={"data_config": AssetIn("get_github_stargazers")},
        outs={
            "data_config": AssetOut(description='Config - Dados de configuração do processo.'),
            "df_week": AssetOut(description='Dataframe - Dados de contagem com marcador SEMANAL.'),
            "df_week_sum": AssetOut(description='Dataframe - Totalizações de contagem por semana/repositório.'),
            "df_year_sum": AssetOut(description='Dataframe - Totalizações de contagem por ano/repositório.')
        }
    )
def data_analysis_process(context: AssetExecutionContext, data_config: MyAssetConfig):
    """
    Processo de preparação de análise de dados.
    """
    logger = get_dagster_logger()
    path_file = f'{data_config.data_path}/{data_config.dataset_name}'

    df = None
    df_week = None
    df_week_sum = None
    df_year_sum = None

    try:
        # Dataframe - Dados "Github-Repos-Stargazers"
        df = pd.read_csv(path_file)
        logger.info(f"Dataframe foi carregado de: {path_file}")

        # Dataframe - Seleção de dados de contagem com marcador SEMANAL.
        df_week=df.groupby(["repo","week"]).count().sort_values(by=["week","repo"]).reset_index()
        df_week=df_week[['repo','week','users']].copy()

        df_week["week"] = pd.to_datetime(df_week["week"], format='%Y-%m-%d')

        # Dataframe - Totalizações de contagem por semana/repositório.
        df_week_sum=df_week.groupby(['repo', 'week'])['users'].sum() \
                    .groupby(level=0).cumsum().reset_index()
        
        # Dataframe - Totalizações de contagem por ano/repositório.
        df_week_sum['year'] = df_week_sum.apply(lambda row : row["week"].replace(day=1, month=1), axis=1)
        df_year_sum = pd.DataFrame({'users' : df_week_sum.groupby(['repo',"year"])['users'].sum().astype(int)}).reset_index()

    except FileNotFoundError as error:
        logger.info(f">> ERRO na leitura do Dataframe: {path_file}")
        logger.info(f">> FileNotFoundError: {error}")

    return data_config, df_week, df_week_sum, df_year_sum


@asset(
        group_name="stargazers",
        ins={
            "data_config": AssetIn("data_config"),
            "df_week": AssetIn("df_week")
        }
    )
def graph_analytic_hist(context: AssetExecutionContext, data_config: MyAssetConfig, df_week: pd.DataFrame):
    """
    Gráfico Analítico - Histórico de Estrelas por Repositório.
    """
    logger = get_dagster_logger()

    sns.set(rc={'figure.figsize':(15,5)})

    # 01 - Grafico histórico
    line1 = sns.lineplot(
        x="week",
        y="users",
        hue="repo",
        hue_order=data_config.github_repos,
        data=df_week)
    line1.set(title='Histórico de Estrelas por Repositório', xlabel="Período", ylabel="Estrelas")
    line1.legend(fontsize=9, title='Github Repos')

    # Convertendo a imagem para um formato que pode ser salvo
    buffer = BytesIO()
    line1.get_figure().savefig(buffer, format="png")
    image_graph_hist = base64.b64encode(buffer.getvalue())

    # Convertendo a imagem em Markdown para visualizá-la no Dagster
    md_graph_hist = f"![img](data:image/png;base64,{image_graph_hist.decode()})"

    # limpando o cache
    del line1, buffer
    plt.clf()

    ## 02 - Grafico histórico após 2022-01-01
    dt = datetime(2022,1,1)

    line2 = sns.lineplot(
        x="week",
        y="users",
        hue="repo",
        hue_order=data_config.github_repos,
        data=df_week.loc[df_week['week']>=dt])
    line2.set(title=f'Histórico de Estrelas por Repositório (após {dt.date()})', xlabel="Período", ylabel="Estrelas")
    line2.legend(fontsize=9, title='Github Repos')

        # Convertendo a imagem para um formato que pode ser salvo
    buffer = BytesIO()
    line2.get_figure().savefig(buffer, format="png")
    image_graph_2022 = base64.b64encode(buffer.getvalue())

    # Convertendo a imagem em Markdown para visualizá-la no Dagster
    md_graph_2022 = f"![img](data:image/png;base64,{image_graph_2022.decode()})"

    # Adicionando o conteúdo Markdown como metadados ao ativo
    context.add_output_metadata(
        metadata={
            "graph_hist": MetadataValue.md(md_graph_hist),            
            "graph_after_2022": MetadataValue.md(md_graph_2022),
        }
    )

    logger.info(f">> Gráfico gerado com sucesso.")



@asset(
        group_name="stargazers",
        ins={
            "data_config": AssetIn("data_config"),
            "df_week_sum": AssetIn("df_week_sum")
        }
    )
def graph_analytic_totals(context: AssetExecutionContext, data_config: MyAssetConfig, df_week_sum: pd.DataFrame):
    """
    Gráfico Analítico - Acumulativo e Ranking por Repositório.
    """
    logger = get_dagster_logger()

    sns.set(rc={'figure.figsize':(15,5)})

    # 01 - Grafico Acumulado
    line = sns.lineplot(
        x="week",
        y="users",
        hue="repo",
        hue_order=data_config.github_repos,
        data=df_week_sum)
    line.set(title='Total Acumulado', xlabel="Período", ylabel=f"Estrelas")
    line.legend(fontsize=9)

    # Convertendo a imagem para um formato que pode ser salvo
    buffer = BytesIO()
    line.get_figure().savefig(buffer, format="png")
    image_graph_line = base64.b64encode(buffer.getvalue())

    # Convertendo a imagem em Markdown para visualizá-la no Dagster
    md_graph_line = f"![img](data:image/png;base64,{image_graph_line.decode()})"

    # limpando o cache
    del line, buffer
    plt.clf()

    # 02 - Grafico Ranking
    df_total = df_week_sum.groupby(["repo"]).max().sort_values(by=["users"]).reset_index()
    bar = sns.barplot(x="repo", y="users", data=df_total)
    bar.set(title='Ranking - Total Estrelas', xlabel="Github Repos", ylabel=f"Total Estrelas")
 
     # Convertendo a imagem para um formato que pode ser salvo
    buffer = BytesIO()
    bar.get_figure().savefig(buffer, format="png")
    image_graph_bar = base64.b64encode(buffer.getvalue())

    # Convertendo a imagem em Markdown para visualizá-la no Dagster
    md_graph_bar = f"![img](data:image/png;base64,{image_graph_bar.decode()})"

    # Adicionando o conteúdo Markdown como metadados ao ativo
    context.add_output_metadata(
        metadata={
            "total_repos": len(data_config.github_repos),
            "total_users": int(df_total['users'].sum()),            
            "table_total": MetadataValue.md(df_total[['repo', 'users']].to_markdown()),
            "graph_total": MetadataValue.md(md_graph_line),            
            "graph_ranking": MetadataValue.md(md_graph_bar),
        }
    )

    logger.info(f">> Gráfico gerado com sucesso.")


@asset(
        group_name="stargazers",
        ins={
            "data_config": AssetIn("data_config"),
            "df_year_sum": AssetIn("df_year_sum")
        }
    )
def graph_analytic_year(context: AssetExecutionContext, data_config: MyAssetConfig, df_year_sum: pd.DataFrame):
    """
    Gráfico Analítico - Total Anual de Estrelas por Repositório.
    """
    logger = get_dagster_logger()

    sns.set(rc={'figure.figsize':(15,5)})

    # 01 - Grafico Anual
    line = sns.lineplot(
        x="year",
        y="users",
        hue="repo",
        hue_order=data_config.github_repos,
        data=df_year_sum)
    line.set(title='Total Anual de Estrelas por Repositório', xlabel="Período", ylabel="Estrelas")
    line.legend(fontsize=9, title='Github Repos')

    # Convertendo a imagem para um formato que pode ser salvo
    buffer = BytesIO()
    line.get_figure().savefig(buffer, format="png")
    image_graph_line = base64.b64encode(buffer.getvalue())

    # Convertendo a imagem em Markdown para visualizá-la no Dagster
    md_graph_line = f"![img](data:image/png;base64,{image_graph_line.decode()})"

    # Adicionando o conteúdo Markdown como metadados ao ativo
    context.add_output_metadata(
        metadata={
            "graph_year": MetadataValue.md(md_graph_line),
        }
    )

    logger.info(f">> Gráfico gerado com sucesso.")

