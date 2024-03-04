import os
import sys
import logging
import locale
from pathlib import Path
from nfp.servicos.arquivos import abrir_json
from nfp.servicos.chrome import get_chrome_path
from nfp.servicos.conexao_bd import conecta_bd

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

logging.basicConfig(level='INFO')

VERSAO = '0.1.2'

BASEDIR = os.path.dirname(__file__)
CONFIG_FILE = "config_maquina.json"

URLBASE = r'https://www.nfp.fazenda.sp.gov.br/EntidadesFilantropicas/CadastroNotaEntidadeAviso.aspx'
INITIAL_FOLDER = ''
DEBUG = False
EXIBIR_POPUP_RESULT = False
CHREXEC = "google-chrome"
if sys.platform == "win32":
    CHREXEC = get_chrome_path()

config_maq = abrir_json(os.path.join(BASEDIR, CONFIG_FILE))

if config_maq:
    try:
        INITIAL_FOLDER = config_maq['dir_planilhas']

        if config_maq['debug_db'] == 'Sim':
            DEBUG = True
        if config_maq['popup_resultados'] == 'Sim':
            EXIBIR_POPUP_RESULT = True
        CHREXEC = config_maq['path_chrome']
        URLBASE = config_maq['url_base']
    except:
        pass
       
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

CONEXAO = conecta_bd(URI, DEBUG)
