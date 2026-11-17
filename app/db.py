from sqlalchemy import create_engine 
from sqlalchemy.orm import DeclarativeBase , sessionmaker
# SQLAlchemy is a Python library for working with SQL databases, such as SQLite, PostgreSQL, and MySQL.


from app.config import settings

engine = create_engine(settings.database_url)
sessionLocal = sessionmaker(bind = engine)


class Base(DeclarativeBase):
    pass 


def get_db():
    db = sessionLocal()
    try:
        yield db
        # yield lets a route use the session during a request, then runs the cleanup afterward.
    finally:
        db.close()
        