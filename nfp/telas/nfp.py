""" Módulo para controle das telas do sistema Nota Fiscal Paulista
"""
import json
from selenium import webdriver
from nfp import CHRDRIVER
import time
import logging


class Nfp():

    url = r'https://www.nfp.fazenda.sp.gov.br/login.aspx?ReturnUrl=%2f'
    exec_path = CHRDRIVER
    default_wait = 60

    def __init__(self, usuario, senha):
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

    def abrir_pagina_login(self):
        self.driver.get(self.url)
        elem = self.driver.find_element_by_id('captchaPnl')
        logging.info('Pagina de login carregada')
        time.sleep(10)
        return elem

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass
