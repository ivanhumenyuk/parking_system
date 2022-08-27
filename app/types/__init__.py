from enum import Enum, unique
from functools import total_ordering
from typing import List, Union


@total_ordering
@unique
class SortableUniqueEnum(Enum):
    """Enum class that implements sorting by enum values
    instead of integer values automatically assigned to each member.
    Should be used as a Base class for Enum classes that supposed to
    be inserted into DB as possible column enumerations.
    """

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    @classmethod
    def list(cls, as_list: bool = True) -> Union[str, List[str]]:
        """Returns string with comma-separated enum values or list of values"""
        if as_list:
            return [e.value for e in cls]
        return ", ".join([e.value for e in cls])
