
"""teste para abertua do navegador"""
from subprocess import Popen, PIPE
from nfp.servicos.interface import abrir_popup
from nfp import CHREXEC, CHRPREFS, URLBASE


def abrir_chrome():
    chrexec = '"{}" --remote-debugging-port=9222 --user-data-dir="{}" {}'.format(CHREXEC, CHRPREFS, URLBASE)
    chrexec = [
        CHREXEC,
        '--remote-debugging-port=9222',
        '--user-data-dir="{}"'.format(CHRPREFS),
        URLBASE
    ]
    Popen(chrexec, shell=False, stdout=PIPE).stdout
    msg = 'ROBÔ EM ESPERA\n\nFaça o login no sistema e responda ao captcha.\n'
    msg += 'Após o login, feche esta janela para iniciar a execução.\n'
    abrir_popup(msg)


def test_get_versao():
    from nfp.servicos.chrome import conferir_chrome
    print(conferir_chrome())


if __name__ == "__main__":
    test_get_versao()
