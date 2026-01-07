# Săptămâna 11: Protocoale de Aplicație — FTP, DNS, SSH și Echilibrare de Sarcină

> Laborator Rețele de Calculatoare — ASE, Informatică Economică
> 
> de Revolvix

## Prezentare Generală

Această sesiune de laborator explorează protocoalele stratului de aplicație și tehnicile de echilibrare a sarcinii. Veți investiga mecanismele fundamentale care permit transferul de fișiere, rezoluția numelor de domeniu și accesul securizat de la distanță, toate esențiale pentru infrastructura modernă a internetului.

**File Transfer Protocol (FTP)** utilizează o arhitectură cu conexiune duală: un canal de control (portul 21) pentru comenzi și autentificare, și canale de date dinamice pentru transferul efectiv al fișierelor. Această separare permite un control sofisticat al fluxului, dar introduce complexități la traversarea NAT — de aceea modul pasiv a devenit predominant în mediile moderne de rețea.

**Domain Name System (DNS)** funcționează ca o bază de date ierarhică distribuită, transformând numele de domeniu lizibile în adrese IP. Arhitectura sa — ce cuprinde rezolveri, servere recursive și servere autoritative — demonstrează principii elegante de proiectare distribută, în timp ce extensiile DNSSEC adaugă validare criptografică pentru a preveni atacurile de otrăvire a cache-ului.

**Secure Shell (SSH)** multiplexează multiple canale logice peste o singură conexiune TCP criptată, suportând sesiuni de terminal, transferuri de fișiere (SFTP/SCP) și redirecționare de porturi. Protocoalele sale de schimb de chei și arhitectura pe straturi oferă atât confidențialitate, cât și autentificare puternică.

**Echilibrarea sarcinii** distribuie traficul de intrare pe mai multe servere backend, îmbunătățind disponibilitatea, scalabilitatea și toleranța la defecte. Veți implementa algoritmi de echilibrare atât în Python simplu, cât și folosind Nginx ca proxy invers, comparând caracteristicile lor de performanță.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** componentele arhitecturale ale protocoalelor FTP, DNS și SSH, inclusiv numerele de port și formatele mesajelor
2. **Explicați** diferențele dintre modurile FTP activ și pasiv și implicațiile lor pentru traversarea firewall-ului și NAT
3. **Implementați** un echilibror de sarcină în Python cu suport pentru algoritmii round-robin, least-connections și IP hash
4. **Demonstrați** echilibrarea sarcinii cu Nginx folosind Docker Compose, inclusiv verificări de stare și configurare de failover
5. **Analizați** traficul de rețea folosind Wireshark pentru a observa comportamentul protocoalelor în practică
6. **Proiectați** servicii containerizate care comunică prin rețele definite, aplicând principiile de izolare a rețelei
7. **Evaluați** compromisurile de performanță între diferite strategii de echilibrare a sarcinii prin benchmarking și analiza latențelor

## Cerințe Preliminare

### Cunoștințe Necesare

- Model TCP/IP și comunicare bazată pe socket-uri (Săptămânile 1-4)
- Fundamente Docker și containerizare (Săptămânile 9-10)
- Structura mesajelor HTTP și paradigma cerere-răspuns (Săptămânile 8-10)
- Programare Python la nivel intermediar (funcții, clase, threading)

### Cerințe Software

| Software | Versiune | Scop |
|----------|---------|------|
| Windows 10/11 | 21H2+ | Sistem de operare gazdă |
| WSL2 | Ubuntu 22.04+ | Mediu de execuție Linux |
| Docker Desktop | 4.20+ | Rulare containere |
| Python | 3.11+ | Execuție scripturi |
| Wireshark | 4.0+ | Analiză pachete |
| Git | 2.40+ | Control versiuni (opțional) |

### Cerințe Hardware

- Minim 8GB RAM (16GB recomandat pentru Docker)
- 10GB spațiu liber pe disc
- Conectivitate la rețea pentru descărcarea imaginilor

## Pornire Rapidă

### Prima Configurare (Rulează o singură dată)

```powershell
# Deschide PowerShell ca Administrator
cd WEEK11_WSLkit_RO

# Verifică cerințele preliminare
python setup/verify_environment.py

# Dacă apar probleme, rulează scriptul de instalare
python setup/install_prerequisites.py
```

### Pornirea Laboratorului

```powershell
# Pornește toate serviciile
python scripts/start_lab.py

# Verifică starea
python scripts/start_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Descriere |
|----------|----------|-----------|
| Nginx Load Balancer | http://localhost:8080 | Punct de intrare echilibror |
| Backend 1 | http://localhost:8081 | Server web direct |
| Backend 2 | http://localhost:8082 | Server web direct |
| Backend 3 | http://localhost:8083 | Server web direct |
| Stare LB | http://localhost:8080/health | Verificare stare |
| Status Nginx | http://localhost:8080/nginx_status | Statistici Nginx |
| Portainer | https://localhost:9443 | Management Docker |

## Exerciții de Laborator

### Exercițiul 1: Servere Backend HTTP

**Obiectiv:** Lansează multiple servere HTTP care vor servi ca backend-uri pentru echilibror.

**Durată estimată:** 15 minute

**Pași:**

1. Deschide trei terminale separate (PowerShell sau WSL)

2. În primul terminal, pornește Backend 1:
   ```powershell
   python src/exercises/ex_11_01_backend.py --id 1 --port 8081 -v
   ```

3. În al doilea terminal, pornește Backend 2:
   ```powershell
   python src/exercises/ex_11_01_backend.py --id 2 --port 8082 -v
   ```

4. În al treilea terminal, pornește Backend 3:
   ```powershell
   python src/exercises/ex_11_03_backend.py --id 3 --port 8083 -v
   ```

5. Testează fiecare backend individual:
   ```powershell
   curl http://localhost:8081/
   curl http://localhost:8082/
   curl http://localhost:8083/
   ```

**Rezultat așteptat:**
```
Backend 1 | Host: NUMELE-PC | Timp: 2025-01-06T14:30:00 | Cerere #1
Backend 2 | Host: NUMELE-PC | Timp: 2025-01-06T14:30:01 | Cerere #1
Backend 3 | Host: NUMELE-PC | Timp: 2025-01-06T14:30:02 | Cerere #1
```

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 1
```

---

### Exercițiul 2: Echilibror de Sarcină Python (Round Robin)

**Obiectiv:** Implementează și testează distribuția round-robin a cererilor.

**Durată estimată:** 20 minute

**Pași:**

1. Cu backend-urile pornite din Exercițiul 1, lansează echiliborul:
   ```powershell
   python src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --listen 0.0.0.0:8080 --algo rr
   ```

2. Trimite cereri multiple prin echilibror:
   ```powershell
   for /L %i in (1,1,6) do @curl -s http://localhost:8080/
   ```

3. Observă cum cererile sunt distribuite ciclic (1→2→3→1→2→3)

**Ce trebuie observat:**
- Fiecare cerere consecutivă merge la un backend diferit
- Distribuția este echitabilă pe termen lung
- Latența este minimă (echilibrul adaugă puțin overhead)

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 2
```

---

### Exercițiul 3: Sesiuni Persistente cu IP Hash

**Obiectiv:** Demonstrează sesiuni fixe unde un client ajunge mereu la același backend.

**Durată estimată:** 15 minute

**Pași:**

1. Oprește echiliborul anterior (Ctrl+C)

2. Repornește cu algoritm IP hash:
   ```powershell
   python src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --listen 0.0.0.0:8080 --algo ip_hash
   ```

3. Trimite cereri multiple:
   ```powershell
   for /L %i in (1,1,5) do @curl -s http://localhost:8080/
   ```

4. Observă că toate cererile merg la același backend

**Când să folosești IP Hash:**
- Aplicații cu stare (coșuri de cumpărături, sesiuni utilizator)
- Cache-uri locale pe server
- Conexiuni WebSocket

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 3
```

---

### Exercițiul 4: Simulare Failover

**Obiectiv:** Observă cum echiliborul gestionează căderea unui backend.

**Durată estimată:** 20 minute

**Pași:**

1. Cu echiliborul în mod round-robin, oprește Backend 2:
   ```powershell
   # În terminalul Backend 2, apasă Ctrl+C
   ```

2. Trimite cereri și observă redistribuirea:
   ```powershell
   for /L %i in (1,1,4) do @curl -s http://localhost:8080/
   ```

3. Repornește Backend 2:
   ```powershell
   python src/exercises/ex_11_01_backend.py --id 2 --port 8082 -v
   ```

4. Verifică reintegrarea în pool:
   ```powershell
   for /L %i in (1,1,6) do @curl -s http://localhost:8080/
   ```

**Ce trebuie observat:**
- Traficul se redistribuie automat la backend-urile sănătoase
- Pot apărea erori scurte în timpul detectării căderilor
- Recuperarea este automată când backend-ul revine

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 4
```

---

### Exercițiul 5: Echilibror Nginx cu Docker

**Obiectiv:** Implementează echilibrare de sarcină la nivel de producție folosind Nginx.

**Durată estimată:** 25 minute

**Pași:**

1. Oprește orice backend-uri Python sau echilibroare care rulează

2. Pornește stiva Docker:
   ```powershell
   cd docker
   docker compose up -d
   cd ..
   ```

3. Verifică că toate containerele rulează:
   ```powershell
   docker ps
   ```

4. Testează distribuția sarcinii:
   ```powershell
   for /L %i in (1,1,6) do @curl -s http://localhost:8080/
   ```

5. Verifică endpoint-ul de stare:
   ```powershell
   curl http://localhost:8080/health
   ```

6. Vizualizează statisticile Nginx:
   ```powershell
   curl http://localhost:8080/nginx_status
   ```

**Experimente de încercat:**
- Modifică `docker/configs/nginx.conf` pentru a schimba algoritmul
- Decomentează `least_conn;` sau `ip_hash;`
- Aplică cu: `docker compose restart nginx`

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 5
```

---

### Exercițiul 6: Client DNS și Analiză Protocol

**Obiectiv:** Înțelege structura mesajelor DNS prin implementare practică.

**Durată estimată:** 20 minute

**Pași:**

1. Interoghează înregistrări A (adrese IPv4):
   ```powershell
   python src/exercises/ex_11_03_dns_client.py google.com A --verbose
   ```

2. Interoghează înregistrări MX (servere de email):
   ```powershell
   python src/exercises/ex_11_03_dns_client.py google.com MX --verbose
   ```

3. Interoghează înregistrări NS (nameservere):
   ```powershell
   python src/exercises/ex_11_03_dns_client.py google.com NS --verbose
   ```

4. Examinează hexdump-ul pachetului și corelează-l cu RFC 1035

**Câmpuri cheie de observat:**
- ID tranzacție (2 octeți)
- Flags (QR, Opcode, RD, RA)
- Contoare secțiuni (QDCOUNT, ANCOUNT)
- Format nume de domeniu (etichete cu prefix de lungime)

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 6
```

---

### Exercițiul 7: Benchmarking și Comparație Performanțe

**Obiectiv:** Măsoară și compară performanța diferitelor configurații de echilibrare.

**Durată estimată:** 25 minute

**Pași:**

1. Benchmark echilibror Python:
   ```powershell
   python src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 500 --c 10
   ```

2. Notează metricile:
   - Cereri pe secundă (RPS)
   - Latență p50, p90, p95, p99
   - Distribuția codurilor de stare

3. Comută la echiliborul Nginx (pornește stiva Docker dacă nu rulează)

4. Benchmark Nginx:
   ```powershell
   python src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 500 --c 10
   ```

5. Compară rezultatele

**Rezultate așteptate:**
| Metric | Python LB | Nginx |
|--------|-----------|-------|
| RPS | 400-1000 | 5000-20000 |
| Latență p50 | 20-50ms | 1-5ms |
| Latență p99 | 50-100ms | 10-20ms |

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 7
```

---

## Demonstrații

### Demo 1: Demonstrație Completă Echilibrare de Sarcină

Rulează demonstrația automată care prezintă toate conceptele:

```powershell
python scripts/run_demo.py --all
```

**Ce se demonstrează:**
- Distribuția sarcinii pe multiple backend-uri
- Inspecția header-elor (X-Backend-ID, X-Served-By)
- Scenarii de failover și recuperare
- Rezultate benchmarking cu statistici

### Demo 2: Demonstrație Failover

```powershell
python scripts/run_demo.py --demo failover
```

Arată comportamentul echilibrării când un backend cade și revine.

## Captura și Analiza Pachetelor

### Capturarea Traficului

```powershell
# Pornește captura
python scripts/capture_traffic.py --interface eth0 --output pcap/week11_capture.pcap

# Sau folosește Wireshark direct
# Deschide Wireshark > Selectează interfața potrivită
```

### Filtre Wireshark Recomandate

```
# Trafic HTTP prin echilibror
tcp.port == 8080 && http

# Doar cereri HTTP
http.request

# Doar răspunsuri HTTP
http.response

# Trafic DNS
dns

# Interogări DNS
dns.flags.response == 0
```

## Oprire și Curățare

### Sfârșitul Sesiunii

```powershell
# Oprește toate containerele (păstrează datele)
python scripts/stop_lab.py

# Verifică oprirea
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```powershell
# Elimină toate containerele, rețelele și volumele pentru această săptămână
python scripts/cleanup.py --full

# Verifică curățarea
docker system df
```

## Teme pentru Acasă

Vezi directorul `homework/` pentru exerciții de aprofundare.

### Tema 1: Echilibror Extins cu Verificări Active de Stare
Implementează verificări periodice HTTP și weighted round-robin.

### Tema 2: Resolver DNS cu Cache
Construiește un resolver local DNS care memorează răspunsurile.

## Depanare

### Probleme Frecvente

#### Problema: Containerele nu pornesc
**Soluție:** Verifică că Docker Desktop rulează și are resurse suficiente alocate.

#### Problema: Portul 8080 este ocupat
**Soluție:** Identifică procesul: `netstat -ano | findstr :8080` și oprește-l sau schimbă portul în configurație.

#### Problema: Distribuție neuniformă
**Soluție:** Verifică setarea algoritmului în nginx.conf și repornește: `docker compose restart nginx`

Pentru mai multe soluții, vezi `docs/troubleshooting.md`.

## Context Teoretic

### Arhitectura FTP

FTP folosește un model cu conexiune duală:
- **Canal de control** (port 21): comenzi și răspunsuri
- **Canal de date** (port dinamic): transfer efectiv de fișiere

Modul **activ** vs **pasiv**:
- Activ: serverul inițiază conexiunea de date (probleme cu NAT/firewall)
- Pasiv: clientul inițiază ambele conexiuni (compatibil NAT)

### Ierarhia DNS

```
                    [Root Servers (.)]
                           |
              +------------+------------+
              |            |            |
          [.com]       [.org]       [.ro]
              |
     +--------+--------+
     |                 |
 [google]          [example]
     |
 [www.google.com] → 142.250.185.78
```

### Canale SSH

SSH multiplexează multiple canale peste o conexiune:
- Canal sesiune (shell interactiv)
- Canal SFTP (transfer fișiere)
- Redirecționare port local/remote
- Agent forwarding

### Algoritmi de Echilibrare

| Algoritm | Comportament | Caz de Utilizare |
|----------|-------------|------------------|
| Round Robin | Rotație ciclică | Sarcini uniforme |
| Least Connections | Cel mai puțin încărcat | Cereri cu durată variabilă |
| IP Hash | Hashing adresă client | Sesiuni persistente |
| Weighted | Ponderat după capacitate | Servere eterogene |

## Referințe

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 959 — File Transfer Protocol
- RFC 1035 — Domain Names - Implementation and Specification
- RFC 4251-4254 — Secure Shell Protocol
- Nginx Documentation: https://nginx.org/en/docs/

## Diagramă Arhitectură

```
                                    ┌─────────────────────────────────────┐
                                    │         STIVĂ DOCKER                │
┌──────────┐                        │  ┌─────────────────────────────┐    │
│          │   Cerere HTTP          │  │     Nginx Load Balancer     │    │
│  Client  │ ──────────────────────►│  │       (s11_nginx_lb)        │    │
│          │                        │  │         :8080               │    │
└──────────┘                        │  └─────────────┬───────────────┘    │
                                    │                │                     │
                                    │    round_robin / least_conn / ip_hash│
                                    │                │                     │
                                    │  ┌─────────────┴───────────────┐    │
                                    │  │                             │    │
                                    │  ▼             ▼             ▼     │
                                    │ ┌───┐       ┌───┐       ┌───┐      │
                                    │ │web│       │web│       │web│      │
                                    │ │ 1 │       │ 2 │       │ 3 │      │
                                    │ └───┘       └───┘       └───┘      │
                                    │  :80         :80         :80       │
                                    │                                     │
                                    │         Rețea: s11_network          │
                                    │         (172.28.0.0/16)             │
                                    └─────────────────────────────────────┘
```

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
