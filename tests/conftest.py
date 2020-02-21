import pytest
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from soft_delete_mixin import SoftDeleteMixin
from .database import Base
from .database import DB_NAME


class Account(Base, SoftDeleteMixin):
    __tablename__ = 'account'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.String(128), nullable=False, index=True)

    def __init__(self, name: str = '', email: str = '', phone: str = ''):
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f'Account(id={self.id}, name={self.name}, email={self.email})'

    def __str__(self):
        return f'{self.name}: {self.email})'


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
