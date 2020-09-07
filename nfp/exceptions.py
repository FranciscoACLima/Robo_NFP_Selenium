""" Módulo para controle de exceções customizadas """


class ErroExtracaoDadosPlanilhaException():

    def __init__(self, msg=''):
        self.message = msg


class PlanilhaInexistenteException():

    def __init__(self, msg=''):
        self.message = msg
