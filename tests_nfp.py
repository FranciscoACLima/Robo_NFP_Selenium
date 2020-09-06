import os
from nfp.telas.nfp import Nfp


def gravar_nota(cod_nota, usuario, senha, driver=None):
    retorno = ''
    tela = Nfp(cod_nota, usuario, senha, driver)
    tela.default_sleep = 5
    if not driver:
        retorno = tela.abrir_pagina_login()
        if retorno:
            return retorno, None
        retorno = tela.logar()
        if retorno:
            return retorno, None
    return retorno, driver


if __name__ == "__main__":
    cod_nota = 'xxxxxxxxxxxx'
    usuario = os.environ['USER_NFP']
    senha = os.environ['SENHA_NFP']
    r, d = gravar_nota(cod_nota, usuario, senha)
    print(r)
