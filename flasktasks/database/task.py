from sqlmodel import Field, Session, SQLModel, select

from flasktasks.database import engine


class TaskRecord(SQLModel, table=True):
    __tablename__ = "tasks"

    task_id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    due_date: str


def select_by_id(id: int):
    statement = select(TaskRecord).where(TaskRecord.task_id == id)
    with Session(engine) as session:
        return session.exec(statement).first()
