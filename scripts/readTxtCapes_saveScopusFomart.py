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

for cc, linha in enumerate(arquivo):
    
    if cc < 20:
    
        if readTile == False and linhaWhite == True:
            print("coletando titulo")            
            artigo['titulo'] = linha
            print('linha {} : {} '.format(cc, linha))
            readTile = True
            linhaWhite = False
        
        if readAutors == False:
            print('coletando autores')
            search1 = re.findall("[A-Z][a-z]+\s[;]\s[A-Z][a-z]+", linha) 
            search2 = re.findall("[^A-Z][a-z]+[,]\s[A-Z]", linha)
            search3 = re.findall("[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z]", linha)
            
            if len(search1) > 0 or len(search2) > 0 or len(search3) > 0:
                artigo['autor'] = linha
                print(linha)
                readAutors = True
        
        if readRef == False:
            
            seaRef1 = re.search("20[0-9][0-9]", linha) # padrão ano
            seaRef2 = re.search("19[0-9][0-9]", linha) # padrão ano
            seaRef3 = re.search("Vol.[0-9]*", linha) # padrão Volume do livro
            seaRef4 = re.search("pp\.[0-9]+", linha)  # padrão pagina do livro

            if ((seaRef1 != None or seaRef2 != None) and seaRef3 != None) or (
                (seaRef1 != None or seaRef2 != None) and seaRef4 != None):                
                artigo['referencia'] = linha
                print(linha)
                readRef = True
            
            # if :
            #     artigo['referencia'] = linha
            #     print(linha)
            #     readRef = True

        if readAbstract == False:

            seaRef1 = re.findall("[a-z]+\.\s[A-Z]", linha) # padrão fim de Oração e inicio da outra
            seaRef2 = re.findall("Directory of Open Access", linha) # PADRÃO FINAL DE PARRAFO
            seaRef3 = re.findall("Fundación Dialnet", linha) # PADRÃO FINAL DE PARRAFO
            seaRef4 = re.findall("SciELO SciELO", linha) # PADRÃO FINAL DE PARRAFO
            seaRef5 = re.findall("ProQuest", linha) # PADRÃO FINAL DE PARRAFO
            seaRef6 = re.findall("Cengage Learning", linha) # PADRÃO FINAL DE PARRAFO
            seaRef7 = re.findall("Palavras-chave", linha) # Padrão palavras chaves
            seaRef8 = re.findall("PALAVRAS-CHAVE", linha)  # Padrão palavras chaves          
            seaRef9 = re.findall("KEYWORDS", linha)  # Padrão palavras chaves

            if len(seaRef1) > 0 or len(seaRef2) > 0 or len(seaRef3) > 0 or len(seaRef4) > 0 or len(seaRef5) > 0 or len(seaRef6) > 0 or len(seaRef7) > 0 or len(seaRef8) > 0 or len(seaRef9) > 0:
                print(linha)
                artigo['abstract'] = linha
                readAbstract = True
        
        if len(linha) == 0 and linhaWhite == False:
            
            readTile = False
            readAutors = False
            readRef = False
            readAbstract = False

            dictArtigo['artivo' + str(contArt)] = artigo

            contArt += 1
            artigo = {}



print('INICIANDO A REIMPRIMIR O TEXTO ')
for keys, mdict in dictArtigo.items():

    print("############################################################################")
    print(keys)

    for kk, vv in mdict.items():

        print('==={} ===: {}'.format(kk, vv))