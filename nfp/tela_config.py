import json
import os

import PySimpleGUI as sg

from nfp import (BASEDIR, CHREXEC, CONFIG_FILE, DEBUG, DIR_RESULT,
                 EXIBIR_POPUP_RESULT, INITIAL_FOLDER, URLBASE)
from nfp.servicos.arquivos import (abrir_json, adicionar_dados_json,
                                   criar_json_dados_robos)
from nfp.tela_root import TelaRoot


class TelaConfig(TelaRoot):

    def __init__(self):
        self.DIR_CFG = BASEDIR
        self.arquivo_config = CONFIG_FILE
        sg.ChangeLookAndFeel('GreenTan')
        self.size_win = (770, 260)  # (570, 360)
        self.titulo = f"Configuração da Aplicação Nota Fiscal Paulista - computador: {os.environ['COMPUTERNAME']}"
        self.size_label = 20
        self.size_cmp = 75
        self.largura = 95

    @property
    def cfg_win(self):
        """ Retorna o dicionário com as configurações do computador para carregar na janela"""
        arq_json = os.path.join(self.DIR_CFG, self.arquivo_config)
        dic = abrir_json(arq_json)
        if not dic:
            self.criar_json_dados_maquina(self.DIR_CFG, self.arquivo_config)
            return self.cfg_win
        return dic

    @property
    def layout(self):
        tam = self.largura
        linhas = []
        linhas.append([
            sg.Text('Configurações utilizadas:', font=self.font_titulo)])
        linhas.append(self.diretorio_saida)
        linhas.append(self.path_chrome)
        linhas.append(self.debug_db)
        linhas.append(self.popup_resultados)
        linhas.append(self.dir_planilhas)
        linhas.append(self.url_base)
        linhas.append([sg.Text('_' * tam)])
        linhas.append([sg.Text('', size=(self.size_cmp, 0)), sg.OK('Gravar', key='gravar', font=self.font_bt_padrao)])
        return linhas

    @property
    def path_chrome(self):
        return self._config_form_diretorio('Google Chrome Exec.:', 'path_chrome')

    @property
    def diretorio_saida(self):
        return self._config_form_diretorio('Extrações planilhas:', 'dir_saida')

    @property
    def debug_db(self):
        titulo = 'Debug Banco de Dados:'
        chave = 'debug_db'
        msg = 'A opção sim faz a aplicação registrar as querys executadas no banco de dados'
        dados = ['Não', 'Sim']
        valor = self.get_cfg_win(chave)
        if not valor:
            valor = 'Não'
        return [
            sg.Text(titulo, size=(self.size_label, 1), font=self.font_label),
            sg.Combo(values=dados, key=chave,
                     size=(self.size_cmp, 1), default_value=valor,
                     font=self.font_input,
                     tooltip=msg,
                     readonly=True)
        ]

    @property
    def popup_resultados(self):
        titulo = 'Mostrar Popup Execução:'
        chave = 'popup_resultados'
        msg = 'Ao desativar esta opção, podemos utilizar o computador enquanto o robô trabalha'
        dados = ['Não', 'Sim']
        valor = self.get_cfg_win(chave)
        if not valor:
            valor = 'Não'
        return [
            sg.Text(titulo, size=(self.size_label, 1), font=self.font_label),
            sg.Combo(values=dados, key=chave,
                     size=(self.size_cmp, 1), default_value=valor,
                     font=self.font_input,
                     tooltip=msg,
                     readonly=True)
        ]

    @property
    def dir_planilhas(self):
        return self._config_form_diretorio('Diretório Padrão Entrada:', 'dir_planilhas')

    @property
    def url_base(self):
        return self._config_form_diretorio('URL Nota Fiscal Paulista:', 'url_base')

    def add_cfg_win(self, chave, valor):
        """ Adiciona uma chave e valor no arquivo de configuração da janela"""
        arq_json = os.path.join(self.DIR_CFG, self.arquivo_config)
        dic = abrir_json(arq_json)
        if not dic:
            dic = {}
        dic[chave] = valor
        if not os.path.isfile(arq_json):
            criar_json_dados_robos(self.DIR_CFG, self.arquivo_config)
        adicionar_dados_json(arq_json, dic)

    def get_cfg_win(self, chave):
        """ Retorna o valor de uma chave do arquivo de configuração da janela"""
        try:
            return self.cfg_win[chave]
        except KeyError:
            return ''

    def _config_form_diretorio(self, titulo, chave):
        return [
            sg.Text(titulo, size=(self.size_label, 1), font=self.font_label),
            sg.Input(self.get_cfg_win(chave),
                     key=chave, size=(self.size_cmp, 1),
                     font=self.font_input),
            sg.FolderBrowse('Buscar', font=self.font_bt_menor)
        ]
    
    def main(self):
        # dir_base = os.path.dirname(__file__)
        # icone = os.path.join(dir_base, 'tela', 'resources',
        #                      'images', 'App_Logo_STI.ico')
        window = sg.Window(self.titulo,
                           self.layout,
                           size=self.size_win,
                           font='sfprodisplay 11',
                           margins=(5, 5),
                           auto_size_text=True,  # icon=icone
                        )
        event, values = window.Read()
        window.bring_to_front()
        while True:
            if event is None:
                window.Close()
                return
            if event == 'gravar':
                for chave in values:
                    self.add_cfg_win(chave, values[chave])
                sg.PopupAutoClose(
                    'Configuração gravada com sucesso',
                    auto_close_duration=5)
                window.Close()
                return

    def criar_json_dados_maquina(self, dir_config, nome_arquivo_maquina):
        if not os.path.exists(dir_config):
            os.makedirs(dir_config)
        path_arquivo = os.path.join(dir_config, nome_arquivo_maquina)
        if not os.path.exists(path_arquivo):
            config_maquina = {
                "path_chrome": CHREXEC,
                "dir_saida": DIR_RESULT,
                "debug_db": DEBUG, 
                "popup_resultados": EXIBIR_POPUP_RESULT,
                "dir_planilhas": INITIAL_FOLDER,
                "url_base": URLBASE,
            }
            with open(path_arquivo, 'w') as write_file:
                write_file.write(json.dumps(config_maquina))


# ---- Funções do módulo ---------
def run():
    janela = TelaConfig()
    janela.main()


# ------------------------------------------
if __name__ == "__main__":
    run()
