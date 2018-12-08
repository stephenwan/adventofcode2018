import requests

input_url = 'https://adventofcode.com/2018/day/{}/input'


def get_input(day, token, parser=None):
    cookies = dict(session=token)
    resp = requests.get(input_url.format(day), cookies=cookies)
    if resp.status_code != 200:
        raise Exception(resp.content())
    lines = resp.text.strip().split('\n')
    return [l if parser is None else parser(l) for l in lines]
