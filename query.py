from sqlalchemy.orm import Query


class SoftDeleteQuery(Query):
    def __new__(cls, *args, **kwargs):
        obj = super(SoftDeleteQuery, cls).__new__(cls)
        if len(args) > 0:
            super(SoftDeleteQuery, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False)
        return obj
