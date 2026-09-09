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
    parser.add_argument('delay', nargs='?', type=int, default=3)

    return parser.parse_args(argv)


# gets the necessary tokens to request a URL
def getHomepage(session):
    page = session.get('https://fckaf.de/', timeout=10)
    page.raise_for_status()

    return html.fromstring(page.content)


def getDelayOptions(tree):
    values = tree.xpath('//*[@id="delay"]/option/@value')

    return {int(value): value for value in values}


def pickDelay(requested, options):
    return min(options, key=lambda delay: (abs(delay - requested), delay))


# extracts the short URL form an html
def extractShort(answer):
    tree = html.fromstring(answer.content)

    ret = tree.xpath('//*[@id="link"]')

    return ret[0].value


# requests a html for the given target and delay
def getShort(target, delay):
    with requests.Session() as session:
        tree = getHomepage(session)

        csrf = tree.xpath('//*[@id="csrf_token"]')[0].value
        delays = getDelayOptions(tree)

        if delays:
            chosen = pickDelay(delay, delays)
            if chosen != delay:
                print(
                    f'Requested delay of {delay} seconds is unavailable; '
                    f'using {chosen} seconds instead.',
                    file=sys.stderr,
                )
                delay = chosen
            delay = delays[delay]

        options = {
            'csrf_token': csrf,
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
