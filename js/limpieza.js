// Espera a que todo el HTML esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. LÓGICA DEL ACORDEÓN (para tarjetas tipo Limpieza) ---
    const allEntries = document.querySelectorAll('[data-accordion-trigger]');
    allEntries.forEach(entry => {
        const trigger = entry.querySelector('.entry-trigger');
        if (trigger) {
            trigger.addEventListener('click', (e) => {
                e.preventDefault(); 
                const isAlreadyActive = entry.classList.contains('is-active');
                
                // Cierra todos los acordeones
                allEntries.forEach(e => e.classList.remove('is-active'));
                
                if (!isAlreadyActive) {
                    entry.classList.add('is-active');
                }
            });
        }
    });

    // --- 2. LÓGICA DEL STICKY NAV (para el menú lateral) ---
    const stickyNavLinks = document.querySelectorAll('.sticky-nav a');
    const contentSections = document.querySelectorAll('.content-section');
    if (stickyNavLinks.length > 0 && contentSections.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    stickyNavLinks.forEach(link => link.classList.remove('is-active'));
                    const id = entry.target.id;
                    const activeLink = document.querySelector(`.sticky-nav a[href="#${id}"]`);
                    if (activeLink) {
                        activeLink.classList.add('is-active');
                    }
                }
            });
        }, { 
            rootMargin: '-30% 0px -60% 0px' 
        });
        contentSections.forEach(section => observer.observe(section));
    }

    // --- 3. LÓGICA DEL MODAL "QUICK VIEW" (para tarjetas tipo Gamer) ---
    const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
    const modal = document.getElementById('product-quick-view');
    const closeBtn = document.getElementById('modal-close-btn');
    const body = document.body;

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

});