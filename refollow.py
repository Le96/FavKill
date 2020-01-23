#!/usr/bin/env python3


import html
import time
import sys
from datetime import datetime

import tweepy

from env.access_token import ACCESS_TOKEN
from env.consumer import CONSUMER_KEY, CONSUMER_SECRET



AUTHORS_PATH = './env/liked_tweet_authors.log'
FOLLOW_LIST_PATH = './env/lta_sort_uniq.log'
LOGFILE_PATH = './env/logfile'
POINTER = None
REDIRECT = 'https://github.com/Le96/FavKill'
USER = '__Li96__'


def acquire_author_name(api: tweepy.API, start_pointer: int):
    liked_list = list(map(lambda item: int(item.strip()),
                          open(LOGFILE_PATH, 'r').readlines()))

    index = start_pointer
    while index < len(liked_list):
        try:
            print('[-]', 'try:', '#{:04d},'.format(index), liked_list[index],
                  end=' ')
            time.sleep(1)
            
            result = api.get_status(liked_list[index])
            print('OK.')
            print('[i]\t', 'username:', result.author.screen_name)
            with open(AUTHORS_PATH, 'a') as fp:
                fp.write(result.author.screen_name + '\n')
            
            index += 1
        except tweepy.error.TweepError as te:
            reason = te.reason.lower()
            if 'no status found' in reason or \
                    'not authorized' in reason or \
                    'suspended' in reason:
                if 'No status found' in reason:
                    print('Not Found.')
                elif 'not authorized' in reason:
                    print('Protected User.')
                else:
                    print('Suspended User.')
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


def follow(api: tweepy.API, start_pointer: int):
    follow_list = list(map(str.strip,
                           open(FOLLOW_LIST_PATH, 'r').readlines()))

    index = start_pointer
    while index < len(follow_list):
        try:
            print('[-]', 'try:', '#{:04d},'.format(index), follow_list[index],
                  end=' ')
            time.sleep(30)
            
            result = api.create_friendship(screen_name=follow_list[index],
                                           follow=False)
            print('OK.')
            print('[i]\t', 'username:', result.name)
            index += 1
        except tweepy.error.TweepError as te:
            reason = te.reason.lower()
            if 'no status found' in reason or \
                    'not authorized' in reason or \
                    'suspended' in reason:
                if 'No status found' in reason:
                    print('Not Found.')
                elif 'not authorized' in reason:
                    print('Protected User.')
                else:
                    print('Suspended User.')
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
    # acquire_author_name(api, start_pointer)
    follow(api, start_pointer)


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
                except BaseException:
                    print('[!]', 'Parse Error.', 'Please Try Again.')
            main(pointer)
    except (EOFError, KeyboardInterrupt):
        print('\n[!]', 'Goodbye!')
