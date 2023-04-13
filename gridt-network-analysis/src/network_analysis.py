import networkx as nx
import matplotlib.pyplot as plt
from dateutil import parser
from datetime import datetime, timezone


def plot_network(nodes: list, edges: list) -> None:
    G = load_graph(nodes, edges)

    colors = [color for _, color in G.nodes('color')]
    positions = nx.spring_layout(G)
    labels = {
        n: f'{message}\n\n\n'
        for n, message in G.nodes('message')
        if message
    }

    nx.draw(G, pos=positions, node_color=colors, with_labels=True)
    nx.draw_networkx_labels(
        G, pos=positions, labels=labels, font_size=9, font_color='hotpink'
    )
    plt.show()


def load_graph(nodes: list, edges: list) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_nodes_from([(node, load_node_data(data)) for node, data in nodes])
    G.add_edges_from([(edge[0], edge[1]) for edge in edges])
    return G


def load_node_data(data: dict) -> dict:
    if data is None:
        return {'color': 'pink'}

    time = parser.parse(data['time_stamp'])
    if (datetime.now(timezone.utc) - time).days > 0:
        return {'color': 'pink'}

    return {'color': 'hotpink', 'message': data['message']}
