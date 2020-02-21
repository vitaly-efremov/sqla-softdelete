import pytest
import sqlalchemy as sa

from soft_delete_mixin import SoftDeleteMixin
from .database import Base


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


@pytest.mark.db
def test_query_all(dbsession):
    # Arrange
    account1 = Account(name='account1')
    account2 = Account(name='account2')

    dbsession.add_all([account1, account2])
    dbsession.flush()

    # Act
    actual_accounts = dbsession.query(Account).all()

    # Assert
    assert set(actual_accounts) == {account1, account2}


@pytest.mark.db
def test_entity_query_filter_not_deleted(dbsession):
    # Arrange
    account1 = Account(name='account1')
    account2 = Account(name='account2')
    account1.deleted = True

    dbsession.add_all([account1, account2])
    dbsession.flush()

    # Act
    actual_accounts = Account.query.all()

    # Assert
    assert actual_accounts == [account2]


@pytest.mark.db
def test_session_query_filter_not_deleted(dbsession):
    # Arrange
    account1 = Account(name='account1')
    account2 = Account(name='account2')
    account1.deleted = True

    dbsession.add_all([account1, account2])
    dbsession.flush()

    # Act
    actual_accounts = dbsession.query(Account).all()

    # Assert
    assert actual_accounts == [account2]
