from datetime import datetime


ENV_PATH = 'env/'

timestamp = datetime.strftime(datetime.now(), '%y%m%d%H%M%S')
LATEST = 'latest'

AUTHOR = 'author_log_'
AUTHOR_LATEST = AUTHOR + LATEST
AUTHOR_TIMESTAMP = AUTHOR + timestamp

FAVKILL = 'favkill_log_'
FAVKILL_LATEST = FAVKILL + LATEST
FAVKILL_TIMESTAMP = FAVKILL + timestamp
