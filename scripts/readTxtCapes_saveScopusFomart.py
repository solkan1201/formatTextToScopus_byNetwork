import pandas as pd  
import io 
import re

#######################################################################
## dictArt = {
#      art_1 : {
#             titulo:  .....,
#             autor: ....,
#             referencia: ....,
#             abstract: .....
#        },
#      art_2 : {
#             titulo:  .....,
#             autor: ....,
#             referencia: ....,
#             abstract: .....
#        },
#      art_3 :
# }


nomeArq = 'Atual_Busca_Periodico_CAPES_Marcia.txt'
arquivo = open(nomeArq)

dictArtigo = {}
readTile =False
readAutors = False
readRef = False
readAbstract = False
linhaWhite = True
contArt = 0
artigo = {}
palaVChaves = ''
verificarleitura = False

if verificarleitura:
    for cc, linha in enumerate(arquivo):
        linha = linha[:-1]
        print("linha {} com {} caracteres".format(cc, len(linha)))
        print("analisando linha: \n", linha)

else:       
    for cc, linha in enumerate(arquivo):
        linha = linha[:-1]
        
        print("analisando linha: \n", linha)
        print("linha {} com {} caracteres".format(cc, len(linha)))
        if readTile == False and linhaWhite == True:
            #print("coletando titulo")            
            artigo['Title'] = '"' + str(linha) + '"'
            #print('linha {} : {} '.format(cc, linha))
            readTile = True
            linhaWhite = False
        
        elif readAutors == False:
            #print('coletando autores')
            search1 = re.findall("[A-Z][a-z]+\s[;]\s[A-Z][a-z]+", linha) 
            search2 = re.findall("[^A-Z][a-z]+[,]\s[A-Z]", linha)
            search3 = re.findall("[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+", linha)
            search4 = re.findall("Vol.[0-9]*", linha)
            print("verificando se leiu errado ", search4)
            
            if (len(search1) > 0 or len(search2) > 0 or len(search3) > 0) and (len(search4) == 0):
                autor = linha.replace(',', '_')
                autor = autor.replace('.', '-')
                autor = autor.replace(';', "|")
                artigo['Authors'] = '"' + str(autor) + '"'
                readAutors = True
            else:                
                search3 = re.findall("[A-Z][a-záô]+\s[A-Z][a-záô]+", linha)
                if len(search4) > 0:
                    artigo['Authors'] = '" "'
                    artigo['referencia'] = '"' + str(linha) + '"'
                    readAutors = True
                    readRef = True
                
                elif readTile == True and readRef == False and len(search3) > 0:
                    autor = linha.replace(',', '_')
                    autor = autor.replace('.', '-')
                    autor = autor.replace(';', "|")
                    artigo['Authors'] = '"' + str(autor) + '"'
                    readAutors = True

        elif readRef == False:
            
            print("lindo referencia ")
            seaRef1 = re.findall("20[0-9][0-9]", linha) # padrão ano
            seaRef2 = re.findall("19[0-9][0-9]", linha) # padrão ano
            seaRef3 = re.findall("Vol.[0-9]*", linha) # padrão Volume do livro
            seaRef4 = re.findall("pp\.[0-9]+", linha)  # padrão pagina do livro

            if ((len(seaRef1) > 0 or len(seaRef2) > 0) and len(seaRef3) > 0) or (
                (len(seaRef1) > 0 or len(seaRef2) > 0) and len(seaRef4) > 0):                
                artigo['referencia'] = '"' + str(linha) + '"'
                #print("referencia : ", linha)
                readRef = True

        elif readAbstract == False:

            cutRevKeyWord = False
            print("entro Abstract")
            seaRef1 = re.findall("[a-z]+\.\s[A-Z]", linha) # padrão fim de Oração e inicio da outra            
            # fontes 
            seaRef2 = re.findall("Directory of Open Access", linha) # PADRÃO FINAL DE PARRAFO
            seaRef3 = re.findall("Fundación Dialnet", linha) # PADRÃO FINAL DE PARRAFO
            seaRef4 = re.findall("SciELO SciELO", linha) # PADRÃO FINAL DE PARRAFO
            seaRef5 = re.findall("ProQuest", linha) # PADRÃO FINAL DE PARRAFO
            seaRef6 = re.findall("Cengage Learning", linha) # PADRÃO FINAL DE PARRAFO
            # encontrar palavras chaves !!
            seaRef7 = re.findall("Palavras-chave", linha) # Padrão palavras chaves
            seaRef8 = re.findall("PALAVRAS-CHAVE", linha)  # Padrão palavras chaves          
            seaRef9 = re.findall("KEYWORDS", linha)  # Padrão palavras chaves
            seaRef10 = re.findall("Palavras-chaves", linha)  # Padrão palavras chaves
            

            if len(seaRef1) > 0 or (readRef == True and (len(linha) > 150 or len(seaRef2)\
                or len(seaRef3) or len(seaRef4) or len(seaRef5) or len(seaRef6))):

                readAbstract = True

                if len(seaRef7) > 0:
                    divText = linha.split("Palavras-chave")
                    linha = str(divText[0]).strip()
                    palaVChaves = str(divText[1]).replace(".", " ").strip()
                    palaVChaves = palaVChaves.replace(":", " ")

                elif len(seaRef9) > 0:
                    divText = linha.split("KEYWORDS")
                    linha = str(divText[0]).strip()
                    palaVChaves = str(divText[1]).replace(".", " ").strip()
                    palaVChaves = palaVChaves.replace(":", " ")
                
                elif len(seaRef8) > 0:
                    divText = linha.split("PALAVRAS-CHAVE")
                    linha = str(divText[0]).strip()
                    palaVChaves = str(divText[1]).replace(".", " ").strip() 
                    palaVChaves = palaVChaves.replace(":", " ")               
                
                elif len(seaRef10) > 0:
                    divText = linha.split("Palavras-chaves")
                    linha = str(divText[0]).strip()
                    palaVChaves = str(divText[1]).replace(".", " ").strip()
                    palaVChaves = palaVChaves.replace(":", " ")

                else:
                    palaVChaves = ''

                if palaVChaves != '':                
                    cutRevKeyWord = True

                if len(seaRef2) > 0:
                    
                    if cutRevKeyWord:
                        nDivText = palaVChaves.split("Directory of Open Access")
                        palaVChaves = nDivText[0]
                        palaVChaves = " ".join(re.split("\s+", palaVChaves, flags= re.UNICODE))
                        palaVChaves = palaVChaves.strip()
                        artigo['Abstract'] = '"' + str(linha) + '"'
                        
                        artigo["Author Keywords"] = '"' + str(palaVChaves) + '"'                        
                    
                    else:
                        nDivText = linha.split("Directory of Open Access")
                        linha = nDivText[0]
                        artigo['Abstract'] = '"' + str(linha) + '"'                                               
                    
                    artigo['fonte'] = "Directory of Open Access"
                
                elif len(seaRef3) > 0:
                    
                    if cutRevKeyWord:
                        nDivText = palaVChaves.split("Fundación Dialnet")
                        palaVChaves = nDivText[0]
                        palaVChaves = " ".join(re.split("\s+", palaVChaves, flags= re.UNICODE))
                        palaVChaves = palaVChaves.strip()
                        artigo['Abstract'] = '"' + str(linha) + '"'
                        
                        artigo["Author Keywords"] = '"' + str(palaVChaves) + '"'                        
                    
                    else:
                        nDivText = linha.split("Fundación Dialnet")
                        linha = nDivText[0]
                        artigo['Abstract'] = '"' + str(linha) + '"'                                                
                    
                    artigo['fonte'] = '"Fundación Dialnet"'

                elif len(seaRef4) > 0:
                    
                    if cutRevKeyWord:
                        nDivText = palaVChaves.split("SciELO SciELO")
                        palaVChaves = nDivText[0]
                        palaVChaves = " ".join(re.split("\s+", palaVChaves, flags= re.UNICODE))
                        palaVChaves = palaVChaves.strip()
                        artigo['abstract'] = '"' + str(linha) + '"'
                        
                        artigo["Author Keywords"] = '"' + str(palaVChaves) + '"'                        
                    
                    else:
                        nDivText = linha.split("SciELO SciELO")
                        linha = nDivText[0]
                        artigo['Abstract'] = '"' + str(linha) + '"'                        
                    
                    artigo['fonte'] = '"SciELO SciELO"'

                elif len(seaRef5) > 0:
                    
                    if cutRevKeyWord:
                        nDivText = palaVChaves.split("ProQuest")
                        palaVChaves = nDivText[0]
                        palaVChaves = " ".join(re.split("\s+", palaVChaves, flags= re.UNICODE))
                        palaVChaves = palaVChaves.strip()
                        artigo['Abstract'] = '"' + str(linha) + '"'
                        
                        artigo["Author Keywords"] = '"' + str(palaVChaves) + '"'                        
                    
                    else:
                        nDivText = linha.split("ProQuest")
                        linha = nDivText[0]
                        artigo['Abstract'] = '"' + str(linha) + '"'                                                
                    
                    artigo['fonte'] = '"ProQuest"'

                elif len(seaRef6) > 0:
                    
                    if cutRevKeyWord:
                        nDivText = palaVChaves.split("Cengage Learning")
                        palaVChaves = nDivText[0]
                        palaVChaves = " ".join(re.split("\s+", palaVChaves, flags= re.UNICODE))
                        palaVChaves = palaVChaves.strip()
                        artigo['Abstract'] = '"' + str(linha) + '"'
                        
                        artigo["Author Keywords"] = '"' + str(palaVChaves) + '"'                        
                    
                    else:
                        nDivText = linha.split("Cengage Learning")
                        linha = nDivText[0]
                        artigo['Abstract'] = '"' + str(linha) + '"'                                               
                    
                    artigo['fonte'] = '"Cengage Learning"'  
                
                else:
                    artigo['Abstract'] = '"' + str(linha) + '"'      

        
        elif len(linha) < 1 and linhaWhite == False:
            #print("entrou a linha branca")
            readTile = False
            readAutors = False
            readRef = False
            readAbstract = False
            linhaWhite = True
            print("===== Salvando o diccionario ===")
            dictArtigo['artivo' + str(contArt)] = artigo

            contArt += 1
            artigo = {}
    
    # Verificando  que o ultimo artigo tenha informação     
    if bool(arquivo) == True: 
        dictArtigo['artivo' + str(contArt)] = artigo

    print('INICIANDO A REIMPRIMIR O TEXTO ')
    for keys, mdict in dictArtigo.items():

        print("############################################################################")
        print(keys)

        for kk, vv in mdict.items():

            print('=== {} ===: {}'.format(kk.upper(), vv))


    ################ convertendo os resultados para Dataframe #############################3
    dfArt = pd.DataFrame.from_dict(dictArtigo, orient='index')  #

    print(dfArt.head())
    print("colunas do Dataframe:  ", dfArt.columns)
    dfArt.to_csv("tables/lsArtigoFormatadov2.csv")
    dfArt['Authors'].to_csv("tables/Authors.csv")
    dfArt[['Title','Authors']].to_csv("tables/tableTileAuthos.csv")

