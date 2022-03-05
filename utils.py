import hashlib


def print_hashsum(content):
    md5 = hashlib.md5()
    md5.update(content)
    print(f'Checksum: {md5.hexdigest()}')


class BinaryNode:
    def __init__(self, prob, content, left=None, right=None):
        self.left = left
        self.right = right
        self.prob = prob
        self.content = content
        self.code = ''

    def get_codes(self,haffman_dict,code=''):
        current_code = code + str(self.code)
        if (self.left):
            self.left.get_codes(haffman_dict,current_code)
        if (self.right):
            self.right.get_codes(haffman_dict,current_code)
        if (not (self.left or self.right)):
            haffman_dict[self.content] = current_code

    def get_dict(self):
        haffman_dict = {}
        self.get_codes(haffman_dict)
        return haffman_dict