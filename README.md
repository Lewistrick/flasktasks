# Flasktasks

> This is a REST API for a task list.

## Installation
- to install dependencies and set up the app: `poetry install --without dev`
- to initialize the database: `yoyo apply`
- to run the app: `run flask`

## Details
This API uses the following libraries:
- `Flask` for the webapp
- `flask-restful` for making it an API
    - because Flask is meant as a full-stack framework and this app only needs the REST API (i.e. backend).
- `SQLModel` for database models
    - because it greatly simplifies working with database models and it makes great use of the powerful SQLAlchemy engine
- `yoyo` for database migrations
    - because it is a simple framework that removes unnecessary SQL statements in the Python code, such as CREATE TABLE