""" Módulo para controle das telas do sistema Nota Fiscal Paulista
"""
import json
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from nfp import CHRDRIVER
import time
import logging
import PySimpleGUI as sg


class Nfp():

    url = r'https://www.nfp.fazenda.sp.gov.br/login.aspx'
    exec_path = CHRDRIVER
    default_wait = 15
    default_sleep = 2

    def __init__(self, cod_nota, usuario, senha, driver=None):
        self.cod_nota = cod_nota
        self.usuario = usuario
        self.senha = senha
        if driver:
            self.driver = driver
            return
        options = webdriver.ChromeOptions()
        print_settings = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local",
                "account": "",
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2,
        }
        prefs = {
            'printing.print_preview_sticky_settings.appState': json.dumps(print_settings),
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--kiosk-printing')
        # options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options, executable_path=self.exec_path)
        self.driver.implicitly_wait(self.default_wait)
        self.driver.set_page_load_timeout(self.default_wait)
        return

    def abrir_pagina_login(self, tentar_novamente=True):
        self.driver.get(self.url)
        try:
            self.recaptcha = self.driver.find_element_by_id('captchaPnl')
            logging.info('Pagina de login carregada')
        except NoSuchElementException:
            return 'ERRO: Página NFP sem resposta'
        except TimeoutException:
            if tentar_novamente:
                return self.abrir_pagina_login(False)
            else:
                return 'ERRO: Captcha não apareceu em {} segundos'.format(self.default_wait)
        time.sleep(1)
        return

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
        msg = 'ROBÔ EM ESPERA\n Por favor responda ao Captcha e em seguida feche'
        msg += '\n essa janela para o robô continuar sua execução.'
        sg.popup(msg)
        time.sleep(1)
        elem = self.driver.find_element_by_id('Login')
        elem.click()
        try:
            elem = self.driver.find_element_by_id('ctl00_divCaixaPostal')
            logging.info('Página NFP aberta')
        except Exception as e:
            return 'ERRO login: {}'.format(e)
        time.sleep(self.default_sleep)
        return

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass
