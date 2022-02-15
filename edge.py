from selenium import webdriver
from settings import EDGE_DRIVER
from selenium.webdriver.edge import service as fs


def edge_browser():
    """edgeブラウザを返す"""
    edge_driver = EDGE_DRIVER
    edge_service = fs.Service(executable_path=edge_driver)
    browser = webdriver.Edge(service=edge_service)

    return browser
