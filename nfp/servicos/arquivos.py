import os
import xlrd
import csv
import json


def abrir_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as read_file:
            return json.load(read_file)
    except Exception:
        return None


def adicionar_dados_json(path, dados):
    try:
        with open(path, 'w') as write_file:
            json.dump(dados, write_file)
    except Exception as e:
        raise e


def criar_json_dados_robos(dir_config, nome_arquivo_robos):
    if not os.path.exists(dir_config):
        os.makedirs(dir_config)
    path_arquivo = os.path.join(dir_config, nome_arquivo_robos)
    if not os.path.exists(path_arquivo):
        with open(path_arquivo, 'w') as write_file:
            write_file.write("{}")


def extrair_dados_planilhas(arquivo, titulos=[], filtros=[]):
    """Extrai dados da planilha de acordo com regras pré-definidas

    Args:
        arquivo (str): caminho da planilha xls ou xlsx
        titulos (list, optional): título das colunas que serão utilizadas. Defaults to [].
        filtros (list, optional): filtros para definir as linhas de saída. Defaults to [].
        Modelo para filtros:
            filtros = [
                {
                    'regra': 'igual',
                    'valores': ['Execução Fiscal']
                },
                {
                    'regra': 'contem',
                    'valores': ['Embargos']
                },
                {
                    'regra': 'nao_contem',
                    'valores': ['AnaliseADV']
                },
            ]
    Returns:
        list: lista das linhas extraídas
    """
    lista_planilha = []
    try:
        wb = xlrd.open_workbook(arquivo)
    except UnicodeDecodeError:  # acionado para arquivos do tipo xls
        wb = xlrd.open_workbook(arquivo, encoding_override="windows-1252")
    sheet = wb.sheet_by_index(0)
    colunas = []
    for n in range(sheet.nrows):
        inserir = True
        if filtros:
            inserir = False
        dados = []
        check_row = sheet.cell(n, 0).value
        if not check_row:
            continue
        if not titulos and 'proc' in str(check_row).lower():
            continue
        for c in range(sheet.ncols):
            planilha_value = sheet.cell(n, c).value
            planilha_value = str(planilha_value).strip()
            if filtros:
                for filtro in filtros:
                    if filtro['regra'] == 'igual':
                        for regra in filtro['valores']:
                            if regra == planilha_value:
                                inserir = True
                    if 'contem' in filtro['regra']:
                        for regra in filtro['valores']:
                            if regra.lower() in planilha_value.lower():
                                inserir = True
                    if 'nao_contem' in filtro['regra']:
                        for regra in filtro['valores']:
                            if regra.lower() in planilha_value.lower():
                                inserir = False
                                continue
            if titulos:
                if len(colunas) != len(titulos):
                    if planilha_value in titulos:
                        colunas.append(c)
                        dados.append(planilha_value)
                    continue
                if c in colunas:
                    dados.append(planilha_value)
                    continue
            else:
                dados.append(planilha_value)
        if inserir:
            lista_planilha.append(dados)
    del wb
    return lista_planilha


def inserir_linha_arq_csv(arquivo, linha):
    with open(arquivo, 'a', newline='') as f:
        writer = csv.writer(f, delimiter=';', dialect='excel')
        writer.writerow(linha)
