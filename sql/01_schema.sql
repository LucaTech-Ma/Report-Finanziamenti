-- Report Finanziamenti: tabelle e regole di accesso.
-- Da incollare una volta in Supabase > SQL Editor > New query, poi "Run".
-- Si può rilanciare senza danni: crea solo ciò che manca e riscrive le regole.

-- Chi può entrare. Una riga per persona: 'editore' legge e scrive, 'lettore' legge soltanto.
create table if not exists public.accessi (
  email text primary key check (email = lower(email)),
  ruolo text not null check (ruolo in ('editore', 'lettore'))
);

-- Un mese per riga: il documento è lo stesso della versione su claude.ai (brand, gruppo, fonte, ...).
create table if not exists public.mesi (
  mese text primary key check (mese ~ '^\d{4}-(0[1-9]|1[0-2])$'),
  dati jsonb not null,
  aggiornato timestamptz not null default now(),
  aggiornato_da text default lower(auth.jwt() ->> 'email')
);

-- Il ruolo di chi è collegato, letto dalla tabella accessi. null = nessun accesso.
create or replace function public.mio_ruolo() returns text
language sql stable security definer set search_path = public as $$
  select ruolo from public.accessi where email = lower(auth.jwt() ->> 'email')
$$;
revoke all on function public.mio_ruolo() from public, anon;
grant execute on function public.mio_ruolo() to authenticated;

-- Senza regole esplicite nessuno vede niente: si accende la sicurezza per riga e si toglie tutto a chi non è collegato.
alter table public.accessi enable row level security;
alter table public.mesi enable row level security;
revoke all on public.accessi, public.mesi from anon;
grant select on public.accessi to authenticated;
grant select, insert, update, delete on public.mesi to authenticated;

drop policy if exists "vedo solo il mio accesso" on public.accessi;
create policy "vedo solo il mio accesso" on public.accessi
  for select to authenticated using (email = lower(auth.jwt() ->> 'email'));

drop policy if exists "leggono editori e lettori" on public.mesi;
create policy "leggono editori e lettori" on public.mesi
  for select to authenticated using (public.mio_ruolo() in ('editore', 'lettore'));

drop policy if exists "inserisce solo l'editore" on public.mesi;
create policy "inserisce solo l'editore" on public.mesi
  for insert to authenticated with check (public.mio_ruolo() = 'editore');

drop policy if exists "modifica solo l'editore" on public.mesi;
create policy "modifica solo l'editore" on public.mesi
  for update to authenticated using (public.mio_ruolo() = 'editore') with check (public.mio_ruolo() = 'editore');

drop policy if exists "elimina solo l'editore" on public.mesi;
create policy "elimina solo l'editore" on public.mesi
  for delete to authenticated using (public.mio_ruolo() = 'editore');

-- A ogni modifica si aggiornano data e autore.
create or replace function public.segna_modifica() returns trigger
language plpgsql set search_path = public as $$
begin
  new.aggiornato := now();
  new.aggiornato_da := lower(auth.jwt() ->> 'email');
  return new;
end $$;
drop trigger if exists segna_modifica on public.mesi;
create trigger segna_modifica before update on public.mesi
  for each row execute function public.segna_modifica();
