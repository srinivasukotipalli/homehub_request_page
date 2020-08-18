from enum import Enum

class RequestType(Enum):
    Plumbing = "PLUMBING"
    ELECTRICAL = "ELECTRICAL"
    PAINTING = "PAINTING"
    DEEPCLEANING = "DEEPCLEANING"


class Status(Enum):
    pending = "pending"
    inprogress = "inprogress"
    completed = "completed"


class State(Enum):
    AndhraPradesh = "AndhraPradesh"
    ArunachalPradesh = "ArunachalPradesh"
    Pune = "Pune"

