import math
import os

import pandas as pd
from nfp.servicos.controles.divide_planilha import (finalizar_execucao,
                                                    selecionar_execucao,
                                                    selecionar_tarefa_ativa)
from nfp.servicos.interface import abrir_popup


class DividePlanilha():

    def __init__(self, parametros):
        if not 'arquivo_entrada' in parametros:
            raise Exception('Arquivo de Entrada não informado.')
        self.path_planilha_entrada = parametros['arquivo_entrada']
        self.tipo_planilha = 'excel'
        if '.csv' in self.path_planilha_entrada:
            self.tipo_planilha = 'csv'
        self.planilha = self._carrega_planilha()
        self.path_planilha_saida = parametros['arquivo_saida']
        if not self.path_planilha_saida:
            self.path_planilha_saida = os.path.dirname(self.path_planilha_entrada)
        self.criterio = parametros['divisao_planilha_criterio']
        self.quantidade = self._valida_quantidade(parametros['divisao_planilha_qtd'])

    def main(self):
        while(True):
            entrada = selecionar_execucao()
            if not entrada:
                return selecionar_tarefa_ativa()
            # entradas
            self.id = entrada.id
            self.tarefa_id = entrada.tarefa_id
            try:
                self.dividir_planilha()
                retorno = 'Ok - planilhas divididas'
            except Exception as e:
                retorno = str(e)
            self.retornar_resultado(retorno)

    def dividir_planilha(self):
        extensao = 'xlsx'
        if self.tipo_planilha == 'csv':
            extensao = 'csv'
        end_slice_index = 0
        num_planilha = 1
        max_linhas = self._calcula_max_linhas_planilha_saida()
        print('**********Máximo de linhas para cada planilha: {}'.format(max_linhas))
        print('Formato: {}'.format(self.tipo_planilha))
        nome_plan = os.path.basename(self.path_planilha_entrada)
        nome_plan = nome_plan.replace('.xlsx', '').replace('.xls', '').replace('.csv', '')
        print(nome_plan)
        while (end_slice_index < len(self.planilha)):
            start_slice_index = end_slice_index
            end_slice_index = end_slice_index + max_linhas
            if (end_slice_index > len(self.planilha)):
                end_slice_index = len(self.planilha) + 1
            nome_arquivo = '{}/Plan_{}_{}.{}'.format(self.path_planilha_saida,
                                                     num_planilha, nome_plan, extensao)
            planilha_slice = self.planilha[start_slice_index:end_slice_index]
            if self.tipo_planilha == 'csv':
                planilha_slice.to_csv(nome_arquivo, index=False)
            else:
                planilha_slice.to_excel(nome_arquivo, index=False)
            num_planilha += 1
            print('**********Linhas {} a {} gravadas no arquivo {}'.format(start_slice_index + 1,
                                                                           end_slice_index,
                                                                           nome_arquivo))

    def _carrega_planilha(self):
        if 'csv' in self.path_planilha_entrada:
            return pd.read_csv(self.path_planilha_entrada, encoding='utf8')
        return pd.read_excel(self.path_planilha_entrada)

    def _qtd_linhas_planilha(self):
        return len(self.planilha)

    def _valida_quantidade(self, str_qtd_criterio):
        # se critério==Linhas, qtd_padrão é igual ao n. de linhas da planilha de entrada
        # se não, qtd_padrao é igual a 1
        qtd_padrao = self._qtd_linhas_planilha() if (self.criterio == 'Linhas') else 1
        # retorna o valor digitado se for um número válido, se não retorna qtde_padrao
        try:
            int_qtd_criterio = int(str_qtd_criterio)
        except ValueError:
            int_qtd_criterio = qtd_padrao
        return int_qtd_criterio

    def _calcula_max_linhas_planilha_saida(self):
        # se critério==Planilhas, max_linhas do arquivo de saída é igual ao n. de linhas da planilha
        # dividido pelo n. informado pelo usuário (arredondado para cima)
        # se não, masx_linhas é igual ao valor informado pelo usuário
        max_linhas = self.quantidade
        if self.criterio == 'Planilhas':
            max_linhas = math.ceil(self._qtd_linhas_planilha() / self.quantidade)
        return max_linhas

    def retornar_resultado(self, retorno):
        texto = 'Retorno: {}'.format(retorno)
        resultado = {'resultado': retorno}
        finalizar_execucao(self.id, resultado)
        abrir_popup(texto, 5)

if __name__ == "__main__":
    parametros = {
        'arquivo_entrada': r"C:\planilhas\teste divide planilhas\procs_testes.csv",
        'arquivo_saida': '',
        'divisao_planilha_criterio': 'Planilhas',
        'divisao_planilha_qtd': '4',
        'divisao_planilha_pacotes': '',
    }
    robo = DividePlanilha(parametros)
    robo.dividir_planilha()
