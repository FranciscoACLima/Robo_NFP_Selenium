""" Módulo de entrada da aplicação
"""
from nfp.servicos.chrome import conferir_chrome
from nfp.servicos.interface import abrir_popup


def main():
    res, v_chrome, v_driver = conferir_chrome()
    if not res:
        msg = 'A versão do chromedriver({}) é diferente da versão do navegador({})'.format(v_driver, v_chrome)
        msg += '\nBaixe uma nova versão em https://chromedriver.chromium.org/downloads'
        msg += '\n\nO arquivo deve ser descompactado em nfp\\binaries'
        if not v_chrome:
            msg = 'Esta aplicação depende do navegador Google Chrome, mas não foi possível localizar onde ele está instalado'
            msg += '\n\nPor favor, instale o Google Chrome ou indique o local de sua instalação no arquivo nfp\\config.py'
            msg += '\n\nExemplo de uso em config_exemplo.py'
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
