import os
from nfp.telas.nfp import Nfp


def gravar_nota(cod_nota, usuario, senha, mes, ano, entidade, driver=None):
    retorno = ''
    tela = Nfp(cod_nota, usuario, senha, mes, ano, entidade, driver)
    tela.default_sleep = 5
    if not driver:
        retorno = tela.abrir_pagina_login()
        if retorno:
            return retorno, None
        retorno = tela.logar()
        if retorno:
            return retorno, None
        tela.configurar_cadastro()
    return retorno, driver


if __name__ == "__main__":
    cod_nota = 'xxxxxxxxxxxx'
    usuario = os.environ['USER_NFP']
    senha = os.environ['SENHA_NFP']
    mes = '08'
    ano = '2020'
    entidade = 'CREN - CENTRO DE RECUPERAÇÃO E EDUCAÇÃO NUTRICIONAL'
    r, d = gravar_nota(cod_nota, usuario, senha, mes, ano, entidade)
    print(r)
