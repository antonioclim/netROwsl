# Săptămâna 8: Nivelul Transport — Server HTTP și Proxy Invers

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică
> 
> de Revolvix

## Prezentare Generală

Nivelul transport reprezintă fundamentul comunicării fiabile între aplicații în rețelele de calculatoare. Acest nivel asigură transferul de date între procesele care rulează pe gazde diferite, oferind servicii de multiplexare, demultiplexare și, în cazul TCP, transfer fiabil de date cu control al fluxului și al congestiei.

În cadrul acestei sesiuni de laborator, vom explora implementarea practică a protocoalelor de nivel transport prin construirea unui server HTTP de la zero și configurarea unui proxy invers cu echilibrare a încărcării. Aceste exerciții demonstrează modul în care protocoalele de nivel aplicație se bazează pe serviciile oferite de TCP pentru a realiza comunicarea client-server.

Infrastructura de laborator utilizează Docker pentru a crea un mediu izolat și reproductibil, cu nginx ca proxy invers și mai multe servere backend Python. Această arhitectură reflectă configurațiile reale din producție și oferă experiență practică cu algoritmi de echilibrare a încărcării.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** componentele cheie ale protocoalelor TCP și UDP și rolurile acestora în comunicarea de rețea
2. **Explicați** procesul de stabilire a conexiunii TCP (three-way handshake) și semnificația fiecărui pas
3. **Implementați** un server HTTP de bază folosind socket-uri Python care gestionează cererile GET și HEAD
4. **Analizați** traficul de rețea folosind Wireshark pentru a observa segmentele TCP și mesajele HTTP
5. **Construiți** un proxy invers simplu cu echilibrare round-robin între mai multe servere backend
6. **Evaluați** diferite algoritmi de echilibrare a încărcării și compromisurile acestora

## Cerințe Preliminare

### Cunoștințe Necesare

- Înțelegerea modelului TCP/IP și a stratificării pe nivele
- Familiaritate cu programarea în Python (socket-uri, threading)
- Cunoștințe de bază despre protocolul HTTP (metode, coduri de stare, antete)
- Experiență cu linia de comandă și comenzi de bază Linux

### Cerințe Software

- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau ulterior
- Git (recomandat)

### Cerințe Hardware

- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Prima Configurare (Se Rulează O Singură Dată)

```powershell
# Deschideți PowerShell ca Administrator
cd WEEK8_WSLkit_RO

# Verificați cerințele preliminare
python setup/verifica_mediu.py

# Dacă apar probleme, rulați asistentul de instalare
python setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```powershell
# Porniți toate serviciile
python scripts/porneste_laborator.py

# Verificați că totul funcționează
python scripts/porneste_laborator.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | https://localhost:9443 | Se setează la prima accesare |
| Proxy HTTP | http://localhost:8080 | - |
| Proxy HTTPS | https://localhost:8443 | Certificat auto-semnat |
| Backend 1 | intern: 172.28.8.21:8080 | - |
| Backend 2 | intern: 172.28.8.22:8080 | - |
| Backend 3 | intern: 172.28.8.23:8080 | - |

## Exerciții de Laborator

### Exercițiul 1: Server HTTP de Bază

**Obiectiv:** Implementarea unui server HTTP simplu care servește fișiere statice.

**Durată:** 45-60 minute

**Fișier:** `src/exercises/ex_8_01_server_http.py`

**Pași:**

1. Deschideți fișierul exercițiului și examinați structura codului
2. Implementați funcția `parseaza_cerere()` pentru a extrage metoda, calea și versiunea HTTP
3. Implementați funcția `este_cale_sigura()` pentru a preveni traversarea directoarelor
4. Implementați funcția `serveste_fisier()` pentru a citi și returna conținutul fișierelor
5. Implementați funcția `construieste_raspuns()` pentru a formata răspunsul HTTP
6. Testați serverul cu curl și browser

**Verificare:**
```bash
# Porniți serverul
python src/exercises/ex_8_01_server_http.py

# Într-un alt terminal, testați
curl -i http://localhost:8888/hello.txt
curl -I http://localhost:8888/index.html
```

**Rezultat Așteptat:**
- Răspuns 200 OK pentru fișiere existente
- Răspuns 404 Not Found pentru fișiere inexistente
- Răspuns 403 Forbidden pentru încercări de traversare a directoarelor

### Exercițiul 2: Proxy Invers cu Echilibrare Round-Robin

**Obiectiv:** Implementarea unui proxy invers care distribuie cererile între mai multe backend-uri.

**Durată:** 60-75 minute

**Fișier:** `src/exercises/ex_8_02_proxy_invers.py`

**Pași:**

1. Examinați clasa `EchilibratorRoundRobin` și înțelegeți algoritmul
2. Implementați metoda `urmatorul_backend()` pentru selecția ciclică
3. Implementați funcția `redirectioneaza_cerere()` pentru proxy-ul către backend
4. Adăugați antetul `X-Forwarded-For` pentru a păstra IP-ul clientului original
5. Testați distribuția cererilor

**Verificare:**
```bash
# Porniți 3 servere backend (în terminale separate)
python -m http.server 8001 --directory www/
python -m http.server 8002 --directory www/
python -m http.server 8003 --directory www/

# Porniți proxy-ul
python src/exercises/ex_8_02_proxy_invers.py

# Testați distribuția
for i in {1..6}; do curl -s http://localhost:8000/; done
```

### Exercițiul 3: Suport pentru Metoda POST

**Obiectiv:** Extinderea serverului HTTP pentru a gestiona cererile POST cu date în corp.

**Durată:** 30-45 minute

**Fișier:** `src/exercises/ex_8_03_suport_post.py`

**Concepte Cheie:**
- Antetul Content-Length pentru determinarea dimensiunii corpului
- Citirea corpului cererii după antete
- Procesarea datelor URL-encoded și JSON

### Exercițiul 4: Limitarea Ratei de Cereri

**Obiectiv:** Implementarea unui mecanism de rate limiting pentru a preveni abuzul.

**Durată:** 45-60 minute

**Fișier:** `src/exercises/ex_8_04_limitare_rata.py`

**Concepte Cheie:**
- Algoritmul token bucket
- Urmărirea cererilor per IP
- Răspunsul 429 Too Many Requests

### Exercițiul 5: Proxy cu Cache

**Obiectiv:** Adăugarea funcționalității de cache la proxy pentru a îmbunătăți performanța.

**Durată:** 60-90 minute

**Fișier:** `src/exercises/ex_8_05_proxy_cache.py`

**Concepte Cheie:**
- Cache în memorie cu TTL (Time To Live)
- Antetele Cache-Control și ETag
- Invalidarea cache-ului

## Demonstrații

### Demo 1: Proxy nginx cu Docker

Demonstrează funcționarea proxy-ului invers nginx cu echilibrare round-robin.

```powershell
python scripts/ruleaza_demo.py --demo docker-nginx
```

**Ce să observați:**
- Distribuția uniformă a cererilor între cele 3 backend-uri
- Antetele X-Backend-ID și X-Backend-Name în răspunsuri
- Contorul de cereri pentru fiecare backend

### Demo 2: Algoritmi de Echilibrare

Compară diferiții algoritmi de echilibrare a încărcării.

```powershell
python scripts/ruleaza_demo.py --demo echilibrare
```

**Ce să observați:**
- Round-robin: distribuție egală (1→2→3→1→2→3)
- Weighted: distribuție proporțională (5:3:1)
- Least-connections: rutare dinamică
- IP-hash: persistența sesiunii

### Demo 3: Handshake TCP

Demonstrează stabilirea conexiunii TCP în trei pași.

```powershell
python scripts/ruleaza_demo.py --demo handshake
```

**Ce să observați în Wireshark:**
- Pachetul SYN inițial de la client
- Răspunsul SYN-ACK de la server
- Confirmarea ACK de la client

## Capturarea și Analiza Traficului

### Capturarea Traficului

```powershell
# Folosind scriptul helper
python scripts/captureaza_trafic.py --interfata eth0 --iesire pcap/captura_s8.pcap

# Sau folosind Wireshark direct
# Deschideți Wireshark > Selectați interfața "Loopback" > Porniți captura
```

### Filtre Wireshark Recomandate

```
# Doar trafic HTTP
http

# Port TCP 8080
tcp.port == 8080

# Doar cereri HTTP
http.request

# Doar răspunsuri HTTP
http.response

# Handshake TCP (pachete SYN)
tcp.flags.syn == 1

# Backend specific
ip.addr == 172.28.8.21

# Urmărește flux TCP
tcp.stream eq 0
```

## Oprire și Curățare

### Sfârșitul Sesiunii

```powershell
# Opriți toate containerele (păstrează datele)
python scripts/opreste_laborator.py

# Verificați oprirea
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```powershell
# Eliminați toate containerele, rețelele și volumele pentru această săptămână
python scripts/curatare.py --complet

# Verificați curățarea
docker system df
```

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de realizat acasă.

### Tema 1: Server HTTPS cu TLS

**Fișier:** `homework/exercises/tema_8_01_server_https.py`

Extindeți serverul HTTP de bază pentru a suporta conexiuni HTTPS folosind TLS.

**Cerințe:**
- Generarea unui certificat auto-semnat
- Implementarea socket-ului TLS
- Suport pentru ambele protocoale (HTTP pe 8080, HTTPS pe 8443)

### Tema 2: Echilibrator cu Ponderi

**Fișier:** `homework/exercises/tema_8_02_echilibrator_ponderat.py`

Implementați un echilibrator de încărcare weighted round-robin cu verificare a stării de sănătate.

**Cerințe:**
- Distribuție proporțională cu ponderile configurate
- Verificarea periodică a sănătății backend-urilor
- Failover automat pentru backend-uri indisponibile

## Depanare

### Probleme Frecvente

#### Docker Desktop nu pornește

**Simptome:** Eroare "Cannot connect to the Docker daemon"

**Soluție:**
1. Porniți Docker Desktop din meniul Start Windows
2. Așteptați 30-60 secunde pentru inițializare
3. Verificați cu: `docker info`

#### Portul 8080 este ocupat

**Simptome:** Eroare "Bind for 0.0.0.0:8080 failed: port is already allocated"

**Soluție:**
```powershell
# Găsiți procesul care folosește portul (PowerShell)
netstat -ano | findstr :8080

# Opriți procesul după PID
taskkill /PID <pid> /F
```

#### Containerele nu pornesc

**Soluție:**
```bash
# Verificați jurnalele containerelor
docker logs week8-nginx-1
docker logs week8-backend1-1

# Reporniți serviciile
python scripts/opreste_laborator.py
python scripts/porneste_laborator.py --reconstruieste
```

Consultați `docs/depanare.md` pentru mai multe soluții.

## Fundamente Teoretice

### Comparație TCP vs UDP

| Caracteristică | TCP | UDP |
|----------------|-----|-----|
| Conexiune | Orientat pe conexiune | Fără conexiune |
| Fiabilitate | Transfer fiabil | Best-effort |
| Ordonare | Păstrată | Nu este garantată |
| Control flux | Da | Nu |
| Control congestie | Da | Nu |
| Overhead | Mai mare | Mai mic |
| Cazuri de utilizare | HTTP, FTP, SSH | DNS, VoIP, streaming |

### HTTP peste TCP

HTTP utilizează TCP ca protocol de transport deoarece necesită:
- **Fiabilitate:** Fiecare octet din cerere/răspuns trebuie livrat corect
- **Ordonare:** Mesajele trebuie reconstruite în ordinea corectă
- **Control flux:** Previne supraîncărcarea serverului/clientului

### Arhitectura Proxy Invers

```
                           ┌─────────────┐
                           │  Backend 1  │
                           │  (Alpha)    │
┌─────────┐   ┌─────────┐  ├─────────────┤
│ Client  │───│  nginx  │──│  Backend 2  │
│         │   │ (proxy) │  │  (Beta)     │
└─────────┘   └─────────┘  ├─────────────┤
                           │  Backend 3  │
                           │  (Gamma)    │
                           └─────────────┘
```

Beneficii:
- **Echilibrarea încărcării:** Distribuie traficul între servere
- **Disponibilitate ridicată:** Failover automat
- **Terminare SSL:** Descarcă criptarea de la backend-uri
- **Cache:** Reduce încărcarea backend-urilor

## Diagrama Arhitecturii

```
┌──────────────────────────────────────────────────────────────────┐
│                     REȚEA week8-laboratory-network               │
│                          172.28.8.0/24                           │
│                                                                  │
│  ┌────────────────┐                                              │
│  │     nginx      │ :8080 (HTTP)                                 │
│  │  (proxy invers)│ :8443 (HTTPS)                                │
│  │  172.28.8.10   │                                              │
│  └───────┬────────┘                                              │
│          │                                                       │
│          │ upstream: round-robin / weighted / least-conn         │
│          │                                                       │
│  ┌───────┴───────┬───────────────┬───────────────┐               │
│  │               │               │               │               │
│  ▼               ▼               ▼               │               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │               │
│  │Backend 1│ │Backend 2│ │Backend 3│ │Portainer│ │               │
│  │ (Alpha) │ │ (Beta)  │ │ (Gamma) │ │  :9443  │ │               │
│  │ :8080   │ │ :8080   │ │ :8080   │ │         │ │               │
│  │.21      │ │.22      │ │.23      │ │         │ │               │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ │               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 793 - Transmission Control Protocol
- RFC 768 - User Datagram Protocol
- RFC 9110 - HTTP Semantics
- RFC 8446 - TLS 1.3
- Documentația nginx: https://nginx.org/en/docs/

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
