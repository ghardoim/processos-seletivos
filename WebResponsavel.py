from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import time

class WebResponsavel():
  def __init__(self, drive):
    self.__drive = webdriver.Edge(executable_path = drive)

  def abre_pagina(self):
    
    self.__drive.get("http://www.csa-ma.com.br/")
    self.__drive.find_element_by_xpath("//*[text()='Blog']").click()

  def get_html(self):
    
    while True:
      try:
        self.__drive.find_element_by_class_name("load-more-button").click()
      except NoSuchElementException:
        break
      time.sleep(2.5)

    lista_de_posts = self.__drive.find_element_by_class_name("span9")
    html = lista_de_posts.get_attribute("innerHTML")
    
    return html

  def escreve_no_campo(self, campo, texto, posicao = 0):
    self.__drive.find_element_by_xpath(f"//*[text()='name=\"{campo}\"']")[posicao].send_keys(f"{texto}")

  def envia_formulario(self):
    self.__drive.find_element_by_xpath("//*[text()='value=\"Enviar\"']").click()
    
    self.__drive.close()

