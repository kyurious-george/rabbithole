from abc import ABC, abstractmethod

from vehicle import Vehicle
from parking_spot import ParkingSpot
from parking_floor import ParkingFloor 

class IParkingStrategy(ABC): 
    @abstractmethod
    def find_spot(self, vehicle: Vehicle, floors: dict[int, ParkingFloor]) -> ParkingSpot | None:
        pass


class ParkLowerLevelStrategy(IParkingStrategy): 
    def find_spot(self, vehicle: Vehicle, floors: dict[int, ParkingFloor]) -> ParkingSpot | None:
        sorted_levels = sorted(floors.keys())
        for i in sorted_levels: 
            floor = floors[i]
            for spot in floor.spots: 
                if spot.open and spot.type == vehicle.size:
                    return spot
        return None


class ParkUpperLevelStrategy(IParkingStrategy): 
    def find_spot(self, vehicle: Vehicle, floors: dict[int, ParkingFloor]) -> ParkingSpot | None:
        sorted_levels = sorted(floors.keys(), reverse=True)
        for i in sorted_levels: 
            floor = floors[i]
            for spot in floor.spots: 
                if spot.open and spot.type == vehicle.size:
                    return spot
        return None
