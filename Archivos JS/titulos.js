var titulos = ["Navidad", "Fernando VII de España", "Revolución francesa", "Segunda Guerra Mundial", "Alan Turing", "El uso del conocimiento en la sociedad"]



function cargaTitulos(){
  for(var i = 0; i < titulos.length; i++){
    creaTitulos(titulos[i]);
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
  
function creaTitulos(titulo){
  var a = document.createElement("a");
  var span = document.createElement("span");

  span.textContent = titulo;
  a.appendChild(span);

  a.href = "paginaInfo.html";
  a.classList = "tituloSolo"
  a.onclick = function(){
      localStorage.setItem("tituloActual", titulo);
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

