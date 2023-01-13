"""DSL for ".pc" DSL"""


from __future__ import annotations
from typing import TYPE_CHECKING

from re import sub as regex_substitute

from .errors import IdentifierNotFoundError, DuplicateIdentifierError

if TYPE_CHECKING:
    from .component import Component  # pragma: no cover
    from .identifier import Identifier  # pragma: no cover


class DSL:
    """Represents a ".pc" DSL object"""

    def __init__(self) -> None:
        """Initialise a DSL object"""
        self._components: dict[Identifier, Component] = {}

    def __eq__(self, other: DSL) -> bool:
        if self._components != other._components:
            return False
        return True

    def __str__(self) -> str:
        return self.__stringify()

    def __repr__(self) -> str:
        component_string = self.__stringify()
        return regex_substitute(r"[\t\n]+", "", component_string)

    @property
    def components(self) -> list[Component]:
        """
        getter for the _components attribute

        Returns:
            list[Component]: A list of components in the DSL object
        """
        return [*self._components.values()]

    def add_component(self, component: Component) -> None:
        """
        adds a Component to the DSL

        Args:
            component (Component): The Component to be added

        Raises:
            DuplicateIdentifierError: If the component has the same Identifier
            as an existing component of the DSL
        """
        if component.identifier in self._components:
            raise DuplicateIdentifierError(
                "The DSL object already has a component with\
                    the same identifier as the provided component"
            )
        # pylint: disable=[protected-access]
        component._dsl = self
        self._components[component.identifier] = component

    def get_component(self, identifier: Identifier) -> Component:
        """
        get a component of the DSL by providing its identifier

        Args:
            identifier (Identifier): Identifier of the Component to be fetched

        Raises:
            IdentifierNotFoundError: If there is no component matching with the provided Identifier

        Returns:
            Component: The Component matching the Identifier
        """
        if identifier not in self._components:
            raise IdentifierNotFoundError(
                "There is no matching component with the provided Identifier in the DSL"
            )
        return self._components[identifier]

    def delete_component(self, identifier: Identifier) -> None:
        """
        delete a component of the DSL by providing its identifier

        Args:
            identifier (Identifier): Identifier of the Component to be deleted

        Raises:
            IdentifierNotFoundError: If there is no component matching with the provided Identifier
        """
        if identifier not in self._components:
            raise IdentifierNotFoundError(
                "There is no matching component with the provided Identifier in the DSL"
            )
        component_associated = self._components[identifier]
        # pylint: disable=[protected-access]
        component_associated._dsl = None
        del self._components[identifier]

    def __stringify(self) -> str:
        # constants
        tab = "\t"
        newline = "\n"
        open_brace = "{"
        closed_brace = "}"

        components_string = newline.join(
            [str(comp) for id, comp in self._components.items()]
        )
        components_string = regex_substitute(r"(\n)", r"\1\t", components_string)

        return (
            f"dsl {open_brace}{newline}{tab}{components_string}{newline}{closed_brace};"
        )
