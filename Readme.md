# Desafio: Construindo um Pipeline de Dados com Python

- **Python** para processamento e transformações de dados.
- **Apache Airflow** para orquestrar o pipeline.
- **Docker** para executar o Airflow em um contêiner, isolando suas dependências e ambiente:
- **Base de dados:** /raw/raw_data.csv

### **Contexto:**

Na era da transformação digital, dados precisos são essenciais para empresas como a "DncInsight Solutions", especializada em análise e processamento de dados. A empresa enfrenta desafios com a qualidade e organização dos dados recebidos, muitas vezes inconsistentes e incompletos. Para resolver isso, "DncInsight Solutions" iniciou um desafio interno para desenvolver um sistema robusto e automatizado para o processamento de dados.

Como engenheiro de dados na "DncInsight Solutions", você é responsável por desenvolver um pipeline de dados usando Apache Airflow. Este pipeline transformará dados brutos em insights valiosos através de um processo que inclui a limpeza e agregação de dados. Diferentemente da abordagem tradicional com AWS S3, você simulará um ambiente de produção usando pastas locais para armazenamento de dados.

### **Objetivo:**

Projetar e implementar um pipeline de dados que ingere dados brutos, os processa e os armazena em três camadas distintas (bronze, prata e ouro) . O pipeline deve ser orquestrado usando o Apache Airflow.

## Configuração inicial
    
### Documentação: Apache Airflow com Docker Compose

  1. Estrutura de Pastas
  Para garantir o mapeamento correto dos volumes e a organização do projeto, a estrutura de pastas deve ser a seguinte:

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
  
  .env: Arquivo para as variáveis de ambiente.

  docker-compose.yml: Arquivo de configuração do Docker Compose.

  /dags: Pasta para armazenar os arquivos de DAGs do Airflow.

  /config: Pasta para arquivos de configuração personalizados do Airflow.

  /logs: Pasta para os logs gerados pelo Airflow.

  /plugins: Pasta para plugins personalizados do Airflow.

  /raw: Pasta para armazenar arquivos de dados brutos.

  /dw: Datawarehouse, com subpastas para o modelo de dados (bronze, silver, gold).

  2. Arquivo .env
  Este arquivo centraliza as variáveis de ambiente, tornando a configuração portátil e segura. Preencha-o com seus dados.


  3. Arquivo compose.yml
  Este arquivo define os serviços do Airflow e do PostgreSQL, incluindo o mapeamento das pastas locais.

  4. Dockerfile automatiza a criação de um ambiente consistente, garantindo que o seu aplicativo funcione da mesma forma em qualquer lugar, eliminando problemas como "funciona na minha máquina".

#### Comandos de Execução

  Use a CLI do Docker Compose (sem hífen) para gerenciar o ambiente.

  1. Inicialização do Ambiente (Primeira vez)
  Este passo cria o banco de dados do Airflow e o usuário admin.

    docker compose --profile init up --build
  
  Após a conclusão, pare o container com Ctrl + C ou, se o container estiver rodando em segundo plano (-d), use docker rm -f airflow-init.

  2. Execução dos Serviços do Airflow
  Este passo inicia o servidor web e o agendador em segundo plano (-d).

    docker compose --profile services up --build -d

Você poderá acessar a interface web do Airflow em http://localhost:8080. O login é admin e a senha é admin.camada.

## Criar a pasta app dentro da dags
    - criar os módulos ETL 
      - raw-loader
      - clean
      - preparation
      - load