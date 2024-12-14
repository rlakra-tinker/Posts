#
# Author: Rohtash Lakra
#
from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from framework.orm.sqlalchemy.entity import BaseEntity


class Document(BaseEntity):
    """
    [documents] Table
    """
    __tablename__ = "documents"

    # foreign key to "users.id" is added
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user: Mapped["User"] = relationship(back_populates="addresses")

    filename: Mapped[str] = mapped_column(String(64))
    data: Mapped[LargeBinary] = mapped_column(LargeBinary)

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"Document <id={self.id!r}, filename={self.filename!r}, data=*, created_at={self.created_at}, updated_at={self.updated_at}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
