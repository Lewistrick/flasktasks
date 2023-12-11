# Flasktasks

> This is a REST API for a task list.

## Installation
- create a virtual environment and activate it:
    - `python -m venv .venv`
    - `.venv\Scripts\activate`
- install dependencies and set up the app:
    - `pip install poetry`
    - `poetry install`
- initialize the database:
    - `yoyo apply`
    - `python create_fake_tasks.py` (this creates 100 tasks with random titles, descriptions and dates)
- to run the app:
    - `flask run`

## Details
This API uses the following libraries:
- `Flask` for the webapp
- `flask-restful` for making it an API
    - because Flask is meant as a full-stack framework and this app only needs the REST API (i.e. backend).
- `SQLModel` for database models
    - because it greatly simplifies working with database models and it makes great use of the powerful SQLAlchemy engine
- `yoyo` for database migrations
    - because it is a simple framework that removes unnecessary SQL statements in the Python code, such as CREATE TABLE