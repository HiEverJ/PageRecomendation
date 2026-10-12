# Reglas del propietario para este proyecto

Estas restricciones se aplican a las correcciones actuales y futuras mientras
el propietario no las cambie expresamente:

- NO crear scripts de prueba.
- NO simular validaciones visuales.
- NO ejecutar pruebas visuales ni pruebas de pantalla.
- NO crear sandboxes ni entornos de prueba aislados.
- No afirmar que se probó lo que no se probó.
- No desplegar a producción sin autorización explícita.

Trabajar en este repositorio real. Se permite leer y revisar código y diferencias,
editar archivos y ejecutar el generador de HTML existente para producir el sitio.
La generación no es una prueba y no debe presentarse como tal.

Conservar búsqueda, filtros, reseñas nativas desplegables, enlaces de afiliado,
consentimiento de analítica y contenido disponible sin JavaScript. Cada categoría
debe tener una identidad visual y distribución propias dentro de la línea premium.
Temporada es una edición especial con identidad y selección específicas.

Fuentes activas: data/catalog.json, data/season.json, scripts/build_site.py,
scripts/departments.py, css/site.css, css/departments.css y js/main.js.
Los HTML son generados: actualizar las fuentes y regenerarlos, no editar solo la salida.
Documentar qué cambió y separar lo implementado de la configuración externa pendiente.
