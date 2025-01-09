#
# Author: Rohtash Lakra
# Reference:
# - https://pyjwt.readthedocs.io/en/2.10.1/
#
from datetime import datetime
from enum import auto, unique

import jwt

from framework.enums import BaseEnum
from framework.exception import AuthenticationException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import AbstractModel


@unique
class TokenType(BaseEnum):
    AUTH = auto()
    JWT = auto()


class JWTTokenModel(AbstractModel):
    """JWTTokenModel represents """
    jwt_token: str
    # Time since epoch
    exp: float | int


class JWTModel(AbstractModel):
    """JWTModel contains the payload to create a JWT Token"""
    user_id: str | None = None
    medium: str
    phone_number: str | None = None
    country_code: str | None = None
    email: str | None = None


class AuthenticatedUser(AbstractModel):
    """An Authenticated User's response payload """
    user_id: str | None = None
    token: str
    user_exists: bool
    token_type: TokenType
    # Time since epoch
    exp: float | int | None = None


class JWTUtils(object):
    ZOOM_VIDEO_SDK_KEY = "ZOOM_VIDEO_SDK_KEY"
    ZOOM_VIDEO_SDK_SECRET = "ZOOM_VIDEO_SDK_SECRET"

    def jwtCreateToken(cls, jwtModel: JWTModel, expiry_in_hours: int = None, exp: int | float = None) -> JWTTokenModel:
        """Creates a JWT token with the provided params.

        Arguments:
            - jwtModel:(JWTModel): The identity for which the JWT token is being created.
            - expiry_in_hours (int, optional): The number of hours after which the token should expire and defaults to
            24 hours.
            - exp (datetime, optional): The exact expiration time for the token. If provided, this value will be used
            directly. If not provided, it will be calculated based on `expires_in_hours` or the default app
            configuration.

        Returns:
            JWTTokenModel: A Pydantic model contains the JWT token and its expiration time as a Unix timestamp.
        """
        now = datetime.now()
        expiry_delta = expiry_in_hours if expiry_in_hours else 24
        exp = (now + expiry_delta).timestamp() if exp is None else exp - now
        jwtToken = jwt.encode({"identity": jwtModel.model_dump(), "expiry_delta": expiry_delta}, "secret",
                              algorithm="HS256")
        return JWTTokenModel(jwt_token=jwtToken, exp=exp)

    def getIdentity(cls, jwtToken: str | None):
        """Validates the request contains the JWT token."""
        if jwtToken is None:
            raise AuthenticationException(HTTPStatus.BAD_REQUEST, "The JWT Token must provide in request!")

        try:
            # Decode the JWT token
            decodedToken = jwt.decode(jwtToken, "secret", algorithms=["HS256"])
            return decodedToken.get('sub')
        except Exception:
            raise AuthenticationException(HTTPStatus.UNAUTHORIZED, "Invalid or Expired JWT Token!")
