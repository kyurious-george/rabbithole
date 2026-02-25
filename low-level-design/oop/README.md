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