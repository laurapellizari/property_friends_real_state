<div align="center">
<h3 align="center">Property-Friends Real State</h3>

  <p align="center">
    Production of a model to estimate property valuations for a real estate client in Chile.
    <br />
    <a href="https://github.com/github_username/repo_name">Project Pipeline</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Architecture</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
# About The Project

O modelo foi construido com o objetivo de prever o custo de propriedades residenciais no Chile com base nas características da propriedade. Para sua produtizacao foram demandados alguns requisitos como: 

- Pipeline robusto que automatize o processo de treinamento, avaliação e implantação do modelo, o qual tenha uma abstracao para conexoes futuras a databases.
  
- API com sistema de seguranca basico e documentada.
  
- Chamadas/previsões de API devem gerar logs usando um registrador para monitoramento de modelo futuro.
  
- Deploy do pipeline e api por meio de um docker.

<!-- Assumptions and Definitions -->
# Assumptions and Definitions

O cliente usará algum serviço de cloud, como Azure, AWS. O projeto desenvolvido pode  ser instanciado na melhor escolha para o cliente.

## Pipeline Definiction - [Kedro]

  Como foi demandado um pipeline robusto para todas as etapas do modelo e que ainda possua uma abstração para uma futura conexão com um database, o Kedro foi o framework escolhido. 
  
  A necessidade por uma robustez pensando em melhorias futuras do modelo, visto que foi realizado um desenvolvimento rápido com muito espaço para melhorias, pesou na escolha ao invés de outros frameworks com a função parecida, mas com uma menor robustez, como por exemplo o DVC ou MetaFlow.
  
  Além disso, o Kedro possui um excelente nível de abstração chamada DataCatalog, com conexões de databases mais utilizados no mercado, como AWS SageMaker, Hive, MongoDB, entre outros. A abstração utilizada foi CSVDataSet, visto que o arquivo estava em formato .csv.
  
  Ainda é de fácil manutenção, possuindo arquivos especificos para modificações no database (catalog.yml) e nos parametros utilizados para construir o modelo (parameters.yml).
  
  Para o deploy do modelo foi construido um pipeline (_model_run()), o qual possui 4 nós. 
  
  - get_train_cols: responsável por construir as colunas que seram utilizadas para treinamento.
  - train_model: responsável por treinar todo o pipeline de transformação e do algoritmo do modelo.
  - predict_model: responsável por realizar as predições do modelo.
  - evaluate_model: responsável por aferir o desempenho do modelo.

A imagem abaixo exemplifica o fluxo:

 Adicionar kedro viz

## Versionamento - [MLFlow]

  Como uma boa prática, é impresendivel versionar código, dados e modelo. Dessa forma, o versionamento de código nesse caso é realizado no github, e para o vesionamento dos dados e do modelo foi implementado a interface com o MLFlow. 
  
  O MLFlow oferece serviçoes de tracking, packaging, reproducible runs e sharing. Além disso, possui uma interface com o kedro, facilitando o desenvolvimento. No próprio código de treinamento do modelo, salvamos o modelo, suas metricas e parametros, garantindo a interface futura com logs para monitoria, como desejado pelo cliente.
  
  A imagem abaixo exemplifica a integração do MLFlow ao projeto:
  
 Adicionar MLFlow

O projeto kedro e as implementações do MLFlow podem ser encontrado no diretório property-friends-real-state.

## Forma de utilização - [FastAPI]

  Levou - se em consideração que um modelo batch atenderia as necessidades do cliente, descartando escolhas que visariam uma arquitetura um pouco mais robusta visando o streaming.
  
  O framework de API escolhido foi FastAPI, visto que sua documentação gerada automaticamente é robusta e atende as necessidades do cliente. 
  
  Para a construção da API foram levadas algumas boas práticas em consideração, como o versionamento, validação de dados via pydantic, prevenção a falhas com HTTPExceptions e uma atenticação via Header. 
  
  A API é composta basicamente por duas rotas: uma get e outra post. A rota get é responsável por verificar a saúde da aplicação e a rota post por carregar o modelo salvo e realizar seu predict. 

## Deploy - [Docker]

  Por fim, todo o processo é modularizado em um docker. Portanto, ao rodar o docker, o modelo será treinado via kedro, salvo via mlflow e exposto via fastapi.

<!-- Melhorias -->
## Melhorias

  1. Atualmente, o container docker não expõe a porta do mlflow ui para o host, não sendo possível enxergar os experimentos e métricas diretamente da API. Consequentemente, a API enxerga um artefato estático. Dessa forma, uma possível melhoria seria a exposição dessa forma, e a implementação de uma maneira dinamica para ver o experimento direto do MLFlow via Docker.
  2. Great-Expectations: Conforme o cliente queira dar mais robustez ao modelo, inserindo mais features ou conectando um database, é essencial monitorar os dados de entrada para que haja garantia de que são do tipo que o modelo espera. O framework great- expectations é uma ótima escolha para essa função.
  3. AirFlow: Conforme o projeto evolua e o modelo necessite ser retreinado a cada período de tempo, seria interessante conectar a arquitetura ao Airflow, um orquestrador de modelos.
  4. Autenticação: Da mesma forma, uma autenticação com maior robustez é impressendivel para garantir segurança. Uma sugestao seria JSON Web Token (JWT).
  5. Escalabilidade: É importante alinhar com o cliente a latencia suficiente para abrangir o tráfigo de dados que ele pretende utilizar na API.
  6. Design Patters: Elaboração de um código mais robusto visando as boas práticas de design patters, como por exemplo a inserção de um Singleton na implementação da API, garantindo a criação de uma só instancia de classe.
  7. Performance ML: Pensando em gerar uma melhor performance do modelo, seria interessante pensar em uma arquitetura de implementação de testes A/B. Por exemplo, se o cliente optar por utilizar Kubernets, pode - se implementar o balanceador de carga AKS para os testes A/B.
  8. CD4ML: Ao integrar o framework em alguma cloud, é interessante automatizar as melhorias que o cientista de dados possa vir a fazer no modelo. Uma maneira de fazer isso é por meio da implementação de pipelines de teste com premissas acordadas com o cliente. Integrando com cloud, Docker, Airflow DAG e ainda pode - se implementar em um pod no AKS para que a imagem do modelo seja implementada.
  9. Monitoria: Com o uso do MLFlow podemos observar algumas nuances ao longo do tempo que possam vir a ser importantes para medir o desempenho d modelo, mas algumas outras implementações como o DataDrift podem ajudar a manter sempre o modelo com alta performance.
  10. Budget: Talvez uma das coisas mais importantes, sempre procurar alinhar se a solução oferecida está dentro do orçamento do cliente.

<!-- GETTING STARTED -->
## Getting Started

Para reproduzir o experimento, é necessário clonar o repositório, contruir a imagem docker:
  ```sh
    docker build -t deploy -f DockerFile .
  ```

E roda - la:
  ```sh
  docker run -p 5000:5000 -p 8000:8000 deploy:lastest
  ```

Uma API_Key disponibilizada é: api_key_1.

Para rodar apenas o kedro e enxergar o kedro viz, assim como a ui do mlflow: 
  ```sh
  cd property-friends-state-real
  ```

  ```sh
  kedro run
  ```

  ```sh
  kedro viz
  ```

  ```sh
  kedro mlflow ui
  ```

### Prerequisites

- env conda



[MLFlow]: https://mlflow.org/
[Docker]: https://www.docker.com/
[FastAPI]: https://fastapi.tiangolo.com/
[Kedro]: https://kedro.org/
