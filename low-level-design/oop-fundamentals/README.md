## Classes

**Classes**: template for defining what objects can store and what they are able to do
- **Attributes**: represent the state or data of an object
- **Methods**: functions inside a class that represent actions that objects can do

```python
class Car:
    # Constructor
    def __init__(self, brand, model):
        # Attributes (private by convention with underscore)
        self.__brand = brand
        self.__model = model
        self.__speed = 0

    # Method to accelerate
    def accelerate(self, increment):
        self.__speed += increment

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
- `self.__{attribute_name}` is the syntax for private attributes in Python
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


## Encapsulation

**Encapsulation**: hiding data and controlling access by using classes and limiting the scope that can be seen

Benefits of Encapsulation: 
- Hiding sensitive data 
- Controlling access by using getters and setters 
- Improving maintainability by hiding internal details 
- Reduces the risk of inconsistent system states

**Access Modifiers**: keywords that control which parts of the code can see and interact with class attributes and methods
- **Private**: accessible only within the same class
- **Protected**: accessible within the same class and subclasses 
- **Public**: accessible from anywhere  

```python
class Product:
    def __init__(self, name: str, price: float):
        self.__name = name       # Name-mangled (private by convention)
        self.__price = price     # Name-mangled (private by convention)
```

General Rule of Thumb: make everything private and then selectively make it public

**Getter**: public methods that provide read only access to an object's attribute
**Setter**: public method that provides write access to an object's attribute, usually with validation logic built in

```python
class Product:
    def __init__(self, name: str, price: float):
        self.__name = name
        self.price = price  # Uses the property setter for validation

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value
```


## Abstraction

**Abstraction**: hiding complexity and showing the essentials

Benefits of Abstraction: 
- Ability to change implementation without changing code of the caller
- Reduce complexity for callers
- Create more classes and easily extend features 
- Share common logic

```python 
from abc import ABC, abstractmethod
from datetime import datetime

class Logger(ABC):
    def __init__(self, level: str):
        self._level = level

    # Abstract method: subclasses decide HOW to deliver the message
    @abstractmethod
    def log(self, message: str) -> None:
        pass

    # Concrete method: shared formatting logic inherited by all subclasses
    def format_message(self, message: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] [{self._level}] {message}"

class ConsoleLogger(Logger):
    def __init__(self, level: str):
        super().__init__(level)

    def log(self, message: str) -> None:
        print(self.format_message(message))

class FileLogger(Logger):
    def __init__(self, level: str, file_path: str):
        super().__init__(level)
        self._file_path = file_path

    def log(self, message: str) -> None:
        # In production, this would write to a file
        print(f"Writing to {self._file_path}: {self.format_message(message)}")
```

## Inheritance

**Inheritance**: Allows for one class to inherit the properties and behaviors of another class

Benefits of Inheritance: 
- Reusing code 
- Provides a logical hierarchy
- Ease of maintainability
- Polymorphism

What Happens?
- Subclass inherits all non-private fields and methods of the superclass
- Subclass overrides inherited methods to provide different implmentation
- Subclass extends the superclass by adding new fields and methods

Types of Inheritance: 
1. **Single Inheritance**: one child class extends one parent class
2. **Multi Level Inheritance**: parent -> child -> grandchild
3. **Hierarchical Inheritance**: multiple child classes extend the same parent 
4. **Multiple Inheritance**: child extends more than one parent (only possible in C++ and Python, should generally avoid)

When to use inheritance? 
- "is-a" relationship is clear
- Parent class defines common behavior in data among children data
- Child class does not violate the behavior expected from the Parent class
- Hierarchy should be max 2-3 levels 

```python 
class Vehicle:
    def __init__(self, make: str, model: str, year: int):
        self._make = make
        self._model = model
        self._year = year

    def start_engine(self):
        print("Engine started")

    def stop_engine(self):
        print("Engine stopped")

    def display_info(self):
        print(f"{self._year} {self._make} {self._model}")


class ElectricCar(Vehicle):
    def __init__(self, make: str, model: str, year: int, battery_capacity: int):
        super().__init__(make, model, year)
        self._battery_capacity = battery_capacity

    def charge_battery(self):
        print(f"Charging {self._battery_capacity}kWh battery")


class GasCar(Vehicle):
    def __init__(self, make: str, model: str, year: int, fuel_tank_size: float):
        super().__init__(make, model, year)
        self._fuel_tank_size = fuel_tank_size

    def fill_tank(self):
        print(f"Filling {self._fuel_tank_size}L fuel tank")
```

## Polymorphism 

**Polymorphism**: using the same method name or interface to have different behaviors depending on the object that is calling the method

Benefits of Polymorphism: 
- Loose coupling
- Flexibility 
- Scalability
- Extensibilty

Two Forms of Polymorphism: 
- **Compile-Time Polymorphism**: also known as method-overloading, when you have methods of the same name but with different parameter inputs
```python
class Calculator:
    def add(self, *args):
        return sum(args)

calc = Calculator()
print(calc.add(2, 3))        # 5
print(calc.add(2.5, 3.5))    # 6.0
print(calc.add(1, 2, 3))     # 6
```
- **Runtime Polymorphism**: also known as method overriding or dynamic dispatch, when a child class overrides a method defined in its parent class and at runtime the decision of which method to use is determined based on the type passed in
```python
class Notification:
    def __init__(self, recipient: str, message: str):
        self._recipient = recipient
        self._message = message

    def send(self):
        print(f"Sending generic notification to {self._recipient}")


class EmailNotification(Notification):
    def __init__(self, recipient: str, message: str, subject: str):
        super().__init__(recipient, message)
        self._subject = subject

    def send(self):
        print(f"Sending EMAIL to {self._recipient} | Subject: {self._subject}")


class SMSNotification(Notification):
    def __init__(self, recipient: str, message: str, phone_number: str):
        super().__init__(recipient, message)
        self._phone_number = phone_number

    def send(self):
        print(f"Sending SMS to {self._phone_number} | Message: {self._message}")


class PushNotification(Notification):
    def __init__(self, recipient: str, message: str, device_token: str):
        super().__init__(recipient, message)
        self._device_token = device_token

    def send(self):
        print(f"Sending PUSH to device {self._device_token[:8]}"
              f"... | Alert: {self._message}")


if __name__ == "__main__":
    notifications = [
        EmailNotification("alice@example.com", "Your order shipped!", "Order Update"),
        SMSNotification("Bob", "Code: 482910", "+1-555-0123"),
        PushNotification("Charlie", "New message", "d8a3f4b2c1e5a9b7"),
    ]

    for n in notifications:
        n.send()
```