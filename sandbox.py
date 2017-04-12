import sys
from pathlib import Path
import logging

from pymemcache.client.base import Client


client = Client(('localhost', 11211))
log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    _, inname, outname = sys.argv

    run(inname, outname)


def run(inname, outname):
    inpath = Path(inname)
    with inpath.open('rb') as f:
        indata = f.read()

    set_file(inname, indata)

    outdata = get_file(inname)

    outdata = indata

    outpath = Path(outname)
    with outpath.open('wb') as f:
        f.write(outdata)


def set_file(name, data):
    """Store a file in memcache by its name."""
    for index, chunk in get_chucks(data):
        key = get_key(name, index)
        log.info("Set %s = %s", key, len(chunk))
        client.set(key, chunk)


def get_file(name):
    """Retrieve a file from memcache by its name."""
    data = b''
    index = 0
    while True:
        key = get_key(name, index)
        chunk = client.get(key)
        if not chunk:
            break

        log.info("Get %s = %s", key, len(chunk))
        data += chunk
        index += 1

    return data


def get_chucks(data, max_bytes=1_000_000):
    for index in range(0, len(data), max_bytes):
        yield index, data[index:index + max_bytes]


def get_key(name, index):
    return f"{name}-{index}"


if __name__ == '__main__':
    main()
