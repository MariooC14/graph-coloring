import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
from networkx.classes import Graph

GRAPH_GEN_SEED = 42
COLORING_SEED = None

def main():
    num_colors = 20

    tutte = nx.tutte_graph()
    random.seed(COLORING_SEED)

    color_random_graph(tutte, num_colors)

    print("Tutte graph coloring valid?", check_coloring(tutte))

    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    plot_graph(tutte, ax, num_colors, 'Tutte (colored)')

    plt.tight_layout()
    plt.show()


def color_random_graph(graph: Graph, num_colors = 10):
    for node in graph.nodes():
        graph.nodes[node]['color'] = random.randrange(0, num_colors)


def check_coloring(graph: Graph):
    for n, nbrs in graph.adj.items():
        for nbr, eattr in nbrs.items():
            if graph.nodes[n].get('color') == graph.nodes[nbr].get('color'):
                return False
    return True


def plot_graph(graph: Graph, ax, num_colors: int, title: str):
    cmap = mpl.cm.Pastel1
    vmin, vmax = 0, num_colors - 1

    pos_bar = nx.spring_layout(graph, seed=GRAPH_GEN_SEED)
    colors_bar = [graph.nodes[n].get('color', 0) for n in graph.nodes()]
    nx.draw(graph,
            pos=pos_bar,
            ax=ax,
            node_color=colors_bar,
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            width=1,
            with_labels=True
            )
    ax.set_title(title)


if __name__ == '__main__':
    main()