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
    pip install dagster dagster-webserver dagster-duckdb dagster-duckdb-pandas
    ```
    <br>

    :point_right:  *Atenção: No Mac com um chip M1 ou M2. Alguns usuários relataram erros de instalação, assim utilize a referentecia da [documentação no site oficial](https://docs.dagster.io/getting-started/install)*
    <br>

   

<br>
<br>

[:back: *Voltar ao documento raiz*](../README.md)
