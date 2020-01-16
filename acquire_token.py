#!/usr/bin/env python3


import os
import webbrowser

from http.server import BaseHTTPRequestHandler, HTTPServer

import autopep8
import tweepy

from env.consumer import CONSUMER_KEY, CONSUMER_SECRET


ENV_PATH = './env'
ACCESS_TOKEN_FILE = ENV_PATH + '/access_token.py'


def main() -> None:
    print('[i]', 'Please Verify This Application.')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    webbrowser.open(auth.get_authorization_url())
    srv = HTTPServer(('127.0.130.96', 13096), Handler)
    srv.handle_request()


class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def do_GET(self):
        # Parse Redirect Request from Twitter
        if not self.path.startswith('/?'):
            self.send_response(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(('<html><body>Authentication success. ' +
                          'Please close the browser.</body></html>').encode())

        # Parse Parameters
        params = self.path.split('?')[-1].split('&')
        token = params[0].split('=')[-1].strip()
        verifier = params[1].split('=')[-1].strip()

        # Acquire Credentials
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.request_token = {'oauth_token': token,
                              'oauth_token_secret': verifier}
        auth.get_access_token(verifier)

        # Ask username
        user_name = ''
        while not user_name:
            user_name = input('[?] Target Username: ')
            if not user_name:
                print('[!]', 'Parse Error.', 'Please Try Again.')
        user_name = user_name.strip()

        # Persistence Them
        os.makedirs(ENV_PATH, exist_ok=True)
        if os.path.isfile(ACCESS_TOKEN_FILE):
            from env.access_token import ACCESS_TOKEN
            new_access_token = ACCESS_TOKEN
        else:
            new_access_token = {}
        new_access_token[user_name] = {
            'KEY': auth.access_token,
            'SECRET': auth.access_token_secret
        }
        code = autopep8.fix_code('ACCESS_TOKEN = \\\n' +
                                 str(new_access_token).replace(', ', ',\n'))
        with open(ACCESS_TOKEN_FILE, 'w') as fp:
            fp.write(code)

        # Finish
        print('[i]', 'Credentials Are Successfully Acquired.')
        return


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\n[!]', 'Goodbye!')
