/**
 * Renderizador de elementos.
 *
 * Dev: Franco Gil
 * Fecha: Agosto 27, 2020
 */

var apiUrl = "http://ec2-34-212-136-15.us-west-2.compute.amazonaws.com";

// function card_buzzcalo( obj_buzzcalo ){

//     buzzcalo_articulo = document.getElementById('buzzcalo_articulos_total');

//     buzzcalo_articulo.innerHTML = `
//         Cantidad <span class="badge badge-light" data-toggle="tooltip"
//             data-placement="top" title="Cantidad: ${obj_buzzcalo.articulos_total}">
//             ${obj_buzzcalo.articulos_total}
//         </span>`

//     buzzcalo_categoria = document.getElementById('buzzcalo_categoria');

//     n = obj_buzzcalo.categoria.length;
//     elemn_interno = '';
//     for(i=0; i < n; i++){
//         elemn_interno += `<li class="list-group-item">
//             ${obj_buzzcalo.categoria[i].nombre}: <span class="badge badge-secondary">
//                 ${obj_buzzcalo.categoria[i].cantidad}
//             </span>
//         </li> `;
//     }

//     buzzcalo_categoria.innerHTML = elemn_interno;
// }

// function card_amazon( obj_amazon ){

//     amazon_articulos_vender = document.getElementById('amazon_articulos_vender');

//     amazon_articulos_vender.innerHTML = `
//         Cantidad <span class="badge badge-light" data-toggle="tooltip"
//             data-placement="top" title="Cantidad: ${obj_amazon.articulos_vender}">
//             ${obj_amazon.articulos_vender}
//         </span>
//     `

//     amazon_listas_actualizadas = document.getElementById('amazon_listas_actualizadas');

//     amazon_listas_actualizadas.innerHTML = `
//         Cantidad <span class="badge badge-light" data-toggle="tooltip"
//             data-placement="top" title="Cantidad: ${obj_amazon.listas_actualizadas}">
//             ${obj_amazon.listas_actualizadas}
//         </span>
//     `
// }

// function card_mercadolibre( obj_mercadolibre ){

//     mercadolibre_destino = document.getElementById('mercadolibre_destino');

//     mercadolibre_destino.innerHTML = `
//     Cantidad <span class="badge badge-light" data-toggle="tooltip"
//         data-placement="top" title="Cantidad: ${obj_mercadolibre.articulos_vendiendo_total}">
//         ${obj_mercadolibre.articulos_vendiendo_total}
//     </span>`;

//     mercadolibre_destino_tienda = document.getElementById('mercadolibre_destino_tienda');

//     n = obj_mercadolibre.tiendas_destino.length;
//     elemn_interno = '';

//     for(i=0; i < n; i++){
//         elemn_interno += `<li class="list-group-item">
//             ${obj_mercadolibre.tiendas_destino[i].nombre}: <span class="badge badge-warning">
//                 ${obj_mercadolibre.tiendas_destino[i].cantidad}
//             </span>
//         </li> `;
//     }

//     mercadolibre_destino_tienda.innerHTML = elemn_interno;
// }

// function card_trm( obj_trm ){

//     trm_metricas = document.getElementById('trm_metricas');

//     // fecha = obj_trm.timestamp;

//     trm_metricas.innerHTML = `
//         <li class="list-group-item">
//             <span class="badge badge-success">COP ➜ USD</span>
//             ${obj_trm.cop} USD 🇺🇸
//         </li>
//         <li class="list-group-item">
//             <span class="badge badge-success">USD ➜ COP</span>
//             ${obj_trm['usd-cop']} COP 🇨🇴
//         </li>
//         <li class="list-group-item">
//             <span class="badge badge-success">USD ➜ MEX:</span>
//             ${obj_trm['usd-mex']} MEX 🇲🇽
//         </li>`;
// }

// async function renderizar(){

//     var endpoint = domain + "/buzzcalo";
//     // var endpint = domain + '/static/assets/server_mock.json';

//     const response = await fetch(endpoint);
//     var staticData = await response.json();

//     card_buzzcalo( staticData.buzzcalo );
//     card_amazon( staticData.amazon );
//     card_mercadolibre( staticData.mercadolibre );
//     card_trm( staticData.trm );
// }

// console.log("Renderizar");

// renderizar();

// console.log("Fin renderizar");

// function getData() {
//   console.log('alicate');
//   // return $.ajax(`${apiUrl}/buzzcalo`);
// }

// getData().then(console.log)
$(() => {
  function getData() {
    return $.ajax(`${apiUrl}/buzzcalo`);
  }

  function renderAccordionChild(section, collapsed = true) {
    const { id, img, title, description, quantity, content } = section;
    const template = `
    <div class="card">
          <div class="card-header" id="heading${id}">
            <h2 class="mb-0">
              <button
                class="btn btn-link btn-block text-left d-flex justify-content-between align-items-center ${
                  collapsed ? "collapsed" : ""
                }"
                type="button"
                ${content ? 'data-toggle="collapse"' : ""}
                data-target="#collapse${id}"
                aria-expanded="${!collapsed}"
                aria-controls="collapse${id}"
              >
                <div class="d-flex align-items-center">
                  <img
                    src="${img}"
                    width="30"
                    height="30"
                    class="d-inline-block align-top rounded mr-2"
                    loading="lazy"
                  />
                  <p class="mb-0 mr-2" style="font-size: 1.25rem">
                    ${title}
                  </p>
                  <p class="m-0 text-dark">${description}</p>
                </div>
                <p class="m-0">
                  Cantidad <span class="badge badge-secondary">${quantity}</span>
                </p>
              </button>
            </h2>
          </div>

          <div
            id="collapse${id}"
            class="collapse ${collapsed ? "" : "show"}"
            aria-labelledby="heading${id}"
            data-parent="#accordion"
          >
            <div class="card-body">
              ${content}
            </div>
          </div>
        </div>
    `;
    $("#accordion").append(template);
  }

  function renderBuzzcalo(data, section) {
    if (!data || !section) {
      return;
    }

    const content = `
    <ul class="list-group list-group-flush">
      ${data.categoria
        .map(
          (c) =>
            `
        <li
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          ${c.nombre}: <span class="badge badge-secondary"> ${c.cantidad} </span>
        </li>`
        )
        .join("")}
    </ul>
    `;

    renderAccordionChild({
      ...section,
      content,
      quantity: data.articulos_total,
    });
  }

  function renderMercadolibre(data, section) {
    if (!data || !section) {
      return;
    }

    const content = `
    <ul class="list-group list-group-flush">
      ${data.tiendas_destino
        .map(
          (c) =>
            `
        <li
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          ${c.nombre}: <span class="badge badge-secondary"> ${c.cantidad} </span>
        </li>`
        )
        .join("")}
    </ul>
    `;

    renderAccordionChild({
      ...section,
      content,
      quantity: data.articulos_vendiendo_total,
    });
  }

  const sections = [
    {
      id: "buzzcalo",
      title: "Cantidades y artículos",
      description: "Artículos de buzzcalo.",
      img: "../../static/assets/images/sm_buzz.ico",
      content: "",
      quantity: 0,
    },
    {
      id: "amazon",
      title: "Amazon",
      description: "Artículos tomados desde Amazon y disponibles para vender.",
      img: "../../static/assets/images/Amazon-512.webp",
      content: "",
      quantity: 0,
    },
    {
      id: "listas-amazon",
      title: "Listas Amazon",
      description: "Cantidad de Listas de Amazon actualizadas.",
      img: "../../static/assets/images/Amazon-512.webp",
      content: "",
      quantity: 0,
    },
    {
      id: "mercadolibre",
      title: "Mercadolibre",
      description: "Cantidad de elementos en tiendas de Mercadolibre.",
      img: "../../static/assets/images/mercado-libre-logo.png",
      content: "",
      quantity: 0,
    },
  ];

  getData().then((data) => {
    const { buzzcalo, mercadolibre, amazon, trm } = data;

    renderBuzzcalo(
      buzzcalo,
      sections.find((s) => s.id === "buzzcalo")
    );

    renderMercadolibre(
      mercadolibre,
      sections.find((s) => s.id === "mercadolibre")
    );

    renderAccordionChild({
      ...sections.find((s) => s.id === "amazon"),
      quantity: amazon.articulos_vender,
    });

    renderAccordionChild({
      ...sections.find((s) => s.id === "listas-amazon"),
      quantity: amazon.listas_actualizadas,
    });

    $("#actualizado").text(
      "Actualizado hace " +
        moment
          .duration((data.timestamp - trm.timestamp) / 60 / 60, "hours")
          .format("hh [horas] [y] mm") +
        " minutos"
    );

    $("#cop-usd").html(`
    <span  class="badge badge-success">COP ➜ USD</span>
      ${trm.cop.toFixed(8)} USD
    `);

    $("#usd-cop").html(`
    <span  class="badge badge-success">USD ➜ COP</span>
      ${trm["usd-cop"].toFixed(2)} COP
    `);

    $("#usd-mex").html(`
    <span  class="badge badge-success">USD ➜ MEX</span>
      ${trm["usd-mex"].toFixed(2)} MEX
    `);

    $("#tasa-mercado").removeClass('d-none');
    $("#loading").remove();
  });
});
