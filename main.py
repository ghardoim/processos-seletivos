from WebResponsavel import WebResponsavel
from CsvResponsavel import CsvResponsavel

wr = WebResponsavel("msedgedriver.exe")
wr.abre_pagina()
html = wr.get_html()
wr.escreve_no_campo("your-name", "Gabriel Hardoim")
wr.escreve_no_campo("Assunto", "Teste processo seletivo Dev RPA")
wr.escreve_no_campo("tel-957", "(21) 96986-5903")
wr.escreve_no_campo("your-name", "CSA - RDP", 1)
wr.escreve_no_campo("your-email", "ghardoim@hotmail.com")
wr.escreve_no_campo("url-541", "https://github.com/ghards")
wr.escreve_no_campo("your-message", "Gostaria de fazer parte do time RPD pois sou um entusiasta da automação de processos e seria formidavél poder contribuir e aprender com uma empresa focada nisso!")
wr.envia_formulario()

cr = CsvResponsavel(html)
cr.cria_arquivo()
cr.escreve_no_arquivo()