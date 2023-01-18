from typing import Dict, List, Any
from Dsl import Dsl
from dependency import Dependency
from PC.component import Component
from PC.layer import Layer
from PC.identifier import Identifier
from PC.prop_reference import PropReference


class Visitor:
    def __init__(self, dsl_instance: Dsl) -> None:
        """
        Initialize the visitor class
        Args:
            dsl_instance (Dsl): instance of DSL
        """
        self.dsl: Dsl = dsl_instance
        self.code: Dict[str, str] = {}
        self.dependencies: Dict[str, List[Dependency]] = {}
        self.active_component_id: str = str()

    def walk(self) -> Dict[str, str]:
        """
        Generate the code for all components
        Returns:
            Dict[str, str]: generated code for all components
        """

        for component in self.dsl.components:

            self.code[str(component.identifier)] = self.visit_componenet(component)

            dependencies_mui: List = []
            dependencies_custom: List = []

            for dependency in self.dependencies[str(component.identifier)]:

                if dependency.lib == "mui":
                    if not self.does_dependency_already_exists(
                        dependencies_mui, dependency.identifier
                    ):
                        dependencies_mui.append(str(dependency.identifier))

                else:
                    if not self.does_dependency_already_exists(
                        dependencies_custom, dependency.identifier
                    ):
                        dependencies_custom.append(str(dependency.identifier))

            imports_mui = "import {{{}}} from '@mui/material';".format(
                ", ".join(dependencies_mui)
            )

            imports_custom = "\n".join(
                [
                    "import {} from './{}';".format(comp, comp)
                    for comp in dependencies_custom
                ]
            )

            self.code[str(component.identifier)] = (
                imports_mui + imports_custom + self.code[str(component.identifier)]
            )

        return self.code

    def visit_componenet(self, component: Component) -> str:

        """
        Generate the code for a single component
        Args:
            component (Component): the component to generate code for
        Returns:
            str: generated code for the component
        """

        code: str = str()

        self.active_component_id = component.identifier

        root_layers: list = []

        for layer in component.layers:
            if layer._is_root:
                root_layers.append(layer.identifier)

        code += (
            f"function {str(component.identifier)}({', '.join([str(prop) for prop in component.props])})"
            + "{"
        )

        code += "    return ("

        if len(root_layers) > 1:
            code += "<>"

        for i in range(len(root_layers)):
            active_component = self.dsl.get_component(self.active_component_id)

            layer = active_component.get_layer(root_layers[i])

            code += self.visit_layer(layer)

        if len(root_layers) > 1:
            code += "</>"

        code += ")"

        code += "}"
        return code

    def visit_layer(self, layer: Layer) -> str:

        """
        Generate the code for a single layer
        Args:
        layer (Layer): the layer to generate code for
        Returns:
        str: generated code for the layer

        """

        if str(self.active_component_id) not in self.dependencies:
            self.dependencies[str(self.active_component_id)] = [
                Dependency(lib=layer.import_library, identifier=layer.import_name)
            ]
        else:
            self.dependencies[str(self.active_component_id)].append(
                Dependency(lib=layer.import_library, identifier=layer.import_name)
            )

        code: str = str()

        code += "<" + str(layer.import_name)

        code += self.resolve_props(layer.props)

        if len(layer.children) > 0:
            code += ">"

            for child in layer.children:

                if isinstance(child, str):
                    code += child
                elif isinstance(child, Identifier):
                    child_layer = self.dsl.get_component(
                        self.active_component_id
                    ).get_layer(child)

                    code += self.visit_layer(child_layer)
                elif isinstance(child, PropReference):
                    code += "{" + str(child.value) + "}"
                else:
                    raise ValueError("layer with unknown child type")

            code += "</" + str(layer.import_name) + ">"

        else:
            code += "/>"

        return code

    def resolve_props(self, props: dict) -> str:

        """
        Generate the code for the props of a layer
        Args:
        props (List[PropReference]): the props to generate code for
        Returns:
        str: generated code for the props

        """

        code: str = ""

        for key, value in props.items():
            if isinstance(value, str):
                code += " " + key + " = " + '"' + value + '"'
            elif isinstance(value, PropReference):
                code += " " + key + "= {" + str(value.value) + "}"
            elif isinstance(value, bool):
                code += " " + key + "= {" + bool(value) + "}"
            elif isinstance(value, (float, int)):
                code += " " + key + "= {" + str(value) + "}"
            elif isinstance(value, dict):
                code += " " + key + " = { " + self.resolve_value(value) + "}"
            elif isinstance(value, list):
                code += " " + key + " = { " + self.resolve_value(value) + "}"
            else:
                raise ValueError("invalid prop type")
        return code

    def resolve_value(self, value: Any) -> str:

        """
        Resolve a value to its appropriate string representation
        Args:
        value (Any): the value to resolve
        Returns:
        str: the string representation of the value
        """
        code: str = ""

        if isinstance(value, str):
            code += '"' + value + '"'
        elif isinstance(value, PropReference):
            code += str(value.Identifier)
        elif isinstance(value, bool):
            code += str(bool(value))
        elif isinstance(value, (float, int)):
            code += str(float(value))
        elif isinstance(value, dict):
            code += "{"

            for key, val in value.items():
                code += key + ":" + self.resolve_value(val) + ","

            code += "}"

        elif isinstance(value, any):
            code += "["

            for val in value:
                code += self.resolve_value(val) + ","

            code += "]"

        return code

    def does_dependency_already_exists(self, deps: list, dep: str) -> bool:

        """
        Check if a dependency already exists
        Args:
        dependencies (List[str]): the list of dependencies
        identifier (Identifier): the identifier of the dependency
        Returns:
        bool: True if the dependency already exists, False otherwise
        """
        return dep in deps
