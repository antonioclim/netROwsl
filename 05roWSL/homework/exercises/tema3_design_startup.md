# Tema 3: Design Rețea pentru Startup

> Laborator Rețele de Calculatoare – Săptămâna 5
> ASE, Informatică Economică | realizat de Revolvix

**Nivel Bloom:** CREATE  
**Timp estimat:** 3-4 ore  
**Punctaj maxim:** 100 puncte

---

## Scenariu

Ești consultant de rețea pentru **CloudNine SRL**, un startup tech cu 45 de angajați care tocmai s-a mutat într-o clădire nouă cu 3 etaje.

CEO-ul îți spune:

> „La parter avem recepția și sala de conferințe. La etajul 1 stau developerii și designerii. La etajul 2 e managementul și HR-ul. În subsol avem camera de servere. Vrem să putem adăuga oameni fără să refacem totul de la zero."

**Constrângeri tehnice:**
- Buget limitat — nu poți cumpăra mai mult de un bloc /22 de la ISP
- Fiecare etaj trebuie să fie în subrețea separată (pentru securitate și management)
- Camera de servere necesită izolare strictă
- Trebuie să existe conexiuni point-to-point între routere

---

## Cerințe

### Partea A: Culegerea Cerințelor (20 puncte)

Înainte de a începe designul, trebuie să aduni mai multe informații.

**Scrie 5 întrebări pe care le-ai adresa CEO-ului** înainte de a începe proiectarea. Pentru fiecare întrebare, explică de ce este importantă pentru design.

**Format:**

| # | Întrebarea | De ce e importantă |
|---|------------|-------------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

**Exemple de direcții** (nu le copia, formulează-ți propriile întrebări):
- Creștere anticipată
- Echipamente existente
- Cerințe de securitate
- Buget
- Aplicații critice

---

### Partea B: Decizii de Design (40 puncte)

Pe baza scenariului, propune și justifică:

#### B1. Segmentarea Rețelei (10 puncte)

Câte subrețele ai crea și de ce? Ia în considerare:
- Etajele fizice
- Tipurile de dispozitive (workstations, servere, echipamente de rețea)
- Posibile VLAN-uri pentru Wi-Fi vizitatori

**Răspunsul tău:**

```
Număr total subrețele: ___

Subrețea 1: _________________ (scop: _________________)
Subrețea 2: _________________ (scop: _________________)
...
```

#### B2. Dimensionare (15 puncte)

Pentru fiecare subrețea, determină:
- Numărul de gazde necesare ACUM
- Numărul de gazde cu marjă de creștere (justifică procentul)
- Prefixul CIDR potrivit

**Format tabel:**

| Subrețea | Gazde Actuale | Creștere % | Gazde Planificate | Prefix |
|----------|---------------|------------|-------------------|--------|
| | | | | |

#### B3. FLSM sau VLSM? (15 puncte)

Alege metoda de subnetare și justifică alegerea:

- [ ] FLSM
- [ ] VLSM

**Justificare (minim 100 cuvinte):**

Consideră:
- Eficiența utilizării adreselor
- Complexitatea administrării
- Scalabilitatea
- Documentația necesară

---

### Partea C: Implementare (30 puncte)

#### C1. Alegerea Blocului de Adrese (5 puncte)

Alege un bloc de adrese private potrivit și justifică:

- [ ] 10.0.0.0/8
- [ ] 172.16.0.0/12
- [ ] 192.168.0.0/16

**Blocul ales:** _______________  
**Justificare:**

#### C2. Schema de Adresare Completă (20 puncte)

Completează tabelul cu alocarea finală:

| Segment | Descriere | Subrețea CIDR | Gateway | Prima Gazdă | Ultima Gazdă | Broadcast |
|---------|-----------|---------------|---------|-------------|--------------|-----------|
| | | | | | | |
| | | | | | | |
| | | | | | | |

**Verificare cu scriptul:**
```bash
python3 src/exercises/ex_5_02_vlsm_ipv6.py vlsm <BAZA> --cerinte <LISTA>
```

#### C3. Adrese pentru Echipamente Cheie (5 puncte)

Alocă adrese specifice pentru:

| Echipament | Subrețea | Adresă IP Alocată |
|------------|----------|-------------------|
| Router principal | | |
| Server DNS | | |
| Server DHCP | | |
| Access Point etaj 1 | | |
| Printer partajat | | |

---

### Partea D: Documentație și Prezentare (10 puncte)

#### D1. Diagramă de Rețea (7 puncte)

Creează o diagramă care să arate:
- Topologia fizică (etaje, camere)
- Subrețelele și adresele lor
- Conexiunile între routere/switch-uri
- Legenda simbolurilor

**Formate acceptate:**
- ASCII art în fișier text
- draw.io / diagrams.net (exportat ca PNG)
- Fotografie a unei scheme desenate de mână (citeț!)

#### D2. Rezumat Executiv (3 puncte)

Scrie un paragraf de 50-100 cuvinte pentru CEO (non-tehnic) care explică:
- Ce ai proiectat
- De ce e o soluție bună
- Cum permite creșterea viitoare

---

## Criterii de Evaluare

| Criteriu | Punctaj | Descriere |
|----------|---------|-----------|
| Calitatea întrebărilor | 20 | Întrebări relevante și bine justificate |
| Justificarea deciziilor | 25 | Raționament clar pentru fiecare alegere |
| Corectitudinea calculelor | 20 | Prefixe corecte, fără suprapuneri |
| Scalabilitatea soluției | 15 | Permite creștere fără refacere |
| Claritatea documentației | 15 | Diagramă clară, rezumat comprehensibil |
| Formatare și prezentare | 5 | Tabel-uri aliniate, structură logică |
| **Total** | **100** | |

---

## Notă Importantă

**Nu există o singură soluție corectă!**

Evaluarea se bazează pe:
1. Procesul de gândire demonstrat
2. Justificarea alegerilor făcute
3. Consistența internă a soluției
4. Corectitudinea tehnică a calculelor

Două soluții complet diferite pot primi același punctaj dacă ambele sunt bine justificate și corecte tehnic.

---

## Format Livrabil

- Fișier PDF sau Word
- Nume: `Tema3_NumePrenume_Grupa.pdf`
- Include toate secțiunile A-D
- Diagrama poate fi inclusă în document sau atașată separat

---

## Indicații și Resurse

### Formule Utile

```
Prefix necesar = 32 - ceil(log2(gazde_necesare + 2))

Gazde disponibile = 2^(32 - prefix) - 2
```

### Verificare cu Scripturile din Kit

```bash
# Calculează prefixul pentru un număr de gazde
python3 -c "from src.utils.net_utils import prefix_pentru_gazde; print(prefix_pentru_gazde(45))"

# Alocă VLSM
python3 src/exercises/ex_5_02_vlsm_ipv6.py vlsm 10.0.0.0/22 --cerinte 50,30,20,10,2

# Analizează o subrețea
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 10.0.0.0/26
```

### Resurse Suplimentare

- [Rezumat Teoretic](../../docs/rezumat_teorie.md) — Concepte VLSM/FLSM
- [Exemple Utilizare](../../docs/exemple_utilizare.md) — Scenarii similare
- RFC 1918 — Adrese Private

---

## Întrebări Frecvente

**Q: Pot folosi și IPv6?**  
A: Nu e obligatoriu, dar poți include o secțiune bonus pentru planul de migrare IPv6.

**Q: Câte echipamente să presupun per departament?**  
A: Folosește informațiile din scenariu (45 angajați total) și distribuie logic.

**Q: E greșit dacă aleg FLSM în loc de VLSM?**  
A: Nu, dacă justifici alegerea. Ambele pot fi soluții valide în funcție de context.

---

*Termen de predare: Conform indicațiilor de la seminar*

---

*Material didactic pentru Laborator Rețele de Calculatoare – ASE București*
