# Intouch

This repository contains a Flask application named `Intouch` that uses PostgreSQL as its database. This application is Dockerized for easy development and deployment.

## Requirements

- Docker
- Docker Compose

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/intouch.git
    cd intouch
    ```

2. **Build and start the Docker containers:**

    ```bash
    docker-compose up --build -d
    ```

    The `-d` flag will run the containers in the background. You can also omit this flag to run it in the foreground and view logs.

## Accessing the Containers

### Intouch Application

  The `Intouch` Flask application will be running on <http://localhost:5005>.

### PostgreSQL Database

The PostgreSQL instance will be accessible at `localhost:5432` (or whichever port you specify in the `docker-compose.yml`).

### Logs and Shell

1. **View logs:**

    - Intouch: `docker-compose logs intouch`
    - PostgreSQL: `docker-compose logs postgres`

2. **Open a shell inside the containers:**

    - Intouch: `docker-compose exec intouch /bin/bash`
    - PostgreSQL: `docker-compose exec postgres psql -U in intouchdb`
