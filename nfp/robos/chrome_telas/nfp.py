""" Módulo para controle das chrome do sistema Nota Fiscal Paulista

"""
import sys
import time
import logging
from subprocess import Popen, PIPE
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from nfp import CHRDRIVER, CHREXEC, CHRPREFS, URLBASE
from nfp.servicos.interface import abrir_popup


class Nfp():

    url = URLBASE
    exec_path = CHRDRIVER
    default_wait = 20
    implicitly_wait = 15
    default_sleep = 2

    def __init__(self, mes, ano, entidade, usuario='', senha=''):
        self.usuario = usuario
        self.senha = senha
        self.mes = str(mes)
        self.ano = str(ano)
        self.entidade = entidade
        self._abrir_chrome()
        options = webdriver.ChromeOptions()
        caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "normal"  #  espera a pagina estar carregada
        # caps["pageLoadStrategy"] = "eager"  #  interativa
        caps["pageLoadStrategy"] = "none"  # não espera a página carregar
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(options=options, executable_path=self.exec_path, desired_capabilities=caps)
        self.driver.implicitly_wait(self.implicitly_wait)
        self.driver.set_page_load_timeout(self.default_wait)
        return

    def _abrir_chrome(self):
        chrexec = [CHREXEC, '--remote-debugging-port=9222','--user-data-dir={}'.format(CHRPREFS.replace(' ', '\ ')), URLBASE]
        if sys.platform == "win32":
            chrexec = '"{}" --remote-debugging-port=9222 --user-data-dir="{}" {}'.format(CHREXEC, CHRPREFS, URLBASE)
        Popen(chrexec, shell=False, stdout=PIPE).stdout
        msg = 'ROBÔ EM ESPERA\n\nFaça o login no sistema e responda ao captcha.\n'
        msg += 'Após o login, feche esta janela para iniciar a execução.\n'
        abrir_popup(msg)

    def abrir_pagina_login(self, tentativa=0):
        self.driver.get(self.url)
        try:
            self.recaptcha = self.driver.find_element_by_id('captchaPnl')
            logging.info('Pagina de login carregada')
        except NoSuchElementException:
            return 'ERRO: Página NFP sem resposta'
        except TimeoutException:
            if tentativa < 3:
                tentativa += 1
                return self.abrir_pagina_login(tentativa)
            else:
                return 'ERRO: Captcha não apareceu em {} segundos'.format(self.default_wait)
        time.sleep(1)
        return

    def configurar_cadastro(self, tentativa=0):
        tentativa += 1
        logging.info('Configurando cadastro entidade, mês e ano')
        try:
            self.driver.implicitly_wait(5)
            erro = self.driver.find_element_by_xpath('//*[@id="tf_body"]/table/tbody/tr[3]/td/p[3]')
            logging.warning('Erro na abertura da tela:')
            logging.warning(erro.text)
            time.sleep(60)
            if tentativa < 10:
                return self.configurar_cadastro(tentativa)
        except Exception as e:
            if tentativa >= 10:
                raise e
        finally:
            self.driver.implicitly_wait(self.implicitly_wait)
        try:
            elem = self.driver.find_element_by_id('ctl00_ConteudoPagina_btnOk')
            elem.click()
            time.sleep(1)
            self.selecionar('ddlEntidadeFilantropica', self.entidade)
            time.sleep(1)
            self.selecionar('ctl00_ConteudoPagina_ddlMes', self.mes)
            time.sleep(1)
            self.selecionar('ctl00_ConteudoPagina_ddlAno', self.ano)
            time.sleep(1)
            elem = self.driver.find_element_by_id('ctl00_ConteudoPagina_btnNovaNota')
            elem.click()
            self._confirmar_msg()
            logging.info('Cadastro entidade, mês e ano configurado')
            return
        except Exception as e:
            if tentativa < 10:
                time.sleep(5)
                logging.info('Erro ao configurar cadastro. Tentando novamente...')
                self.driver.get(self.url)
                return self.configurar_cadastro(tentativa)
            raise e

    def _confirmar_msg(self):
        try:
            elem = self.driver.find_element_by_xpath("//div[4]/div[11]/div/button[1]")
            elem.click()
        except Exception:
            pass

    def gravar_nota(self, cod_nota, tentativa=0):
        logging.info('Gravando nota fiscal...')
        tentativa += 1
        try:
            elem = self.driver.find_element_by_xpath("//fieldset/div[4]/fieldset/input")
            elem.clear()
            cod_nota = cod_nota.strip()
            logging.info(f'Codigo: {cod_nota} - tentativa: {tentativa}')
            elem.send_keys(Keys.HOME)
            elem.send_keys(cod_nota)
            time.sleep(1)
            elem.send_keys(Keys.ENTER)
            time.sleep(2)
            elem = self.driver.find_element_by_xpath('//*[@id="ConteudoPrincipal"]/div[2]/div[1]')
            logging.info(elem.text)
            if 'Doação registrada com sucesso' in elem.text:
                return 'OK - NF gravada'
            if 'Este pedido já existe no sistema' in elem.text:
                return 'NF ja existe'
            if 'excedeu o prazo máximo para cadastro' in elem.text:
                return 'NF fora do prazo'
            if tentativa < 4:
                return self.gravar_nota(cod_nota, tentativa)
            return 'ERRO: erro ao gravar a NF'
        except Exception:
            if tentativa < 10:
                self.configurar_cadastro()
                return self.gravar_nota(cod_nota, tentativa)
            return 'ERRO: erro ao gravar a NF'

    def logar(self):
        elem = self.driver.find_element_by_id('UserName')
        elem.clear()
        elem.send_keys(self.usuario)
        time.sleep(1)
        elem = self.driver.find_element_by_id('Password')
        elem.clear()
        elem.send_keys(self.senha)
        time.sleep(1)
        logging.info('Aguardando resolução do Captcha')
        self.recaptcha.click()
        msg = 'ROBÔ EM ESPERA\nPor favor responda ao Captcha e em seguida feche'
        msg += '\nessa janela para o robô continuar sua execução.'
        abrir_popup(msg)
        time.sleep(1)
        elem = self.driver.find_element_by_id('Login')
        elem.click()
        try:
            elem = self.driver.find_element_by_id('ctl00_divCaixaPostal')
            logging.info('Página NFP aberta')
        except Exception as e:
            return 'ERRO login: {}'.format(e)
        return

    def selecionar(self, id, valor):
        elem = self.driver.find_element_by_id(id)
        for option in elem.find_elements_by_tag_name('option'):
            if valor.lower() in option.text.lower():
                option.click()
                break
        return
