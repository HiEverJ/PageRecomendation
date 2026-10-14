"""Editorial presentation and seasonal selection; used only at build time."""
from datetime import datetime, timezone, timedelta
from html import escape as e
import json
from ornaments import ornament

SEASONS = {
    'halloween': {
        'label':'Halloween', 'symbol':'✦', 'kicker':'Edición de octubre / Halloween',
        'heading':'Que caiga la noche.',
        'intro':'Luz baja, sombras largas y una película que dé un poco de miedo. Ideas del catálogo para ambientar Halloween, sin comprar toda una decoración de un solo uso.',
        'title':'Halloween: luces y ambiente para una noche de cine | Recomienda[Top]',
        'description':'Prepara una noche de Halloween con iluminación, proyección y detalles acogedores. Ideas de ambiente con puntos a revisar y enlaces a tiendas.',
        'note':'La atmósfera hace la magia.',
        'chapters':[(3,'Enciende la oscuridad','Luz que cambia el ánimo de una habitación.'),(3,'Una noche de película','Prepara la escena, el sonido y un rincón cómodo.'),(2,'Quédate un rato más','Pequeños detalles para alargar la sobremesa.')],
        'products':['tira-de-luz-neon-led-inteligente-rgbic-5-metros','tira-de-luces-led-calidas','lampara-de-sal-del-himalaya','mini-proyector-inteligente-con-android-y-wi-fi-soporta-1080p','bocina-portatil-xiaomi-sound-pocket-ip67','manta-de-tejido-waffle','set-de-8-tazas-de-vidrio-con-doble-pared-80ml','prensa-francesa-de-vidrio-y-acero-inoxidable-1-litro']
    },
    'navidad': {
        'label':'Navidad','symbol':'✧','kicker':'Edición de invierno / Navidad',
        'heading':'Lo bonito es compartir.',
        'intro':'Una casa iluminada, café recién hecho y detalles pensados para alguien. Ideas de nuestro catálogo para celebrar Navidad y seguir disfrutándolas después.',
        'title':'Navidad: regalos y detalles para celebrar en casa | Recomienda[Top]',
        'description':'Descubre ideas de regalos de Navidad, luz cálida y detalles para la mesa. Recomendaciones breves de hogar y tecnología con enlaces a tiendas.',
        'note':'Un detalle. Muchas maneras de decirlo.',
        'chapters':[(3,'La casa se viste de fiesta','Texturas y luz para recibir con calma.'),(3,'Alrededor de la mesa','El café como excusa para volver a encontrarse.'),(3,'Para alguien en especial','Objetos que acompañan una rutina todo el año.')],
        'products':['tira-de-luces-led-calidas','manta-de-tejido-waffle','fundas-de-cojin-de-lino','prensa-francesa-de-vidrio-y-acero-inoxidable-1-litro','set-de-8-tazas-de-vidrio-con-doble-pared-80ml','set-de-3-tablas-de-bambu-para-picar','audifonos-nothing-ear-a-con-anc','bocina-portatil-xiaomi-sound-pocket-ip67','set-de-velas-de-soya']
    },
    'san-valentin': {
        'label':'San Valentín','symbol':'♡','kicker':'Edición de febrero / San Valentín',
        'heading':'Los detalles dicen más.',
        'intro':'Un café para dos, una playlist compartida o un rincón para quedarse. Ideas para regalar tiempo y atención en San Valentín, con objetos que tengan sentido después de la fecha.',
        'title':'San Valentín: detalles y regalos para compartir | Recomienda[Top]',
        'description':'Ideas para San Valentín: café, música y detalles para un rincón compartido. Descubre productos y qué revisar antes de elegir un regalo.',
        'note':'Para tu persona favorita. O para ti.',
        'chapters':[(3,'Un momento para dos','Haz espacio para una conversación sin prisa.'),(3,'Su pequeño ritual','Piensa en eso que disfruta cada día.'),(2,'Una luz distinta','La intención se nota en los detalles.')],
        'products':['prensa-francesa-de-vidrio-y-acero-inoxidable-1-litro','set-de-8-tazas-de-vidrio-con-doble-pared-80ml','manta-de-tejido-waffle','audifonos-nothing-ear-a-con-anc','bocina-portatil-xiaomi-sound-pocket-ip67','mini-refrigerador-skincare-6l-con-espejo-y-luz-led','set-de-velas-de-soya','lampara-de-sal-del-himalaya']
    },
    'entretiempo': {
        'label':'Temporada','symbol':'✺','kicker':'Edición abierta / Pequeñas celebraciones',
        'heading':'No hace falta una fecha.',
        'intro':'Ideas para celebrar lo cotidiano: compartir una bebida, renovar un rincón o sorprender a alguien. La selección cambia cuando llega una nueva edición de temporada.',
        'title':'Temporada: ideas para regalar y celebrar en casa | Recomienda[Top]',
        'description':'Encuentra ideas para celebrar y regalar: pequeños detalles de hogar, café y música con reseñas breves y enlaces a Mercado Libre y AliExpress.',
        'note':'Las pequeñas ocasiones también cuentan.',
        'chapters':[(3,'Para compartir','Una buena conversación empieza por hacerse un hueco.'),(3,'Para disfrutar','Regalos que encuentran lugar en la rutina.')],
        'products':['prensa-francesa-de-vidrio-y-acero-inoxidable-1-litro','set-de-8-tazas-de-vidrio-con-doble-pared-80ml','manta-de-tejido-waffle','audifonos-nothing-ear-a-con-anc','bocina-portatil-xiaomi-sound-pocket-ip67','fundas-de-cojin-de-lino']
    }
}

def get_season(root):
    settings=json.loads((root/'data/season.json').read_text(encoding='utf-8'))
    # Mexico City remains UTC-6; do not let the build host choose the date.
    today=datetime.now(timezone(timedelta(hours=-6))).date()
    mode=settings.get('mode','auto')
    if mode == 'auto':
        md=(today.month,today.day)
        key='halloween' if (10,1)<=md<=(10,31) else 'navidad' if (11,1)<=md<=(12,31) else 'san-valentin' if (1,15)<=md<=(2,14) else 'entretiempo'
    else:
        key=mode
    if key not in SEASONS:
        raise ValueError('Temporada desconocida: '+key)
    return key,SEASONS[key]

DEPARTMENTS={
    'hogar': {'word':'Habitar','mood':'Texturas suaves / Rituales cotidianos','hero': 'manta-de-tejido-waffle','title':'Hogar: organización y utensilios para tu día a día | Recomienda[Top]', 'description':'Ideas para organizar la casa, cocinar y crear rincones cómodos. Descubre utensilios y accesorios con reseñas breves y puntos a revisar antes de comprar.', 'chapters':[(7,'El arte de estar en casa','Texturas, luz y pequeños rituales que invitan a bajar el ritmo.'),(7,'Todo encuentra su lugar','Organizar también es dejar espacio para lo que sí utilizas.'),(7,'La cocina, sin prisa','Objetos que acompañan la preparación, la mesa y el primer café.')]},
    'tecnologia': {'word':'Conectar','mood':'Diseño preciso / Utilidad diaria','hero':'audifonos-nothing-ear-a-con-anc','title':'Tecnología: audio, escritorio y casa conectada | Recomienda[Top]', 'description':'Explora audífonos, monitores, accesorios USB-C y dispositivos para casa. Recomendaciones de tecnología con criterios de compatibilidad y enlaces a tiendas.', 'chapters':[(9,'Tu estación de ideas','Conexiones y herramientas para un escritorio que trabaje contigo.'),(6,'Una casa conectada','Automatiza una rutina concreta, no toda tu vida de golpe.'),(6,'Lo que va contigo','Audio, energía y pequeñas pantallas para cambiar de escenario.')]},
    'limpieza': {'word':'Renovar','mood':'Espacios claros / Rutinas sencillas','hero':'cepillo-de-limpieza-electrico-inalambrico-rotativo','title':'Limpieza: herramientas para cocina, pisos y baño | Recomienda[Top]', 'description':'Elige accesorios de limpieza según cada superficie. Ideas para cocina, pisos y baño con advertencias de compatibilidad y enlaces a Mercado Libre y AliExpress.', 'chapters':[(6,'Empieza por la cocina','De las superficies de trabajo a los detalles que más se usan.'),(8,'Una rutina más ligera','Herramientas para elegir según el material y el tamaño de la tarea.'),(5,'El último detalle','Orden y cuidado para los rincones de uso diario.')]},
    'decoracion': {'word':'Componer','mood':'Luz, materia / Equilibrio','hero':'lampara-de-sal-del-himalaya','title':'Decoración: textiles y luz para renovar un rincón | Recomienda[Top]', 'description':'Ideas de decoración con mantas, cojines, iluminación y objetos pequeños. Aprende qué medidas, materiales y cuidados revisar para que encajen en tu espacio.', 'chapters':[(3,'Capas que cambian un espacio','Textiles y luz para empezar sin sustituirlo todo.'),(4,'Objetos con presencia','Una pieza elegida con intención puede ser suficiente.')]},
    'gamer': {'word':'Play.','mood':'Menos distracciones / Más inmersión','hero':'teclado-mecanico-75-triple-conexion','title':'Setup gamer: pantalla, teclado, audio y luz | Recomienda[Top]', 'description':'Ideas para un setup gamer sobrio: monitores, teclados, audio y luz RGB. Compara compatibilidad y espacio antes de elegir accesorios para jugar o crear.', 'chapters':[(3,'El núcleo de tu setup','Lo que ves, lo que escuchas y lo que tocas en cada sesión.'),(4,'Tu siguiente nivel','Completa el espacio para jugar, trabajar o transmitir.')]}
}

def season_art(key):
    # Decorative inline vectors: no image downloads or canvas, excluded from accessibility tree.
    if key=='halloween':
        drawing='''<circle cx="240" cy="155" r="112" fill="#f6b963"/><path d="M30 168q40-47 72-8q15-50 40-5q30-35 66 2q-47 0-68 37q-48-35-110-26" fill="#271c33"/><path d="M294 80q25-24 42-1q11-29 26-2q20-18 39 1q-35 0-50 25q-25-23-57-23" fill="#271c33"/><path d="M39 370Q80 190 205 242Q275 187 339 298Q378 423 226 435Q75 453 39 370" fill="#ec743d"/><ellipse cx="165" cy="340" rx="65" ry="99" fill="#ff924c"/><ellipse cx="235" cy="340" rx="43" ry="93" fill="#f58242"/><path d="m178 248 7-57 25-9-4 57" fill="#81905c"/><path d="m91 325 50-24-13 46zm109-12 40-13 25 38zm-86 58 37 8 16-13 22 15 36-14-32 44-47-1z" fill="#271c33"/>'''
    elif key=='navidad':
        drawing='''<g fill="#f1cd80"><path d="m210 28 12 29 32 2-24 22 7 30-27-16-27 16 7-30-24-22 32-2z"/><circle cx="72" cy="123" r="4"/><circle cx="345" cy="184" r="6"/><circle cx="62" cy="310" r="6"/></g><path d="m210 89-93 140h44L91 327h58l-67 78h257l-68-78h58l-70-98h44z" fill="#44806b"/><path d="m210 118-45 94h40l-48 96h48l-41 75h118l-63-75h39l-44-96h28z" fill="#689681"/><g fill="#eed9aa"><circle cx="171" cy="257" r="9"/><circle cx="244" cy="328" r="10"/><circle cx="209" cy="197" r="7"/></g><path d="M92 401h103v65H92z" fill="#b85055"/><path d="M133 400h18v66h-18z" fill="#f1cd80"/><path d="M247 413h89v53h-89z" fill="#f1cd80"/><path d="M282 413h17v53h-17z" fill="#b85055"/>'''
    elif key=='san-valentin':
        drawing='''<circle cx="215" cy="247" r="174" fill="#ead0cf"/><path d="M211 366Q47 262 84 162Q127 85 211 177Q296 85 339 162Q376 262 211 366" fill="#a83652"/><path d="M212 329Q97 256 118 189Q138 151 183 183" fill="none" stroke="#df7b8e" stroke-width="8"/><g fill="#a83652"><path d="m60 78 5 16 16 5-16 5-5 16-5-16-16-5 16-5z"/><path d="m344 360 5 16 16 5-16 5-5 16-5-16-16-5 16-5z"/></g>'''
    else:
        drawing='''<circle cx="210" cy="250" r="155" fill="#eed79c"/><path d="M89 227h244v191H89z" fill="#b9694d"/><path d="M190 227h40v191h-40zM77 204h268v49H77z" fill="#f4e4ba"/><path d="M208 201Q90 155 141 113Q199 83 210 201Q241 77 290 115Q336 165 208 201" fill="none" stroke="#a45037" stroke-width="15"/>'''
    return '<svg class="season-illustration" viewBox="0 0 420 500" aria-hidden="true" focusable="false">'+drawing+'</svg>'

def hero(slug,heading,intro,items,products,image,season_key,season):
    if slug=='festividades':
        kicker=season['kicker'];word=season['label'];mood=season['note']
        art=season_art(season_key)
    else:
        cfg=DEPARTMENTS[slug];kicker='La selección / '+{'hogar':'Hogar','tecnologia':'Tecnología','limpieza':'Limpieza','decoracion':'Decoración','gamer':'Gamer'}[slug]
        word=cfg['word'];mood=cfg['mood'];p=next(p for p in products if p['id']==cfg['hero'])
        art=f'<a class="department-object" href="#{e(p["id"])}" aria-label="Descubrir {e(p["title"])}">{image(p,True)}</a>'
    return f'''<section class="department-hero wrap"><div class="department-copy"><span class="eyebrow">{e(kicker)}</span><h1>{e(heading)}</h1><p>{e(intro)}</p><div class="hero-actions"><a class="button" href="#seleccion">Descubrir {len(items)} ideas ↓</a><a class="text-link" href="catalogo.html">Todo el catálogo</a></div></div><div class="department-scene"><span class="scene-word" aria-hidden="true">{e(word)}</span><div class="scene-orbit" aria-hidden="true"></div>{art}<span class="scene-caption">{e(mood)}</span></div></section>'''

def chapters(items,origin,card,definitions,season_key="entretiempo"):
    motif=season_key if origin=="festividades.html" else origin.removesuffix(".html")
    blocks=[];links=[];start=0
    for n,(size,title,description) in enumerate(definitions,1):
        rows=items[start:start+size];section_id='capitulo-'+str(n)
        if not rows:continue
        links.append(f'<a href="#{section_id}" data-chapter-link="{section_id}"><span>{n:02}</span> {e(title)}</a>')
        drawing=ornament(motif,n-1)
        tail=('<div class="ink-divider" aria-hidden="true"><span></span>'+ornament(motif,n,small=True)+'<span></span></div>') if n==len(definitions) else ''
        markup=''.join(card(p,start+i+1,origin,level=4) for i,p in enumerate(rows))
        blocks.append(f'''<section class="product-chapter chapter-{n}" id="{section_id}" data-chapter aria-labelledby="{section_id}-title"><div class="chapter-intro"><span class="chapter-number" aria-hidden="true">{n:02}</span><div><span class="eyebrow">La selección / <span data-chapter-count>{len(rows)} ideas</span></span><h3 id="{section_id}-title">{e(title)}</h3><p>{e(description)}</p></div>{drawing}</div><div class="grid chapter-grid">{markup}</div>{tail}</section>''')
        start+=size
    # New catalogue items are retained if the editor has not assigned a chapter yet.
    if start<len(items):
        blocks.append('<section class="product-chapter" id="capitulo-mas" data-chapter aria-label="Más ideas"><div class="chapter-intro"><h3>Más ideas para descubrir</h3></div><div class="grid chapter-grid">'+''.join(card(p,start+i+1,origin,level=4) for i,p in enumerate(items[start:]))+'</div></section>')
    return '<nav class="chapter-nav" aria-label="Recorrer la selección">'+''.join(links)+'</nav>'+''.join(blocks)
