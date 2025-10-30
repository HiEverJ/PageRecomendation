// Espera a que todo el HTML esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. LÓGICA DE PESTAÑAS (TABS) ---
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabPanels = document.querySelectorAll('.tab-panel');

    tabLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // 1. Obtener el target del panel
            const targetId = link.getAttribute('data-tab-target');
            const targetPanel = document.querySelector(targetId);

            // 2. Quitar 'is-active' de todos los enlaces y paneles
            tabLinks.forEach(l => l.classList.remove('is-active'));
            tabPanels.forEach(p => p.classList.remove('is-active'));

            // 3. Añadir 'is-active' al enlace y panel clicados
            link.classList.add('is-active');
            if (targetPanel) {
                targetPanel.classList.add('is-active');
            }
        });
    });

    // --- 2. LÓGICA DEL "MODAL QUICK VIEW" ---
    const allTriggers = document.querySelectorAll('[data-modal-trigger]');
    const modal = document.getElementById('product-quick-view');
    const closeBtn = document.getElementById('modal-close-btn');
    const body = document.body;

    if (allTriggers.length > 0 && modal && closeBtn) {
        
        // Elementos del modal que se van a rellenar
        const modalImage = document.getElementById('modal-image');
        const modalTag = document.getElementById('modal-tag');
        const modalTitle = document.getElementById('modal-title');
        const modalDescription = document.getElementById('modal-description');
        const modalButtons = document.getElementById('modal-buttons');

        // Función para abrir el modal
        function openModal(e) {
            e.preventDefault();
            const trigger = e.currentTarget;
            
            // 1. Obtener datos del "trigger" (la tarjeta en la que se hizo clic)
            // Corregido: Obtener la 'src' de la etiqueta 'img'
            const imageUrl = trigger.querySelector('.card-image img').src; 
            
            const detailsDiv = trigger.querySelector('.product-full-details');
            if (!detailsDiv) return; // No hacer nada si no hay detalles

            // Corregido: Obtener datos del 'card-content' y 'product-full-details'
            const tag = trigger.querySelector('.card-tag').textContent;
            const title = trigger.querySelector('h3').textContent;
            const description = detailsDiv.querySelector('p').textContent;
            const buttonsHTML = detailsDiv.querySelector('.button-group').innerHTML;
            
            // 3. Rellenar el modal con los datos
            modalImage.src = imageUrl;
            modalTag.textContent = tag;
            modalTitle.textContent = title;
            modalDescription.textContent = description;
            modalButtons.innerHTML = buttonsHTML;

            // 4. Mostrar el modal
            body.classList.add('modal-active');
        }

        // Función para cerrar el modal
        function closeModal() {
            body.classList.remove('modal-active');
        }

        // 5. Asignar los eventos
        allTriggers.forEach(trigger => trigger.addEventListener('click', openModal));
        closeBtn.addEventListener('click', closeModal);
        
        // Cerrar al hacer clic en el fondo (backdrop)
        modal.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-backdrop')) {
                closeModal();
            }
        });
    }

});