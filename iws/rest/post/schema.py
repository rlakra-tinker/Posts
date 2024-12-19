#
# Author: Rohtash Lakra
#

from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import LargeBinary

from framework.orm.sqlalchemy.schema import BaseSchema


class Post(BaseSchema):
    """
    [posts] Table
    """
    __tablename__ = "posts"

    # foreign key to "users.id" is added
    # not Optional[], therefore will be NOT NULL
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # not Optional[], therefore will be NOT NULL
    title: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    author: Mapped[str] = mapped_column(String(64))
    # Optional[], therefore will be NULL
    description: Mapped[Optional[str]] = mapped_column(String(255))
    # not Optional[], therefore will be NOT NULL
    posted_on: Mapped[datetime] = mapped_column(insert_default=func.now())

    # Other variants of 'Mapped' are available, most commonly the 'relationship()' construct indicated above.
    # In contrast to the column-based attributes, 'relationship()' denotes a linkage between two ORM classes.
    # attachments: Mapped[List["Attachment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    # Optional[], therefore will be NULL
    attachments: Mapped[Optional[List["Attachment"]]] = relationship(back_populates="post",
                                                                     cascade="all, delete-orphan")

    def addAttachment(self, attachment):
        self.attachments.__add__(attachment)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.id!r}, filename={self.filename!r}, data=*, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class Attachment(BaseSchema):
    """
    [addresses] Table
    """
    __tablename__ = "attachments"

    # foreign key to "posts.id" is added
    # not Optional[], therefore will be NOT NULL
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    # not Optional[], therefore will be NOT NULL
    post: Mapped["Post"] = relationship(back_populates="attachments")

    # not Optional[], therefore will be NOT NULL
    filename: Mapped[str] = mapped_column(String(64))
    # size: Mapped[int] = mapped_column()
    # not Optional[], therefore will be NOT NULL
    data: Mapped[LargeBinary] = mapped_column(LargeBinary)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.id!r}, filename={self.filename!r}, data=*, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class Document(BaseSchema):
    """
    [documents] Table
    """
    __tablename__ = "documents"

    filename: Mapped[str] = mapped_column(String(64))
    data: Mapped[LargeBinary] = mapped_column(LargeBinary)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.id!r}, filename={self.filename!r}, data=*, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
