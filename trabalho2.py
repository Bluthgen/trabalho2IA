# coding= utf-8
# #!python2

from __future__ import division

import glob
import os
from StringIO import StringIO

import numpy
from nltk import *
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
#import pdfminer
from pdfminer.pdfparser import PDFParser

#import ply.lex as lex
#import ply.yacc as yacc


#import PyPDF2

#nltk.download()

path= os.path.realpath(__file__)[:-12] + "Artigos\\"
pdfs= [arq for arq in glob.glob(path + "*.pdf")]
artigos= []
count= 0
for pdf in pdfs:
    with open(pdf, "rb") as artigo:
        if count < -1:
            count= count+1
            continue
        atual= []
        leitor= PDFParser(artigo)
        documento= PDFDocument(leitor)
        gerenciador= PDFResourceManager()
        buffer= StringIO()
        parametros= LAParams()
        codec= "utf-8"
        conversor= TextConverter(gerenciador, buffer, codec= codec, laparams= parametros)
        interpretador= PDFPageInterpreter(gerenciador, conversor)
        for pagina in PDFPage.create_pages(documento):
            interpretador.process_page(pagina)
        linhas= buffer.getvalue().splitlines()
        separadas= []
        separadas.extend(linha.split() for linha in linhas)
        atual= [y for x in separadas for y in x]
        #print(atual)
        artigos.append([palavra.lower() for palavra in atual if palavra.isalpha()])
        #print(artigos)
        #exit()
tudo= [y for x in artigos for y in x if len(y) > 4]
frequenciaGlobal= FreqDist(tudo)
print(frequenciaGlobal.most_common(10))
