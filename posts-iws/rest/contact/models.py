#
# Author: Rohtash Lakra
#

from framework.model.abstract import AbstractEntity


class Contact(AbstractEntity):
    first_name: str = None
    last_name: str = None
    country: str = None
    subject: str = None

    def json(self):
        return self.model_dump()
