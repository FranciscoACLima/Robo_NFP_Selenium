""" Configurações """
import os
import logging
from pathlib import Path

DEBUG = False

URLBASE = r'https://www.nfp.fazenda.sp.gov.br/EntidadesFilantropicas/CadastroNotaEntidadeAviso.aspx'

BASEDIR = os.path.dirname(__file__)

CHRDRIVER = os.path.join(BASEDIR, 'binaries', 'chromedriver')

CHREXEC = "google-chrome"

CHRPREFS = os.path.join(BASEDIR, "prefs_chrome")

URI = os.path.join(BASEDIR, 'controle_execucao.db')

logging.info('CHRDRIVER: {}'.format(CHRDRIVER))

DIR_RESULT = os.path.join(Path.home(), 'resultados_nfp')
