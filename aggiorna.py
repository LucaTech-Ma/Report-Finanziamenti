"""Costruisce index.html per GitHub Pages: la pagina del Report Finanziamenti con i dati incorporati.

La pagina su claude.ai legge i mesi dal suo database. Fuori da claude.ai quel database non c'è,
quindi qui i mesi vengono incorporati nella pagina come copia in sola lettura.

Uso, dalla cartella report-finanziamenti-github:
    1. esporta i mesi aggiornati dal report su claude.ai in export/mesi/ (chiedilo a Claude)
    2. python aggiorna.py
    3. git add index.html && git commit -m "Dati aggiornati al ..." && git push
"""
import json
from datetime import date
from pathlib import Path

QUI = Path(__file__).resolve().parent
BOZZA = QUI.parent / "2026-10-26_bozza_mensile-finanziamenti.html"
EXPORT = QUI / "export" / "mesi"
USCITA = QUI / "index.html"

mesi = []
for f in sorted(EXPORT.glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    d = d.get("data", d)  # tollera sia il documento semplice sia {id, data, version}
    if isinstance(d, dict) and d.get("mese"):
        mesi.append(d)
if not mesi:
    raise SystemExit("Nessun mese trovato in export/mesi: esporta prima i dati.")

oggi = date.today()
mesi_it = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
dati = {"generato": f"{oggi.day} {mesi_it[oggi.month-1]} {oggi.year}", "mesi": mesi}
blocco_dati = "<script>window.DATI_STATICI = " + json.dumps(dati, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";</script>\n"

testo = BOZZA.read_text(encoding="utf-8")
punto_script = testo.index("<script>\n(function(){")
testo = testo[:punto_script] + blocco_dati + testo[punto_script:]
inizio_corpo = testo.index('<div class="wrap">')
testa, corpo = testo[:inizio_corpo].strip(), testo[inizio_corpo:].strip()

pagina = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
{testa}
</head>
<body>
{corpo}
</body>
</html>
"""
USCITA.write_text(pagina, encoding="utf-8")
print(f"Scritto {USCITA.name}: {len(mesi)} mesi, da {mesi[0]['mese']} a {mesi[-1]['mese']}, {len(pagina):,} caratteri")
