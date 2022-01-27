# Robo_NFP_Selenium

Robô de cadastro de Nota Fiscal Paulista para instituições sem fins lucrativos.

## Preparação do código para criação do ambiente de desenvolvimento

Crie um diretório para o projeto e dentro dele faça o clone do repositório
`git clone https://github.com/FranciscoACLima/Robo_NFP_Selenium.git`

## Instalação do ambiente de desenvolvimento e execução

Antes de mais nada, instale o pacote virtualenv no Python
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
`executar_robo.sh`

Os scripts estão configurados para utilizar o ambiente virtual `venv`


## Aviso de atualização do chromedriver:

O Selenium automatiza o navegador Google Chrome a partir do executável chromedriver (https://chromedriver.chromium.org/downloads).

A aplicação verifica a versão do Navegador Chrome instalado com a versão do chromedriver presente no diretório `nfp/binaries`.
Havendo diferença entre eles, **abre um popup informando as versões encontradas** e fecha a aplicação.

Substitua o executável em `nfp/binaries` pelo correspondente à versão do Chrome instalado.
