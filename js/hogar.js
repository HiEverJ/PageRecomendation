// Espera a que todo el HTML esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // Seleccionamos TODAS las cuadrículas interactivas de la página
    const allGrids = document.querySelectorAll('.product-grid-small');

    // Procesamos cada cuadrícula por separado
    allGrids.forEach(grid => {
        const cards = grid.querySelectorAll('.product-card-small');

        cards.forEach(card => {
            card.addEventListener('click', () => {
                
                // 1. Comprobar si la tarjeta en la que se hizo clic ya está activa
                const isAlreadyActive = card.classList.contains('is-active');

                // 2. Primero, quitar la clase 'is-active' de TODAS las tarjetas en ESTA cuadrícula
                cards.forEach(c => c.classList.remove('is-active'));
                
                // 3. Quitar la clase 'grid-is-active' del contenedor de la cuadrícula
                grid.classList.remove('grid-is-active');

                // 4. Si la tarjeta no estaba activa, la activamos (y el grid)
                if (!isAlreadyActive) {
                    card.classList.add('is-active');
                    grid.classList.add('grid-is-active');
                }
                // Si ya estaba activa, los pasos 2 y 3 ya la han cerrado.
            });
        });
    });

});