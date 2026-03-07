from oop.classes import BankAccount
import pytest

def test_init():
    account1 = BankAccount("account1")
    assert account1.owner_name == "account1"
    assert account1._balance == 0
    assert account1._id

def test_deposit(): 
    account1 = BankAccount("account1")
    with pytest.raises(ValueError):
        assert account1.deposit(-1)

    account1.deposit(1)
    assert account1._balance == 1

def test_withdraw(): 
    account1 = BankAccount("account1")
    with pytest.raises(ValueError): 
        account1.withdraw(-1)

    with pytest.raises(ValueError): 
        account1.withdraw(1)

    account1.deposit(1)
    assert account1._balance == 1
    account1.withdraw(1)
    assert account1._balance == 0

def test_get_balance(): 
    account1 = BankAccount("account1")
    assert account1.get_balance() == 0

    account1.deposit(100)
    assert account1.get_balance() == 100

def test_get_id(): 
    account1 = BankAccount("account1")
    id = account1._id
    assert account1.get_id() == id