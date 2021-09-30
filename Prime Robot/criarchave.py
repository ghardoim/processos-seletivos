from selenium import webdriver
from bs4 import BeautifulSoup
from os import getenv
import requests as rq

xpath_base = '//*[@id="content"]/div/div[2]/div/div'

def get_meu_ip():
    return BeautifulSoup(rq.get("https://www.meuip.com.br/").text, 'html.parser').find("h3").text.split(" ")[3]

browser = webdriver.Chrome()
browser.get("https://developer.clashroyale.com/#/login")

browser.find_element_by_id("email").send_keys(getenv("email"))
browser.find_element_by_id("password").send_keys(getenv("senha"))
browser.find_element_by_xpath(f'{xpath_base}/div/div/div/div/form/div[4]/button').click()

browser.get("https://developer.clashroyale.com/#/accounts")
browser.find_element_by_xpath(f'{xpath_base}/section[2]/div/div/div[2]/p/a').click()

browser.find_element_by_id("name").send_keys("prime_bot")
browser.find_element_by_id("description").send_keys("Desafio Prime Bot")
browser.find_element_by_id("range-0").send_keys(get_meu_ip())
browser.find_element_by_xpath(f'{xpath_base}/section/div/div/div[2]/form/div[5]/button').click()