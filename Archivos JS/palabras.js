// FUNCIONES DE PALABRAS
function verificarPalabras(){
    
    var palabras = document.getElementById('busquedaPalabras').value;
    if(palabras.trim() === ''){
        document.getElementById('listaPalabras').innerHTML = "Por favor ingrese palabras válidas";
        var boton = document.getElementById("botonSeguir");
        boton.style.display = "none";

    }else{
        var palabrasSeparadas = palabras.split(' ');
        var palabrasUnicas = [...new Set(palabrasSeparadas)];

        
        localStorage.setItem('listaPalabras', JSON.stringify(palabrasUnicas));
        document.getElementById('listaPalabras').innerHTML = palabrasUnicas;

        var boton = document.getElementById("botonSeguir");
        boton.style.display = "block";
    }
    var myModalEl = document.querySelector('#modalPalabras');
    var modal = bootstrap.Modal.getOrCreateInstance(myModalEl);
    modal.show();
}


// FUNCIONES DE PALABRAS INFO
var info = {
    "palabra": "Revolución",
    "paginas": [
      {
        "direccion": "https://www.ejemplo.com/inicio",
        "numero": 125
      },
      {
        "direccion": "https://www.ejemplo.com/servicios",
        "numero": 20
      },
      {
        "direccion": "https://www.ejemplo.com/contacto",
        "numero": 33
      }
    ],
    "porcentajeTodasPaginas": 50,
    "porcentajeTitulos": 75,
    "porcentajeSubtitulos": 30,
    "porcentajeTexto": 90
}

function cargarPagina(){
    var palabras = JSON.parse(localStorage.getItem('listaPalabras'));
    console.log(palabras);
    palabras.forEach(function(elemento) {
        cargarInformacion(elemento);
    });
    cargarTotal();

}

function cargarInformacion(elemento){
    // Crear el contenedor principal
    var divPrincipal = document.createElement('div');
    divPrincipal.classList.add('row', 'text-center', 'cajaPrincipal');

    // Crear titulo de palabra
    var titulo = document.createElement('h4');
    titulo.textContent = info.palabra;
    divPrincipal.appendChild(titulo);


    // Crear la tabla y agregar los datos de las páginas
    var tabla = document.createElement('table');
    tabla.classList.add('table', 'table-primary', 'table-striped');

    // Crear el encabezado de la tabla
    var encabezado = document.createElement('thead');
    var encabezadoRow = document.createElement('tr');
    encabezado.innerHTML = `
        <th scope="col">Página</th>
        <th scope="col">Cantidad</th>
    `;
    encabezado.appendChild(encabezadoRow);
    tabla.appendChild(encabezado);

    // Agregar datos de páginas a la tabla
    var cuerpoTabla = document.createElement('tbody');
    info.paginas.forEach(function(data) {
        var fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${data.direccion}</td>
            <td>${data.numero}</td>
        `;
        cuerpoTabla.appendChild(fila);
    });
    tabla.appendChild(cuerpoTabla);
    divPrincipal.appendChild(tabla);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = info.porcentajeTodasPaginas;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% en todas las páginas";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = info.porcentajeTitulos;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en titulos";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = info.porcentajeSubtitulos;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en subtitulos";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = info.porcentajeTexto;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en el texto";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    // Agregar todo al body del documento
    document.body.appendChild(divPrincipal);

}

function cargarTotal(){
    // Crear el contenedor principal
    var divPrincipal = document.createElement('div');
    divPrincipal.classList.add('row', 'text-center', 'cajaPrincipal');

    // Crear titulo de palabra
    var titulo = document.createElement('h2');
    titulo.textContent = "RESULTADOS GENERALES";
    divPrincipal.appendChild(titulo);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = info.porcentajeTodasPaginas;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% en todas las páginas";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = info.porcentajeTitulos;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en titulos";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = info.porcentajeSubtitulos;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en subtitulos";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = info.porcentajeTexto;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en el texto";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    // Agregar todo al body del documento
    document.body.appendChild(divPrincipal);
}