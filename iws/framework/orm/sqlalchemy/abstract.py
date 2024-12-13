#
# Author: Rohtash Lakra
#
from enum import unique, auto
from math import ceil

from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from framework.enums import AutoUpperCase


@unique
class EntityOperation(AutoUpperCase):
    """Entity Operations"""
    DELETED = auto()
    INSERTED = auto()
    LOADED = auto()
    UPDATED = auto()


class Pagination(object):
    """Pagination Class is returned by `Query.paginate`. You can also construct it from any other SQLAlchemy query
    object if you are working with other libraries. Additionally, it is possible to pass ``None`` as query object in
    which case the `prev` and `next` will no longer work.

    """

    def __init__(self, query, page: int, page_size: int, total: int, items):
        #: The query object that was used to create this pagination object.
        self.query = query
        #: The current page number (1 indexed).
        self.page = page
        #: The number of items to be displayed on a page.
        self.page_size = page_size
        #: The total number of items matching the query.
        self.total = total
        #: The items for the current page.
        self.items = items
        if self.page_size == 0:
            self.pages = 0
        else:
            #: The total number of pages.
            self.pages = int(ceil(self.total / float(self.page_size)))
        #: Number of the previous page.
        self.prev_page = self.page - 1
        #: True if a previous page exists.
        self.has_prev = self.page > 1
        #: Number of the next page.
        self.next_page = self.page + 1
        #: True if a next page exists.
        self.has_next = self.page < self.pages

    def prev(self, throw_error: bool = False):
        """Returns a `Pagination` object for the previous page."""
        assert self.query is not None, 'a query object is required for this method to work'
        return self.query.paginate(self.page - 1, self.page_size, throw_error)

    def next(self, throw_error: bool = False):
        """Returns a `Pagination` object for the next page."""
        assert self.query is not None, 'a query object is required for this method to work'
        return self.query.paginate(self.page + 1, self.per_page, throw_error)


class BaseQuery(orm.Query):
    """The query class is either SQLAlchemy’s orm.Query class or a child class that inherits from it.
    The query property is what allows the 'Model.query' style access and is easy to create, but does require access to
    the database session when setting up.

    The default query object used for models. This can be subclassed and replaced for individual models by setting
    the 'Model.query_class' attribute. This is a subclass of a standard SQLAlchemy 'sqlalchemy.orm.query.Query' class,
    and has all the methods of a standard query as well.
    """

    def paginate(self, page: int, page_size: int = 20, throw_error: bool = True):
        """Return `Pagination` instance using already defined query parameters.
        """
        if throw_error and page < 1:
            raise IndexError

        if page_size is None:
            page_size = self.DEFAULT_PER_PAGE

        items = self.page(page, page_size).all()
        if not items and page != 1 and throw_error:
            raise IndexError

        # No need to count if we're on the first page and there are fewer items than we expected.
        if page == 1 and len(items) < page_size:
            total = len(items)
        else:
            total = self.order_by(None).count()

        return Pagination(self, page, page_size, total, items)


class QueryProperty(object):
    """Query property accessor which gives the model access to query capabilities via `BaseModel.query` which is
    equivalent to ``session.query(Model)``.

    For the query property functionality, we need to define this query property class.
    """

    def __init__(self, session):
        self.session = session

    def __get__(self, model, AbstractEntity):
        mapper = orm.class_mapper(AbstractEntity)
        if mapper:
            if not getattr(AbstractEntity, 'query_class', None):
                AbstractEntity.query_class = BaseQuery
            query_property = AbstractEntity.query_class(mapper, session=self.session())

            return query_property


def set_query_property(model_class, session):
    """A helper method for attaching the query property to the model."""
    model_class.query = QueryProperty(session)


class BaseModel(object):
    """Baseclass for custom user models."""

    # the query class used. The `query` attribute is an instance of this class. By default, a `BaseQuery` is used.
    query_class = BaseQuery

    # an instance of `query_class`. Can be used to query the database for instances of this model.
    query = None


class Auditable(object):
    """Auditable Entity"""
    pass


class BaseEntity(Auditable):
    """AbstractEntity Entity"""

    # the query class used. The `query` attribute is an instance of this class. By default, a `BaseQuery` is used.
    query_class = BaseQuery

    # an instance of `query_class`. Can be used to query the database for instances of this model.
    query = None


"""
Create the declarative base. This will become the common source for all future SQLAlchemy classes.
For example:
from .abstract import Model
class User(Model):
    # define user model
    pass

"""
# Model = declarative_base(cls=BaseModel)
AbstractEntity = declarative_base(cls=BaseEntity)


class NamedEntity(AbstractEntity):
    """NamedEntity Entity"""
    pass
