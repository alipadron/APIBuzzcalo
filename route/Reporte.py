"""
Descripción:

Ruta con un conjunto de endpoints que suministrarán información de los elementos
dentro de la base de datos.
"""

import time

from flask_cors import CORS, cross_origin
from flask import session, request, jsonify, make_response
from flask import Blueprint, render_template, redirect, url_for

from db.Database import Database
from model.Articulo import Articulo

reporte = Blueprint('reporte', __name__)

CORS(reporte)

@reporte.route('/buzzcalo', methods=['GET'])
def obtener_reporte():
    status_code = 200

    db = Database()
    modelo_articulo = Articulo(db=db)
    destino = '33166' # Por defecto el destino será 33166, US Zip Code - Florida

    articulos_total = db.raw_query('select count(*) \
        from conjunto_url where tipo like(\'%Item\')')

    # buzzcalo - filtros
    articulos_total = int( articulos_total[0][0] )

    conjunto_categoria = db.raw_query('select distinct(categoria->>\'nombre\') \
        from conjunto_url where tipo like(\'%-Lista\') and categoria->>\'nombre\' is not null')

    out_categoria = []
    for categoria in conjunto_categoria:
        t_out = modelo_articulo.tomar_articulo_cat(
            tipo_url='Amazon-Item',
            categoria=categoria[0],
            destino=destino,
            # not_tienda,
            # tienda,
            q_random=True,
            idioma=None,
            # completo=False,
            # tomado=False,
            # limite=1,
            modo_dict=False,
            solo_cant=True,
            check_tomado_art=False
        )
        out_categoria.append( 
            {
                'nombre'    : t_out['categoria'],
                'cantidad'  : t_out['cantidad']
            }
        )

    # amazon - filtros
    articulos_vender = db.raw_query('select count(*) \
        from conjunto_articulo where informacion != \'{}\' and destino like(\'%33166%\');')
    articulos_vender = articulos_vender[0][0]

    listas_total = db.raw_query('select count(*) \
        from conjunto_url where tipo like(\'%Lista%\')')
    listas_total = listas_total[0][0]

    listas_actualizadas = db.raw_query('select count(*) \
        from conjunto_url where tipo like(\'Amazon-Lista%\') and \
            cast( extract( epoch from now() ) as int ) - timestamp < 8 * 3600')
    listas_actualizadas = listas_actualizadas[0][0]
    
    # mercadolibre - filtros
    articulos_vendiendo_total = db.raw_query('select count(*) \
        from conjunto_articulo where sku is not null;')
    articulos_vendiendo_total = articulos_vendiendo_total[0][0]

    conjunto_tiendas = db.raw_query('select nombre from tienda')
    out_conjunto_tiendas = []
    for tienda in conjunto_tiendas:
        t_out = db.raw_query('select count(*) \
            from conjunto_articulo where sku->>\'{}\' is not null'.format( tienda[0] ))
        out_conjunto_tiendas.append(
            {
                'nombre'    : tienda,
                'cantidad'  : int( t_out[0][0] )
            }
        )

    # trm - filtro
    trm = db.raw_query('select trm from trm where id_trm = \'trm_buzzcalo\'')
    trm = trm[0][0]

    # proxies - filtros
    gratuito = db.raw_query('select count(*) \
        from conjunto_proxy where en_uso = True and gratuito=True')
    gratuito = gratuito[0][0]

    premium = db.raw_query('select count(*) \
        from conjunto_proxy where en_uso = True and gratuito=False')
    premium = premium[0][0]

    out = {
        'timestamp' : int( time.time() ),
        'reporte'   : 'buzzcalo',
        'status'    : 'ok',
        'buzzcalo'  : {
            'articulos_total'   : articulos_total,
            'categoria'         : out_categoria
        },
        'amazon' : {
            'articulos_vender'      : articulos_vender,
            'listas_total'          : listas_total,
            'listas_actualizadas'   : listas_actualizadas

        },
        'mercadolibre' : {
            'articulos_vendiendo_total' : articulos_vendiendo_total,
            'tiendas_destino'           : out_conjunto_tiendas

        },
        'trm' : trm,
        'proxy' : [
            {
                'nombre'    : 'gratuito',
                'cantidad'  : gratuito
            },
            {
                'nombre'    : 'premium',
                'cantidad'  : premium
            }
        ]

    }

    db.close()
    return jsonify(out), status_code
