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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(64))
    author: Mapped[str] = mapped_column(String(64))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    posted_on: Mapped[datetime] = mapped_column(insert_default=func.now())

    # Other variants of 'Mapped' are available, most commonly the 'relationship()' construct indicated above.
    # In contrast to the column-based attributes, 'relationship()' denotes a linkage between two ORM classes.
    attachments: Mapped[List["Attachment"]] = relationship(back_populates="post", cascade="all, delete-orphan")

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"Document <id={self.id!r}, filename={self.filename!r}, data=*, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class Attachment(BaseSchema):
    """
    [addresses] Table
    """
    __tablename__ = "attachments"

    # foreign key to "posts.id" is added
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="attachments")

    filename: Mapped[str] = mapped_column(String(64))
    # size: Mapped[int] = mapped_column()
    data: Mapped[LargeBinary] = mapped_column(LargeBinary)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"Attachment <id={self.id!r}, filename={self.filename!r}, data=*, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
