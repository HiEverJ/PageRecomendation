// Espera a que todo el HTML esté cargado
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. LÓGICA DEL EXPANDER ---
    const allTriggers = document.querySelectorAll('[data-expander-trigger]');
    const expander = document.getElementById('product-expander');
    const closeBtn = document.getElementById('expander-close-btn');
    const body = document.body;

    if (allTriggers.length > 0 && expander && closeBtn) {
        
        // Elementos del expander que se van a rellenar
        const expanderImage = document.getElementById('expander-image');
        const expanderTag = document.getElementById('expander-tag');
        const expanderTitle = document.getElementById('expander-title');
        const expanderDescription = document.getElementById('expander-description');
        const expanderButtons = document.getElementById('expander-buttons');

        // Función para abrir el expander
        function openExpander(e) {
            e.preventDefault();
            const trigger = e.currentTarget;
            
            // 1. Obtener datos del "trigger" (la tarjeta en la que se hizo clic)
            // Obtener la imagen de fondo de la tarjeta
            const imageStyle = trigger.style.backgroundImage;
            const imageUrl = imageStyle.slice(5, -2); // Extrae la URL del 'url("...")'
            
            const tag = trigger.querySelector('.card-tag').textContent;
            const title = trigger.querySelector('h3').textContent;
            
            // 2. Buscar descripción y botones en el div oculto
            const detailsDiv = trigger.querySelector('.product-full-details');
            let description = 'No hay descripción disponible.'; // Default
            let buttonsHTML = '';

            if (detailsDiv) {
                const longDesc = detailsDiv.querySelector('p');
                if (longDesc) {
                    description = longDesc.textContent;
                }
                const buttonGroup = detailsDiv.querySelector('.button-group');
                if (buttonGroup) {
                    buttonsHTML = buttonGroup.innerHTML;
                }
            }
            
            // 3. Rellenar el expander con los datos
            expanderImage.src = imageUrl;
            expanderTag.textContent = tag;
            expanderTitle.textContent = title;
            expanderDescription.textContent = description;
            expanderButtons.innerHTML = buttonsHTML;

            // 4. Mostrar el expander
            body.classList.add('expander-active');
        }

        // Función para cerrar el expander
        function closeExpander() {
            body.classList.remove('expander-active');
        }

        // 5. Asignar los eventos
        allTriggers.forEach(trigger => trigger.addEventListener('click', openExpander));
        closeBtn.addEventListener('click', closeExpander);
        
        // Opcional: Cerrar al hacer clic en el fondo oscuro
        expander.addEventListener('click', (e) => {
            if (e.target === expander) {
                closeExpander();
            }
        });
    }

    // (No hay lógica de Sticky Nav en esta página)

});