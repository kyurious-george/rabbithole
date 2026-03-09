# "uses-a" Relationships

## Association

**Association**: relationship between two classes where one object uses, communicates, or references another
- Properties
    - Directionality: who knows about whom? 
    - Multiplicity: how many objects are connected?

**Directionality**: which class holds a reference to the other and whether communication is one-way or two-way
- **Unidirectional Association**: only one class holds a reference to the other
    - *ex: services, gateways, interfaces*
- **Bidirectional Assocation**: both classes hold references to each other
    - *ex: team and player*

**Multiplicity**: how many instances of one class can be associated with instances of another class
- **1-1**: each object of one class is associated to exactly one object of another class 
    - *ex: user and profiles*
- **1-N**: one object of a class is linked to multiple objects of another class 
    - *ex: manufacturer and car model*
    - Note: this is by far the most common of the relationships

## Dependency

**Dependency**: represents the weakest form of relationship between classes and reflects a one-time interaction 
- One class relies on another class but does not need to hold onto a permanent reference to it 

Forms of Dependency: 
- Method Parameters: dependent class receives another class as a parameter, uses it in the method call, and then garbage collects 
- Local Variables: dependent class creates instance of another class, uses it, and then garbage collects it
- Return Types: dependent class method returns instance of another class (basically factory pattern)
- Static Method Calls: when you import a library and use it

**Dependency Injection**: dependent classes receive dependencies in methods instead of creating them
- Testability 
- Modularity
- Loose Coupling

# "has-a" Relationships

## Aggregation

**Aggregation**: form of association that model "whole-part" relationship with loose ownership (parts do not contain references to the whole)
- "Whole" does not create or destroy the "part" aka simply a logical grouping
- *ex: playlist and song*

## Composition

**Composition**: strongest form of association that model "whole-part" relationship where the whole owns the part and controls their lifecycle (responsible for creating and destroying)
- Parts are not shared with any other objects 
- Parts can only exist with a whole 
- *ex: car and parts (engine, transmission, etc.)*

*Favor composition over inheritance*
- Allows for breaking down complex behavior into smaller parts 
- Avoids tight coupling and fragility that comes with inheritance

# "can-be-a" Relationships

## Realization

**Relationship**: form of relationship that defines a contract where a class implements the definition defined by an interface
- Interface (ABC) and implementing class

Components of Relization:
- **Interface**: defines "what must be done" aka method signatures
- **Class**: implements "how it is done" and must contain all method signatures defined in the interface3