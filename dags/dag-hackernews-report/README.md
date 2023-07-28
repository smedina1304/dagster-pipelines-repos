<p align="center">
   <img src="https://dagster.io/images/brand/logos/dagster-primary-horizontal.png" width="200" style="max-width: 200px;">
</p>

_____

# dag_hackernews_report

Neste projeto de exemplo, está sendo coletado e sumarizado o conteúdo das últimas postagens realizadas em um site popular de notícias chamado [Hacker News](https://news.ycombinator.com/), o site apresenta histórias enviadas por usuários sobre tecnologia, startups e outras fontes da Internet. Onde estes dados serão apresentados em metadados dos _"assets"_, como *Strings*, *Listas*, *DataFrames* e *Gráficos* informativos.

Este é um modelo de projeto padrão do [Dagster](https://dagster.io/) gerado automaticamente pelo comando [*"dagster project scaffold"*](https://docs.dagster.io/getting-started/create-new-project), que pode ser consultado na documentação oficial.


## Resumo do processo de criação do projeto

Primeiro, conclua os tópicos de instalação e preparação do ambiente Python com os paciotes do Dagster listados no [*README.md*](../README.md) documento na raiz do projeto.

Seguindo, comando de criação do projeto na pasta _DAGS_:

```shell
dagster project scaffold --name dag-hackernews-report
```

Depois de executar a criação, deve haver um novo diretório chamado _`dag-hackernews-report`_ em seu diretório atual. Este diretório contém os arquivos que compõem seu projeto Dagster seguindo o padrão de projeto _`scaffold`_. Em seguida, é necessário instalar as dependências do Python que usará durante o uso do projeto.

```shell
cd dag-hackernews-report
pip install -e ".[dev]"
```

Em seguida, os dados de localização do módulo devem ser incluidos no arquivo _`workspace.yaml`_ na pasta raiz, onde o Dagster deverá ser executado nesta estrutura de multiplos projetos.

```yaml
load_from:
  - python_module:
      module_name: dag_hackernews_report
      working_directory: dags/dag-hackernews-report
```

👉 Atenção: Observe uma pequena diferença nos parametros _`module_name`_ e _`working_directory`_, onde no comando de criação do projeto padrão _scaffold_ o nome foi informado com o _hìfen_ (_`-`_) "_`dag-hackernews-report`_", porem para o módulo gerado pelo comando do Dagster mudou para _underscore_ (_`_`_). Esta pequena diferença pode impossibilitar a execução do projeto.


Para verificar se funcionou o que foi realizado até o momento pode executar o Dagster localmente, com o seguinte comando na pasta raiz do projeto onde está localizado o arquivo _`workspace.yaml`_.

```shell
dagster dev
```

Navegue para URL http://localhost:3000 para ver a interface do usuário (_IU_) do Dagster. Este comando executará o Dagster até que você esteja pronto para pará-lo. Para interromper o processo de longa duração, pressione Control+C no terminal em que o processo está sendo executado.

Com isso e tudo rodando bem, a é possível iniciar a escrever os _"assets"_, _"jobs"_ e _"schedulers"_, que podem ser localizados neste projetos em dois arquivos apenas:
    - `dag_hackernews_report/assets.py`
    - `dag_hackernews_report/__init__.py`


## Desenvolvimento

Para um melhor entendimento, utilize a referência do [tutorial](https://docs.dagster.io/tutorial/introduction) na página oficial do Dagster. Propositalmente este exemplo foi baseado neste tutorial para utilizar de todo conteúdo explicativo dado pelo produto.

### Adicionando novas dependências do Python

Pode-se especificar novas dependências do Python em `setup.py`, sendo necessário para alterações ou testes desejados com base neste projeto.

### Testes unitários

Testes automatizados podem ser codificados na pasta `dag_hackernews_report_tests`, podendo executá-los usando `pytest`:

```bash
pytest dag_hackernews_report_tests
```

👉 Atenção: esta funcionalidade não foi aplicada neste projeto.

## Implantação no Dagster Cloud

Confira a documentação do ["Dagster Cloud"](https://docs.dagster.cloud) para saber mais.

