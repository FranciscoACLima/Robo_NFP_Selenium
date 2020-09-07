import os
from datetime import datetime
import nfp.servicos.model as tables
import nfp.servicos.controle_execucao as ctrlexec
from nfp.config import BASEDIR, URI


class ControleNFP(ctrlexec.ControleExecucao):

    def __init__(self, entradas, uri):
        self.entradas = entradas
        self.uri = uri
        self.table_name = 'notas_fiscais'
        self.configurar_base_de_dados()
        self.model = tables.NotaFiscal

    def carregar_entradas(self, tarefa_id):
        if not self.tarefa_nova:
            return 3, 'usando tarefa ativa'
        session = self.DBSession()
        for entrada in self.entradas:
            try:
                registro = self.model()
                registro.cod_nota = entrada[0]
                registro.tarefa_id = tarefa_id
                session.add(registro)
            except IndexError as e:
                return 1, str(e)
        session.commit()
        return 0, 'entradas carregadas'

    def finalizar_execucao(self, id_execucao, dic):
        session = self.DBSession()
        registro = session.query(self.model).get(id_execucao)
        registro.fim = datetime.now()
        registro.resultado = dic['resultado']
        session.add(registro)
        session.commit()
        return registro


# ---------- Funções do módulo -------------
def carregar_entradas(entradas, uri=URI):
    controle = ControleNFP(entradas, uri)
    tarefa = controle.selecionar_tarefa_ativa(criar_nova=True)
    if not tarefa:
        return 2, 'tarefa não configurada'
    return controle.carregar_entradas(tarefa.id)


def selecionar_execucao(uri=URI):
    controle = ControleNFP([], uri)
    tarefa = controle.selecionar_tarefa_ativa()
    if not tarefa:
        return None
    return controle.selecionar_execucao(tarefa.id)


def finalizar_execucao(id_execucao, retorno, uri=URI):
    controle = ControleNFP([], uri)
    return controle.finalizar_execucao(id_execucao, retorno)


def finalizar_tarefa_ativa(uri=URI):
    controle = ControleNFP([], uri)
    return controle.finalizar_tarefa()


def selecionar_tarefa_ativa(uri=URI):
    controle = ControleNFP([], uri)
    return controle.selecionar_tarefa_ativa()


def selecionar_ultima_tarefa_finalizada(uri=URI):
    controle = ControleNFP([], uri)
    return controle.selecionar_ultima_tarefa_finalizada()


def extrair_dados_tarefa(tarefa_id, arquivo, uri=URI):
    from app_robos.servicos.xlsx import criar_planilha
    registros = listar_dados_tarefa(tarefa_id, uri=uri)
    return criar_planilha(registros, arquivo)


def contar_processos_executados(tarefa_id, uri=URI):
    controle = ControleNFP([], uri)
    return controle.contador_processos_tarefa(tarefa_id)


def listar_dados_tarefa(tarefa_id, uri=URI):
    controle = ControleNFP([], uri)
    registros = controle.extrair_dados_tarefa(tarefa_id)
    return registros


# -------------------- testes do módulo ---------------
def test_criar_planilha():
    registros = extrair_dados_tarefa(1)
    arquivo = os.path.join(BASEDIR, 'teste.xlsx')
    from app_robos.servicos.xlsx import criar_planilha
    retorno = criar_planilha(registros, arquivo)
    print(retorno)


def test_conferir_colunas():
    controle = ControleNFP([], URI)
    print(controle)
    diferenca = controle.localizar_colunas_faltantes()
    print(diferenca)
    controle.atualizar_colunas_tabela()


# ----------------------------------------
if __name__ == "__main__":
    test_conferir_colunas()
