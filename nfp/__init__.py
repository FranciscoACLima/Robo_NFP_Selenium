import os
import logging
import locale
from nfp.config import DIR_RESULT

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

logging.basicConfig(level='INFO')

if not os.path.isdir(DIR_RESULT):
    os.mkdir(DIR_RESULT)
