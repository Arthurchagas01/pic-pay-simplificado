# Simplified PicPay

This project is a solution for the PicPay Back-end selection process, which required simulating a "simplified PicPay system."

## Requirements from the Selection Process

The process description outlined the basic functions and tasks the script should perform, including:

- Both user types must provide full name, CPF, email, and password. CPF/CNPJ and emails must be unique in the system. Only one registration per CPF or email address is allowed.
- Users can send money (transfer funds) to merchants and between users.
- Merchants can only receive transfers; they cannot send money.
- Validate if the user has sufficient balance before processing the transfer.
- Before finalizing the transfer, an external authorization service must be consulted. Use this mock service: https://util.devi.tools/api/v2/authorize (via GET request).
- The transfer operation must be transactional (i.e., reversed in case of any inconsistency), ensuring that funds return to the sender's wallet if an issue occurs.
- The service must be RESTful.

All these tasks were implemented and tested. The only exception was the notification mock service, which was not working and therefore not included.

**Note:** The above items were extracted directly from the selection process description, as referenced in the "References" section.

## Technologies and Libraries Used

To develop the project according to the specifications, a monolithic architecture was used with Python and a virtual environment (venv). The following libraries were necessary for proper functionality, along with PostgreSQL as the database:

- FastAPI
- SQLAlchemy
- Alembic
- Psycopg2
- HTTPX
- Pytest
- Uvicorn

## Challenges Faced

Several challenges arose during the project that required careful decision-making to ensure proper application functionality and user-transaction relationships, as well as API route structuring.

### User and Transaction Table Relationships

The first challenge was designing the relationship between the Users (`users`) and Transactions (`transactions`) tables. A user could perform multiple transactions, but each transaction should always involve two distinct users—meaning a user could not transfer money to themselves.

To address this, the Transactions table was designed with four entries to represent foreign key relationships, implementing a **many-to-one** format.

### User Type Identification

The second challenge was determining how to distinguish between individual users (PF) and merchants (PJ). A boolean field `user_store` (indicating "is a merchant") was introduced:
- If `user_store = True`, the user is a merchant (PJ).
- If `user_store = False`, the user is an individual (PF).

### Notification Mock Issues

The final challenge was implementing notifications. The project description specified using a mock service for notification simulation. However, this mock service was unresponsive, so an alternative approach was taken: the function simply returns a JSON confirmation.

To enable the notification mock, remove the `#` comments from the lines that validate if the mock service response is `200`. The relevant file is `notification_service.py`.

## API Documentation

### Users API

#### Retrieve All Users
**Endpoint:** `GET /users/`

| Parameter  | Type | Description |
|------------|------|-------------|
| N/A        | N/A  | Returns all registered users |

#### Create a New User
**Endpoint:** `POST /users/`

| Parameter      | Type     | Description |
|---------------|---------|-------------|
| `first_name`  | string  | **Required**. User's first name |
| `last_name`   | string  | **Required**. User's last name |
| `document`    | string  | **Required**. User's CPF/CNPJ (validated as unique) |
| `email`       | string  | **Required**. User's email (validated as unique) |
| `password`    | string  | **Required**. User's password |
| `balance`     | integer | **Required**. User's initial balance |
| `user_store`  | boolean | **Required**. Defines if user is a merchant (PJ) or individual (PF) |

### Transactions API

#### Retrieve All Transactions Sent by a User
**Endpoint:** `GET /transactions/sent/{user_id}`

| Parameter  | Type     | Description |
|------------|---------|-------------|
| `user_id`  | integer | **Required**. Returns all transactions sent by the user |

#### Retrieve All Transactions Received by a User
**Endpoint:** `GET /transactions/received/{user_id}`

| Parameter  | Type     | Description |
|------------|---------|-------------|
| `user_id`  | integer | **Required**. Returns all transactions received by the user |

#### Create a Transaction
**Endpoint:** `POST /transactions/`

| Parameter     | Type     | Description |
|--------------|---------|-------------|
| `amount`     | integer | **Required**. Transfer amount |
| `sender_id`  | integer | **Required**. User sending the funds |
| `receiver_id`| integer | **Required**. User receiving the funds |

**Note:** Merchants (PJ) can only receive money and cannot send funds.

## Running Tests

To run the tests, use the following command:
```bash
pytest
```

## References

- [PicPay Back-end Challenge](https://github.com/PicPay/picpay-desafio-backend?tab=readme-ov-file)
- [Pytest - Best Practices](https://docs.pytest.org/en/latest/explanation/goodpractices.html#test-package-name)
- [SQLAlchemy ORM - Relationship Building](https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_building_relationship.htm)
- [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)

