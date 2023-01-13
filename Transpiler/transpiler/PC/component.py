"""Component for ".pc" DSL"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from re import sub as regex_substitute

from .identifier import Identifier
from .errors import IdentifierNotFoundError, DuplicateIdentifierError

if TYPE_CHECKING:
    from .dsl import DSL  # pragma: no cover
    from .layer import Layer  # pragma: no cover


class Component:
    """Represents a ".pc" Component object"""

    def __init__(self, name: str) -> None:
        """
        Initialize a Component object

        Args:
            name (str): The value of the Identifier for the Component
        """
        self._dsl: Optional[DSL] = None
        self._identifier: Identifier = Identifier(name)
        self._props: set[Identifier] = set()
        self._layers: dict[Identifier, Layer] = {}

    def __eq__(self, other: Component) -> bool:
        if self._identifier != other.identifier:
            return False
        if self._props != other._props:
            return False
        if self._layers != other._layers:
            return False
        return True

    def __str__(self) -> str:
        return self.__stringify()

    def __repr__(self) -> str:
        component_string = self.__stringify()
        return regex_substitute(r"[\t\n]+", "", component_string)

    @property
    def identifier(self) -> Identifier:
        """
        getter for the _identifier attribute

        Returns:
            Identifier: The identifier of the Component
        """
        return self._identifier

    @property
    def props(self) -> set[Identifier]:
        """
        getter for the _props attribute

        Returns:
            set[Identifier]: The set of props associated to the component
        """
        return self._props

    def add_prop(self, identifier: Identifier) -> None:
        """
        adds a prop to the Component

        Args:
            identifier (Identifier): Identifier of the prop to be added

        Raises:
            DuplicateIdentifierError: If the component already has a prop with
            the same Identifier
        """
        if identifier in self._props:
            raise DuplicateIdentifierError(
                "The Component already has a prop with the same Identifier"
            )
        self._props.add(identifier)

    def delete_prop(self, identifier: Identifier) -> None:
        """
        deletes a prop from the component

        Args:
            identifier (Identifier): Identifier of the prop to be deleted

        Raises:
            IdentifierNotFoundError: If the provided Identifier does not match with
            any props in the component
        """
        if identifier not in self._props:
            raise IdentifierNotFoundError(
                "There is no matching prop with the provided Identifier"
            )
        self._props.remove(identifier)

    @property
    def layers(self) -> list[Layer]:
        """
        getter for the _components attribute

        Returns:
            list[Layer]: A list of layers in the Component object
        """
        return [*self._layers.values()]

    def get_layer(self, identifier: Identifier) -> Layer:
        """
        get a specific layer from the component

        Args:
            identifier (Identifier): The identifier of the layer to fetch

        Raises:
            IdentifierNotFoundError: If there is no matching layer
            for the provided identifier in the Component

        Returns:
            Layer: The layer matching the identifier provided
        """
        if identifier not in self._layers:
            raise IdentifierNotFoundError(
                "There is no matching layer with the provided Identifier in the Component"
            )
        return self._layers[identifier]

    def add_layer(self, layer: Layer) -> None:
        """
        adds a Layer to the component

        Args:
            layer (Layer): The Layer to be added

        Raises:
            DuplicateIdentifierError: If the component already has a layer with the same
            identifier as the provided layer
        """
        if layer.identifier in self._layers:
            raise DuplicateIdentifierError(
                "The Component already has a layer with the same identifier as the provided layer"
            )
        # pylint: disable=[protected-access]
        layer._component = self
        self._layers[layer.identifier] = layer

    def delete_layer(self, identifier: Identifier) -> None:
        """
        deletes a layer from the component
        Args:
            identifier (Identifier): The identifier of the layer to be deleted

        Raises:
            IdentifierNotFoundError: If there is no matching layer with
            the provided Identifier in the component
        """
        if identifier not in self._layers:
            raise IdentifierNotFoundError(
                "There is no matching layer with the provided Identifier in the Component"
            )
        associated_layer = self._layers[identifier]
        # pylint: disable=[protected-access]
        associated_layer._component = None
        del self._layers[identifier]

    def __stringify(self) -> str:
        # constants
        tab = "\t"
        newline = "\n"
        open_brace = "{"
        closed_brace = "}"

        prop_separator = ", "
        props_string = f"{prop_separator.join([identifier.value for identifier in sorted(self._props)])}"
        layers_string = (
            f"{newline.join([str(layer) for layer in self._layers.values()])}"
        )
        layers_string = regex_substitute(r"(\n)", r"\1\t", layers_string)
        return (
            # header
            f"component {self._identifier.value}({props_string}) {open_brace}"
            # layers
            f"{newline}{tab}{layers_string}{newline}"
            # footer
            f"{closed_brace};"
        )
