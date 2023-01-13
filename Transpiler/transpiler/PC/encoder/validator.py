"""Validator for ".pc" DSL"""

from __future__ import annotations
from typing import TYPE_CHECKING
from ..dsl import DSL
from ..identifier import Identifier
from ..prop_reference import PropReference

from ..errors import IdentifierNotFoundError

from .errors import StructuralIntegrityError

if TYPE_CHECKING:
    from ..layer import Layer  # pragma: no cover


def validate(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;

    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If the DSL's structural integrity is not valid
    """
    validate_min_one_root_layer(dsl)
    validate_no_orphan_non_root_layers(dsl)
    validate_no_unknown_parent_layers(dsl)
    validate_no_unknown_child_layers(dsl)
    validate_identifier_import_name_in_layer(dsl)
    validate_string_import_library_in_layer(dsl)
    validate_no_references_to_unknown_custom_component(dsl)
    validate_no_mismatching_props_in_references_to_custom_component(dsl)
    validate_no_unknown_prop_reference_in_layer_children(dsl)
    validate_no_unknown_prop_reference_in_layer_props(dsl)


def validate_min_one_root_layer(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;
    Verify there is at least one root layer in every component

    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If there are no root layers in any component
    """
    for component in dsl.components:
        # Group root layers
        root_layers: list[Layer] = []
        for layer in component.layers:
            if layer.is_root:
                root_layers.append(layer)

        # Verify there exists at least one root layer in a component
        if len(root_layers) == 0:
            raise StructuralIntegrityError(
                "Every component in a DSL must contain at least one root layer"
            )


def validate_no_orphan_non_root_layers(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;
    Verify there is at least one root layer in every component

    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If there are orphan non-root layers in any component
    """
    for component in dsl.components:
        # Group non-root layers
        non_root_layers: list[Layer] = []
        for layer in component.layers:
            if not layer.is_root:
                non_root_layers.append(layer)

        # Verify there exist no orphan non-root layer in a component
        for layer in non_root_layers:
            if layer.parent is None:
                raise StructuralIntegrityError(
                    f"An orphan non-root layer {layer.identifier}"
                    f" is found in component {component.identifier}"
                )


def validate_no_unknown_parent_layers(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;
    Verify there are no unknown parent layers


    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If there are any unknown parent layers
    """
    for component in dsl.components:
        # Group non-root layers
        non_root_layers: list[Layer] = []
        for layer in component.layers:
            if not layer.is_root:
                non_root_layers.append(layer)

        # Verify there are no layers with unknown parent layer
        for layer in non_root_layers:
            try:
                component.get_layer(layer.parent)
            except IdentifierNotFoundError as exc:
                raise StructuralIntegrityError(
                    f"The layer {layer.identifier} of component "
                    f"{component.identifier} has an unknown parent"
                ) from exc


def validate_no_unknown_child_layers(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;
    Verify there are no unknown child layers

    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If there are any unknown child layers
    """
    for component in dsl.components:
        # Verify there are no layers with unknown child layers
        for layer in component.layers:
            for child in layer.children:
                if isinstance(child, Identifier):
                    try:
                        component.get_layer(child)
                    except IdentifierNotFoundError as exc:
                        raise StructuralIntegrityError(
                            f"The layer {layer.identifier} of component "
                            f"{component.identifier} has an unknown child layer {child}"
                        ) from exc


def validate_identifier_import_name_in_layer(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;
    Verify the attribute import_name is an Identifier

    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If import_name attribute isn't an Identifier
    """
    for component in dsl.components:
        for layer in component.layers:
            if not isinstance(layer.import_name, Identifier):
                raise StructuralIntegrityError(
                    f"The layer {layer.identifier} of component "
                    f"{component.identifier} has import name of type other than an Identifier"
                )


def validate_string_import_library_in_layer(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;
    Verify the attribute import_library is a string

    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If import_library attribute isn't a string
    """
    for component in dsl.components:
        for layer in component.layers:
            if not isinstance(layer.import_library, str):
                raise StructuralIntegrityError(
                    f"The layer {layer.identifier} of component "
                    f"{component.identifier} has import library of type other than a string"
                )


def validate_no_references_to_unknown_custom_component(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;
    Verify there aren't any references to an unknown component

    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If a reference to an unknown component is found
    """
    for component in dsl.components:
        for layer in component.layers:
            if layer.import_library == "custom":
                try:
                    dsl.get_component(layer.import_name)
                except IdentifierNotFoundError as exc:
                    raise StructuralIntegrityError(
                        f"The layer {layer.identifier} of component "
                        f"{component.identifier} references an unknown component"
                    ) from exc


def validate_no_mismatching_props_in_references_to_custom_component(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;
    Verify there aren't any mismatched props in custom component references

    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If a reference to an unknown component is found
    """
    for component in dsl.components:
        for layer in component.layers:
            if layer.import_library == "custom":
                layer_props = list(layer.props.keys())
                custom_component = dsl.get_component(layer.import_name)
                custom_component_props = [
                    identifier.value for identifier in custom_component.props
                ]
                layer_props.sort()
                custom_component_props.sort()
                if layer_props != custom_component_props:
                    raise StructuralIntegrityError(
                        f"prop mismatch while invoking component {layer.import_name}"
                        f" in layer {layer.identifier}"
                    )


def validate_no_unknown_prop_reference_in_layer_children(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;
    Verify there aren't unknown props referenced in layer's children

    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If a reference to an unknown prop is found
    """
    for component in dsl.components:
        for layer in component.layers:
            for child in layer.children:
                if isinstance(child, PropReference):
                    if child.value not in component.props:
                        raise StructuralIntegrityError(
                            f"Reference to an unknown prop {child.value} "
                            f" in children of layer {layer.identifier} "
                            f"of component {component.identifier}."
                        )


def validate_no_unknown_prop_reference_in_layer_props(dsl: DSL) -> None:
    """
    Validate a DSL object for structural integrity;
    Verify there aren't unknown props referenced in layer's props

    Args:
        dsl (DSL): The DSL object to be validated

    Raises:
        StructuralIntegrityError: If a reference to an unknown prop is found
    """
    for component in dsl.components:
        for layer in component.layers:
            check_for_unknown_prop_in_obj(obj=layer.props, layer=layer)


def check_for_unknown_prop_in_obj(obj: dict[str, Layer.Value], layer: Layer) -> None:
    for key, value in obj.items():
        if isinstance(value, PropReference):
            if value.value not in layer._component.props:
                raise StructuralIntegrityError(
                    f"Reference to an unknown prop {value} "
                    f" in children of layer {layer.identifier} "
                    f"of component {layer._component.identifier}."
                )
        elif isinstance(value, dict):
            check_for_unknown_prop_in_obj(value, layer)
