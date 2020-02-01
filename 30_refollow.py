#!/usr/bin/env python3


from logging import INFO, basicConfig, getLogger

import tweepy
from const import AUTHOR_LATEST, ENV_PATH

USER = '__Li96__'

logger = getLogger(__name__)
basicConfig(level=INFO)


def follow(api: tweepy.API, start_pointer: int):
    from datetime import datetime
    from time import sleep

    from util import sort_and_uniq
    # FOLLOW_LIST_PATH = './env/lta_sort_uniq.log'
    # follow_list = list(map(str.strip,
    #                        open(FOLLOW_LIST_PATH, 'r').readlines()))
    follow_list = sort_and_uniq(map(str.strip,
            open(ENV_PATH + AUTHOR_LATEST).readlines()))

    index = start_pointer
    while index < len(follow_list):
        username = follow_list[index]
        try:
            logger.info('Try: #{:04d}, {}'.format(index, username))
            sleep(4 * 60)

            result = api.create_friendship(screen_name=follow_list[index],
                                           follow=False)
            logger.info('OK. Username: {}'.format(result.name))
            index += 1
        except tweepy.error.TweepError as te:
            reason = te.reason.lower()
            if 'cannot find' in reason or \
                    'not authorized' in reason or \
                    'suspended' in reason:
                if 'cannot find' in reason:
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
    follow(api, start_pointer)


if __name__ == '__main__':
    try:
        from util import acquire_pointer
        main(acquire_pointer())
    except (EOFError, KeyboardInterrupt):
        logger.warning('Abort')
