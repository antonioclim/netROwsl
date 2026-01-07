# Teme pentru Acasă: Săptămâna 4

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

## Prezentare Generală

Acest director conține temele pentru săptămâna 4 a laboratorului de Rețele de Calculatoare.
Temele sunt concepute pentru a consolida conceptele învățate în timpul laboratorului.

## Structura Directorului

```
homework/
├── README.md           # Acest fișier
├── exercises/          # Șabloane pentru exerciții
│   ├── tema_4_01.py   # Tema 1: Protocol TEXT extins
│   └── tema_4_02.py   # Tema 2: Simulator senzori
└── solutions/          # Director pentru soluții (gol inițial)
```

## Temele

### Tema 4.01: Protocol TEXT Extins
**Fișier:** `exercises/tema_4_01.py`

**Obiectiv:** Extindeți clientul protocolului TEXT cu funcționalități suplimentare.

**Cerințe:**
1. Implementați comenzile suplimentare:
   - `EXPIRE <cheie> <secunde>`: Setează un TTL pentru o cheie
   - `TTL <cheie>`: Returnează timpul rămas până la expirare
   - `INCR <cheie>`: Incrementează o valoare numerică
   - `DECR <cheie>`: Decrementează o valoare numerică

2. Adăugați logging pentru toate operațiunile
3. Implementați reconectare automată în caz de deconectare
4. Adăugați suport pentru comenzi din fișier batch

**Punctaj:** 25 puncte

### Tema 4.02: Simulator Rețea Senzori
**Fișier:** `exercises/tema_4_02.py`

**Obiectiv:** Creați un simulator complet pentru o rețea de senzori IoT.

**Cerințe:**
1. Implementați un generator de senzori virtuali care:
   - Creează N senzori cu ID-uri unice
   - Fiecare senzor trimite citiri la intervale configurabile
   - Temperaturile variază realist în funcție de "locație"

2. Implementați analiza datelor primite:
   - Calcularea mediei temperaturii per senzor
   - Detectarea valorilor anormale (outliers)
   - Generarea unui raport sumar

3. Adăugați vizualizare (opțional, bonus):
   - Grafic temperatură în timp
   - Hartă termică a senzorilor

**Punctaj:** 30 puncte (+ 10 puncte bonus pentru vizualizare)

## Instrucțiuni de Predare

1. **Completați** fișierele din `exercises/`
2. **Testați** implementările folosind scripturile de test
3. **Copiați** fișierele completate în `solutions/`
4. **Arhivați** și predați conform instrucțiunilor din Moodle

## Termen Limită

Consultați pagina cursului din Moodle pentru termenul limită actualizat.

## Criterii de Evaluare

| Criteriu | Puncte |
|----------|--------|
| Funcționalitate corectă | 50% |
| Calitatea codului | 20% |
| Documentare și comentarii | 15% |
| Gestionarea erorilor | 15% |

## Resurse Utile

- `docs/theory_summary.md` - Rezumat teoretic
- `docs/commands_cheatsheet.md` - Referință comenzi
- `src/apps/` - Implementări de referință

## Întrebări și Asistență

Pentru întrebări legate de teme:
1. Consultați mai întâi documentația din `docs/`
2. Verificați secțiunea FAQ din Moodle
3. Postați pe forumul cursului

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
