import sys
from pathlib import Path
import logging

from pymemcache.client.base import Client
from pymemcache.client.murmur3 import murmur3_32


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

    outpath = Path(outname)
    with outpath.open('wb') as f:
        f.write(outdata)


def set_file(name, data):
    """Store a file in memcache by its name."""
    count = 0
    for index, chunk in get_chunks(data):
        key = get_key(name, index)
        log.info("Set %s = %s", key, len(chunk))
        client.set(key, chunk)
        count += 1

    key = get_key(name, 'count')
    client.set(key, count)
    log.info("Set expected count: %s", count)


def get_file(name):
    """Retrieve a file from memcache by its name."""
    key = get_key(name, 'count')
    expected_count = int(client.get(key))
    log.info("Get expected count: %s", expected_count)

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

    log.info("Get count: %s", index)
    assert index == expected_count

    return data


def get_chunks(data, max_bytes=1_000_000):
    for index in range(0, len(data), max_bytes):
        yield index // max_bytes, data[index:index + max_bytes]


def get_key(name, index):
    encoded = murmur3_32(name)
    return f"{encoded}-{index}"


if __name__ == '__main__':
    main()
