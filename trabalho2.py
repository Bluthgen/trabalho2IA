# coding= utf-8
# #!python2

from __future__ import division

import textract
import glob
import os
from StringIO import StringIO

import numpy
from nltk import *
import re

#import ply.lex as lex
#import ply.yacc as yacc

#import nltk
#nltk.download('stopwords')

#erro citação com et all aquivo 120 erro, citação online, nome de Majdandzic lendo errado, 120 com lixo, 13 citação 22(, no nome) erro e 26(online)
#linhasP tem a divisão das referencias
def retiraRef(preLinhas):
    linhasP = re.sub("\n", " " ,preLinhas)
    linhasP = re.split(r"\[\d*\]", linhasP)
    linhasP= [linha for linha in linhasP if len(linha) > 5]
    linhas = []
    linhas.extend(re.split("\"",linha) for linha in linhasP)
    autor = []
    titulo = []

    for linha in linhas:
        #print(linha)
        if len(linha)>1:
            #ta adicionando um virgula no final não arrume com slipt
            titulo.append(linha[1])
            aux = []
            aux.extend(re.split("\,|and|et al.",linha[0]))
            autores=[]
            for aux2 in aux:
                if len(aux2) > 1:
                    autores.append(aux2)
            autor.append(autores)
            #print(autores)
        else:
            aux = []
            aux.extend(re.split("\,",linha[0]))
            if re.search("and", aux[0]) is not None:
                aux2 = []
                aux2.extend(re.split("\.",aux[1]))
                titulo.append(aux2[0])

                aux2 = []
                aux2.extend(re.split("and",aux[0]))
                autor.append(aux2)
                #print(aux2)
            else:
                i=0
                aux3 = []
                for aux2 in aux:
                    i=i+1
                    if len(aux2) > 20:
                        auxT = []
                        auxT.extend(re.split("\.",aux[1]))
                        titulo.append(auxT[0])

                        aux3 = []
                        aux3.append(aux[0])
                        autor.append(aux3)
                        break
                    
                    if re.search(r"^ and (.*)", aux2) is not None:
                        auxT = []
                        auxT.extend(re.split("\.",aux[i]))
                        titulo.append(auxT[0])
                        
                        aux4 = []
                        aux4.extend(re.split("and",aux2))
                        aux3.append(aux4[1])
                        autor.append(aux3)
                        break
                    else:
                        aux3.append(aux2)
                        
                    
    print(autor)
    print(titulo)
        

path= os.path.realpath(__file__)[:-12] + "Artigos\\"
pdfs= [arq for arq in glob.glob(path + "17.pdf")]
artigos= []
artigosFull= []
referencias= []
count= 0
stopwords= corpus.stopwords.words('english')
for pdf in pdfs:
    text = textract.process(pdf)
    preLinhas = re.split("REFERENCES",text)
    linhas= preLinhas[0].splitlines()
    retiraRef(preLinhas[1])
    separadas= []
    #print(linhas)
    separadas.extend(re.split("\s|,|;|\.|\(|\)",linha) for linha in linhas)
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
