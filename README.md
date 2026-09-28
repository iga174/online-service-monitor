# Online Service Monitor

A simple REST API for monitoring web services and tracking their availability and response times.

The application periodically checks registered services, stores the results in a SQLite database, and provides statistics about their performance.

## Features

* Add, update and delete monitored services
* Check service availability and response time
* Store results in SQLite
* View previous service checks
* Calculate response time statistics
* Calculate service availability
* Automatic service checks every 60 seconds
* REST API built with FastAPI
* Docker support
* Automated tests with Pytest

## Tech Stack

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **SQLite**
* **HTTPX**
* **Pytest**
* **Docker**

## API Endpoints

| Method | Endpoint                    | Description               |
| ------ | --------------------------- | ------------------------- |
| GET    | `/`                         | Get all services          |
| POST   | `/services`                 | Add a new service         |
| GET    | `/service/{id}`             | Get a specific service    |
| PATCH  | `/services/{id}`            | Update a service          |
| DELETE | `/services/{id}`            | Delete a service          |
| POST   | `/services/{id}/check`      | Check a service           |
| GET    | `/services/{id}/checks`     | Get service check history |
| GET    | `/services/{id}/statistics` | Get service statistics    |

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/iga174/online-service-monitor.git
cd online-service-monitor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the API

```bash
uvicorn app.main:app
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation is available at:

```text
http://localhost:8000/docs
```

## Running with Docker

Build the Docker image:

```bash
docker build -t python-monitor .
```

Run the container:

```bash
docker run -p 8000:8000 python-monitor
```

The API will then be available at:

```text
http://localhost:8000
```

## Running Tests

Run all tests with:

```bash
pytest
```

The tests use a separate in-memory SQLite database.

## Project Structure

```text
online-service-monitor/
├── app/
│   ├── checks.py
│   ├── database.py
│   ├── database_models.py
│   ├── main.py
│   ├── schemas.py
│   ├── services.py
│   └── statistics.py
├── tests/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Database

The application uses SQLite for data storage.

The local database file is excluded from Git using `.gitignore`.

## License

This project is for learning and portfolio purposes.

