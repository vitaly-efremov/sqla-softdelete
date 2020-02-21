import pytest
from sqlalchemy.orm.exc import ObjectDeletedError

from tests.conftest import Account


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
def test_get_all_not_deleted(dbsession):
    # Arrange
    account1 = Account(name='account1')
    account2 = Account(name='account2')
    account1.delete()

    dbsession.add_all([account1, account2])
    dbsession.flush()

    # Act
    actual_accounts = dbsession.query(Account).all()

    # Assert
    assert actual_accounts == [account2]


@pytest.mark.db
def test_filter_not_deleted(dbsession):
    # Arrange
    account1 = Account(name='account1')
    account2 = Account(name='account2')
    account3 = Account(name='account2')
    account1.delete()

    dbsession.add_all([account1, account2, account3])
    dbsession.flush()

    # Act
    actual_accounts = dbsession.query(Account).filter(Account.name == 'account2').all()

    # Assert
    assert actual_accounts == [account2, account3]


@pytest.mark.db
def test_get_not_deleted(dbsession):
    # Arrange
    account = Account(name='account')

    dbsession.add(account)
    dbsession.flush()

    # Act
    actual_account = dbsession.query(Account).get(account.id)

    # Assert
    assert actual_account == account


@pytest.mark.db
def test_get_deleted(dbsession):
    # Arrange
    account = Account(name='account')
    account.delete()

    dbsession.add(account)
    dbsession.flush()
    dbsession.expire(account)

    # Act & Assert
    with pytest.raises(ObjectDeletedError):
        dbsession.query(Account).get(account.id)
