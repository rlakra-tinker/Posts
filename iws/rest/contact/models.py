#
# Author: Rohtash Lakra
#
from framework.orm.pydantic.model import AbstractModel


class Contact(AbstractModel):
    first_name: str = None
    last_name: str = None
    country: str = None
    subject: str = None

    def __str__(self) -> str:
        """Returns the string representation of this object"""
        return f"{type(self).__name__} <id={self.get_id()}, first_name={self.first_name}, last_name={self.last_name}, country={self.country}, subject={self.subject}>"

    # def __repr__(self) -> str:
    #     """Returns the string representation of this object"""
    #     return str(self)

    @staticmethod
    def create(first_name, last_name, country, subject):
        """Creates the contact object with values"""
        print(f"first_name:{first_name}, last_name:{last_name}, country:{country}, subject:{subject}")
        return Contact(first_name=first_name, last_name=last_name, country=country, subject=subject)
