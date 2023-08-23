# dag_stargazers_analysis

Neste projeto de exemplo, está sendo coletado e sumarizado o conteúdo registrado no Github das últimas pessoas que marcaram com estrela uma lista de repositórios selecionados do Github. Onde estes dados serão apresentados em metadados dos _"assets"_, como *Strings*, *Listas*, *DataFrames* e *Gráficos* informativos.

Este é um modelo de projeto que utiliza a _API Github_ para Python e foi baseado no conteúdo apresentado no blog do _Dagster_ [_"A Dagster Crash Course" by Pete Hunt_](https://dagster.io/blog/dagster-crash-course-oct-2022). Como o projeto anterior [Hacker News - dag_hackernews_report](../dag-hackernews-report/README.md), este também foi iniciado  automaticamente pelo comando [*"dagster project scaffold"*](https://docs.dagster.io/getting-started/create-new-project), que pode ser consultado na documentação oficial.


## Resumo do processo de criação do projeto

Primeiro, conclua os tópicos de instalação e preparação do ambiente Python com os paciotes do Dagster listados no [*README.md*](../README.md) documento na raiz do projeto.

Seguindo, comando de criação do projeto na pasta _DAGS_:

```shell
dagster project scaffold --name dag-stargazers-analysis
```

Depois de executar a criação, deve haver um novo diretório chamado _`dag-stargazers-analysis`_ em seu diretório atual. Este diretório contém os arquivos que compõem seu projeto Dagster seguindo o padrão de projeto _`scaffold`_. Em seguida, é necessário instalar as dependências do Python que usará durante o uso do projeto.

```shell
cd dag-stargazers-analysis
pip install -e ".[dev]"
```

Em seguida, os dados de localização do módulo devem ser incluidos no arquivo _`workspace.yaml`_ na pasta raiz, onde o Dagster deverá ser executado nesta estrutura de multiplos projetos.

```yaml
load_from:
  - python_module:
      module_name: dag_hackernews_report
      working_directory: dags/dag-hackernews-report
  - python_module:
      module_name: dag_stargazers_analysis
      working_directory: dags/dag-stargazers-analysis
```

👉 Atenção: Observe a mesmas diferença nos parametros _`module_name`_ e _`working_directory`_ comentatada no projeto anterior [Hacker News - dag_hackernews_report](../dag-hackernews-report/README.md), sendo que a configuração referente a este exemplo se refere a pasta _`dag-stargazers-analysis`_.


Para verificar se funcionou o que foi realizado até o momento pode executar o Dagster localmente, com o seguinte comando na pasta raiz do projeto onde está localizado o arquivo _`workspace.yaml`_.

```shell
dagster dev
```

Navegue para URL http://localhost:3000 para ver a interface do usuário (_IU_) do Dagster. Este comando executará o Dagster até que você esteja pronto para pará-lo. Para interromper o processo de longa duração, pressione Control+C no terminal em que o processo está sendo executado.

Com isso observe o conteú programado os _"assets"_, _"jobs"_ e _"schedulers"_, que podem ser localizados neste projeto em dois arquivos apenas:
    - `dag_stargazers_analysis/assets.py`
    - `dag_stargazers_analysis/__init__.py`

Como requisito para atender os pacotes utilizados nesta _DAG_, segue a instrução de intalação:

```shell
pip install PyGithub seaborn
```

## Desenvolvimento

Para uma variação e outros comentários sobre a utilização do mesmo cenário de dados, utilize a referência do blog[_"A Dagster Crash Course" by Pete Hunt_](https://dagster.io/blog/dagster-crash-course-oct-2022) na página oficial do Dagster. Propositalmente este exemplo foi baseado neste blog para utilizar de todo conteúdo explicativo gerado pelo grupo de profissionais que utilizam o _Dagster_.

### Adicionando novas dependências do Python

Pode-se especificar novas dependências do Python em `setup.py`, sendo necessário para alterações ou testes desejados com base neste projeto.

### Testes unitários

Testes automatizados podem ser codificados na pasta `dag_stargazers_analysis_tests`, podendo executá-los usando `pytest`:

```bash
pytest dag_stargazers_analysis_tests
```

👉 Atenção: esta funcionalidade não foi aplicada neste projeto.

## Implantação no Dagster Cloud

Confira a documentação do ["Dagster Cloud"](https://docs.dagster.cloud) para saber mais.

_____


[:back: *Voltar ao documento raiz*](/README.md)