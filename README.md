# Desafio: Pipeline de Dados com Apache Airflow

## 1\. Contexto do Projeto

Na era da transformação digital, dados precisos são essenciais para empresas como a "DncInsight Solutions", que enfrenta desafios com a qualidade e organização dos dados recebidos. Para resolver isso, a empresa iniciou um desafio interno para desenvolver um sistema robusto e automatizado para o processamento de dados.

Como engenheiro de dados, você foi responsável por desenvolver um pipeline utilizando **Python** e **Apache Airflow** para transformar dados brutos em insights valiosos. O projeto utiliza **Docker** para isolar o ambiente e as dependências, e a simulação de um ambiente de produção foi realizada com pastas locais, em vez de serviços de cloud como o AWS S3.

## 2\. Objetivo

Projetar e implementar um pipeline de dados que ingere dados brutos, os processa e os armazena em três camadas distintas (**bronze**, **silver** e **gold**). O pipeline é orquestrado pelo Apache Airflow.

## 3\. Arquitetura do Pipeline

O pipeline segue a arquitetura de camadas **Bronze, Silver e Gold**, garantindo que os dados sejam progressivamente refinados e transformados em informações prontas para consumo.

### Camada Bronze: Ingestão e Persistência

A primeira etapa do pipeline é responsável por buscar os dados brutos de sua fonte original e salvá-los em um formato otimizado.

  * **Task:** `upload_raw_data_to_bronze`
  * **Ações:**
      * Carrega o dataset inicial da pasta **`raw/`**.
      * Cria uma cópia exata do arquivo na pasta **`bronze/`**, salvando-o no formato `.parquet` para manter a originalidade e consistência dos dados.

### Camada Silver: Tratamento e Enriquecimento

Nesta fase, os dados são carregados da camada Bronze e passam por um processo de limpeza e enriquecimento para melhorar sua qualidade e usabilidade.

  * **Task:** `process_bronze_to_silver`
  * **Transformações:**
      * Lê o arquivo `.parquet` da pasta `bronze/`.
      * **Tratamento de Dados:** Transforma o formato de colunas de data, remove dados nulos e corrige erros de digitação nos e-mails.
      * **Enriquecimento:** Calcula a idade do usuário a partir da data de nascimento e adiciona a nova coluna `age` ao dataset.
      * Salva o novo dataset, agora limpo e enriquecido, na pasta **`silver/`** no formato `.parquet`.

### Camada Gold: Análise e Agregação

A etapa final utiliza os dados da camada Silver para gerar insights e resumos analíticos, criando datasets prontos para uso em dashboards e relatórios.

  * **Task:** `process_silver_to_gold`
  * **Transformações:**
      * Lê o arquivo `.parquet` da pasta `silver/`.
      * **Classificação:** Classifica os usuários por faixa etária, criando uma nova coluna chamada `age_group`.
      * **Agrupamento:** Agrupa o dataset por `age_group` e `subscription_status`, contando o número de usuários ativos e inativos em cada grupo.
      * **Persistência:**
          * Salva um arquivo `.parquet` na pasta **`gold/`** com as colunas `name`, `email`, `date_of_birth`, `signup_date`, `subscription_status`, `age` e `age_group`.
          * Salva um arquivo `.csv` na pasta **`gold/`** com os dados agrupados por faixa etária e o status de subscrição.

## 4\. Estrutura do Projeto

A estrutura de pastas foi organizada para garantir o mapeamento correto dos volumes e a organização do projeto:

```
.
├── .env
├── compose.yml
├── dags/
├── config/
├── logs/
├── plugins/
├── raw/
└── dw/
  ├── bronze/
  ├── silver/
  └── gold/
```

## 5\. Configuração e Execução

### Pré-requisitos

Certifique-se de ter o **Docker** e o **Docker Compose** instalados em sua máquina.

### Documentação: Apache Airflow com Docker Compose

#### 1\. Arquivos de Configuração

  * **`.env`**: Centraliza as variáveis de ambiente, tornando a configuração portátil e segura.
  * **`compose.yml`**: Define os serviços do Airflow e do PostgreSQL, incluindo o mapeamento das pastas locais.

#### 2\. Comandos de Execução

Use a CLI do Docker Compose para gerenciar o ambiente.

**Inicialização do Ambiente (Primeira vez)**
Este passo cria o banco de dados do Airflow e o usuário admin.

```bash
docker compose --profile init up --build
```

Após a conclusão, pare o contêiner com `Ctrl + C` ou use `docker rm -f airflow-init` se estiver rodando em segundo plano.

**Execução dos Serviços do Airflow**
Este passo inicia o servidor web e o agendador em segundo plano.

```bash
docker compose --profile services up --build -d
```

Você poderá acessar a interface web do Airflow em `http://localhost:8080`. O login e a senha padrão são **admin**.