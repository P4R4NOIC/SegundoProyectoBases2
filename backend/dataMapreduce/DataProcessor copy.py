import mysql.connector as mariadb
import time
# decodigo.com
mariadb_conexion = mariadb.connect(host='localhost', port='3307',
                                   user='root', password='gabo1', database='wordsPages')
cursor = mariadb_conexion.cursor()


def dataMR1():
    fichero=open('./dataMapreduce/outputMR1.txt', 'r')
    lineas = fichero.readlines()
    mariadb_conexion.start_transaction()
    try:
        for linea in lineas:
            
            if linea[0] == 'ÿ' and linea[1]=='þ':
                linea=linea.replace('ÿ',  '', 1)
                linea=linea.replace('þ',  '', 1)
        
            newline = linea.replace('\t', '').replace('"','').replace('\x00', '').replace('\n', '').replace('null','')
            
            
            elementos = newline.split("','")
            
            
            elementos = [elemento.replace("'",'') for elemento in elementos if elemento]
            
            if elementos!=[]:
                cursor.execute("INSERT INTO pagina (link, can_titulos, titulo_principal) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE can_titulos = VALUES(can_titulos), titulo_principal = VALUES(titulo_principal)", (elementos[0], elementos[2], elementos[1]))

            
        mariadb_conexion.commit()
    except Exception as e:
        
        print(f"Error: {e}")
        mariadb_conexion.rollback()    

def dataMR2():
    fichero=open('./dataMapreduce/outputMR2.txt', 'r')
    lineas = fichero.readlines()
    mariadb_conexion.start_transaction()
    try:
        for linea in lineas:
        
            if linea[0] == 'ÿ' and linea[1]=='þ':
                linea=linea.replace('ÿ',  '', 1)
                linea=linea.replace('þ',  '', 1)
        
            newline = linea.replace('\t', '').replace('"','').replace('\x00', '').replace('\n', '').replace('null','')
            
            
            elementos = newline.split("','")
           
            
            elementos = [elemento.replace("'",'') for elemento in elementos if elemento]
            
            if elementos!=[]:
                if elementos[0] == 'Pagina':
                    cursor.execute('select * from pagina where pagina.link=%s',(elementos[1],))
                    resultado=cursor.fetchone()
                else:
                    cursor.execute('select * from pagina where pagina.link=%s',(elementos[0],))
                    resultado=cursor.fetchone()
                
                if resultado is not None:
                    print(elementos)
                    if elementos[0]=='pagina':
                        update_query = 'UPDATE pagina SET can_palabras=%s WHERE link=%s'
                        cursor.execute(update_query,(elementos[3],elementos[1]))       
                    elif elementos[1]=='subtitulo':
                        print('x')
                        if len(elementos)==3:
                            cursor.execute("INSERT INTO subtitulos (link_pagina,nombre_subtitulo,cantidad_palabras) VALUES (%s,%s,%s)", (elementos[0],'Numero solo',elementos[2]))
                        else:
                            cursor.execute("INSERT INTO subtitulos (link_pagina,nombre_subtitulo,cantidad_palabras) VALUES (%s,%s,%s)", (elementos[0],elementos[2],elementos[3]))
                    elif elementos[1]=='titulo':
                        if len(elementos)==3:
                            cursor.execute("INSERT INTO subtitulos (link_pagina,nombre_subtitulo,cantidad_palabras) VALUES (%s,%s,%s)", (elementos[0],'Numero solo',elementos[2]))
                        else:
                            cursor.execute("INSERT INTO titulos (link_pagina,nombre_titulo,cantidad_palabras) VALUES (%s,%s,%s)", (elementos[0],elementos[2],elementos[3]))
                    
        mariadb_conexion.commit()
    except Exception as e:
        
        print(f"Error: {e}")
        mariadb_conexion.rollback() 
"""'with open('./dataMapreduce/outputMR4.txt', 'w') as f:
    f.writelines(contenido)""" 
def dataMR3():
    fichero=open('./dataMapreduce/outputMR3.txt', 'r')
    lineas = fichero.readlines()
    mariadb_conexion.start_transaction()
    try:
        for linea in lineas:
        
            if linea[0] == 'ÿ' and linea[1]=='þ':
                linea=linea.replace('ÿ',  '', 1)
                linea=linea.replace('þ',  '', 1)
        
            newline = linea.replace('\t', '').replace('"','').replace('\x00', '').replace('\n', '').replace('null','')
            
            
            elementos = newline.split("','")
           
            
            elementos = [elemento.replace("'",'') for elemento in elementos if elemento]
            print(elementos)
            if elementos!=[]:
                cursor.execute('select * from pagina where pagina.link=%s',(elementos[0],))
                resultado=cursor.fetchone()
                if resultado is not None:
                    if elementos[1]=='active':
                        update_query = 'UPDATE pagina SET can_referencias=%s WHERE link=%s'
                        cursor.execute(update_query,(elementos[2],elementos[0]))       
                    elif elementos[3]=='active':
                        cursor.execute("INSERT INTO referencias (link_pagina,id_cita,link,activo) VALUES (%s,%s,%s,%s)", (elementos[0],elementos[2],elementos[1],True))
                    elif elementos[3]=='inactive':
                        cursor.execute("INSERT INTO referencias (link_pagina,id_cita,link,activo) VALUES (%s,%s,%s,%s)", (elementos[0],elementos[2],elementos[1],False))
        mariadb_conexion.commit()
    except Exception as e:
        
        print(f"Error: {e}")
        mariadb_conexion.rollback() 
def dataMR4():
    fichero=open('./dataMapreduce/outputMR4.txt', 'r')
    lineas = fichero.readlines()
    mariadb_conexion.start_transaction()
    try:
        for linea in lineas:
        
            if linea[0] == 'ÿ' and linea[1]=='þ':
                linea=linea.replace('ÿ',  '', 1)
                linea=linea.replace('þ',  '', 1)
        
            newline = linea.replace('\t', '').replace('"','').replace('\x00', '').replace('\n', '').replace('null','')
            
            
            elementos = newline.split("','")
           
            
            elementos = [elemento.replace("'",'') for elemento in elementos if elemento]
            
            if elementos!=[]:
                update_query = 'UPDATE referencias SET nombre_cita=%s,usos=%s  WHERE link_pagina=%s AND id_cita=%s'
                cursor.execute(update_query,(elementos[1],elementos[3],elementos[0],elementos[2]))
        mariadb_conexion.commit()
    except Exception as e:
        
        print(f"Error: {e}")
        mariadb_conexion.rollback() 
def dataMR5():
    fichero=open('./dataMapreduce/outputMR5.txt', 'r')
    lineas = fichero.readlines()
    mariadb_conexion.start_transaction()
    try:
        for linea in lineas:
        
            if linea[0] == 'ÿ' and linea[1]=='þ':
                linea=linea.replace('ÿ',  '', 1)
                linea=linea.replace('þ',  '', 1)
        
            newline = linea.replace('\t', '').replace('"','').replace('\x00', '').replace('\n', '').replace('null','')
            
            
            elementos = newline.split("','")
           
            
            elementos = [elemento.replace("'",'') for elemento in elementos if elemento]
           
            if elementos!=[]:
                cursor.execute('select * from pagina where pagina.link=%s',(elementos[0],))
                resultado=cursor.fetchone()
                if resultado is not None:
                    if elementos[1]=='pagina':
                        update_query = 'UPDATE pagina SET can_imagenes=%s  WHERE link=%s'
                        cursor.execute(update_query,(elementos[2],elementos[0]))
                    else:
                        update_query = 'UPDATE pagina SET can_palabrasximagenes=%s  WHERE link=%s'
                        cursor.execute(update_query,(elementos[1],elementos[0]))
        mariadb_conexion.commit()
    except Exception as e:
        
        print(f"Error: {e}")
        mariadb_conexion.rollback() 
def dataMR6():
    fichero=open('./dataMapreduce/outputMR6.txt', 'r')
    lineas = fichero.readlines()
    mariadb_conexion.start_transaction()
    try:
        for linea in lineas:
        
            if linea[0] == 'ÿ' and linea[1]=='þ':
                linea=linea.replace('ÿ',  '', 1)
                linea=linea.replace('þ',  '', 1)
        
            newline = linea.replace('\t', '').replace('"','').replace('\x00', '').replace('\n', '').replace('null','')
            
            
            elementos = newline.split("','")
           
            
            elementos = [elemento.replace("'",'') for elemento in elementos if elemento]
            
            
            if elementos!=[]:
                if elementos[0]=='titulo':
                    cursor.execute('select * from pagina where pagina.link=%s',(elementos[1],))
                    resultado=cursor.fetchone()
                    if resultado is not None:
                        cursor.execute("UPDATE PalabrasMasComunes SET enTitulo=%s  WHERE link_pagina=%s AND palabra=%s", (True,elementos[1],elementos[3]))
                elif elementos[0]=='pagina':
                    cursor.execute('select * from pagina where pagina.link=%s',(elementos[1],))
                    resultado=cursor.fetchone()
                    if resultado is not None:
                        cursor.execute("INSERT INTO PalabrasMasComunes (link_pagina,palabra,veces,entitulo) VALUES (%s,%s,%s,%s)", (elementos[1],elementos[3],elementos[4],False))
        mariadb_conexion.commit()
    except Exception as e:
        
        print(f"Error: {e}")
        mariadb_conexion.rollback() 
def dataMR7():
    fichero=open('./dataMapreduce/outputMR7.txt', 'r')
    lineas = fichero.readlines()
    try:
        palabra_actual=""
        for linea in lineas:
        
            if linea[0] == 'ÿ' and linea[1]=='þ':
                linea=linea.replace('ÿ',  '', 1)
                linea=linea.replace('þ',  '', 1)
        
            newline = linea.replace('\t', '').replace('"','').replace('\x00', '').replace('\n', '').replace('null','')
            
            
            elementos = newline.split("','")
           
            
            elementos = [elemento.replace("'",'') for elemento in elementos if elemento]
            
            
            if elementos!=[]:
                cursor.execute('select * from pagina where pagina.link=%s',(elementos[1],))
                resultado=cursor.fetchone()
                if resultado is not None:
                    cursor.execute('select * from Palabra where Palabra.palabra=%s',(elementos[0],))
                    re_p=cursor.fetchone()
                    if re_p is None:
                        
                        cursor.execute("INSERT INTO Palabra (palabra)VALUES(%s)",(elementos[0],))
                        mariadb_conexion.commit()
                        ultimo_id = cursor.lastrowid
                        cursor.execute("INSERT INTO PalabrasXPaginas (id_palabra, link_pagina, veces) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE veces = VALUES(veces)", (ultimo_id, elementos[1], elementos[2]))
                        mariadb_conexion.commit()
                    else:
                        cursor.execute("INSERT INTO PalabrasXPaginas (id_palabra, link_pagina, veces) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE veces = VALUES(veces)", (ultimo_id, elementos[1], elementos[2]))
                        mariadb_conexion.commit()
                        

                        
        
    except Exception as e:
        
        print(f"Error: {e}")
        mariadb_conexion.rollback() 
def dataMR8():
    fichero=open('./dataMapreduce/outputMR8.txt', 'r')
    lineas = fichero.readlines()
    
    try:
        for linea in lineas:
        
            if linea[0] == 'ÿ' and linea[1]=='þ':
                linea=linea.replace('ÿ',  '', 1)
                linea=linea.replace('þ',  '', 1)
        
            newline = linea.replace('\t', '').replace('"','').replace('\x00', '').replace('\n', '').replace('null','')
            
            
            elementos = newline.split("','")
           
            
            elementos = [elemento.replace("'",'') for elemento in elementos if elemento]
            print(elementos)
            if elementos!=[]:
                if len(elementos)==3:
                    cursor.execute('select * from pagina where pagina.link=%s',(elementos[0],))
                    resultado=cursor.fetchone()
                    if resultado is not None:
                        
                        cursor.execute("SELECT id FROM Palabra where palabra=%s",(elementos[1],))
                        id=cursor.fetchall()
                        if id is not None:
                            id=id[0][0]
                            update_query = 'UPDATE PalabrasXPaginas SET porcentaje=%s  WHERE link_pagina=%s AND id_palabra = %s'
                            cursor.execute(update_query,(elementos[2],elementos[0],id))
                            mariadb_conexion.commit()
    except Exception as e:
        
        print(f"Error: {e}")
        mariadb_conexion.rollback() 

def dataMR9():
    fichero=open('./dataMapreduce/outputMR9.txt', 'r')
    lineas = fichero.readlines()
    mariadb_conexion.start_transaction()
    try:
        for linea in lineas:
        
            if linea[0] == 'ÿ' and linea[1]=='þ':
                linea=linea.replace('ÿ',  '', 1)
                linea=linea.replace('þ',  '', 1)
        
            newline = linea.replace('\t', '').replace('"','').replace('\x00', '').replace('\n', '').replace('null','')
            
            
            elementos = newline.split("','")
           
            
            elementos = [elemento.replace("'",'') for elemento in elementos if elemento]
            if elementos!=[]:
                cursor.execute("SELECT id FROM Palabra where palabra=%s",(elementos[0],))
                id=cursor.fetchall()
                print(elementos[0])
                print(id)
                if id !=[]:
                    id=id[0][0]
                    
                    if elementos[1] == 'p': 
                        tag_id = 1
                    elif elementos[1] == 'li': 
                        tag_id = 2
                    elif elementos[1] == 'td': 
                        tag_id = 3
                    elif elementos[1] == 'th': 
                        tag_id = 4
                    elif elementos[1] == 'img': 
                        tag_id = 5
                    elif elementos[1] == 'h1': 
                        tag_id = 6
                    elif elementos[1] == 'h2': 
                        tag_id = 7
                    elif elementos[1] == 'h3': 
                        tag_id = 8
                    else:
                        time.sleep(5)

                    if 'tag_id' in locals():
                        print(elementos)
                        insert_query = 'INSERT INTO tagxpalabra (id_palabra, id_tag, porcentaje) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE porcentaje = %s'
                        cursor.execute(insert_query, (id, tag_id, elementos[2], elementos[2]))
        mariadb_conexion.commit()
    except Exception as e:
        
        print(f"Error: {e}")
        mariadb_conexion.rollback()
dataMR1()
dataMR2()
dataMR3()
dataMR4()
dataMR6()
dataMR7()
dataMR8()
dataMR9()   

