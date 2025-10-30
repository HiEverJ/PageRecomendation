// Espera a que todo el HTML esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. LÓGICA DE PESTAÑAS (TABS) CON CAMBIO DE COLOR ---
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabPanels = document.querySelectorAll('.tab-panel');

    // Función para manejar el cambio de color
    function setActiveTab(link) {
        // 1. Obtener el target del panel y el nuevo color
        const targetId = link.getAttribute('data-tab-target');
        const targetPanel = document.querySelector(targetId);
        const newAccentColor = link.getAttribute('data-color-accent');
        const newAccentColorRgb = link.getAttribute('data-color-accent-rgb');
        const newBgColor = link.getAttribute('data-color-bg'); // ¡Nueva línea!

        // 2. Quitar 'is-active' de todos los enlaces y paneles
        tabLinks.forEach(l => l.classList.remove('is-active'));
        tabPanels.forEach(p => p.classList.remove('is-active'));

        // 3. Añadir 'is-active' al enlace y panel clicados
        link.classList.add('is-active');
        if (targetPanel) {
            targetPanel.classList.add('is-active');
        }

        // 4. Aplicar el nuevo color de acento Y FONDO al contenedor
        if (contentWrapper && newAccentColor && newAccentColorRgb && newBgColor) {
            contentWrapper.style.setProperty('--active-accent', newAccentColor);
            contentWrapper.style.setProperty('--active-accent-rgb', newAccentColorRgb);
            
            // ¡NUEVO! Aplicar el fondo tintado al panel
            if (targetPanel) {
                targetPanel.style.backgroundColor = newBgColor;
            }
            
            // 5. Actualizar el color del glitch del Hero H1
            // Seleccionamos el H1 (no el pseudo-elemento)
            const heroH1 = document.querySelector('.hero-glitch h1');
            if (heroH1) {
                // Establecemos variables que el CSS SÍ puede leer
                heroH1.style.setProperty('--glitch-color-1', newAccentColor);
                // Usamos un color secundario para el 'after' (puedes cambiar esta lógica)
                heroH1.style.setProperty('--glitch-color-2', 'var(--gamer-accent-alt-glitch)'); 
            }
        }
    }

    // Asignar el evento click a cada enlace de pestaña
    tabLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            setActiveTab(link);
        });
    });

    // --- Asegurarse de que el color se aplique al cargar la página ---
    const activeTabOnLoad = document.querySelector('.tab-link.is-active');
    if (activeTabOnLoad) {
        setActiveTab(activeTabOnLoad);
    }

    // --- 2. LÓGICA DEL MODAL "QUICK VIEW" (para tarjetas tipo Gamer) ---
    const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
    const modal = document.getElementById('product-quick-view');
    const closeBtn = document.getElementById('modal-close-btn');

    if (modalTriggers.length > 0 && modal && closeBtn) {
        
        const modalImage = document.getElementById('modal-image');
        const modalTag = document.getElementById('modal-tag');
        const modalTitle = document.getElementById('modal-title');
        const modalDescription = document.getElementById('modal-description');
        const modalButtons = document.getElementById('modal-buttons');

        function openModal(e) {
            e.preventDefault();
            const trigger = e.currentTarget;
            
            const imageUrl = trigger.querySelector('.card-image img').src; 
            const detailsDiv = trigger.querySelector('.product-full-details');
            if (!detailsDiv) return; 

            const tag = trigger.querySelector('.card-tag').textContent;
            const title = trigger.querySelector('h3').textContent;
            const description = detailsDiv.querySelector('p').textContent;
            const buttonsHTML = detailsDiv.querySelector('.button-group').innerHTML;
            
            modalImage.src = imageUrl;
            modalTag.textContent = tag;
            modalTitle.textContent = title;
            modalDescription.textContent = description;
            modalButtons.innerHTML = buttonsHTML;

            body.classList.add('modal-active');
        }

        function closeModal() {
            body.classList.remove('modal-active');
        }

        modalTriggers.forEach(trigger => trigger.addEventListener('click', openModal));
        closeBtn.addEventListener('click', closeModal);
        
        modal.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-backdrop')) {
                closeModal();
            }
        });
    }

    // --- 3. LÓGICA DEL ACORDEÓN (para tarjetas tipo Limpieza) ---
    const allEntries = document.querySelectorAll('[data-accordion-trigger]');
    allEntries.forEach(entry => {
        const trigger = entry.querySelector('.entry-trigger');
        if (trigger) {
            trigger.addEventListener('click', (e) => {
                e.preventDefault(); 
                const isAlreadyActive = entry.classList.contains('is-active');
                
                // Cierra todos los acordeones DENTRO DEL MISMO PANEL
                const parentPanel = entry.closest('.tab-panel');
                if (parentPanel) {
                    parentPanel.querySelectorAll('[data-accordion-trigger]').forEach(e => {
                        if (e !== entry) {
                            e.classList.remove('is-active');
                        }
                    });
                }
                
                // Abre o cierra el actual
                entry.classList.toggle('is-active', !isAlreadyActive);
            });
        }
    });

});