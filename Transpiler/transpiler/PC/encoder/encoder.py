"""Encoder for ".pc" DSL"""


from ..dsl import DSL  # pragma: no cover
from .validator import validate


def encode(dsl: DSL) -> str:
    """
    Serializes a DSL object

    Args:
        dsl (DSL): The DSL object to be validated

    Returns:
        str: serialized DSL object
    """
    validate(dsl)
    return repr(dsl)
