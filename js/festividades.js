// Espera a que todo el HTML esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. LÓGICA DE "DESENVOLVER REGALO" (ACORDEÓN) ---
    // Seleccionamos todas las tarjetas que tienen el atributo 'data-gift-card'
    const allGiftCards = document.querySelectorAll('[data-gift-card]');

    allGiftCards.forEach(card => {
        // El "gatillo" para abrir/cerrar es toda la vista previa
        const trigger = card.querySelector('.gift-preview'); 
        const toggleBtn = card.querySelector('.gift-toggle-btn');

        if (trigger) {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                // Comprueba si la tarjeta en la que se hizo clic ya estaba abierta
                const isAlreadyOpen = card.classList.contains('is-open');

                // --- Lógica de Acordeón ---
                // 1. Primero, cierra TODAS las tarjetas
                allGiftCards.forEach(c => {
                    c.classList.remove('is-open');
                    const btn = c.querySelector('.gift-toggle-btn');
                    if (btn) btn.textContent = 'Ver Detalles ▼';
                });

                // 2. Si la tarjeta no estaba abierta, ábrela.
                if (!isAlreadyOpen) {
                    card.classList.add('is-open');
                    if (toggleBtn) toggleBtn.textContent = 'Cerrar Detalles ▲';
                }
                // Si ya estaba abierta, el paso 1 ya la cerró.
            });
        }
    });

    // --- 2. LÓGICA DEL STICKY NAV (Marcar activo al hacer scroll) ---
    const stickyNav = document.getElementById('festive-nav');
    const stickyNavLinks = document.querySelectorAll('.festive-nav-wrapper a');
    const contentSections = document.querySelectorAll('.category-section');
    const header = document.querySelector('.main-header');

    if (stickyNav && stickyNavLinks.length > 0 && contentSections.length > 0 && header) {
        
        // Calcular el offset para el Intersection Observer
        // Restamos la altura del header fijo y la del nav fijo para que la sección
        // se marque como "activa" justo cuando pasa por debajo del nav.
        const headerHeight = header.offsetHeight;
        const navHeight = stickyNav.offsetHeight;
        // Un margen extra de 30px para que se active un poco antes de llegar al borde
        const offset = -(headerHeight + navHeight + 30); 

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                // Si la sección está entrando en la pantalla (visible)
                if (entry.isIntersecting) {
                    const id = entry.target.id;
                    
                    // Quitar 'is-active' de todos los enlaces
                    stickyNavLinks.forEach(link => link.classList.remove('is-active'));
                    
                    // Añadir 'is-active' al enlace correspondiente
                    const activeLink = document.querySelector(`.festive-nav-wrapper a[href="#${id}"]`);
                    if (activeLink) {
                        activeLink.classList.add('is-active');
                    }
                }
            });
        }, { 
            // Definimos el margen superior negativo para el "trigger"
            rootMargin: `${offset}px 0px -60% 0px` 
        });

        // Observar cada sección de contenido
        contentSections.forEach(section => observer.observe(section));

        // --- Lógica de Clic para Scroll Suave ---
        stickyNavLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const href = link.getAttribute('href');
                const targetElement = document.querySelector(href);
                
                if (targetElement) {
                    // Calculamos la posición exacta a la que hacer scroll
                    // Posición del elemento + scroll actual - altura del header - altura del nav - 10px de margen
                    const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY;
                    const offsetPosition = targetPosition - headerHeight - navHeight - 10;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth' // Scroll suave
                    });

                    // Opcional: Actualizar el estado activo inmediatamente al hacer clic
                    // (El observer lo haría al terminar el scroll, pero esto es más rápido)
                    stickyNavLinks.forEach(l => l.classList.remove('is-active'));
                    link.classList.add('is-active');
                }
            });
        });
    }

});