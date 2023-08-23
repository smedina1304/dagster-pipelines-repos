<p align="center">
   <img src="https://dagster.io/images/brand/logos/dagster-primary-horizontal.png" width="200" style="max-width: 200px;">
</p>

_____

# dagster-pipelines-repos


### Preparação do Ambiente Python (`venv`) e IDE de Desenvolvimento:
<br>

#### Ambiente de desenvolvimento (IDE):
- Linguagem Python 3.8 (ou superior)
- VS Code (IDE)
    - Plugins (requeridos): 
        - Python extension for VS Code.
        - Pylance
<br>

#### Ambiente Virtual Python para configuração de pacotes requetidos para o desenvolvimento.

- Para instalação do Python e pip (_`Dagster suporta Python 3.8+`_), este tutorial pressupõe que você tenha alguma familiaridade com o Python, e deve ser capaz de acompanhá-lo mesmo se vier de uma linguagem de programação diferente. Para verificar se o Python e pip(o gerenciador de pacotes do Python) já estão instalados em seu ambiente ou instalá-los, siga as instruções [aqui](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

<br>

- Criando o ambiente virtual chamado **`"venv"`**:

    ```shell
    python -m venv venv
    ```
    <br>

    :point_right:  *Atenção: No windows para funcionamento do **`"venv"`** pode ser necessário executar o seguinte comando via Powershell:*
    <br>

    ```shell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```
    <br>


- Ativando o ambiente virtual **`"venv"`**:

    No Windows via Powershell utilizar "`Activate.ps1`".

    ```shell
    .\venv\Scripts\Activate.ps1
    ```
    <br>

    No Windows via CMD utilizar "`activate.bat`".

    ```shell
    .\venv\Scripts\activate.bat
    ```
    <br>

    No `Linux` ou `MAC` utiliar "`activate`".

    ```shell
    source .venv/bin/activate
    ```
    <br>

    :point_right:  *Atenção: Para verificar que está funcionando e o ambiente foi ativado, deve aparecer o nome do ambiente destacado com prefixo do seu prompt de comandos, conforme abaixo:*
    <br>

    ```shell
    (venv)
    ```

<br>

#### Instalação dos Pacotes necessários.
- Todos os pacotes requeridos para o projeto estão listados no arquivo "`requirements.txt`" na pasta `root` do projeto. Para instalação utilize os comandos abaixo:

    <br>

    Passo opcional para atualização do `pip` no ambiente **`venv`**:

    ```shell
    python -m pip install --upgrade pip
    ```
    
    ou utilizando o próprio `pip` para atualizar.

    ```shell
    pip install --upgrade pip
    ```
    <br>

    Passo de instalação dos pacotes via arquivo *`requirements.txt`*:

    ```shell
    pip install -r requirements.txt
    ```

    <br> 

    Como ponto adicional e opcional seguem os pacotes utilizados especificamente para cada _`pipeline (DAG)`_ conforme abaixo.

    <br>

   - [dags/dag-hackernews-report](dags/dag-hackernews-report/README.md)

    ```shell
    pip install PyGithub seaborn
    ```
    <br>

   - [dags/dag-stargazers-analysis](dags/dag-stargazers-analysis/README.md)

    ```shell
    pip install Office365-REST-Python-Client
    ```
    <br>

    :point_right: *Importante: A instalação inicial dos pacotes do Dagster será abordada em detalhes no [próximo tópico](../docs/doc-02-Instalacao-Dagster.md) desta documentação, mesmo que também estejam incluidos no arquivo `requirements.txt`. Esta observação também é válida para os pacotes utilizados especificamente para da cenário (DAG).*

_____

[:back: *Voltar ao documento raiz*](../README.md)
