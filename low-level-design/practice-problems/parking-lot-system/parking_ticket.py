from vehicle import Vehicle
from parking_spot import ParkingSpot
import datetime

class ParkingTicket: 
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot, time_in: datetime.datetime):
        self.vehicle = vehicle
        self.spot = spot
        self.time_in = time_in