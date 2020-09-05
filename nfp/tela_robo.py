"""Módulo para carregamento da tela
"""
import PySimpleGUI as sg


class TelaRobo(object):
    font_titulo = 'sfprodisplay 11 bold'
    font_titulo_robo = 'sfprodisplay 23 bold'
    font_label = 'sfprodisplay 10'
    font_input = 'sfprodisplay 10'
    font_texto = 'sfprodisplay 10'
    font_bt_padrao = 'sfprodisplay 11'
    font_bt_menor = 'sfprodisplay 9'

    def __init__(self):
        self.titulo = 'Robô Cadastro Nota Fiscal Paulista'

    @property
    def layout(self):
        """ Layout base

            linhas:
                1. menu
                2. colunas com as opções dos robôs disponíveis
        """
        linhas = []
        linhas += [sg.Menu(self.menu, tearoff=True)]
        ajuda = 'Depois de clicar, aguarde a execução\n'
        ajuda += 'Não mexa no mouse ou teclado\nenquanto o robô estiver trabalhando'
        linhas += [sg.Column([
            [sg.OK('Executar Robô', key='executar', font=self.font_bt_padrao, tooltip=ajuda)]],
            pad=(145, 0))]
        return [linhas]

    @property
    def menu(self):
        lista = [
            'Robô Nota Fiscal Paulista::gravar_nfp',
            'Utilitário para Dividir Planilha::divide_planilha'
            ]
        return [
            ['Robos Disponíveis', lista],
            ['Configuração', ['Configurações da máquina::config_maquina']],
            ['Ajuda', 'Sobre::sobre'],
        ]

    def main(self):
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
                self.testar_funcionamento_selenium()
                return

    def testar_funcionamento_selenium(self):
        from nfp.telas.nfp import Nfp
        robo = Nfp('', '')
        robo.abrir_pagina_login()
        sg.popup('Execução Funcionou !')


# ------------------------------
if __name__ == "__main__":
    pass
