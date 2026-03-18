"""
The network of choice is a Tutte graph. It has a chromatic number of 3.
This program does the following:
1. Generates a Tutte graph
2. Assigns the graph a random coloring with 3 colors
3. Plots the graph with the assigned colors
4. Counts the initial number of conflicts
5. Attempts to reduce the number of conflicts using a simple local search algorithm
6. Plots the number of conflicts over time
"""
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
from networkx.classes import Graph

GRAPH_GEN_SEED = 2026
COLORING_SEED = 2026
NUM_COLORS = 3
MAX_GRAPH_TRAVERSAL_ATTEMPTS = 5

def main():
    random.seed(GRAPH_GEN_SEED)
    graph = nx.tutte_graph()
    random.seed(COLORING_SEED)
    color_graph_randomly(graph, NUM_COLORS)

    fig, ax = plt.subplots(1, 1)
    plot_graph(graph, ax, NUM_COLORS, 'Randomly Coloured Tutte Graph')
    plt.tight_layout()
    plt.show()

    print(f"Initial number of conflicts: {count_conflicts(graph)}")

    conflicts_over_time = repair_graph_coloring(graph, MAX_GRAPH_TRAVERSAL_ATTEMPTS)

    print(f"Final number of conflicts: {conflicts_over_time[-1]}")

    fig, ax = plt.subplots(1, 1)
    plot_graph(graph, ax, NUM_COLORS, 'Tutte Graph after Local Search Repair')
    plt.tight_layout()
    plt.show()

    plot_conflicts_over_time(conflicts_over_time)


def repair_graph_coloring(graph: Graph, max_traversals = MAX_GRAPH_TRAVERSAL_ATTEMPTS):
    '''
    Attempts to repair the graph coloring using a simple local search algorithm.
    :return: The number of conflicts of the graph after each node traversed and changed.
    '''
    conflicts_over_time = []
    done = False
    for i in range(max_traversals):
        if done:
            break
        for edge_idx, neighbors_dict in graph.adjacency():
            num_conflicts = count_conflicts(graph)
            conflicts_over_time.append(num_conflicts)
            if num_conflicts == 0:
                print(f"Found a valid coloring!")
                done = True             # Break out of the outer loop too
                break
            potential_conflicts  = [0 for _ in range(NUM_COLORS)]

            for neighbor, neighbor_attrs in neighbors_dict.items():
                nbr_color = graph.nodes[neighbor]['color']
                potential_conflicts[nbr_color] += 1

            color_to_change_to = potential_conflicts.index(min(potential_conflicts))
            graph.nodes[edge_idx]['color'] = color_to_change_to

    return conflicts_over_time


def color_graph_randomly(graph: Graph, num_colors = 3):
    for node in graph.nodes():
        graph.nodes[node]['color'] = random.randrange(0, num_colors)


def count_conflicts(graph: Graph):
    conflicts = 0
    for n, nbrs in graph.adj.items():
        for nbr, eattr in nbrs.items():
            if graph.nodes[n].get('color') == graph.nodes[nbr].get('color'):
                conflicts += 1
    return conflicts


def plot_conflicts_over_time(conflicts_over_time):
    plt.figure()
    plt.plot(conflicts_over_time)
    plt.title('Conflicts over time')
    plt.xlabel('Trial')
    plt.ylabel('Number of conflicts')
    plt.tight_layout()
    plt.show()


def plot_graph(graph: Graph, ax, num_colors: int, title: str):
    cmap = mpl.cm.Pastel1
    vmin, vmax = 0, num_colors - 1

    pos_bar = nx.spring_layout(graph, seed=GRAPH_GEN_SEED)
    colors_bar = [graph.nodes[n].get('color', 0) for n in graph.nodes()]
    nx.draw(graph,
            pos=pos_bar,
            ax=ax,
            cmap=cmap,
            node_color=colors_bar,
            vmin=vmin,
            vmax=vmax,
            width=1,
            with_labels=True
            )
    ax.set_title(title)


if __name__ == '__main__':
    main()