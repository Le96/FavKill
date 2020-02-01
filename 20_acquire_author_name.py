#!/usr/bin/env python3


from logging import INFO, basicConfig, getLogger

import tweepy
from const import AUTHOR_LATEST, AUTHOR_TIMESTAMP, ENV_PATH,\
    FAVKILL_LATEST, FAVKILL_TIMESTAMP

USER = '__Li96__'

logger = getLogger(__name__)
basicConfig(level=INFO)


def acquire_author_name(api: tweepy.API, start_pointer: int):
    import os
    from datetime import datetime
    from time import sleep

    liked_list = list(map(lambda item: int(item.strip()),
                          open(ENV_PATH + FAVKILL_LATEST, 'r').readlines()))

    index = start_pointer
    while index < len(liked_list):
        id_ = liked_list[index]
        try:
            logger.info('Try: #{:04d}, {:d}'.format(index, id_))
            sleep(1)

            result = api.get_status(id_)
            logger.info('OK. Username: {}'.format(result.author.screen_name))

            author = ENV_PATH + AUTHOR_TIMESTAMP
            with open(author, 'a') as log_fp:
                log_fp.write(result.author.screen_name + '\n')
            os.remove(ENV_PATH + AUTHOR_LATEST)
            os.symlink(AUTHOR_TIMESTAMP, ENV_PATH + AUTHOR_LATEST)

            index += 1
        except tweepy.error.TweepError as te:
            reason = te.reason.lower()
            if 'no status found' in reason or \
                    'not authorized' in reason or \
                    'suspended' in reason:
                if 'No status found' in reason:
                    logger.warning('Not found.')
                elif 'not authorized' in reason:
                    logger.warning('Protected user.')
                else:
                    logger.warning('Suspended user.')
                index += 1
            elif 'might be automated' in reason or '429' in reason:
                if 'might be automated' in reason:
                    logger.error('Tool filter detected.')
                else:
                    logger.error('Rate limit exceeded.')
                waittime = int(600 - datetime.now().timestamp() % 600)
                logger.info('Waiting until the next x0 minutes. ' + 
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
    acquire_author_name(api, start_pointer)


if __name__ == '__main__':
    try:
        from util import acquire_pointer
        main(acquire_pointer())
    except (EOFError, KeyboardInterrupt):
        logger.warning('Abort')
