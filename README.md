# Robo_NFP_Selenium

Robô de cadastro de Nota Fiscal Paulista para instituições sem fins lucrativos.

Na execução, o robô aguarda que o usuário faça o login e responda ao captcha antes de iniciar o cadastro das notas.

O robô foi desenvolvido para ser executado no navegador ``Google Chrome`` 

## Utilitário Divide Planilha

Para auxiliar na distribuição da execução do robô em mais de um computador, foi incluído um utilitário para divisão de uma planilha no formato excel ou csv em várias.


## Executável para Windows 64

https://github.com/FranciscoACLima/Robo_NFP_Selenium/releases/download/0.1.1/RoboNFP_WIN64.zip

## Preparação do código para criação do ambiente de desenvolvimento

Crie um diretório para o projeto e dentro dele faça o clone do repositório
`git clone https://github.com/FranciscoACLima/Robo_NFP_Selenium.git`

### Preparação do ambiente para execução no Python 3

O projeto está preparado para utilizar o [virtualenv](https://virtualenv.pypa.io/en/latest/) para desenvolvimento e execução da aplicação
Instale o pacote virtualenv no Python
`pip install virtualenv`
ou 
`pip3 install virtualenv`

Entre na pasta do repositório e crie um ambiente virtual chamado venv

`cd <diretorio>/Robo_NFP_Selenium`

Criar um ambiente virtual: 
`virtualenv venv`

Ative o ambiente virtual

No Windows: 
`venv/scripts/activate` 

No Linux: 
`source venv/bin/activate`

Instale as dependências necessárias: 
`pip install -r requirements.txt`

Observações para instalação no Linux:

Instale também o pacote `python3-tk` para que a interface gráfica funcione.

Altere as configurações padrão da aplicação, criando o arquivo `nfp/config.py` de acordo com o exemplo: `config_exemplo.py`

### Execução em desenvolvimento

`python run.py`


### Execução via script:

Windows: 
`executar_robo.cmd`

Linux: 
`./executar_robo.sh`

Os scripts cmd e sh estão configurados para utilizar o ambiente virtual `venv`


## Atualização do chromedriver:

O robô utiliza a biblioteca [Selenium](https://www.selenium.dev/) para automatizar o navegador **Google Chrome** através do executável [chromedriver](https://chromedriver.chromium.org/downloads).

A partir da versão 0.0.3, aplicação verifica a versão do navegador **Chrome** instalado e faz o donwload da versão do **crhomedriver** correspondente de forma automática.


