#!/usr/bin/env python3


from env.credentials import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, \
                            CONSUMER_KEY, CONSUMER_SECRET

import tweepy
import twitter


LOGFILE_PATH = './env/logfile'


def test(api) -> None:
    # read current progress
    with open(LOGFILE_PATH, 'r') as log_fp:
        log = sorted(list(map(int, log_fp.read().strip().split('\n'))))
        current = log[0]
    print('oldest:', current)
    result = api.GetFavorites(screen_name='_Le96_', count=200, max_id=current)
    print(result)
    print('# of result:', len(result))


def main() -> None:
    # api handler
    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET,
                      sleep_on_rate_limit=True)
    assert api

    test(api)
    return

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
        with open(LOGFILE_PATH, 'a') as log_fp:
            log_fp.write(status.id_str + '\n')

        # delete
        api.destroy_favorite(status.id)


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\n[!]', 'Goodbye!')
