#
# Author: Rohtash Lakra
#

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from framework.orm.sqlalchemy.schema import BaseSchema


class Contact(BaseSchema):
    __tablename__ = "contacts"

    # not Optional[], therefore will be NOT NULL
    first_name: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    last_name: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    country: Mapped[str] = mapped_column(String(64))
    # not Optional[], therefore will be NOT NULL
    subject: Mapped[str] = mapped_column(String(64))

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.get_id()}, first_name={self.first_name}, last_name={self.last_name}, country={self.country}, subject={self.subject}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
