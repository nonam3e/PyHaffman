import utils
from utils import BinaryNode
import sys
import pathlib


def compress():
    try:
        name = sys.argv[1]
        raw = open(name, "rb")
    except IndexError:
        print("Choose file to compress")
        exit()
    if pathlib.Path(name).suffix == ".bubylda":
        print("File has already been compressed")
        exit()
    content = raw.read()
    counter = {}
    for letter in content:
        if counter.get(chr(letter)) is None:
            counter[chr(letter)] = 1
        else:
            counter[chr(letter)] += 1

    node = utils.get_tree(counter)
    codes = node.get_dict()

    print(codes)
    print(counter)
    raw_size = len(content) * 8
    compressed_size = 0
    for key in codes:
        compressed_size += len(codes[key]) * counter[key]

    print(f"raw: {raw_size} compressed without header: {compressed_size}")
    empty_bits = (8 - compressed_size % 8) % 8
    print(empty_bits)
    utils.print_hashsum(content)
    output = open(f"{pathlib.Path(name).stem}.bubylda", "wb")

    output.write(empty_bits.to_bytes(1, byteorder="big"))
    for key in counter:
        output.write(key.encode())
        output.write(counter[key].to_bytes(4, byteorder="big"))
    output.write((0).to_bytes(1, byteorder="big"))

    buffer = "0" * empty_bits
    for word in content:
        buffer += codes[chr(word)]
    #print(buffer)
    print(len(buffer))
    output.write(int(buffer, 2).to_bytes(len(buffer) // 8, byteorder='big'))


if __name__ == '__main__':
    compress()
