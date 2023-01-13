"""Identifier for ".pc" DSL"""


from regex import match

from .errors import InvalidIdentifierError


class Identifier:
    """Represents an Identifier in ".pc" DSL object"""

    # RegEx for unicode categories
    regex_letter = r"[\p{L}]"
    regex_half_space = r"\u200C"
    regex_zero_width_joiner = r"\u200D"
    regex_non_spacing_mark = r"[\p{Mn}]"
    regex_decimal_digit_number = r"[\p{Nd}]"
    regex_connector_punctuation = r"[\p{Pc]"

    regex_backslash = r"\\"
    regex_hex_digit = r"[_0-9a-fA-F]"
    regex_unicode_escape_sequence = (
        f"{regex_backslash}u{{{regex_hex_digit}{regex_hex_digit}}}|"
        f"{regex_backslash}u{regex_hex_digit}{regex_hex_digit}{regex_hex_digit}{regex_hex_digit}"
    )

    regex_identifier_start = (
        f"[$_]|" f"{regex_letter}|" f"{regex_unicode_escape_sequence}"
    )
    regex_identifier_part = (
        f"{regex_identifier_start}|"
        f"{regex_non_spacing_mark}|"
        f"{regex_decimal_digit_number}|"
        f"{regex_connector_punctuation}|"
        f"{regex_half_space}|"
        f"{regex_zero_width_joiner}"
    )
    regex_identifier = f"({regex_identifier_start})({regex_identifier_part})*"

    def __init__(self, value: str) -> None:
        """
        Initialises an Identifier

        Args:
        value (str): value of the identifier

        Raises:
        InvalidIdentifierError: If the value provided isn't a valid Identifier
        """
        if match(self.regex_identifier, value):
            self._value: str = value
        else:
            raise InvalidIdentifierError()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Identifier):
            return NotImplemented
        if self._value == other.value:
            return True
        return False

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Identifier):
            return NotImplemented
        if self._value < other.value:
            return True
        return False

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return str(self._value)

    @property
    def value(self) -> str:
        """
        getter for the _value attribute

        Returns:
            str: The value of the Identifier
        """
        return self._value
