from bs4 import BeautifulSoup
import pandas as panda

class CsvResponsavel():
  def __init__(self, html):
    self.__soup = BeautifulSoup(html, "html.parser")


  def cria_arquivo(self):
    panda.DataFrame(columns = ["url_img", "titulo", "data_postagem", "resumo",]).to_csv(path_or_buf = "informacoes_web.csv")

  def escreve_no_arquivo(self):
    for row in self.__soup.find_all(name = "div", attrs = {"class" : "row"}):

      conteudo_do_post = row.find(name = "div", attrs = {"class" : "post-content"})
      
      url_img = row.find(name = "img")
      titulo = conteudo_do_post.find(name = "h3").a.text
      data_da_postagem = conteudo_do_post.find(name = "div", attrs = {"class" : "post-date"}).p.text
      resumo = row.find(name = 'div', attrs = {"class" : "post-excerpt"}).p.next_sibling.text

      panda.DataFrame(data = [ url_img, titulo, data_da_postagem, resumo ]).to_csv('informacoes_web.csv', mode = 'a', header = False)