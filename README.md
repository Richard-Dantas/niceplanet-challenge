<h1 align="center"> Teste BackEnd Niceplanet </h1>
🚀 Projeto desenvolvido como parte do processo seletivo para ingresso na empresa Niceplanet Geotecnologia

# Tecnologias Utilizadas
- Python
- Django Rest Framework
- Sqlite
- JWT Auth

# Sobre o Desenvolvimento
![clean-architecture-2](https://github.com/Richard-Dantas/niceplanet-challenge/assets/82357121/45eb4e88-2eaf-4da1-a31e-6df0d2b81955)

O projeto foi desenvolvido utilizando os pricípios de arquitetura limpa, onde se diz sobre fluxo, dependência e boas práticas

Abaixo segue toda a estrutura de pastas da aplicação:

```bash
src
├── core
│   ├── analiseHistorico
│   │   ├── application
│   │   │   └── use_cases
│   │   └── domain
│   │       ├── IRepository
│   ├── produtores
│   │   ├── application
│   │   │   └── use_cases
│   │   ├── domain
│   │   │   ├── IRepository
│   │   ├── infra
│   │   └── tests
│   │       ├── application
│   │       │   ├── integration
│   │       │   └── unit
│   │       ├── domain
│   │       └── infra
│   ├── propriedades
│   │   ├── application
│   │   │   └── use_cases
│   │   ├── domain
│   │   │   ├── IRepository
│   │   └── infra
│   └── vinculos
│       ├── application
│       │   └── use_cases
│       ├── domain
│       │   ├── IRepository
│       └── infra
└── django_project
    ├── analiseHistoricos_app
    │   └── migrations
    ├── produtores_app
    │   ├── fixtures
    │   ├── migrations
    │   └── tests
    ├── propriedades_app
    │   ├── fixtures
    │   └── migrations
    └── vinculos_app
        ├── fixtures
        └── migrations
```

Dentro de src/core é possível visualizar a camada mais interna do projeto, que o domínio. Dentro de domain são construídas as entidades, como analiseHistorico, produtores etc. e também ficam as abstrações dos repositórios. 
Isso implica em dizer nesse nível a dependência foi invertida, que é um dos princípios SOLID para desenvolvimento, e também foi utilizado o pattern Repository, que abstrai a camada de persistência e fornece uma interface para acessar os dados.
Apenas no contexto de Produtores foi possível implementar testes unitários para domain, application e infra(que é onde ficou a implementação de um repositório em memória para os testes) e também de integração. Os demais testes de integração ficaram no contexto do django
que será explicado em breve.

Dentro de application ficam os casos de uso/serviços que são utilizados para realizar as operações com as entidades de domínio.

Em infrastructe é onde fica a implementação das abstrações do repositories, poderiam ficar também configurações banco de dados e de mapeamentos de entidades
```bash
analiseHistorico
├── application
└── domain
produtores
├── application
├── domain
├── infra
└── tests
│   ├── application
│       ├── integration
│   │   └── unit
│   ├── domain
│   └── infra
propriedades
├── application
│   ├── domain
│   └── infra
vinculos
├── application
├── domain
└── infra
```
Em relação ao django_project há algumas coisas interessantes. Para não ter que realizar um dump, dentro de fixtures há o json referente ao contexto, que mesmo que o banco seja dropado, ao executar as migrações os dados serão inseridos automaticamente.

Dentro de cada _app há um arquivo repository.py que implementa a abstração dos repositories citada anteriormente, porém com um banco de dados real, e também arquivos serializers.py para facilitar o retorno dos jsons de cada requisição.

Normalmente quando utilizo outras linguagens, não gosto de fazer buscas por "RequestQuery", que passa por exemplo um id na url etc. pois as vezes isso pode expor alguma informação sensível, costumo optar pelo "Requestbody", apesar do verbo GET não suportar requisições
com informação no BODY, por isso acabo usando POST em alguns cenários de consulta, mas no contexto deste teste, todas as requisições de busca estão em uma rota GET.

```bash
└── django_project
    ├── analiseHistoricos_app
    │   └── migrations
    ├── produtores_app
    │   ├── fixtures
    │   ├── migrations
    │   └── tests
    ├── propriedades_app
    │   ├── fixtures
    │   └── migrations
    └── vinculos_app
        ├── fixtures
        └── migrations
```
Pontos a serem considerados:

  -  Optei por não utilizar IDs incrementais como foi passado no Json por email, estão sendo utilizados UUID

A motivação por trás disso é que eu acreditava que não me faltaria tempo e implementaria a API também em PHP, utilizando o mesmo banco de dados. Nesse caso não haveria risco de falha na criação de IDs caso eu executasse uma mesma operação de criação em duas APIs
diferentes, visto que UUID são únicos globalmente, e apesar de IDs incrementais serem mais performáticos, perdem um pouco em questão de segurança em relação ao UUID

# Os Testes

O projeto está contando com 45 testes, sendo eles unitários e de integração, validando desde asserção de conteúdos retornados até o código da resposta.

Para os testes foi utilizado o Padrão Given-When-Then, que os subdivide em 3 partes: Arrange(Preparar), Act(Agir), Assert(Verificar)

Em alguns testes esse padrão é mais visível do que em outros.

Para executa-los após tudo estar configurado, basta ir em testting no vccode e rodar

# Da Instalação e Execução

```bash
sudo apt install python3-pip
pip3 install virtualenv
virtualenv venv
```
```bash
pip install pytest
python -m pip install Django
pip install djangorestframework
pip install pytest-django
pip install djangorestframework-simplejwt
```

```bash
python manage.py makemigrations
python manage.py migrate
```

O comando abaixo é de suma importância. Todos os testes na camada mais externa da API necessitam de autenticação, visto o requisito "Faça autenticação do usuário para ter acesso aos dados;"

Então execute o comando abaixo e a partir do super usuário que você criar você conseguirá buscar o token pela rota /api/token/?Content-Type=application/json passando username e password no body da requisição, por exemplo:

{"username": "root", "password": "root"}

```bash
python manage.py createsuperuser
```

Com o token gerado (O Acess Token) basta colocar no header de cada requisição o "Authorization" com value "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA3MTE3NjM1LCJpYXQiOjE3MDcxMTczMzUsImp0aSI6Ijc5ZDA3NmE3NTlmOTQyZWU4OGY2YmJiMTUxYzhkNjExIiwidXNlcl9pZCI6MX0.d7W3_BIzN0f1uDnShiCtDm_wgtRRqapvh1whUI2S6fQ"
por exemplo. Caso contrário em todas as rotas terá um retorno 401

Por fim:

```bash
python manage.py runserver
```
se persistirem erros, segue a lista de todos os pacotes instalados no meu virtual env:
```bash
Package                       Version
----------------------------- -------
asgiref                       3.7.2
Django                        5.0.1
djangorestframework           3.14.0
djangorestframework-jwt       1.11.0
djangorestframework-simplejwt 5.3.1
iniconfig                     2.0.0
packaging                     23.2
pip                           23.3.1
pluggy                        1.4.0
PyJWT                         1.7.1
pytest                        8.0.0
pytest-django                 4.8.0
pytz                          2024.1
setuptools                    69.0.2
sqlparse                      0.4.4
wheel                         0.42.0
```

Agora com a adição do Swagger:

Acesse a rota /docs após ter executado o comando python manage.py runserver e já ter criado o superuser.
Em "Authorize" insira as credenciais do seu superuser e então você poderá utilizar as rotas normalmente.

O arquivo que continha a json do postman estava com o nome rotas.postman_collection e foi atualizado para rotas.json