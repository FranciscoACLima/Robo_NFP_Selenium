import os
from nfp.telas.nfp import Nfp


def gravar_nota(cod_nota, tela):
    retorno = tela.gravar_nota(cod_nota)
    return retorno


def gravar_notas():
    notas = [
        '35200713574594023480590008047871044653273229',
        '35200713574594023480590008047871044957896722',
        '35200713574594023480590008047871044969829596',
        '35200713574594023480590008047871044984635322',
        '35200713574594023480590008047871045101507791',
        '35200713574594023480590008047871044696054332',
        '35200713574594023480590008047871044796028724',
        '35200713574594023480590008047871044840250946',
        '35200713574594023480590008047871044901873794',
        '35200713574594023480590008047871045175496955',
        '35200713574594023480590008047871045190254576',
    ]
    usuario = os.environ['USER_NFP']
    senha = os.environ['SENHA_NFP']
    mes = '08'
    ano = '2020'
    entidade = 'CREN - CENTRO DE RECUPERAÇÃO E EDUCAÇÃO NUTRICIONAL'
    tela = Nfp(usuario, senha, mes, ano, entidade)
    retorno = tela.abrir_pagina_login()
    if retorno:
        return retorno, None
    retorno = tela.logar()
    if retorno:
        return retorno, None
    tela.configurar_cadastro()
    i = 1
    for cod_nota in notas:
        retorno = gravar_nota(cod_nota, tela)
        print('NF {} Retorno: {}'.format(i, retorno))
        i += 1


# ---------------------------------
if __name__ == "__main__":
    gravar_notas()
