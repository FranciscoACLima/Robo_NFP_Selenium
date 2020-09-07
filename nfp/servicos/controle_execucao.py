import os
from datetime import datetime
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import nfp.servicos.model as tables
from nfp.config import DEBUG, URI


class ControleExecucao(object):

    uri = URI
    tarefa = None
    tarefa_nova = False

    def configurar_base_de_dados(self):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + self.uri
        engine = db.create_engine(SQLALCHEMY_DATABASE_URI, echo=DEBUG)
        self.DBSession = sessionmaker(bind=engine)
        if os.path.isfile(self.uri):
            if not engine.dialect.has_table(engine, self.table_name):
                print('Tabela {} ainda não existe. Criando tabela...'.format(self.table_name))
                base = tables.Base
                base.metadata.create_all(engine)
            return
        print('Base de dados ainda não existe. Criando...')
        base = tables.Base
        base.metadata.create_all(engine)
        print('usando base de dados: ' + self.uri)

    def get_tarefa(self, tarefa_id):
        session = self.DBSession()
        tarefa = tables.Tarefa
        query = session.query(tarefa).filter(
            tarefa.id == tarefa_id,
        )
        registro = query.first()
        return registro

    def atualizar_colunas_tabela(self):
        colunas = self.localizar_colunas_faltantes()
        if not colunas:
            return
        session = self.DBSession()
        for coluna, tipo in colunas.items():
            session.execute('ALTER TABLE %s ADD COLUMN %s %s' % (self.table_name, coluna, tipo))
        session.commit()

    def localizar_colunas_faltantes(self):
        tabela = self.table_name
        session = self.DBSession()
        result = session.execute("SELECT name FROM PRAGMA_TABLE_INFO('%s')" % (tabela))
        colunas_bd = set()
        for coluna in result.fetchall():
            colunas_bd.add(coluna[0])
        mapper = self.model.__mapper__.columns
        colunas = set()
        colunas_dic = {}
        for column in mapper:
            colunas.add(column.name)
            colunas_dic[column.name] = str(column.type)
        diferencas = list(colunas - colunas_bd)
        if diferencas:
            retorno = {}
            for diferenca in diferencas:
                retorno[diferenca] = colunas_dic[diferenca]
            return retorno
        return None

    def extrair_dados_tarefa(self, tarefa_id):
        session = self.DBSession()
        execucao = self.model
        # busca uma tarefa iniciada
        filtro = [execucao.tarefa_id == tarefa_id]
        query = session.query(execucao).filter(
            *filtro,
        )
        registros = query.all()
        if not registros:
            return None
        colunas = [column.name for column in self.model.__mapper__.columns]
        remover = ['id', 'tarefa_id', 'inicio', 'fim']
        for item in remover:
            try:
                colunas.remove(item)
            except Exception:
                pass
        linhas = [
            [getattr(valor, column.name)
                for column in self.model.__mapper__.columns
                if not(column.name in remover)]
            for valor in registros]
        return [colunas] + linhas

    def contador_processos_tarefa(self, tarefa_id):
        session = self.DBSession()
        execucao = self.model
        query = session.query(execucao).filter(
            execucao.tarefa_id == tarefa_id
        )
        registros = query.all()
        executadas = [reg.fim for reg in registros if reg.fim is not None]
        ex = len(executadas)
        # ex += 1
        tot = len(registros)
        return ex, tot

    def finalizar_tarefa(self):
        session = self.DBSession()
        tarefa = tables.Tarefa
        robo = self.table_name
        # busca a tarefa iniciada
        query = session.query(tarefa).filter(
            tarefa.inicio.isnot(None),
            tarefa.fim.is_(None),
            tarefa.robo == robo,
        )
        registro = query.first()
        if not registro:
            return None
        # registra a finalização da tarefa
        # registro = tarefa()
        registro.robo = robo
        registro.fim = datetime.now()
        session.add(registro)
        session.commit()
        return registro

    def limpar_tabela(self, tabela):
        session = self.DBSession()
        session.execute('''DELETE FROM {}'''.format(tabela))
        session.commit()

    def reativar_tarefa(self, tarefa_id):
        session = self.DBSession()
        tarefa = tables.Tarefa
        query = session.query(tarefa).filter(
            tarefa.id == tarefa_id,
        )
        registro = query.first()
        registro.fim = None
        session.commit()
        return True

    def selecionar_execucao(self, tarefa_id):
        session = self.DBSession()
        execucao = self.model
        tarefa = tables.Tarefa
        # busca uma tarefa iniciada
        query = session.query(execucao).filter(
            execucao.inicio.isnot(None),
            execucao.fim.is_(None),
            execucao.tarefa_id == tarefa_id
        ).join(tarefa).filter(tarefa.fim.is_(None))
        registro = query.first()
        if registro:
            return registro
        # busca a primeira tarefa livre
        query = session.query(execucao).filter(
            execucao.inicio.is_(None),
            execucao.tarefa_id == tarefa_id
        ).join(tarefa).filter(tarefa.fim.is_(None))
        registro = query.first()
        # se não houver nenhuma livre, retorna vazio
        if not registro:
            return None
        # registra a tarefa livre encontrada como iniciada
        registro.inicio = datetime.now()
        session.add(registro)
        session.commit()
        return registro

    def selecionar_tarefa_ativa(self, criar_nova=False):
        session = self.DBSession()
        tarefa = tables.Tarefa
        robo = self.table_name
        # busca uma tarefa iniciada
        query = session.query(tarefa).filter(
            tarefa.inicio.isnot(None),
            tarefa.fim.is_(None),
            tarefa.robo == robo,
        )
        registro = query.first()
        if registro:
            self.tarefa_nova = False
            return registro
        # registra a entrada da tarefa marcando como iniciada
        if criar_nova:
            registro = tarefa()
            registro.robo = robo
            registro.inicio = datetime.now()
            session.add(registro)
            session.commit()
            self.tarefa_nova = True
            return registro
        return None

    def selecionar_ultima_tarefa_finalizada(self):
        session = self.DBSession()
        tarefa = tables.Tarefa
        robo = self.table_name
        # busca a ultima tarefa finalizada
        query = session.query(tarefa).filter(
            tarefa.inicio.isnot(None),
            tarefa.fim.isnot(None),
            tarefa.robo == robo,
        ).order_by(tarefa.fim.desc())
        return query.first()

    def __del__(self):
        del self.DBSession


# ---------------- Funções de módulo ------
def selecionar_ultima_tarefa_remota_finalizada(tarefa_remota_id):
    ctrl = ControleExecucao()
    ctrl.uri = URI
    ctrl.table_name = 'tarefas'
    ctrl.configurar_base_de_dados()
    return ctrl.selecionar_ultima_tarefa_remota_finalizada(tarefa_remota_id)


def get_id_tarefa_remota(tarefa_id):
    ctrl = ControleExecucao()
    ctrl.uri = URI
    ctrl.table_name = 'tarefas'
    ctrl.configurar_base_de_dados()
    return ctrl.get_id_tarefa_remota(tarefa_id)


def get_tarefa(tarefa_id):
    ctrl = ControleExecucao()
    ctrl.uri = URI
    ctrl.table_name = 'tarefas'
    ctrl.configurar_base_de_dados()
    return ctrl.get_tarefa(tarefa_id)


def reativar_tarefa(tarefa_id):
    ctrl = ControleExecucao()
    ctrl.uri = URI
    ctrl.table_name = 'tarefas'
    ctrl.configurar_base_de_dados()
    return ctrl.reativar_tarefa(tarefa_id)


# ----------------------------------------
if __name__ == "__main__":
    pass
