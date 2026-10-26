# Report Finanziamenti su Supabase

La versione del Report Finanziamenti da aprire fuori da claude.ai, con un link. La pagina su GitHub Pages contiene solo il codice: i mesi stanno su Supabase e si vedono solo dopo l'accesso con email e password (create da Luca su Supabase). Luca inserisce i mesi nuovi direttamente da questa pagina.

## Come è fatto
- `index.html` – la pagina pubblicata. Si genera con `python costruisci.py` dalla pagina su claude.ai (`../2026-10-26_bozza_mensile-finanziamenti.html`), che resta l'unica fonte del codice.
- `sql/01_schema.sql` – tabelle e regole di accesso: chi non è collegato non vede niente, chi è in `accessi` come `lettore` legge, come `editore` legge e scrive.
- `dati-locali/` – **esclusa da git**: lo storico con i dati reali (`02_storico.sql`) e l'elenco delle email autorizzate (`03_accessi.sql`). Non va mai pubblicata.

## Regole
- I numeri non entrano mai nel repository: né nella pagina né nella storia dei commit.
- Prima di pubblicare, chiedere conferma a Luca e verificare che senza accesso il database non restituisca niente.
- Per dare o togliere l'accesso a una persona: riga in `accessi` e utente in Authentication > Users.
