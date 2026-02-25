from enum import Enum

class LightColor(Enum):
    GREEN = ("GREEN", 25)
    RED = ("RED", 30)
    YELLOW = ("YELLOW", 5)

    def __init__(self, name, duration):
        self._name = name
        self._duration = duration

class TrafficLight():
    _light_transitions = {
        LightColor.GREEN: LightColor.YELLOW, 
        LightColor.YELLOW: LightColor.RED, 
        LightColor.RED: LightColor.GREEN,
    }

    def __init__(self):
        self.color = LightColor.RED
    
    def next(self): 
        return self._light_transitions.get(self.color)

    def display(self):
        print(f"{self.color._name} ({self.color._duration}s)")
    
if __name__ == "__main__":
    light = TrafficLight()
    for i in range(6):
        light.display()
        light.color = light.next()
