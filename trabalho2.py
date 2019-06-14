# coding= utf-8
# #!python2

from __future__ import division

#import textract
import glob
import os
import re
from StringIO import StringIO

import igraph
import numpy
import plotly
from nltk import *

#import ply.lex as lex
#import ply.yacc as yacc

#import nltk
#nltk.download('stopwords')

#erro citação com et all aquivo 120 erro, 120 com lixo

#titulo e autor sujo nao arrumar com split ,' espaço
#50 algumas referencias tem a palavra [online] acho melhor arrumar quando acabar tudo

#erros
#13 referencia 22 virgula no titulo
#20 referencia 30 com ponto
#21 referencia 3 e 7 virgula no titulo
#22 referencia 13 titulo e autor errado, não mude isso para tratar pois da outro erro len(aux2) > 20
#29 referencia 13 titulo com ponto
#29 referencia 36 virgula no titulo
#29 varias referencias o titulo é pego como o nome da sigla, mas as vezes não
#48 referencia 7 virgula no titulo
#49 referencia 38 () não lidos no titulo
#49 referencia 41 e 42 idiota inverteu os campos de titulo e autor
#Parei de ver erros que não se destacao 
#98 referencia 98 titulo com virgula
#118 mexi na verificação do And não sei se ferrou algo

def retiraRef(preLinhas):
    linhasP = re.sub(r"\. \(.*\d*\)." and r"\(.*\d*\).", "," ,preLinhas)
    linhasP = re.split("\n|\r", linhasP)
    
    linhassP = []
    i=0
    firstTime=0
    jaAdd=0
    posb=0
    linhasP = [linha for linha in linhasP if len(linha) > 0]
    #print(linhasP)
    #print(linhasP)
    for linhass in linhasP:
        i=i+1
        if len(linhass)>0 and linhass[0] == "[" and re.search(r"\d", linhass[1]):
            if firstTime==0:
                posb=i
                firstTime=1
            else:
                if posb == (i-1):
                    if jaAdd==0:
                        linhassP.append(re.sub(r"\[\d*\]","", linhasP[posb-1]))
                    jaAdd=0
                    #print(linhasP[posb-1])
                    posb=i
                else:
                    new = ""
                    for k in range(posb, i):
                        new = new + " " + linhasP[k-1]
                    linhassP.append(re.sub(r"\[\d*\]","", new))
                    #print(new)
                    jaAdd=0
                    posb=i
    if linhasP[posb-1] != linhasP[-1]:
        linhassP.append(re.sub(r"\[\d*\]","", linhasP[posb-1]))
    linhasP= [linha for linha in linhassP]
    linhas = []
    linhas.extend(re.split("\"",linha) for linha in linhasP)
    #print(linhas)
    autor = []
    titulo = []

    for linha in linhas:
        #print(linha)
        if len(linha)>1:
            titulo.append(linha[1])
            aux = []
            aux.extend(re.split("\,| and|et al.",linha[0]))
            autores=[]
            for aux2 in aux:
                if len(aux2) > 1:
                    autores.append(aux2)
            autor.append(autores)
            #print(autores)
            #print(linha[1])
        else:
            aux = []
            aux.extend(re.split("\,",linha[0]))
            if re.search(r"^ and (.*)", aux[0]) is not None:
                aux2 = []
                aux2.extend(re.split("and",aux[0]))
                autor.append(aux2)
            #    print(aux2)

                if re.search(r"^[Online]. Available: ", str(aux)):
                    aux[1] = re.sub(r"\[Online]. Available:","", str(aux[1]))
                    titulo.append(aux[1])
            #        print(aux[1])
                else:
                    aux2 = []
                    i=1
                    if re.search("^ Eds", str(aux[i])):
                       i=i+1
                    aux2.extend(re.split("\.",aux[i]))
                    titulo.append(aux2[0])
            #        print(aux2[0])
            else:
                i=0
                aux3 = []
                for aux2 in aux:
                    i=i+1
                    if re.search(r"^ and (.*)", aux2):
                        aux4 = []
                        aux4.extend(re.split("and",aux2))
                        aux3.append(aux4[1])
                        autor.append(aux3)
            #            print(aux3)
                        
                        if re.search(r"\[Online]. Available: ", str(aux2)) is not None:
                            titulo.append([])
            #                print("[]")
                        else:
                            auxT = []
                            if re.search("^ Eds.", aux2):
                                i=i+1
                            auxT.extend(re.split("\.",aux[i]))
                            titulo.append(auxT[0])
            #                print(auxT[0])
                        break
                    elif re.search(r"^ Eds.", aux2) is not None:
                        if re.search(r"\[Online]. Available: ", str(aux)) is not None:
                            titulo.append([])
            #                print("[]")
                        else:
                            auxT = []
                            auxT.extend(re.split("\.",aux[i]))
                            titulo.append(auxT[0])
                        autor.append(aux3)
            #            print(aux3)
            #            print(auxT[0])
                        break
                        
                    if len(aux2) > 20:
                        #linha mudada do et al que citei
                        aux[0]=re.sub(r"et al.","", aux[0])
                        aux3 = []
                        aux3.append(aux[0])
                        autor.append(aux3)
            #            print(aux3)

                        if re.search(r"^[Online]. Available: ", str(aux[1])) is not None:
                            titulo.append([])
            #                print("[]")
                        else:
                            auxT = []
                            auxT.extend(re.split("\.",aux[1]))
                            titulo.append(auxT[0])
            #                print(auxT[0])

                        
                        break
                    else:
                        aux3.append(aux2)
                        
                    
    #print(autor)
    #print(titulo)
    return (autor, titulo)
        
def retiraAutorTitulo(texto):
    autorStopWords= ["IEEE", "Fellow", "Member", "Student", "Senior"]
    linhas= re.split("\n", text)
    linhaTitulo= linhas[4]
    linhaAutores= linhas[5]
    autores= []
    if linhaAutores.count(", ") > 0:
        autoresQuebrado= linhaAutores.split(", ")
        for parte in autoresQuebrado:
            if len(parte) < 2:
                continue
            flag= False
            for stopWord in autorStopWords:
                if parte.count(stopWord) > 0:
                    flag= True
                    break
            if flag:
                continue
            if not parte.startswith("and "):
                autores.append(parte)
            else:
                partes= parte.split("and ")
                for parcial in partes:
                    if len(parcial) > 1:
                        autores.append(parcial)
    elif linhaAutores.count(" and ") > 0:
        partes= linhaAutores.split(" and ")
        for parcial in partes:
            if len(parcial) > 1:
                autores.append(parcial)
    autoresFinal= []
    for autor in autores:
        if autor.endswith("\r"):
            autor= autor[:-1]
        autoresFinal.append(autor)
    return (autoresFinal, linhaTitulo)

def montaGrafo(referencias):
    trabalhos= []
    citados= []
    for referencia in referencias:
        if referencia[0][1].endswith("\r"):
            trabalhos.append(referencia[0][1][:-1])
        else:
            trabalho.append(referencia[0][1])
        temp= []
        for titulo in referencia[1][1]:
            if titulo.endswith("\r"):
                temp.append(titulo[:-1])
            else:
                temp.append(titulo)
        citados.append(temp)
    #print(trabalhos)        
    temp= []
    for grupo in trabalhos:
        temp.append(grupo)
    for grupo in citados:
        #temp.extend(grupo)
        for titulo in grupo:
            if titulo.endswith("\r"):
                temp.append(titulo[:-1])
            else:
                temp.append(titulo)
    vertices= []
    [vertices.append(x) for x in temp if x not in vertices]
    #print(trabalhos)
    #print(citados)
    #print(vertices)
    grafo= igraph.Graph()
    grafo.add_vertices(len(vertices))
    grafo.vs["Autores"]= vertices
    edges= []
    for trabalho in trabalhos:
        indice= trabalhos.index(trabalho)
        for citado in citados[indice]:
            indice1= vertices.index(trabalho)
            indice2= vertices.index(citado)
            edges.append((indice1, indice2))
    grafo.add_edges(edges)
    
    layout= grafo.layout("kk")
    #igraph.plot(grafo, layout= layout)
    Xn= [layout[k][0] for k in range(len(vertices))]
    Yn= [layout[k][1] for k in range(len(vertices))]
    Xe= []
    Ye= []
    for e in edges:
        Xe+= [layout[e[0]][0], layout[e[1]][0], None]
        Ye+= [layout[e[0]][1], layout[e[1]][1], None]
    #grafo.es["Titulos"]= titulos
    
    trace1= plotly.graph_objs.Scatter(x= Xe, y= Ye, mode= "lines", line= dict(color= "rgb(125,125,125)", width= 1))
    trace2= plotly.graph_objs.Scatter(x= Xn, y= Yn, mode= "markers", name="Artigos", marker=dict(symbol='circle',
                             size=6,
                             color=[],
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=vertices,
               hoverinfo='text')
    axis=dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')
    
    plotLayout= plotly.graph_objs.Layout(title="Grafo das relações de citação entre os Artigos analizados",
         width=1000,
         height=1000,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
            ),
        margin=dict(
        t=100
            ),
        hovermode='closest')

    fig= plotly.graph_objs.Figure(data= [trace1, trace2], layout= plotLayout)
    
    plotly.offline.plot(fig, filename= "Citacoes.html")

    return grafo

path= os.path.realpath(__file__)[:-12] + "Artigos\\"
pdfs= [arq for arq in glob.glob(path + "*.txt")]
artigos= []
artigosFull= []
referencias= []
count= 0
stopwords= corpus.stopwords.words('english')
referencias= []
for pdf in pdfs:
    #text = textract.process(pdf)
    text= []
    with open(pdf, "r") as arquivo:
        text= arquivo.read()
    #print(text) 
    retiraAutorTitulo(text)
    preLinhas = re.split("REFERENCES",text)
    linhas= preLinhas[0].splitlines()
    temp1= retiraRef(preLinhas[1])
    temp2= retiraAutorTitulo(text)
    referencias.append((temp2, temp1))
    continue
    '''
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
    '''
montaGrafo(referencias)
exit()
tudoRelevante= [y for x in artigos for y in x if not y in stopwords and len(y)>2]
tudo= [y for x in artigosFull for y in x]
frequenciaRelevante= FreqDist(tudoRelevante)
print(frequenciaRelevante.most_common(10))
