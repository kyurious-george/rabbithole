'''
Problem: Build a TemperatureSensor class that collects temperature readings and provides statistical access. 
The sensor should validate that readings fall within a reasonable range and never expose its internal list of readings directly.

Requirements:
- Private list of readings
- addReading(value): adds a temperature reading, but only if it's between -50 and 150 degrees (inclusive). Reject out-of-range values.
- getAverage(): returns the average of all readings, or 0 if no readings exist
- getReadingCount(): returns how many readings have been recorded
- getReadings(): returns a copy of the readings list (not the original)
'''
from copy import copy

class TemperatureSensor: 
    def __init__(self, readings: list[int] = []): 
        self.__readings = readings
    
    def get_average(self):
        if not self.__readings:
            return 0
        return round(sum(self.__readings) / len(self.__readings), 2)
        
    def get_reading_count(self):
        return len(self.__readings)

    def get_readings(self): 
        return copy(self.__readings)
    
    def add_reading(self, reading: int):
        if (reading < -50) or (reading > 150): 
            print("Failure: Input {reading} is out of range. Please input readings between -50 and 150 degrees only.")
            return 
        self.__readings.append(reading)


if __name__ == "__main__":
    sensor = TemperatureSensor()
    sensor.add_reading(22.5)
    sensor.add_reading(23.1)
    sensor.add_reading(200.0)  # Should be rejected
    sensor.add_reading(-10.0)

    print(f"Count: {sensor.get_reading_count()}")  # 3
    print(f"Average: {sensor.get_average()}")       # 11.87
        
        

