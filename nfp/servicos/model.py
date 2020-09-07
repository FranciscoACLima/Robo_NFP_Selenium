from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class NotaFiscal(Base):
    __tablename__ = 'notas_fiscais'

    id = Column(Integer, primary_key=True)
    tarefa_id = Column(Integer, ForeignKey('tarefas.id'), nullable=False)
    cod_nota = Column(String, nullable=False)
    inicio = Column(DateTime)
    fim = Column(DateTime)
    resultado = Column(String)
    tarefa = relationship('Tarefa', foreign_keys=tarefa_id)

    def __repr__(self):
        return "<NotaFiscal(num_proc='{}')>".format(self.num_proc)


class Tarefa(Base):
    __tablename__ = 'tarefas'

    id = Column(Integer, primary_key=True)
    robo = Column(String, nullable=False)
    inicio = Column(DateTime)
    fim = Column(DateTime)
    status = Column(String)

    def __repr__(self):
        return "<Tarefa(id='{}'; robo='{}')>".format(self.id, self.robo)
