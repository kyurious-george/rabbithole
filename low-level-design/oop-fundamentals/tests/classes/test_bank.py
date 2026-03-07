import pytest
from oop.classes import Bank, BankAccount   

def test_init(): 
    bank = Bank()
    assert len(bank.accounts) == 0 and bank.num_accounts == 0

def test_create_account():
    bank = Bank()
    account = bank.create_account("account1")
    assert isinstance(account, BankAccount)
    assert bank._num_accounts() == 1
    assert len(bank.accounts) and account.get_id() in bank.accounts