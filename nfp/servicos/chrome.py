"""Funcionalidades para verificação da lidar com as versoes do chrome-driver"""
import logging
import sys
from nfp import CHREXEC, CHRDRIVER
from nfp.servicos.utilitarios_cmd import executar_comando, executar_comando_com_retorno


def conferir_chrome():
    v_chrome = get_versao_chrome()
    v_driver = get_versao_chromedriver()
    if v_chrome == v_driver:
        return True, v_chrome, v_driver
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


# ----------------------------------------------
if __name__ == "__main__":
    pass
