import utils
import sys
import pathlib


def decompress():
    raw = ''
    name = ''
    try:
        name = sys.argv[1]
        raw = open(name, "rb")
    except IndexError:
        print("Choose file to decompress")
        exit()
    if pathlib.Path(name).suffix != ".bubylda":
        print("File hasn't been compressed yet")
        exit()
    body_size = pathlib.Path(name).stat().st_size
    # print(f"file size: {body_size}")
    empty_bits = int.from_bytes(raw.read(1), "big")
    body_size -= 1
    counter = {}
    while True:
        char = raw.read(1)
        body_size -= 1
        if char == b'\x00':
            break
        prob = int.from_bytes(raw.read(4), "big")
        body_size -= 4
        counter[char] = prob
    print(counter)
    node = utils.get_tree(counter)
    draw = False
    try:
        if sys.argv[2] == "draw":
            draw = True
    except IndexError:
        pass
    node.get_dict(draw)
    # utils.print_hashsum(content)
    print(empty_bits)
    print(f"body size: {body_size}")
    buffer = int.from_bytes(raw.read(1), "big")
    body_size -= 1
    buffer = buffer >> empty_bits
    buffer_size = 8 - empty_bits
    current_node = node
    output = open(f"decompressed{pathlib.Path(name).stem}", "wb")
    while body_size >= 0:
        while buffer_size > 0:
            bit = buffer & 1
            if bit:
                current_node = current_node.right
            else:
                current_node = current_node.left
            if len(current_node.content) == 1:
                output.write(current_node.content)
                current_node = node
            buffer = buffer >> 1
            buffer_size -= 1
        buffer = int.from_bytes(raw.read(1), "big")
        body_size -= 1
        buffer_size = 8
    output.close()
    raw.close()
    utils.print_hashsum(f"decompressed{pathlib.Path(name).stem}")


if __name__ == '__main__':
    decompress()
