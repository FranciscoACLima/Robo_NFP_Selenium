# Robo_NFP_Selenium

Robô de cadastro de Nota Fiscal Paulista para instituições sem fins lucrativos.


## Instalação do ambiente de desenvolvimento e execução

`cd <diretorio>/Robo_NFP_Selenium`

Para alterar as configurações padrão da aplicação, criar o arquivo `nfp/config.py` de acordo com o exemplo: `config_exemplo.py`

Criar um ambiente virtual: 
`virtualenv venv`

Ativar o ambiente Windows: 
`venv/scripts/activate` 

Ativar o ambiente Linux: 
`source venv/bin/activate`

Instalar as dependências: 
`pip install -r requirements.txt`

Observações para instalação no Linux:

Instalar o pacote `python3-tk` para que a interface gráfica funcione.


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