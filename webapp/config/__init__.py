from enum import Enum


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
    WAITING = "WAITING"
    RESERVED = "RESERVED"
    AVAILABLE = "AVAILABLE"

    @classmethod
    def choices(cls):
        print(tuple((i.name, i.value) for i in cls))
        return tuple((i.name, i.value) for i in cls)


def get_slot_status(booking_status: BookingStatus):
    switcher = {
        BookingStatus.WAITING: SlotStatus.WAITING,
        BookingStatus.BOOKED: SlotStatus.RESERVED,
        BookingStatus.PARKED: SlotStatus.RESERVED,
        BookingStatus.COMPLETED: SlotStatus.AVAILABLE,
        BookingStatus.CANCELLED: SlotStatus.AVAILABLE,
    }
    return switcher.get(booking_status, SlotStatus.AVAILABLE)



