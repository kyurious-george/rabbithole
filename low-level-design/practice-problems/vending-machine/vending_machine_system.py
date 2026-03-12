import logging
from typing import Optional

from product import Product
from money import Money


class VendingMachineSystem: 
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.products: dict[Product, int] = {}
        self.money: dict[Money, int] = {money: 0 for money in Money}

    def add_product(self, product: Product): 
        if product in self.products:
            self.logger.warning(f"Product {product.name} is already in the vending machine system.")
            return 

        self.products[product] = 0
        self.logger.info(f"Adding new product {product.name} to vending machine system")
    
    def remove_product(self, product: Product):
        if product not in self.products:
            self.logger.warning(f"Product {product.name} is not in vending machine system")
            return 
    
        del self.products[product]
        self.logger.info(f"Removing product {product.name} to vending machine system")

    def restock_product(self, product: Product, quantity: int): 
        if product not in self.products: 
            self.logger.warning(f"Product {product.name} not in vending machine system")
            return 
        if quantity <= 0: 
            self.logger.warning(f"Quantity {quantity} must be greater than 0")
            return 

        self.products[product] += quantity
        self.logger.info(f"Restocking {quantity} of {product.name} to vending machine system")

    def add_money(self, money: Money, quantity: int):
        if quantity <= 0: 
            self.logger.warning(f"Quantity {quantity} must be greater than 0")
        self.money[money] += quantity
    
    def collect_money(self) -> float: 
        result = 0
        for money, quantity in self.money.items(): 
            result += money.value * quantity
        self.money: dict[Money, int] = {money: 0 for money in Money}
        return result

    def buy_product(self, product: Product, payment: list[Money]) -> dict[Money, int] | None:
        if product not in self.products: 
            self.logger.warning(f"Product {product.name} is not in vending machine system")
            return 
        if self.products[product] == 0: 
            self.logger.warning(f"Product {product.name} is out of stock")
            return 
        
        total_payment = sum(money.value for money in payment)
        if product.price > total_payment: 
            self.logger.warning(f"Insufficient Funds: {total_payment}/{product.price}")
            return 
        
        change_owed = total_payment - product.price

        for money in payment:
            self.money[money] += 1

        self.products[product] -= 1

        if change_owed > 0.00:
            return self.get_change(change_owed)
        else:
            return {}
    
    def get_change(self, exceeding_balance: float) -> Optional[dict[Money, int]]: 
        desc_money = sorted(self.money.keys(), key=lambda x: x.value, reverse=True)
        change = {}
        for money in desc_money: 
            while exceeding_balance > 0 and money.value <= exceeding_balance and self.money[money] > 0: 
                self.money[money] -= 1
                exceeding_balance -= money.value
                change[money] = change.get(money, 0) + 1
        return change