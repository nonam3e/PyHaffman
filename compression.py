import utils
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
    counter= {}
    for letter in content:
        if counter.get(chr(letter)) == None:
            counter[chr(letter)] = 1
        else:
            counter[chr(letter)] += 1
    counter = sorted(counter.items(), key=lambda x: x[1])
    print(counter)

    utils.print_hashsum(content)


if __name__ == '__main__':
    compress()