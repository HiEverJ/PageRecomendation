// Espera a que todo el HTML esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. LÓGICA DEL ACORDEÓN (Para que las tarjetas se abran) ---
    
    // Selecciona todos los articles que son acordeones
    const allEntries = document.querySelectorAll('[data-accordion-trigger]');

    allEntries.forEach(entry => {
        // El botón clicable es el div .entry-trigger
        const trigger = entry.querySelector('.entry-trigger');
        
        if (trigger) {
            trigger.addEventListener('click', (e) => {
                e.preventDefault(); // Previene cualquier comportamiento por defecto
                
                // Comprobar si el que se ha clicado ya está activo
                const isAlreadyActive = entry.classList.contains('is-active');
                
                // Primero, cerrar TODOS los acordeones
                allEntries.forEach(e => e.classList.remove('is-active'));
                
                // Si NO estaba activo, ábrelo.
                // Si SÍ estaba activo, el paso anterior ya lo ha cerrado.
                if (!isAlreadyActive) {
                    entry.classList.add('is-active');
                }
            });
        }
    });

    // --- 2. LÓGICA DEL STICKY NAV (Para que se actualice el menú) ---
    const stickyNavLinks = document.querySelectorAll('.sticky-nav a');
    const contentSections = document.querySelectorAll('.content-section');

    if (stickyNavLinks.length > 0 && contentSections.length > 0) {
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                // Si la sección está visible (intersectando)
                if (entry.isIntersecting) {
                    // 1. Quitar 'is-active' de todos los enlaces
                    stickyNavLinks.forEach(link => link.classList.remove('is-active'));
                    
                    // 2. Añadir 'is-active' al enlace correspondiente
                    const id = entry.target.id;
                    const activeLink = document.querySelector(`.sticky-nav a[href="#${id}"]`);
                    if (activeLink) {
                        activeLink.classList.add('is-active');
                    }
                }
            });
        }, { 
            // Ajusta estos márgenes para "sentir" la sección
            // -30% (top): se activa cuando la sección ha pasado el 30% superior de la pantalla
            // -60% (bottom): se desactiva cuando la sección está por debajo del 60% de la pantalla
            rootMargin: '-30% 0px -60% 0px' 
        });

        // Observar cada sección de contenido
        contentSections.forEach(section => observer.observe(section));
    }
});