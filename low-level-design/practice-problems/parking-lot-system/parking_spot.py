from vehicle_size import VehicleSize
from vehicle import Vehicle

class ParkingSpot: 
    def __init__(self, id: tuple[int, int], type: VehicleSize): 
        self.id: tuple[int, int] = id 
        self.__type: VehicleSize = type
        self.__open: bool = True
        self.__vehicle: Vehicle | None = None

    @property
    def open(self): 
        return self.__open
    
    @property
    def type(self):
        return self.__type

    def park_vehicle(self, vehicle: Vehicle) -> None:
        self.__vehicle: Vehicle = vehicle
        self.__open: bool = False
    
    def unpark_vehicle(self) -> Vehicle: 
        vehicle: Vehicle = self.__vehicle 
        self.__vehicle: Vehicle = None
        self.__open: bool = True
        return vehicle