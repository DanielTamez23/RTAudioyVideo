// Función para mostrar/ocultar el botón de scroll hacia arriba
window.onscroll = function() {
    var scrollButton = document.querySelector('.scroll-to-top');
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        scrollButton.style.display = "block";  // Muestra el botón cuando se hace scroll
    } else {
        scrollButton.style.display = "none";  // Oculta el botón cuando se está en la parte superior
    }
};

// Función que se ejecuta al hacer clic en el botón de "scroll to top"
function scrollToTop() {
    document.querySelector('.header').scrollIntoView({ behavior: 'smooth' });
}

// Función para alternar el menú hamburguesa
function toggleMenu() {
    const menu = document.querySelector('.nav-links');
    menu.classList.toggle('active');
    const bars = document.querySelector('.menu-icon');
    bars.classList.toggle('active');
}

// Animación para el cambio de color de los enlaces del menú al hacer hover
const menuLinks = document.querySelectorAll('.nav-links a');
menuLinks.forEach(link => {
    link.addEventListener('mouseenter', () => {
        link.style.transition = 'color 0.3s';
        link.style.color = '#f1c40f';  // Cambiar el color del enlace al hacer hover
    });
    link.addEventListener('mouseleave', () => {
        link.style.color = '';  // Restaurar color original
    });
});

// Implementación del carrusel de imágenes
let currentSlide = 0;
const slides = document.querySelectorAll('.image-slide');
const totalSlides = slides.length;
const carouselContainer = document.querySelector('.carousel-container');  // Contenedor del carrusel

// Función para mostrar una imagen del carrusel
function showSlide(index) {
    if (index >= totalSlides) currentSlide = 0;
    if (index < 0) currentSlide = totalSlides - 1;

    // Mover el contenedor del carrusel para mostrar las imágenes de manera fluida
    const offset = -currentSlide * 33.333;  // Desplazamos el carrusel de 1/3 de su ancho cada vez
    carouselContainer.style.transition = 'transform 0.5s ease';  // Hacemos que el movimiento sea suave
    carouselContainer.style.transform = `translateX(${offset}%)`;
}

// Función para avanzar al siguiente slide
function nextSlide() {
    currentSlide++;
    if (currentSlide >= totalSlides - 2) {  // Hacer que el carrusel vuelva al principio cuando llegue al final
        currentSlide = 0;
    }
    showSlide(currentSlide);
}

// Función para retroceder al slide anterior
function prevSlide() {
    currentSlide--;
    if (currentSlide < 0) {  // Hacer que el carrusel vuelva al final cuando llegue al principio
        currentSlide = totalSlides - 3;
    }
    showSlide(currentSlide);
}

// Mostrar la primera imagen
showSlide(currentSlide);

// Intervalo de 3 segundos para el carrusel de imágenes
setInterval(nextSlide, 3000);

// Agregar soporte para swipe (móviles) con movimiento libre
let startX;
let endX;
let touchStartTime;
let touchEndTime;

const carousel = document.querySelector('.carousel');  // Contenedor del carrusel

carousel.addEventListener('touchstart', (e) => {
    startX = e.touches[0].pageX;  // Capturar la posición inicial del toque
    touchStartTime = Date.now();  // Capturamos el tiempo de inicio del toque
});

carousel.addEventListener('touchmove', (e) => {
    endX = e.touches[0].pageX;  // Capturar la posición del toque en movimiento
    const diffX = startX - endX;  // Distancia recorrida en X
    const offset = -currentSlide * 33.333 + (diffX / window.innerWidth) * 100;  // Ajuste proporcional

    // Mover el carrusel de acuerdo al movimiento
    carouselContainer.style.transition = 'none';  // Sin transición para un movimiento suave
    carouselContainer.style.transform = `translateX(${offset}%)`;
});

carousel.addEventListener('touchend', (e) => {
    touchEndTime = Date.now();  // Capturamos el tiempo final del toque
    const diffX = startX - endX;  // Distancia recorrida en X
    const swipeDuration = touchEndTime - touchStartTime;  // Duración del toque

    // Si el swipe fue suficientemente rápido y largo, avanzar o retroceder según el movimiento
    if (Math.abs(diffX) > window.innerWidth / 4 || swipeDuration < 200) {
        if (diffX > 0) {
            nextSlide();  // Deslizar a la siguiente imagen
        } else {
            prevSlide();  // Deslizar a la imagen anterior
        }
    } else {
        showSlide(currentSlide);  // Mantener la posición actual si no fue un swipe lo suficientemente fuerte
    }
});

// Asegurarse de que las imágenes se muestren correctamente
const images = document.querySelectorAll('.image-slide');
images.forEach(image => {
    image.style.width = '33.333%';  // Mostrar tres imágenes a la vez
    image.style.height = 'auto';  // Mantener la proporción de las imágenes
});

// Implementar la animación para la barra de progreso de carga
const progressBar = document.querySelector('.progress-bar');
let progress = 0;

function updateProgressBar() {
    progress += 1;
    progressBar.style.width = progress + '%';
    if (progress < 100) {
        setTimeout(updateProgressBar, 50);
    }
}
document.addEventListener('DOMContentLoaded', updateProgressBar);

// Cambio de color de los enlaces cuando se hace scroll
window.addEventListener('scroll', () => {
    let menuLinks = document.querySelectorAll('.menu-container a');
    menuLinks.forEach(link => {
        if (link.getBoundingClientRect().top < window.innerHeight && link.getBoundingClientRect().bottom > 0) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

// Mostrar y ocultar las secciones del menú al hacer scroll
const sections = document.querySelectorAll('.servicios-container, .image-section, .empresa-seccion, .historia');
const threshold = window.innerHeight * 0.5;

function checkVisibility() {
    sections.forEach(section => {
        if (section.getBoundingClientRect().top < threshold) {
            section.classList.add('visible');
        } else {
            section.classList.remove('visible');
        }
    });
}

window.addEventListener('scroll', checkVisibility);
checkVisibility();

// Función para el control de la animación de "Reparación" (con el color de fondo)
const ctaLinks = document.querySelectorAll('.cta-link');
ctaLinks.forEach(link => {
    link.addEventListener('mouseenter', () => {
        link.style.backgroundColor = '#f39c12';
        link.style.transition = 'background-color 0.3s ease';
    });
    link.addEventListener('mouseleave', () => {
        link.style.backgroundColor = '';
    });
});

// Función para manejar el formulario de contacto
const form = document.querySelector('form');
const formButton = form.querySelector('button');
formButton.addEventListener('click', (event) => {
    event.preventDefault();  // Prevenir el envío del formulario por defecto
    const nombre = form.querySelector('#nombre').value;
    const categoria = form.querySelector('#categoria').value;
    const marca = form.querySelector('#marca').value;
    const descripcion = form.querySelector('#descripcion').value;
    const whatsapp = form.querySelector('#whatsapp').value;
    const correo = form.querySelector('#correo').value;

    if (nombre && categoria && marca && descripcion && whatsapp && correo) {
        // Simulando el proceso de envío
        const mensajeConfirmacion = document.getElementById('mensaje-confirmacion');
        mensajeConfirmacion.style.display = 'block';
    } else {
        alert('Por favor, llena todos los campos del formulario.');
    }
});

// Establecer el comportamiento del icono de WhatsApp
const whatsappIcon = document.querySelector('#whatsapp');
whatsappIcon.addEventListener('click', () => {
    alert('Redirigiendo al WhatsApp...');
});

// Establecer el comportamiento del icono de correo
const emailIcon = document.querySelector('#email');
emailIcon.addEventListener('click', () => {
    alert('Redirigiendo al correo...');
});

// Establecer el comportamiento del icono de teléfono
const phoneIcon = document.querySelector('#phone');
phoneIcon.addEventListener('click', () => {
    alert('Redirigiendo al teléfono...');
});

// Añadir animación de aparición cuando se cargan los contenidos
const appearElements = document.querySelectorAll('.empresa-seccion, .historia, .ubicacion-container, .servicios-container');
appearElements.forEach(el => {
    el.classList.add('fade');
});
