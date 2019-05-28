import glob
import os

import PyPDF2

path= os.path.realpath(__file__)[:-12] + "Artigos\\"
pdfs= [arq for arq in glob.glob(path + "*.pdf")]

for pdf in pdfs:
    with open(pdf, "rb") as artigo:
        leitor= PyPDF2.PdfFileReader(artigo)
        for pagina in leitor.pages:
            print(pagina.extractText())
    exit()
