var info = {"numTitulos":"10",
            "palabrasTitulo":"7",
            "referenciasLinks":"19",
            "palabrasNum":"5000",
            "palabrasSub":"800",
            "links":"9",
            "imagenesAlt":"56"}

function cargarPagina(){
    document.getElementById("tituloPagina").textContent = "Información General"
    cargarInfo();
}



function cargarInfo(){
    document.getElementById("titulos").textContent = "Numero de títulos en General: " + info["numTitulos"];
    document.getElementById("titulosPalabras").textContent = "Palabras distintas por título en General: " + info["palabrasTitulo"];
    document.getElementById("refLinks").textContent = "Referencias con links en General: " + info["referenciasLinks"]; 
    document.getElementById("palabras").textContent = "Palabras distintas en General: " + info["palabrasNum"];
    document.getElementById("palabrasSub").textContent = "Palabras por subtítulo en General: " + info["palabrasSub"];
    document.getElementById("links").textContent = "Links activos en General: " + info["links"];
    document.getElementById("alts").textContent = "Imagenes con Alt en General: " + info["imagenesAlt"];


}