import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_driver(config):
    options = webdriver.ChromeOptions()
    if config['webdriver']['options']['headless']:
        options.add_argument('--headless')
    if config['webdriver']['options']['disable_gpu']:
        options.add_argument('--disable-gpu')
    if config['webdriver']['options']['no_sandbox']:
        options.add_argument('--no-sandbox')
    if config['webdriver']['options']['start_maximized']:
        options.add_argument('start-maximized')
    if config['webdriver']['options']['disable_infobars']:
        options.add_argument('disable-infobars')
    if config['webdriver']['options']['disable_extensions']:
        options.add_argument('--disable-extensions')

    user_agent = config['webdriver']['user_agent']
    options.add_argument(f'user-agent={user_agent}')

    path_to_chromedriver = config['webdriver']['chrome_driver_path']
    expanded_path = os.path.expanduser(path_to_chromedriver)
    service = Service(executable_path=expanded_path)
    driver = webdriver.Chrome(service=service, options=options)
    logging.info("WebDriver setup complete.")
    return driver
