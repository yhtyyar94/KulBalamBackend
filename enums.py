from enum import Enum

class OrderStatus(str, Enum):
    PENDING = 'pending'
    AWAITING = 'awaiting_payment'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
