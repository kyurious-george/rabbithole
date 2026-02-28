import datetime

from parking_floor import ParkingFloor
from parking_strategy import IParkingStrategy, ParkLowerLevelStrategy
from payment_strategy import IPaymentStrategy, FlatFeeStrategy
from parking_ticket import ParkingTicket
from vehicle import Vehicle

class ParkingLot: 
    def __init__(self):
        self.floors: dict[int, ParkingFloor] | None = {}
        self.tickets: dict[str, ParkingTicket] = {}
        self.payment_strategy: IPaymentStrategy = FlatFeeStrategy()
        self.parking_strategy: IParkingStrategy = ParkLowerLevelStrategy()
    
    def set_parking_strategy(self, parking_strategy: IParkingStrategy):
        self.parking_strategy = parking_strategy
    
    def set_payment_strategy(self, payment_strategy: IPaymentStrategy): 
        self.payment_strategy = payment_strategy
        
    def add_floor(self, floor: ParkingFloor): 
        if floor.num in self.floors: 
            raise ValueError(f"There already exists a floor level {floor.num}")
        self.floors[floor.num] = floor

    def display_state(self): 
        sorted_levels = sorted(self.floors.keys())
        for level in sorted_levels:
            self.floors[level].display_floor()
    
    def park_vehicle(self, vehicle: Vehicle) -> None:
        spot = self.parking_strategy.find_spot(vehicle, self.floors)
        if not spot:
            print(f"Parking Lot Full: cannot park vehicle {vehicle.plate_number} of size {vehicle.size}")
            return 

        self.tickets[vehicle.plate_number] = ParkingTicket(vehicle=vehicle, spot=spot, time_in=datetime.datetime.now())
        spot.park_vehicle(vehicle)
        print(f"Parking vehicle {vehicle.plate_number} in spot {spot.id}")

    def unpark_vehicle(self, plate_number: str): 
        ticket = self.tickets.get(plate_number, None)
        if not ticket: 
            print(f"Vehicle {plate_number} cannot be found inside the parking lot")
            return 
        
        total_cost = self.payment_strategy.process_payment(ticket=ticket, time_out=datetime.datetime.now())
        ticket.spot.unpark_vehicle()
        print(f"Unparking vechile {plate_number}, Total Payment Required: {total_cost}")