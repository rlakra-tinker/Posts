#
# Author: Rohtash Lakra
#
from rest.account.repository import AccountRepository
from framework.service import AbstractService
from rest.account.models import Account


class AccountService(AbstractService):

    def __init__(self):
        self.dao = AccountRepository()

    def find_by_id(self, id:int):
        """
        Returns the next ID of the account
        """
        last_id = super(AccountService, self).find_by_id(id)
        if not last_id:
            last_id = 0
        if not self.accounts and len(self.accounts) > 0:
            last_id = max(account["id"] for account in self.accounts)

        return last_id + 1

    def register(self, account: Account):
        account = self.dao.create(account)
        return account


    def update(self, account: Account):
        account = self.dao.create(account)
        return account