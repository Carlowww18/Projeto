import os
from selenium import webdriver
from pathlib import Path
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Define o caminho correto para o ChromeDriver
ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME

def make_chrome_browser(*options):
    # Configura as opções do Chrome
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    # Cria o serviço do ChromeDriver
    chrome_service = Service(executable_path=ChromeDriverManager().install())

    # Inicializa o navegador usando o ChromeDriver
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

    return browser


if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    # Acessa o site
    browser.get('http://www.google.com.br/')
    sleep(3)
    browser.quit()