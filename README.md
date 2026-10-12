# Recomienda[Top]

Catálogo estático de orientación de compra para Mercado Libre y AliExpress.
Proyecto real: `C:\Sources\PageRecomendation`. Dominio declarado: `www.recomiendatop.lat`.

## Editar

- `data/catalog.json`: 64 fichas, textos, imágenes y destinos comerciales.
- `scripts/build_site.py`: páginas, selecciones, navegación y metadata.
- `css/site.css`: base visual, sin Sass ni fuentes externas.
- `css/departments.css`: identidades visuales y composiciones por categoría.
- `scripts/departments.py`: escenas, capítulos, temporadas y selecciones estacionales.
- `data/season.json`: edición automática por fecha o selección manual.
- `js/main.js`: menú, filtros y preferencias de analítica.

Después de cambiar datos o textos de página, ejecuta `python scripts/build_site.py`.
Solo genera HTML y archivos SEO; no levanta servidores, no ejecuta pruebas ni despliega.
No necesita paquetes adicionales. Conserva los IDs del catálogo para mantener enlaces.

Los HTML generados incluyen todo el contenido. JavaScript solo añade búsqueda,
filtros y navegación adaptable; los detalles y enlaces funcionan sin él.
Las hojas CSS/Sass y los JS por categoría anteriores permanecen como referencia,
pero **ya no se cargan**. No recompilarlos pensando que son el diseño activo.

## Documentación

- `docs/NOTAS-DE-CAMBIO.txt`: hallazgos, cambios, límites y archivos afectados.
- `docs/inventario-original.json`: inventario anterior, incluidas fichas incompletas.
  Su campo `ready` es previo a recuperar el href duplicado de enchufes inteligentes.

## Antes de publicar

Completar identidad/contacto y aviso de privacidad; revisar etiquetas del contenedor
GTM-W4BPKXL4, derechos de imágenes, destinos comerciales, dominio y redirecciones.
Los eventos `affiliate_click` requieren configuración externa para verse en Analytics.
Se carga GTM solo cuando el visitante acepta. Rechazarlo no impide usar el catálogo.

Publicar los HTML, `css/site.css`, `css/departments.css`, `js/main.js`, imágenes necesarias, `robots.txt`,
`sitemap.xml` y `CNAME` según el proveedor. No hace falta publicar `data/`, `scripts/`
ni `docs/`. El 404 necesita que el hosting devuelva un estado 404 real.

No se realizaron pruebas automatizadas, visuales, capturas ni entornos aislados.
La revisión manual en pantallas queda al dueño. No se desplegó a producción.

## Identidades y temporadas

Cada departamento conserva los controles comunes y tiene su propia composición.
Consulta `docs/IDENTIDADES-Y-TEMPORADAS.txt` para los cambios y las notas SEO.

`data/season.json` admite `auto`, `halloween`, `navidad`, `san-valentin` o
`entretiempo` en el campo `mode`. Auto se evalúa **al generar el sitio**, con
fecha de Ciudad de México: Halloween en octubre, Navidad en noviembre/diciembre,
San Valentín del 15 de enero al 14 de febrero, y entretiempo el resto del año.
Cambiar la fecha no actualiza por sí solo un sitio ya publicado: regenerar y
publicar requiere el flujo y la autorización del dueño. No hay despliegue automático.

Las restricciones permanentes del propietario están registradas en `AGENTS.md`.
