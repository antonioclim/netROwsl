# Tema 1: Proiectare Rețea Corporativă cu VLSM

> Laborator Rețele de Calculatoare – Săptămâna 5
> ASE, Informatică Economică | realizat de Revolvix

## Obiective

- Aplicarea tehnicii VLSM pentru proiectarea unei scheme de adresare eficiente
- Documentarea deciziilor de proiectare și justificarea alegerilor
- Calcularea și verificarea corectitudinii alocărilor

## Scenariu

Compania **TechVision SRL** a achiziționat blocul de adrese `172.20.0.0/22` și trebuie să proiecteze schema de adresare pentru cele 6 departamente din sediul central:

| Departament | Abreviere | Cerință gazde |
|-------------|-----------|---------------|
| Dezvoltare Software | DEV | 120 |
| Vânzări și Marketing | SALES | 55 |
| Resurse Umane | HR | 25 |
| Financiar-Contabilitate | FIN | 30 |
| IT și Suport | IT | 15 |
| Management | MGT | 8 |

**Cerințe suplimentare:**
- 2 legături point-to-point între routere (2 gazde fiecare)
- Spațiu rezervat pentru extindere viitoare (minim 100 adrese)

## Cerințe

### Partea A: Analiză preliminară (20 puncte)

1. Calculați spațiul total de adrese disponibil în blocul `172.20.0.0/22`
2. Calculați numărul total de adrese necesare pentru toate cerințele
3. Verificați dacă blocul este suficient de mare

### Partea B: Schema VLSM (40 puncte)

1. Aplicați algoritmul VLSM pentru a aloca subrețele tuturor departamentelor
2. Pentru fiecare subrețea, documentați:
   - Adresa de rețea și prefixul
   - Masca de rețea
   - Adresa de broadcast
   - Intervalul de gazde utilizabile
   - Prima și ultima adresă de gazdă

### Partea C: Documentație (20 puncte)

Completați tabelul următor:

| Nr. | Departament | Cerință | Subrețea | Prefix | Disponibile | Eficiență |
|-----|-------------|---------|----------|--------|-------------|-----------|
| 1 | | | | | | |
| 2 | | | | | | |
| ... | | | | | | |

Calculați eficiența globală a schemei.

### Partea D: Verificare și Diagramă (20 puncte)

1. Verificați că subrețelele nu se suprapun
2. Desenați o diagramă a rețelei care arată:
   - Toate subrețelele
   - Conexiunile între routere
   - Intervalele de adrese

## Format Livrabil

- Fișier PDF sau Word cu toate răspunsurile
- Numele fișierului: `Tema1_NumePrenume_Grupa.pdf`

## Criterii de Evaluare

| Criteriu | Punctaj |
|----------|---------|
| Corectitudinea calculelor VLSM | 40 |
| Documentație completă | 20 |
| Justificarea deciziilor | 20 |
| Diagramă clară și corectă | 15 |
| Formatare și prezentare | 5 |
| **Total** | **100** |

## Indicații

1. Începeți prin a sorta cerințele descrescător
2. Pentru fiecare cerință, calculați prefixul minim necesar
3. Alocați subrețelele în ordine, asigurându-vă că fiecare începe la o graniță validă
4. Puteți folosi scripturile din kit pentru verificare:
   ```powershell
   python src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.20.0.0/22 --cerinte 120,55,30,25,15,8,2,2
   ```

## Exemplu de Calcul

Pentru cerința de 120 gazde:
- Adrese necesare: 120 + 2 = 122
- Putere de 2 următoare: 128 = 2^7
- Biți gazdă: 7
- Prefix: 32 - 7 = /25
- Gazde disponibile: 126

---

*Termen de predare: Conform indicațiilor de la seminar*
