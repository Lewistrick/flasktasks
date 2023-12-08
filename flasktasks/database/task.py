from datetime import datetime

from flask import abort
from loguru import logger
from sqlmodel import Field, Session, SQLModel, select

from flasktasks.config import settings
from flasktasks.database import engine


class TaskRecord(SQLModel, table=True):
    __tablename__ = "tasks"

    task_id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    due_date: str

    def create(self):
        """Create a task in the database. Returns the ID of the created task."""
        # Check if the due_date has the correct format
        logger.debug("Parsing date")
        try:
            datetime.strptime(self.due_date, settings.database_date_format)
        except ValueError:
            abort(422, f"Date could not be parsed: {self.due_date}")

        logger.debug("Creating session")
        with Session(engine) as session:
            logger.debug("Add")
            session.add(self)
            logger.debug("Commit")
            session.commit()
            logger.debug("Done")
            # The commit will create the task ID (auto-increment)
            return self.task_id


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
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
