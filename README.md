<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Property-Friends Real State</h3>

  <p align="center">
    Production of a model to estimate property valuations for a real estate client in Chile.
    <br />
    <a href="https://github.com/github_username/repo_name">Project Pipeline</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Architecture</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

O modelo foi construido com o objetivo de prever o custo de propriedades residenciais no Chile com base nas características da propriedade. Para sua produtizacao foram demandados alguns requisitos como: 

- Pipeline robusto que automatize o processo de treinamento, avaliação e implantação do modelo, o qual tenha uma abstracao para conexoes futuras a databases.
- API com sistema de seguranca basico e documentada.
- Chamadas/previsões de API devem gerar logs usando um registrador para monitoramento de modelo futuro.
- Deploy do pipeline e api por meio de um docker.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Assumptions and Definitions -->
## Assumptions and Definitions

O cliente usará algum serviço de cloud, como Azure, AWS. O projeto desenvolvido pode  ser instanciado na melhor escolha para o cliente.

Pipeline Definiction - Kedro:
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

## Adicionar kedro viz

Versionamento - MLFlow:
  Como uma boa prática, é impresendivel versionar código, dados e modelo. Dessa forma, o versionamento de código nesse caso é realizado no github, e para o vesionamento dos dados e do modelo foi implementado a interface com o MLFlow. 
  O MLFlow oferece serviçoes de tracking, packaging, reproducible runs e sharing. Além disso, possui uma interface com o kedro, facilitando o desenvolvimento. No próprio código de treinamento do modelo, salvamos o modelo, suas metricas e parametros, garantindo a interface futura com logs para monitoria, como desejado pelo cliente.
  A imagem abaixo exemplifica a integração do MLFlow ao projeto:
## Adicionar MLFlow

O projeto kedro e as implementações do MLFlow podem ser encontrado no diretório property-friends-real-state.

Forma de utilização - API:
  Levou - se em consideração que um modelo batch atenderia as necessidades do cliente, descartando escolhas que visariam uma arquitetura um pouco mais robusta visando o streaming.
  O framework de API escolhido foi FastAPI, visto que sua documentação gerada automaticamente é robusta e atende as necessidades do cliente. 
  Para a construção da API foram levadas algumas boas práticas em consideração, como o versionamento, validação de dados via pydantic, prevenção a falhas com HTTPExceptions e uma atenticação via Header. 
  A API é composta basicamente por duas rotas: uma get e outra post. A rota get é responsável por verificar a saúde da aplicação e a rota post por carregar o modelo salvo e realizar seu predict. 

Deploy - Docker
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

### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

kedro viz
kedro mlflow ui
### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
