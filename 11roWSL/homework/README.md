# Teme pentru Acasă - Săptămâna 11

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

## Prezentare Generală

Acest director conține temele pentru săptămâna 11, care extind conceptele de echilibrare a sarcinii și protocoale DNS studiate în laborator.

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
- Instrucțiuni de utilizare
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

---

## Întrebări Frecvente

**Î: Pot folosi biblioteci externe?**
R: Da, pentru DNS puteți folosi `dnspython` ca referință, dar implementarea de bază trebuie făcută manual.

**Î: Ce înregistrări DNS trebuie să suport?**
R: Minim A și AAAA. MX și NS sunt bonus.

**Î: Cum testez health check-urile?**
R: Opriți manual un backend și observați cum echiliborul îl marchează ca nesănătos.

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
