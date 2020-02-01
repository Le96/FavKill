#!/usr/bin/env python3


import html
import time
import sys
from datetime import datetime

from logging import INFO, basicConfig, getLogger

import tweepy

from const import ENV_PATH, FAVKILL_LATEST


LOGFILE_PATH = './env/logfile'
POINTER = None
REDIRECT = 'https://github.com/Le96/FavKill'
USER = '__Li96__'

logger = getLogger(__name__)
basicConfig(level=INFO)


def relike(api: tweepy.API, start_pointer: int) -> None:
    from datetime import datetime
    from time import sleep

    liked_list = list(map(lambda item: int(item.strip()),
                          open(ENV_PATH + FAVKILL_LATEST, 'r').readlines()))

    index = start_pointer
    while index < len(liked_list):
        id_ = liked_list[index]
        try:
            logger.info('Try: #{:04d}, {:d}'.format(index, id_))
            sleep(3)
    
            result = api.create_favorite(liked_list[index])
            logger.info('OK. Liked: {:d}'.format(result.id))
            logger.info('  ' + html.unescape(result.text.replace('\n', '').strip())[:30])
            
            index += 1
        except tweepy.error.TweepError as te:
            reason = te.reason
            if 'You have already' in reason or \
                    'No status found' in reason or \
                    'protected users' in reason:
                if 'You have already' in reason:
                    logger.warning('Already liked.')
                elif 'No status found' in reason:
                    logger.warning('Not found.')
                else:
                    logger.warning('Protected tweet.')
                index += 1
            elif 'might be automated' in reason or '429' in reason:
                if 'might be automated' in reason:
                    logger.error('Tool filter detected.')
                else:
                    logger.error('Rate limit exceeded.')
                waittime = int(600 - datetime.now().timestamp() % 600)
                logger.info('Waiting until the next x0 minutes.' +
                      '({} sec.)'.format(waittime))
                sleep(waittime)
                continue
            else:
                logger.error('Uncaught error: {}'.format(reason))
                break


def main(start_pointer: int) -> None:
    from util import create_api

    api = create_api(USER)

    # do
    relike(api, start_pointer)


if __name__ == '__main__':
    try:
        from util import acquire_pointer
        main(acquire_pointer())
    except (EOFError, KeyboardInterrupt):
        logger.warning('Abort')
