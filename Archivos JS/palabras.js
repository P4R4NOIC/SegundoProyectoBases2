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

        var palabrasSinTildes = palabrasUnicas.map(function(palabra) {
            return quitarTildes(palabra);
        });
        
        localStorage.setItem('listaPalabras', JSON.stringify(palabrasSinTildes));
        document.getElementById('listaPalabras').innerHTML = palabrasSinTildes;

        var boton = document.getElementById("botonSeguir");
        boton.style.display = "block";
    }
    var myModalEl = document.querySelector('#modalPalabras');
    var modal = bootstrap.Modal.getOrCreateInstance(myModalEl);
    modal.show();
}

function quitarTildes(palabra) {
    return palabra.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

// FUNCIONES DE PALABRAS INFO
// var info = {
//     "palabra": "Revolución",
//     "paginas": [
//       {
//         "direccion": "https://www.ejemplo.com/inicio",
//         "numero": 125
//       },
//       {
//         "direccion": "https://www.ejemplo.com/servicios",
//         "numero": 20
//       },
//       {
//         "direccion": "https://www.ejemplo.com/contacto",
//         "numero": 33
//       }
//     ],
//     "porcentajeTodasPaginas": 50,
//     "porcentajeTitulos": 75,
//     "porcentajeSubtitulos": 30,
//     "porcentajeTexto": 90
// }

function pedirPalabras(palabra){
    let datosRecibidos;
    // Hacer la solicitud GET al servidor
    fetch('http://localhost:3000/palabra/'+palabra)
    .then(response => {
        if (!response.ok) {
            alert('No se pudo obtener la información del usuario');
        }
        return response.json(); // Parsea la respuesta JSON
    })
    .then(data => {
        // Datos recibidos
        datosRecibidos = data;
        cargarInformacion(datosRecibidos);
    })
    .catch(error => {
        console.error('Error al obtener la información del usuario:', error);
    });
}

function cargarPagina(){
    var palabras = JSON.parse(localStorage.getItem('listaPalabras'));
    localStorage.setItem('sumaTodasPaginas', 0);
    localStorage.setItem('sumaTitulos', 0);
    localStorage.setItem('sumaSubtitulos', 0);
    localStorage.setItem('sumaTexto', 0);
    localStorage.setItem('contador', 0);

    function procesarPalabras(index) {
        if (index < palabras.length) {
            pedirPalabras(palabras[index]);

            // Especificar el tiempo de pausa en milisegundos (por ejemplo, 1000 para 1 segundo)
            setTimeout(function() {
                procesarPalabras(index + 1);
            }, 1000); // Pausa de 1 segundo
        } else {
            // Luego de completar el bucle, llamar a cargarTotal
            cargarTotal();
        }
    }

    // Llamar a la función con el índice inicial
    procesarPalabras(0);

}

function cargarInformacion(info){
    console.log(info);
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
    parrafo.textContent = parseFloat(info.porcentajeTodasPaginas.toFixed(4));
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% en todas las páginas";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = parseFloat(info.porcentajeTitulos.toFixed(4));
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en titulos";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = parseFloat(info.porcentajeSubtitulos.toFixed(4));
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en subtitulos";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = parseFloat(info.porcentajeTexto.toFixed(4));
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en el texto";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    // Agregar todo al body del documento
    document.body.appendChild(divPrincipal);

    //CONTADOR
    var sumaTodasPaginas = parseFloat(localStorage.getItem('sumaTodasPaginas'));
    var sumaTitulos = parseFloat(localStorage.getItem('sumaTitulos'));
    var sumaSubtitulos = parseFloat(localStorage.getItem('sumaSubtitulos'));
    var sumaTexto = parseFloat(localStorage.getItem('sumaTexto'));
    var contador = parseInt(localStorage.getItem('contador'));

    sumaTodasPaginas += parseFloat(info.porcentajeTodasPaginas);
    sumaTitulos += parseFloat(info.porcentajeTitulos);
    sumaSubtitulos += parseFloat(info.porcentajeSubtitulos);
    sumaTexto += parseFloat(info.porcentajeTexto);
    contador += 1;

    localStorage.setItem('sumaTodasPaginas', sumaTodasPaginas);
    localStorage.setItem('sumaTitulos', sumaTitulos);
    localStorage.setItem('sumaSubtitulos', sumaSubtitulos);
    localStorage.setItem('sumaTexto', sumaTexto);
    localStorage.setItem('contador', contador);

}

function cargarTotal(){

    var sumaTodasPaginas = parseFloat(localStorage.getItem('sumaTodasPaginas'));
    var sumaTitulos = parseFloat(localStorage.getItem('sumaTitulos'));
    var sumaSubtitulos = parseFloat(localStorage.getItem('sumaSubtitulos'));
    var sumaTexto = parseFloat(localStorage.getItem('sumaTexto'));
    var contador = parseInt(localStorage.getItem('contador'));


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
    parrafo.textContent = sumaTodasPaginas/contador;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% en todas las páginas";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = sumaTitulos/contador;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en titulos";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = sumaSubtitulos/contador;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en subtitulos";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    var divCol = document.createElement('div');
    divCol.classList.add('col');
    var parrafo = document.createElement('p');
    parrafo.textContent = sumaTexto/contador;
    var segundoParrafo = document.createElement('p');
    segundoParrafo.textContent = "% de veces en el texto";
    divCol.appendChild(segundoParrafo);
    divCol.appendChild(parrafo);
    divPrincipal.appendChild(divCol);

    // Agregar todo al body del documento
    document.body.appendChild(divPrincipal);
}