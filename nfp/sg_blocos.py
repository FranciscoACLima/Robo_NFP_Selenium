import PySimpleGUI as sg
from nfp import INITIAL_FOLDER

TAM_TXT = 15
TAM_BOX = 50

TAM_TXT_1 = 10
TAM_BOX_1 = 62

TAM_TXT_2 = 50
TAM_BOX_2 = 15



class SgBlocos():
    
    def arquivo_entrada(self, prefixo):
        """ Arquivo de entrada para os robôs

            Retorna uma linha
        """
        ajuda = 'Prepare a planilha de acordo com as\n'
        ajuda += 'informações contidas na coluna ao lado'
        arq =self.get_cfg_win(prefixo + 'arquivo_entrada')
        return [
            sg.Text('Planilha de Entrada:', size=(TAM_TXT, 1), font=self.font_label),
            sg.Input(arq, key=prefixo + 'arquivo_entrada', size=(TAM_BOX, 1),
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
            sg.Text('Mês de referência:', size=(TAM_TXT, 1), font=self.font_label),
            sg.Combo(values=meses, key=prefixo + 'mes',
                        size=(TAM_BOX, 1), default_value=valor,
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
            sg.Text('Ano de referência:', size=(TAM_TXT, 1), font=self.font_label),
            sg.Combo(values=meses, key=prefixo + 'ano',
                        size=(TAM_BOX, 1), default_value=valor,
                        font=self.font_input, readonly=True)
        ]

    def sel_entidade(self, prefixo):
        valor = self.get_cfg_win(prefixo + 'entidade')
        if not valor:
            valor = 'CREN - CENTRO DE RECUPERAÇÃO E EDUCAÇÃO NUTRICIONAL'
        return [
            sg.Text('Entidade:', size=(TAM_TXT_1, 1), font=self.font_label),
            sg.Input(valor, key=prefixo + 'entidade', size=(TAM_BOX_1, 1),
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
            sg.Text('Diretório de Saída:', size=(TAM_TXT, 1), font=self.font_label),
            sg.Input(texto,
                    key=prefixo + 'arquivo_saida', size=(TAM_BOX, 1),
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
            sg.Text('Diretório de Entrada:', size=(TAM_TXT, 1), font=self.font_label),
            sg.Input(texto,
                    key=prefixo + 'diretorio_entrada', size=(TAM_BOX, 1),
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
        text = sg.Text('Divisão por quantidade de:', size=(TAM_TXT_2, 1), font=self.font_label)
        combo = sg.Combo(values=opcoes, key=prefixo + 'divisao_planilha_criterio',
                        size=(TAM_BOX_2, 1), default_value=valor,
                        font=self.font_input, readonly=True)
        return [text, combo]


    def divisao_planilha_qtd(self, prefixo):
        return [
            sg.Text('Em quantas planilhas/linhas será a divisão:', size=(TAM_TXT_2, 1), font=self.font_label),
            sg.Input(self.get_cfg_win(prefixo + 'divisao_planilha_qtd'),
                    key=prefixo + 'divisao_planilha_qtd', size=(TAM_BOX_2, 1),
                    font=self.font_input)
        ]

    def contem_titulo(self, prefixo):
        ajuda = 'Informe se a planilha contém ou não linha de título de colunas'
        opcoes = [
            'Sim',
            'Não',
        ]
        valor = self.get_cfg_win(prefixo + 'contem_titulo')
        if not valor:
            valor = 'Sim'
        text = sg.Text('Planilha possui linha de título:', size=(TAM_TXT_2, 1), font=self.font_label)
        combo = sg.Combo(values=opcoes, key=prefixo + 'contem_titulo',
                        size=(TAM_BOX_2, 1), default_value=valor,
                        font=self.font_input, readonly=True, tooltip=ajuda)
        return [text, combo]