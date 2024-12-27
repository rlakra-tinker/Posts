#
# Author: Rohtash Lakra
#

import logging
from typing import Dict, Any

from pydantic import model_validator

from framework.model import AbstractModel

logger = logging.getLogger(__name__)


class Role(AbstractModel):
    """Role contains properties specific to this object."""

    name: str = None
    active: bool = False
    meta_data: Dict[str, Any] = None

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
        return f"{type(self).__name__} <id={self.get_id()}, name={self.name}, active={self.active}, meta_data={self.meta_data}, {super()._auditable()}>"

    def __repr__(self) -> str:
        """Returns the string representation of this object"""
        return str(self)
