import os
import webbrowser

import PySimpleGUI as sg

from nfp import VERSAO
from nfp.tela_root import TelaRoot


class Sobre(TelaRoot):

    def __init__(self):
        super().__init__()
        self.titulo = 'Robô Nota Fiscal Paulista'
        self.link_1 = 'https://www.selenium.dev/'
        self.texto_link_1 = self.link_1
        self.link_2 = 'https://github.com/FranciscoACLima'
        self.texto_link_2 = self.link_2
        self.link_3 = 'https://selenium-python.readthedocs.io/'
        self.texto_link_3 = self.link_3
        self.link_4 = 'https://github.com/FranciscoACLima/Robo_NFP_Selenium/blob/main/LICENSE'
        self.texto_link_4 = 'MIT License'

    @property
    def layout(self):
        tam = 58
        linhas = []
        linhas.append([sg.Text(
            f'Robô Nota Fiscal Paulista - Versão {VERSAO}',
            font=self.font_titulo)])
        texto = '\nRobô para auxiliar as instituições no cadastro de notas fiscais paulista'
        linhas.append([sg.Text(texto,font=self.font_texto)])
        linhas.append([sg.Text('_' * tam)])
        texto1 = 'Aplicação desenvolvida por Francisco A. C. Lima   -'
        linhas.append([
            sg.Text(
                texto1,
                font=self.font_texto),
            sg.Text(
            self.texto_link_4,
            click_submits=True,
            key='link_4',
            text_color='blue',
            tooltip='Clique para ir para a página',
            font=self.font_texto)])
        linhas.append([sg.Text(
            self.texto_link_2,
            click_submits=True,
            key='link_2',
            text_color='blue',
            tooltip='Clique para ir para a página',
            font=self.font_texto)])
        linhas.append([sg.Text('_' * tam)])
        # linhas.append([sg.Text('')])
        linhas.append([sg.Text('Automação executada com Selenium', font=self.font_titulo)])
        linhas.append([sg.Text(
            self.texto_link_1,
            click_submits=True,
            key='link_1',
            text_color='blue',
            tooltip='Clique para ir para a página',
            font=self.font_texto)])
        linhas.append([sg.Text(
            self.texto_link_3,
            click_submits=True,
            key='link_3',
            text_color='blue',
            tooltip='Clique para ir para a página',
            font=self.font_texto)])
        # linhas.append([sg.Text('_' * tam)])
        return linhas

    def main(self):
        dir_base = os.path.dirname(__file__)
        icone = os.path.join(dir_base, 'tela', 'resources',
                             'images', 'App_Logo_STI.ico')
        window = sg.Window(self.titulo,
                           self.layout,
                           size=(500, 270),
                           font='sfprodisplay 11',
                           margins=(5, 5),
                           auto_size_text=True,
                           icon=icone)
        event, values = window.Read()
        while True:
            if event is None:
                window.Close()
                return
            if event == 'link_1':
                sg.PopupAutoClose(
                    'Abrindo a página web: \n{}'.format(self.texto_link_1),
                    title='Aguarde...',
                    line_width=250)
                webbrowser.open_new(self.link_1)
                event, values = window.Read()
                continue
            if event == 'link_2':
                sg.PopupAutoClose(
                    'Abrindo a página web: \n{}'.format(self.texto_link_2),
                    title='Aguarde...',
                    line_width=250)
                webbrowser.open_new(self.link_2)
                event, values = window.Read()
                continue
            if event == 'link_3':
                sg.PopupAutoClose(
                    'Abrindo a página web: \n{}'.format(self.texto_link_3),
                    title='Aguarde...',
                    line_width=250)
                webbrowser.open_new(self.link_3)
                event, values = window.Read()
                continue
            if event == 'link_4':
                sg.PopupAutoClose(
                    'Abrindo a página web: \n{}'.format(self.texto_link_4),
                    title='Aguarde...',
                    line_width=250)
                webbrowser.open_new(self.link_4)
                event, values = window.Read()
                continue


# ---- Funções do módulo ---------
def run():
    janela = Sobre()
    janela.main()


# ------------------------------------------
if __name__ == "__main__":
    run()
