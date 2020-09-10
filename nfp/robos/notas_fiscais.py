import logging
from nfp.servicos.controles.notas_fiscais import (selecionar_execucao, finalizar_execucao,
                                                  contar_processos_executados, selecionar_tarefa_ativa)
from nfp.servicos.interface import abrir_popup
from nfp.telas.nfp import Nfp


class CadastraNFP():

    meses = {
        'Janeiro': '01',
        'Fevereiro': '02',
        'Março': '03',
        'Abril': '04',
        'Maio': '05',
        'Junho': '06',
        'Julho': '07',
        'Agosto': '08',
        'Setembro': '09',
        'Outubro': '10',
        'Novembro': '11',
        'Dezembro': '12'
    }

    def __init__(self, parametros):
        self.entidade = parametros['entidade']
        self.mes = self.meses[parametros['mes']]
        self.ano = parametros['ano']
        logging.info('Mês/Ano: {}/{}'.format(self.mes, self.ano))
        logging.info('Entidade: {}'.format(self.entidade))

    def main(self):
        tela = None
        while(True):
            entrada = selecionar_execucao()
            if not entrada:
                return selecionar_tarefa_ativa()
            if not tela:
                tela = Nfp(self.mes, self.ano, self.entidade)
                tela.configurar_cadastro()
            self.id = entrada.id
            self.tarefa_id = entrada.tarefa_id
            cod_nota = entrada.cod_nota
            retorno = self.gravar_nota(cod_nota, tela)
            self.retornar_resultado(retorno, entrada)

    def gravar_nota(self, cod_nota, tela):
        retorno = tela.gravar_nota(cod_nota)
        return retorno

    def retornar_resultado(self, retorno, entrada):
        log = 'Retorno: {}'.format(retorno)
        logging.info(log)
        resultado = {'resultado': retorno}
        finalizar_execucao(self.id, resultado)
        ex, tot = contar_processos_executados(self.tarefa_id)
        texto = ' {} de {} notas carregadas'.format(ex, tot)
        abrir_popup(texto, 4)


if __name__ == "__main__":
    parametros = {
        'mes': '08',
        'ano': '2020',
        'entidade': 'CREN - CENTRO DE RECUPERAÇÃO E EDUCAÇÃO NUTRICIONAL'
    }
    robo = CadastraNFP(parametros)
    result = robo.main()
    print('Resultado:', result)
