# sqla-softdelete
Simple soft delete for SQLAlchemy ORM

How to install
------------  
```
  pip install -r sqla-softdelete
```

How to use
------------    
To make your SQLAlchemy model (entity) support just inherit it from `SoftDeleteMixin`. 
For instance:
```python
from sqla_softdelete import SoftDeleteMixin


class Account(SoftDeleteMixin, Base):
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
```

All set now.
```python
    account = Account(name='account')
    
    Session.add(account)
    Session.flush()
    
    account.delete()
    Session.expire(account)

    actual_accounts = dbsession.query(Account).all() 
    print(f'Actual accounts: {actual_accounts}')
```