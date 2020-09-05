import os
import logging
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

logging.basicConfig(level='INFO')

dir_path = os.path.dirname(__file__)
CHRDRIVER = os.path.join(dir_path, 'binaries', 'chromedriver.exe')
logging.info('CHRDRIVER: {}'.format(CHRDRIVER))
