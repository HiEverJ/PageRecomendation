"""Small decorative line drawings, emitted as static SVG without external assets."""
DRAWINGS = {
 'hogar': [
  '<path d="M24 51h47v24q-3 16-23 16T24 75zM71 57h8q18 0 12 15q-3 8-20 8M18 97h72M38 39q-9-9 0-17m15 17q-9-9 0-17"/>',
  '<path d="m15 60 45-38 45 38M27 53v46h66V53M49 99V72h22v27M10 106h100"/><path class="ink-wash" d="m27 55 33-27 33 27v44H27z"/>',
  '<path d="M32 98V58q0-20 28-20t28 20v40M23 98h74M42 38l-7-17m42 17 7-17M44 65q16 13 32 0"/>'
 ],
 'tecnologia': [
  '<rect x="23" y="34" width="74" height="48" rx="7"/><path d="M49 82v15m22-15v15M36 99h48M35 48h24m-24 11h43M9 44h7m88 22h7"/><circle cx="91" cy="19" r="4"/>',
  '<path d="M21 60h23V32h33m-33 28h37v31M21 81h23V60m33-28v14h25"/><circle cx="17" cy="60" r="5"/><circle cx="17" cy="81" r="5"/><circle cx="77" cy="27" r="5"/><circle cx="81" cy="96" r="5"/><circle cx="106" cy="46" r="5"/>',
  '<rect x="37" y="18" width="46" height="85" rx="9"/><path d="M51 27h18M55 93h10m-3-51-13 23h14l-7 17 18-26H60z"/>'
 ],
 'limpieza': [
  '<path d="M60 17Q30 52 30 72a30 30 0 0 0 60 0Q90 52 60 17zM42 72q0 16 16 18"/><path class="ink-wash" d="M60 26Q37 58 37 73a23 23 0 0 0 46 0Q83 58 60 26z"/>',
  '<path d="m43 20 5 20 20 5-20 5-5 20-5-20-20-5 20-5zm43 39 4 13 13 4-13 4-4 13-4-13-13-4 13-4z"/><circle cx="28" cy="90" r="8"/><circle cx="92" cy="27" r="5"/>',
  '<path d="M33 99q-9-44 10-65q39 0 45-17q13 52-15 66q-21 12-40 16zm0 0 39-44M49 78l-1-17m1 17 19-1"/>'
 ],
 'decoracion': [
  '<path d="M47 19h26v19q0 8 12 21q24 37-7 43H42Q11 96 35 59q12-13 12-21zM48 28h24M41 85q15 10 37 0"/><path class="ink-wash" d="M42 63q-19 30 5 32h26q24-2 5-32z"/>',
  '<path d="M23 102V54a37 37 0 0 1 74 0v48zM36 102V55a24 24 0 0 1 48 0v47M12 107h96"/><circle cx="60" cy="55" r="9"/>',
  '<path d="M25 99h70M60 98V55M34 56h52L74 22H46zM60 22v-7M22 42l-9-3m85 3 9-3"/>'
 ],
 'gamer': [
  '<path d="M37 43h46q12 0 17 22l6 23q3 16-11 10L77 83H43L25 98q-14 6-11-10l6-23q5-22 17-22zM32 57v18m-9-9h18"/><circle cx="79" cy="60" r="3"/><circle cx="90" cy="70" r="3"/><path d="m53 30 7-12 7 12"/>',
  '<path d="M24 74V57a36 36 0 0 1 72 0v17M24 62h8v28h-8q-10 0-10-14t10-14zm72 0h-8v28h8q10 0 10-14T96 62zM88 91q0 13-22 13"/><path class="ink-wash" d="M21 66h7v20h-7zm71 0h7v20h-7z"/>',
  '<path d="m36 36-22 24 22 24m48-48 22 24-22 24M68 24 51 96"/><path d="M24 107h72"/>'
 ],
 'halloween': [
  '<path d="M60 39q-37-20-44 18q-10 43 44 43t44-43q-7-38-44-18zm0 0q-4-16 12-22M60 40q-24 24 0 60m0-60q24 24 0 60M33 62l11-7 2 12zm41-7 11 7-13 5zM39 79q21 16 42 0"/><path class="ink-wash" d="M24 60q-7 31 23 33q-11-28 2-47q-20-8-25 14z"/>',
  '<path d="M87 21a39 39 0 1 0 11 67A34 34 0 0 1 87 21zM16 20l3 8 8 3-8 3-3 8-3-8-8-3 8-3zM99 45l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"/>',
  '<path d="M10 47q20-17 37 4l6-15 7 9 7-9 6 15q17-21 37-4q-18 9-18 26q-18-9-32 13q-14-22-32-13q0-17-18-26z"/>'
 ],
 'navidad': [
  '<path d="m60 15-25 33h12L26 75h16l-17 22h70L78 75h16L73 48h12zM60 97v13M43 65l32 7M43 87l31 2"/>',
  '<circle cx="60" cy="68" r="31"/><path d="M49 37V24h22v13M60 24V9M41 68q19-15 38 0M45 80q15-12 30 0"/>',
  '<path d="M23 52h74v50H23zM17 40h86v17H17zm43 0v62M60 40Q20 26 34 13Q54 6 60 40Q66 6 86 13Q100 26 60 40"/>'
 ],
 'san-valentin': [
  '<path d="M60 95Q7 59 24 32Q42 12 60 38Q78 12 96 32Q113 59 60 95z"/><path class="ink-wash" d="M60 86Q19 58 31 38Q43 24 60 49Q77 24 89 38Q101 58 60 86z"/>',
  '<path d="M19 35h82v61H19zM19 35l41 32 41-32M19 96l28-30m54 30L73 66M60 20q-14-10-10-16q5-5 10 2q5-7 10-2q4 6-10 16"/>',
  '<path d="M60 105V59m0 22q-27 0-27-22q27 0 27 22zm0 12q27 0 27-22q-27 0-27 22zM60 60Q26 44 39 24Q48 14 60 29Q72 14 81 24Q94 44 60 60z"/>'
 ],
 'entretiempo': [
  '<path d="M23 52h74v50H23zM17 40h86v17H17zm43 0v62M60 40Q20 26 34 13Q54 6 60 40Q66 6 86 13Q100 26 60 40"/>',
  '<path d="m60 18 9 30 31 10-31 10-9 30-9-30-31-10 31-10zM20 19l7 7m73-7-7 7M20 98l7-7m73 7-7-7"/>'
 ]
}

def ornament(key, index=0, small=False):
    drawings=DRAWINGS.get(key,DRAWINGS['entretiempo'])
    cls='ink-mark ink-mark-small' if small else 'ink-mark'
    return f'<span class="{cls}" aria-hidden="true"><svg viewBox="0 0 120 120" width="120" height="120" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" focusable="false">{drawings[index % len(drawings)]}</svg></span>'
