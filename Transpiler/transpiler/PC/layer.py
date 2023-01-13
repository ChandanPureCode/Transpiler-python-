"""Layer for ".pc" DSL"""

from __future__ import annotations
from typing import TYPE_CHECKING, TypeAlias, Optional, Union
from numbers import Number

from re import sub as regex_substitute

from .identifier import Identifier
from .prop_reference import PropReference
from .errors import InvalidTransactionError, IdentifierNotFoundError

if TYPE_CHECKING:
    from .component import Component  # pragma: no cover


class Layer:
    """Represents a Layer in ".pc" DSL object"""

    # stringify constants
    tab = "\t"
    newline = "\n"
    open_brace = "{"
    open_bracket = "["
    closed_brace = "}"
    closed_bracket = "]"

    # Type definitions
    Value: TypeAlias = Union[
        None | bool, str, Number, dict[str, "Value"], list["Value"], PropReference
    ]
    Child: TypeAlias = Union[str, Identifier, PropReference]

    def __init__(self, name: str) -> None:
        """
        Initialize a Layer object

        Args:
            name (str): The value of the Identifier for the Layer
        """
        self._component: Optional[Component] = None
        self._identifier: Identifier = Identifier(name)
        self._is_root: bool = False
        self._parent: Optional[Identifier] = None
        self._children: list[Layer.Child] = []
        self.props: dict[str, Layer.Value] = {}
        self.import_library: Optional[str] = None
        self.import_name: Optional[Identifier] = None

    def __eq__(self, other: Layer) -> bool:
        if self._identifier != other._identifier:
            return False
        if self._is_root != other._is_root:
            return False
        if self.import_name != other.import_name:
            return False
        if self.import_library != other.import_library:
            return False
        if self._parent != other._parent:
            return False
        if set(self._children) != set(other._children):
            return False
        if not self.__check_eq_props(other):
            return False
        return True

    def __str__(self) -> str:
        return self.__stringify()

    def __repr__(self) -> str:
        layer_string = self.__stringify()
        return regex_substitute(r"[\t\n]+", "", layer_string)

    @property
    def identifier(self) -> Identifier:
        """
        getter for the _identifier attribute

        Returns:
            Identifier: The identifier of the Layer
        """
        return self._identifier

    @property
    def is_root(self) -> bool:
        """
        getter for the _is_root attribute

        Returns:
            bool: whether the layer is a root layer
        """
        return self._is_root

    @is_root.setter
    def is_root(self, value: bool) -> None:
        """
        setter for the _is_root attribute

        Args:
            value (bool): whether the layer is a root layer

        Raises:
            InvalidTransactionError: If the layer already has a parent layer
        """
        if value is True and self._parent is not None:
            raise InvalidTransactionError(
                "A layer with an parent can't be a root layer"
            )
        self._is_root = value

    @property
    def parent(self) -> Optional[Identifier]:
        """
        getter for the _parent attribute

        Returns:
            Optional[Identifier]: The identifier of the parent if exists
        """
        return self._parent

    @parent.setter
    def parent(self, identifier: Identifier) -> None:
        """
        setter for the _parent attribute

        Args:
            identifier (Identifier): The identifier of the parent

        Raises:
            InvalidTransactionError: If the layer is a root layer
            InvalidTransactionError: If the provided identifier matches with the layers identifier
            InvalidTransactionError: If the layer isn't associated with a Component
            IdentifierNotFoundError: If there is no layer with the provided identifier
            in the associated component
        """
        # Check if the layer is a root layer
        if self._is_root:
            raise InvalidTransactionError("A root layer can't have a parent")
        # Check if the identifier is of the same layer
        if self._identifier == identifier:
            raise InvalidTransactionError("A layer can't have itself as it's parent")
        # Check if the identifier exists in children
        if identifier in self._children:
            raise InvalidTransactionError(
                "The layer associated with the provided identifier is a child of the layer"
            )
        # Check if the layer belongs to a component
        if self._component is None:
            raise InvalidTransactionError(
                "A layer outside of a component can't have a parent"
            )

        # Check if the identifier belongs to a layer of the same component
        try:
            parent_layer = self._component.get_layer(identifier)
            # pylint: disable=[protected-access]
            parent_layer._children.append(self._identifier)
        except IdentifierNotFoundError as exc:
            raise IdentifierNotFoundError(
                "There is no layer with the provided identifier in the component"
            ) from exc

        self._parent = identifier

    def delete_parent(self) -> None:
        """
        reset parent property
        """
        if self._parent is not None and self._component is not None:
            parent_layer = self._component.get_layer(self._parent)
            # pylint: disable=[protected-access]
            parent_layer._children.remove(self._identifier)
            self._parent = None

    @property
    def children(self) -> list[Layer.Child]:
        """
        getter for the _children attribute

        Returns:
            list[Layer.Child]: list of children associated with the layer
        """
        return self._children

    def add_child(self, child: Layer.Child) -> None:
        """
        adds a child to a Layer

        Args:
            child (Layer.Child): child to be added

        Raises:
            InvalidTransactionError: If the provided layer is the layer itself
            InvalidTransactionError: If the layer isn't associated with a Component
            InvalidTransactionError: If the provided layer is a root layer
            InvalidTransactionError: If the provided layer already has a parent
            IdentifierNotFoundError: If there is no layer in the associated component
            with the provided identifier
        """
        if isinstance(child, Identifier):
            # Check if the identifier is of the same layer
            if child == self._identifier:
                raise InvalidTransactionError("A layer can't have itself as a child")
            # Check if the layer belongs to a component
            if self._component is None:
                raise InvalidTransactionError(
                    "A layer outside of a component can't have another layer as a child"
                )
            # Check if the identifier provided is the _parent attribute
            if child == self._parent:
                raise InvalidTransactionError(
                    "The layer associated with the provided identifier is the parent of the layer"
                )
            # Check if the identifier belongs to a layer of the same component
            try:
                child_layer = self._component.get_layer(child)
                if child_layer.is_root:
                    raise InvalidTransactionError(
                        "A root layer can't be a child of another layer"
                    )
                # pylint: disable=[protected-access]
                if child_layer._parent is not None:
                    raise InvalidTransactionError(
                        "The layer with the provided identifier already has a child"
                    )
                # pylint: disable=[protected-access]
                child_layer._parent = self._identifier
            except IdentifierNotFoundError as exc:
                raise IdentifierNotFoundError(
                    "There is no layer with the provided identifier in the component"
                ) from exc

        # Add the child
        self._children.append(child)

    def remove_child(self, child: Layer.Child) -> None:
        """
        remove a child from the Layer

        Args:
            child (Layer.Child): The child to be removed

        Raises:
            InvalidTransactionError: If the provided child isn't present
        """
        if child not in self._children:
            raise InvalidTransactionError(
                "The provided LayerChild isn't a child of the Layer"
            )
        # Remove child from _children attribute
        self._children.remove(child)
        # If the child is a layer
        if isinstance(child, Identifier) and self._component is not None:
            child_layer = self._component.get_layer(child)
            # pylint: disable=[protected-access]
            child_layer._parent = None

    def __stringify(self) -> str:
        return (
            # header
            f'layer {"root " if self._is_root else ""}'
            f"{self._identifier} {Layer.open_brace}{Layer.newline}"
            # type statement
            f'{Layer.tab}type "{self.import_library}" {self.import_name};{Layer.newline}'
            # props statement
            f"{Layer.tab}props {self.__stringify_value_dict(dictionary=self.props)};{Layer.newline}"
            # parent statement
            f'{Layer.tab}parent {self._parent if self._parent is not None else "null"};'
            f"{Layer.newline}"
            # children statement
            f"{Layer.tab}children {self.__stringify_layer_child_array(children=self._children)};"
            f"{Layer.newline}"
            # footer
            f"{Layer.closed_brace};"
        )

    def __stringify_value_dict(self, dictionary: dict[str, Layer.Value]) -> str:
        # dict stringified
        dict_string: str = ""
        pair_strings: list[str] = []
        for key in dictionary:
            pair_strings.append(f'"{key}" = {self.__stringify_value(dictionary[key])}')
        if len(pair_strings) > 0:
            dict_string = (
                f"{Layer.newline}{Layer.tab}"
                + f",{Layer.newline}{Layer.tab}".join(pair_strings)
                + f",{Layer.newline}"
            )
            dict_string = regex_substitute(r"(\t+)", r"\1\t", dict_string)
            dict_string = dict_string + "\t"
        return f"{Layer.open_brace}{dict_string}{Layer.closed_brace}"

    def __stringify_value_array(self, arr: list[Layer.Value]) -> str:
        # list stringified
        arr_string: str = ""
        item_strings: list[str] = []
        for item in arr:
            item_strings.append(self.__stringify_value(item))
        if len(item_strings) > 0:
            arr_string = (
                f"{Layer.newline}{Layer.tab}"
                + f",{Layer.newline}{Layer.tab}".join(item_strings)
                + f",{Layer.newline}"
            )
            arr_string = regex_substitute(r"(\t+)", r"\1\t", arr_string)
        return f"{Layer.open_bracket}{arr_string}{Layer.tab}{Layer.closed_bracket}"

    def __stringify_value(self, val: Layer.Value) -> str:
        if isinstance(val, bool):
            return str(val).lower()
        if isinstance(val, str):
            return f'"{val}"'
        if isinstance(val, Number):
            return str(val)
        if isinstance(val, PropReference):
            return str(val)
        if isinstance(val, dict):
            return self.__stringify_value_dict(val)
        if isinstance(val, list):
            return self.__stringify_value_array(val)
        return "null"

    def __stringify_layer_child_array(self, children: list[Layer.Child]) -> str:
        # children stringified
        children_string: str = ""
        children_strings: list[str] = []
        for child in children:
            if isinstance(child, str):
                children_strings.append(f'"{child}"')
            else:
                children_strings.append(str(child))
        if len(children_strings) > 0:
            children_string = (
                f"{Layer.newline}{Layer.tab}{Layer.tab}"
                + f",{Layer.newline}{Layer.tab}{Layer.tab}".join(children_strings)
                + f",{Layer.newline}{Layer.tab}"
            )
        return f"{Layer.open_bracket}{children_string}{Layer.closed_bracket}"

    def __check_eq_props(self, other: Layer) -> bool:
        return self.__check_eq_dict(self.props, other.props)

    def __check_eq_dict(self, a: dict[str, Value], b: dict[str, Value]) -> bool:
        if len(a) != len(b):
            return False
        for key in a:
            if key not in b:
                return False
            else:
                if isinstance(a[key], dict):
                    if not isinstance(b[key], dict):
                        return False
                    if not self.__check_eq_dict(a[key], b[key]):
                        return False
                elif isinstance(a[key], list):
                    if not isinstance(b[key], list):
                        return False
                    for item in a[key]:
                        if item not in b[key]:
                            return False
                else:
                    if a[key] != b[key]:
                        return False
        return True
