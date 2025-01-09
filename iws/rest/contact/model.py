#
# Author: Rohtash Lakra
#
import logging

from pydantic import model_validator

from framework.orm.pydantic.model import BaseModel

logger = logging.getLogger(__name__)


class Contact(BaseModel):
    """Contact contains properties specific to this object."""

    first_name: str = None
    last_name: str = None
    country: str = None
    subject: str = None

    @classmethod
    @model_validator(mode="before")
    def pre_validator(cls, values):
        logger.debug(f"pre_validator({values})")
        return values

    @model_validator(mode="after")
    def post_validator(self, values):
        logger.debug(f"post_validator({values})")
        return self

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return ("{} <id={}, first_name={}, last_name={}, country={}, subject={}, {}>"
                .format(self.getClassName(),
                        self.id,
                        self.first_name,
                        self.last_name,
                        self.country,
                        self.subject,
                        self._auditable()))

    # def __repr__(self) -> str:
    #     """Returns the string representation of this object"""
    #     return str(self)

    @staticmethod
    def create(first_name, last_name, country, subject):
        """Creates the contact object with values"""
        print(f"first_name:{first_name}, last_name:{last_name}, country:{country}, subject:{subject}")
        return Contact(first_name=first_name, last_name=last_name, country=country, subject=subject)
