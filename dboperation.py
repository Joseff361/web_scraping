import psycopg2


class DBWebscraping:
    def __init__(self):
        pass

    def insert_webscraping(self, connection, carga):
        try:
          mydb = connection.connect()         
          cur = mydb.cursor() 
          # insertando un registro
          sql = "insert into webscraping (busqueda, busqueda_area, pagina_web, url_pagina, url_busqueda,fecha_creacion,fecha_modificacion, id_keyword, delati_team) values (%s,%s,%s,%s,%s,current_date,current_date,%s,%s)"
          params = (carga["busqueda"], carga["busqueda_area"], carga["pagina"], carga["url_principal"],carga["url_busqueda"], carga["id_keyword"], carga["delati_team"])
                    
          cur.execute(sql, params)                 

          mydb.commit()

          sql = "SELECT last_value FROM webscraping_id_webscraping_seq"
          cur.execute(sql)  
          row_id = int(cur.fetchone()[0])
          
          # close the communication with the PostgreSQL
          cur.close()
          mydb.close()      
        except (Exception, psycopg2.DatabaseError) as error:                
                print (error)
                mydb.close()
        
        print(row_id)        
        return row_id


class DBOferta:
    def __init__(self):
        pass

    def insert_oferta(self, connection, oferta):        
        try:
            mydb = connection.connect()
            cur = mydb.cursor()                                    
            sql = "insert into Oferta (id_webscraping, titulo,empresa,lugar,salario,oferta_detalle,url_oferta,url_pagina,time_publicacion, area, id_anuncioempleo,fecha_publicacion, fecha_creacion,fecha_modificacion) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,current_date,current_date)"            
            params = (oferta["id_carga"], oferta["puesto"].strip(), oferta["empresa"].strip(), oferta["lugar"].strip(),oferta["salario"].strip(),oferta["detalle"].strip(), oferta["url"], oferta["url_pagina"], oferta["time_publicacion"], oferta["area"], oferta["id_anuncioempleo"], oferta["fecha_publicacion"])
            cur.execute(sql, params)        
            mydb.commit()            


            sql = "SELECT last_value FROM Oferta_id_Oferta_seq"
            cur.execute(sql)  
            row_id = int(cur.fetchone()[0])  
            
            # close the communication with the PostgreSQL
            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
                print ("-------------Exception, psycopg2.DatabaseError-------------------")
                print (error)
                mydb.close()        
            
        return row_id

    def evitar_redundancia(self, connection, oferta):        
        try:
            mydb = connection.connect()
            cur = mydb.cursor()                                    
            row = None
            sql = "SELECT * FROM OFERTA WHERE URL_OFERTA = '" + oferta["url"] + "' AND ID_ESTADO IS NULL LIMIT 1;" 
            #print(sql)
            cur.execute(sql)  
            row = cur.fetchone()

            # close the communication with the PostgreSQL
            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
                print ("-------------Exception, psycopg2.DatabaseError-------------------")
                print (error)
                mydb.close()        
            
        return row


class DBOfertadetalle:
    def __init__(self):
        pass

    def update_ofertadetalle(self, connection, requisito):
        mydb = connection.connect()
        mycursor = mydb.cursor()
        sql = "UPDATE OFERTA_DETALLE SET descripcion_normalizada=:1 where id_ofertadetalle=:2"
        params = (requisito["descripcion_normalizada"], requisito["iddescripcion"])

        mycursor.execute(sql, params)
        mydb.commit()

    def insertOfertaDetalle(self, connection, detalle):
        try:
            mydb= connection.connect()
            mycursor= mydb.cursor()
            sql= "insert into oferta_detalle ( id_ofertadetalle, id_oferta, descripcion, fecha_creacion, fecha_modificacion) values (DEFAULT,%s,%s,current_date,current_date)"
            params= (detalle["id_oferta"],detalle["descripcion"])
            mycursor.execute(sql, params)
            mydb.commit()
            # close the communication with the PostgreSQL
            mycursor.close()
            mydb.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print ("-------------Exception, psycopg2.DatabaseError-------------------")
            print (error)
            mydb.close()
        
        return 1


class DBKeyworSearch:
    def __init__(self):
        pass

    def obtener_descripcion(self, connection):        
        try:
            mydb = connection.connect()
            cur = mydb.cursor()                                    

            sql = "SELECT DESCRIPCION, ID_TIPOKEYWORD FROM KEYWORD_SEARCH"
            cur.execute(sql)  
            
            array_de_tuplas = []
            row = cur.fetchone()
            while row is not None:
                array_de_tuplas.append(row)
                row = cur.fetchone()

            # close the communication with the PostgreSQL
            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
                print ("-------------Exception, psycopg2.DatabaseError-------------------")
                print (error)
                mydb.close()        
            
        return array_de_tuplas
