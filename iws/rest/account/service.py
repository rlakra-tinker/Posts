#
# Author: Rohtash Lakra
#
from framework.service import AbstractService
from rest.account.model import User
from rest.account.repository import UserRepository


class UserService(AbstractService):

    def __init__(self):
        self.dao = UserRepository()

    def find_by_id(self, id: int):
        """
        Returns the next ID of the account
        """
        last_id = super(UserService, self).find_by_id(id)
        if not last_id:
            last_id = 0

        if not self.accounts and len(self.accounts) > 0:
            last_id = max(account["id"] for account in self.accounts)

        return last_id + 1

    def register(self, user: User):
        user = self.dao.create(user)
        return user

    def update(self, user: User):
        user = self.dao.create(user)
        return user
