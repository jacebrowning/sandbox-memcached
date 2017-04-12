from pymemcache.client.base import Client


def main():
    client = Client(('localhost', 11211))

    client.set('foobar', 'Hello, world!')

    result = client.get('foobar')
    print(result)

    result = client.get('missing')
    print(result)


if __name__ == '__main__':
    main()
