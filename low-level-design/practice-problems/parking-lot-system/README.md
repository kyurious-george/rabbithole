# Design 

## Requirements
- The parking lot should have multiple levels, each level with a certain number of parking spots.
- The parking lot should support different types of vehicles, such as cars, motorcycles, and trucks.
- Each parking spot should be able to accommodate a specific type of vehicle.
- The system should assign a parking spot to a vehicle upon entry and release it when the vehicle exits.
- The system should track the availability of parking spots and provide real-time information to customers.
- The system should handle multiple entry and exit points and support concurrent access.

## Assumptions
- Once placed in queue to get in or out of the parking out, vehicle must wait the queue
- Floors can only be added or old ones replaced

## Classes
- `ParkingLot`:
    - 
- `ParkingTicket`: 
    - spot_number
    - id  
    - time_in
    - time_out 
    - vehicle
- `ParkingFloor`:
    - grid: m x n matrix where each coordinate (i, j) is either `None`, `ParkingSpot`, `Entry`, `Exit`
- `ParkingSpot` 
    - spot_number: int 
    - supported_vehicle: set of supported `VehicleType` 
    - is_taken: bool for whether the spot is currently taken
- `Entry`:
    - queue: list of `Vehicle` that are in line to get in
- `Exit`: 
    - queue: list of `Vehicle` that are in line to get out 
- `Vehicle`: 
    - license_plate: uuid.uuid4() for the sake of demo
    - type: `VehicleType`
- `VehicleType`: enum for car, motorcycle, or truck 