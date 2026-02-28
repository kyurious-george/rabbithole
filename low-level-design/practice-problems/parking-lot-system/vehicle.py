from vehicle_size import VehicleSize

class Vehicle: 
    def __init__(self, plate_number: str, size: VehicleSize): 
        self.__size: VehicleSize = size
        self.__plate_number: str = plate_number

    @property
    def size(self): 
        return self.__size
    
    @property
    def plate_number(self): 
        return self.__plate_number
    