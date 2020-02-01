import logging

import tweepy


def acquire_pointer() -> int:
    import sys

    logger = logging.Logger(__name__)

    if 1 < len(sys.argv) and sys.argv[1].isdecimal():
        return int(sys.argv[1])

    pointer = -1
    buffer = ''
    while pointer < 0:
        buffer = input('Start with: ')
        try:
            pointer = int(buffer)
        except ValueError:
            logger.error('Interger parse error. Please try again.')
            continue
        if pointer < 0:
            logger.warn(
                'Specified pointer is negative value. Please try again.')

    return pointer


def create_api(target: str) -> tweepy.API:
    from env.credentials.access_token import ACCESS_TOKEN
    from env.credentials.consumer import CONSUMER_KEY, CONSUMER_SECRET

    logger = logging.Logger(__name__)

    # authentication credentials
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    try:
        auth.set_access_token(ACCESS_TOKEN[target]['KEY'],
                              ACCESS_TOKEN[target]['SECRET'])
    except KeyError:
        logger.error('username not found: ' + target)
        return None

    # api handler
    logger.info('successfully created')
    return tweepy.API(auth, wait_on_rate_limit=True,
                      wait_on_rate_limit_notify=True)


def sort_and_uniq(l: list) -> list:
    return sorted(set(l))