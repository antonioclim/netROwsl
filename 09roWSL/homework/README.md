# Teme pentru Acasă: Săptămâna 9

> Nivelul Sesiune (L5) și Nivelul Prezentare (L6)
> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

---

## Prezentare Generală

Această săptămână include două teme care vă vor ajuta să consolidați
cunoștințele despre protocoale binare și gestionarea sesiunilor.

| Temă | Titlu | Punctaj | Dificultate |
|------|-------|---------|-------------|
| 1 | Protocol Multi-Format | 100 puncte | Medie |
| 2 | Mașină de Stări pentru Sesiuni | 100 puncte | Medie-Avansată |

**Termen limită**: Următoarea sesiune de laborator

---

## Tema 1: Protocol Multi-Format (100 puncte)

### Descriere

Implementați un protocol binar care suportă mai multe tipuri de mesaje:
TEXT, INTEGER și BLOB. Fiecare mesaj trebuie să aibă un header standardizat
cu validare CRC-32.

### Cerințe

1. **Structura Header (40 puncte)**
   - Octeți magic: `b'MFMT'` (4 octeți)
   - Versiune: 1 (1 octet)
   - Tip mesaj: TEXT=1, INTEGER=2, BLOB=3 (1 octet)
   - Lungime payload (4 octeți, network byte order)
   - CRC-32 al payload-ului (4 octeți, network byte order)

2. **Funcția `impacheteaza_mesaj()` (30 puncte)**
   - Primește tipul și datele
   - Returnează mesajul binar complet (header + payload)
   - Calculează CRC-32 corect

3. **Funcția `despachetaza_mesaj()` (30 puncte)**
   - Primește mesajul binar
   - Verifică octeții magic și versiunea
   - Verifică CRC-32
   - Returnează tipul și payload-ul decodat

### Fișier

Completați implementarea în: `homework/exercises/tema_9_01.py`

### Exemple de Utilizare

```python
# Împachetare mesaj text
mesaj = impacheteaza_mesaj(TIP_TEXT, "Salut!")
print(mesaj.hex())

# Despachetare
tip, date = despachetaza_mesaj(mesaj)
print(f"Tip: {tip}, Date: {date}")
```

---

## Tema 2: Mașină de Stări pentru Sesiuni (100 puncte)

### Descriere

Implementați o mașină de stări finite (FSM) pentru gestionarea sesiunilor
de tip FTP. Mașina trebuie să valideze tranzițiile între stări și să
mențină un istoric al stărilor.

### Cerințe

1. **Stări definite (20 puncte)**
   - DECONECTAT
   - CONECTAT
   - AUTENTIFICARE
   - AUTENTIFICAT
   - TRANSFER
   - EROARE

2. **Tranzițiile valide (40 puncte)**
   ```
   DECONECTAT → CONECTAT (conectare)
   CONECTAT → AUTENTIFICARE (user)
   AUTENTIFICARE → AUTENTIFICAT (pass corect)
   AUTENTIFICARE → EROARE (pass greșit)
   AUTENTIFICAT → TRANSFER (retr/stor)
   TRANSFER → AUTENTIFICAT (transfer complet)
   * → DECONECTAT (quit/timeout)
   EROARE → DECONECTAT (reset)
   ```

3. **Funcționalități (40 puncte)**
   - `tranzitie(eveniment)`: Schimbă starea dacă tranziția e validă
   - `stare_curenta()`: Returnează starea curentă
   - `istoric()`: Returnează lista stărilor anterioare
   - `este_autentificat()`: Verifică dacă sesiunea e autentificată

### Fișier

Completați implementarea în: `homework/exercises/tema_9_02.py`

### Exemple de Utilizare

```python
sesiune = MasinaStariSesiune()

# Simulare flux FTP
sesiune.tranzitie("conectare")
print(sesiune.stare_curenta())  # CONECTAT

sesiune.tranzitie("user")
sesiune.tranzitie("pass_corect")
print(sesiune.este_autentificat())  # True

sesiune.tranzitie("retr")
sesiune.tranzitie("transfer_complet")

sesiune.tranzitie("quit")
print(sesiune.istoric())  # Lista tuturor stărilor
```

---

## Criterii de Evaluare

### Tema 1: Protocol Multi-Format

| Criteriu | Puncte |
|----------|--------|
| Structura header corectă | 20 |
| Network byte order | 10 |
| CRC-32 corect | 10 |
| Funcția impacheteaza_mesaj | 30 |
| Funcția despachetaza_mesaj | 20 |
| Tratare erori | 10 |
| **Total** | **100** |

### Tema 2: Mașină de Stări

| Criteriu | Puncte |
|----------|--------|
| Definire stări | 20 |
| Tranzițiile implementate corect | 25 |
| Validare tranziții invalide | 15 |
| Istoric funcțional | 15 |
| Metode helper | 15 |
| Tratare erori | 10 |
| **Total** | **100** |

---

## Instrucțiuni de Predare

1. **Completați fișierele** din `homework/exercises/`
2. **Testați local**:
   ```bash
   python homework/exercises/tema_9_01.py
   python homework/exercises/tema_9_02.py
   ```
3. **Verificați cu testele**:
   ```bash
   python -m pytest homework/exercises/ -v
   ```
4. **Pregătiți pentru predare**:
   - Asigurați-vă că codul rulează fără erori
   - Adăugați comentarii explicative
   - Respectați formatul cerut

---

## Resurse Utile

- `docs/sumar_teorie.md` - Concepte teoretice
- `docs/fisa_comenzi.md` - Referință rapidă pentru struct și CRC
- `src/exercises/ex_9_01_endianness.py` - Exemplu endianness
- `src/exercises/ex_9_02_pseudo_ftp.py` - Exemplu protocol FTP

---

## Întrebări Frecvente

**Î: Pot folosi biblioteci externe?**
R: Nu, folosiți doar modulele standard Python (struct, zlib, etc.)

**Î: Ce se întâmplă dacă CRC-ul nu se potrivește?**
R: Aruncați o excepție ValueError cu un mesaj descriptiv.

**Î: Trebuie să gestionez timeout-uri în FSM?**
R: Da, orice eveniment de timeout trebuie să ducă la DECONECTAT.

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
