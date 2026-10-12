"""Render static pages from the editorial catalogue. This is a build tool, not a test.
Run from any directory: python scripts/build_site.py
No network, third-party packages, server or deployment is required.
"""
from pathlib import Path
from html import escape
import json
from departments import get_season, DEPARTMENTS, hero as department_hero, chapters

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://www.recomiendatop.lat/'
PRODUCTS = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))
SEASON_KEY, SEASON = get_season(ROOT)
LABELS = {'hogar':'Hogar', 'tecnologia':'Tecnología', 'limpieza':'Limpieza', 'hallazgos':'Hallazgos'}
NAV = [('index.html','Inicio'), ('hogar.html','Hogar'), ('tecnologia.html','Tecnología'), ('limpieza.html','Limpieza'), ('decoracion.html','Decoración'), ('gamer.html','Gamer'), ('festividades.html',SEASON['label'])]
e = escape

def url(page):
    return BASE if page == 'index.html' else BASE + page

def image(product, hero=False):
    loading = 'fetchpriority="high"' if hero else 'loading="lazy"'
    return f'<img src="{e(product["image"])}" alt="{e(product["title"])}" width="640" height="480" {loading} decoding="async">'

def card(p, n, origin, level=3):
    stores = '|'.join(x['store'] for x in p['links'])
    search = ' '.join([p['title'],p['tag'],p['summary'],LABELS[p['category']]])
    permalink = '#' + p['id'] if origin == 'catalogo.html' else 'catalogo.html#' + p['id']
    shops = ''.join(f'<a class="shop" href="{e(x["url"])}" target="_blank" rel="sponsored noopener noreferrer" data-store="{e(x["store"])}" aria-label="Ver {e(p["title"])} en {e(x["store"])}; abre otra pestaña">{e(x["store"])} <span aria-hidden="true">↗</span></a>' for x in p['links'])
    return f'''<article class="product" id="{e(p['id'])}" data-product data-category="{p['category']}" data-stores="{e(stores)}" data-search="{e(search)}">
    <div class="product-image">{image(p)}<span class="product-number" aria-hidden="true">{n:02}</span></div>
    <div class="product-body"><span class="eyebrow">{e(LABELS[p['category']])}</span><h{level}><a href="{e(permalink)}">{e(p['title'])}</a></h{level}>
    <p class="product-summary">{e(p['summary'])}</p>
    <details class="review"><summary>Antes de elegir<span class="sr-only">: {e(p['title'])}</span></summary><p>{e(p['check'])}</p></details>
    <div class="shops">{shops}</div><p class="product-note">Precio y disponibilidad en tienda · Abre otra pestaña</p></div></article>'''

def filters(items):
    categories = list(dict.fromkeys(p['category'] for p in items))
    options = ''.join(f'<option value="{c}">{LABELS[c]}</option>' for c in categories)
    return f'''<form id="filters" class="toolbar" role="search" aria-label="Buscar en esta selección" hidden>
    <div class="filter-fields"><div class="field"><label for="search">¿Qué te gustaría encontrar?</label><input id="search" name="q" type="search" maxlength="120" placeholder="Audífonos, café, organización…" autocomplete="off"></div>
    <div class="field"><label for="category">Categoría</label><select id="category" name="category"><option value="">Todas</option>{options}</select></div>
    <div class="field"><label for="store">Tienda</label><select id="store" name="store"><option value="">Cualquiera</option><option>Mercado Libre</option><option>AliExpress</option></select></div><button class="reset" type="reset">Limpiar filtros</button></div>
    <p id="result-count" class="results" role="status" aria-live="polite" aria-atomic="true">{len(items)} productos</p></form>'''

def catalogue(items, origin, heading='La selección', interactive=True):
    slug=origin.removesuffix('.html')
    definitions=SEASON['chapters'] if slug=='festividades' else DEPARTMENTS.get(slug,{}).get('chapters')
    layout=chapters(items,origin,card,definitions) if definitions else '<div class="grid">'+''.join(card(p,i+1,origin) for i,p in enumerate(items))+'</div>'
    return f'''<section id="seleccion" class="section wrap" aria-labelledby="selection-heading"><div class="section-head"><div><span class="eyebrow">Piezas con un propósito</span><h2 id="selection-heading">{e(heading)}</h2></div><p>Lee lo esencial, abre los detalles y decide si encaja contigo.</p></div>
    {filters(items) if interactive else ''}{layout}
    <div id="empty-results" class="empty" hidden><h3>No encontramos coincidencias.</h3><p>Prueba otra palabra o usa «Limpiar filtros» para volver a ver la selección.</p></div></section>'''

def guide(title, sections):
    content = ''.join(f'<details><summary>{e(h)}</summary><p>{e(p)}</p></details>' for h,p in sections)
    return f'<section class="guide wrap" aria-label="Guía de compra"><div><span class="eyebrow">Una compra más pensada</span><h2>{e(title)}</h2></div><div>{content}</div></section>'

def shell(page, title, description, content, items=None, noindex=False):
    nav = ''
    for f,label in NAV:
        current = 'aria-current="page"' if f == page else ''
        href = './' if f == 'index.html' else f
        seasonal = f'class="season-link" data-season="{SEASON_KEY}" aria-label="Temporada: {e(label)}"' if f=='festividades.html' else ''
        decoration = f'<span aria-hidden="true">{SEASON["symbol"]}</span> ' if seasonal else ''
        nav += f'<a href="{href}" {current} {seasonal}>{decoration}{label}</a>'
    department=page.removesuffix('.html')
    palette={'hogar':'#f6efe5','tecnologia':'#eef2f6','limpieza':'#edf5f2','decoracion':'#f4eee8','gamer':'#11131e','festividades':{'halloween':'#20172b','navidad':'#122f28','san-valentin':'#f8e9ec','entretiempo':'#f5ecd9'}[SEASON_KEY]}
    theme_color=palette.get(department,'#f5f3ed')
    graph = [{ '@type':'WebSite','@id':BASE+'#website','url':BASE,'name':'Recomienda[Top]','inLanguage':'es-MX'},
             {'@type':'CollectionPage' if items else 'WebPage','@id':url(page)+'#page','url':url(page),'name':title,'description':description,'inLanguage':'es-MX','isPartOf':{'@id':BASE+'#website'}}]
    if page != 'index.html':
        graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Inicio','item':BASE},{'@type':'ListItem','position':2,'name':title.split(' | ')[0],'item':url(page)}]})
    if items:
        graph[1]['mainEntity']={'@id':url(page)+'#selection'}
        graph.append({'@type':'ItemList','@id':url(page)+'#selection','numberOfItems':len(items),'name':title.split(' | ')[0],'itemListElement':[{'@type':'ListItem','position':i+1,'name':p['title'],'url':url(page)+'#'+p['id']} for i,p in enumerate(items)]})
    extra_style='<link rel="stylesheet" href="css/departments.css">'
    schema = json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
    html = f'''<!doctype html>
<html lang="es-MX"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="robots" content="{'noindex, follow' if noindex else 'index, follow, max-image-preview:large'}">
<link rel="canonical" href="{url(page)}"><link rel="icon" href="img/favicon.png" type="image/png"><meta name="theme-color" content="{theme_color}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_MX"><meta property="og:site_name" content="Recomienda[Top]"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{url(page)}"><meta property="og:image" content="{BASE}img/logo-recomiendatop.png"><meta property="og:image:alt" content="Recomienda Top"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{BASE}img/logo-recomiendatop.png">
<link rel="stylesheet" href="css/site.css">{extra_style}<script src="js/main.js" defer></script><script type="application/ld+json">{schema}</script></head>
<body data-department="{department}" data-season="{SEASON_KEY}"><a class="skip" href="#contenido">Saltar al contenido</a><header class="header"><div class="wrap header-inner"><a class="brand" href="./" aria-label="Recomienda Top, inicio">Recomienda<span>[Top]</span></a><button id="menu-toggle" class="menu-toggle" type="button" aria-controls="navigation" aria-expanded="true" hidden>Menú <span aria-hidden="true">☰</span></button><nav id="navigation" class="nav" aria-label="Principal">{nav}</nav></div></header>
<main id="contenido" tabindex="-1">{content}</main>
<footer class="footer"><div class="wrap footer-inner"><div><a class="brand" href="./">Recomienda<span>[Top]</span></a><p>Ideas para elegir con más intención.<br>© 2026 Recomienda[Top].</p></div><nav class="footer-links" aria-label="Información"><a href="catalogo.html">Todo el catálogo</a><a href="criterio-editorial.html">Nuestro criterio y afiliación</a><a href="privacidad.html">Privacidad</a><button id="privacy-preferences" type="button" hidden>Preferencias de analítica</button></nav></div></footer>
<section id="consent" class="consent" aria-labelledby="consent-title" hidden><h3 id="consent-title">Tú eliges qué compartir.</h3><p>Podemos cargar Google Tag Manager para medir visitas y clics hacia tiendas. Es opcional: puedes seguir explorando sin analítica. <a href="privacidad.html">Conoce los detalles</a>.</p><div class="consent-actions"><button type="button" data-consent="rejected">Sin analítica</button><button type="button" data-consent="accepted">Aceptar analítica</button></div><p id="consent-status" class="consent-status" role="status"></p></section>
</body></html>'''
    (ROOT/page).write_text(html+'\n',encoding='utf-8')

DISCLOSURE = '<p class="wrap disclosure">Algunos enlaces son de afiliado: podemos recibir una comisión si compras. Estas son orientaciones editoriales, sin pruebas de uso propias. Confirma modelo, precio, envío y devolución en la tienda. <a href="criterio-editorial.html">Así seleccionamos</a>.</p>'

def select(category):
    return [p for p in PRODUCTS if p['category'] == category]

def pick(*ids):
    by_id = {p['id']: p for p in PRODUCTS}
    return [by_id[product_id] for product_id in ids]

home_items = pick('audifonos-nothing-ear-a-con-anc', 'soporte-ergonomico-plegable-de-aluminio-para-laptop', 'power-bank-ugreen-10-000mah-con-magsafe-20w') + pick('prensa-francesa-de-vidrio-y-acero-inoxidable-1-litro', 'carrito-organizador-multiusos-de-3-niveles', 'manta-de-tejido-waffle')
hero_product=pick('audifonos-nothing-ear-a-con-anc')[0]
categories=[('hogar','Hogar','Orden, cocina y pequeños rituales.'),('tecnologia','Tecnología','Dispositivos que encajan en tu día.'),('limpieza','Limpieza','Herramientas para cada superficie.'),('decoracion','Decoración','Texturas, luz y objetos con intención.'),('gamer','Gamer','Un escritorio para jugar y crear.'),('festividades','Temporada · '+SEASON['label'],SEASON['note'])]
category_links=''.join(f'<a class="category-link" data-category="{slug}" href="{slug}.html"><strong>{label}</strong><span aria-hidden="true">↗</span><small>{desc}</small></a>' for slug,label,desc in categories)
home=f'''<section class="hero wrap"><div class="hero-copy"><span class="eyebrow">El placer de elegir bien</span><h1>Menos ruido.<br>Mejores <em>hallazgos.</em></h1><p>Recomendaciones breves de productos para tu casa y tu día a día. Descubre qué mirar antes de comprar en Mercado Libre y AliExpress.</p><div class="hero-actions"><a class="button" href="catalogo.html">Explorar el catálogo <span aria-hidden="true">↗</span></a><a class="text-link" href="criterio-editorial.html">Conoce nuestro criterio</a></div></div><div class="hero-art">{image(hero_product,True)}<div class="art-label"><span class="art-index" aria-hidden="true">01 /</span><a href="catalogo.html#{hero_product['id']}">Un detalle para escuchar distinto<br><strong>Nothing Ear (a) →</strong></a></div></div></section>
<div class="wrap trust-line"><span>Reseñas breves, sin rodeos</span><span>Lo útil y lo que debes revisar</span><span>Tú eliges dónde comprar</span></div>
<section class="section wrap"><div class="section-head"><div><span class="eyebrow">Encuentra tu siguiente idea</span><h2>¿Por dónde empezamos?</h2></div><a class="text-link" href="catalogo.html">Ver todos los productos ↗</a></div><div class="category-links">{category_links}</div></section>{DISCLOSURE}
{catalogue(home_items,'index.html','Pequeños cambios. Buenas ideas.',False)}
<section class="manifesto wrap"><div><span class="eyebrow">Comprar con intención</span><h2>No todo lo que llama<br>la atención te hace falta.</h2></div><div><p>Una buena recomendación empieza por una necesidad. Aquí encontrarás ideas de uso y puntos a revisar, sin contadores de urgencia ni descuentos que no podemos confirmar.</p><a href="criterio-editorial.html">Lee cómo trabajamos ↗</a></div></section>'''
shell('index.html','Recomendaciones para hogar y tecnología | Recomienda[Top]','Descubre productos de Mercado Libre y AliExpress con reseñas breves, ideas de uso y puntos a revisar antes de comprar. Hogar, tecnología y más.',home,home_items)

CONFIG = {
'hogar':('Un hogar que funciona para ti.','Objetos para organizar, cocinar y disfrutar tus espacios. Empieza por lo que usas cada día y elige pensando en el lugar que realmente tienes.',select('hogar'),'El espacio manda.',[
('Antes de llenar la cocina','Mide repisas, cajones y superficies. Un organizador útil permite acceder a lo que ya tienes; no debería obligarte a reorganizar todo para que quepa.'),('Materiales y mantenimiento','Comprueba si tapas, mangos y accesorios requieren cuidados distintos. Piensa también dónde se secarán y guardarán después de cada uso.'),('Cuándo dejarlo pasar','Si duplica una función que ya resuelves bien o no tiene un sitio claro, quizá no sea la compra que necesitas ahora.')]),
'tecnologia':('Tecnología con sentido.','Audio, escritorio y casa conectada: ideas para resolver una necesidad concreta. El modelo exacto y la compatibilidad importan más que una lista larga de funciones.',select('tecnologia'),'Primero, compatibilidad.',[
('No te quedes con el nombre','Comprueba número de modelo, generación y versión regional. Publicaciones visualmente parecidas pueden incluir accesorios, garantías o conexiones diferentes.'),('El costo que no sale en la foto','Considera adaptadores, repuestos, baterías y suscripciones. Revisa qué funciona sin una cuenta adicional y durante cuánto tiempo habrá soporte.'),('Una especificación no es una experiencia','Resolución admitida, capacidad nominal o potencia máxima no cuentan toda la historia. Busca evidencia independiente y condiciones de medición antes de comparar.')]),
'limpieza':('Cada superficie, su cuidado.','Herramientas y accesorios para una rutina más práctica. Elige por el material que vas a limpiar, el espacio disponible y los repuestos que podrás conseguir.',select('limpieza'),'El acabado importa.',[
('Empieza por la superficie','Consulta las instrucciones del acabado y del limpiador. Una solución abrasiva, el vapor o un adhesivo pueden ser inadecuados para algunos materiales.'),('Piensa en la segunda compra','Filtros, paños, cabezales y baterías forman parte del costo de uso. Comprueba si puedes conseguir repuestos antes de elegir el aparato.'),('Más potencia no resuelve todo','Valora peso, maniobrabilidad y guardado. No presentamos resultados de desinfección, filtración o autonomía como si se hubieran medido aquí.')]),
'decoracion':('Un espacio que se sienta tuyo.','Pequeños cambios de textura, luz y organización. Esta selección reúne piezas del catálogo de hogar para renovar un rincón sin empezar desde cero.',pick('fundas-de-cojin-de-lino', 'manta-de-tejido-waffle', 'tira-de-luces-led-calidas', 'lampara-de-sal-del-himalaya', 'set-de-velas-de-soya', 'fuente-zen-de-escritorio-con-cascada', 'repisa-esquinera-flotante-minimalista'),'Diseña desde lo cotidiano.',[
('Una paleta antes que muchos objetos','Elige dos o tres tonos presentes en el espacio y repítelos en textiles o iluminación. Una foto de tienda no reproduce siempre el color real del material.'),('Mide más que el objeto','Considera la escala respecto al sofá, mesa o pared. Deja sitio para circular, limpiar y utilizar lo que ya tienes.'),('Luz con una función','Distingue luz de ambiente y luz para trabajar. Una lámpara decorativa puede acompañar una escena sin iluminar lo suficiente para leer.')]),
'gamer':('Tu setup, a tu manera.','Empieza por el escritorio: pantalla, teclado, audio y luz. Son productos del catálogo de tecnología que puedes valorar para jugar, trabajar o crear; no una clasificación de rendimiento.',pick('monitor-lg-ultra-wide-curvo-34-100hz', 'teclado-mecanico-75-triple-conexion', 'audifonos-sony-wh-1000xm6-noise-cancelling', 'soporte-ergonomico-plegable-de-aluminio-para-laptop', 'webcam-4k-pro-con-aro-de-luz-integrado', 'tira-de-luz-neon-led-inteligente-rgbic-5-metros', 'hub-usb-c-8-en-1-docking-station-pd-100w'),'Antes de montar el setup.',[
('La pantalla debe encajar con el equipo','Comprueba resolución de salida, puertos y capacidad de tu computadora. El monitor panorámico de esta selección no es una recomendación automática para competición.'),('Periféricos que puedas usar horas','Valora distribución del teclado, tamaño del escritorio y ajuste de audífonos. La comodidad individual no se deduce de una etiqueta gamer.'),('Compra por fases','Resuelve primero el dispositivo que te limita. Iluminación y accesorios pueden esperar si aún necesitas una conexión o una superficie de trabajo adecuada.')]),
'festividades':('Regala algo que tenga lugar.','Ideas para café, música, casa y pequeños rituales. Una selección para cumpleaños, Navidad o un detalle sin fecha, con enlaces que ya forman parte de nuestro catálogo.',pick('prensa-francesa-de-vidrio-y-acero-inoxidable-1-litro', 'set-de-8-tazas-de-vidrio-con-doble-pared-80ml', 'manta-de-tejido-waffle', 'set-de-velas-de-soya', 'fundas-de-cojin-de-lino')+pick('audifonos-nothing-ear-a-con-anc', 'bocina-portatil-xiaomi-sound-pocket-ip67'),'Piensa en quien lo recibe.',[
('Su rutina es la mejor pista','Elige algo que acompañe una actividad que ya disfruta. Evita regalar un dispositivo que exija comprar varios accesorios para comenzar a usarlo.'),('Compatibilidad y devolución','Confirma modelos de teléfono, medidas y preferencias antes de elegir. Revisa condiciones de cambio y si la tienda permite enviar un comprobante de regalo.'),('La fecha también cuenta','Comprueba plazo de entrega según el domicilio y deja margen para incidencias. No mostramos una fecha garantizada de llegada ni descuentos de temporada sin confirmar.')])
}
for slug,(heading,intro,items,guide_title,sections) in CONFIG.items():
    label=dict((x[0],x[1]) for x in categories)[slug]
    if slug=='festividades':
        heading,intro=SEASON['heading'],SEASON['intro']
        items=pick(*SEASON['products'])
        guide_title='Celebra con intención.'
        sections=[('El ambiente, a tu medida','Elige por lo que vas a hacer: una película, una cena o un regalo. Los productos pertenecen al catálogo habitual; no son artículos oficiales de la celebración.'),('Antes de preparar la escena','Confirma dimensiones, conexiones, cuidados y plazo de entrega. No coloques textiles junto a fuentes de calor ni uses iluminación en exteriores sin comprobar su protección.'),('Que tenga vida después','Prioriza objetos que sigan siendo útiles cuando termine la celebración. La ambientación puede cambiar sin empezar de cero cada año.')]
        title,description=SEASON['title'],SEASON['description']
    else:
        title,description=DEPARTMENTS[slug]['title'],DEPARTMENTS[slug]['description']
    content=f'<nav class="wrap breadcrumb" aria-label="Ruta de navegación"><a href="./">Inicio</a> / <span aria-current="page">{e(label)}</span></nav>'
    content+=department_hero(slug,heading,intro,items,PRODUCTS,image,SEASON_KEY,SEASON)
    content+=DISCLOSURE+catalogue(items,slug+'.html')+guide(guide_title,sections)
    next_slug=categories[(next(i for i,c in enumerate(categories) if c[0]==slug)+1)%len(categories)][0]
    next_label=next(c[1] for c in categories if c[0]==next_slug)
    content+=f'<aside class="wrap department-next"><span class="eyebrow">Cambia de ambiente</span><a href="{next_slug}.html">Descubre {e(next_label)} <span aria-hidden="true">↗</span></a></aside>'
    shell(slug+'.html',title,description,content,items)

content='<section class="wrap category-hero"><span class="eyebrow">El catálogo</span><h1>Encuentra lo que<br>va contigo.</h1><p>Busca por nombre o idea de uso. Filtra por categoría y tienda, lee los detalles y compara la publicación antes de decidir.</p></section>'+DISCLOSURE+catalogue(PRODUCTS,'catalogo.html','Todos los hallazgos')
shell('catalogo.html','Catálogo de productos y recomendaciones | Recomienda[Top]','Explora recomendaciones de hogar, tecnología y limpieza. Busca productos y filtra por Mercado Libre o AliExpress para comparar opciones.',content,PRODUCTS)

editorial='''<article class="wrap prose"><span class="eyebrow">Nuestro criterio</span><h1>Recomendar también<br>es poner límites.</h1><p>Recomienda[Top] es un catálogo de ideas de compra con orientación editorial. Queremos que puedas entender para qué podría servirte un producto y qué conviene revisar antes de abrir una tienda.</p>
<h2>Qué encontrarás aquí</h2><p>Reseñas breves basadas en el catálogo y las descripciones de producto disponibles en este proyecto. Las fichas distinguen una idea de uso de los detalles que debes confirmar con el vendedor. No son pruebas de laboratorio ni reseñas basadas en uso personal documentado.</p>
<h2>Qué no damos por demostrado</h2><p>No asignamos estrellas ni declaramos un producto «el mejor» sin evidencia propia. Tampoco garantizamos autenticidad, rendimiento, beneficios de salud o disponibilidad. Los nombres y características identifican la referencia del catálogo: la publicación de la tienda puede cambiar o incluir varias versiones.</p>
<h2>Cómo usar una recomendación</h2><ul><li>Decide primero qué necesidad quieres resolver.</li><li>Lee «Antes de elegir» para reconocer posibles límites o incompatibilidades.</li><li>Comprueba modelo, variantes, vendedor, envío, devolución y precio final en la tienda.</li><li>Compara con lo que ya tienes y con otras alternativas antes de comprar.</li></ul>
<h2>Enlaces de afiliación</h2><p>Algunos enlaces a Mercado Libre y AliExpress son de afiliado. Podemos recibir una comisión si una compra cumple las condiciones del programa. No vendemos ni cobramos los productos: el pedido, el pago, la entrega y las devoluciones se gestionan con la tienda y su vendedor.</p><p>Los enlaces se abren en otra pestaña y están identificados en el código como patrocinados. Si hay dos tiendas, comprueba que ofrezcan el mismo modelo y accesorios antes de comparar precios.</p>
<h2>Actualizaciones y precios</h2><p>No mostramos precios ni descuentos que no podamos mantener actualizados. La selección no implica una oferta vigente ni una auditoría del vendedor. Tampoco pedimos tu correo ni simulamos una suscripción o un envío de mensajes.</p><p><a href="catalogo.html">Explora el catálogo →</a></p></article>'''
shell('criterio-editorial.html','Nuestro criterio y afiliación | Recomienda[Top]','Conoce cómo leer nuestras recomendaciones, sus límites y la relación de afiliación con enlaces hacia tiendas.',editorial)

privacy='''<article class="wrap prose"><span class="eyebrow">Privacidad y preferencias</span><h1>Explorar es tu elección.<br>Compartir datos, también.</h1>
<h2>Búsqueda y filtros</h2><p>El buscador filtra las fichas en tu navegador. Este sitio no envía el texto que escribes a un buscador externo y no ofrece cuentas, pagos ni formularios de contacto.</p>
<h2>Analítica opcional</h2><p>Antes de que aceptes, este código no carga Google Tag Manager. Si aceptas, se carga el contenedor GTM-W4BPKXL4 de Google. Las etiquetas configuradas por el administrador pueden medir visitas y utilizar cookies. El sitio envía además un evento de clic de afiliación con el identificador del producto, la tienda y la ruta de la página, sin el texto de tus búsquedas.</p><p>La configuración de ese contenedor se administra fuera de este sitio. La información sobre servicios habilitados, cookies y plazos de conservación debe corresponder a las etiquetas que estén efectivamente activas. Puedes consultar también la <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">información de privacidad de Google (otra pestaña)</a>.</p>
<h2>Cambiar de elección</h2><p>Usa «Preferencias de analítica» en el pie de página. La elección se guarda en el almacenamiento local de este navegador como recomiendatop-analytics-v1. Si retiras la aceptación después de cargar las etiquetas, la página se recarga para dejar de cargarlas. Esto no elimina automáticamente cookies previas de Google ni datos ya enviados; puedes borrar cookies desde tu navegador.</p><p>Si el almacenamiento está bloqueado, tu elección puede durar solo durante esta visita. Sin JavaScript no se carga la analítica ni se guardan preferencias.</p>
<h2>Tiendas y alojamiento</h2><p>Al seguir un enlace sales a un servicio externo, que aplica sus propias condiciones y puede usar identificadores de afiliación. El alojamiento de este sitio también puede tratar datos técnicos de conexión, como dirección IP y solicitudes de archivos, según su configuración.</p>
<h2>Alcance de esta información</h2><p>Esta página explica el funcionamiento del sitio. No proporciona una identidad legal ni un canal de ejercicio de derechos que todavía no han sido aportados por el responsable. Esa información y los detalles de las etiquetas activas deben completarse para disponer de un aviso integral.</p></article>'''
shell('privacidad.html','Privacidad y analítica opcional | Recomienda[Top]','Cómo funcionan los filtros, las preferencias locales, la analítica opcional y los enlaces a tiendas de Recomienda Top.',privacy)

health='''<article class="wrap prose"><span class="eyebrow">Selección en preparación</span><h1>La salud merece<br>otro nivel de cuidado.</h1><p>No tenemos una selección de salud con evidencia suficiente para recomendar aquí. Hemos retirado las fichas de ejemplo para evitar presentarlas como reseñas reales.</p><p>Puedes seguir explorando ideas para tu casa y tu escritorio, con sus límites y puntos a revisar.</p><a class="button" href="catalogo.html">Explorar el catálogo ↗</a></article>'''
shell('salud.html','Selección de salud en preparación | Recomienda[Top]','La selección de salud no está disponible. Descubre otras categorías del catálogo.',health,noindex=True)
shell('404.html','Página no encontrada | Recomienda[Top]','Encuentra productos y categorías en el catálogo de Recomienda Top.','<section class="wrap prose"><span class="eyebrow">404 / Un pequeño desvío</span><h1>Este hallazgo<br>no está aquí.</h1><p>La dirección puede haber cambiado. Vuelve al catálogo para encontrar productos por nombre, categoría o tienda.</p><a class="button" href="/catalogo.html">Ir al catálogo ↗</a></section>',noindex=True)
# Error pages can be served for nested unknown URLs; resolve all relative assets at the site root.
error_page=ROOT/'404.html'
error_page.write_text(error_page.read_text(encoding='utf-8').replace('<head>','<head><base href="/">',1),encoding='utf-8')
pages=['index.html','catalogo.html',*[slug+'.html' for slug in CONFIG],'criterio-editorial.html','privacidad.html']
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{url(p)}</loc></url>\n' for p in pages)+'</urlset>\n',encoding='utf-8')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /docs/\nDisallow: /data/\nDisallow: /scripts/\n\nSitemap: '+BASE+'sitemap.xml\n',encoding='utf-8')
print('Páginas estáticas generadas en',ROOT)
