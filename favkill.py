#!/usr/bin/env python3


import time

import tweepy
from env.access_token import ACCESS_TOKEN
from env.consumer import CONSUMER_KEY, CONSUMER_SECRET


LOGFILE_PATH = './env/logfile'
NSFW_TUPLE = ('🔞', 'nsfw')
USER = '_Le96_'


def delete_status(api: tweepy.API, status_id: int,
                  logging: bool = True) -> None:
    if logging:
        with open(LOGFILE_PATH, 'a') as log_fp:
            log_fp.write(str(status_id) + '\n')

    # delete
    api.destroy_favorite(status_id)
    print('[i]\t\t', 'Successfully Deleted.')


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
    counter = 0
    for status in tweepy.Cursor(api.favorites, id=USER, count=200).items():
        counter += 1
        print('[-]', 'try:', '#{:04d}'.format(counter), status.id)
        print('[i]\t', status.text.replace('\n', '').strip()[:40])

        # check
        # 100%
        if any([hashtag['text'].lower() == 'todaysmazai' for hashtag
                in status.entities['hashtags']]):
            print('[-]\t', 'Not Deleted:', '#TodaysMazai')
            # time.sleep(1)
            continue
        if any([nsfw in status.text.lower() for nsfw in NSFW_TUPLE]):
            print('[+]\t', 'Deleted:', 'NSFW Instruction')
            delete_status(api, status.id)
            # time.sleep(1)
            continue
        # 80%
        if status.retweeted:
            print('[-]\t', 'Not Deleted:', 'Retweeted')
            # time.sleep(1)
            continue
        if hasattr(status, 'possibly_sensitive') and\
                status.possibly_sensitive and status.favorite_count > 10:
            print('[+]\t', 'Deleted:', 'Possibly Sensitive')
            delete_status(api, status.id)
            # time.sleep(1)
            continue
        if status.in_reply_to_screen_name:
            print('[-]\t', 'Not Deleted:', 'Reply')
            # time.sleep(1)
            continue
        # 50%
        checked = False
        if status.favorite_count < 75:
            print('[i]\t', 'Not Deleted?:', 'Not Popular')
            checked = True
        if 'media' not in status.entities or not any([media['type'] == 'photo'
                                                      for media in status.entities['media']]):
            print('[i]\t', 'Not Deleted?:', 'Photo Not Found')
            checked = True
        # last resort
        if not checked:
            print('[+]\t', 'Deleted:', 'Default')
            delete_status(api, status.id)
        # time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\n[!]', 'Goodbye!')
