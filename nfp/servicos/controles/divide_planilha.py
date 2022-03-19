import os
from datetime import datetime
import nfp.servicos.model as tables
import nfp.servicos.controles.controle_execucao as ctrlexec
from nfp import URI


class ControleDividePlanilha(ctrlexec.ControleExecucao):

    def __init__(self, entradas, uri):
        super().__init__()
        self.entradas = entradas
        self.uri = uri
        self.table_name = 'divide_planilha'
        self.configurar_base_de_dados()
        self.model = tables.DividePlanilha
        self.atualizar_colunas_tabela()

    def carregar_entradas(self, tarefa_id):
        if not self.tarefa_nova:
            return 3, 'usando tarefa ativa'
        session = self.session
        entrada_remota_id = 0
        try:
            registro = self.model()
            registro.tarefa_id = tarefa_id
            registro.entrada_remota_id = entrada_remota_id
            session.add(registro)
        except IndexError as e:
            return 1, str(e)
        session.commit()
        return 0, 'entradas carregadas'

    def finalizar_execucao(self, id_execucao, dic):
        session = self.session
        registro = session.query(self.model).get(id_execucao)
        registro.fim = datetime.now()
        registro.resultado = dic['resultado']
        session.add(registro)
        session.commit()
        return registro


# ---------- Funções do módulo -------------
def carregar_entradas(entradas, uri=URI):
    controle = ControleDividePlanilha(entradas, uri)
    tarefa = controle.selecionar_tarefa_ativa(criar_nova=True)
    if not tarefa:
        return 2, 'tarefa não configurada'
    return controle.carregar_entradas(tarefa.id)


def selecionar_execucao(uri=URI):
    controle = ControleDividePlanilha([], uri)
    tarefa = controle.selecionar_tarefa_ativa()
    if not tarefa:
        return None
    return controle.selecionar_execucao(tarefa.id)


def finalizar_execucao(id_execucao, retorno, uri=URI):
    controle = ControleDividePlanilha([], uri)
    return controle.finalizar_execucao(id_execucao, retorno)


def finalizar_tarefa_ativa(uri=URI):
    controle = ControleDividePlanilha([], uri)
    return controle.finalizar_tarefa()


def selecionar_tarefa_ativa(uri=URI):
    controle = ControleDividePlanilha([], uri)
    return controle.selecionar_tarefa_ativa()


def selecionar_ultima_tarefa_finalizada(uri=URI):
    controle = ControleDividePlanilha([], uri)
    return controle.selecionar_ultima_tarefa_finalizada()


def extrair_dados_tarefa(tarefa_id, arquivo, uri=URI):
    from nfp.servicos.xlsx import criar_planilha
    registros = listar_dados_tarefa(tarefa_id, uri=uri)
    return criar_planilha(registros, arquivo)


def contar_processos_executados(tarefa_id, uri=URI):
    controle = ControleDividePlanilha([], uri)
    return controle.contador_processos_tarefa(tarefa_id)


def listar_dados_tarefa(tarefa_id, uri=URI):
    controle = ControleDividePlanilha([], uri)
    registros = controle.extrair_dados_tarefa(tarefa_id)
    return registros


# ----------------------------------------
if __name__ == "__main__":
    pass
