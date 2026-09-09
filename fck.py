#!/usr/bin/env python3

import argparse
import sys

import requests
from lxml import html


def main():
    args = getArgs()

    try:
        print(getShort(args.target, args.delay))
    except Exception:
        print('Uh, oh! Something went wrong', file=sys.stderr)
        return 1

    return 0


# gets the arguments (target and delay)
def getArgs(argv=None):
    parser = argparse.ArgumentParser(description='Create a shortened fckaf.de URL.')
    parser.add_argument('target', metavar='URL')
    parser.add_argument('delay', nargs='?', type=int, default=5)

    return parser.parse_args(argv)


# gets the necessary tokens to request a URL
def getTokens(session):
    page = session.get('https://fckaf.de/', timeout=10)
    page.raise_for_status()
    tree = html.fromstring(page.content)

    token = tree.xpath('//*[@id="csrf_token"]')

    return token[0].value


# extracts the short URL form an html
def extractShort(answer):
    tree = html.fromstring(answer.content)

    ret = tree.xpath('//*[@id="link"]')

    return ret[0].value


# requests a html for the given target and delay
def getShort(target, delay):
    with requests.Session() as session:
        token = getTokens(session)

        options = {
            'csrf_token': token,
            'target': target,
            'delay': delay,
            'submit': 'Speichern'
        }

        answer = session.post(
            'https://fckaf.de/',
            data=options,
            timeout=10,
        )
        answer.raise_for_status()

        return extractShort(answer)


if __name__ == "__main__":
    raise SystemExit(main())
