"""Módulo para carregamento da tela
"""
import os
import PySimpleGUI as sg
from nfp.servicos.arquivos import abrir_json, adicionar_dados_json, criar_json_dados_robos
from nfp.config import BASEDIR
import importlib as il


class TelaRobo(object):

    JSON_CFG = 'config_window.json'
    font_titulo = 'sfprodisplay 11 bold'
    font_titulo_robo = 'sfprodisplay 23 bold'
    font_label = 'sfprodisplay 10'
    font_input = 'sfprodisplay 10'
    font_texto = 'sfprodisplay 10'
    font_bt_padrao = 'sfprodisplay 11'
    font_bt_menor = 'sfprodisplay 9'

    def __init__(self):
        self.titulo = 'Robôs Nota Fiscal Paulista'
        sg.ChangeLookAndFeel('GreenTan')

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
        linhas += [sg.Menu(self.menu, tearoff=True)]
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
            {'cod': 'pagina_inicial',
             'nome': 'Página Inicial'},
            {'cod': 'notas_fiscais',
             'nome': 'Grava Notas Fiscais'},
            {'cod': 'divide_planilha',
             'nome': 'Divide uma Planilha em várias'}
        ]

    @property
    def robo_ativo(self):
        return self._robo_ativo

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

    def col_esquerda_notas_fiscais(self):
        texto = 'Este robô grava Nota Fiscal Paulista  para instituições sem fins lucrativos.'
        texto += '\nQuando o robô é executado, uma nova janela do navegador Google Chrome é aberta'
        texto += '\nna página de login da nota fiscal.'
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

    def arquivo_entrada(self, prefixo):
        """ Arquivo de entrada para os robôs

            Retorna uma linha
        """
        ajuda = 'Prepare a planilha de acordo com as\n'
        ajuda += 'informações contidas na coluna ao lado'
        return [
            sg.Text('Planilha de Entrada:', size=(15, 1), font=self.font_label),
            sg.Input(self.get_cfg_win(prefixo + 'arquivo_entrada'),
                     key=prefixo + 'arquivo_entrada', size=(47, 1),
                     font=self.font_input,
                     tooltip=ajuda),
            sg.FileBrowse('Buscar', font=self.font_bt_menor)
        ]

    def sel_mes(self, prefixo):
        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
                 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        valor = self.get_cfg_win(prefixo + 'mes')
        if not valor:
            valor = 'Janeiro'
        return [
            sg.Text('Mês de referência:', size=(15, 1), font=self.font_label),
            sg.Combo(values=meses, key=prefixo + 'mes',
                     size=(42, 1), default_value=valor,
                     font=self.font_input, readonly=True)
        ]

    def sel_ano(self, prefixo):
        import datetime
        now = datetime.datetime.now()
        ano_atual = now.year
        ano_anterior = str(int(ano_atual - 1))
        meses = [ano_anterior, ano_atual]
        valor = self.get_cfg_win(prefixo + 'ano')
        if not valor:
            valor = ano_atual
        return [
            sg.Text('Ano de referência:', size=(15, 1), font=self.font_label),
            sg.Combo(values=meses, key=prefixo + 'ano',
                     size=(42, 1), default_value=valor,
                     font=self.font_input, readonly=True)
        ]

    def sel_entidade(self, prefixo):
        valor = self.get_cfg_win(prefixo + 'entidade')
        if not valor:
            valor = 'CREN - CENTRO DE RECUPERAÇÃO E EDUCAÇÃO NUTRICIONAL'
        return [
            sg.Text('Entidade:', size=(7, 1), font=self.font_label),
            sg.Input(valor, key=prefixo + 'entidade', size=(64, 1),
                     font=self.font_input)
        ]

    def col_direita_notas_fiscais(self, prefixo):
        layout = []
        tam = 66
        layout.append([sg.Text(' ' * tam)])
        if not self.get_tarefa_ativa(prefixo):
            layout.append(self.arquivo_entrada(prefixo))
        layout.append(self.sel_mes(prefixo))
        layout.append(self.sel_ano(prefixo))
        layout.append([sg.Text(' ' * tam)])
        layout.append([sg.Text(' ' * tam)])
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
        separador_vertical = sg.VerticalSeparator(pad=None)
        if robo['cod'] == 'pagina_inicial':
            separador_vertical = sg.Column([])
        if not size_e:
            size_e = (300, 380)
        if not size_d:
            size_d = (558, 380)
        return [
            [sg.Text(
                robo['nome'],
                pad=(20, 5),
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
                    pad=(6, 0),
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
        return sg.Column(
            layout,
            visible=visivel,
            key=robo['cod'],
            size=(970, 550),
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
                pad=(145, 0))]
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

    def main(self):
        ultimo_robo = self.get_cfg_win('robo_selecionado')
        if not ultimo_robo:
            self.add_cfg_win('robo_selecionado', 'pagina_inicial')
        self.robo_ativo = ultimo_robo
        window = sg.Window(self.titulo,
                           self.layout,
                           size=(967, 500),
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
                self.executar_robo()
                return
            self.seleciona_robos(window, event)
            event, values = window.Read()

    def executar_robo(self):
        sg.popup('Executar selecionado')


# ------------------------------
if __name__ == "__main__":
    pass
