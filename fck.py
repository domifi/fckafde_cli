#!/usr/bin/env python3

import sys

import requests
from lxml import html


def main():
    try:
        args = getArgs()
        target = args[0]
        delay = args[1]

        print(getShort(target, delay))
    except:
        print('Uh, oh! Something went wrong')


# gets the arguments (target and delay)
def getArgs():
    delay = 5
    target = ''

    if len(sys.argv) == 2:
        target = sys.argv[1]
    elif len(sys.argv) == 3:
        target = sys.argv[1]
        delay = sys.argv[2]

    return [target, delay]


# gets the necessary tokens to request a URL
def getTokens():
    page = requests.get('https://fckaf.de/')
    tree = html.fromstring(page.content)

    token = tree.xpath('//*[@id="csrf_token"]')
    sessionID = page.cookies.get_dict()['session']

    return [token[0].value, sessionID]


# extracts the short URL form an html
def extractShort(answer):
    tree = html.fromstring(answer.content)

    ret = tree.xpath('//*[@id="link"]')

    return ret[0].value


# requests a html for the given target and delay
def getShort(target, delay):
    tokens = getTokens()

    options = {
        'csrf_token': tokens[0],
        'target': target,
        'delay': delay,
        'submit': 'Speichern'
        'session'
    }

    headers = {
        'Cookie': 'session=' + tokens[1]
    }

    answer = requests.post('https://fckaf.de/', data=options, headers=headers)

    return extractShort(answer)


if __name__ == "__main__":
    main()
