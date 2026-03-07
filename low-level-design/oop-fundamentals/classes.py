"""
Design Bank Account Class
Problem: Create a BankAccount class that manages a simple bank account with deposit, withdrawal, and balance checking functionality.

Requirements:

- Fields: accountNumber, ownerName, balance
- Constructor that initializes the account with owner name and account number (balance starts at 0)
    - deposit(amount): adds money to balance (only positive amounts)
    - withdraw(amount): removes money if sufficient balance exists, returns success/failure
    - getBalance(): returns current balance
"""
import uuid

class BankAccount: 
    def __init__(self, owner_name): 
        self.owner_name = owner_name
        self._balance = 0 
        self._id = uuid.uuid4()
    
    def deposit(self, amount):
        if amount <= 0: 
            raise ValueError("Failure: Deposited amount (${amount}) is not valid") 
        
        self._balance += amount
        print("Success: Deposited amount (${amount}), account balance is now at (${self.balance})")

    def withdraw(self, amount):
        if amount <= 0: 
            raise ValueError("Failure: Withdrawal amount (${amount}) is not valid") 
        if self.get_balance() - amount < 0: 
            raise ValueError("Failure: Account balance too low (${self.balance})")
        self._balance -= amount
        print("Success: Withdrawn amount (${amount}), account balance is now at (${self.balance})")
    
    def get_balance(self): 
        return self._balance
    
    def get_id(self):
        return self._id

class Bank: 
    def __init__(self):
        self.accounts = {}
        self.num_accounts = 0
    
    def _num_accounts(self):
        return self.num_accounts

    def create_account(self, owner_name):
        self.num_accounts += 1
        account = BankAccount(owner_name)
        self.accounts[account.get_id()] = account
        return account