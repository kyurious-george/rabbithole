from vehicle import Vehicle
from vehicle_size import VehicleSize
from parking_spot import ParkingSpot

class ParkingFloor: 
    def __init__(self, num: int):
        self.num: int = num
        self.__spots: list[ParkingSpot] = []

    @property
    def spots(self): 
        return self.__spots

    def add_spot(self, size: VehicleSize) -> None:
        spot = ParkingSpot(id = [self.num, len(self.__spots)], type = size)
        self.__spots.append(spot)
    
    def display_floor(self): 
        num_compact = num_medium = num_large = num_unavaliable = 0
        for spot in self.__spots: 
            if spot.open:
                match spot.type: 
                    case VehicleSize.COMPACT: 
                        num_compact += 1
                    case VehicleSize.MEDIUM: 
                        num_medium += 1
                    case VehicleSize.LARGE: 
                        num_large += 1
            else: 
                num_unavaliable += 1
        print(f"------------ FLOOR {self.num} ------------")
        print(f"Total Capacity: {len(self.__spots)}")
        print(f"# Filled: {num_unavaliable}")
        print(f"Current Avaliabilty")
        print(f"- # Compact: {num_compact}")
        print(f"- # Medium: {num_medium}")
        print(f"- # Large: {num_large}")
