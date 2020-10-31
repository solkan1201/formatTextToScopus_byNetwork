from pandas import DataFrame
import pandas as pd  

import io 
import re

def codigoEnumerador(num):
    idCog = 0
    
    if num < 10:
        idCog = '000' + str(num)
    elif num < 100:
        idCog = '00' + str(num)
    elif num < 1000:
        idCog = '0' + str(num)
    else:
        idCog = str(num)

    return idCog

nomeArq = "tables/Authors.csv"
arquivo = open(nomeArq)

dictAutors = {}
allnameAuth = []
idAut ='auth'
contador = 0
lsedges = []


for cc, linha in enumerate(arquivo):
    if cc != 0:
        linha = linha[:-1]
        # print("analisando linha: \n", linha)
        # print("linha {} com {} caracteres".format(cc, len(linha)))
        linha = linha.split('"""')
        artg = str(linha[0]).replace(",","")
        if len(linha[1]) > 1:

            print(linha[1]) 
            lsAuthor = linha[1].split('|')

            lsCodtemp = []
            for ii, aut in enumerate(lsAuthor):
                
                if aut not in  allnameAuth:
                    allnameAuth.append(aut)
                    enumeCC = codigoEnumerador(contador)
                    contador += 1
                    enumeCC = idAut + enumeCC
                    dictAutors[enumeCC] = aut
                    lsCodtemp.append(enumeCC)
                
                else:
                    for kk, vv in dictAutors.items():
                        if aut == vv:
                            lsCodtemp.append(kk)
            
            if len(lsCodtemp) != 1:
                for ii in range(0, len(lsCodtemp) - 1):
                    for jj in range(ii + 1, len(lsCodtemp)):
                        lsedges.append([lsCodtemp[ii], lsCodtemp[jj], 'undirected', artg])
            
            else:
                lsedges.append([lsCodtemp[0], lsCodtemp[0], 'undirected', artg])

for edges in lsedges:
    print(edges)
print("terminou de convertir")
dfEdges = pd.DataFrame(lsedges, columns=['Source','Target','Type','Label'])
dfAuth = pd.DataFrame.from_dict(dictAutors, orient='index')

print("saving table of edges  📌")
#, columns=['indice', 'Source','Target','Type','Label']
dfEdges.to_csv("redes/networkCoAuthors.csv", index= True)
dfAuth.to_csv("tables/tableAuthorsCodificado.csv", index= True)  # columns=['codigo_auth', 'name_author']


