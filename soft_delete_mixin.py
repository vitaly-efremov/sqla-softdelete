import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.orm import Query


class SoftDeleteMixin:
    deleted = sa.Column(sa.Boolean(), default=False)


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
                entity.deleted.is_(False),
            )

    return query


@event.listens_for(SoftDeleteMixin, 'load', propagate=True)
def load(obj, context):
    include_deleted = context.query._execution_options.get('include_deleted', False)
    if obj.deleted and not include_deleted:
        raise TypeError(f'Deleted object {obj} was loaded, did you use joined eager loading?')
