document.addEventListener('DOMContentLoaded', () => {

    const body = document.body; // Para controlar el scroll del modal

    // --- LÓGICA DEL MODAL "QUICK VIEW" ---
    // (Aplica a CUALQUIER cosa con [data-modal-trigger],
    // incluyendo .advent-card y .product-featurette)
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
            
            // Extraer datos de los atributos 'data-*'
            const imageUrl = trigger.dataset.image;
            const tag = trigger.dataset.tag;
            const title = trigger.dataset.title;
            const description = trigger.dataset.description;
            const buttonsHTML = trigger.dataset.buttons;
            
            // Rellenar el modal
            modalImage.src = imageUrl;
            modalTag.textContent = tag;
            modalTitle.textContent = title;
            modalDescription.textContent = description;
            modalButtons.innerHTML = buttonsHTML;

            body.classList.add('modal-active'); // Activa el scroll-lock
        }

        function closeModal() {
            body.classList.remove('modal-active'); // Desactiva el scroll-lock
        }

        // Asignar eventos
        modalTriggers.forEach(trigger => trigger.addEventListener('click', openModal));
        closeBtn.addEventListener('click', closeModal);
        
        // Cierra el modal al hacer clic en el fondo
        modal.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-backdrop')) {
                closeModal();
            }
        });

        // Cierra el modal con la tecla Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === "Escape" && body.classList.contains('modal-active')) {
                closeModal();
            }
        });
    }

});