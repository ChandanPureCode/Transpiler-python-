from typing import Dict, List
from Dsl import Dsl
from dependency import Dependency
from PC.component import Component
from PC.layer import Layer

from PC.identifier import Identifier

from PC.prop_reference import PropReference


class Visitor:
    def __init__(self, dsl_instance: Dsl) -> None:
        self.dsl: Dsl = dsl_instance
        self.code: Dict[str, str] = {}
        self.dependencies: Dict[str, List[Dependency]] = {}
        self.active_component_id: str = str()

    def walk(self) -> Dict[str, str]:

        for component in self.dsl.components:

            self.code[component.identifier] = self.visit_componenet(component)

            dependencies_mui: List = []
            dependencies_custom: List = []

            print(self.code[component.identifier])

            for dependency in self.dependencies[component.identifier]:

                if dependency.lib == "mui":
                    if not self.does_dependency_already_exists(
                        dependencies_mui, dependency.comp
                    ):
                        dependencies_mui.append(dependency.comp)

                else:
                    if not self.does_dependency_already_exists(
                        dependencies_custom, dependency.comp
                    ):
                        dependencies_custom.append(dependency.comp)

            imports_mui = "import {{{}}} from '@mui/material';".format(
                ", ".join(dependencies_mui)
            )

            imports_custom = "\n".join(
                [
                    "import {} from './{}';".format(comp, comp)
                    for comp in dependencies_custom
                ]
            )

            self.code[component.identifier] = (
                imports_mui + imports_custom + self.code[component.identifier]
            )

        return self.code

    def visit_componenet(self, component: Component) -> str:

        print("component entering .....")

        code: str = str()

        self.active_component_id = component.identifier

        root_layers: list = []

        for layer in component.layers:

            print(layer.identifier)

            if layer.identifier.value.startswith("$id0"):

                root_layers.append(layer.identifier)

        code += f"def {component.identifier}({', '.join(component.props)}):"

        code += "    return ("

        print(root_layers)
        if len(root_layers) > 1:
            code += "<>"

        for i in range(len(root_layers)):
            active_component = self.dsl.components[self.active_component_id]
            layer = active_component.layers[root_layers[i]]
            code += self.visit_layer(layer)

        if len(root_layers) > 1:
            code += "</>"

        code += ")"

        code += "}"

        print("component exiting .....")

        return code

    def visit_layer(self, layer: Layer) -> str:

        print("entering layer ......")

        print(self.active_component_id)

        self.dependencies[self.active_component_id].append(
            Dependency(lib=layer.Type.Category, identifier=layer.Type.Identifier)
        )

        code: str = str()

        code += "<" + layer.import_name

        code += self.resolve_props(layer.props)

        if len(layer.children) > 0:
            code += ">"

            for child in layer.children:
                if isinstance(child, str):
                    code += child
                elif isinstance(child, Identifier):
                    layer = self.dsl.components[self.active_component_id].layers[
                        child.Identifier
                    ]
                    code += self.visit(layer)
                elif isinstance(child, PropReference):
                    code += "{" + child.Identifier + "}"
                else:
                    raise ValueError("layer with unknown child type")

            # component invocation closing tag
            code += "</" + layer.Type.Identifier + ">"
        else:
            # close opening tag
            code += "/>"

        return code

    def resolve_props(props: dict) -> str:
        """_summary_

        Args:
            props (dict): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """

        code = ""

        for key, value in props.items():
            if isinstance(value, str):
                code += f" {key}={value}"
            elif isinstance(value, PropReference):
                code += f" {key}={value.Identifier}"
            elif isinstance(value, bool):
                code += f" {key}={str(value)}"
            elif isinstance(value, (float, int)):
                code += f" {key}={str(value)}"
            elif isinstance(value, dict):
                code += f" {key}=" + "{" + parse_value(value) + "}"
            elif isinstance(value, list):
                code += f" {key}=[{','.join(parse_value(x) for x in value)}]"
            else:
                raise ValueError("invalid prop type")
        return code

    def parse_value(value) -> str:
        """_summary_

        Args:
            value (_type_): _description_

        Raises:
            ValueError: _description_

        Returns:
            str: _description_
        """

        if isinstance(value, str):
            return value
        elif isinstance(value, PropReference):
            return value.Identifier
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, (float, int)):
            return str(value)
        elif isinstance(value, dict):
            return ",".join([f"{key}:{parse_value(val)}" for key, val in value.items()])
        elif isinstance(value, list):
            return ",".join([parse_value(x) for x in value])
        else:
            raise ValueError("invalid prop type")

    def does_dependency_already_exists(deps: list, dep: str) -> bool:
        """_summary_

        Args:
            deps (list): _description_
            dep (str): _description_

        Returns:
            bool: _description_
        """
        return dep in deps
