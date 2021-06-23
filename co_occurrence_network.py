import networkx as nx
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from stop_words import get_stop_words
from nltk.tokenize import sent_tokenize, TweetTokenizer
from string import punctuation
from pathlib import Path

#USER DEFINED VARIABLES 
URL = Path(r"./data/from_russia_w_love.txt") # location of the text document 

#ZOOM-IN controls the number of nodes you see
# If this number is set too low, you would only see a hairball 
ZOOM_IN = 20 

#instead of letting the script find key words for you
# you can define your own key words here 
# the user-defined key words will be plotted instead
USE_INSTEAD = [
    "secret",
    "service",
    "bond",
    "general",
    "colonel",
    "g",
    "rosa",
    "klebb",
    "comrade",
    "kerim",
    "james",
    "tatiana",
    "romanova",
    "red",
    "grant",
    "kronsteen",
    "q",
]
CASE_USE_INSTEAD = list(map(lambda x: x.title(), USE_INSTEAD))

def open_file_to_lower(url):
    """the function reads in a file and returns a lower case string

    Args:
        url ([file path]): [the location of the text document]

    Returns:
        [string]: [a string of text]
    """

    with open(url, "r", encoding="utf-8") as file_obj:
        text_string = file_obj.read().lower()
    return text_string

def final_list(G):
    """[summary]
    Note that this method is obsolete if you use the user-defined 
    variable `USE_INSTEAD`

    Args:
        G ([a graph object]): a complete network 

    Returns:
        [set]: a list of key words based on their vertex degrees
    """
    sorted_list_of_tuples = sorted(
        G.edges(data=True), key=lambda x: x[2]["count"], reverse=True
    )
    extract = sorted_list_of_tuples[0:ZOOM_IN]
    first_element, second_element = [], []
    for element in extract:
        first_element.append(element[0])
        second_element.append(element[1])
    return set(first_element + second_element)

def clean_network(str_obj):
    """the function filters out all stop words and punctuations and 
    returns a graph object
    

    Args:
        str_obj ([string]): [a string of text]

    Returns:
        [a graph object]: [the cleaned graph version of the string object]
    """
    G = nx.Graph()
    ignore_words = set(stopwords.words("english")) | set(punctuation)
    ignore_words = ignore_words | set(["“", "”", "‘", "’", "—"])
    ignore_words = ignore_words | set(list(get_stop_words("en")))
    sentences = sent_tokenize(str_obj)
    for sentence in sentences:
        words = TweetTokenizer().tokenize(sentence)
        filtered = [word.lower() for word in words if word.lower() not in ignore_words]
        for v in filtered:
            try:
                G.nodes[v]["count"] += 1
            except KeyError:
                G.add_node(v)
                G.nodes[v]["count"] = 1
            for w in filtered:
                if v == w:
                    continue
                try:
                    G.edges[v, w]["count"] += 1
                except KeyError:
                    G.add_edge(v, w, count=1)
    return G


def plot_G(G):
    """The function draws a graph object

    Args:
        G ([graph]): A networkX Graph object
    """
    counts = [G.edges[edge]["count"] for edge in G.edges]
    pos = nx.spring_layout(G)

    color_map = []
    for node in G:
        if G.degree(node) >= 10:
            color_map.append("#6a0dad")
        else:
            color_map.append("#478778")

    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=100, alpha=0.1)
    # fmt: off
    options = {
        "edge_cmap": plt.cm.Blues, 
        "width": 8,
        "edge_color": counts,
        "alpha":0.5,
    }
    # fmt: on
    nx.draw_networkx_edges(G, pos, **options)
    nx.draw_networkx_edges(G, pos, edge_color="#808080", alpha=0.5)

    labels = {}
    for node in G.nodes():
        labels[node] = node.title()

    nx.draw_networkx_labels(G, pos, labels, font_color="b", font_family="DejaVu Sans")
    plt.tight_layout()
    plt.show()

def back_up_draw_method():
    """[summary]
    This method is obsolete. I included it here for the sake of completeness
    The method draws an unweighted network 
    """
    G = nx.Graph()
    with open(URL, "r") as file_obj:
        for i, row in enumerate(file_obj):
            row = row.strip().split()
            if len(row) not in (0, 1):
                self_node = row[0]
                for neighbors in row[1:]:
                    G.add_edge(self_node, neighbors)
            elif len(row) == 1:
                if row[0] not in G:
                    nx.add_node(row[0])
            else:
                print(f"row {i+1} is empty")

    nx.draw_networkx(G)
    plt.gca().margins(0.15, 0.15)
    plt.show()

    nx.write_adjlist(G, "out.adjlist")

def main():
    file_lower = open_file_to_lower(URL)
    G = clean_network(file_lower)
    G_sub = G.subgraph(USE_INSTEAD)  # final_list(G)
    plot_G(G_sub)

if __name__ == "__main__":
    main()
