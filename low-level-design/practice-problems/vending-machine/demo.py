import logging

from product import Product
from money import Money
from vending_machine_system import VendingMachineSystem

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

vending_machine = VendingMachineSystem()

# Add products
coke = Product("Coke", 1.50)
water = Product("Water", 1.00)
chips = Product("Chips", 2.25)

vending_machine.add_product(coke)
vending_machine.add_product(water)
vending_machine.add_product(chips)

# Try adding a duplicate
vending_machine.add_product(coke)

# Restock products
vending_machine.restock_product(coke, 5)
vending_machine.restock_product(water, 3)
vending_machine.restock_product(chips, 2)

# Load change into the machine
vending_machine.add_money(Money.QUARTER, 20)
vending_machine.add_money(Money.DIME, 20)
vending_machine.add_money(Money.NICKEL, 20)

# Buy a water ($1.00) with exact change
print("\n--- Buy Water with exact change ---")
change = vending_machine.buy_product(water, [Money.DOLLAR])
print(f"Change: {change}")

# Buy a coke ($1.50) with $2.00
print("\n--- Buy Coke with $2.00 ---")
change = vending_machine.buy_product(coke, [Money.DOLLAR, Money.DOLLAR])
print(f"Change: {change}")

# Try buying out-of-stock product
print("\n--- Buy product not in stock ---")
candy = Product("Candy", 0.75)
vending_machine.buy_product(candy, [Money.DOLLAR])

# Try buying with insufficient funds
print("\n--- Buy Chips with insufficient funds ---")
vending_machine.buy_product(chips, [Money.DOLLAR])

# Collect all money from machine
print("\n--- Collect money ---")
total = vending_machine.collect_money()
print(f"Total collected: ${total:.2f}")
