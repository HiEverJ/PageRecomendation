// Espera a que todo el HTML esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // Selección de elementos del DOM
    const hamburgerBtn = document.getElementById('hamburger-btn');
    const mainNav = document.getElementById('main-nav');

    // Verificar que los elementos existen
    if (hamburgerBtn && mainNav) {
        
        // Añadir 'listener' al botón
        hamburgerBtn.addEventListener('click', () => {
            // Alterna la clase 'is-active' en el botón (para la anim. 'X')
            hamburgerBtn.classList.toggle('is-active');
            
            // Alterna la clase 'is-active' en el menú (para mostrar/ocultar)
            mainNav.classList.toggle('is-active');
        });
    }

});