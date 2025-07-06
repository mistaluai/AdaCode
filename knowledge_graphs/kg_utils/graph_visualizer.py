from pyvis.network import Network
from rdflib import Graph, Namespace
from knowledge_graphs.topics_kg.builder.config import NAMESPACE, RELATIONSHIPS


class GraphVisualizer:
    """
    Visualizes an RDF knowledge graph using pyvis.
    """

    def __init__(self, ttl_path: str):
        self.graph = Graph()
        self.graph.parse(ttl_path, format="turtle")
        self.ns = Namespace(NAMESPACE)
        self.allowed_relations = {rel[0] for rel in RELATIONSHIPS}

    def visualize(self, output_html: str = "kg_visualization.html") -> None:
        net = Network(height="750px", width="100%", directed=True)
        net.force_atlas_2based()

        # Keep track of added nodes to avoid duplicates
        added_nodes = set()

        for subj, pred, obj in self.graph:
            subj_label = subj.split("/")[-1]
            pred_label = pred.split("/")[-1]
            obj_label = obj.split("/")[-1]

            if pred_label not in self.allowed_relations:
                continue

            # Add nodes if not already added
            if subj_label not in added_nodes:
                net.add_node(subj_label, label=subj_label, color="#FFD700")  # gold
                added_nodes.add(subj_label)

            if obj_label not in added_nodes:
                net.add_node(obj_label, label=obj_label, color="#87CEEB")  # sky blue
                added_nodes.add(obj_label)

            # Add edge with label = relation
            net.add_edge(subj_label, obj_label, label=pred_label, color="#666")

        # Save and open
        net.show(output_html, notebook=False)
        print(f"Graph saved to {output_html}")

if __name__ == "__main__":
    gv = GraphVisualizer("/kg.ttl")
    gv.visualize("topics_kg_graph.html")
