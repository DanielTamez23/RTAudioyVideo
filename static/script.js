document.addEventListener("DOMContentLoaded", function () {
    const galleryContainer = document.querySelector(".image-gallery-container");
    const slides = document.querySelectorAll(".image-slide");
    const totalImages = slides.length;
    const imagesPerView = 3;
    let index = 0;

    // Clonar las primeras 3 imágenes y agregarlas al final (truco de loop infinito)
    for (let i = 0; i < imagesPerView; i++) {
        const clone = slides[i].cloneNode(true);
        galleryContainer.appendChild(clone);
    }

    function moveSlide() {
        index++;

        galleryContainer.style.transition = "transform 1s ease-in-out";
        galleryContainer.style.transform = `translateX(-${(index * 100) / 3}%)`;

        // Cuando llegamos al final, saltamos instantáneamente al inicio sin animación
        if (index === totalImages) {
            setTimeout(() => {
                galleryContainer.style.transition = "none";
                index = 0;
                galleryContainer.style.transform = `translateX(0%)`;
            }, 1000); // Se espera a que termine la animación antes de resetear
        }
    }

    setInterval(moveSlide, 3000); // Cambia cada 3 segundos

    document.addEventListener("DOMContentLoaded", function () {
        const form = document.querySelector("form");  // Seleccionamos el formulario
        const mensajeConfirmacion = document.getElementById("mensaje-confirmacion");
    
        form.addEventListener("submit", function (event) {
            event.preventDefault(); // Evitar que el formulario se envíe y la página se recargue
    
            // Mostrar el mensaje de confirmación
            mensajeConfirmacion.style.display = "block";
    
            // Opcional: Ocultar el mensaje después de 5 segundos
            setTimeout(function () {
                mensajeConfirmacion.style.display = "none";
            }, 5000);
        });
    });
});