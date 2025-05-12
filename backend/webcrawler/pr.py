import re
import requests
from bs4 import BeautifulSoup as bs
import sys
import json
import time
from urllib.error import HTTPError
from urllib.parse import urlparse
from nltk.stem import PorterStemmer
from nltk.tokenize import  word_tokenize
from unidecode import unidecode

paginas=[]
link = "https://es.wikipedia.org/wiki/%C3%81lex_Cabrera"
def quitar_tildes_especifico(cadena):
    # Diccionario de mapeo de tildes para la "ñ"
    tildes_enye = {'á': 'a','Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u'}
    
    # Reemplazar tildes para la "ñ" en la cadena
    for tilde, sin_tilde in tildes_enye.items():
        cadena = cadena.replace(tilde, sin_tilde)

    return cadena
def webCrawler(url,n,lista_vistos):
    data={}
    website = url
    dominio_deseado ="es.wikipedia.org"
    parsed_url = urlparse(website)
    
    
    if dominio_deseado == parsed_url.netloc and requests.head(website).status_code==200:
        
        resultado=requests.get(website)
        data['url']=website
        data['mainTitle']=""
        data["tag"]="h1"
        data["titulos"]=[]
        data["images"]=[]
        data["texto"]=[]
        data["referencias"]=""
        
        stemmer = PorterStemmer()
        soup = bs(resultado.text,'html.parser')
        mainT=soup.find('h1').text
        patron = patron = re.compile(r'[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]')
        descripcion=patron.sub('',mainT)
        descripcion=quitar_tildes_especifico(descripcion)
        palabras= word_tokenize(descripcion)
        wordsT=[]
        for p in palabras:
            wordsT.append({
            p:stemmer.stem(p)
            })  
        data['mainTitle']={"string":quitar_tildes_especifico(mainT),"text":wordsT}
        main= soup.find_all('div',id='mw-content-text')
        
        figuras = main[0].find_all('figure')

        imagenes_descrip = []
        urls_procesadas = set()

        for figura in figuras:
            img = figura.find('img')
            figcaption = figura.find('figcaption')

            if img:
                imagen_src = img['src']

                # Verificar si la URL ya ha sido procesada
                if imagen_src not in urls_procesadas:
                    descripcion = figcaption.text if figcaption else ''
                    descripcion = patron.sub('', descripcion)
                    descripcion=quitar_tildes_especifico(descripcion)
                    palabras = word_tokenize(descripcion)
                    wordsT = []
                    for p in palabras:
                        if p=="":
                            p="-"
                        else:
                            p=p.lower()
                        wordsT.append({
                            p: stemmer.stem(p)
                        })
                    imagenes_descrip.append({
                        "url": imagen_src,
                        "tag": "img",
                        "text": wordsT
                    })

                    
                    urls_procesadas.add(imagen_src)
        imagenes_sin_figura = main[0].find_all('img', {'src': True, 'alt': False})
        
        for img in imagenes_sin_figura:
            imagen_src = img['src']

            
            if imagen_src not in urls_procesadas:
                imagenes_descrip.append({
                    "url": imagen_src,
                    "tag": "img",
                    "text": '-'
                })

                
                urls_procesadas.add(imagen_src)

        data['images'] = imagenes_descrip
        parrafosH1=[]
        Siguiente_h1 = main[0].find_next()
    
        while Siguiente_h1 and Siguiente_h1.name != 'h2'  and Siguiente_h1.name != 'h3':
            if Siguiente_h1.name == 'p':
                descripcion = Siguiente_h1.text
                descripcion=patron.sub('',descripcion)
                descripcion=quitar_tildes_especifico(descripcion)
                palabras= word_tokenize(descripcion)
                wordsT=[]
                for p in palabras:
                    if p=="":
                        p="-"
                    else:
                        p=p.lower()
                    wordsT.append({
                        p:stemmer.stem(p)
                    })
                if wordsT ==[]:
                    wordsT="-"
                parrafosH1.append({
                    "text":wordsT,
                    "tag":'p'
                })
                
            elif Siguiente_h1.name == 'table':
                texto_tabla = Siguiente_h1.find_all('td') + Siguiente_h1.find_all('th')
                for text in texto_tabla:
                    if text.text!="" and text.text !="\n":
                        valort=''
                        if text.name=='td':
                            valort='td'
                        elif text.name=='th':
                            valort='th'
                        descripcion = text.text
                        descripcion=patron.sub('',descripcion)
                        descripcion=quitar_tildes_especifico(descripcion)
                        palabras= word_tokenize(descripcion)
                        wordsT=[]
                        for p in palabras:
                            if p=="":
                                p="-"
                            else:
                                p=p.lower()
                            wordsT.append({
                                p:stemmer.stem(p)
                            })
                        if wordsT ==[]:
                            wordsT="-"
                        parrafosH1.append({
                            "text":wordsT,
                            "tag":valort
                        })
            elif Siguiente_h1.name == 'li':
                descripcion = Siguiente_h1.text
                descripcion=patron.sub('',descripcion)
                descripcion=quitar_tildes_especifico(descripcion)
                palabras= word_tokenize(descripcion)
                wordsT=[]
                for p in palabras:
                    if p=="":
                        p="-"
                    else:
                        p=p.lower()
                    wordsT.append({
                        p:stemmer.stem(p)
                    })
                if wordsT ==[]:
                    wordsT="-"
                parrafosH1.append({
                    "text":wordsT,
                    "tag":'li'
                })
            Siguiente_h1=Siguiente_h1.find_next()
        data['texto']=parrafosH1

        subtitulos = main[0].find_all('h2')
        secTitulos =[]

        for sub in subtitulos:
            
            if sub.find("span",class_="mw-headline")==None:
                sectitulo=sub.text
                sectitulo=patron.sub('',sectitulo)
                sectitulo=quitar_tildes_especifico(sectitulo)
            else:
               sectitulo= sub.find("span",class_="mw-headline").text
               sectitulo=patron.sub('',sectitulo)
               sectitulo=quitar_tildes_especifico(sectitulo)
            parrafos_h2 =[]
            subtituP=[]
            Siguiente_h2 = sub.find_next()
            
            if sectitulo != "Enlaces externos":
                while Siguiente_h2 and Siguiente_h2.name != 'h2':
                    if Siguiente_h2.name == 'p':
                        descripcion = Siguiente_h2.text
                        
                        descripcion=patron.sub('',descripcion)
                        descripcion=quitar_tildes_especifico(descripcion)
                        
                        palabras= word_tokenize(descripcion)
                        
                        wordsT=[]
                        for p in palabras:
                            if p=="":
                                p="-"
                            else:
                                p=p.lower()
                            wordsT.append({
                                p:stemmer.stem(p)
                            })
                        if wordsT ==[]:
                            wordsT="-"    
                        parrafos_h2.append({
                            "text":wordsT,
                            "tag":'p'
                        })
                        
                        Siguiente_h2=Siguiente_h2.find_next()  
                    elif Siguiente_h2.name == 'table':
                        
                        texto_tabla = Siguiente_h2.find_all('td') + Siguiente_h2.find_all('th')
                        
                        for text in texto_tabla:
                            
                            if text.text!="" and text.text !="\n":
                                valort=''
                                if text.name=='td':
                                    valort='td'
                                elif text.name=='th':
                                    valort='th'
                                descripcion = text.text
                                


                                descripcion=patron.sub('',descripcion)
                                descripcion=quitar_tildes_especifico(descripcion)

                                palabras= word_tokenize(descripcion)

                                wordsT=[]
                                for p in palabras:
                                    if p=="":
                                        p="-"
                                    else:
                                        p=p.lower()
                                    wordsT.append({
                                        p:stemmer.stem(p)
                                    })
                                if wordsT ==[]:
                                    wordsT="-"
                                parrafos_h2.append({
                                    "text":wordsT,
                                    "tag":valort
                                })
                                
                                
                        Siguiente_h2=Siguiente_h2.find_next()
                    
                    elif Siguiente_h2.name == 'li' :
                        
                        descripcion = Siguiente_h2.text
                        
                        descripcion=patron.sub('',descripcion)
                        descripcion=quitar_tildes_especifico(descripcion)

                        palabras= word_tokenize(descripcion)
                        wordsT=[]
                        for p in palabras:
                            if p=="":
                                p="-"
                            else:
                                p=p.lower()
                            wordsT.append({
                                p:stemmer.stem(p)
                            })
                        if wordsT ==[]:
                            wordsT="-"
                        parrafos_h2.append({
                            "text":wordsT,
                            "tag":'li'
                        })
                        Siguiente_h2=Siguiente_h2.find_next()  
                    elif Siguiente_h2.name == 'h3':
                        if Siguiente_h2.find("span",class_="mw-headline")==None:
                            tertitulo=Siguiente_h2.text
                            tertitulo=patron.sub('',tertitulo)
                            tertitulo=quitar_tildes_especifico(tertitulo)
                        else:
                            tertitulo = Siguiente_h2.find("span",class_="mw-headline").text
                            tertitulo=patron.sub('',tertitulo)
                            tertitulo=quitar_tildes_especifico(tertitulo)
                        
                        parrafos_h3 =[]
                        Siguiente_h3 = Siguiente_h2.find_next()
                        while Siguiente_h3:
                            
                            if Siguiente_h3.name == 'p':
                                descripcion = Siguiente_h3.text
                                descripcion=patron.sub('',descripcion)
                                descripcion=quitar_tildes_especifico(descripcion)
                                palabras= word_tokenize(descripcion)
                                wordsT=[]
                                for p in palabras:
                                    if p=="":
                                        p="-"
                                    else:
                                        p=p.lower()
                                    wordsT.append({
                                        p:stemmer.stem(p)
                                    })
                                if wordsT==[]:
                                    wordsT="-"
                                parrafos_h3.append({
                                    "text":wordsT,
                                    "tag":'p'
                                })    
                            elif Siguiente_h3.name == 'table':
                                texto_tabla = Siguiente_h3.find_all('td') + Siguiente_h3.find_all('th')
                                for text in texto_tabla:
                                    if text.text!="" and text.text !="\n":
                                        valort=''
                                        if text.name=='td':
                                            valort='td'
                                        elif text.name=='th':
                                            valort='th'
                                        descripcion = text.text
                                        descripcion=patron.sub('',descripcion)
                                        descripcion=quitar_tildes_especifico(descripcion)
                                        palabras= word_tokenize(descripcion)
                                        wordsT=[]
                                        for p in palabras:
                                            if p=="":
                                                p="-"
                                            else:
                                                p=p.lower()
                                            wordsT.append({
                                                p:stemmer.stem(p)
                                            })
                                        if wordsT==[]:
                                            wordsT="-"
                                        parrafos_h3.append({
                                            "text":wordsT,
                                            "tag":valort
                                        })
                            elif Siguiente_h3.name == 'li':
                                descripcion = Siguiente_h3.text
                                descripcion=patron.sub('',descripcion)
                                descripcion=quitar_tildes_especifico(descripcion)
                                palabras= word_tokenize(descripcion)
                                wordsT=[]
                                for p in palabras:
                                    if p=="":
                                        p="-"
                                    else:
                                        p=p.lower()
                                    wordsT.append({
                                        p:stemmer.stem(p)
                                    })
                                parrafos_h3.append({
                                    "text":wordsT,
                                    "tag":'li'
                                })
                                
                            elif Siguiente_h3.name == "h3":
                                descripcion = tertitulo
                                descripcion=patron.sub('',descripcion)
                                descripcion=quitar_tildes_especifico(descripcion)
                                
                                palabras= word_tokenize(descripcion)
                                wordsT=[]
                                for p in palabras:
                                    if p=="":
                                        p="-"
                                    else:
                                        p=p.lower()
                                    wordsT.append({
                                        p:stemmer.stem(p)
                                    })
                                if wordsT ==[]:
                                    wordsT="-"
                                    if parrafos_h3==[]:
                                        parrafos_h3='-'
                                subtituP.append({
                                    "subtitulo": {"string":tertitulo,"text":wordsT},
                                    "tag":"h3",
                                    "text":parrafos_h3
                                })
                                tertitulo = Siguiente_h3.text
                                parrafos_h3 =[]
                                
                                
                            elif Siguiente_h3.name == "h2":
                                descripcion = tertitulo
                                descripcion=patron.sub('',descripcion)
                                descripcion=quitar_tildes_especifico(descripcion)
                                
                                palabras= word_tokenize(descripcion)
                                wordsT=[]
                                for p in palabras:
                                    if p=="":
                                        p="-"
                                    else:
                                        p=p.lower()
                                    wordsT.append({
                                        p:stemmer.stem(p)
                                    })
                                if wordsT ==[]:
                                    wordsT="-"
                                    if parrafos_h3==[]:
                                        parrafos_h3='-'
                                subtituP.append({
                                    "subtitulo": {"string":tertitulo,"text":wordsT},
                                    "tag":"h3",
                                    "text":parrafos_h3
                                })
                                Siguiente_h2 = Siguiente_h3
                                break
                            
                            Siguiente_h3 = Siguiente_h3.find_next()
                            
                            if Siguiente_h3==None:
                                descripcion = tertitulo
                                descripcion=patron.sub('',descripcion)
                                descripcion=quitar_tildes_especifico(descripcion)
                                
                                palabras= word_tokenize(descripcion)
                                wordsT=[]
                                for p in palabras:
                                    if p=="":
                                        p="-"
                                    else:
                                        p=p.lower()
                                    wordsT.append({
                                        p:stemmer.stem(p)
                                    })
                                if wordsT ==[]:
                                    wordsT="-"
                                    if parrafos_h3==[]:
                                        parrafos_h3='-'
                                subtituP.append({
                                    "subtitulo": {"string":tertitulo,"text":wordsT},
                                    "tag":"h3",
                                    "text":parrafos_h3
                                })
                                
                                Siguiente_h2=Siguiente_h3   
                    else:
                        Siguiente_h2=Siguiente_h2.find_next()    
                descripcion = sectitulo
                descripcion=patron.sub('',descripcion)
                descripcion=quitar_tildes_especifico(descripcion)

                palabras= word_tokenize(descripcion)
                wordsT=[]
                for p in palabras:
                    if p=="":
                        p="-"
                    else:
                        p=p.lower()
                    wordsT.append({
                    p:stemmer.stem(p)
                    })
                if wordsT ==[]:
                    wordsT="-"
                    if parrafos_h2==[]:
                        parrafos_h2='-'
                secTitulos.append({
                    "titulo": {"string":sectitulo,"text":wordsT},
                    "tag":"h2",
                    "text":parrafos_h2,
                    "subtitulos":subtituP
                })
        data["titulos"]=secTitulos
        referencias = main[0].find('div',class_='listaref')
        
        if referencias!=None:
            lis = referencias.find_all('li')
            references = []
            uses =[]
            
            citas= soup.find_all('sup',class_='reference separada')
            
            i =0
            for li in lis:
                
                i=1+i
                
                citacompleta=li.find('span',class_='reference-text')
                
                if citacompleta == None:
                    if li.find('a')==None:
                        url=li.text
                    else:
                        url=li.find('a')['href']

                elif citacompleta.find('a') ==None and citacompleta.find('href') == None:
                    url="-"
                else:
                    if citacompleta.find('a').get("href","")=="":
                        url='-'
                    else:
                        url=citacompleta.find('a')['href']
                if citacompleta == None:
                    ferenceAccess= li
                elif citacompleta.find('span') == None:
                    ferenceAccess=citacompleta
                else:
                    ferenceAccess=citacompleta.find('span')
                references.append({
                    "url":url,
                    "text":ferenceAccess.text
                })
            p1=re.compile(r'#')
            for ci in citas:
                
                if ci.find('a') ==None: 
                    uses.append({"id":"-"})
                else:    
                    uses.append({"id":p1.sub('',ci.find('a')["href"])})
            
            data["referencias"]={"tag":'h1',"references":references,"uses":uses}
            
            paginas.append({
                "Pagina":data
            })
            
        else:
            data["referencias"]=""
            
            paginas.append({
                "Pagina":data
            })
       
        
        """if n >0:
               
            redirreciones = main[0].find_all('a')
            lista_enlaces=[] 
            patron_wiki = re.compile(r'^/wiki/')
            for links in redirreciones:
                if lista_enlaces not in redirreciones:
                    if links.get("href","")!="":
                        lista_enlaces.append(links["href"])
            enlaces_filtrados = [enlace for enlace in lista_enlaces if patron_wiki.search(enlace)]
            
            for visto in enlaces_filtrados:
                
                if visto in lista_vistos:
                    enlaces_filtrados.remove(visto)
                else:
                    lista_vistos.append(visto)
            
            parte1_enlace="https://es.wikipedia.org"
            for enlace in enlaces_filtrados:
                peso = len(json.dumps(paginas).encode('utf-8'))
                peso_kb = peso / 1024
                peso_mb = peso_kb / 1024
                print(peso_mb)
                if peso_mb<=260:
                    webCrawler(parte1_enlace+enlace,n-1,lista_vistos)
                else:
                    break"""
            
    else:
        print('sirve')
    
    
webCrawler(link,2,[])

with open('data.json', 'w',encoding='utf-8') as file:
            json.dump(paginas, file,ensure_ascii=False)










    

