import requests
import os

input_url = 'https://adventofcode.com/2018/day/{}/input'


def get_token():
    return os.environ.get('ADVENTOFCODE_TOKEN')


def get_input(day, token, parser=None):
    cookies = dict(session=token)
    resp = requests.get(input_url.format(day), cookies=cookies)
    if resp.status_code != 200:
        raise Exception(resp.content())
    lines = resp.text.strip().split('\n')
    return [l if parser is None else parser(l) for l in lines]


def get_input_from_file(path, parser=None):
    with open(path, 'r') as f:
        lines = f.read().strip().split('\n')
    return [l if parser is None else parser(l) for l in lines]
