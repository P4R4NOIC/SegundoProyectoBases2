var titulosLista;

function pideTitulos(){
  pedirTitulos();
}

function cargaTitulos(){

  for(var i = 0; i < titulosLista.length; i++){
    creaTitulos(titulosLista[i]["titulo_principal"], titulosLista[i]["link"]);
  }

  gsap.utils.toArray('.lineaCompleta').forEach((line, i) => {
 



    const velocidad = 100 
    
    const titulos = line.querySelectorAll("a"),
          tl = carrusel(titulos, -velocidad )
      
    titulos.forEach(titulo => {
      titulo.addEventListener("mouseenter", () => gsap.to(tl, {timeScale: 0, overwrite: true}));
      titulo.addEventListener("mouseleave", () => gsap.to(tl, {timeScale: 1, overwrite: true}));
    });
    
  });


}
  
function creaTitulos(titulo, link){
  var a = document.createElement("a");
  var span = document.createElement("span");

  span.textContent = titulo;
  a.appendChild(span);

  a.href = "paginaInfo.html";
  a.classList = "tituloSolo"
  a.onclick = function(){
      localStorage.setItem("tituloActual", titulo);
      localStorage.setItem("linkActual", link);
  }

  document.getElementById("lineaCompleta").appendChild(a);
}

function carrusel(titulos, velocidad) {
    
    titulos = gsap.utils.toArray(titulos);
    let firstBounds = titulos[0].getBoundingClientRect(),
        lastBounds = titulos[titulos.length - 1].getBoundingClientRect(),
        arriba = firstBounds.top - firstBounds.height - Math.abs(titulos[1].getBoundingClientRect().top - firstBounds.bottom),
        abajo = lastBounds.top,
        distancia = abajo - arriba,
        duration = Math.abs(distancia / velocidad),
        tl = gsap.timeline({repeat: -1}),
        plus = velocidad < 0 ? "-=" : "+=",
        minus = velocidad < 0 ? "+=" : "-=";
    titulos.forEach(el => {
      let bounds = el.getBoundingClientRect(),
          ratio = Math.abs((abajo - bounds.top) / distancia);
      if (velocidad < 0) {
        ratio = 1 - ratio;
      }
      tl.to(el, {
        y: plus + distancia * ratio,
        duration: duration * ratio,
        ease: "none"
      }, 0);
      tl.fromTo(el, {
        y: minus + distancia
      }, {
        y: plus + (1 - ratio) * distancia,
        ease: "none",
        duration: (1 - ratio) * duration,
        immediateRender: false
      }, duration * ratio)
    });
    return tl;
  }

function pedirTitulos(){
    let datosRecibidos;
    // Hacer la solicitud GET al servidor
    fetch('http://localhost:3000/paginas')
    .then(response => {
        if (!response.ok) {
            alert('No se pudo obtener la información del usuario');
        }
        return response.json(); // Parsea la respuesta JSON
    })
    .then(data => {
        // Datos recibidos
        datosRecibidos = data;
        titulosLista = datosRecibidos;
        
       
        cargaTitulos();
    })
    .catch(error => {
        console.error('Error al obtener la información del usuario:', error);
    });
}