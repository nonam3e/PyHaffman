import utils
import sys
import pathlib

def decompress():
    try:
        name = sys.argv[1]
        raw = open(name, "rb")
    except IndexError:
        print("Choose file to decompress")
        exit()
    if pathlib.Path(name).suffix != ".bubylda":
        print("File hasn't been compressed yet")
        exit()
    content = raw.read()
    utils.print_hashsum()


if __name__ == '__main__':
    decompress()

