#!/usr/bin/env python3


import time


import tweepy
from env.credentials import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, \
                            CONSUMER_KEY, CONSUMER_SECRET


def limit_handled(cursor: tweepy.Cursor) -> [tweepy.Status]:
    while True:
        try:
            yield cursor.next()
        except (tweepy.error.TweepError):
            print('[!]', 'Rate Limit Found. Waiting...')
            time.sleep(60)


def test(api, current):
    result = api.favorites(id='_Le96_', count=200)  # max_id=current)
    print(result)
    print(len(result))
    raise KeyboardInterrupt


def main() -> None:
    # authentication credentials
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    # api handler
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    # read current progress
    with open('logfile', 'r') as log_fp:
        log = sorted(list(map(int, log_fp.read().strip().split('\n'))))
        current = log[0]

    test(api, current)

    # do
    for status in tweepy.Cursor(api.favorites, id='_Le96_').items():
        print('[i]', 'status.text:', status.text)

        # check
        if any([ht['text'] == 'TodaysMazai' for ht
                in status.entities['hashtags']]):
            print('[-]', '#TodaysMazai found.')
            continue
        if 'media' not in status.entities or not any(
                [m['type'] == 'photo' for m in status.entities['media']]):
            print('[-]', 'Photo not found.')
            continue
        if status.favorite_count < 100 or status.retweet_count < 100:
            print('[-]', 'Tweet is not so popular.')
            continue

        # log
        print('[+]', 'delete:', status.id, status.text)

        # save
        with open('logfile', 'a') as log_fp:
            log_fp.write(status.id_str + '\n')

        # delete
        api.destroy_favorite(status.id)


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\n[!]', 'Goodbye!')
