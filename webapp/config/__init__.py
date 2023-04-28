from enum import Enum
from datetime import datetime, timedelta


class UserType(Enum):
    CLIENT = "client"
    PARTNER = "partner"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)


class ParkingLotStatus(Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)


class BookingStatus(Enum):
    WAITING = "WAITING"
    BOOKED = "BOOKED"
    PARKED = "PARKED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)


class SlotStatus(Enum):
    RESERVED = "RESERVED"
    AVAILABLE = "AVAILABLE"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)


def get_slot_status(booking_status: BookingStatus):
    switcher = {
        BookingStatus.WAITING.value: SlotStatus.RESERVED,
        BookingStatus.BOOKED.value: SlotStatus.RESERVED,
        BookingStatus.PARKED.value: SlotStatus.RESERVED,
        BookingStatus.COMPLETED.value: SlotStatus.AVAILABLE,
        BookingStatus.CANCELLED.value: SlotStatus.AVAILABLE,
    }
    return switcher.get(booking_status, SlotStatus.AVAILABLE)


def get_deltatime(value: str):
    t = datetime.strptime(value, "%H:%M:%S")
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
