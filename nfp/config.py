""" Configurações """
import os
import logging

DEBUG = False

URLBASE = r'https://www.nfp.fazenda.sp.gov.br/EntidadesFilantropicas/CadastroNotaEntidadeAviso.aspx'

BASEDIR = os.path.dirname(__file__)

CHRDRIVER = os.path.join(BASEDIR, 'binaries', 'chromedriver')

CHREXEC = "google-chrome"

CHRPREFS = r"/home/gil-2004/Aplicacoes/Robo_NFP_Selenium/prefs_chrome"

URI = os.path.join(BASEDIR, 'controle_execucao.db')

logging.info('CHRDRIVER: {}'.format(CHRDRIVER))

DIR_RESULT = os.path.join(BASEDIR, 'resultados')
