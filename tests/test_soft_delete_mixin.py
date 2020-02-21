import pytest
import sqlalchemy as sa

from .database import Base


class Account(Base):
    __tablename__ = 'account'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.String(128), nullable=False, index=True)
    phone = sa.Column(sa.String(128))

    def __init__(self, name: str = '', email: str = '', phone: str = ''):
        self.name = name
        self.email = email
        self.phone = phone


@pytest.mark.db
def test_mixin(dbsession):
    # Arrange
    account1 = Account(name='account1')
    account2 = Account(name='account2')

    dbsession.add_all([account1, account2])
    dbsession.flush()

    # Act
    actual_accounts = dbsession.query(Account).all()

    # Assert
    assert set(actual_accounts) == {account1, account2}
