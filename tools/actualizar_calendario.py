#!/usr/bin/env python3
"""Genera atlantida/calendario.js a partir del iCal de Airbnb.

Uso: python3 tools/actualizar_calendario.py <archivo.ics> [fecha_AAAA-MM-DD]
Toma todas las reservas y bloqueos (DTSTART..DTEND, DTEND exclusivo) y los
publica como noches ocupadas, sin nombres ni códigos.
Imprime CHANGED o UNCHANGED.
"""
import json, re, sys, datetime, pathlib

ics = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
ics = re.sub(r"\r?\n[ \t]", "", ics)  # desplegar líneas continuadas
upd = sys.argv[2] if len(sys.argv) > 2 else datetime.date.today().isoformat()

def d(v):
    v = v.strip()[:8]
    return f"{v[:4]}-{v[4:6]}-{v[6:8]}"

busy = []
for ev in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", ics, re.S):
    s = re.search(r"DTSTART[^:]*:(\d{8})", ev)
    e = re.search(r"DTEND[^:]*:(\d{8})", ev)
    if s and e:
        busy.append([d(s.group(1)), d(e.group(1))])
busy.sort()

out = pathlib.Path(__file__).resolve().parent.parent / "atlantida" / "calendario.js"
old = out.read_text() if out.exists() else ""
m = re.search(r'"busy":\s*(\[.*\])', old, re.S)
same = m is not None and json.loads(m.group(1)) == busy
if same:
    print("UNCHANGED")
    sys.exit(0)
out.write_text("window.CBC_CAL=" + json.dumps({"updated": upd, "busy": busy}) + ";\n")
print("CHANGED", len(busy), "rangos")
