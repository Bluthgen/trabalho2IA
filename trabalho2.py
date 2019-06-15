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

def retiraRef(preLinhas):
    linhasP = re.sub(r"\. \(.*\d*\)." and r"\(.*\d*\).", "," ,preLinhas)
    linhasP = re.split("\n|\r", linhasP)
    
    linhassP = []
    i=0
    firstTime=0
    jaAdd=0
    posb=0
    linhasP = [linha for linha in linhasP if len(linha) > 0]
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
                    posb=i
                else:
                    new = ""
                    for k in range(posb, i):
                        new = new + " " + linhasP[k-1]
                    linhassP.append(re.sub(r"\[\d*\]","", new))
                    jaAdd=0
                    posb=i
    if linhasP[posb-1] != linhasP[-1]:
        linhassP.append(re.sub(r"\[\d*\]","", linhasP[posb-1]))
    linhasP= [linha for linha in linhassP]
    linhas = []
    linhas.extend(re.split("\"",linha) for linha in linhasP)
    autor = []
    titulo = []

    for linha in linhas:
        if len(linha)>1:
            titulo.append(linha[1])
            aux = []
            aux.extend(re.split("\,| and|et al.",linha[0]))
            autores=[]
            for aux2 in aux:
                if len(aux2) > 1:
                    autores.append(aux2)
            autor.append(autores)
        else:
            aux = []
            aux.extend(re.split("\,",linha[0]))
            if re.search(r"^ and (.*)", aux[0]) is not None:
                aux2 = []
                aux2.extend(re.split("and",aux[0]))
                autor.append(aux2)

                if re.search(r"^[Online]. Available: ", str(aux)):
                    aux[1] = re.sub(r"\[Online]. Available:","", str(aux[1]))
                    titulo.append(aux[1])
                else:
                    aux2 = []
                    i=1
                    if re.search("^ Eds", str(aux[i])):
                       i=i+1
                    aux2.extend(re.split("\.",aux[i]))
                    titulo.append(aux2[0])
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
                        
                        if re.search(r"\[Online]. Available: ", str(aux2)) is not None:
                            titulo.append([])
                        else:
                            auxT = []
                            if re.search("^ Eds.", aux2):
                                i=i+1
                            auxT.extend(re.split("\.",aux[i]))
                            titulo.append(auxT[0])
                        break
                    elif re.search(r"^ Eds.", aux2) is not None:
                        if re.search(r"\[Online]. Available: ", str(aux)) is not None:
                            titulo.append([])
                        else:
                            auxT = []
                            auxT.extend(re.split("\.",aux[i]))
                            titulo.append(auxT[0])
                        autor.append(aux3)
                        break
                        
                    if len(aux2) > 20:
                        aux[0]=re.sub(r"et al.","", aux[0])
                        aux3 = []
                        aux3.append(aux[0])
                        autor.append(aux3)

                        if re.search(r"^[Online]. Available: ", str(aux[1])) is not None:
                            titulo.append([])
                        else:
                            auxT = []
                            auxT.extend(re.split("\.",aux[1]))
                            titulo.append(auxT[0])
                        break
                    else:
                        aux3.append(aux2)
    return (autor, titulo)
        
def retiraAutorTitulo(texto):
    autorStopWords= ["IEEE", "Fellow", "Member", "Student", "Senior"]
    linhas= re.split("\n", text)
    publicado= ""
    if linhas[0].startswith("IEEE"):
        publicado= linhas[0].split(",")[0]
    else:
        publicado= linhas[2].split(",")[0]
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
            if parte.count("and ") == 0:
                autores.append(parte)
            elif parte.count(" and ") == 0:
                partes= parte.split("and ")
                for parcial in partes:
                    if len(parcial) > 1:
                        autores.append(parcial)
            else:
                partes= parte.split(" and ")
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
    return (autoresFinal, linhaTitulo, publicado)

def printaGrafos(grafo, vertices, edges, titulo, arquivo):
    layout2d= grafo.layout("fr")
    layout3d= grafo.layout("kk", dim= 3)
    Xn2= [layout2d[k][0] for k in range(len(vertices))]
    Yn2= [layout2d[k][1] for k in range(len(vertices))]
    Xe2= []
    Ye2= []
    for e in edges:
        Xe2+= [layout2d[e[0]][0], layout2d[e[1]][0], None]
        Ye2+= [layout2d[e[0]][1], layout2d[e[1]][1], None]

    Xn3= [layout3d[k][0] for k in range(len(vertices))]
    Yn3= [layout3d[k][1] for k in range(len(vertices))]
    Zn3= [layout3d[k][2] for k in range(len(vertices))]
    Xe3= []
    Ye3= []
    Ze3= []
    for e in edges:
        Xe3+= [layout3d[e[0]][0], layout3d[e[1]][0], None]
        Ye3+= [layout3d[e[0]][1], layout3d[e[1]][1], None]
        Ze3+= [layout3d[e[0]][2], layout3d[e[1]][2], None]
    
    trace13d= plotly.graph_objs.Scatter3d(x= Xe3, y= Ye3, z= Ze3, mode= "lines", line= dict(color= "rgb(125,125,125)", width= 1))
    trace23d= plotly.graph_objs.Scatter3d(x= Xn3, y= Yn3, z= Zn3, mode= "markers", name="Artigos", marker=dict(symbol='circle',
                             size=6,
                             color=[],
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=vertices,
               hoverinfo='text')

    trace12d= plotly.graph_objs.Scatter(x= Xe2, y= Ye2, mode= "lines", line= dict(color= "rgb(125,125,125)", width= 1))
    trace22d= plotly.graph_objs.Scatter(x= Xn2, y= Yn2, mode= "markers", name="Artigos", marker=dict(symbol='circle',
                             size=6,
                             color=[],
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=vertices,
               hoverinfo='text')

    axis = dict(showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')
    plotLayout2d= plotly.graph_objs.Layout(title=titulo,
                            width=1000, height=1000,
                            showlegend=False,
                            xaxis=dict(axis),
                            yaxis=dict(axis),
                            margin=dict(t=100),
                            hovermode='closest')

    axis = dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')
    plotLayout3d= plotly.graph_objs.Layout(title=titulo,
                                           width=1000, height=1000,
                                           showlegend=False,
                                           scene=dict(
                                               xaxis=dict(axis),
                                               yaxis=dict(axis),
                                               zaxis=dict(axis)),
                                           margin=dict(t=100),
                                           hovermode='closest')

    fig2d= plotly.graph_objs.Figure(data= [trace12d, trace22d], layout= plotLayout2d)
    fig3d= plotly.graph_objs.Figure(data= [trace13d, trace23d], layout= plotLayout3d)
    
    plotly.offline.plot(fig2d, filename= arquivo + ".html")
    plotly.offline.plot(fig3d, filename= arquivo + "3d.html")

def montaGrafos(referencias, frequencias):
    trabalhos= []
    autores= []
    autores2= []
    autoresRef= []
    citados= []
    publicacoes= []
    verticesAR1= []
    verticesP= []
    edgesP= []
    for referencia in referencias:
        if referencia[0][2] not in publicacoes:
            publicacoes.append(referencia[0][2])
            verticesP.append(referencia[0][2])
        if referencia[0][1].endswith("\r"):
            trabalhos.append(referencia[0][1][:-1])
            verticesP.append(referencia[0][1][:-1])
        else:
            trabalhos.append(referencia[0][1])
            verticesP.append(referencia[0][1])
        edgesP.append((verticesP.index(referencia[0][2]), len(verticesP) - 1))
        temp= []
        for autor in referencia[0][0]:
            autores.append(autor)
            autoresRef.append(autor)
        for autor in referencia[1][0]:
            autoresRef.append(autor)
            for a in autor:
                verticesAR1.append(a)
        for titulo in referencia[1][1]:
            if re.search(r"\[Online]", titulo):
                temp22= re.split(r"\[Online]", titulo)
                titulo = temp22[0]
            if titulo.endswith("\r") or titulo.endswith(",") or titulo.endswith(" ") or titulo.startswith(" "):
                aux= titulo
                while aux.endswith("\r") or aux.endswith(",") or aux.endswith(" "):
                    aux= aux[:-1]
                while aux.startswith(" "):
                    aux= aux[1:]
                temp.append(aux)
                verticesAR1.append(aux)
            else:
                temp.append(titulo)
                verticesAR1.append(titulo)
        citados.append(temp)

        temp= []
        for autoress in referencia[1][0]:
            if type(autoress) is list:
                for autor in autoress:
                    if autor.endswith(" "):
                        temp.append(autor[:-1])
                    elif autor.startswith(" "):
                        temp.append(autor[1:])
                    else:
                        temp.append(autor)
            else:
                if autoress.endswith(" "):
                    temp.append(autoress[:-1])
                elif autoress.startswith(" "):
                    temp.append(autoress[1:])
                else:
                    temp.append(autoress)
        autores2.append(temp)

    temp= []
    for grupo in autores2:
        if type(grupo) is list:
            for autor in grupo:
                temp.append(autor)
        else:
            temp.append(autor)
    verticesAL= []
    [verticesAL.append(x) for x in temp if x not in verticesAL]
    verticesAL.extend(trabalhos)
    
    temp= []
    for grupo in trabalhos:
        temp.append(grupo)
    for grupo in citados:
        for titulo in grupo:
            if re.search(r"\[Online]", titulo):
                temp22= re.split(r"\[Online]", titulo)
                titulo = temp22[0]
            if titulo.endswith("\r") or titulo.endswith(",") or titulo.endswith(" ") or titulo.startswith(" "):
                aux= titulo
                while aux.endswith("\r") or aux.endswith(",") or aux.endswith(" "):
                    aux= aux[:-1]
                while aux.startswith(" "):
                    aux= aux[1:]
                temp.append(aux)
            else:
                temp.append(titulo)
    verticesC= []
    [verticesC.append(x) for x in temp if x not in verticesC]
    verticesA= []
    verticesA.extend(autores)
    verticesA.extend(trabalhos)

    verticesAR= []
    [verticesAR.append(x) for x in verticesAR1 if x not in verticesAR]
    edgesAR= []

    verticesF= []
    edgesF= []
    for freq in frequencias:
        verticesF.append(freq[0])
        for palavra in freq[1]:
            if verticesF.count(palavra[0]) == 0:
                verticesF.append(palavra[0])
            edgesF.append((verticesF.index(freq[0]), verticesF.index(palavra[0])))
    
    grafoC= igraph.Graph()
    grafoC.add_vertices(len(verticesC))
    edgesC= []

    grafoA= igraph.Graph()
    grafoA.add_vertices(len(verticesA))
    edgesA= []

    grafoAR= igraph.Graph()
    grafoAR.add_vertices(len(verticesAR))

    grafoP= igraph.Graph()
    grafoP.add_vertices(len(verticesP))
    grafoP.add_edges(edgesP)

    grafoAL= igraph.Graph()
    grafoAL.add_vertices(len(verticesAL))
    edgesAL= []

    for referencia in referencias:
        for i in range(len(referencia[1][0])):
            nome= referencia[1][1][i]
            listaAutores= referencia[1][0][i]
            if re.search(r"\[Online]", nome):
                temp22= re.split(r"\[Online]", nome)
                nome = temp22[0]
            while nome.endswith("\r") or nome.endswith(",") or nome.endswith(" "):
                nome= nome[:-1]
            while nome.startswith(" "):
                nome= nome[1:]
            indice1= verticesAR.index(nome)
            for autor in listaAutores:
                indice2= verticesAR.index(autor)
                edgesAR.append((indice2, indice1))
    
    grafoF= igraph.Graph()
    grafoF.add_vertices(len(verticesF))
    grafoF.add_edges(edgesF)
    
    for trabalho in trabalhos:
        indice= trabalhos.index(trabalho)
        for autor in autores:
            if autor in referencias[indice][0][0]:
                indice1= verticesA.index(trabalho)
                indice2= verticesA.index(autor)
                edgesA.append((indice1, indice2))
        for citado in citados[indice]:
            indice1= verticesC.index(trabalho)
            indice2= verticesC.index(citado)
            edgesC.append((indice1, indice2))
        for autor in autores2[indice]:
            indice1= verticesAL.index(trabalho)
            indice2= verticesAL.index(autor)
            edgesAL.append((indice1, indice2))
    
    grafoA.add_edges(edgesA)
    grafoC.add_edges(edgesC)
    grafoAR.add_edges(edgesAR)
    grafoAL.add_edges(edgesAL)
    
    printaGrafos(grafoC, verticesC, edgesC, "Grafo das relações de citação entre os Artigos", "Citacoes")
    printaGrafos(grafoA, verticesA, edgesA, "Grafo das relações de autoria entre os Artigos", "Autoria")
    printaGrafos(grafoAR, verticesAR, edgesAR, "Grafo das relações de autoria entre os Artigos referenciados", "AutoriaRef")
    printaGrafos(grafoF, verticesF, edgesF, "Grafo dos termos mais frequentes em cada Artigo", "Frequentes")
    printaGrafos(grafoP, verticesP, edgesP, "Grafo das relações das publicação dos Artigos", "Publicacao")
    printaGrafos(grafoAL, verticesAL, edgesAL, "Grafo das relações de citação autoral entre os Artigos", "AutoriaAl")
    return

def retiraInstituicao(texto):
    novoTexto=""
    quebrado= texto.split("\n")
    flag= False
    inicio= 0
    fim= 0
    rodape= []
    instituicoes= []
    for i in range(1000):
        linha= quebrado[i]
        if not flag and not linha.startswith("Manuscript"):
            continue
        elif linha.startswith("Manuscript"):
            inicio= i
            flag= True
        elif flag and not linha.startswith("Digital Object"):
            rodape.append(linha)
            fim= i
        else:
            break
    novoTexto= texto[:inicio] + texto[fim+1:]
    if rodape[-1].startswith("Color"):
        rodape= rodape[:-1]
    if rodape[-1].startswith("This paper"):
        rodape= rodape[:-1]

    for linha in rodape:
        temp= linha.split(" with the ")
        #print(temp)
        #print(temp)
        quem= temp[0]
        if quem.endswith(" are"):
            quem= quem[:-4]
        elif quem.endswith(" is"):
            quem= quem[:-3]
        temp2= temp[1].split(" (")
        temp2= temp2[0]
        onde= temp2.split(" and")[0]
        if onde.endswith("\r") or onde.endswith(" ") or onde.endswith(","):
            onde= onde[:-1]
        instituicoes.append((quem, onde))
        

    return (novoTexto, instituicoes)


path= os.path.realpath(__file__)[:-12] + "Artigos\\"
pdfs= [arq for arq in glob.glob(path + "*.txt")]
artigos= []
artigosFull= []
referencias= []
count= 0
stopwords= corpus.stopwords.words('english')
referencias= []
frequencias=[]
for pdf in pdfs:
    #text = textract.process(pdf)
    text= []
    with open(pdf, "r") as arquivo:
        text= arquivo.read()
    #print(text) 
    (text, instituicoes)= retiraInstituicao(text)
    retiraAutorTitulo(text)
    preLinhas = re.split("REFERENCES",text)
    linhas= preLinhas[0].splitlines()
    temp1= retiraRef(preLinhas[1])
    temp2= retiraAutorTitulo(text)
    referencias.append((temp2, temp1))
    #continue
    #print(linhas)
    separadas= []
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
    artigosFull.append(atual)
    relevante= [x.lower() for x in atual if x not in stopwords and len(x) > 3 and x.isalpha()]
    artigos.append(relevante)
    frequencias.append((temp2[1], FreqDist(relevante).most_common(10)))
    #print(relevante)
    #break

#montaGrafos(referencias, frequencias)
tudoRelevante= [y for x in artigos for y in x]
tudo= [y for x in artigosFull for y in x]
frequenciaRelevante= FreqDist(tudoRelevante)
print(frequenciaRelevante.most_common(10))
