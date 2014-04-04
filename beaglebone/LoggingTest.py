import logging
import os
import time
import datetime

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y_%H-%M-%S')
path = 'log/%s.log' % st
log_path = '../log/%s.log' % st

os.path.exists(path)
logging.basicConfig(filename=log_path, level=logging.DEBUG)
logging.info(st)
logging.warning('MONGOLIAN')
logging.info('I like GREEN eggs and ham')
logging.debug('I do like them SAM I AM')