"""Módulo para carregamento da tela
"""
import importlib as il
import os
import platform
import subprocess
import sys
import time

import PySimpleGUI as sg

import nfp.tela_config as cfg
import nfp.tela_sobre as sbr
from nfp import BASEDIR, DIR_RESULT
from nfp.robos.controlador_robos import ControladorRobos
from nfp.servicos.arquivos import (abrir_json, adicionar_dados_json,
                                   criar_json_dados_robos)
from nfp.tela_root import TelaRoot
from nfp.sg_blocos import SgBlocos

class TelaRobo(SgBlocos, TelaRoot):

    JSON_CFG = 'config_window.json'

    def __init__(self):
        self.titulo = 'Robôs Nota Fiscal Paulista'
        sg.ChangeLookAndFeel('GreenTan')
        self.size_win = (950, 500)
        self.size_d = (558, 380)
        self.left_ult_linha = 145
        self.tam_linha = 67
        self.pad_titulo = (40, 5)
        if platform.system() == 'Linux':
            self.size_win = (962, 500)
            self.size_d = (578, 380)
            self.pad_titulo = (30, 5)
            self.font_titulo_robo = 'sfprodisplay 21 bold'
            self.font_input = 'sfprodisplay 8'
            self.left_ult_linha = 140
            self.tam_linha = 80


    @property
    def cfg_win(self):
        """ Retorna o dicionário com as configurações da janela"""
        arq_json = os.path.join(BASEDIR, self.JSON_CFG)
        dic = abrir_json(arq_json)
        if not dic:
            dic = {}
        return dic

    @property
    def layout(self):
        """ Layout base

            linhas:
                1. menu
                2. colunas com as opções dos robôs disponíveis
        """
        selecionado = self.get_cfg_win('robo_selecionado')
        linhas = []
        linhas += [sg.Menu(self.menu, tearoff=False)]
        for robo in self.robos:
            visivel = False
            if robo['cod'] == selecionado:
                self.robo_selecionado = robo['cod']
                visivel = True
            coluna = self.configura_coluna_robo(robo, visivel)
            linha = [coluna]
            linhas += linha
        return [linhas]

    @property
    def menu(self):
        lista = []
        for robo in self.robos:
            lista.append(robo['nome'] + '::' + robo['cod'])
        return [
            ['Robos Disponíveis', lista],
            ['Configuração', ['Configurações da máquina::config_maquina']],
            ['Ajuda', 'Sobre::sobre'],
        ]

    @property
    def robos(self):
        return [
            {'cod': 'notas_fiscais',
             'nome': 'Grava Notas Fiscais'},
            {'cod': 'divide_planilha',
             'nome': 'Divide uma Planilha em Várias'}
        ]

    @property
    def robo_ativo(self):
        return self._robo_ativo

    @property
    def dir_saida(self):
        return DIR_RESULT

    @robo_ativo.setter
    def robo_ativo(self, cod_robo):
        for robo in self.robos:
            if robo['cod'] == cod_robo:
                self._robo_ativo = robo
                return
        self._robo_ativo = None

    def col_esquerda_pagina_inicial(self):
        return [
            [sg.Text('')],
        ]

    def col_direita_pagina_inicial(self):
        return [
            [sg.Text('Página Inicial')],
        ]

    # COLUNAS ROBO DIVIDE PLANILHA
    def col_esquerda_divide_planilha(self):
        texto = 'Este robô divide a planilha informada em várias, utilizando como referência uma quantidade de linhas ou '
        texto += 'uma quantidade de planilhas.'
        texto1 = 'O arquivo de entrada é a planilha Excel que será dividida.'
        texto1 += '\n\n\nApós a inclusão das informações, clique em "Executar Robô" e aguarde a finalização da execução.'
        return [
            [sg.Text('O que faz este robô:', font=self.font_titulo)],
            [sg.Text(texto, size=(35, 6), font=self.font_texto)],
            [sg.Text('Como executá-lo:', font=self.font_titulo)],
            [sg.Text(texto1, size=(35, 8), font=self.font_texto)],
        ]

    def col_direita_divide_planilha(self, prefixo):
        layout = []
        tam = self.tam_linha
        layout.append([sg.Text(' ' * tam)])
        if not self.get_tarefa_ativa(prefixo):
            layout.append(self.arquivo_entrada(prefixo))
        layout.append(self.arquivo_saida(prefixo))
        layout.append([sg.Text('_' * tam, (tam, 2))])
        layout.append(self.divisao_planilha_criterio(prefixo))
        layout.append(self.divisao_planilha_qtd(prefixo))
        layout.append(self.contem_titulo(prefixo))
        return layout
    # --------------------------------------------

    # COLUNAS ROBO NOTAS FISCAIS
    def col_esquerda_notas_fiscais(self):
        texto = 'Este robô grava Nota Fiscal Paulista  para instituições sem fins lucrativos.'
        texto += '\nQuando o robô é executado, uma nova janela do navegador Google Chrome é aberta'
        texto += ' na página de login da nota fiscal.'
        texto1 = 'O arquivo de entrada é uma planilha Excel contendo 1 coluna:'
        texto1 += '\n  1. código da nota fiscal'
        texto1 += '\n\nApós a inclusão das informações, clique em "Executar Robô"'
        texto1 += ' e aguarde a finalização da execução.'
        texto2 = 'OBS: O robô aguarda o login e a \nresolução do CAPTCHA'
        return [
            [sg.Text('O que faz este robô:', font=self.font_titulo)],
            [sg.Text(texto, size=(35, 6), font=self.font_texto)],
            [sg.Text('Como executá-lo:', font=self.font_titulo)],
            [sg.Text(texto1, size=(35, 8), font=self.font_texto)],
            [sg.Text(texto2, size=(35, 2), font=self.font_titulo)],
        ]

    def col_direita_notas_fiscais(self, prefixo):
        layout = []
        tam = self.tam_linha
        layout.append([sg.Text(' ' * tam)])
        if not self.get_tarefa_ativa(prefixo):
            layout.append(self.arquivo_entrada(prefixo))
        layout.append(self.sel_mes(prefixo))
        layout.append(self.sel_ano(prefixo))
        layout.append([sg.Text('_' * tam, (tam, 2))])
        layout.append(self.sel_entidade(prefixo))
        return layout

    def get_tarefa_ativa(self, nome_robo):
        try:
            package = "nfp.servicos.controles.{}".format(nome_robo)
            ctrl = il.import_module(package)
            return ctrl.selecionar_tarefa_ativa()
        except Exception:
            return None

    def get_processos_executados(self, tarefa):
        if not tarefa:
            return (None, None)
        try:
            package = "nfp.servicos.controles.{}".format(tarefa.robo)
            ctrl = il.import_module(package)
            return ctrl.contar_processos_executados(tarefa.id)
        except Exception as e:
            print('Excecao levantada em get_processos_executados():', e)
            print('Tarefa:', str(tarefa))
            return (None, None)

    def get_ultima_tarefa_finalizada(self, nome_robo):
        try:
            package = "nfp.servicos.controles.{}".format(nome_robo)
            ctrl = il.import_module(package)
            return ctrl.selecionar_ultima_tarefa_finalizada()
        except Exception:
            return None

    def add_cfg_win(self, chave, valor):
        """ Adiciona uma chave e valor no arquivo de configuração da janela"""
        arq_json = os.path.join(BASEDIR, self.JSON_CFG)
        dic = abrir_json(arq_json)
        if not dic:
            dic = {}
        dic[chave] = valor
        if not os.path.isfile(arq_json):
            criar_json_dados_robos(BASEDIR, self.JSON_CFG)
        adicionar_dados_json(arq_json, dic)

    def get_cfg_win(self, chave):
        try:
            return self.cfg_win[chave]
        except KeyError:
            return ''

    def configura_layout_coluna_robo(self, robo, col_e, col_d,
                                     scroll=True, size_e=None, size_d=None):
        """ coluna com as configurações de cada robô
            A coluna é composta de duas colunas:
                1. Esquerda -> Orientações
                2. Direita -> Formulários
        """
        # define uma linha vertical entre as colunas com exceção à pagina inicial
        separador_vertical = sg.VerticalSeparator(color='black', pad=None)
        if robo['cod'] == 'pagina_inicial':
            separador_vertical = sg.Column([])
        if not size_e:
            size_e = (300, 380)
        if not size_d:
            size_d = self.size_d
        return [
            [sg.Text(
                robo['nome'],
                pad=self.pad_titulo,
                justification='center',
                font=self.font_titulo_robo,
                relief=sg.RELIEF_RIDGE,
                size=(47, 1),
                text_color='#0c2624',
            )],
            [
                sg.Column(
                    col_e,
                    size=size_e,
                    pad=(10, 0),
                    scrollable=scroll,
                    vertical_scroll_only=scroll
                ),
                separador_vertical,
                sg.Column(
                    col_d,
                    size=size_d,
                    pad=(0, 0),
                    scrollable=scroll,
                    vertical_scroll_only=scroll),
            ]
        ]

    def configura_coluna_robo(self, robo, visivel):
        """ configura coluna robo

            As linhas são montadas a partir de uma lista vazia,
            para adicionar uma linha, use lista.append(linha)
            para adicionar uma lista de linhas use lista += linhas

        """
        layout = [
            [sg.Text(robo['nome'])],
            [sg.Text(robo['cod'])],
            [sg.Text('Tela em construção...', size=(40, 18))]
        ]
        layout.append([sg.Text(robo['cod'])])
        layout.append(self.configura_ultima_linha_robo(robo['cod']))
        if robo['cod'] == 'pagina_inicial':
            layout = self.configura_layout_coluna_robo(
                robo=robo,
                col_e=self.col_esquerda_pagina_inicial(),
                col_d=self.col_direita_pagina_inicial(),
                size_e=(230, 1),
                scroll=False)
        if robo['cod'] == 'notas_fiscais':
            layout = self.configura_layout_coluna_robo(
                robo=robo,
                col_e=self.col_esquerda_notas_fiscais(),
                col_d=self.col_direita_notas_fiscais(robo['cod']))
            layout.append(self.configura_ultima_linha_robo(robo['cod']))
        if robo['cod'] == 'divide_planilha':
            layout = self.configura_layout_coluna_robo(
                robo=robo,
                col_e=self.col_esquerda_divide_planilha(),
                col_d=self.col_direita_divide_planilha(robo['cod']))
            layout.append(self.configura_ultima_linha_robo(robo['cod']))
        return sg.Column(
            layout,
            visible=visivel,
            key=robo['cod'],
            size=self.size_win,
            pad=(0, 0),
        )

    def configura_ultima_linha_robo(self, nome_robo, executar=True):
        ultima_linha = self.configura_informacoes_tarefa(nome_robo)
        ultima_linha += [sg.Button('Abortar Tarefa', key='abortar_tarefa', font=self.font_bt_menor)]
        ultima_linha += [sg.Button('Extrair Resultados', key='extrair_resultados', font=self.font_bt_menor)]
        ultima_linha += [sg.Text('', size=(8, 0))]
        ajuda = 'Depois de clicar, aguarde a execução\n'
        ajuda += 'Não mexa no mouse ou teclado\nenquanto o robô estiver trabalhando'
        if executar:
            ultima_linha += [sg.Column([
                [sg.OK('Executar Robô', key='executar', font=self.font_bt_padrao, tooltip=ajuda)]],
                pad=(self.left_ult_linha, 0))]
        return ultima_linha

    def configura_informacoes_tarefa(self, nome_robo):
        texto = 'Não consta nenhuma tarefa para este robô.'
        tarefa = self.get_tarefa_ativa(nome_robo)
        if tarefa:
            status = 'EM ANDAMENTO'
            ex, tot = self.get_processos_executados(tarefa)
            complem = '\n {} de {} processo(s) completado(s).'.format(ex, tot)
            data_inic = tarefa.inicio.strftime('%d/%m/%Y %H:%M')
            texto = ' Tarefa iniciada em {} \n Situação: {} {}'.format(data_inic, status, complem)
        else:
            tarefa = self.get_ultima_tarefa_finalizada(nome_robo)
            if tarefa:
                status = 'FINALIZADA'
                data_inic = tarefa.inicio.strftime('%d/%m/%Y %H:%M')
                complem = 'em ' + tarefa.fim.strftime('%d/%m/%Y %H:%M')
                texto = ' Tarefa iniciada em {} \n Situação: {} {}'.format(data_inic, status, complem)
        return [
            sg.Text(
                texto,
                text_color='black',
                background_color='#f0e965',
                size=(40, 0),
                font=self.font_texto)
        ]

    def seleciona_robos(self, window, event):
        if not ('::') in event:
            pass
        array = event.split('::')
        selecionado = array[1]
        self.add_cfg_win('robo_selecionado', selecionado)
        for robo in self.robos:
            visivel = False
            if robo['cod'] == selecionado:
                visivel = True
                self.robo_ativo = selecionado
            elemento = window.Element(robo['cod'])
            elemento.Update(visible=visivel)

    def _gravar_campos_tela(self, values):
        for chave in values:
            if 'senha' in str(chave) or 'arquivo_entrada' in str(chave):
                self.add_cfg_win(chave, '')
            else:
                self.add_cfg_win(chave, values[chave])

    def main(self):
        ultimo_robo = self.get_cfg_win('robo_selecionado')
        if not ultimo_robo:
            self.add_cfg_win('robo_selecionado', 'notas_fiscais')
        self.robo_ativo = ultimo_robo
        window = sg.Window(self.titulo,
                           self.layout,
                           size=self.size_win,
                           font='sfprodisplay 11',
                           margins=(5, 5),
                           auto_size_text=True,
                           icon='')
        event, values = window.Read()
        while True:
            if event is None:
                window.Close()
                return
            if 'executar' in event:
                values[self.robo_ativo['cod'] + 'dir_saida'] = self.dir_saida
                self._gravar_campos_tela(values)
                sg.PopupAutoClose(
                    ' Robô em execução. tecle \n ___ ALT + SHIFT + C ___ \n para abortar a tarefa',
                    auto_close_duration=5)
                window.Close()
                try:
                    retorno = ControladorRobos().main(self.robo_ativo['cod'], values)
                except KeyboardInterrupt:
                    retorno = "Execução interrompida pelo usuário"
                if retorno:
                    sg.Popup(retorno)
                return self.main()
            if 'abortar_tarefa' in event:
                retorno = self.abortar_tarefa(values)
                if retorno != 'Não':
                    sg.Popup(str(retorno))
                if self.reiniciar_tela:
                    window.Close()
                    return self.main()
                event, values = window.Read()
                continue
            if 'extrair_resultados' in event:
                retorno = self.extrair_resultados(values)
                msg = str(retorno[0])
                if 'criada com sucesso' in retorno[0].lower():
                    msg += '\nAguarde... Abrindo a planilha.'
                    try:
                        self.abrir_planilha(retorno[1])
                    except Exception:
                        pass
                sg.PopupAutoClose(msg, auto_close_duration=5)
                if self.reiniciar_tela:
                    window.Close()
                    return self.main()
                event, values = window.Read()
                continue
            if '::sobre' in event:
                sbr.run()
                event, values = window.Read()
                continue
            if '::config_maquina' in event:
                cfg.run()
                event, values = window.Read()
                continue
            self.seleciona_robos(window, event)
            event, values = window.Read()

    def abrir_planilha(self, filename):
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

    def extrair_resultados(self, values):
        self.reiniciar_tela = False
        nome_robo = self.robo_ativo['cod']
        package = "nfp.servicos.controles.{}".format(nome_robo)
        ctrl = il.import_module(package)
        tarefa = self.get_tarefa_ativa(nome_robo)
        if not tarefa:
            tarefa = self.get_ultima_tarefa_finalizada(nome_robo)
            if not tarefa:
                return 'Não consta nenhuma tarefa para este robô\n'
        tarefa_id = tarefa.id
        diretorio = self.dir_saida
        data_hora = time.strftime("%Y%m%d-%H%M", time.gmtime())
        arquivo = os.path.join(
            diretorio,
            'result_' + str(tarefa_id) + '_' + self.robo_ativo['cod'] + '_' + data_hora + '.xlsx'
        )
        retorno = ctrl.extrair_dados_tarefa(tarefa_id, arquivo)
        return retorno[1], arquivo

    def abortar_tarefa(self, values):
        self.reiniciar_tela = False
        nome_robo = self.robo_ativo['cod']
        package = "nfp.servicos.controles.{}".format(nome_robo)
        ctrl = il.import_module(package)
        tarefa = self.get_tarefa_ativa(nome_robo)
        if not tarefa:
            return 'Não consta tarefa em andamento para este robô\n'
        msg = 'Deseja realmente abortar a tarefa atual?\n'
        resultado = sg.Popup(msg, custom_text=('Sim', 'Não'))
        if resultado == 'Não':
            return resultado
        if ctrl.finalizar_tarefa_ativa():
            msg = 'Tarefa abortada.\n'
            self.reiniciar_tela = True
        else:
            msg = 'Tarefa não foi abortada, tente novamente.\n'
        return msg


# ------------------------------
if __name__ == "__main__":
    pass
