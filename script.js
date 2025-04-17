// Efecto de escritura en el título
const titulo = document.getElementById("titulo");
const texto = "Juan Romero";
let i = 0;

function escribir() {
  if (i < texto.length) {
    titulo.textContent = texto.slice(0, i + 1);
    i++;
    setTimeout(escribir, 150);
  }
}
escribir();

// Animaciones al hacer scroll
const animables = document.querySelectorAll(".fade-in");

function mostrarAnimados() {
  animables.forEach((el) => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 100) {
      el.classList.add("visible");
    }
  });
}
window.addEventListener("scroll", mostrarAnimados);
window.addEventListener("load", mostrarAnimados);

// Botón volver arriba
const btnArriba = document.getElementById("btn-arriba");

window.addEventListener("scroll", () => {
  if (window.scrollY > 200) {
    btnArriba.style.display = "block";
  } else {
    btnArriba.style.display = "none";
  }
});

btnArriba.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

// Lightbox
const imagenes = document.querySelectorAll(".img-galeria");
const lightbox = document.getElementById("lightbox");
const imgAmpliada = document.getElementById("img-ampliada");
const cerrar = document.getElementById("cerrar");

imagenes.forEach((img) => {
  img.addEventListener("click", () => {
    lightbox.style.display = "block";
    imgAmpliada.src = img.src;
  });
});

cerrar.addEventListener("click", () => {
  lightbox.style.display = "none";
});
// Lightbox para imagen de perfil
const imgPerfil = document.querySelector(".perfil-click");
const lightboxPerfil = document.getElementById("lightbox-perfil");
const imgPerfilAmpliada = document.getElementById("img-perfil-ampliada");
const cerrarPerfil = document.getElementById("cerrar-perfil");

if (imgPerfil && lightboxPerfil && imgPerfilAmpliada && cerrarPerfil) {
  imgPerfil.addEventListener("click", () => {
    lightboxPerfil.style.display = "block";
    imgPerfilAmpliada.src = imgPerfil.src;
  });

  cerrarPerfil.addEventListener("click", () => {
    lightboxPerfil.style.display = "none";
  });

  // Cerrar si hacen clic fuera de la imagen
  lightboxPerfil.addEventListener("click", (e) => {
    if (e.target === lightboxPerfil) {
      lightboxPerfil.style.display = "none";
    }
  });
}

