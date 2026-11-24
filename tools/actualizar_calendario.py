#!/usr/bin/env python3
"""Genera atlantida/calendario.js a partir del iCal de Airbnb.

Uso: python3 tools/actualizar_calendario.py <archivo.ics> [fecha_AAAA-MM-DD]
Toma todas las reservas y bloqueos (DTSTART..DTEND, DTEND exclusivo) y los
publica como noches ocupadas, sin nombres ni códigos.
Siempre reescribe el archivo con la fecha y hora de sincronización e imprime CHANGED.
"""
import json, re, sys, datetime, pathlib

ics = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
ics = re.sub(r"\r?\n[ \t]", "", ics)  # desplegar líneas continuadas
# Fecha y hora de la sincronización, en hora de Uruguay (UTC-3, sin horario de verano).
# El segundo argumento (fecha) se acepta por compatibilidad; la hora se toma del reloj.
uy = datetime.timezone(datetime.timedelta(hours=-3))
upd = datetime.datetime.now(uy).strftime("%Y-%m-%dT%H:%M-03:00")

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
# Siempre se reescribe para que la página muestre la fecha y hora de la última sincronización.
out.write_text("window.CBC_CAL=" + json.dumps({"updated": upd, "busy": busy}) + ";\n")
print("CHANGED", len(busy), "rangos", "(fechas iguales, solo hora de sincronización)" if same else "(fechas nuevas)")
