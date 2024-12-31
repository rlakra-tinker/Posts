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
    """ PostSchema represents [posts] Table """

    __tablename__ = "posts"

    # foreign key to "users.id" is added
    # not Optional[], therefore will be NOT NULL
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # not Optional[], therefore will be NOT NULL
    title: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    author: Mapped[str] = mapped_column(String(64))
    # Optional[], therefore will be NULL
    content: Mapped[Optional[str]] = mapped_column(String(255))
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
        return ("{} <id={}, user_id={}, title={}, author={}, content={}, posted_on={}, {}, attachments={}>"
                .format(self.getClassName(), self.id, self.user_id, self.title, self.author, self.content,
                        self.posted_on, self.auditable(), self.attachments))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class Attachment(BaseSchema):
    """ AttachmentSchema represents [attachments] Table """

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
        return ("{} <id={}, filename={}, data=*, {}>"
                .format(self.getClassName(), self.id, self.filename, self.auditable()))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class Comment(BaseSchema):
    """ CommentSchema represents [comments] Table """

    __tablename__ = "comments"

    # foreign key to "posts.id" is added
    # not Optional[], therefore will be NOT NULL
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    # foreign key to "users.id" is added
    # not Optional[], therefore will be NOT NULL
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Optional[], therefore will be NULL
    content: Mapped[Optional[str]] = mapped_column(String(255))

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, post_id={}, user_id={}, {}>"
                .format(self.getClassName(), self.id, self.post_id, self.user_id, self.auditable()))

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{self.getClassName()} <id={self.id!r}, content={self.content!r}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)


class Document(BaseSchema):
    """ DocumentSchema represents [documents] Table """

    __tablename__ = "documents"

    filename: Mapped[str] = mapped_column(String(64))
    data: Mapped[LargeBinary] = mapped_column(LargeBinary)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, filename={}, data=*, {}>"
                .format(self.getClassName(), self.id, self.filename, self.auditable()))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
