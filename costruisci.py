"""Costruisce index.html per GitHub Pages: il Report Finanziamenti con i dati letti da Supabase.

La pagina contiene solo il codice. I mesi stanno su Supabase e si vedono solo dopo l'accesso con
email e password; le regole del database (sql/01_schema.sql) decidono chi legge e chi scrive.
La chiave qui sotto è quella pubblica ("publishable"): è fatta per stare nel browser.

Uso, dalla cartella report-finanziamenti-supabase:
    1. python costruisci.py
    2. git add index.html && git commit -m "..." && git push
Da rifare solo quando cambia la pagina su claude.ai, non quando si inserisce un mese.
"""
import json
from pathlib import Path

SUPABASE = {"url": "https://xemttyxuzkxvcyvqnggo.supabase.co", "chiave": "sb_publishable_N0OXDDubt-t-Htt1dMbjbQ_nJLhknxS"}
LIBRERIA = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.57.4/dist/umd/supabase.js"

QUI = Path(__file__).resolve().parent
BOZZA = QUI.parent / "2026-10-26_bozza_mensile-finanziamenti.html"
USCITA = QUI / "index.html"

testo = BOZZA.read_text(encoding="utf-8")
blocco = f'<script src="{LIBRERIA}"></script>\n<script>window.SUPABASE_CONFIG = {json.dumps(SUPABASE)};</script>\n'
punto_script = testo.index("<script>\n(function(){")
testo = testo[:punto_script] + blocco + testo[punto_script:]
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
print(f"Scritto {USCITA.name}: {len(pagina):,} caratteri, nessun dato incorporato")
