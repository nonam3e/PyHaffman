import hashlib
import pathlib


def print_hashsum(content):
    try:
        pathlib.Path(content).is_file()
        content = open(content, "rb").read()
    except TypeError:
        pass
    finally:
        if isinstance(content, bytes):
            md5 = hashlib.md5()
            md5.update(content)
            print(f'Checksum: {md5.hexdigest()}')


def get_tree(prob_dict):
    counter = sorted(prob_dict.items(), key=lambda x: x[1])
    # print(counter)

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

    def get_codes(self, haffman_dict, code=''):
        current_code = code + str(self.code)
        if (self.left):
            self.left.get_codes(haffman_dict, current_code)
        if (self.right):
            self.right.get_codes(haffman_dict, current_code)
        if (not (self.left or self.right)):
            haffman_dict[self.content] = current_code

    def get_dict(self):
        haffman_dict = {}
        self.get_codes(haffman_dict)
        return haffman_dict
