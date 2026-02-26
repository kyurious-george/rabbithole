## Classes

**Classes**: template for defining what objects can store and what they are able to do
- **Attributes**: represent the state or data of an object
- **Methods**: functions inside a class that represent actions that objects can do

```python
class Car:
    # Constructor
    def __init__(self, brand, model):
        # Attributes (private by convention with underscore)
        self._brand = brand
        self._model = model
        self._speed = 0

    # Method to accelerate
    def accelerate(self, increment):
        self._speed += increment

if __name__ == "__main__":
    # Creating objects of the Car class
    corolla = Car("Toyota", "Corolla")
    mustang = Car("Ford", "Mustang")

    corolla.accelerate(20)
    mustang.accelerate(40)

    # Displaying status of each car
    corolla.display_status()
    print("-----------------")
    mustang.display_status()
```

**Private**: attributes or methods that are hidden to the user (these are usually helper functions and sensitive data)
- `self._{attribute_name}` is the syntax for private attributes in Python
- `self.__{private_method_name}` is the syntax for private methods in Python

**Public**: attributes or methods that are open and accessible to the user (can use from the main function)
- Note: attributes and methods are public by default in Python
- Use `@property` to specify an attribute as public read only (allows `{object}.{attribute}` syntax but you can't modify the attribute data)


## Enums

**Enum**: special data type that defines a fixed set of constants and allows for compilers and type checkers to be catch errors early 

```python 
from enum import Enum

class Coin(Enum):
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUARTER = 25
    
    def __init__(self, value): # attributes get init automatically and as a tuple for the {ENUM}.{attribute}
        self.coin_value = value
    
    def get_value(self):
        return self.coin_value
```

Some Details about Enums:
- `{enum}.name` is automatically assigned without having to init
- `{enum}.attribute1, {enum}.attribute2` are automatically assigned by unpacking the tuple that the enum is set to
- You can have distinctly named enums that have the same values (values are not unique except when `@enum.unique` is specified, however, names must be unique) 


## Interfaces 

**Interfaces**: list of methods that the implementing classes must provide, however, the implementation is not written (actual implementation routes to the individual classes)

Properties of Interfaces:
- Defines behavior through method signatures without defining the actual implementation 
- Polymorphism: one code can work with many different implementations seemlessly 
- Decoupling: separates the code that uses the interface from the code that implements the interface (ie. think of it as a wall blocking the two sides so you have to think less)

```python
# Defining an interface 
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def initiate_payment(self, amount):
        pass

# Implementing an interface
class StripePayment(PaymentGateway):
    def initiate_payment(self, amount):
        print(f"Processing payment via Stripe: ${amount}")

class RazorpayPayment(PaymentGateway):
    def initiate_payment(self, amount):
        print(f"Processing payment via Razorpay: ₹{amount}")

# Using the interface
class CheckoutService:
    # Dependency Injection: the interface receives the dependencies from the outside and is able use them because it is typed as an interface
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway
    
    def set_payment_gateway(self, payment_gateway):
        self.payment_gateway = payment_gateway
    
    def checkout(self, amount):
        self.payment_gateway.initiate_payment(amount)
```