#!/usr/bin/env python3


from logging import INFO, basicConfig, getLogger

import tweepy


NSFW_TUPLE = ('🔞', 'nsfw')
USER = '_Le96_'

logger = getLogger(__name__)
basicConfig(level=INFO)


def delete_status(api: tweepy.API, status_id: int, log: bool = True) -> None:
    import os
    from const import ENV_PATH, FAVKILL_LATEST, FAVKILL_TIMESTAMP

    if log:
        with open(ENV_PATH + FAVKILL_TIMESTAMP, 'a') as log_fp:
            log_fp.write(str(status_id) + '\n')
        os.remove(ENV_PATH + FAVKILL_LATEST)
        os.symlink(FAVKILL_TIMESTAMP, ENV_PATH + FAVKILL_LATEST)

    # delete
    api.destroy_favorite(status_id)
    logger.info('Successfully deleted')


def check(status: tweepy.Status) -> bool:
    # 100%
    if any([hashtag['text'].lower() == 'todaysmazai' for hashtag
            in status.entities['hashtags']]):
        logger.info('Not delete: #TodaysMazai')
        return False
    if any([nsfw in status.text.lower() for nsfw in NSFW_TUPLE]):
        logger.info('Delete: NSFW instruction')
        return True
    # 80%
    if status.retweeted:
        logger.info('Not delete: Retweeted')
        return False
    if hasattr(status, 'possibly_sensitive') and \
            status.possibly_sensitive and status.favorite_count > 10:
        logger.info('Delete: Possibly sensitive')
        return True
    if status.in_reply_to_screen_name:
        logger.info('Not delete: Reply')
        return False
    # 50%
    if status.favorite_count < 75:
        logger.info('Not delete: Not popular')
        return False
    if 'media' not in status.entities or not any(media['type'] == 'photo'
                                                 for media in status.entities['media']):
        logger.info('Not delete: Photo is not found')
        return False
    logger.info('Delete: Default')
    return True


def main() -> None:
    from util import create_api

    api = create_api(USER)

    # do
    for counter, status in enumerate(tweepy.Cursor(api.favorites, id=USER, count=200).items()):
        logger.info('Try: #{:04d}, {:d}'.format(counter, status.id))
        logger.info('Text: {}'.format(
            status.text.replace('\n', '').strip()[:40]))

        if check(status):
            delete_status(api, status.id)


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        logger.warning('Abort')
