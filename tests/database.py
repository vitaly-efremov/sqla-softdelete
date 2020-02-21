from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

DB_NAME = 'sqlite:///.test_database'
Session = scoped_session(sessionmaker())


class Entity:
    query: Query = Session.query_property(query_cls=Query)


meta = MetaData()
Base = declarative_base(metadata=meta, cls=Entity)
