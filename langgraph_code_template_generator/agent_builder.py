import argparse
from pathlib import Path
import yaml
from typing import Dict, List, Any


class AgentBuilder:
    # Template directory path
    TEMPLATE_DIR = Path("agent_builder_template")
    
    @classmethod
    def init_agent_template(cls, agent_name: str):
        """Create agent folder and an empty 'yaml' file

        Args:
            agent_name: Name of the agent to create
        """
        # Create base agents directory if it doesn't exist
        agents_base_dir = Path("agents")
        agents_base_dir.mkdir(exist_ok=True)

        # Create agent-specific directory
        agent_dir = agents_base_dir / agent_name
        agent_dir.mkdir(exist_ok=True)

        # Create YAML file with initial content
        yaml_file = agent_dir / f"design.yaml"
        
        # Read design yaml template
        template_path = cls.TEMPLATE_DIR / "design_yaml.txt"
        if not template_path.exists():
            raise ValueError(f"Template file not found at {template_path}")
            
        with open(template_path, 'r') as f:
            yaml_content = f.read()
        
        # Write the YAML content to the file
        with open(yaml_file, "w") as f:
            f.write(yaml_content)

    @classmethod
    def build_code_template(cls, agent_name: str):
        """Create the graph and the test python files as well as a 'puml' diagram

        Args:
            agent_name: Name of the agent to set up
        """
        design_data = cls._validate_design(agent_name)

        cls._create_graph_files(agent_name, design_data)
        cls._create_test_file(agent_name)
        cls._create_puml_file(agent_name, design_data)

    @classmethod
    def _validate_design(cls, agent_name: str) -> Dict[str, List[Dict[str, Any]]]:
        """Validate the design.yaml file structure

        Args:
            agent_name: Name of the agent to validate

        Returns:
            The parsed design data if valid

        Raises:
            ValueError: If design file is invalid or missing required elements
        """
        yaml_path = Path(f"agents/{agent_name}/design.yaml")

        if not yaml_path.exists():
            raise ValueError(f"Design file not found at {yaml_path}")

        with open(yaml_path, 'r') as f:
            design_data = yaml.safe_load(f)

        # Check if nodes list exists
        if not design_data or 'nodes' not in design_data or not isinstance(design_data['nodes'], list):
            raise ValueError("Design file must contain a 'nodes' list")
            
        # Check if START node is defined
        start_node_exists = any(node.get('name') == "START" for node in design_data['nodes'])
        if not start_node_exists:
            raise ValueError("Design file must contain a 'START' node")

        # Validate each node
        for i, node in enumerate(design_data['nodes']):
            if not isinstance(node, dict):
                raise ValueError(f"Node at index {i} must be a dictionary")

            if 'name' not in node:
                raise ValueError(f"Node at index {i} is missing a 'name' field")

            if 'description' not in node:
                raise ValueError(f"Node '{node.get('name', f'at index {i}')}' is missing a 'description' field")

            if 'connections' not in node or not isinstance(node['connections'], list):
                raise ValueError(f"Node '{node.get('name')}' must have a 'connections' list")

        return design_data

    @classmethod
    def _create_graph_files(cls, agent_name: str, design_data: Dict[str, List[Dict[str, Any]]]):
        """Create the graph.py and graph_builder.py files with the necessary classes

        Args:
            agent_name: Name of the agent
            design_data: The validated design data
        """
        nodes = design_data['nodes']

        # Read template files
        node_method_template_path = cls.TEMPLATE_DIR / "node_method.txt"
        edge_method_template_path = cls.TEMPLATE_DIR / "edge_method.txt"
        
        if not node_method_template_path.exists():
            raise ValueError(f"Template file not found at {node_method_template_path}")
        if not edge_method_template_path.exists():
            raise ValueError(f"Template file not found at {edge_method_template_path}")
            
        with open(node_method_template_path, 'r') as f:
            node_method_template = f.read()
        
        with open(edge_method_template_path, 'r') as f:
            edge_method_template = f.read()

        # Prepare node methods and conditional edge methods
        node_methods = []
        edge_methods = []

        # Generate node method for each node
        for node in nodes:
            node_name = node['name']
            node_desc = node['description']

            # Use the template for node methods
            node_method = node_method_template.format(
                node_name=node_name,
                node_desc=node_desc
            )
            
            if node_name != "START":
                node_methods.append(node_method)

            # Check if this node has more than one connection (needs conditional edge)
            if len(node['connections']) > 1:
                connections_str = ", ".join([f'"{conn}"' for conn in node['connections']])
                
                # Use the template for edge methods
                edge_method = edge_method_template.format(
                    node_name=node_name,
                    connections_str=connections_str
                )
                
                edge_methods.append(edge_method)

        # Create graph.py file
        cls._create_graph_py(agent_name, node_methods, edge_methods)
        
        # Create graph_builder.py file
        cls._create_graph_builder_py(agent_name, nodes)

    @classmethod
    def _create_graph_py(cls, agent_name: str, node_methods: List[str], edge_methods: List[str]):
        """Create the graph.py file with Node and Edge classes

        Args:
            agent_name: Name of the agent
            node_methods: List of node method implementations
            edge_methods: List of edge method implementations
        """
        # Read graph template
        template_path = cls.TEMPLATE_DIR / "graph.txt"
        if not template_path.exists():
            raise ValueError(f"Template file not found at {template_path}")

        with open(template_path, 'r') as f:
            template_content = f.read()

        # Replace template placeholders
        content = template_content.replace(">>>>>NODE_METHODS<<<<<", "".join(node_methods).strip())
        content = content.replace(">>>>>CONDITIONAL_EDGE_METHODS<<<<<", "".join(edge_methods).strip())

        # Write to file
        graph_file_path = Path(f"agents/{agent_name}/graph.py")
        with open(graph_file_path, 'w') as f:
            f.write(content)

    @classmethod
    def _create_graph_builder_py(cls, agent_name: str, nodes: List[Dict[str, Any]]):
        """Create the graph_builder.py file

        Args:
            agent_name: Name of the agent
            nodes: List of node definitions
        """
        # Read graph_builder template
        template_path = cls.TEMPLATE_DIR / "graph_builder.txt"
        if not template_path.exists():
            raise ValueError(f"Template file not found at {template_path}")
            
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Generate nodes code
        add_nodes_code = cls._generate_add_nodes_code(nodes)
        
        # Generate edges code
        regular_edges_code = cls._generate_regular_edges_code(nodes)
        conditional_edges_code = cls._generate_conditional_edges_code(nodes)
        edges_code = regular_edges_code + ("\n\n" + conditional_edges_code if conditional_edges_code else "")
        
        # Replace template placeholders
        content = template_content.replace(">>>>>NODES<<<<<", add_nodes_code.strip())
        content = content.replace(">>>>>EDGES<<<<<", edges_code.strip())
        
        # Write to file
        graph_builder_file_path = Path(f"agents/{agent_name}/graph_builder.py")
        with open(graph_builder_file_path, 'w') as f:
            f.write(content)

    @staticmethod
    def _generate_add_nodes_code(nodes):
        """Generate code for adding nodes to the graph"""
        code_lines = []
        for node in nodes:
            if node["name"] != "START":
                code_lines.append(f'        graph.add_node("{node["name"]}", self.nodes.{node["name"]}_node)')
        return "\n".join(code_lines)

    @staticmethod
    def _generate_conditional_edges_code(nodes):
        """Generate code for adding conditional edges to the graph"""
        code_lines = []
        for node in nodes:
            if len(node['connections']) > 1:
                destinations = ", ".join([f'{conn}: {conn}' if conn in ["START", "END"] else f'"{conn}": "{conn}"' for conn in node['connections']])
                code_lines.append(f'''        graph.add_conditional_edges(
            "{node["name"]}",
            self.edges.{node["name"]}_edge,
            {{
                {destinations}
            }}
        )''')
        return "\n".join(code_lines) if code_lines else ""

    @staticmethod
    def _generate_regular_edges_code(nodes):
        """Generate code for adding regular edges to the graph"""
        code_lines = []
        for node in nodes:
            if len(node['connections']) == 1:
                start_key = node["name"] if node["name"] in ["START", "END"] else f'"{node["name"]}"'
                end_key = node["connections"][0] if node["connections"][0] in ["START", "END"] else f'"{node["connections"][0]}"'
                code_lines.append(f'        graph.add_edge({start_key}, {end_key})')
        return "\n".join(code_lines) if code_lines else ""

    @classmethod
    def _create_test_file(cls, agent_name: str):
        """Create the test.py. The file contains a unittest TestCase class with:
         - methods for testing the entire workflow
         - methods for testing each node and edge.

        Args:
            agent_name: Name of the agent
        """
        # Read template files
        template_path = cls.TEMPLATE_DIR / "test_imports.txt"
        test_function_path = cls.TEMPLATE_DIR / "test_function.txt"
        node_test_method_path = cls.TEMPLATE_DIR / "node_test_method.txt"
        edge_test_method_path = cls.TEMPLATE_DIR / "edge_test_method.txt"
        
        # Validate template files exist
        for path in [template_path, test_function_path, node_test_method_path, edge_test_method_path]:
            if not path.exists():
                raise ValueError(f"Template file not found at {path}")
        
        # Read template contents
        with open(template_path, 'r') as f:
            import_content = f.read()
            
        with open(test_function_path, 'r') as f:
            test_function_template = f.read()
            
        with open(node_test_method_path, 'r') as f:
            node_test_method_template = f.read()
            
        with open(edge_test_method_path, 'r') as f:
            edge_test_method_template = f.read()
        
        # Get design data to generate node and edge tests
        design_data = cls._validate_design(agent_name)
        nodes = design_data['nodes']
        
        # Generate node test methods
        node_test_methods = []
        for node in nodes:
            node_name = node['name']
            if node_name != "START":  # Skip START node as it doesn't have an implementation
                node_desc = node['description']
                node_test = node_test_method_template.format(
                    node_name=node_name,
                    node_desc=node_desc
                )
                node_test_methods.append(node_test)
        
        # Generate edge test methods
        edge_test_methods = []
        for node in nodes:
            if len(node['connections']) > 1:  # Only create test for nodes with multiple connections
                node_name = node['name']
                connections_str = ", ".join([f'"{conn}"' for conn in node['connections']])
                edge_test = edge_test_method_template.format(
                    node_name=node_name,
                    connections_str=connections_str
                )
                edge_test_methods.append(edge_test)
        
        # Convert node and edge methods to class methods
        indented_node_methods = []
        for method in node_test_methods:
            indented_method = "    " + method.replace("\n", "\n    ")
            indented_node_methods.append(indented_method)
            
        indented_edge_methods = []
        for method in edge_test_methods:
            indented_method = "    " + method.replace("\n", "\n    ")
            indented_edge_methods.append(indented_method)
        
        # Convert snake_case to PascalCase for class name
        pascal_case_name = ''.join(word.capitalize() for word in agent_name.split('_'))
        
        # Format the test function template
        test_function_content = test_function_template.format(
            agent_name=pascal_case_name,
            input_dict='{"input": "Test input"}',
            node_test_methods="\n\n".join(indented_node_methods).strip(),
            edge_test_methods="\n\n".join(indented_edge_methods).strip()
        )
        
        # Combine imports and test function
        test_file_content = f"{import_content}\n\n{test_function_content}"

        # Write to file
        test_file_path = Path(f"agents/{agent_name}/test.py")
        with open(test_file_path, 'w') as f:
            f.write(test_file_content.strip())

    @classmethod
    def _create_puml_file(cls, agent_name: str, design_data: Dict[str, List[Dict[str, Any]]]):
        """Create the design.puml file for diagram visualization

        Args:
            agent_name: Name of the agent
            design_data: The validated design data
        """
        # Read PUML template
        template_path = cls.TEMPLATE_DIR / "design_puml.txt"
        if not template_path.exists():
            raise ValueError(f"Template file not found at {template_path}")
            
        with open(template_path, 'r') as f:
            template_content = f.read()
            
        nodes = design_data['nodes']
        
        # Generate nodes content
        nodes_content = ""
        for node in nodes:
            status = node.get('status', 'NOT_IMPLEMENTED')
            nodes_content += f'node {node["name"]} {status}_NODE_COLOR[\n  {node["name"]}\n]\n\n'
            
        # Generate edges content
        edges_content = ""
        for node in nodes:
            node_name = node["name"]
            for connection in node["connections"]:
                if connection == "END":
                    edges_content += f'{node_name} --> END\n'
                else:
                    edges_content += f'{node_name} --> {connection}\n'
                    
        # Replace template placeholders
        content = template_content.replace("@startuml agent_name", f"@startuml {agent_name}")
        content = content.replace(">>>>>NODES<<<<<", nodes_content.strip())
        content = content.replace(">>>>>EDGES<<<<<", edges_content.strip())
        
        # Write to file
        puml_file_path = Path(f"agents/{agent_name}/design.puml")
        with open(puml_file_path, 'w') as f:
            f.write(content)

    @classmethod
    def update_design_puml(cls, agent_name: str):
        """Regenerate the design.puml file based on the latest design.yaml content
        
        Args:
            agent_name: Name of the agent whose PUML file needs to be updated
        """
        # First validate the design to ensure it's correct
        design_data = cls._validate_design(agent_name)
        
        # Then regenerate the PUML file
        cls._create_puml_file(agent_name, design_data)


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description='Build and manage agent templates')

    # Add mutually exclusive argument group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--init_agent_template', metavar='agent_name', 
                       help='Initialize a new agent template with the given name')
    group.add_argument('--build_code_template', metavar='agent_name',
                       help='Build code template for the specified agent')
    group.add_argument('--update_design_puml', metavar='agent_name',
                       help='Update the PUML diagram for the specified agent')

    # Parse the arguments
    args = parser.parse_args()

    # Execute the appropriate function based on the arguments
    if args.init_agent_template:
        AgentBuilder.init_agent_template(args.init_agent_template)
    elif args.build_code_template:
        AgentBuilder.build_code_template(args.build_code_template)
    elif args.update_design_puml:
        AgentBuilder.update_design_puml(args.update_design_puml)
