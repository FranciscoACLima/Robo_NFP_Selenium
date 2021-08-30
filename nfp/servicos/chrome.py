"""Funcionalidades para verificação da lidar com as versoes do chrome-driver"""
import logging
import os
import stat
import sys
from shutil import rmtree
from urllib import request

import requests
from nfp import BASEDIR, CHRDRIVER, CHREXEC
from nfp.servicos.utilitarios_cmd import (executar_comando,
                                          executar_comando_com_retorno)


def baixar_arquivo(arquivo, origem, destino):
    url = origem + '/' + arquivo
    print(url)
    destino = os.path.join(destino, arquivo)
    request.urlretrieve(url, destino)
    response = destino
    return str(response)


def descompactar(arquivo, path):
    import zipfile
    with zipfile.ZipFile(arquivo, 'r') as zip_ref:
        zip_ref.extractall(path)


def conferir_chrome():
    v_chrome = get_versao_chrome()
    v_driver = get_versao_chromedriver()
    if v_chrome == v_driver:
        return True, v_chrome, v_driver
    try:
        baixar_chromedriver(v_chrome)
        return True, v_chrome, v_driver
    except Exception as e:
        logging.warning(e)
        return False, v_chrome, v_driver


def get_versao_chrome():
    if sys.platform == "win32":
        return _get_versao_chrome_windows()
    cmd = CHREXEC
    args = ['--version']
    marca = 'Google Chrome '
    res, err = executar_comando(cmd, *args, debug=True)
    if err:
        raise Exception('Erro ao capturar a versao do Google Chrome: {}'.format(err))
    res = res.decode('ascii')
    pos_i = res.find(marca)
    pos_f = res.find('.')
    return int(res[pos_i + len(marca): pos_f])


def get_versao_chromedriver():
    try:
        cmd = CHRDRIVER
        args = ['--version']
        marca = 'ChromeDriver '
        res, err = executar_comando(cmd, *args, debug=True)
        if err:
            raise Exception('Erro ao capturar a versao do Chromedriver: {}'.format(err))
        res = res.decode('ascii')
        pos_i = res.find(marca)
        pos_f = res.find('.')
        return int(res[pos_i + len(marca): pos_f])
    except Exception as e:
        logging.warning(f'Chrome driver nao encontrado {e}')
        return ''


def _get_versao_chrome_windows():
    exec_chrome = CHREXEC.replace('/', '\\').replace('\\', '\\\\')
    cmd = r'wmic datafile where name="{}" get Version /value'.format(exec_chrome)
    result = executar_comando_com_retorno(cmd)
    if not('Version' in result):
        return 0
    pos_i = result.find('=')
    pos_f = result.find('.')
    return int(result[pos_i + 1: pos_f])


def baixar_chromedriver(versao):
    sistema = 'linux64'
    platform = sys.platform
    if platform == 'win32':
        sistema = 'win32'
    elif platform == 'darwin':
        sistema = 'mac_64'
    url = f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{versao}'
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f'Erro ao buscar ultimo release chromedriver versao {versao} - cod {r.status_code}')
    print(r.status_code)
    last_release = r.content.decode('utf-8')
    arquivo = f'chromedriver_{sistema}.zip'
    destino = os.path.join(BASEDIR, 'binaries')
    if os.path.isdir(destino):
        rmtree(destino)
    os.mkdir(destino)
    url = f'https://chromedriver.storage.googleapis.com/{last_release}'
    arq_zip = baixar_arquivo(arquivo, url, destino)
    print(arq_zip)
    descompactar(arq_zip, destino)
    if platform != 'win32':
        os.chmod(CHRDRIVER, 0o755)


# ----------------------------------------------
if __name__ == "__main__":
    versao = get_versao_chrome()
    print(versao)
    baixar_chromedriver(versao)
