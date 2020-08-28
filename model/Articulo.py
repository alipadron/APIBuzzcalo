"""
Descripción:

Clase que manejará consultas sobre la tabla 'conjunto_articulo'.

Será útil para decerementar la compleidad en sintaxis al momento
de manipular elementos de esta tabla.
"""

import re
import json
import html
import random

import uuid
from time import strftime, gmtime


class Articulo():

    def __init__(self, db):
        """
        Constructor de la clase Articulo.
        """
        self.db = db


    def insertar_articulo(self, art:dict):
        """
        Método que permitirá insertar una fila dentro de la tabla
        'conjunto_articulo'.

        :param atr dict. Diccionario con item a incluir en la tabla
        'conjunto_articulo'
        """
        art_keys = list( art.keys() )

        timestamp = {
            'date': strftime("%d-%b-%Y", gmtime()),
            'time': strftime('%H:%M:%S', gmtime())
        }

        clave_pri = uuid.uuid5(uuid.NAMESPACE_DNS, '{}{}'.format(
            art['id_url'], timestamp['time']
        ))
        
        self.db.raw_insert(
            'INSERT INTO conjunto_articulo \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
                    %s, %s, %s, %s)',
            (
                str(clave_pri),         # id_articulo
                art['id_url'],
                art['asin'] if 'asin' in art_keys\
                    else None,
                art['hash'],
                art['nombre'],
                art['marca'],
                art['moneda'],
                art['precio_venta'] if art['precio_venta'] else 0,
                None,
                art['descripcion_corta'] if 'descripcion_corta' in art_keys\
                    else None,
                art['descripcion'],
                art['disponibilidad'],
                art['stock'] if 'stock' in art_keys\
                    else None,
                art['imagenes'],
                json.dumps( art['informacion'] ) if 'informacion' in art_keys\
                    else None,
                art['destino'] if 'destino' in art_keys\
                    else None,
                art['idioma'] if 'idioma' in art_keys\
                    else None,
                art['sku'] if 'sku' in art_keys\
                    else None
                # tomado & descripcion_completa = False
            )
        )

    
    def eliminar_articulo(self, id_articulo:str):
        """
        Método que permitirá eliminar un artículo de la tabla.
        """
        if id_articulo:
            self.db.raw_delete('DELETE FROM conjunto_articluo \
                WHERE id_articulo=\'{}\'')

    
    def filtrar_articulo(self, filtro:dict) -> list:
        """
        Método que permite consultar artículos dependiendo de los filtros
        a realizar.

        Todas las comparaciones serán de igualdad.

        :param filtro dict. Attributos y sus posibles valores a tomar 
        en cuenta durante las comparaciones.

        :return out list <tuple>. Retorna una lista con los atributos
        de la consulta.
        """

        t_filtro = ''
        for (k,v) in filtro.items():
            t_filtro += ' {} = \'{}\' '.format( k, v )

        consulta = 'SELECT * FROM conjunto_articulo WHERE {}'.format( t_filtro )

        out = self.db.raw_query( consulta )

        if len(out):
            t_out = []
            for fila in out:
                t_out.append(
                    list( map( lambda x: html.unescape(x), 
                        [ e for e in fila if type(e) == str] ))
                )
            out = t_out

        return out if len( out ) else []


    def obtener_articulo(self, id_articulo:str='', asin:str='') -> list:
        """
        Método que permite obtener un articulo usando los atributos
        'id_articulo', 'asin' como filtros.

        :return list <tuple>. Retorna una lista con los atributos
        de la consulta.
        """
        filtro = {}

        if id_articulo:
            filtro['id_articulo'] = id_articulo
        
        if asin:
            filtro['asin'] = asin
        
        if filtro == {}:
            return filtro

        return self.filtrar_articulo( filtro=filtro )

    # CRITIC: Si la tabla 'conjunto_articulo' sufre cambios, esto método también
    def obtener_articulo_dict( self, id_url:str='', asin:str=''):
        """
        Método que permite realizar una consulta de un artíuclo
        lo retorna en modo diccionario, incluyendo todos los attrs.

        :param id_url str. Identificador del artículo a filtrar.

        :param asin str. Código ASIN (Solo Amazon) del artículo a filtrar.
        """
        filtro = ''

        if id_url != '':
            filtro = ' id_url = \'{}\''.format( id_url)
            
        elif asin != '':
            filtro = ' asin = \'{}\''.format(asin)

        if filtro == '':
            print('[INFO] Filtro es vacio, no se prcede con la consulta.\n')
            return {}

        consulta = 'SELECT * FROM conjunto_articulo where {}'.format( filtro )

        values = self.db.raw_query(consulta)

        if len( values ) < 1:
            print('[INFO] Consulta sobre: {} resulta en vacio.\n')
            return {}

        key = [
            'id_articulo', 'id_url', 'asin', 'hash', 'nombre', 'marca', 
            'moneda', 'precio_venta', 'precio_regular', 'descripcion_corta', 'descripcion',
            'disponibilidad', 'stock', 'imagenes', 'informacion', 'destino', 'idioma', 'sku',
            'tomado', 'extraccion_completa', 'tipo', 'timestamp'
        ]
        values = list( values[0] )

        out = dict( zip(key, values))

        if type(out['informacion']) == str:
            out['informacion'] = json.loads( out['informacion'] )

        return out 


    # CRITIC: Si la tabla 'conjunto_articulo' sufre cambios, esto método también
    def obtener_informacion(self, id_articulo:str='', asin:str='', articulo:list=[]) -> dict:
        """
        Método que retorna el attr. 'informacion'.

        :param id_articulo str.

        :param asin str.

        :param articulo list. Si el articulo ya está disponible, entonces
        no es necesario usar el método 'obtener_articulo' para obtenerlo.

        :return dict out. Ejemplo:
            Para articulos de  tipo Amazon-Item.
            {'informacion': {
                    'Dimensiones del paquete': '10.91 x 7.44 x 0.55 pulgadas',
                    'Peso del producto': '7 onzas',
                    'ASIN': 'XXXXXXXXX',
                    'Edad recomendada por el fabricante': '',
                    'Clasificación en los más vendidos de Amazon': '',
                    'Opinión media de los clientes': '',
                    'Fabricante': ''
                }
            }
        """
        if len( articulo ) < 1:
            vals = self.obtener_articulo( id_articulo, asin )
        else:
            vals = articulo

        if len( vals[0] ) < 1:
            return {}

        vals = vals[0]
        
        if 'ASIN' in vals[-3]:
            inf = -3
        elif 'ASIN' in vals[-4]:
            inf = -4

        if type( vals[ inf ] ) == str:
            vals = json.loads( vals[ inf ] )

        out = {
            'informacion' : vals
        }

        return out 


    def actualizar_articulo(self, attrs:dict):
        """
        Método que permite actualizar artículos partiendo de un
        diccionario con atributos.

        Se debe incluir al menos un atributo que permita filtrar
        el artículo.

        Ejemplo:{
            'id_articulo': str,
            'asin' : str,
            'key':  value ,... 
        }

        :param attrs dict. Diccionario con información necesaria para
        para inciar el proceso de actualización.
        """
        keys = list( attrs.keys() )
        filtro, atributos = '', ''

        if 'id_url' in keys:
            filtro += ' id_url = \'{}\' '.format( attrs['id_url'] )

        if 'asin' in keys:
            if filtro != '':
                filtro += ' and '
            filtro += ' asin = \'{}\' '.format( attrs['asin'] )

        for (k, v) in attrs.items():
            if k != 'asin' and k != 'id_url':
                if k == 'informacion':
                    v = json.dumps( attrs['informacion'] )

                atributos += ' {} = \'{}\', '.format( k, v )
        
        # Se elimina el último separador
        atributos = atributos[:-2]

        # print( filtro )
        # print( atributos )

        consulta = 'UPDATE conjunto_articulo\
            SET {}\
            WHERE {}'.format( atributos, filtro )

        self.db.raw_update( consulta )

    
    def tomar_articulo_cat(self, tipo_url:str, categoria:str='', destino='', \
        not_tienda:str='', tienda:str='', q_random:bool=False, \
        idioma:str='', completo:bool=False, tomado:bool=False, limite:int=1, \
        modo_dict:bool=False, solo_cant:bool=False, check_tomado_art:bool=False):
        """
        Método que realiza una serie de joins para encontrar artículos dada una 
        secuencia de parámetros.

        El attr. 'tipo_url' será el que contenga el artículo a tomar. Por ejemplo
        para el caso de Amazon el url que cumple con esto es el url de tipo
        'Amazon-Item'.

        :param tipo_url str [REQUERIDO]. Determina el url que contiene el item a tomar. 
        Para el caso de Amazon, es 'Amazon-Item'.

        :param categoria str. Categoría al que deberá pertenecer el 
        url a tomar.

        :param destino str. Cada artículo posee un destino en sus attrs. 
        por lo cual será útil para las filtraciones. Si el attr. es vacío, no
        filtrará por destino.

        :param not_tienda str. Nombre de la tienda al cual no debe pertenecer
        el artículo a tomar.

        :param tienda str. Nombre de la tienda al cual debe pertenecer el 
        articulo a tomar

        :param q_random bool. Este parámetro permite tomar elementos de modo aleatorio
        partiendo de filtraciones anteriores.

            Si es Verdad, consulta y luego se toma un item aleatorio.
            Si es Falso, se consulta y se retorna la primera ocurrencia,

        :param idioma str. Parámetro que determina si se puede filtrar por algún idioma
        del el artículo. Si no se requiere filtrar por algún idioma, colocarlo en vacío.

        :param completo bool. Determina si el artículo a tomar está en las condiciones
        necesarias para ser utilizado en tiendas destino.

        :param tomado bool. Determina si el artículo a sido tomado, esto evita usar
        el mismo recurso o artículo en más de una ocasión.

        :param limit int. Cantidad de elementos a retornar partiendo de un filtrado
        anterior. Cuando el parámetro q_random está habilitado, el límite por 
        defecto será igualado a 1.

        :param modo_dict bool.

            Si es Verdad, se retornará una lista con diccionarios dentro. Ejemplo:
                [
                    {
                        id_url    : str,
                        asin      : str,
                        categoria : {
                            id    : str,
                            ref   : str,
                            name  : str,
                            nivel : int,
                            nombre: str
                        },
                        url       : str
                    }
                ]
            Sie es False, se retornará una lista con tuplas.

        :param solo_cant bool. Para obtener cantidades se debe habilitar el param.
        'q_random' a Verdad.
            True: Se consulta solo la cantidad de filas disponibles dado el filtro.
            Ejemplo de salida: 
                {
                    'tipo_url'  : str,
                    'categoria' : str,
                    'destino'   : str,
                    'cantidad'  : int
                }

            False: Se consulta la cantidad de filas disponibles dado el filtro y sus valores.
            La salida será una lista de tuplas o un diccionario, dependiendo de los resultados
            y del param 'modo_dict'.

        :param check_tomado_art bool. 
            Verdad: Se actualizará el attributo 'tomado' del Artículo a Verdad.
            Falso: El attributo 'tomado' no sufrirá  de actualizaciones.

        :return list out. Lista con los elementos retornados.
        """

        params = 'c_a.id_url, c_a.asin, url_out.categoria, url_out.url'

        consulta = 'select Q_PARAMS \
            from conjunto_articulo as c_a \
            inner join( \
                \
                select c_u_3.id_url, c_u_3.url, url_gen.categoria \
                from conjunto_url as c_u_3 \
                    inner join(\
                        \
                        select c_u_2.id_url, url_cat.categoria \
                        from conjunto_url as c_u_2 \
                            inner join ( \
                                select c_u.id_url, c_u.categoria \
                                from conjunto_url as c_u \
                                where \
                                    categoria->>\'nombre\' like(\'%{}%\') \
                                ) url_cat \
                            on c_u_2.id_url_referencia = url_cat.id_url \
                    ) url_gen \
                on c_u_3.id_url_referencia = url_gen.id_url \
                where \
                    c_u_3.tipo = \'{}\' TIENDA \
            ) url_out \
        on c_a.id_url = url_out.id_url \
        where COMPLETO TOMADO IDIOMA DESTINO'.format( categoria, tipo_url )

        # Con esta lista de condiciones se arma el filtro para el atrículo
        articulo_cond = []

        t_completo = 'is True' if completo else 'is not True'
        articulo_cond.append( 'c_a.extraccion_completa {}'.format( t_completo ) )
        consulta = consulta.replace( 'COMPLETO', '' )

        t_tomado = 'is True' if tomado else 'is not True'
        articulo_cond.append( 'c_a.tomado {}'.format( t_tomado ) )
        consulta = consulta.replace('TOMADO', '' )

        if idioma != None:
            articulo_cond.append( 'c_a.idioma like(\'%{}%\')'.format( idioma ) )
        consulta = consulta.replace('IDIOMA', '')

        if destino != None:
            articulo_cond.append( 'c_a.destino like(\'%{}%\')'.format( destino ) )
        consulta = consulta.replace('DESTINO', '')

        # Aplico filtros sobre el atributo
        consulta += ' and '.join( articulo_cond )

        # Se modifica el tipo de tienda a filtrar
        tienda_filtro = ''
        if not_tienda != '':
            tienda_filtro = ' and c_u_3.id_url not in ( \
                    select id_url from url_tienda, tienda \
                    where tienda.nombre = \'{}\' )'.format( not_tienda )
        elif tienda != '':
            tienda_filtro = ' and c_u_3.id_url in ( \
                    select id_url from url_tienda, tienda \
                    where tienda.nombre = \'{}\' )'.format( tienda )

        consulta = consulta.replace('TIENDA', tienda_filtro)
        # print( consulta )

        if q_random:
            t_consulta = consulta.replace( 'Q_PARAMS', 'count(*)' )

            # print( t_consulta )

            n = self.db.raw_query( t_consulta )

            if solo_cant:
                return {
                    'tipo_url'  : tipo_url,
                    'categoria' : categoria,
                    'destino'   : destino,
                    'cantidad'  : n[0][0] if len(n) and len(n[0]) else 0
                }

            if not len(n) or not len(n[0]):
                print('[INFO] Url de tipo {} no disponible'.format(
                    tipo_url
                ))
                return []

            if n[0][0] <= 0: 
                return []

            n = random.randint(1, int(n[0][0]))

            consulta += ' limit {} offset {}-1'.format( 
                str(limite), str(n)
            )

        consulta = consulta.replace('Q_PARAMS', params)
        # print( consulta )
        out = self.db.raw_query( consulta )
        
        out_dict = []
        if modo_dict:
            key = ['id_url', 'asin', 'categoria', 'url']

        # 2 modos de retorno | actualización a cumplir con dict con lista
        for fila in out:
            t_dict, t_art_update = {}, {}
            value = list( fila )
            if modo_dict:
                t_dict = dict( zip( key, value ))
                out_dict.append( t_dict )
                t_art_asin = t_dict['asin']
            else:
                # lista con tupla
                t_art_asin = value[1]

            if check_tomado_art:
                t_art_update = { 
                    'asin'  : t_art_asin,
                    'tomado' : True
                }
                self.actualizar_articulo(attrs=t_art_update)
                # print('articulo actualizado: {}'.format( t_art_update['asin'] ) )
            
        out = out_dict if modo_dict else out
        
        return out


    def ampliar_sku(self, sku:dict, id_url:str='', asin:str=''):
        """
        Método que permitirá ampliar el attr. sku del artículo
        filtrado por el identificador 'id_url'.

        El attr. SKU (dentro del contexto de mercadolibre) indica
        que un artículo pertenece a una tienda. Luego de ser insertado
        en la tienda, usando las correspondientes APIs para las tiendas
        destino.

        :param sku dict. Diccionario con las propiedades necesarias
        para ser diferenciado de otros SKU.

        Ejemplo del parámetro 'sku':
        {
            'nombre_tienda' : 1234
        }

        :param id_url str. Identificador que definirá el artículo a 
        añadirle un nuevo SKU.

        :param asin str. Identificador del artículo.
        """

        if id_url != '':
            filtro = 'id_url = \'{}\''.format( id_url )
        elif asin != '':
            filtro = 'asin = \'{}\''.format( asin )

        if filtro == '':
            print('[INFO] no existen filtros, no se continua la consulta')
            return 

        # Determinar si el SKU es nulo
        out = self.db.raw_query(
            'select sku from conjunto_articulo where {}'.format( filtro )
        )
        
        if not out[0][0]:
            # sku nulo
            t_sku = 'sku = \'{}\''.format( json.dumps( sku ) )
        else:
            items_sku = list( list( sku.items() )[0] ) 
            t_sku  = 'sku = jsonb_set( sku::jsonb, {}, {}::jsonb, true )'.format( 
                '\'{' + items_sku[0] + '}\'',
                "'" + str( items_sku[1] ) + "'"
            )

        consulta = 'update conjunto_articulo set {} where {}'.format( t_sku, filtro )

        self.db.raw_update( consulta )


"""
from db.Database import Database
from model.Articulo import Articulo

db = Database()
modelo_articulo = Articulo( db=db )

asin = 'B081KQF332'
asin2 = 'B07K8Y613T'
out = modelo_articulo.obtener_articulo_dict( asin=asin )

out = modelo_articulo.obtener_informacion( asin=asin )

out2 = modelo_articulo.obtener_informacion( asin=asin2 )

# tomar elementos y retornarlos usando diccionarios

categoria='Juguetes y juegos'
destino='33166'
tienda = 'ML-COL-A'
tipo='Amazon-Item'

conjunto_url = modelo_articulo.tomar_articulo_cat(
    categoria=categoria,
    tipo_url=tipo,
    destino=destino,
    not_tienda=tienda,
    # tienda=tienda,
    q_random=True,
    check_tomado=None,
    sku=False,
    modo_dict=True
)

db.close()

"""
        