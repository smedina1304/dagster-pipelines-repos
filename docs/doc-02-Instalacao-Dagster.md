<p align="center">
   <img src="https://dagster.io/images/brand/logos/dagster-primary-horizontal.png" width="200" style="max-width: 200px;">
</p>

_____

# dagster-pipelines-repos


### Instalação do Dagster e Pacotes necessários:
<br>

:point_right: *Importante: Recomendamos a instalação do Dagster dentro de um virtualenv do Python.  Assim sendo necessário que a instalação do ambiente Python tenha sido realizada previamente, caso contrário, consulte os [tópico anterior](../docs/doc-01-Preparação-Ambiente-Desenv.md) desta documentação. Se estiver executando o Anaconda, instale o Dagster dentro de um ambiente Conda.*

<br>

#### Requisito: 

- Dagster suporta Python 3.8+, para verificar se o Python e o gerenciador de pacotes pip já estão instalados em seu ambiente, você pode executar:

    ```shell
    python --version
    pip --version
    ```

<br>

#### Instalação: 

- Para instalar o Dagster, execute o seguinte comando no seu terminal com o **`"venv"`** ativo:

    ```shell
    pip install dagster
    ```
    <br>

- Como opção e instalando complementos adicionais outros pacotes podem ser adicionados junto a instalação do *core* do Dagster.

    ```shell
    pip install dagster dagster-webserver dagster-duckdb dagster-duckdb-pandas matplotlib
    ```
    <br>

    :point_right:  *Atenção: No Mac com um chip M1 ou M2. Alguns usuários relataram erros de instalação, assim utilize a referentecia da [documentação no site oficial](https://docs.dagster.io/getting-started/install)*
    <br>

- Após a instalação verifique se os pacotes abaixo foram instalados, pois serão utilizados nos exemplos deste projeto, outros pacotes podem ser instalados por suas preferências ou por dependencias de outros pacotes, e não estaram na lista abaixo:
    - **requests**: será usado para baixar dados da internet e integrar com APIs HTTP.
    - **pandas**: é uma biblioteca popular para trabalhar com DataFrames.
    - **matplotlib**: é uma biblioteca muito utilizada que facilita a criação de gráficos em Python.
    - **dagster_duckdb**: é a biblioteca utilizada pelo Dagster para integrar as funcionalidades do DuckDB para ler e gravar dados. O DuckDB é um Data Warehouse em processo semelhante ao SQLite, que será utilizado para persistência de dados.
    - **dagster_duckdb_pandas**: é a biblioteca utilizada pelo Dagster que permite carregar dados do DuckDB em Pandas DataFrames e vice-versa.
    <br>

- Para listar os pacoter ou bibliotecas instaladas no Python, você pode utilizar o comando abaixo:

    ```shell
    pip freeze
    ```

- Para atualizar o arquivo *`requirements.txt`*, o comando abaixo poder ser utilizado na mesma pasta do arquivo:

    ```shell
    pip freeze > requirements.txt
    ```

_____


[:back: *Voltar ao documento raiz*](../README.md)
