#!/usr/bin/env python3


import tweepy
from env.access_token import ACCESS_TOKEN
from env.consumer import CONSUMER_KEY, CONSUMER_SECRET


LOGFILE_PATH = './env/logfile'
REDIRECT = 'https://github.com/Le96/FavKill'
USER = '__Li96__'


def main() -> None:
    # authentication credentials
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('[!]', "can't acquire redirect_url.")
        return
    print(redirect_url)
    # token = session.get('request_token')
    # session.delete('request_token')
    # auth.request_token = {'oauth_token': token,
    #                       'oauth_token_secret': verifier}
    

    auth.set_access_token(ACCESS_TOKEN[USER]['KEY'],
                          ACCESS_TOKEN[USER]['SECRET'])

    # api handler
    api = tweepy.API(auth,
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\n[!]', 'Goodbye!')
