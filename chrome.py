from selenium import webdriver
from settings import CHROME_DRIVER
from selenium.webdriver.chrome import service as fs


def chrome_browser():
    """chromeブラウザを返す"""
    chrome_driver = CHROME_DRIVER
    chrome_service = fs.Service(executable_path=chrome_driver)
    browser = webdriver.Chrome(service=chrome_service)

    return browser
