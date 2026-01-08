# Săptămâna 11: Protocoale de Aplicație — FTP, DNS, SSH și Echilibrare de Sarcină

> Laborator Rețele de Calculatoare — ASE, Informatică Economică
> 
> de Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `11roWSL`

**Arhitectura Mediului:**
```
Windows 11 → WSL2 → Ubuntu 22.04 (implicit) → Docker Engine → Portainer CE
```

**Credențiale Standard:**
| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

---

## 📥 Clonarea Laboratorului Acestei Săptămâni

### Pasul 1: Deschide PowerShell (Windows)

Apasă `Win + X` → Selectează "Windows Terminal" sau "PowerShell"

### Pasul 2: Navighează și Clonează

```powershell
# Creează folderul de rețele dacă nu există
mkdir D:\RETELE -ErrorAction SilentlyContinue
cd D:\RETELE

# Clonează Săptămâna 11
git clone https://github.com/antonioclim/netROwsl.git SAPT11
cd SAPT11
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 11roWSL/
cd 11roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT11\
    └── 11roWSL\
        ├── artifacts/       # Rezultate generate (capturi, loguri)
        ├── docker/          # Configurație Docker
        │   ├── configs/     # Configurare Nginx
        │   ├── web1/        # Conținut backend 1
        │   ├── web2/        # Conținut backend 2
        │   ├── web3/        # Conținut backend 3
        │   └── volumes/     # Volume persistente
        ├── docs/            # Documentație suplimentară
        │   ├── commands_cheatsheet.md
        │   ├── further_reading.md
        │   ├── theory_summary.md
        │   └── troubleshooting.md
        ├── homework/        # Teme pentru acasă
        │   └── exercises/   # hw_11_01, hw_11_02
        ├── pcap/            # Fișiere de captură .pcap
        ├── scripts/         # Scripturi de automatizare
        │   └── utils/       # Utilitare Docker și rețea
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă
        │   ├── apps/        # Aplicații demonstrative
        │   ├── exercises/   # Exerciții Python
        │   └── utils/       # Utilitare rețea
        ├── tests/           # Teste automatizate
        └── README.md        # Acest fișier
```

---

## 🔧 Configurarea Inițială a Mediului (Doar Prima Dată)

### Pasul 1: Deschide Terminalul Ubuntu

Din Windows, ai mai multe opțiuni:
- Click pe "Ubuntu" în meniul Start, SAU
- În PowerShell tastează: `wsl`, SAU
- În Windows Terminal selectează tab-ul "Ubuntu"

Vei vedea promptul Ubuntu:
```
stud@CALCULATOR:~$
```

### Pasul 2: Pornește Serviciul Docker

```bash
# Pornește Docker (necesar după fiecare restart Windows)
sudo service docker start
# Parolă: stud

# Verifică că Docker rulează
docker ps
```

**Output așteptat:**
```
CONTAINER ID   IMAGE                    STATUS          NAMES
abc123...      portainer/portainer-ce   Up 2 hours      portainer
```

Dacă vezi containerul `portainer` în listă, mediul este pregătit.

### Pasul 3: Verifică Accesul la Portainer

1. Deschide browser-ul web (Chrome, Firefox, Edge)
2. Navighează la: **http://localhost:9000**

**Credențiale de autentificare:**
- Utilizator: `stud`
- Parolă: `studstudstud`

**Ce să faci dacă Portainer nu răspunde:**
```bash
# Verifică dacă containerul Portainer există
docker ps -a | grep portainer

# Dacă e oprit, pornește-l
docker start portainer

# Dacă nu există, creează-l
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

### Pasul 4: Navighează la Folderul Laboratorului în WSL

```bash
# Navighează la folderul laboratorului
cd /mnt/d/RETELE/SAPT11/11roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor pentru Săptămâna 11

Navighează: **Home → local → Containers**

Vei vedea containerele specifice laboratorului:
- **s11_nginx_lb** - Echilibror de sarcină Nginx (172.28.0.x:8080)
- **s11_backend_1** - Server web backend 1 (172.28.0.x:80)
- **s11_backend_2** - Server web backend 2 (172.28.0.x:80)
- **s11_backend_3** - Server web backend 3 (172.28.0.x:80)

### Acțiuni asupra Containerelor în Portainer

Pentru orice container, poți efectua următoarele operații:

| Acțiune | Descriere | Cum să o faci |
|---------|-----------|---------------|
| **Start** | Pornește containerul oprit | Butonul verde ▶ |
| **Stop** | Oprește containerul | Butonul roșu ■ |
| **Restart** | Repornește containerul | Butonul ↻ |
| **Logs** | Vezi jurnalele containerului | Click pe nume → tab "Logs" |
| **Console** | Accesează shell-ul containerului | Click pe nume → tab "Console" → "Connect" |
| **Inspect** | Vezi configurația JSON detaliată | Click pe nume → tab "Inspect" |
| **Stats** | Monitorizare CPU/Memorie/Rețea în timp real | Click pe nume → tab "Stats" |

### Vizualizarea Rețelei s11_network

1. Navighează: **Networks**
2. Click pe **s11_network**
3. Vezi configurația IPAM: 172.28.0.0/16
4. Vezi toate containerele conectate și IP-urile lor

### Modificarea Configurației Nginx prin Portainer

1. **Console** pe s11_nginx_lb
2. Editează /etc/nginx/nginx.conf (sau folosește configurația montată)
3. Sau editează local `docker/configs/nginx.conf` și rulează:
   ```bash
   docker compose restart nginx
   ```

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a observa distribuția traficului prin echilibror
- Pentru analiza protocolului DNS

### Pasul 1: Lansează Wireshark

Din Meniul Start Windows: Caută "Wireshark" → Click pentru a deschide

Alternativ, din PowerShell:
```powershell
& "C:\Program Files\Wireshark\Wireshark.exe"
```

### Pasul 2: Selectează Interfața de Captură

**CRITIC:** Selectează interfața corectă pentru traficul WSL:

| Numele Interfeței | Când să Folosești |
|-------------------|-------------------|
| **vEthernet (WSL)** | ✅ Cel mai frecvent - capturează traficul Docker WSL |
| **vEthernet (WSL) (Hyper-V firewall)** | Alternativă dacă prima nu funcționează |
| **Loopback Adapter** | Doar pentru trafic localhost (127.0.0.1) |
| **Ethernet/Wi-Fi** | Trafic rețea fizică (nu Docker) |

**Cum selectezi:** Dublu-click pe numele interfeței SAU selecteaz-o și click pe icoana aripioarei albastre de rechin.

### Pasul 3: Generează Trafic

Cu Wireshark capturând (vei vedea pachete apărând în timp real), rulează exercițiile:

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT11/11roWSL

# Pornește mediul de laborator
python3 scripts/start_lab.py

# Testează echilibrorul
for i in {1..6}; do curl -s http://localhost:8080/; done
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 11

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

**Filtre pentru Trafic HTTP prin Echilibror:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.port == 8080` | Trafic echilibror | Cereri către load balancer |
| `http` | Tot traficul HTTP | Analiză generală HTTP |
| `http.request` | Doar cereri HTTP | Vezi ce trimite clientul |
| `http.response` | Doar răspunsuri HTTP | Vezi ce returnează backend-urile |
| `http.request.uri == "/"` | Cereri către rădăcină | Identifică cereri principale |
| `http.request.uri contains "health"` | Verificări de stare | Trafic health check |
| `http.response.code == 200` | Răspunsuri OK | Succes |
| `http.response.code >= 500` | Erori server | Probleme backend |

**Filtre pentru Trafic DNS:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `dns` | Tot traficul DNS | Analiză generală DNS |
| `dns.qry.name contains "google"` | Interogări specifice | Filtrare domenii |
| `dns.flags.response == 0` | Doar interogări | Cereri DNS |
| `dns.flags.response == 1` | Doar răspunsuri | Răspunsuri DNS |
| `dns.qry.type == 1` | Înregistrări A | Adrese IPv4 |
| `dns.qry.type == 15` | Înregistrări MX | Servere email |
| `dns.qry.type == 2` | Înregistrări NS | Nameservere |

**Filtre pentru Rețeaua Laboratorului:**

| Filtru | Scop | Container |
|--------|------|-----------|
| `ip.addr == 172.28.0.0/16` | Toată rețeaua | Toate containerele |
| `tcp.port == 80` | Trafic backend | Backend-uri Nginx |

**Combinarea filtrelor:**
- ȘI: `http && tcp.port == 8080`
- SAU: `tcp.port == 8080 || tcp.port == 80`
- NU: `!arp && !icmp`

### Analiza Distribuției Sarcinii în Wireshark

1. Capturează trafic în timp ce rulezi:
   ```bash
   for i in {1..10}; do curl -s http://localhost:8080/; done
   ```
2. Folosește filtrul: `http.response`
3. Observă răspunsurile de la diferite backend-uri
4. Analizează header-urile pentru identificarea backend-ului

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP normal |
| Albastru deschis | Trafic UDP (DNS) |
| Verde deschis | Trafic HTTP |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |
| Text negru, fundal roșu | Erori TCP |
| Text negru, fundal galben | Avertismente, retransmisii |

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT11\11roWSL\pcap\`
3. Nume fișier conform exercițiului:
   - `captura_s11_loadbalancer.pcap` - Trafic echilibror
   - `captura_s11_dns.pcap` - Rezoluție DNS
   - `captura_s11_failover.pcap` - Test failover
4. Format: Wireshark/pcap sau pcapng (implicit)

---

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
| Docker Engine | 24.0+ | Rulare containere (în WSL) |
| Portainer CE | 2.19+ | Management vizual Docker (port 9000) |
| Python | 3.11+ | Execuție scripturi |
| Wireshark | 4.0+ | Analiză pachete |
| Git | 2.40+ | Control versiuni (opțional) |

### Cerințe Hardware

- Minim 8GB RAM (16GB recomandat pentru Docker)
- 10GB spațiu liber pe disc
- Conectivitate la rețea pentru descărcarea imaginilor

## Pornire Rapidă

### Prima Configurare (Rulează o singură dată)

```bash
# Deschide terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT11/11roWSL

# Verifică cerințele preliminare
python3 setup/verify_environment.py

# Dacă apar probleme, rulează scriptul de instalare
python3 setup/install_prerequisites.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT11/11roWSL

# Pornește toate serviciile
python3 scripts/start_lab.py

# Verifică starea
python3 scripts/start_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Descriere |
|----------|----------|-----------|
| Portainer | http://localhost:9000 | Management Docker |
| Nginx Load Balancer | http://localhost:8080 | Punct de intrare echilibror |
| Backend 1 | http://localhost:8081 | Server web direct |
| Backend 2 | http://localhost:8082 | Server web direct |
| Backend 3 | http://localhost:8083 | Server web direct |
| Stare LB | http://localhost:8080/health | Verificare stare |
| Status Nginx | http://localhost:8080/nginx_status | Statistici Nginx |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Exerciții de Laborator

### Exercițiul 1: Servere Backend HTTP

**Obiectiv:** Lansează multiple servere HTTP care vor servi ca backend-uri pentru echilibror.

**Durată estimată:** 15 minute

**Pași:**

1. Deschide trei terminale separate (PowerShell sau WSL)

2. În primul terminal, pornește Backend 1:
   ```bash
   python3 src/exercises/ex_11_01_backend.py --id 1 --port 8081 -v
   ```

3. În al doilea terminal, pornește Backend 2:
   ```bash
   python3 src/exercises/ex_11_01_backend.py --id 2 --port 8082 -v
   ```

4. În al treilea terminal, pornește Backend 3:
   ```bash
   python3 src/exercises/ex_11_01_backend.py --id 3 --port 8083 -v
   ```

5. Testează fiecare backend individual:
   ```bash
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
```bash
python3 tests/test_exercises.py --exercise 1
```

---

### Exercițiul 2: Echilibror de Sarcină Python (Round Robin)

**Obiectiv:** Implementează și testează distribuția round-robin a cererilor.

**Durată estimată:** 20 minute

**Pași:**

1. Cu backend-urile pornite din Exercițiul 1, lansează echiliborul:
   ```bash
   python3 src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --listen 0.0.0.0:8080 --algo rr
   ```

2. Trimite cereri multiple prin echilibror:
   ```bash
   for i in {1..6}; do curl -s http://localhost:8080/; done
   ```

3. Observă cum cererile sunt distribuite ciclic (1→2→3→1→2→3)

**Ce trebuie observat:**
- Fiecare cerere consecutivă merge la un backend diferit
- Distribuția este echitabilă pe termen lung
- Latența este minimă (echilibrul adaugă puțin overhead)

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 2
```

---

### Exercițiul 3: Sesiuni Persistente cu IP Hash

**Obiectiv:** Demonstrează sesiuni fixe unde un client ajunge mereu la același backend.

**Durată estimată:** 15 minute

**Pași:**

1. Oprește echiliborul anterior (Ctrl+C)

2. Repornește cu algoritm IP hash:
   ```bash
   python3 src/exercises/ex_11_02_loadbalancer.py --backends localhost:8081,localhost:8082,localhost:8083 --listen 0.0.0.0:8080 --algo ip_hash
   ```

3. Trimite cereri multiple:
   ```bash
   for i in {1..5}; do curl -s http://localhost:8080/; done
   ```

4. Observă că toate cererile merg la același backend

**Când să folosești IP Hash:**
- Aplicații cu stare (coșuri de cumpărături, sesiuni utilizator)
- Cache-uri locale pe server
- Conexiuni WebSocket

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 3
```

---

### Exercițiul 4: Simulare Failover

**Obiectiv:** Observă cum echiliborul gestionează căderea unui backend.

**Durată estimată:** 20 minute

**Pași:**

1. Cu echiliborul în mod round-robin, oprește Backend 2:
   ```bash
   # În terminalul Backend 2, apasă Ctrl+C
   ```

2. Trimite cereri și observă redistribuirea:
   ```bash
   for i in {1..4}; do curl -s http://localhost:8080/; done
   ```

3. Repornește Backend 2:
   ```bash
   python3 src/exercises/ex_11_01_backend.py --id 2 --port 8082 -v
   ```

4. Verifică reintegrarea în pool:
   ```bash
   for i in {1..6}; do curl -s http://localhost:8080/; done
   ```

**Ce trebuie observat:**
- Traficul se redistribuie automat la backend-urile sănătoase
- Pot apărea erori scurte în timpul detectării căderilor
- Recuperarea este automată când backend-ul revine

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 4
```

---

### Exercițiul 5: Echilibror Nginx cu Docker

**Obiectiv:** Implementează echilibrare de sarcină la nivel de producție folosind Nginx.

**Durată estimată:** 25 minute

**Pași:**

1. Oprește orice backend-uri Python sau echilibroare care rulează

2. Pornește stiva Docker:
   ```bash
   cd /mnt/d/RETELE/SAPT11/11roWSL/docker
   docker compose up -d
   cd ..
   ```

3. Verifică că toate containerele rulează:
   ```bash
   docker ps
   ```

4. Testează distribuția sarcinii:
   ```bash
   for i in {1..6}; do curl -s http://localhost:8080/; done
   ```

5. Verifică endpoint-ul de stare:
   ```bash
   curl http://localhost:8080/health
   ```

6. Vizualizează statisticile Nginx:
   ```bash
   curl http://localhost:8080/nginx_status
   ```

**Experimente de încercat:**
- Modifică `docker/configs/nginx.conf` pentru a schimba algoritmul
- Decomentează `least_conn;` sau `ip_hash;`
- Aplică cu: `docker compose restart nginx`

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 5
```

---

### Exercițiul 6: Client DNS și Analiză Protocol

**Obiectiv:** Înțelege structura mesajelor DNS prin implementare practică.

**Durată estimată:** 20 minute

**Pași:**

1. Interoghează înregistrări A (adrese IPv4):
   ```bash
   python3 src/exercises/ex_11_03_dns_client.py google.com A --verbose
   ```

2. Interoghează înregistrări MX (servere de email):
   ```bash
   python3 src/exercises/ex_11_03_dns_client.py google.com MX --verbose
   ```

3. Interoghează înregistrări NS (nameservere):
   ```bash
   python3 src/exercises/ex_11_03_dns_client.py google.com NS --verbose
   ```

4. Examinează hexdump-ul pachetului și corelează-l cu RFC 1035

**Câmpuri cheie de observat:**
- ID tranzacție (2 octeți)
- Flags (QR, Opcode, RD, RA)
- Contoare secțiuni (QDCOUNT, ANCOUNT)
- Format nume de domeniu (etichete cu prefix de lungime)

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 6
```

---

### Exercițiul 7: Benchmarking și Comparație Performanțe

**Obiectiv:** Măsoară și compară performanța diferitelor configurații de echilibrare.

**Durată estimată:** 25 minute

**Pași:**

1. Benchmark echilibror Python:
   ```bash
   python3 src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 500 --c 10
   ```

2. Notează metricile:
   - Cereri pe secundă (RPS)
   - Latență p50, p90, p95, p99
   - Distribuția codurilor de stare

3. Comută la echiliborul Nginx (pornește stiva Docker dacă nu rulează)

4. Benchmark Nginx:
   ```bash
   python3 src/exercises/ex_11_02_loadbalancer.py loadgen --url http://localhost:8080/ --n 500 --c 10
   ```

5. Compară rezultatele

**Rezultate așteptate:**
| Metric | Python LB | Nginx |
|--------|-----------|-------|
| RPS | 400-1000 | 5000-20000 |
| Latență p50 | 20-50ms | 1-5ms |
| Latență p99 | 50-100ms | 10-20ms |

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 7
```

---

## Demonstrații

### Demo 1: Demonstrație Completă Echilibrare de Sarcină

Rulează demonstrația automată care prezintă toate conceptele:

```bash
python3 scripts/run_demo.py --all
```

**Ce se demonstrează:**
- Distribuția sarcinii pe multiple backend-uri
- Inspecția header-elor (X-Backend-ID, X-Served-By)
- Scenarii de failover și recuperare
- Rezultate benchmarking cu statistici

### Demo 2: Demonstrație Failover

```bash
python3 scripts/run_demo.py --demo failover
```

Arată comportamentul echilibrării când un backend cade și revine.

## Captura și Analiza Pachetelor

### Capturarea Traficului

```bash
# Pornește captura
python3 scripts/capture_traffic.py --interface eth0 --output pcap/week11_capture.pcap

# Sau folosește Wireshark direct pe Windows
# Selectează interfața vEthernet (WSL)
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

# Rețeaua laboratorului
ip.addr == 172.28.0.0/16
```

## Oprire și Curățare

### La Sfârșitul Sesiunii

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT11/11roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/stop_lab.py

# Verifică oprire - ar trebui să vezi doar portainer
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```bash
# Elimină toate containerele, rețelele și volumele pentru această săptămână
python3 scripts/cleanup.py --full

# Verifică curățarea
docker system df
```

## Teme pentru Acasă

Vezi directorul `homework/` pentru exerciții de aprofundare.

### Tema 1: Echilibror Extins cu Verificări Active de Stare
Implementează verificări periodice HTTP și weighted round-robin.

### Tema 2: Resolver DNS cu Cache
Construiește un resolver local DNS care memorează răspunsurile.

---

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

    Portainer (global): http://localhost:9000
```

---

## 🔧 Depanare Extinsă

### Probleme Docker

**Problemă:** "Cannot connect to Docker daemon"
```bash
# Pornește serviciul Docker în WSL
sudo service docker start
# Parolă: stud

# Verifică statusul
sudo service docker status

# Verifică că funcționează
docker ps
```

**Problemă:** Permisiune refuzată la rularea docker
```bash
# Adaugă utilizatorul la grupul docker
sudo usermod -aG docker $USER

# Aplică modificările
newgrp docker

# Sau deconectează-te și reconectează-te din WSL
exit
wsl
```

**Problemă:** Serviciul Docker nu pornește
```bash
# Verifică statusul detaliat
sudo service docker status

# Rulează daemon-ul manual pentru a vedea erorile
sudo dockerd

# Verifică log-urile
sudo cat /var/log/docker.log
```

### Probleme Portainer

**Problemă:** Nu pot accesa http://localhost:9000
```bash
# Verifică dacă containerul Portainer există și rulează
docker ps -a | grep portainer

# Dacă e oprit, pornește-l
docker start portainer

# Dacă nu există, creează-l
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest

# Verifică log-urile
docker logs portainer
```

**Problemă:** Am uitat parola Portainer
```bash
# ATENȚIE: Aceasta resetează Portainer (pierde setările dar NU containerele)
docker stop portainer
docker rm portainer
docker volume rm portainer_data

# Recreează cu comanda de mai sus
# La prima accesare, setează parola nouă: studstudstud
```

### Probleme Wireshark

**Problemă:** Nu se capturează pachete
- ✅ Verifică interfața corectă selectată (vEthernet WSL)
- ✅ Asigură-te că traficul este generat ÎN TIMPUL capturii
- ✅ Verifică că filtrul de afișare nu ascunde pachetele (șterge filtrul)
- ✅ Încearcă "Capture → Options" și activează modul promiscuous

**Problemă:** "No interfaces found" sau eroare de permisiune
- Rulează Wireshark ca Administrator (click dreapta → Run as administrator)
- Reinstalează Npcap cu opțiunea "WinPcap API-compatible Mode" bifată

**Problemă:** Nu văd traficul containerelor Docker
- Selectează interfața `vEthernet (WSL)`, nu `Ethernet` sau `Wi-Fi`
- Asigură-te că containerele sunt pe rețea bridge, nu host

### Probleme Specifice Săptămânii 11

**Problemă:** Portul 8080 este ocupat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 8080

# Oprește procesul care ocupă portul
# Sau schimbă portul în docker-compose.yml
```

**Problemă:** Containerele nu pornesc
```bash
# Verifică imaginile Docker
docker images | grep nginx

# Descarcă imaginea manual dacă lipsește
docker pull nginx:alpine

# Verifică log-urile
docker compose logs
```

**Problemă:** Distribuție neuniformă
```bash
# Verifică algoritmul în nginx.conf
cat docker/configs/nginx.conf | grep -A5 upstream

# Modifică și repornește
# Decomentează least_conn; sau ip_hash; după caz
docker compose restart nginx
```

**Problemă:** Backend-urile nu răspund
```bash
# Verifică starea containerelor
docker ps | grep s11_backend

# Verifică log-urile unui backend specific
docker logs s11_backend_1

# Testează conectivitatea internă
docker exec s11_nginx_lb curl http://web1/
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect s11_network

# Verifică DNS în container
docker exec s11_nginx_lb cat /etc/resolv.conf
```

**Problemă:** Erori la conectarea între containere
```bash
# Verifică că toate containerele sunt în aceeași rețea
docker network inspect s11_network | grep -A2 Containers
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT11/11roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/stop_lab.py

# Verifică - ar trebui să vezi doar portainer
docker ps
```

### Sfârșit de Săptămână (Completă)

```bash
# Curățare completă laborator
python3 scripts/cleanup.py --full

# Elimină imaginile nefolosite
docker image prune -f

# Elimină rețelele nefolosite
docker network prune -f

# Verifică utilizarea discului
docker system df
```

### Resetare Totală (Înainte de Semestru Nou)

```bash
# ATENȚIE: Aceasta elimină TOTUL în afară de Portainer

# Oprește toate containerele EXCEPTÂND Portainer
docker stop $(docker ps -q --filter "name=s11_")

# Elimină containerele oprite (nu Portainer)
docker container prune -f

# Elimină imaginile nefolosite
docker image prune -a -f

# Elimină rețelele nefolosite
docker network prune -f

# Verifică că Portainer încă rulează
docker ps
```

**⚠️ NU rula NICIODATĂ `docker system prune -a` fără să excluzi Portainer!**

### Verificare Post-Curățare

```bash
# Verifică ce a rămas
docker ps -a          # Containere
docker images         # Imagini
docker network ls     # Rețele
docker volume ls      # Volume

# Ar trebui să vezi doar:
# - Container: portainer
# - Volum: portainer_data
# - Rețele: bridge, host, none (implicite)
```

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
