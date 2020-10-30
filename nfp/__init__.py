import os
import sys
import logging
import locale
from pathlib import Path

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

logging.basicConfig(level='INFO')

try:
    from nfp.config import DEBUG
    DEBUG = DEBUG
except Exception:
    DEBUG = False

try:
    from nfp.config import EXIBIR_POPUP_RESULT
    EXIBIR_POPUP_RESULT = EXIBIR_POPUP_RESULT
except Exception:
    EXIBIR_POPUP_RESULT = True

try:
    from nfp.config import CHREXEC
    CHREXEC = CHREXEC
except Exception:
    if sys.platform == "win32":
        CHREXEC = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    else:
        CHREXEC = "google-chrome"

URLBASE = r'https://www.nfp.fazenda.sp.gov.br/EntidadesFilantropicas/CadastroNotaEntidadeAviso.aspx'

BASEDIR = os.path.dirname(__file__)

URI = os.path.join(BASEDIR, 'controle_execucao.db')

CHRDRIVER = os.path.join(BASEDIR, 'binaries', 'chromedriver')
if sys.platform == "win32":
    CHRDRIVER += '.exe'
logging.info('CHRDRIVER: {}'.format(CHRDRIVER))

CHRPREFS = os.path.join(BASEDIR, "prefs_chrome")
if not os.path.isdir(CHRPREFS):
    os.mkdir(CHRPREFS)
logging.info('CHRPREFS: {}'.format(CHRPREFS))

DIR_RESULT = os.path.join(Path.home(), 'resultados_nfp')
if not os.path.isdir(DIR_RESULT):
    os.mkdir(DIR_RESULT)
logging.info('DIR_RESULT: {}'.format(DIR_RESULT))
