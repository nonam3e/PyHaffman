import hashlib
import pathlib
import networkx as nx
import matplotlib.pyplot as plt


def print_hashsum(content):
    try:
        pathlib.Path(content).is_file()
        content = open(content, "rb").read()
    except TypeError:
        if isinstance(content, bytes):
            pass
    finally:
        md5 = hashlib.md5()
        md5.update(content)
        print(f'Checksum: {md5.hexdigest()}')


def get_tree(prob_dict):
    counter = sorted(prob_dict.items(), key=lambda x: x[1])

    nodes = []
    for item in counter:
        nodes.append(BinaryNode(content=item[0], prob=item[1]))

    while len(nodes) > 1:
        left = nodes[0]
        right = nodes[1]
        right.code = 1
        left.code = 0
        new_node = BinaryNode(prob=left.prob + right.prob, content=left.content + right.content, left=left, right=right)
        nodes.remove(right)
        nodes.remove(left)
        nodes.append(new_node)
        nodes = sorted(nodes, key=lambda x: x.prob)
        # for node in nodes:
        #     print(f"{node.content}:{node.prob}",end=' ')
        # print("\n----")
    return nodes[0]


class BinaryNode:
    def __init__(self, prob, content, left=None, right=None):
        self.left = left
        self.right = right
        self.prob = prob
        self.content = content
        self.code = ''

    def get_codes(self, haffman_dict, code='', G=None):
        current_code = code + str(self.code)
        if self.left:
            if G is not None:
                G.add_edge(f"{self.content}:{current_code}",
                           f"{self.left.content}:{current_code}0")
            self.left.get_codes(haffman_dict, current_code, G)
        if self.right:
            if G is not None:
                G.add_edge(f"{self.content}:{current_code}",
                           f"{self.right.content}:{current_code}1")
            self.right.get_codes(haffman_dict, current_code, G)
        if not (self.left or self.right):
            haffman_dict[self.content] = current_code

    def get_dict(self, make_plot=False):
        haffman_dict = {}
        if make_plot:
            G = nx.Graph()
            self.get_codes(haffman_dict, G=G)
            nx.draw_kamada_kawai(G, with_labels=True, node_size=500, font_size=8, font_weight="bold", node_color="purple")
            plt.show()
        else:
            self.get_codes(haffman_dict)

        return haffman_dict

    def dfs(self, G):
        if self.left:
            G.add_edge(f"{self.content}",
                       f"{self.left.content}")
            self.left.dfs(G)
        if self.right:
            G.add_edge(f"{self.content}",
                       f"{self.right.content}")
            self.right.dfs(G)

    def draw_tree(self):
        G = nx.Graph()
        self.dfs(G)
        nx.draw_kamada_kawai(G, with_labels=True)
        plt.show()
