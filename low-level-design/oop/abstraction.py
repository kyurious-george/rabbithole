"""
Problem: Build a shape calculation system using an abstract class. 
The abstract Shape class has abstract methods for calculating area and perimeter, plus a concrete describe() method that all shapes inherit.

Requirements:

- Abstract Shape class with: abstract area() and perimeter() methods, plus a concrete describe() method that prints "Shape: [name], Area: [area], Perimeter: [perimeter]"
- Circle: takes a radius. Area = pi r^2, Perimeter = 2 pi * r
- Rectangle: takes width and height. Area = w h, Perimeter = 2 (w + h)
- describe() should work for any shape without modification
"""
from abc import ABC, abstractmethod
from math import pi

class Shape(ABC):
    def __init__(self, name): 
        self.__name = name

    @abstractmethod
    def area(self) -> int:
        pass

    @abstractmethod
    def perimeter(self) -> int:
        pass

    def describe(self) -> None: 
        print(f"Shape: {self.__name}, Area: {self.area()}, Perimeter: {self.perimeter()}")


class Circle(Shape): 
    def __init__(self, radius):
        super().__init__("Circle")
        self.__radius = radius
    
    def area(self) -> int: 
        return pi * (self.__radius ** 2)

    def perimeter(self) -> int: 
        return 2 * pi * self.__radius
    

class Rectangle(Shape): 
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.__width = width
        self.__height = height

    def area(self) -> int: 
        return self.__width * self.__height
    
    def perimeter(self) -> int: 
        return 2 * (self.__width + self.__height)


if __name__ == "__main__":
    circle = Circle(5.0)
    circle.describe()

    rectangle = Rectangle(4.0, 6.0)
    rectangle.describe()

