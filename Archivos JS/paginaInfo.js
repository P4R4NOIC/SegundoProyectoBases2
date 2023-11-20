
var info;
            



function cargarPagina(){
    document.getElementById("tituloPagina").textContent = localStorage.getItem("tituloActual");
    pagina = localStorage.getItem("linkActual")
    paginaCodificada = encodeURIComponent(pagina)
    pedirInfo(paginaCodificada);
    
}

function cargarInfo(){
    document.getElementById("titulos").textContent = "Numero de títulos: " + info["canTitulos"];
    document.getElementById("titulosPalabras").textContent = "Palabras distintas por título: " + info["palabrasDifTitulos"];
    document.getElementById("refLinks").textContent = "Referencias con links: " + info["referenciasLink"]; 
    document.getElementById("palabras").textContent = "Palabras distintas: " + info["canPalabras"];
    document.getElementById("palabrasSub").textContent = "Palabras por subtítulo: " + info["palabrasDifSubtitulos"];
    document.getElementById("links").textContent = "Links activos: " + info["canReferencias"];
    document.getElementById("alts").textContent = "Imagenes con Alt: " + info["canImagenes"];
    document.getElementById("palabrasImagen").textContent = "Palabras en imagenes: " + info["canPalabrasImagenes"]
   
    for(var i = 0; i < info["citas"].length; i++){

        var referencia = info["citas"][i]["link"];
        var usos = info["citas"][i]["usos"];
        var label1 = document.createElement("label");
        var label2 = document.createElement("label");

        label1.classList = "textoSimple";
        label1.id = "referencia";
        label1.textContent = "Referencia " + (i+1) + ": " + referencia;

        label2.classList = "textoSimple";
        label2.id = "usos";
        label2.textContent = "Numero de usos: " + usos;

        document.getElementById("referenciasLista").appendChild(label1);
        document.getElementById("referenciasLista").appendChild(label2);

    }

    for(var i = 0; i < info["palabrasComunes"].length; i++){

        var tr = document.createElement("tr");
        var th = document.createElement("th");
        var td = document.createElement("td");

        th.scope = "row";
        th.textContent = info["palabrasComunes"][i]["palabra"];
        var enTitulo = "Si";
        if(info["palabrasComunes"][i]["enTitulo"] === 0){
            enTitulo = "No";
        } 
        td.scope = "row";
        td.textContent = enTitulo;

        tr.appendChild(th);
        tr.appendChild(td);


        document.getElementById("cuerpoTabla").appendChild(tr);
    }


}


function pedirInfo(pagina){
    let datosRecibidos;
    console.log(pagina)
    // Hacer la solicitud GET al servidor
    fetch('http://localhost:3000/datosPorPagina/' + pagina)
    .then(response => {
        if (!response.ok) {
            alert('No se pudo obtener la información del usuario');
        }
        return response.json(); // Parsea la respuesta JSON
    })
    .then(data => {
        // Datos recibidos
        datosRecibidos = data;
        info = datosRecibidos;
        console.log(info);
        cargarInfo();
    })
    .catch(error => {
        console.error('Error al obtener la información del usuario:', error);
    });
}