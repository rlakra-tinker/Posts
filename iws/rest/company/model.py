#
# Author: Rohtash Lakra
#

import logging
from typing import Optional

from pydantic import model_validator

from framework.orm.pydantic.model import NamedModel

logger = logging.getLogger(__name__)


class Company(NamedModel):
    """Role contains properties specific to this object."""

    # not Optional[], therefore will be NOT NULL except for the parent entity
    parent_id: int | None = None
    # not Optional[], therefore will be NOT NULL
    branches: Optional["Company"] = None
    # not Optional[], therefore will be NOT NULL
    active: bool = False

    def to_json(self) -> str:
        """Returns the JSON representation of this object."""
        logger.debug(f"{type(self).__name__} => type={type(self)}, object={str(self)}")
        return self.model_dump_json()

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
        return ("{} <id={}, parent_id={}, name={}, active={}, {}>"
                .format(type(self).__name__, self.id, self.parent_id, self.name, self.active, self._auditable()))

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
