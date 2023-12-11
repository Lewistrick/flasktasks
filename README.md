# Flasktasks

This is a REST API for a task list, written by Erick Wilts.

The API lets the user manipulate tasks that have a title, a description and a due_date. Manipulations include:
- Seeing a task
- Seeing a list of all tasks (including pagination)
- Creating a task
- Editing a task
- Deleting a task
- Searching for a task (including pagination and sorting)

## Installation

### Only the first time
- create a virtual environment and activate it:
    - `python -m venv .venv`
    - `.venv\Scripts\activate`
- install dependencies and set up the app:
    - `pip install poetry`
    - `poetry install`
- initialize the database (SQLite):
    - `yoyo apply`
    - `python create_fake_tasks.py` (this creates 100 tasks with random titles, descriptions and dates)

### Optional
- copy the `.env_example` to `.env` and change the configuration values if they need to be different
    - `DATABASE_LOCATION`: where the database file will be saved
    - `PAGE_SIZE`: the default number of tasks to show in get-all and search

### From the first time onward
- to run the app:
    - `flask run`
- to run tests:
    - `pytest` (only runs tests for the `database` module; this showcases my unit testing skills, while not consuming my limited assessment time)

## Endpoints
- GET `/tasks` shows all tasks
- GET `/tasks/<id>` (replace `<id>` with the task ID) shows task with given ID
- POST `/tasks` creates a task (payload must be Application/JSON with `title` and `due_date` fields, optional `description` field)
    - supports pagination (use parameters `page` (to specify page number) and `size` (to specify page length), e.g. `?page=2&size=10`); both are optional
- PATCH `/tasks/<id>` edits a task (payload optionally contains `title`, `due_date` and `description` and will only update given fields)
- DELETE `/tasks/<id>` deletes a task with given ID
- GET `/tasks/search/<query>` searches for all tasks that contain the exact string `<query>`
    - supports pagination (use parameters `page` (to specify page number) and `size` (to specify page length), e.g. `?page=2&size=10`; both are optional)
    - supports sorting (use parameters `sort` (to specify field to sort by) and `desc` (to sort in descending order), e.g. `?sort=due_date&desc=1`; `sort` is optional, `desc` does nothing if sort is not given)

## Details
This API uses the following libraries:
- `Flask` for the webapp
- `Flask-RESTful` for making it an API
    - because Flask is meant as a full-stack framework and this app only needs the REST API (i.e. backend).
- `SQLModel` for database models
    - because it greatly simplifies working with database models and it makes great use of the powerful SQLAlchemy engine
- `yoyo` for database migrations
    - because it is a simple framework that removes unnecessary SQL statements in the Python code, such as CREATE TABLE
- `pytest` for tests