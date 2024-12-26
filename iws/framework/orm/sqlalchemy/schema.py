#
# Author: Rohtash Lakra
#
# References: -
# - https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# - https://docs.sqlalchemy.org/en/20/orm/inheritance.html
#
import logging
from datetime import datetime
from enum import unique, auto
from math import ceil

from sqlalchemy import func, orm, String, event
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

from framework.enums import AutoUpperCase

logger = logging.getLogger(__name__)


@unique
class SchemaOperation(AutoUpperCase):
    """Entity Operations"""
    # Adds new data or records to the database
    CREATE = auto()
    # Removes data from the database
    DELETE = auto()
    # Retrieves data from the database
    READ = auto()
    # Modifies existing data in the database
    UPDATE = auto()


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

    def __init__(self):
        # super().__init__(entities=None)
        self.DEFAULT_PER_PAGE = 20

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

    def __get__(self, model, AbstractSchema):
        mapper = orm.class_mapper(AbstractSchema)
        if mapper:
            if not getattr(AbstractSchema, 'query_class', None):
                AbstractSchema.query_class = BaseQuery
            query_property = AbstractSchema.query_class(mapper, session=self.session())

            return query_property


def set_query_property(model_class, session):
    """A helper method for attaching the query property to the model."""
    model_class.query = QueryProperty(session)


class Auditable(object):
    """Auditable Entity"""
    __abstract__ = True


class AbstractSchema(Auditable):
    """
    AbstractSchema define module-level constructs that will form the structures which we will be querying from the
    database. This structure, known as a Declarative Mapping, defines at once both a Python object model, and database
    metadata that describes real SQL tables that exist, or will exist, in a particular database:

    The mapping starts with a base class, which above is called 'AbstractSchema', and is created by making a simple
    subclass against the 'DeclarativeBase' class.

    Individual mapped classes are then created by making subclasses of 'AbstractSchema'.
    A mapped class typically refers to a single particular database table, the name of which is indicated by using
    the '__tablename__' class-level attribute.

    Normally, when one would like to map two different subclasses to individual tables, and leave the base class
    unmapped, this can be achieved very easily. When using Declarative, just declare the base class with
    the '__abstract__' indicator:
    """
    __abstract__ = True

    """
    ID - Primary Key
    
    All ORM mapped classes require at least one column be declared as part of the primary key, typically by using
    the 'Column.primary_key' parameter on those 'mapped_column()' objects that should be part of the key.
    """
    # primary_key=True, therefore will be NOT NULL
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # not Optional[], therefore will be NOT NULL
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    # not Optional[], therefore will be NOT NULL
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __init__(self, **kwargs):
        """
        Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
        A constructor similar to that supplied by Declarative is illustrated:
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def set_attrs(self, **kwargs):
        """
        Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
        A constructor similar to that supplied by Declarative is illustrated:
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])

    # the query class used. The `query` attribute is an instance of this class. By default, a `BaseQuery` is used.
    query_class = BaseQuery

    # an instance of `query_class`. Can be used to query the database for instances of this model.
    query = None

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.id!r}, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)

    def auditable(self) -> str:
        """Returns the string representation of this object"""
        return f"created_at={self.created_at}, updated_at={self.updated_at}>"

    def to_json(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    # def load_and_not_raise(self, data):
    #     try:
    #         return self.load(data)
    #     except ValidationError as e:
    #         err = get_error(exception=None, msg=e.messages, status=422)
    #         return abort(make_response(err, err.get('error').get('status')))
    #
    # def validate_and_raise(self, data):
    #     errors = self.validate(data)
    #
    #     if errors:
    #         err = get_error(exception=None, msg=errors, status=422)
    #         return abort(make_response(err, err.get('error').get('status')))


"""
Create the declarative base. This will become the common source for all future SQLAlchemy classes.
For example:
from .abstract import Model
class User(Model):
    # define user model
    pass

"""

# Model = declarative_base(cls=AbstractSchema)
BaseSchema = declarative_base(cls=AbstractSchema)


@event.listens_for(BaseSchema.metadata, "column_reflect")
def column_reflect(inspector, table, column_info):
    # set column.key = "attr_<lower_case_name>"
    logger.info(f"column_reflect({table}, {column_info})")
    # column_info["key"] = "attr_%s" % column_info["name"].lower()


# class BaseSchema(DeclarativeBase):
#     """
#     AbstractSchema define module-level constructs that will form the structures which we will be querying from the
#     database. This structure, known as a Declarative Mapping, defines at once both a Python object model, and database
#     metadata that describes real SQL tables that exist, or will exist, in a particular database:
#
#     The mapping starts with a base class, which above is called 'BaseSchema', and is created by making a simple
#     subclass against the 'DeclarativeBase' class.
#
#     Individual mapped classes are then created by making subclasses of 'BaseSchema'.
#     A mapped class typically refers to a single particular database table, the name of which is indicated by using
#     the '__tablename__' class-level attribute.
#
#     Normally, when one would like to map two different subclasses to individual tables, and leave the base class
#     unmapped, this can be achieved very easily. When using Declarative, just declare the base class with
#     the '__abstract__' indicator:
#     """
#     __abstract__ = True
#
#     """
#     ID - Primary Key
#
#     All ORM mapped classes require at least one column be declared as part of the primary key, typically by using
#     the 'Column.primary_key' parameter on those 'mapped_column()' objects that should be part of the key.
#     """
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#
#     # auditable fields
#     created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
#     updated_at: Mapped[datetime] = mapped_column(insert_default=func.now())
#
#     def __init__(self, **kwargs):
#         """
#         Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
#         A constructor similar to that supplied by Declarative is illustrated:
#         """
#         for key in kwargs:
#             setattr(self, key, kwargs[key])
#
#     def set_attrs(self, **kwargs):
#         """
#         Alternatively, the same Table objects can be used in fully “classical” style, without using Declarative at all.
#         A constructor similar to that supplied by Declarative is illustrated:
#         """
#         for key in kwargs:
#             setattr(self, key, kwargs[key])
#
#     # the query class used. The `query` attribute is an instance of this class. By default, a `BaseQuery` is used.
#     query_class = BaseQuery
#
#     # an instance of `query_class`. Can be used to query the database for instances of this model.
#     query = None
#
#     def __str__(self) -> str:
#         """Returns the string representation of this object"""
#         return f"BaseSchema <id={self.id!r}, created_at={self.created_at}, updated_at={self.updated_at}>"
#
#     def __repr__(self) -> str:
#         """Returns the string representation of this object"""
#         return str(self)
#
#     def auditable(self) -> str:
#         """Returns the string representation of this object"""
#         return f"created_at={self.created_at}, updated_at={self.updated_at}>"


class NamedSchema(BaseSchema):
    """NamedEntity Schema"""
    __abstract__ = True

    # not Optional[], therefore will be NOT NULL
    name: Mapped[str] = mapped_column(String(64))
