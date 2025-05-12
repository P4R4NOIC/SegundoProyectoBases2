var info;

           

function cargarPagina(){
    document.getElementById("tituloPagina").textContent = "Información General"
    pedirInfo();
    
}



function cargarInfo(){
    document.getElementById("titulos").textContent = "Numero de títulos en General: " + info["cantidadTitulos"];
    document.getElementById("titulosPalabras").textContent = "Palabras distintas por título en General: " + info["palabrasxTitulo"];
    document.getElementById("refLinks").textContent = "Referencias con links en General: " + info["cantitadReferencias"]; 
    document.getElementById("palabras").textContent = "Palabras distintas en General: " + info["cantidadPalabras"];
    document.getElementById("palabrasSub").textContent = "Palabras por subtítulo en General: " + info["palabrasxSubtitulo"];
    document.getElementById("links").textContent = "Links activos en General: " + info["referenciasActivas"];
    document.getElementById("alts").textContent = "Imagenes con Alt en General: " + info["cantidadAltImagenes"];


}


function pedirInfo(){
    let datosRecibidos;
    // Hacer la solicitud GET al servidor
    fetch('http://localhost:3000/generales')
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