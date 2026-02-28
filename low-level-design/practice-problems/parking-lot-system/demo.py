from parking_lot import ParkingLot
from parking_floor import ParkingFloor
from vehicle_size import VehicleSize
from vehicle import Vehicle

def main():
    # Initial Small Parking Lot 
    lot = ParkingLot()

    floor1 = ParkingFloor(1)
    floor1.add_spot(VehicleSize.COMPACT)
    floor1.add_spot(VehicleSize.COMPACT)

    floor2 = ParkingFloor(2)
    floor2.add_spot(VehicleSize.LARGE)
    floor2.add_spot(VehicleSize.LARGE)

    lot.add_floor(floor1)
    lot.add_floor(floor2)

    # Display empty lot
    lot.display_state()

    # Add one compact car and one large car 
    compact1 = Vehicle("123", VehicleSize.COMPACT)
    large1 = Vehicle("1234", VehicleSize.LARGE)
    lot.park_vehicle(compact1)
    lot.park_vehicle(large1)

    # Display new lot with two new cars
    lot.display_state()

    # unpark compact 
    lot.unpark_vehicle("123")
    lot.display_state()

    # Try to add car that has no spots in the parking lot
    medium1 = Vehicle("12345", VehicleSize.MEDIUM)
    lot.park_vehicle(medium1)
    lot.display_state()

if __name__ == "__main__": 
    main()
