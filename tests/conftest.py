import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .database import Base
from .database import DB_NAME


@pytest.fixture(scope='session')
def engine():
    return create_engine(DB_NAME)


@pytest.yield_fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.yield_fixture
def dbsession(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
