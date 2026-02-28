from abc import ABC, abstractmethod
import datetime

from parking_ticket import ParkingTicket

class IPaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, ticket: ParkingTicket, time_out: datetime.time) -> float: 
        pass 


class FlatFeeStrategy(IPaymentStrategy): 
    rate = 5
    
    def process_payment(self, ticket: ParkingTicket, time_out: datetime.time) -> float: 
        delta: datetime.timedelta = time_out - ticket.time_in
        num_days = delta.days 
        # math.ceil the number of days
        if delta - datetime.timedelta(days=num_days) > datetime.timedelta(0):
            num_days += 1
        return self.rate * num_days


class HourlyRateStrategy(IPaymentStrategy): 
    rate = 1.5

    def process_payment(self, ticket: ParkingTicket, time_out: datetime.time) -> float: 
        delta: datetime.timedelta = time_out - ticket.time_in
        num_hrs = delta.hours 
        # math.ceil the number of hrs
        if delta - datetime.timedelta(days=num_hrs) > datetime.timedelta(0):
            num_hrs += 1
        return self.rate * num_hrs