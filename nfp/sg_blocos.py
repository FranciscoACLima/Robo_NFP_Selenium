import PySimpleGUI as sg
from nfp import INITIAL_FOLDER

TAM_TXT = 24
TAM_BOX = 45


class SgBlocos():
    
    def arquivo_entrada(self, prefixo):
        """ Arquivo de entrada para os robôs

            Retorna uma linha
        """
        ajuda = 'Prepare a planilha de acordo com as\n'
        ajuda += 'informações contidas na coluna ao lado'
        arq =self.get_cfg_win(prefixo + 'arquivo_entrada')
        return [
            sg.Text('Planilha de Entrada:', size=(15, 1), font=self.font_label),
            sg.Input(arq, key=prefixo + 'arquivo_entrada', size=(47, 1),
                        font=self.font_input,
                        tooltip=ajuda),
            sg.FileBrowse('Buscar', font=self.font_bt_menor, initial_folder=INITIAL_FOLDER)
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

    def arquivo_saida(self, prefixo, limpo=False):
        """ Arquivo de saida para os robôs

            Retorna uma linha
        """
        ajuda = 'Se não for indicado, será utilizado \n'
        ajuda += 'o diretório da planilha de entrada'
        if limpo:
            self.add_cfg_win(prefixo + 'arquivo_saida', '')
            texto = ""
        else:
            texto = self.get_cfg_win(prefixo + 'arquivo_saida')
        return [
            sg.Text('Diretório de Saída:', size=(15, 1), font=self.font_label),
            sg.Input(texto,
                    key=prefixo + 'arquivo_saida', size=(47, 1),
                    font=self.font_input,
                    tooltip=ajuda
                    ),
            sg.FolderBrowse('Buscar', font=self.font_bt_menor)
        ]

    def diretorio_entrada(self, prefixo, limpo=False):
        """ Diretório de entrada das planilhas que serão unificadas

            Retorna uma linha
        """
        if limpo:
            self.add_cfg_win(prefixo + 'diretorio_entrada', '')
            texto = ''
        else:
            texto = self.get_cfg_win(prefixo + 'diretorio_entrada')
        return [
            sg.Text('Diretório de Entrada:', size=(15, 1), font=self.font_label),
            sg.Input(texto,
                    key=prefixo + 'diretorio_entrada', size=(47, 1),
                    font=self.font_input
                    ),
            sg.FolderBrowse('Buscar', font=self.font_bt_menor)
        ]


    def divisao_planilha_criterio(self, prefixo):
        opcoes = [
            'Planilhas',
            'Linhas',
        ]
        valor = self.get_cfg_win(prefixo + 'divisao_planilha_criterio')
        if not valor:
            valor = 'Planilhas'
        text = sg.Text('Divisão por quantidade de:', size=(38, 1), font=self.font_label)
        combo = sg.Combo(values=opcoes, key=prefixo + 'divisao_planilha_criterio',
                        size=(20, 1), default_value=valor,
                        font=self.font_input, readonly=True)
        return [text, combo]


    def divisao_planilha_qtd(self, prefixo):
        return [
            sg.Text('Em quantas planilhas/linhas será feita a divisão:', size=(38, 1), font=self.font_label),
            sg.Input(self.get_cfg_win(prefixo + 'divisao_planilha_qtd'),
                    key=prefixo + 'divisao_planilha_qtd', size=(20, 1),
                    font=self.font_input)
        ]


    def unificacao_planilhas_qtd_linhas_titulo(self, prefixo):
        values = ['Sim', 'Não']
        qtd_linhas = 'Sim'
        if self.get_cfg_win(prefixo + 'qtd_linhas_titulo'):
            try:
                qtd = int(self.get_cfg_win(prefixo + 'qtd_linhas_titulo'))
                if qtd < 1:
                    qtd_linhas = 'Não'
            except Exception:
                qtd_linhas = self.get_cfg_win(prefixo + 'qtd_linhas_titulo')
        return [
            sg.Text('Planilhas contêm linha de título:', size=(50, 1), font=self.font_label),
            sg.Combo(values=values, default_value=qtd_linhas,
                    key=prefixo + 'qtd_linhas_titulo', size=(14, 1), font=self.font_input)
        ]
