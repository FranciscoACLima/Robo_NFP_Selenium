""" Módulo de entrada da aplicação
"""


def main():
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
