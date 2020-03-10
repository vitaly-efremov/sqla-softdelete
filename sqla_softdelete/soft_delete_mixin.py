from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.orm import Query


class SoftDeleteMixin:
    deleted_at = sa.Column(sa.DateTime(timezone=True), nullable=True)

    def delete(self, deleted_at: datetime = None):
        self.deleted_at = deleted_at or datetime.now()

    def restore(self):
        self.deleted_at = None


@event.listens_for(Query, 'before_compile', retval=True)
def before_compile(query):
    include_deleted = query._execution_options.get('include_deleted', False)
    if include_deleted:
        return query

    for column in query.column_descriptions:
        entity = column['entity']
        if entity is None:
            continue

        inspector = inspect(column['entity'])
        mapper = getattr(inspector, 'mapper', None)
        if mapper and issubclass(mapper.class_, SoftDeleteMixin):
            query = query.enable_assertions(False).filter(
                entity.deleted_at.is_(None),
            )

    return query


@event.listens_for(SoftDeleteMixin, 'load', propagate=True)
def load(obj, context):
    include_deleted = context.query._execution_options.get('include_deleted', False)
    if obj.deleted_at and not include_deleted:
        raise TypeError(f'Deleted object {obj} was loaded, did you use joined eager loading?')
