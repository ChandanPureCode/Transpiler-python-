"""PropReference for ".pc" DSL"""

from .identifier import Identifier


# pylint: disable=[too-few-public-methods]
class PropReference:
    """Represents a PropReference in ".pc" DSL object"""

    def __init__(self, identifier: Identifier) -> None:
        """Initialises a PropReference with a given Identifier"""

        self._value = identifier

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PropReference):
            return NotImplemented
        if self._value == other.value:
            return True
        return False

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return f"prop {self._value}"

    def __repr__(self) -> str:
        return f"prop {self._value}"

    @property
    def value(self) -> Identifier:
        """
        getter for the _value attribute

        Returns:
            Identifier: Identifier of the PropReference
        """
        return self._value
