from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

DB_NAME = 'sqlite:///.test_database'

meta = MetaData()
Base = declarative_base(metadata=meta)
