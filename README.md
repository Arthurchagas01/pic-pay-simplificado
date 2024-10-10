
# PicPay Simplificado

O projeto consiste na resolução de um processo seletivo do PicPay Back-end no qual era solicitado que se simulasse um "sistema PicPay simplificado". 

# O que foi solicitado na descrição do processo

Na descrição do processo, foi descrito o funcionamento de algumas funções e tarefas básicas que o script deveria fazer, tais como: 

* Para ambos tipos de usuário, precisamos do Nome Completo, CPF, e-mail e Senha. CPF/CNPJ e e-mails devem ser únicos no sistema. Sendo assim, seu sistema deve permitir apenas um cadastro com o mesmo CPF ou endereço de e-mail;

* Usuários podem enviar dinheiro (efetuar transferência) para lojistas e entre usuários;

* Lojistas só recebem transferências, não enviam dinheiro para ninguém;

* Validar se o usuário tem saldo antes da transferência;

* Antes de finalizar a transferência, deve-se consultar um serviço autorizador externo, use este mock https://util.devi.tools/api/v2/authorize para simular o serviço utilizando o verbo GET;

* A operação de transferência deve ser uma transação (ou seja, revertida em qualquer caso de inconsistência) e o dinheiro deve voltar para a carteira do usuário que envia;

* Este serviço deve ser RESTFul.

Todas essas tarefas foram feitas e testadas. Apenas uma que não foi incluída acima e ela era relativa ao mock de notificação que não está funcionando e não foi inserida.

Obs: Esses itens acima foram retirados do próprio processo conforme link no campo Referência.

# Tecnologias e bibliotecas utilizadas

Para criar o projeto nos moldes que foi solicitado, foi utilizado a linguagem Python com a utilização de um ambiente venv com as bibliotecas abaixo que foram necessárias para o funcionamento adequado:

* alembic            1.13.3
* annotated-types    0.7.0
* anyio              4.6.0
* certifi            2024.8.30
* charset-normalizer 3.3.2
* click              8.1.7
* colorama           0.4.6
* fastapi            0.115.0
* greenlet           3.1.1
* h11                0.14.0
* httpcore           1.0.6
* httpx              0.27.2
* idna               3.10
* iniconfig          2.0.0
* Mako               1.3.5
* MarkupSafe         2.1.5
* packaging          24.1
* pip                24.2
* pluggy             1.5.0
* psycopg2           2.9.9
* pydantic           2.9.2
* pydantic_core      2.23.4
* pytest             8.3.3
* pytest-asyncio     0.24.0
* requests           2.32.3
* sniffio            1.3.1
* SQLAlchemy         2.0.35
* starlette          0.38.6
* typing_extensions  4.12.2
* urllib3            2.2.3
* uvicorn            0.30.6


# Desafios

Durante o projeto existiram alguns desafios que foram necessárias algumas decisões para o bom funcionamento da aplicação, permitindo que as relações entre os usuários e as transações fossem possíveis e também na criação das rotas das APIs.

O primeiro desafio foi na criação das tabelas de Usuário (users) e Transações (transactions): era necessário criar um relacionamento entre as partes tal que um usuário poderia efetivar várias transações, no entanto, cada transação só poderiam ter dois usuários distintos, ou seja, o usuário não poderia enviar pra ele mesmo. 

Assim, foi criado na tabela de Transações 4 entradas que representariam o relacionamento com a chave estrageira (foreign_key) de forma que seria o formato Many-to-one (muitos-para-um).

O segundo desafio foi relativo as decisões sobre como seria informado se o usuário é uma pessoa física ou jurídica. Uma variável booleana user_store, com o sentido de "usuario_loja", se tornou a solução para representar a loja. Se a variável for colocada como True, será entendido como uma loja, caso contrário, se for False, será entendido como um usuário pessoa física.

O último desafio ocorreu durante o desenvolvimento das notificações, pois foi informado na descrição do projeto que deveria ser utilizado um mock para simular o envio de notificação, no entanto, foi tomado a decisão de utilizar apenas o retorno da função com as informações em um json para confirmação. O mock informado não respondia aos comandos e foi mais prático seguir dessa forma. 

No entanto, caso queira utilizar no projeto, basta retirar o "#" das linhas que validam se o retorno do mock foi 200 e isso deverá torná-lo usável no projeto. O arquivo é o notification_service.py.





# Documentação da API

## Api relativa aos usuários criados (users)

#### Retorna todos os itens:
### Função: get_all_users()

```http
  GET /users/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `N/A` | `N/A` | Retorna todos os usuários criados |

#### Cria um usuário (user):
### Função: create_new_user(new_user)

```http
  POST /users/
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `first_name`      | `string` | **Obrigatório**. O nome do usuário|
| `last_name`      | `string` | **Obrigatório**. O sobrenome do usuário |
| `document`      | `string` | **Obrigatório**. O CPF/CNPJ do usuário e este será validado se é único |
| `email`      | `string` | **Obrigatório**. O email do usuário e este será validado se é único |
| `password`      | `string` | **Obrigatório**. A senha do usuário |
| `balance`      | `integer` | **Obrigatório**. O saldo do usuário |
| `user_store`      | `boolean` | **Obrigatório**. Se o usuário é PF ou PJ |

Obs: Ao criar um usuário, é gerado um id e esse id é utilizado como sender_id no caso de envio de recurso e receiver_id, caso o usuário receba recurso nos próximos itens.

## Api relativa as transações criadas (transactions)

#### Retorna todos as transações enviadas por usuário (user_id):
### Função: get_transactions_sent(user_id)

```http
  GET /transactions/sent/{user_id}
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `user_id` | `integer` | **Obrigatório**. Retorna todos as transações que foram enviadas pelo usuário|

#### Retorna todos as transações recebidas por usuário (user_id):
### Função: get_transactions_received(user_id)

```http
  GET /transactions/received/{user_id}
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `user_id` | `integer` | **Obrigatório**. Retorna todos as transações que foram recebidas pelo usuário |

#### Cria uma transação que será enviada por um usuário que possui saldo para efetuar essa transferência e que não seja PJ e recebida por outro:
### Função: get_transactions_received(user_id)

```http
  POST /transactions/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `amount` | `integer` | **Obrigatório**. Valor que será transferido |
| `sender_id` | `integer` | **Obrigatório**. Usuário que enviará o recurso |
| `receiver_id` | `integer` | **Obrigatório**. Usuário que receberá o recurso |

Obs: PJ só recebe dinheiro e não envia.
# Rodando os testes

Para rodar os testes, rode o seguinte comando

```bash
  pytest
```


# Referência

 - [Desafio Back-end PicPay](https://github.com/PicPay/picpay-desafio-backend?tab=readme-ov-file)

- [Pytest - Good Integration Practices](https://docs.pytest.org/en/latest/explanation/goodpractices.html#test-package-name)

- [SQLAlchemy ORM - Building Relationship](https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_building_relationship.htm)

- [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
