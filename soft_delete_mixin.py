import sqlalchemy as sa

from query import SoftDeleteQuery


class SoftDeleteMixin:
    deleted = sa.Column(sa.Boolean(), default=False)

    query_class = SoftDeleteQuery
