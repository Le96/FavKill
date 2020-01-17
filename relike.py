#!/usr/bin/env python3


import html
import time
import sys
from datetime import datetime

import tweepy

from env.access_token import ACCESS_TOKEN
from env.consumer import CONSUMER_KEY, CONSUMER_SECRET


LOGFILE_PATH = './env/logfile'
POINTER = None
REDIRECT = 'https://github.com/Le96/FavKill'
USER = '__Li96__'


def main(start_pointer: int) -> None:
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

    index = start_pointer
    while index < len(liked_list) + 1:
        try:
            print('[-]', 'try:', '#{:04d},'.format(index), liked_list[index],
                  end=' ')
            time.sleep(3)
            result = api.create_favorite(liked_list[index])
            print('Liked.')
            print('[i]\t',
                  html.unescape(result.text.replace('\n', '').strip())[:40])
            index += 1
        except tweepy.error.TweepError as te:
            reason = te.reason
            if 'You have already' in reason:
                print('Already Liked.')
                index += 1
            elif 'No status found' in reason:
                print('Not Found.')
                index += 1
            elif 'might be automated' in reason or '429' in reason:
                if 'might be automated' in reason:
                    print('Tool Filter Detected.')
                else:
                    print('Rate Limit Exceeded.')
                waittime = 600 - datetime.now().timestamp() % 600
                print('[i]\t', 'Waiting until the next x0 minutes.',
                        '({} sec.)'.format(int(waittime)))
                time.sleep(waittime)
                continue
            else:
                print('[!]', reason)
                break


if __name__ == '__main__':
    try:
        if POINTER:
            main(POINTER)
        elif 1 < len(sys.argv) and sys.argv[1].isdecimal():
            main(int(sys.argv[1]))
        else:
            pointer = -1
            while pointer < 0:
                try:
                    pointer = int(input('[?]', 'Start With:'))
                except:
                    print('[!]', 'Parse Error.', 'Please Try Again.')
            main(pointer)
    except (EOFError, KeyboardInterrupt):
        print('\n[!]', 'Goodbye!')
