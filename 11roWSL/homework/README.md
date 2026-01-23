# Teme pentru Acasă - Săptămâna 11

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

> 📚 Ai nevoie de ajutor cu conceptele? Vezi [Analogii pentru Concepte](../docs/analogii_concepte.md).

## Prezentare Generală

Acest director conține temele pentru săptămâna 11, care extind conceptele de echilibrare a sarcinii și protocoale DNS studiate în laborator.

---

## Tema 1: Echilibror Extins cu Verificări Active de Stare

**Fișier:** `exercises/hw_11_01.py`

**Punctaj total:** 100 puncte

### Descriere

Extindeți echiliborul de sarcină Python pentru a suporta:

1. **Verificări active de stare (40 puncte)**
   - Verificări periodice HTTP către backend-uri
   - Marcare ca "nesănătos" după 3 eșecuri consecutive
   - Marcare ca "sănătos" după 2 succese consecutive
   - Interval configurabil (implicit: 5 secunde)

2. **Weighted Round Robin (30 puncte)**
   - Acceptă ponderi prin linie de comandă
   - Distribuie traficul proporțional cu ponderile
   - Exemplu: `--weights 3,2,1` pentru 50%/33%/17%

3. **Endpoint de statistici (20 puncte)**
   - `/stats` returnează JSON cu:
     - Total cereri procesate
     - Cereri per backend
     - Starea de sănătate a fiecărui backend
     - Timpul de funcționare

4. **Degradare grațioasă (10 puncte)**
   - Returnează HTTP 503 când toate backend-urile sunt indisponibile
   - Mesaj clar de eroare
   - Continuă să verifice pentru recuperare

### Exemple de Utilizare

```powershell
# Pornește cu ponderi și health checks
python hw_11_01.py --backends localhost:8081,localhost:8082,localhost:8083 --weights 3,2,1 --health-interval 5

# Accesează statisticile
curl http://localhost:8080/stats
```

### Rezultat Așteptat `/stats`

```json
{
  "uptime_seconds": 3600,
  "total_requests": 15000,
  "backends": [
    {
      "host": "localhost",
      "port": 8081,
      "weight": 3,
      "healthy": true,
      "requests": 7500,
      "active_connections": 2
    },
    {
      "host": "localhost",
      "port": 8082,
      "weight": 2,
      "healthy": true,
      "requests": 5000,
      "active_connections": 1
    },
    {
      "host": "localhost",
      "port": 8083,
      "weight": 1,
      "healthy": false,
      "requests": 2500,
      "active_connections": 0
    }
  ]
}
```

---

## Tema 2: Resolver DNS cu Cache

**Fișier:** `exercises/hw_11_02.py`

**Punctaj total:** 100 puncte

### Descriere

Implementați un resolver DNS local care memorează răspunsurile:

1. **Server DNS UDP (30 puncte)**
   - Ascultă pe portul 5353
   - Parsează interogări DNS conform RFC 1035
   - Suportă tipurile A, AAAA, MX, NS

2. **Implementare cache (30 puncte)**
   - Stochează răspunsurile cu TTL
   - Elimină automat înregistrările expirate
   - Contorizează hit-uri și miss-uri

3. **Rezoluție upstream (25 puncte)**
   - Redirecționează interogările necache-uite către 8.8.8.8
   - Parsează răspunsurile și le memorează
   - Gestionează timeout-urile grațios

4. **Statistici și management (15 puncte)**
   - Total interogări procesate
   - Raport hit/miss
   - Golire cache prin semnal (SIGUSR1)
   - Afișare conținut cache

### Exemple de Utilizare

```powershell
# Pornește resolver-ul
python hw_11_02.py --listen 0.0.0.0:5353 --upstream 8.8.8.8

# Testează cu dig (din altă fereastră)
dig @localhost -p 5353 google.com A

# Afișează statisticile
python hw_11_02.py --stats

# Golește cache-ul (Linux)
kill -SIGUSR1 <PID>
```

### Rezultat Așteptat

```
[DNS Resolver] Ascultă pe 0.0.0.0:5353
[DNS Resolver] Upstream: 8.8.8.8:53
[DNS Resolver] Cache activat (max TTL: 3600s)

[Query] google.com A din 127.0.0.1
[Cache MISS] Interogare upstream...
[Cache] Stocat google.com A (TTL: 299s)
[Response] 142.250.185.78

[Query] google.com A din 127.0.0.1
[Cache HIT] google.com A
[Response] 142.250.185.78

[Stats] Total: 2 | Hits: 1 (50%) | Miss: 1 (50%)
```

---

## Exerciții Suplimentare de Evaluare și Creare

> Aceste exerciții dezvoltă gândirea critică și abilitățile de proiectare.

### E1. Evaluare Algoritmi (Nivel: EVALUATE)

**Punctaj:** 15 puncte bonus

**Scenariu:** Un magazin online are următorul profil de trafic:
- 60% cereri rapide (listare produse) — ~50ms răspuns
- 30% cereri medii (detalii produs) — ~200ms răspuns  
- 10% cereri lente (checkout cu plată) — ~2000ms răspuns

**Cerință:** Analizează și justifică care algoritm de echilibrare este mai potrivit: Round Robin sau Least Connections?

**Livrabil:** Document de 1-2 pagini cu:
1. Analiza comportamentului fiecărui algoritm pentru acest scenariu
2. Simulare cu date concrete (distribuția cererilor pe 3 backend-uri)
3. Recomandare finală cu justificare tehnică
4. Identificarea cazurilor în care Round Robin ar fi totuși preferabil

<details>
<summary>Ghid de evaluare</summary>

**Răspuns așteptat:**

**Least Connections** este superior pentru acest scenariu deoarece:
1. Cererile au durată foarte variabilă (50ms vs 2000ms = 40x diferență)
2. Round Robin ar supraîncărca backend-urile care primesc multe checkout-uri
3. Least Connections adaptează distribuția în timp real la încărcare

**Round Robin ar fi OK dacă:**
- Toate cererile ar avea durată similară
- Backend-urile ar avea capacități diferite (cu ponderi)
- Simplitatea implementării ar fi prioritară

**Criterii de punctare:**
- Analiză corectă: 5 puncte
- Simulare cu date: 5 puncte
- Justificare clară: 5 puncte
</details>

---

### E2. Proiectare Arhitectură (Nivel: CREATE)

**Punctaj:** 20 puncte bonus

**Cerință:** Proiectează o arhitectură de echilibrare pentru o aplicație cu:
- 50.000 cereri/secundă în vârf
- 99.9% disponibilitate (max 8.7 ore downtime/an)
- Clienți din Europa și Asia

**Livrabil:** Document cu:

1. **Diagramă arhitectură** (ASCII sau imagine)
   - Câte niveluri de load balancing?
   - Câte servere la fiecare nivel?
   - Cum sunt distribuite geografic?

2. **Justificare pentru fiecare decizie:**
   - Ce algoritm la fiecare nivel și de ce?
   - Cum asiguri failover între regiuni?
   - Ce se întâmplă când o regiune cade complet?

3. **Calcule de capacitate:**
   - Câte cereri poate gestiona fiecare server?
   - Care e marja de siguranță?

<details>
<summary>Ghid de evaluare</summary>

**Elemente așteptate:**

1. **Multi-nivel:** DNS geographic + LB regional + LB local
2. **Multi-regiune:** Cel puțin 2 regiuni (EU + Asia)
3. **Redundanță:** Minimum 3 servere per punct critic
4. **Failover:** DNS cu health checks sau Anycast

**Criterii de punctare:**
- Diagrama completă: 5 puncte
- Justificare algoritmi: 5 puncte
- Failover design: 5 puncte
- Calcule realiste: 5 puncte
</details>

---

### E3. Analiză Comparativă (Nivel: ANALYSE)

**Punctaj:** 15 puncte bonus

**Cerință:** Rulează următoarele teste și analizează rezultatele:

```bash
# Test 1: Round Robin cu backend-uri egale
# (decomentează round_robin în nginx.conf)
for i in {1..100}; do curl -s http://localhost:8080/ | grep -o "web[0-9]"; done | sort | uniq -c

# Test 2: IP Hash cu același client
for i in {1..100}; do curl -s http://localhost:8080/ | grep -o "web[0-9]"; done | sort | uniq -c

# Test 3: Least Connections cu un backend lent
# (adaugă --delay 0.5 la ex_11_01_backend.py pentru web3)
```

**Livrabil:** Raport cu:
1. Rezultatele fiecărui test (output-uri concrete)
2. Explicație pentru fiecare rezultat
3. Grafic cu distribuția cererilor
4. Concluzii despre când să folosești fiecare algoritm

**Întrebări de analiză:**
- Care test arată distribuție uniformă? De ce?
- Care test trimite totul la un singur backend? De ce?
- Cum se comportă least_conn când web3 are latență mare?
- Ce s-ar întâmpla cu IP Hash dacă ai 1000 de clienți diferiți?

---

## Provocări Bonus

### Bonus 1: Connection Pooling (+10 puncte)

Implementați reutilizarea conexiunilor HTTP în echilibror:

- Mențineți conexiuni deschise către backend-uri
- Configurați dimensiunea pool-ului
- Gestionați timeout-urile și reconectarea

### Bonus 2: DNS over HTTPS (DoH) (+10 puncte)

Extindeți resolver-ul DNS pentru a suporta DoH:

- Suport pentru https://cloudflare-dns.com/dns-query
- Format wireformat sau JSON
- Configurabil prin linie de comandă

### Bonus 3: Circuit Breaker Pattern (+10 puncte)

Implementați pattern-ul circuit breaker în echilibror:

- Stări: CLOSED, OPEN, HALF-OPEN
- Deschidere după N eșecuri
- Testare periodică în starea HALF-OPEN
- Înregistrare tranziții

---

## Criterii de Evaluare

### Funcționalitate (60%)

- Codul rulează fără erori
- Toate cerințele sunt implementate
- Comportament corect în cazuri limită

### Calitatea Codului (20%)

- Cod curat și organizat
- Nume descriptive pentru variabile și funcții
- Comentarii explicative unde e necesar
- Tratarea erorilor

### Gestionare Erori (10%)

- Input invalid gestionat corect
- Timeout-uri implementate
- Mesaje de eroare utile

### Raport (10%)

- Descriere a implementării
- Decizii de proiectare explicate
- Instrucțiuni de folosire
- Rezultate ale testelor

---

## Termen Limită și Predare

- **Termen limită:** 2 săptămâni de la laborator
- **Format:** Arhivă ZIP cu codul sursă și raportul
- **Denumire:** `Nume_Prenume_Grupa_S11.zip`

### Conținut Arhivă

```
Nume_Prenume_Grupa_S11/
├── hw_11_01.py
├── hw_11_02.py
├── raport.pdf
└── README.txt (instrucțiuni de rulare)
```

---

## Resurse Utile

- RFC 1035: Domain Names - Implementation and Specification
- Python `struct` module: https://docs.python.org/3/library/struct.html
- Python `socket` module: https://docs.python.org/3/library/socket.html
- Pattern Circuit Breaker: https://martinfowler.com/bliki/CircuitBreaker.html
- [Analogii pentru Concepte](../docs/analogii_concepte.md) — Explicații vizuale

---

## Întrebări Frecvente

**Î: Pot folosi biblioteci externe?**
R: Da, pentru DNS puteți folosi `dnspython` ca referință, dar implementarea de bază trebuie făcută manual.

**Î: Ce înregistrări DNS trebuie să suport?**
R: Minim A și AAAA. MX și NS sunt bonus.

**Î: Cum testez health check-urile?**
R: Opriți manual un backend și observați cum echiliborul îl marchează ca nesănătos.

**Î: Exercițiile E1-E3 sunt obligatorii?**
R: Nu, sunt bonus pentru cei care vor să aprofundeze. Temele 1 și 2 sunt obligatorii.

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
