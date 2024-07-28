#
# Author: Rohtash Lakra
#
from typing import Dict
from framework.service import AbstractService
from .models import User


class AccountService(AbstractService):

    def __init__(self):
        self.accounts: Dict[int, User] = {}

    def _find_next_id(self):
        """
        Returns the next ID of the account
        """
        last_id = super(AccountService, self)._find_next_id()
        if not self.accounts and len(self.accounts) > 0:
            last_id = max(account["id"] for account in self.accounts)

        return last_id + 1

    def add(self, user: User):
        print(f"user: {user}")
        user.id = self._find_next_id()
        print(f"user.id: {user.id}")
        self.accounts[user.id] = user

    def register(self, username, password):
        user = User(username=username, password=password)
        self.add(user)
        return {
            "user_name": "user_name"
        }
