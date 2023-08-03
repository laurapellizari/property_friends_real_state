<div align="center">
<h3 align="center">Property-Friends Real State</h3>

  <p align="center">
    Production of a model to estimate property valuations for a real estate client in Chile.
    <br />
    <a href="https://github.com/laurapellizari/property_friends_real_state/blob/main/images/kedro_viz.png">Project Pipeline</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Architecture</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
# About The Project

The model was built with the objective of predicting the cost of residential properties in Chile based on the characteristics of the property. For its production, some requirements were demanded, such as:

- Robust pipeline that automates the process of training, evaluation and deployment of the model, which has an abstraction for future connections to databases.
  
- API with basic and documented security system.
  
- API calls/predictions should be logged using a logger for future model monitoring.
  
- Deploy the pipeline and api through a docker.

<!-- Assumptions and Definitions -->
# Assumptions and Definitions

Customer will use some cloud service such as Azure, AWS. The developed project can be instantiated in the best choice for the client.

## Pipeline Definiction - [Kedro]

  As a robust pipeline was required for all stages of the model and that still has an abstraction for a future connection to a database, Kedro was the chosen framework.
  
  The need for robustness with a view to future improvements to the model, given that rapid development was carried out with a lot of room for improvement, weighed in on the choice over other frameworks with a similar function, but with less robustness, such as DVC or MetaFlow.
  
  In addition, Kedro has an excellent level of abstraction called DataCatalog, with connections to the most used databases on the market, such as AWS SageMaker, Hive, MongoDB, among others. The abstraction used was CSVDataSet, since the file was in .csv format.
  
  It is still easy to maintain, having specific files for modifying the database (catalog.yml) and the parameters used to build the model (parameters.yml).
  
  To deploy the model, a pipeline (_model_run()) was built, which has 4 nodes.
  
  - get_train_cols: responsible for building the columns that will be used for training.
  - train_model: responsible for training the entire transformation pipeline and the model algorithm.
  - predict_model: responsible for making model predictions.
  - evaluate_model: responsible for assessing the performance of the model.

The image below exemplifies the flow:

![alt text](https://github.com/laurapellizari/property_friends_real_state/blob/main/images/kedro_viz.png)

## Versioning - [MLFlow]

  As a good practice, it is essential to version code, data and model. In this way, the code versioning in this case is carried out on github, and for the versioning of the data and the model, the interface with MLFlow was implemented.
  
  MLFlow offers tracking, packaging, reproducible runs and sharing services. In addition, it has an interface with kedro, facilitating development. In the model's training code itself, we save the model, its metrics and parameters, ensuring the future interface with logs for monitoring, as desired by the customer.
  
  The image below exemplifies the integration of MLFlow to the project:
  ![alt text](https://github.com/laurapellizari/property_friends_real_state/blob/main/images/mlflow_1.png)
  
  ![alt text](https://github.com/laurapellizari/property_friends_real_state/blob/main/images/mlflow_2.png)
 
The kedro project and MLFlow implementations can be found in the directory property-friends-real-state.

## Application - [FastAPI]

   It was taken into account that a batch model would meet the needs of the client, discarding choices that would aim at a slightly more robust architecture aimed at streaming.
  
  The chosen API framework was FastAPI, since its automatically generated documentation is robust and meets the customer's needs.
  
  For the construction of the API, some good practices were taken into account, such as versioning, data validation via pydantic, failure prevention with HTTPExceptions and authentication via Header.
  
  The API is basically composed of two routes: one get and the other post. The get route is responsible for checking the health of the application and the post route for loading the saved model and performing its predict.
  
  The API project can be found in the property-friends-real-state-api directory.

## Deploy - [Docker]

  Finally, the entire process is modularized in a docker. Therefore, when running docker, the model will be trained via kedro, saved via mlflow and exposed via FastAPI.

<!-- Improvements -->
## Improvements

  1. Currently, the docker container does not expose the mlflow ui port to the host, and it is not possible to see the experiments and metrics directly from the API. Consequently, the API sees a static artifact. Thus, a possible improvement would be exposing it this way, and implementing a dynamic way to see the experiment directly from MLFlow via Docker.
  2. Great-Expectations: As the customer wants to give more robustness to the model, inserting more features or connecting a database, it is essential to monitor the input data so that there is a guarantee that it is the type that the model expects. The great-expectations framework is a great choice for this role.
  3. AirFlow: As the project evolves and the model needs to be retrained every period of time, it would be interesting to connect the architecture to Airflow, a model orchestrator.
  4. Authentication: In the same way, more robust authentication is essential to guarantee security. A suggestion would be JSON Web Token (JWT).
  5. Scalability: It is important to align with the client enough latency to cover the data traffic that he intends to use in the API.
  6. Design Patters: Elaboration of a more robust code aiming at the good practices of design patters, such as the insertion of a Singleton in the API implementation, guaranteeing the creation of a single class instance.
  7. ML Performance: Thinking about generating better model performance, it would be interesting to think about an A/B test implementation architecture. For example, if the customer chooses to use Kubernets, the AKS load balancer can be implemented for A/B testing.
  8. CD4ML: When integrating the framework in some cloud, it is interesting to automate the improvements that the data scientist may make in the model. One way to do this is by implementing test pipelines with assumptions agreed upon with the customer. Integrating with cloud, Docker, Airflow DAG and it can even be deployed in a pod in AKS so that the model image is deployed.
  9. Monitoring: With the use of MLFlow we can observe some nuances over time that may become important to measure the performance of the model, but some other implementations such as DataDrift can help to always keep the model with high performance.
  10. Budget: Perhaps one of the most important things, always try to align whether the solution offered is within the customer's budget.
      
<!-- GETTING STARTED -->
## Getting Started

To reproduce the experiment, it is necessary to clone the repository, and upload the client data in the following directory:

  ```sh
  property-friends-real-state/data/01_raw
  ```

Build the docker image:

  ```sh
    docker build -t deploy -f DockerFile .
  ```

And run it:

  ```sh
  docker run -p 5000:5000 -p 8000:8000 deploy:lastest
  ```

An available API_Key is: api_key_1.

To run only kedro and see kedro viz, as well as the mlflow ui:

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
