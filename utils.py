import hashlib
def print_hashsum(content) :
    md5 = hashlib.md5()
    md5.update(content)
    print(f'Checksum: {md5.hexdigest()}')