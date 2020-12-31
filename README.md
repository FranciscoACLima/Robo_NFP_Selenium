# Robo_NFP_Selenium

Robô de cadastro de Nota Fiscal Paulista para instituições sem fins lucrativos.

## Instalação do ambiente de desenvolvimento e execução

`cd <diretorio>/Robo_NFP_Selenium`

Criar o arquivo `nfp\config.py` de acordo com o exemplo: `config_exemplo.py`

Criar um ambiente virtual: 
`virtualenv venv`

Ativar o ambiente Windows: 
`venv\scripts\activate` 

Ativar o ambiente Linux: 
`source venv/bi/activate`

Instalar as dependências: 
`pip install -r requirements.txt`

Observações para instalação no Linux:

Instalar o pacote `python3-tk` para que a interface gráfica funcione

### Execução em desenvolvimento

`python run.py`

### Execução via script:

Windows: 
`executar_robo.cmd`

Linux: 
`executar_robo.sh`