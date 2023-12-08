from sqlmodel import SQLModel, create_engine

from flasktasks.config import settings

engine = create_engine(settings.database_connection_string)
SQLModel.metadata.create_all(engine)
