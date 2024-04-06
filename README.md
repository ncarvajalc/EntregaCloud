# Project - Cloud Software Development

This is a FastAPI project initialized using [`create-fastapi-project`](https://github.com/allient/create-fastapi-project), designed to provide a quick start for building APIs with [FastAPI](https://fastapi.tiangolo.com/).

It was modified to use in the Cloud Software Development course at Universidad de los Andes.

## Getting Started

> **Note:** Before running the project, make sure you have installed [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

The commands in this documentation can be customized on the **Makefile**. It uses docker to run the services.

- Setup development environment:

```bash
# Install virtual environment for auto-completion
make setup
```

You should change the python interpreter in your IDE to the one in the virtual environment.

- Run the server:

```bash
# Run locally with docker in dev mode and force build
make run-dev-build
# or
# Run locally with docker in dev mode
make run-dev
# or
# Run locally with docker in prod mode (Autorelod disabled)
make run-prod
```

Open [http://localhost/docs](http://localhost/docs) with your browser to see the result.

- Clean the environment:

```bash
# Clean the environment. This will delete the virtual environment and python cache
make clean
```

## Learn More

To learn more about Fastapi, take a look at the following resources:

- [Fastapi Documentation](https://fastapi.tiangolo.com/).
- [asyncer-tutorial](https://asyncer.tiangolo.com/tutorial/).
