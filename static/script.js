document.addEventListener("DOMContentLoaded", function () {
    // ----- Carrusel de imágenes -----
    const galleryContainer = document.querySelector(".image-gallery-container");
    let slides = document.querySelectorAll(".image-slide");
    let totalImages = slides.length;
    let index = 0;
    let imagesPerView = getImagesPerView();
    let isMobile = window.innerWidth < 768;  // Detecta si es móvil

    // Asegúrate de que el ancho de cada imagen sea proporcional al número de imágenes por vista
    function updateImageWidth() {
        slides.forEach(slide => {
            slide.style.flex = `0 0 ${100 / imagesPerView}%`;
        });
    }

    // Clonar las primeras imágenes y agregarlas al final para loop infinito
    for (let i = 0; i < imagesPerView; i++) {
        const clone = slides[i].cloneNode(true);
        galleryContainer.appendChild(clone);
    }

    function getImagesPerView() {
        // Ajusta el número de imágenes visibles según el tamaño de la pantalla
        if (window.innerWidth < 768) {
            return 1;  // En pantallas pequeñas, 1 imagen por vista
        } else if (window.innerWidth < 1024) {
            return 2;  // En pantallas medianas, 2 imágenes por vista
        } else {
            return 3;  // En pantallas grandes, 3 imágenes por vista
        }
    }

    function moveSlide() {
        index++;
        galleryContainer.style.transition = "transform 1s ease-in-out";
        galleryContainer.style.transform = `translateX(-${(index * 100) / imagesPerView}%)`;

        if (index === totalImages) {
            setTimeout(() => {
                galleryContainer.style.transition = "none";
                index = 0;
                galleryContainer.style.transform = `translateX(0%)`;
            }, 1000);
        }
    }

    let autoSlide = setInterval(moveSlide, 3000);

    // ----- Soporte para deslizar con el dedo en dispositivos móviles -----
    let touchStartX = 0;
    let touchEndX = 0;
    let touchMoveX = 0;
    let startTranslateX = 0;

    // Si es móvil, habilitar el swipe
    if (isMobile) {
        galleryContainer.addEventListener("touchstart", function (e) {
            touchStartX = e.changedTouches[0].screenX;
            startTranslateX = parseInt(galleryContainer.style.transform.replace('translateX(', '').replace('%)', '')) || 0; // Guardar la posición actual
            galleryContainer.style.transition = "none";  // Desactivar transición al comenzar a deslizar
        });

        galleryContainer.addEventListener("touchmove", function (e) {
            touchMoveX = e.changedTouches[0].screenX - touchStartX; // Detecta el movimiento
            galleryContainer.style.transform = `translateX(${startTranslateX + (touchMoveX / imagesPerView)}%)`; // Desplazar el carrusel mientras se mueve
        });

        galleryContainer.addEventListener("touchend", function (e) {
            touchEndX = e.changedTouches[0].screenX;
            handleGesture();
        });

        function handleGesture() {
            const swipeThreshold = 50; // Mínima distancia para considerar como swipe

            // Movimiento rápido hacia la izquierda (siguiente)
            if (touchEndX < touchStartX - swipeThreshold) {
                clearInterval(autoSlide);
                index++;
                if (index >= totalImages) {
                    index = 0;
                }
            } 
            // Movimiento rápido hacia la derecha (anterior)
            else if (touchEndX > touchStartX + swipeThreshold) {
                clearInterval(autoSlide);
                index--;
                if (index < 0) {
                    index = totalImages - 1;
                }
            }

            // Finaliza el movimiento con una transición suave
            galleryContainer.style.transition = "transform 1s ease-in-out";
            galleryContainer.style.transform = `translateX(-${(index * 100) / imagesPerView}%)`;

            // Reinicia el slider automático después de un swipe
            autoSlide = setInterval(moveSlide, 3000);
        }
    }

    // ----- Mensaje de confirmación del formulario -----
    const form = document.querySelector("form");
    const mensajeConfirmacion = document.getElementById("mensaje-confirmacion");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        mensajeConfirmacion.style.display = "block";

        setTimeout(function () {
            mensajeConfirmacion.style.display = "none";
        }, 5000);
    });

    // Llama a la función que ajusta las imágenes por vista al cambiar el tamaño de la ventana
    updateImageWidth();
    window.addEventListener("resize", function() {
        imagesPerView = getImagesPerView();
        isMobile = window.innerWidth < 768;  // Actualiza la detección de móvil
        updateImageWidth();
    });
});
