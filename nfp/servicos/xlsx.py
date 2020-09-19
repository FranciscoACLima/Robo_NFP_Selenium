# -*- coding: utf-8 -*-
"""Classe para criar e ler arquivos xlsx

módulo para lidar com arquivos do Excel no SikuliX
"""
import os
import fnmatch
from math import ceil
# from vendors_lib import xlrd, xlsxwriter
import xlrd
import xlsxwriter


class Xlsx(object):

    def __init__(self, arquivo=''):
        self.arquivo = arquivo
        self._diretorio = ''
        self.planilha = None
        self.linhas = []
        self.linhasTitulo = 1

    @property
    def diretorio(self):
        arquivo = self.arquivo
        separador = '\\'
        if '/' in arquivo:
            separador = '/'
        pos = arquivo.rfind(separador)
        if pos < 0:
            return ''
        return arquivo[:pos + 1]

    @property
    def nome(self):
        arquivo = self.arquivo
        separador = '\\'
        if '/' in arquivo:
            separador = '/'
        pos = arquivo.rfind(separador)
        if pos < 0:
            return ''
        return arquivo[pos + 1:]

    def abre(self):
        self.planilha = xlrd.open_workbook(self.arquivo, on_demand=True)

    def converteArqsDiretorioPlanilha(self, dir, tipo='pdf', file='lista_arquivos.xlsx'):
        lista = self.listaArquivos(dir)
        arquivo = dir + '/' + file
        linhas = [['processo', 'resultado']]
        for linha in lista:
            if not(tipo in linha):
                continue
            linhas.append([linha])
        self.grava(arquivo, linhas)

    def divide(self, qtde, num_inic=1, modo='planilhas', pacote=None):
        try:
            qtde = int(qtde)
        except Exception:
            raise ValueError('A quantidade tem que ser um numero')
        if qtde < 2:
            raise ValueError('A quantidade para dividir nao pode ser menor que 2')
        planilha = self.planilha
        plan = planilha.sheet_by_index(0)
        num_rows = plan.nrows
        if qtde >= num_rows:
            raise ValueError('Quantidade para dividir maior que quantidade de linhas')
        div = (float(num_rows) - 1) / qtde
        if modo == 'linhas':
            div = qtde
        div = ceil(div)
        titulo = plan.row_values(0)
        n = num_inic
        linhas = []
        nome_pacote = ''
        indice_pacote = 0
        if pacote:
            nome_pacote, indice_pacote = self.separaNumeroDoPacote(pacote)
        for i in range(1, num_rows):
            colunas = plan.row_values(i)
            if nome_pacote:
                prefx = nome_pacote
                sufx = str(indice_pacote)
                colunas += [prefx + '-' + sufx]
            linhas.append(colunas)
            if (i % div == 0) or (i == num_rows - 1):  # se está na quebra ou chegou ao final
                nome = 'Plan' + str(n)
                arq = self.diretorio + nome + '_' + self.nome
                linhas.insert(0, titulo)
                self.grava(arq, linhas, nome)
                linhas = []
                n += 1
                indice_pacote += 1
        return n - num_inic

    def separaNumeroDoPacote(self, pacote):
        lista = pacote.split('-')
        if len(lista) > 2:
            msg = 'Nome de pacote para expediente: {} invalido. Use apenas um "-" para separacao'.format(pacote)
            raise ValueError(msg)
        numero = int(lista[1])
        if numero:
            return lista[0], numero

    def grava(self, arquivo, linhas, nome='plan1'):
        planilha = self._criaNova(arquivo)
        plan = planilha.add_worksheet(nome)
        row = 0
        col = 0
        for linha in linhas:
            for celula in linha:
                plan.write(row, col, celula)
                col += 1
            row += 1
            col = 0
        planilha.close()

    def juntaPlanilhas(self, diretorio):
        planilha = self._criaNova(diretorio + '/plan_unificada.xlsx')
        plan1 = planilha.add_worksheet('plan1')
        lista = self.listaArquivos(diretorio, '*.xlsx')
        if not lista:
            return False
        row = 0
        col = 0
        inicio = 0
        for item in lista:
            if 'plan_unificada' in item:
                continue
            item = diretorio + '/' + item
            plan1, row, col, inicio = self._acrescentaPlan(item, plan1, row, col, inicio)
        planilha.close()
        return 1

    def _acrescentaPlan(self, arquivo, plan1, row, col, inicio):
        xlsx = Xlsx(arquivo)
        xlsx.abre()
        plan = xlsx.planilha.sheet_by_index(0)
        num_rows = plan.nrows
        for i in range(inicio, num_rows):
            linha = plan.row_values(i)
            for celula in linha:
                plan1.write(row, col, celula)
                col += 1
            col = 0
            if i == 0:
                inicio = self.linhasTitulo
            row += 1
        return plan1, row, 0, inicio

    def listaArquivos(self, diretorio, filtro='*.*'):
        if not(os.path.isdir(diretorio)):
            raise ValueError('Diretorio {} invalido'.format(dir))
        lista = fnmatch.filter(os.listdir(diretorio), filtro)
        lista.sort()
        return lista

    def _criaNova(self, caminho):
        # a opção constant_memory ajuda para os casos de planilhas muito grande
        planilha = xlsxwriter.Workbook(caminho)
        planilha.constant_memory = True
        return planilha


# -----------------------------------------------#
#                                                #
#               Funções de módulo                #
#                                                #
# -----------------------------------------------#

def extrai_linhas(plan, coluna=None, formato='dict', limpar_texto=True):
    plan = Xlsx(plan)
    plan.abre()
    sheet = plan.planilha.sheet_by_index(0)
    num_rows = sheet.nrows
    linhas = {}
    if formato == 'list':
        linhas = []
    for i in range(num_rows):
        linha = sheet.row_values(i)
        num = str(linha[coluna])
        if limpar_texto:
            num = num.replace('.', '').replace('-', '')
        if formato == 'list':
            linhas.append(num)
            continue
        linhas[num] = linha
    return linhas


def extrair_dados_planilhas(arquivo):
    lista_planilha = []
    wb = xlrd.open_workbook(arquivo)
    sheet = wb.sheet_by_index(0)
    for n in range(sheet.nrows):
        dados = []
        check_row = sheet.cell(n, 0).value
        if not check_row or 'proc' in str(check_row).lower():
            continue
        for c in range(sheet.ncols):
            planilha_value = sheet.cell(n, c).value
            planilha_value = str(planilha_value).strip()
            dados.append(planilha_value)
        lista_planilha.append(dados)
    del wb
    return lista_planilha


def extrai_diferenca(menor, maior, coluna=0, entrada='plan'):
    if entrada == 'lista':
        try:
            lista1 = [x.replace('.', '').replace('-', '') for x in menor]
        except AttributeError as e:
            print('Erro extrai_diferenca: ' + str(e))
            return -1, 'Lista de processos (menor) invalida'
    else:
        try:
            lista1 = extrai_linhas(menor, coluna, 'list')
        except AttributeError as e:
            print('Erro extrai_diferenca: ' + str(e))
            return -1, 'Lista de processos (menor) invalida'
    try:
        lista2 = extrai_linhas(maior, coluna, 'list')
    except AttributeError as e:
        print('Erro extrai_diferenca: ' + str(e))
        return -1, 'Lista de processos (maior) invalida'
    lista2_dic = extrai_linhas(maior, coluna)
    resultado = []
    qtde = 0
    for item in lista2:
        if not(item in lista1):
            qtde += 1
            resultado.append(lista2_dic[item])
    print('quantidade', qtde)
    if qtde <= 1:
        return 0, 'sem diferencas entre as colunas indicadas'
    retorno = maior.replace('.xlsx', '_diff.xlsx')
    plan = Xlsx()
    plan.grava(retorno, resultado)
    return qtde - 1, retorno


def criar_planilha(linhas, arquivo):
    plan = Xlsx()
    try:
        plan.grava(arquivo, linhas)
        del plan
    except xlsxwriter.exceptions.FileCreateError as e:
        return 1, str(e)
    return 0, ' Planilha criada com sucesso.\n {}\n '.format(arquivo)


# ------------------------------------------------#
if __name__ == '__main__':
    entradas = [
        ['888-99', '100,00', 'Autor 1', 'Reu 1', 'Juiz 1'],
        ['3333-55', '130,00', 'Autor 2', 'Reu 2'],
    ]
    criar_planilha(entradas, 'teste.xlsx')
