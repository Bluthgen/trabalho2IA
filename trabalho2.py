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
import re

#import ply.lex as lex
#import ply.yacc as yacc


#import PyPDF2

#import nltk
#nltk.download('stopwords')

path= os.path.realpath(__file__)[:-12] + "Artigos\\"
pdfs= [arq for arq in glob.glob(path + "*.pdf")]
artigos= []
artigosFull= []
referencias= []
count= 0
stopwords= corpus.stopwords.words('english')
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
        separadas.extend(re.split("\s|,|;|\.|\(|\)|\xe2\x80\x94",linha) for linha in linhas)
        i= 1
        separadas= [linhaSeparada for linhaSeparada in separadas if len(linhaSeparada) > 0]
        
        #Juntando palavras quebradas pela mudança de linha
        for linhaSeparada in separadas:
            if len(linhaSeparada) > 0 and len(linhaSeparada[-1]) > 0:
                if linhaSeparada[-1][-1] == "-":
                    temp= linhaSeparada[-1][:-1]
                    linhaSeparada.remove(linhaSeparada[-1])
                    linhaSeparada.append(temp + separadas[i][0])
                    separadas[i].remove(separadas[i][0])
            i= i+1
        #separadas= word_tokenize(buffer.getvalue())
        atual= [y for x in separadas for y in x]
        #print(atual)
        artigos.append([palavra.lower() for palavra in atual if palavra.isalpha()])
        artigosFull.append(atual)
        #print(artigos)
        break
tudoRelevante= [y for x in artigos for y in x if not y in stopwords and len(y)>2]
tudo= [y for x in artigosFull for y in x]
frequenciaRelevante= FreqDist(tudoRelevante)
print(frequenciaRelevante.most_common(10))

for artigo in artigosFull:
    indice= 0
    listaTemp= artigo[:]
    print(listaTemp.count("REFERENCES"))
    if listaTemp.count("REFERENCES") == 1:
        indice= tudo.index("REFERENCES")
        teste= artigo[indice:]
        #Não está funcionando esta parte
        #print(teste[teste.index("“"):teste.index("”") + 1])
    elif listaTemp.count("REFERENCES") > 1:
        for i in range(listaTemp.count("REFERENCES") - 1):
            listaTemp= listaTemp[listaTemp.index("REFERENCES")+1 : ]
        indice= listaTemp.index("REFERENCES")
        print(artigo[indice:])
        exit()
#frequenciaFull= FreqDist(y for x in artigosFull for y in x)

#print(len([y for x in artigos for y in x if y.lower() not in stopwords]) / len([y for x in artigos for y in  x])) #0.546361893147
