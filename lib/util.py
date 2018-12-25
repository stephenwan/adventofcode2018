import requests
import os
import time

input_url = 'https://adventofcode.com/2018/day/{}/input'


def get_token():
    return os.environ.get('ADVENTOFCODE_TOKEN')


def get_input(day, token, parser=None, break_lines=True):
    cookies = dict(session=token)
    resp = requests.get(input_url.format(day), cookies=cookies)
    if resp.status_code != 200:
        raise Exception(resp.content())
    input = resp.text
    if break_lines:
        return [l if parser is None else parser(l) for l in input.split('\n')]
    else:
        return input if parser is None else parser(input)


def get_input_from_file(path, parser=None, break_lines=True):
    with open(path, 'r') as f:
        input = f.read()
    if break_lines:
        return [l if parser is None else parser(l) for l in input.split('\n')]
    else:
        return input if parser is None else parser(input)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(f'{method.__name__}, {te - ts}')
        return result
    return timed
