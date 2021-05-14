import requests as req
import zipfile as zf

def leLinhas(file, sep = None):
  with arquivozip.open(file, "r") as csvfile:
    return [ linha.decode("utf8").rstrip().split(sep) for linha in csvfile.readlines() ]

filename = "teste_true_term.zip"
resp = req.get("https://datawarehouse-true.s3-sa-east-1.amazonaws.com/teste-true/teste_true_term.zip")

with open(filename, "wb") as download:
  download.write(resp.content)

with zf.ZipFile(filename, "r") as arquivozip:
  linhasCSV = leLinhas("encad-termicas.csv", ",")
  linhasDAT = leLinhas("TERM.DAT")
  
  usinasCSV = [ linha[1] for linha in linhasCSV ]
  usinasDAT = [ linha[1] for linha in linhasDAT ]
  
  for usina in usinasCSV:
    if usina != "nome" and usina in usinasDAT:
      linhasDAT[usinasDAT.index(usina)] = linhasCSV[usinasCSV.index(usina)] 

with zf.ZipFile(filename, "w") as arquivozip:
  with arquivozip.open("TERM_TRUE.DAT", "w") as new:
    [ new.write(str(linha).encode()) for linha in linhasDAT ]


