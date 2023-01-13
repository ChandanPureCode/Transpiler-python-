"""The encoder module"""

from .encoder import encode
from .validator import validate

from .errors import StructuralIntegrityError

__all__ = ["encode", "validate", "StructuralIntegrityError"]
