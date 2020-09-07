""" Configurações """
import os
import logging


URLBASE = r'https://www.nfp.fazenda.sp.gov.br/EntidadesFilantropicas/CadastroNotaEntidadeAviso.aspx'

dir_path = os.path.dirname(__file__)
CHRDRIVER = os.path.join(dir_path, 'binaries', 'chromedriver.exe')


CHREXEC = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

CHRPREFS = r"C:\DevApps\source\Robo_NFP_Selenium\prefs_chrome"

logging.info('CHRDRIVER: {}'.format(CHRDRIVER))
