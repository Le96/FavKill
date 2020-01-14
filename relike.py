#!/usr/bin/env python3


import time


import tweepy

from env.access_token import ACCESS_TOKEN
from env.consumer import CONSUMER_KEY, CONSUMER_SECRET


LOGFILE_PATH = './env/logfile'
REDIRECT = 'https://github.com/Le96/FavKill'
USER = '__Li96__'
POINTER = 283


def main() -> None:
    # authentication credentials
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN[USER]['KEY'],
                          ACCESS_TOKEN[USER]['SECRET'])

    # api handler
    api = tweepy.API(auth,
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    # do
    liked_list = list(map(lambda item: int(item.strip()),
                      open(LOGFILE_PATH, 'r').readlines()))

    for index in range(POINTER, len(liked_list) + 1):
        try:
            print('[i]', 'try:', '#', index, ',', liked_list[index])
            result = api.create_favorite(liked_list[index])
            print('[i]', 'liked:', result.text)
            index += 1
            time.sleep(3)
        except tweepy.error.TweepError as te:
            reason = te.reason
            if 'You have already' in reason:
                print('[i]', 'already liked.')
                index += 1
            elif 'No status found' in reason:
                print('[i]', 'not found.')
                index += 1
            elif '429' in reason:
                print('[i]', 'Rate Limit Exceeded.')
                # api.rate_limit_status()
                time.sleep(60)
                continue
            else:
                print('[!]', reason)
                break


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\n[!]', 'Goodbye!')
