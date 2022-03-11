import utils
import sys
import pathlib


def compress():
    name = ''
    raw = ''
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
    for item in content:
        letter = item.to_bytes(1, byteorder="big")
        if counter.get(letter) is None:
            counter[letter] = 1
        else:
            counter[letter] += 1

    node = utils.get_tree(counter)
    draw = False
    try:
        if sys.argv[2] == "draw":
            draw = True
    except IndexError:
        pass
    codes = node.get_dict(draw)

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
    output = open(f"{pathlib.Path(name)}.bubylda", "wb")

    output.write(empty_bits.to_bytes(1, byteorder="big"))
    for key in counter:
        output.write(key)
        output.write(counter[key].to_bytes(4, byteorder="big"))
    output.write(b'\x00')

    buffer = "0" * empty_bits
    for letter in content:
        buffer += codes[letter.to_bytes(1, byteorder="big")]
        while len(buffer) >= 8:
            output.write(int(buffer[7::-1], 2).to_bytes(1, byteorder='big'))
            buffer = buffer[8:]
    # print(buffer)
    # print(len(buffer))
    # output.write(int(buffer, 2).to_bytes(len(buffer) // 8, byteorder='big'))
    raw.close()
    output.close()


if __name__ == '__main__':
    compress()
