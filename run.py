""" Módulo de entrada da aplicação
"""
from nfp.servicos.chrome import conferir_chrome
from nfp.servicos.interface import abrir_popup


def main():
    res, v_chrome, v_driver = conferir_chrome()
    if not(res):
        msg = 'A versão do chromedriver({}) é diferente da versão do navegador({})'.format(v_driver, v_chrome)
        msg += '\nBaixe uma nova versão em https://chromedriver.chromium.org/downloads'
        abrir_popup(msg)
        return
    try:
        from nfp.tela_robo import TelaRobo
        robo = TelaRobo()
        robo.main()
    except Exception as e:
        print('Houve um erro ao executar a aplicação')
        print(str(e))


# --------------------------------------
if __name__ == "__main__":
    main()
