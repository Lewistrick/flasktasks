from datetime import datetime

from flask import abort
from loguru import logger
from pydantic import ValidationError, field_validator
from sqlmodel import Field, Session, SQLModel, select

from flasktasks.config import settings
from flasktasks.database import engine


class TaskRecord(SQLModel, table=True):
    __tablename__ = "tasks"

    task_id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = ""
    due_date: str

    def create(self):
        """Create a task in the database. Returns the ID of the created task."""
        with Session(engine) as session:
            session.add(self)
            try:
                # Make sure the updates conform to the validation;
                # this is possible because SQLModel uses pydantic for data validation
                self.model_validate(self)
            except ValidationError as e:
                # No harm is done here: the session has not been committed
                abort(422, e)
            session.commit()
            # The commit will create the task ID (auto-increment)
            return self.task_id

    @field_validator("due_date")
    def validate_due_date(cls, due_date):
        """Check if the due_date has the correct format."""
        try:
            datetime.strptime(due_date, settings.database_date_format)
        except ValueError:
            raise ValueError(f"Date could not be parsed: {due_date}")
        return due_date


def select_all_tasks():
    """Select all tasks from the database."""
    statement = select(TaskRecord)
    with Session(engine) as session:
        return session.exec(statement).all()


def select_by_id(task_id: int):
    """Select one task from the database, given its ID.

    If the task doesn't exist, return None.
    """
    statement = select(TaskRecord).where(TaskRecord.task_id == task_id)
    with Session(engine) as session:
        return session.exec(statement).first()


def delete_by_id(task_id: int):
    """Delete one task from the database, given an ID.

    Return True if the task exists, False otherwise.
    """
    task = select_by_id(task_id)
    if task is None:
        return False

    with Session(engine) as session:
        session.delete(task)
        session.commit()

    return True


def update_by_id(task_id: int, **changes):
    """Update one task in the database, given an ID.

    Return True if the task exists, False otherwise.
    """
    task = select_by_id(task_id)
    if task is None:
        return None
    with Session(engine) as session:
        for attribute, new_value in changes.items():
            logger.info(f"Setting '{attribute}' of task {task_id} to {new_value}")
            setattr(task, attribute, new_value)

        try:
            # Make sure the updates conform to the validation;
            # this is possible because SQLModel uses pydantic for data validation
            task.model_validate(task)
        except ValidationError as e:
            # No harm is done here: the session has not been committed
            abort(422, e)

        session.add(task)
        session.commit()
        session.refresh(task)
        return task


def search_by_query(query: str, sort_by: str | None = None, sort_desc: bool = False):
    """Search tasks by query.

    The query is a text that should be contained completely within the description or
    the title of the text.

    If sort_by is given, sort by this value; if sort_desc is True, sort descending.

    It's not possible to use string searching operations in SQLModel statements, so a
    statement is created that selects all tasks and then uses Python-native string
    operations to search in the description and the title.
    Using the yield_per(100) generator makes sure that this will not become too
    memory-heavy, but also doesn't put a too heavy load on the database engine.
    """
    statement = select(TaskRecord)
    if sort_by:
        try:
            sort_column = getattr(TaskRecord, sort_by)
        except AttributeError:
            abort(404, f"Can't sort by column {sort_by}: column doesn't exist")

        if sort_desc:
            sort_column = sort_column.desc()
        statement = statement.order_by(sort_column)

    with Session(engine) as session:
        for task in session.exec(statement).yield_per(100):
            if query in task.description or query in task.title:
                yield task
