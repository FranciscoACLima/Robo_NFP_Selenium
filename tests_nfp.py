import os
from nfp.telas.nfp import Nfp
from nfp.utilitarios.arquivos import extrair_dados_planilhas, inserir_linha_arq_csv


def gravar_nota(cod_nota, tela):
    retorno = tela.gravar_nota(cod_nota)
    return retorno


def gravar_notas():
    plan = r"C:\Users\franc\Documents\Notas fiscais 2020\agosto\teste_1.xlsx"
    linhas = extrair_dados_planilhas(plan)
    usuario = os.environ['USER_NFP']
    senha = os.environ['SENHA_NFP']
    mes = '08'
    ano = '2020'
    entidade = 'CREN - CENTRO DE RECUPERAÇÃO E EDUCAÇÃO NUTRICIONAL'
    tela = Nfp(usuario, senha, mes, ano, entidade)
    # retorno = tela.abrir_pagina_login()
    # if retorno:
    #     return retorno, None
    # retorno = tela.logar()
    # if retorno:
    #     return retorno, None
    tela.configurar_cadastro()
    i = 1
    arq_result = r"C:\Users\franc\Documents\Notas fiscais 2020\agosto\result_teste_1.csv"
    for linha in linhas:
        cod_nota = linha[0]
        retorno = gravar_nota(cod_nota, tela)
        print('NF {} Retorno: {}'.format(i, retorno))
        i += 1
        inserir_linha_arq_csv(arq_result, [cod_nota, retorno])


# ---------------------------------
if __name__ == "__main__":
    gravar_notas()
