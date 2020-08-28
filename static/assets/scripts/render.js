/**
 * Renderizador de elementos.
 * 
 * Dev: Franco Gil
 * Fecha: Agosto 27, 2020
*/

var domain = "http://127.0.0.1:8000";


function card_buzzcalo( obj_buzzcalo ){

    buzzcalo_articulo = document.getElementById('buzzcalo_articulos_total');

    buzzcalo_articulo.innerHTML = `
        Cantidad <span class="badge badge-light" data-toggle="tooltip" 
            data-placement="top" title="Cantidad: ${obj_buzzcalo.articulos_total}">
            ${obj_buzzcalo.articulos_total}
        </span>`

    buzzcalo_categoria = document.getElementById('buzzcalo_categoria');

    n = obj_buzzcalo.categoria.length;
    elemn_interno = '';
    for(i=0; i < n; i++){
        elemn_interno += `<li class="list-group-item">
            ${obj_buzzcalo.categoria[i].nombre}: <span class="badge badge-secondary">
                ${obj_buzzcalo.categoria[i].cantidad}
            </span>
        </li> `;
    }

    buzzcalo_categoria.innerHTML = elemn_interno;
}


function card_amazon( obj_amazon ){

    amazon_articulos_vender = document.getElementById('amazon_articulos_vender');

    amazon_articulos_vender.innerHTML = `
        Cantidad <span class="badge badge-light" data-toggle="tooltip" 
            data-placement="top" title="Cantidad: ${obj_amazon.articulos_vender}">
            ${obj_amazon.articulos_vender}
        </span>
    `

    amazon_listas_actualizadas = document.getElementById('amazon_listas_actualizadas');

    amazon_listas_actualizadas.innerHTML = `
        Cantidad <span class="badge badge-light" data-toggle="tooltip" 
            data-placement="top" title="Cantidad: ${obj_amazon.listas_actualizadas}">
            ${obj_amazon.listas_actualizadas}
        </span>
    `
}


function card_mercadolibre( obj_mercadolibre ){

    mercadolibre_destino = document.getElementById('mercadolibre_destino');

    mercadolibre_destino.innerHTML = `
    Cantidad <span class="badge badge-light" data-toggle="tooltip" 
        data-placement="top" title="Cantidad: ${obj_mercadolibre.articulos_vendiendo_total}">
        ${obj_mercadolibre.articulos_vendiendo_total}
    </span>`;

    mercadolibre_destino_tienda = document.getElementById('mercadolibre_destino_tienda');

    n = obj_mercadolibre.tiendas_destino.length;
    elemn_interno = '';

    for(i=0; i < n; i++){
        elemn_interno += `<li class="list-group-item">
            ${obj_mercadolibre.tiendas_destino[i].nombre}: <span class="badge badge-warning">
                ${obj_mercadolibre.tiendas_destino[i].cantidad}
            </span>
        </li> `;
    }

    mercadolibre_destino_tienda.innerHTML = elemn_interno;
}


function card_trm( obj_trm ){

    trm_metricas = document.getElementById('trm_metricas');

    // fecha = obj_trm.timestamp;

    trm_metricas.innerHTML = `
        <li class="list-group-item">
            <span class="badge badge-success">COP ➜ USD</span>
            ${obj_trm.cop} USD 🇺🇸
        </li>
        <li class="list-group-item">
            <span class="badge badge-success">USD ➜ COP</span>
            ${obj_trm['usd-cop']} COP 🇨🇴
        </li>
        <li class="list-group-item">
            <span class="badge badge-success">USD ➜ MEX:</span>
            ${obj_trm['usd-mex']} MEX 🇲🇽
        </li>`;
}


async function renderizar(){

    var endpoint = domain + "/buzzcalo"

    const response = await fetch(endpoint);
    var staticData = await response.json();

    //console.log( staticData )
    card_buzzcalo( staticData.buzzcalo );
    card_amazon( staticData.amazon );
    card_mercadolibre( staticData.mercadolibre );
    card_trm( staticData.trm );
}

console.log("Renderizar");

renderizar();

console.log("Fin renderizar");
