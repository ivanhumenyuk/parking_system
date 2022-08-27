from typing import TYPE_CHECKING, List, NoReturn, Union

import sqlalchemy as sa
from flask_sqlalchemy import BaseQuery, Model
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Query, joinedload

if TYPE_CHECKING:
    from app import db


class MarketQuery(BaseQuery):
    """Mixin class for database queries."""

    def with_(self, relations: List[str]) -> Query:
        joins = [joinedload(rel) for rel in relations]
        return self.options(*joins)


class MarketQueryWithSoftDelete(MarketQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(MarketQueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted_at=None) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        from app import db

        return self.__class__(
            self._only_full_mapper_zero("get"), session=db.session(), _with_deleted=True
        )

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(MarketQueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.deleted_at else None


class MarketModel(Model):
    @declared_attr
    def id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, "__table__", None) is not None:
                _type = sa.ForeignKey(base.id)
                break
        else:
            _type = sa.Integer

        return sa.Column(_type, primary_key=True, autoincrement=True)

    @classmethod
    def insert_or_ignore(
        cls, objects: List[Union[dict, "db.Model"]], commit: bool = True
    ):
        from app import db

        insert_command = (
            insert(cls, bind=db.session)
            .values(
                [
                    obj
                    if type(obj) == dict
                    else {
                        c.name: getattr(obj, c.name)
                        for c in obj.__table__.columns
                        if getattr(obj, c.name) is not None
                    }
                    for obj in objects
                ]
            )
            .on_conflict_do_nothing()
        )

        # executing command
        db.session.execute(insert_command)
        if commit:
            db.session.commit()


class CreatedAtMixin:
    created_at = sa.Column(
        sa.DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
    )


class CreatedUpdatedAtMixin:
    created_at = sa.Column(
        sa.DateTime(timezone=True), default=func.now(), server_default=func.now()
    )
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
    )


class UpdatedAtMixin:
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
    )


class DeletedAtMixin:
    deleted_at = sa.Column(sa.DateTime(timezone=True))

    def soft_delete(self) -> NoReturn:
        self.deleted_at = func.now()


class CreatedDeletedAtMixin(CreatedAtMixin, UpdatedAtMixin):
    ...


class FullTimestampsMixin(CreatedUpdatedAtMixin, DeletedAtMixin):
    ...
