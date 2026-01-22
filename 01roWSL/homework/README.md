# Teme pentru Acasă - Săptămâna 1

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## Prezentare Generală

Acest director conține temele pentru acasă aferente Săptămânii 1.
Fiecare temă include: descrierea cerințelor, script de pornire (starter), și criterii de evaluare.

---

## Teme Disponibile

### Tema 1: Raport de Configurare a Rețelei

**Obiectiv:** Documentați configurația completă a rețelei pe calculatorul personal.

**Cerințe:**
1. Rulați scriptul `exercises/tema_1_01_raport_retea.py`
2. Completați secțiunile marcate cu `TODO`
3. Analizați și interpretați rezultatele
4. Răspundeți la întrebările din șablon

**Livrabile:**
- `raport_retea.md` — raportul completat cu analiza voastră

**Criterii de Evaluare:**
| Criteriu | Punctaj |
|----------|---------|
| Completitudine date | 40% |
| Corectitudine interpretări | 30% |
| Analiză și observații proprii | 20% |
| Formatare Markdown | 10% |

---

### Tema 2: Analiza Protocoalelor TCP/UDP

**Obiectiv:** Capturați și comparați traficul TCP și UDP.

**Cerințe:**
1. Capturați trafic TCP pe portul 9090
2. Capturați trafic UDP pe portul 9091
3. Identificați handshake-ul TCP în captură
4. Comparați overhead-ul celor două protocoale

**Livrabile:**
- `tcp_analiza.pcap` — captura traficului TCP
- `udp_analiza.pcap` — captura traficului UDP
- `analiza_protocol.md` — raportul de analiză

**Criterii de Evaluare:**
| Criteriu | Punctaj |
|----------|---------|
| PCAP-uri valide și complete | 30% |
| Identificare corectă handshake | 25% |
| Comparație overhead argumentată | 30% |
| Calitate raport și concluzii | 15% |

---

## Rubrica Detaliată de Evaluare

### Tema 1: Raport de Configurare a Rețelei

| Criteriu | 0 puncte | 5 puncte | 10 puncte |
|----------|----------|----------|-----------|
| **Interfețe identificate** | Lipsă sau eronate complet | Parțial corecte (1-2 greșeli) | Toate corecte + explicații |
| **Tabela rutare explicată** | Neexplicată sau copiată | Explicație superficială | Fiecare linie explicată corect |
| **Analiză DNS** | Lipsă complet | Servere identificate fără context | + Public vs privat explicat |
| **Observații originale** | Lipsă sau evident copiate | 1-2 observații banale | 3+ observații relevante, proprii |
| **Formatare Markdown** | Haotică, greu de citit | Acceptabilă cu erori minore | Profesională, consistentă |

**Punctaj maxim:** 50 puncte (se normalizează la nota finală)

### Tema 2: Analiza Protocoalelor TCP/UDP

| Criteriu | 0 puncte | 5 puncte | 10 puncte |
|----------|----------|----------|-----------|
| **Fișiere PCAP** | Lipsă sau corupte | Prezente dar incomplete | Complete, trafic vizibil |
| **Handshake identificat** | Neidentificat | Parțial (doar SYN găsit) | SYN, SYN-ACK, ACK — toate 3 |
| **Overhead calculat** | Necalculat | Calcul cu erori | Calcul corect + explicație |
| **Comparație TCP/UDP** | Lipsă | Superficială ("TCP e mai mare") | Argumentată cu numere |
| **Concluzii** | Lipsă | Banale | Originale și corecte tehnic |

**Punctaj maxim:** 50 puncte

### Penalizări

- **Predare cu întârziere:** -10% per zi (maxim 3 zile, apoi 0)
- **Secțiuni TODO necompletate:** -5% per secțiune
- **Plagiat detectat:** 0 puncte + raportare la comisia de etică
- **Fișiere lipsă din arhivă:** -20%

### Bonusuri

- **Analiză suplimentară** (ex: TIME_WAIT explicat detaliat): +5%
- **Diagrame originale** (desenate, nu copiate): +5%
- **Comparație cu documentația oficială RFC:** +10%

---

## Lucrul în Perechi (Pair Programming)

Temele sunt **individuale**, dar discuțiile și debugging-ul în perechi sunt încurajate. Cercetările arată că Pair Programming îmbunătățește înțelegerea și reduce erorile.

### Metoda Driver-Navigator

| Rol | Ce face | Durată |
|-----|---------|--------|
| **Driver** | Scrie cod, tastează comenzi, navighează în fișiere | 15-20 min |
| **Navigator** | Verifică ce scrie Driver-ul, sugerează abordări, caută în documentație | 15-20 min |

După 15-20 minute, **schimbați rolurile**. Rotația e importantă!

### Reguli de Aur

**Navigator-ul POATE:**
- ✅ Spune "încearcă comanda `ss -tlnp`"
- ✅ Întreba "ce crezi că va afișa asta?"
- ✅ Sugera "hai să verificăm documentația pentru parametrul ăsta"
- ✅ Indica erori: "cred că lipsește un două puncte pe linia 15"

**Navigator-ul NU poate:**
- ❌ Dicta cod linie cu linie ("scrie i-p-space-a-d-d-r...")
- ❌ Lua tastatura din mâna Driver-ului
- ❌ Critica în loc să sugereze

**Driver-ul TREBUIE:**
- ✅ Să explice ce face și de ce
- ✅ Să asculte sugestiile Navigator-ului
- ✅ Să întrebe dacă ceva nu e clar

### Ce Este Permis vs. Interzis

| ✅ Permis | ❌ Interzis |
|-----------|-------------|
| Discuții despre concepte | Copierea codului final |
| Debugging împreună | Un singur om face toată munca |
| Împărtășirea resurselor găsite | Predarea aceluiași cod |
| Explicarea abordărilor | Împărțirea temei ("tu faci 1, eu fac 2") |

---

## Instrucțiuni de Predare

### Format

Arhivați livrabilele într-un fișier ZIP cu numele:
```
tema1_<nr_matricol>_<nr_tema>.zip
```

Exemplu: `tema1_123456_1.zip`

### Structura Arhivei

```
tema1_123456_1/
├── raport_retea.md
└── (alte fișiere necesare)
```

### Termen Limită

Verificați platforma de e-learning pentru data exactă de predare.

---

## Integritate Academică

### Ce este permis

✓ Consultarea documentației oficiale (man pages, RFC-uri)
✓ Utilizarea exemplelor din laborator ca punct de plecare
✓ Discuții conceptuale cu colegii ("cum funcționează TCP?")
✓ Căutarea de soluții la erori specifice pe Stack Overflow
✓ Pair Programming pentru debugging

### Ce NU este permis

✗ Copierea codului de la colegi
✗ Partajarea soluțiilor complete (nici "să vezi cum am făcut eu")
✗ Utilizarea soluțiilor de pe internet fără înțelegere
✗ Predarea muncii altcuiva
✗ Folosirea ChatGPT/Claude/AI pentru a genera soluția completă

**Clarificare AI:** Poți folosi AI pentru a înțelege concepte ("explică-mi TCP handshake"), dar NU pentru a genera raportul sau codul. Dacă nu poți explica fiecare linie din temă, nu o preda.

---

## Resurse Utile

- `../docs/rezumat_teoretic.md` — Concepte teoretice + analogii CPA
- `../docs/fisa_comenzi.md` — Comenzi utile (include diferențe PowerShell/Bash)
- `../docs/depanare.md` — Soluții la probleme comune
- `../docs/intrebari_peer_instruction.md` — Întrebări pentru auto-evaluare
- `../src/exercises/` — Exemple de cod

---

## Întrebări Frecvente

**Î: Pot folosi alt limbaj decât Python?**
R: Da, dar trebuie să documentați cum se rulează codul și ce dependențe are.

**Î: Ce fac dacă scriptul nu funcționează?**
R: Verificați `docs/depanare.md`. Dacă nu găsiți soluția, cereți ajutor la laborator (cu mesajul de eroare complet!).

**Î: Pot preda mai devreme?**
R: Da, oricând înainte de termen. Nu există bonus pentru predare timpurie.

**Î: Ce se întâmplă dacă ratez termenul?**
R: -10% pe zi, maxim 3 zile întârziere. După 3 zile: 0 puncte.

**Î: Pot lucra cu colegul?**
R: Da, pentru discuții și debugging. Tema predată trebuie să fie munca ta, scrisă de tine.

**Î: Cum știu dacă am copiat prea mult?**
R: Dacă nu poți explica verbal fiecare linie din temă, ai copiat prea mult.

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix | 2025*
