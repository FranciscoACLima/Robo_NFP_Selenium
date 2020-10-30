""" Controlador da execução do robô selecionado na tela
"""
import nfp.exceptions as ex
import importlib as il
import xlrd
import logging
import time
import os
from nfp.robos.notas_fiscais import CadastraNFP
from nfp.servicos.interface import abrir_popup


class ControladorRobos():
    robos = [
        {'codigo': 'notas_fiscais', 'robo': CadastraNFP},
        {'codigo': 'divide_planilhas', 'robo': None}
    ]

    def main(self, codigo, dict_parametros):
        self.lista_resultado = []
        self.tarefa_ativa = None
        self.codigo_robo = codigo
        dict_parametros_robo_ativo = {}
        for key, value in dict_parametros.items():
            if self.codigo_robo in str(key):
                key = key.replace(self.codigo_robo, '')
                dict_parametros_robo_ativo[key] = value
        select = list(filter(lambda x: (x['codigo'] == self.codigo_robo), self.robos))
        if not select:
            raise Exception('Codigo Robo {} invalido'.format(self.codigo_robo))
        self.select = select
        package = "nfp.servicos.controles.{}".format(self.codigo_robo)
        ctrl = il.import_module(package)
        try:
            tarefa_ativa = ctrl.selecionar_tarefa_ativa()
            if not tarefa_ativa:
                if not dict_parametros_robo_ativo['arquivo_entrada'].strip():
                    return "ERRO: Nenhuma planilha informada"
                try:
                    entradas = self.extrair_dados_planilhas(dict_parametros_robo_ativo['arquivo_entrada'])
                except Exception as e:
                    return str(e)
                if not entradas:
                    return "Não foi possível carregar os dados da planilha"
                retorno = ctrl.carregar_entradas(entradas)
                valor = retorno[0]
                texto = retorno[1]
                if valor > 0:
                    msg = 'Erro no carregamento das entradas "{}" - cod erro {}'.format(texto, valor)
                    return msg
                tarefa_ativa = ctrl.selecionar_tarefa_ativa()
            logging.info('Entradas carregadas e tarefa ativa selecionada')
            # confere se a tarefa possui entradas
            contador = ctrl.contar_processos_executados(tarefa_ativa.id)
            if not contador[1]:
                msg = 'Tarefa nao possui entradas para trabalhar'
                return msg
            robo = select[0]['robo'](dict_parametros_robo_ativo)
            # executa o robô
            retorno = robo.main()
            dir_saida = dict_parametros_robo_ativo['dir_saida']
            extrair_resultados(self.codigo_robo, retorno, dir_saida)
            return
        except Exception as e:
            print(e)
            return " Erro. {} \n Execução cancelada.".format(e)

    def extrair_dados_planilhas(self, arquivo):
        lista_planilha = []
        try:
            wb = xlrd.open_workbook(arquivo)
        except IOError as io:
            print(io)
            raise ex.PlanilhaInexistenteException('Planilha de entrada inexistente.')
        except Exception as e:
            print(e)
            raise ex.ErroExtracaoDadosPlanilhaException(e)
        sheet = wb.sheet_by_index(0)
        for n in range(sheet.nrows):
            dados = []
            for c in range(sheet.ncols):
                planilha_value = sheet.cell(n, c).value
                if isinstance(planilha_value, float):
                    if planilha_value.is_integer():
                        planilha_value = int(planilha_value)
                planilha_value = str(planilha_value).strip()
                dados.append(planilha_value)
            lista_planilha.append(dados)
        del wb
        return lista_planilha


# ---------- função de módulo ------------
def extrair_resultados(codigo, ativa, dir_saida):
    data_hora = time.strftime("%Y%m%d-%H%M", time.gmtime())
    msg = 'Tarefa completada. \nGravando planilha com os resultados...'
    abrir_popup(texto=msg, tempo=5)
    package = "nfp.servicos.controles.{}".format(codigo)
    ctrl = il.import_module(package)
    arquivo = 'result_' + str(ativa.id) + '_' + codigo + '_' + data_hora + '.xlsx'
    path_arquivo = os.path.join(dir_saida, arquivo)
    retorno = ctrl.extrair_dados_tarefa(ativa.id, path_arquivo)
    msg = '\n Tarefa não finalizada.'
    if retorno[0] == 0:
        if ctrl.finalizar_tarefa_ativa():
            msg = '\n Tarefa finalizada.'
    texto = retorno[1] + msg
    abrir_popup(texto=texto)


# --------------------------------------
if __name__ == "__main__":
    parametros = {
        'codigo': 'notas_fiscais',
        'notas_fiscaismes': '08',
        'notas_fiscaisano': '2020',
        'notas_fiscaisentidade': 'CREN - CENTRO DE RECUPERAÇÃO E EDUCAÇÃO NUTRICIONAL',
        'notas_fiscaisdir_saida': 'C:/DevApps',
        'notas_fiscaisarquivo_entrada': r"C:\Users\franc\Documents\Notas fiscais 2020\agosto\teste_1.xlsx"
    }
    controle = ControladorRobos()
    result = controle.main('notas_fiscais', parametros)
    print('Resultado:', result)
