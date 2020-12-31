"""Funcionalidades para verificação da lidar com as versoes do chrome-driver"""
import sys
from nfp import CHREXEC, CHRDRIVER
from nfp.servicos.utilitarios_cmd import executar_comando


def conferir_chrome():
    v_chrome = get_versao_chrome()
    v_driver = get_versao_chromedriver()
    if v_chrome == v_driver:
        return True, v_chrome, v_driver
    return False, v_chrome, v_driver


def get_versao_chrome():
    cmd = CHREXEC
    args = ['--version']
    marca = 'Google Chrome '
    if sys.platform == "win32":
        cmd = r'wmic datafile where name="{}" get Version /value'.format(CHREXEC)
        args = []
        marca = '='
    res, err = executar_comando(cmd, *args, shell=False, debug=True)
    if err:
        raise Exception('Erro ao capturar a versao do Google Chrome: {}'.format(err))
    res = res.decode('ascii')
    pos_i = res.find(marca)
    pos_f = res.find('.')
    return int(res[pos_i + len(marca): pos_f])


def get_versao_chromedriver():
    cmd = CHRDRIVER
    args = ['--version']
    marca = 'ChromeDriver '
    res, err = executar_comando(cmd, *args, shell=False, debug=True)
    if err:
        raise Exception('Erro ao capturar a versao do Chromedriver: {}'.format(err))
    res = res.decode('ascii')
    pos_i = res.find(marca)
    pos_f = res.find('.')
    return int(res[pos_i + len(marca): pos_f])


# ----------------------------------------------
if __name__ == "__main__":
    pass
