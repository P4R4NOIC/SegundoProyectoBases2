
var info = {"numTitulos":"10",
            "palabrasTitulo":"7",
            "referenciasLinks":"19",
            "referencias":[{
                "referencia":"https://es.wikipedia.org/wiki/Minecraft", "usos":"30"},
                {"referencia":"https://es.wikipedia.org/wiki/Minecraft2", "usos":"31"},
                {"referencia":"https://es.wikipedia.org/wiki/Minecraft3", "usos":"32"}
            ],
            "palabrasNum":"5000",
            "palabrasSub":"800",
            "links":"9",
            "imagenesAlt":"56",
            "palabras":[{"palabra":"super", "titulo":"No"}]}
            



function cargarPagina(){
    document.getElementById("tituloPagina").textContent = localStorage.getItem("tituloActual")
    cargarInfo();
}

function cargarInfo(){
    document.getElementById("titulos").textContent = "Numero de títulos: " + info["numTitulos"];
    document.getElementById("titulosPalabras").textContent = "Palabras distintas por título: " + info["palabrasTitulo"];
    document.getElementById("refLinks").textContent = "Referencias con links: " + info["referenciasLinks"]; 
    document.getElementById("palabras").textContent = "Palabras distintas: " + info["palabrasNum"];
    document.getElementById("palabrasSub").textContent = "Palabras por subtítulo: " + info["palabrasSub"];
    document.getElementById("links").textContent = "Links activos: " + info["links"];
    document.getElementById("alts").textContent = "Imagenes con Alt: " + info["imagenesAlt"];
   
    for(var i = 0; i < info["referencias"].length; i++){

        var referencia = info["referencias"][i]["referencia"];
        var usos = info["referencias"][i]["usos"];
        var label1 = document.createElement("label");
        var label2 = document.createElement("label");

        label1.classList = "textoSimple";
        label1.id = "referencia";
        label1.textContent = "Referencia " + (i+1) + ": " + referencia;

        label2.classList = "textoSimple";
        label2.id = "usos";
        label2.textContent = "Numero de usos: " + usos;

        document.getElementById("derecha").appendChild(label1);
        document.getElementById("derecha").appendChild(label2);

    }

    for(var i = 0; i < info["palabras"].length; i++){

        var tr = document.createElement("tr");
        var th = document.createElement("th");
        var td = document.createElement("td");

        th.scope = "row";
        th.textContent = info["palabras"][i]["palabra"];

        td.scope = "row";
        td.textContent = info["palabras"][i]["titulo"]

        tr.appendChild(th);
        tr.appendChild(td);


        document.getElementById("cuerpoTabla").appendChild(tr);
    }


}
