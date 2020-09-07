""" Configurações """
import os
import logging

DEBUG = True

URLBASE = r'https://www.nfp.fazenda.sp.gov.br/EntidadesFilantropicas/CadastroNotaEntidadeAviso.aspx'

BASEDIR = os.path.dirname(__file__)

CHRDRIVER = os.path.join(BASEDIR, 'binaries', 'chromedriver.exe')

CHREXEC = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

CHRPREFS = r"C:\DevApps\source\Robo_NFP_Selenium\prefs_chrome"

URI = os.path.join(BASEDIR, 'controle_execucao.db')

logging.info('CHRDRIVER: {}'.format(CHRDRIVER))
