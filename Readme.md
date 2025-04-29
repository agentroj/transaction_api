# Transaction Management API

**Author:** Rogelio “Roj” Padida Jr.

A simple RESTful API for creating and retrieving transactions using Django & DRF, backed by SQLite.

## Requirements

- Docker & Docker-Compose (for containerized)
- Python 3.8+ (for local)

## Quickstart with Docker

```bash
git clone <your-repo-url> transaction_api
cd transaction_api
docker-compose up --build
```
API will be available at `http://localhost:8000/transactions/`

## Local Setup Without Docker

```bash
git clone <your-repo-url> transaction_api
cd transaction_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoints

| Method | URL                    | Description                 |
| ------ | ---------------------- | --------------------------- |
| POST   | `/transactions/`       | Create new transaction      |
| GET    | `/transactions/`       | List all transactions       |
| GET    | `/transactions/{id}/`  | Retrieve single transaction |

## Validation Rules

- `amount` must be positive (> 0)  
- `transaction_type` must be `DEPOSIT` or `WITHDRAWAL`

## Running Tests

```bash
pytest
# or
python manage.py test
```