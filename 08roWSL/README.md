# Săptămâna 8: Nivelul Transport — Server HTTP și Proxy Invers

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică
> 
> de Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `08roWSL`

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

# Clonează Săptămâna 8
git clone https://github.com/antonioclim/netROwsl.git SAPT8
cd SAPT8
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 08roWSL/
cd 08roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, www/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT8\
    └── 08roWSL\
        ├── artifacts/       # Rezultate generate (capturi, loguri)
        ├── docker/          # Configurație Docker și nginx
        │   └── configs/     # Configurări nginx
        │       └── nginx/   # nginx.conf și conf.d/
        ├── docs/            # Documentație suplimentară
        │   ├── depanare.md
        │   ├── fisa_comenzi.md
        │   └── rezumat_teoretic.md
        ├── homework/        # Teme pentru acasă
        │   └── exercises/   # tema_8_01, tema_8_02
        ├── pcap/            # Fișiere de captură .pcap
        ├── scripts/         # Scripturi de automatizare
        │   └── utils/       # Utilitare Docker și rețea
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă
        │   ├── apps/        # backend_server.py
        │   ├── exercises/   # ex_8_01, ex_8_02, etc.
        │   └── utils/       # Utilitare rețea
        ├── tests/           # Teste automatizate
        ├── www/             # Fișiere statice (index.html, hello.txt)
        │   └── api/         # status.json
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
cd /mnt/d/RETELE/SAPT8/08roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor pentru Săptămâna 8

Navighează: **Home → local → Containers**

Vei vedea containerele specifice laboratorului:
- **week8-nginx-proxy** - Proxy invers nginx (172.28.8.10:8080/8443)
- **week8-backend-1** - Backend Alpha (172.28.8.21:8080 intern)
- **week8-backend-2** - Backend Beta (172.28.8.22:8080 intern)
- **week8-backend-3** - Backend Gamma (172.28.8.23:8080 intern)

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

### Vizualizarea Rețelei week8-laboratory-network

1. Navighează: **Networks**
2. Click pe **week8-laboratory-network**
3. Vezi configurația IPAM: 172.28.8.0/24, gateway 172.28.8.1
4. Vezi toate containerele conectate și IP-urile lor

### Monitorizarea Load Balancing-ului

În Portainer poți observa echilibrarea încărcării:
1. **Containers** → Click pe **week8-backend-1** → **Stats**
2. Repetă pentru backend-2 și backend-3
3. Observă distribuția traficului între cele 3 backend-uri

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a observa handshake-ul TCP în trei pași
- Pentru analiza cererilor HTTP și răspunsurilor

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
cd /mnt/d/RETELE/SAPT8/08roWSL

# Test proxy HTTP
curl -i http://localhost:8080/

# Observă echilibrarea round-robin
for i in {1..6}; do curl -s http://localhost:8080/ | grep Backend; done

# Test server HTTP local
python3 src/exercises/ex_8_01_server_http.py &
curl -i http://localhost:8888/hello.txt
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 8

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

**Filtre pentru Trafic HTTP:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `http` | Tot traficul HTTP | Analiză generală HTTP |
| `http.request` | Doar cereri HTTP | Vezi ce trimite clientul |
| `http.response` | Doar răspunsuri HTTP | Vezi ce returnează serverul |
| `http.request.method == GET` | Cereri GET | Metoda principală |
| `http.request.method == POST` | Cereri POST | Trimitere date |
| `http.response.code == 200` | Răspunsuri OK | Cereri reușite |
| `http.response.code >= 400` | Erori HTTP | Cereri eșuate |

**Filtre pentru Porturi:**

| Filtru | Scop | Serviciu |
|--------|------|----------|
| `tcp.port == 8080` | Proxy HTTP nginx | Trafic principal |
| `tcp.port == 8443` | Proxy HTTPS nginx | Trafic criptat |
| `tcp.port == 8888` | Server HTTP exercițiu | Ex. 1 |
| `tcp.port == 8001 or tcp.port == 8002 or tcp.port == 8003` | Servere backend | Ex. 2 |

**Filtre pentru Analiza TCP:**

| Filtru | Scop | Ce să observi |
|--------|------|---------------|
| `tcp.flags.syn == 1` | Pachete SYN | Inițieri conexiuni |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Doar SYN inițial | Prima cerere |
| `tcp.flags.syn == 1 && tcp.flags.ack == 1` | SYN-ACK | Răspuns server |
| `tcp.flags.fin == 1` | Pachete FIN | Închidere conexiuni |
| `tcp.analysis.retransmission` | Retransmisii | Probleme rețea |

**Filtre pentru Backend-uri:**

| Filtru | Scop | Backend |
|--------|------|---------|
| `ip.addr == 172.28.8.10` | nginx proxy | Proxy |
| `ip.addr == 172.28.8.21` | Backend Alpha | #1 |
| `ip.addr == 172.28.8.22` | Backend Beta | #2 |
| `ip.addr == 172.28.8.23` | Backend Gamma | #3 |

**Combinarea filtrelor:**
- ȘI: `http && tcp.port == 8080`
- SAU: `tcp.port == 8080 || tcp.port == 8443`
- NU: `!arp && !dns`

### Analiza Handshake-ului TCP în Trei Pași

Caută această secvență pentru o conexiune HTTP:
1. **SYN**: Client → nginx (Flags: SYN)
2. **SYN-ACK**: nginx → Client (Flags: SYN, ACK)
3. **ACK**: Client → nginx (Flags: ACK)

Apoi urmează:
4. **HTTP GET**: Client → nginx (cererea HTTP)
5. **HTTP 200**: nginx → Client (răspunsul HTTP)

Filtru pentru a vedea doar handshake-uri: `tcp.flags.syn == 1`

### Analiza Echilibrării Round-Robin în Wireshark

Pentru a observa cum nginx distribuie cererile:

1. Aplică filtrul: `http.request`
2. Generează 6 cereri consecutive:
   ```bash
   for i in {1..6}; do curl -s http://localhost:8080/; done
   ```
3. Observă în Wireshark distribuția: 1→2→3→1→2→3
4. Examinează antetul `X-Backend-ID` în răspunsuri

### Urmărirea unei Conversații HTTP Complete

1. Găsește un pachet HTTP din conversația pe care vrei să o examinezi
2. Click dreapta → **Follow → TCP Stream**
3. Vei vedea:
   - **Roșu**: Cererea HTTP (GET /path HTTP/1.1, antete)
   - **Albastru**: Răspunsul HTTP (HTTP/1.1 200 OK, antete, corp)
4. Observă antetele adăugate de nginx: `X-Forwarded-For`, `X-Backend-ID`

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP normal |
| Verde deschis | Trafic HTTP |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |
| Text negru, fundal roșu | Erori TCP |
| Text negru, fundal galben | Avertismente, retransmisii |

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT8\08roWSL\pcap\`
3. Nume fișier conform exercițiului:
   - `captura_s8_handshake.pcap`
   - `captura_s8_roundrobin.pcap`
   - `captura_s8_http_local.pcap`
4. Format: Wireshark/pcap sau pcapng (implicit)

### Exportarea Datelor pentru Analiză

1. **File → Export Packet Dissections → As CSV**
2. Selectează câmpurile de exportat
3. Salvează în folderul `artifacts/` pentru procesare Python

---

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

- Windows 10/11 cu WSL2 activat (Ubuntu 22.04)
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau ulterior
- Git (recomandat)

### Cerințe Hardware

- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Prima Configurare (Se Rulează O Singură Dată)

```bash
# Deschide terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT8/08roWSL

# Verificați cerințele preliminare
python3 setup/verifica_mediu.py

# Dacă apar probleme, rulați asistentul de instalare
python3 setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT8/08roWSL

# Porniți toate serviciile
python3 scripts/porneste_laborator.py

# Verificați că totul funcționează
python3 scripts/porneste_laborator.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Proxy HTTP | http://localhost:8080 | - |
| Proxy HTTPS | https://localhost:8443 | Certificat auto-semnat |
| Backend 1 | intern: 172.28.8.21:8080 | - |
| Backend 2 | intern: 172.28.8.22:8080 | - |
| Backend 3 | intern: 172.28.8.23:8080 | - |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

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
python3 src/exercises/ex_8_01_server_http.py

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
python3 -m http.server 8001 --directory www/
python3 -m http.server 8002 --directory www/
python3 -m http.server 8003 --directory www/

# Porniți proxy-ul
python3 src/exercises/ex_8_02_proxy_invers.py

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

```bash
python3 scripts/ruleaza_demo.py --demo docker-nginx
```

**Ce să observați:**
- Distribuția uniformă a cererilor între cele 3 backend-uri
- Antetele X-Backend-ID și X-Backend-Name în răspunsuri
- Contorul de cereri pentru fiecare backend

### Demo 2: Algoritmi de Echilibrare

Compară diferiții algoritmi de echilibrare a încărcării.

```bash
python3 scripts/ruleaza_demo.py --demo echilibrare
```

**Ce să observați:**
- Round-robin: distribuție egală (1→2→3→1→2→3)
- Weighted: distribuție proporțională (5:3:1)
- Least-connections: rutare dinamică
- IP-hash: persistența sesiunii

### Demo 3: Handshake TCP

Demonstrează stabilirea conexiunii TCP în trei pași.

```bash
python3 scripts/ruleaza_demo.py --demo handshake
```

**Ce să observați în Wireshark:**
- Pachetul SYN inițial de la client
- Răspunsul SYN-ACK de la server
- Confirmarea ACK de la client

## Capturarea și Analiza Traficului

### Capturarea Traficului

```bash
# Folosind scriptul helper (din WSL)
python3 scripts/captureaza_trafic.py --interfata eth0 --iesire pcap/captura_s8.pcap

# Sau folosind Wireshark direct
# Deschideți Wireshark > Selectați interfața vEthernet (WSL) > Porniți captura
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

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT8/08roWSL

# Opriți toate containerele (păstrează datele, Portainer rămâne activ!)
python3 scripts/opreste_laborator.py

# Verificați oprirea
docker ps
# Ar trebui să vezi doar: portainer
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```bash
# Eliminați toate containerele, rețelele și volumele pentru această săptămână
python3 scripts/curatare.py --complet

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

#### Docker nu pornește în WSL

**Simptome:** Eroare "Cannot connect to the Docker daemon"

**Soluție:**
```bash
# Pornește serviciul Docker în WSL
sudo service docker start
# Parolă: stud

# Verifică statusul
sudo service docker status

# Verifică cu
docker info
```

#### Portul 8080 este ocupat

**Simptome:** Eroare "Bind for 0.0.0.0:8080 failed: port is already allocated"

**Soluție:**
```bash
# Găsiți procesul care folosește portul (în WSL)
ss -tlnp | grep 8080

# Opriți procesul sau folosiți alt port
```

#### Containerele nu pornesc

**Soluție:**
```bash
# Verificați jurnalele containerelor
docker logs week8-nginx-proxy
docker logs week8-backend-1

# Reporniți serviciile
python3 scripts/opreste_laborator.py
python3 scripts/porneste_laborator.py --reconstruieste
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
│  ┌─────────┐ ┌─────────┐ ┌─────────┐             │               │
│  │Backend 1│ │Backend 2│ │Backend 3│             │               │
│  │ (Alpha) │ │ (Beta)  │ │ (Gamma) │             │               │
│  │ :8080   │ │ :8080   │ │ :8080   │             │               │
│  │.21      │ │.22      │ │.23      │             │               │
│  └─────────┘ └─────────┘ └─────────┘             │               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
          │
          │ Expunere porturi
          ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Gazdă Windows                               │
│                                                                  │
│   localhost:9000 ──► Portainer (administrare globală)            │
│   localhost:8080 ──► nginx HTTP                                  │
│   localhost:8443 ──► nginx HTTPS                                 │
│                                                                  │
│   Wireshark ──► Captură trafic pe interfața vEthernet (WSL)      │
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

### Probleme Specifice Săptămânii 8

**Problemă:** nginx nu pornește
```bash
# Verifică configurația nginx
docker exec week8-nginx-proxy nginx -t

# Verifică log-urile nginx
docker logs week8-nginx-proxy

# Verifică că backend-urile sunt pornite
docker ps | grep week8-backend
```

**Problemă:** Backend-urile nu răspund
```bash
# Verifică starea de sănătate
curl -i http://localhost:8080/nginx-health

# Verifică direct un backend
docker exec week8-backend-1 curl -s http://localhost:8080/health
```

**Problemă:** Echilibrarea nu funcționează corect
```bash
# Testează manual
for i in {1..10}; do
  echo "Cerere $i:"
  curl -s http://localhost:8080/ | grep Backend
done
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week8-laboratory-network

# Verifică DNS în container
docker exec week8-backend-1 cat /etc/resolv.conf
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 8080

# Oprește procesul sau folosește alt port
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT8/08roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/opreste_laborator.py

# Verifică - ar trebui să vezi doar portainer
docker ps
```

### Sfârșit de Săptămână (Completă)

```bash
# Curățare completă laborator
python3 scripts/curatare.py --complet

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
docker stop $(docker ps -q --filter "name=week8")

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

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
