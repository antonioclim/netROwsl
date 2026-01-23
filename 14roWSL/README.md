# Săptămâna 14: Recapitulare Integrată și Evaluare Proiect

> Laborator Rețele de Calculatoare - ASE, Informatică Economică
>
> by Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `14roWSL`

**Arhitectura Mediului:**
```
Windows 11 → WSL2 → Ubuntu 22.04 (implicit) → Docker Engine → Portainer CE
```

**Credențiale Standard:**
| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

**⚠️ IMPORTANT:** Portul **9000** este rezervat pentru Portainer. Serverul Echo utilizează portul **9090**.

---

## 📥 Clonarea Laboratorului Acestei Săptămâni

### Pasul 1: Deschide PowerShell (Windows)

Apasă `Win + X` → Selectează "Windows Terminal" sau "PowerShell"

### Pasul 2: Navighează și Clonează

```powershell
# Creează folderul de rețele dacă nu există
mkdir D:\RETELE -ErrorAction SilentlyContinue
cd D:\RETELE

# Clonează Săptămâna 14
git clone https://github.com/antonioclim/netROwsl.git SAPT14
cd SAPT14
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 14roWSL/
cd 14roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT14\
    └── 14roWSL\
        ├── artifacts/       # Rezultate generate
        ├── docker/          # Configurație Docker
        │   ├── docker-compose.yml
        │   └── Dockerfile
        ├── docs/            # Documentație suplimentară
        │   ├── rezumat_teoretic.md
        │   ├── depanare.md
        │   └── glosar.md    # 📖 Definiții termeni tehnici
        ├── homework/        # Teme pentru acasă
        │   ├── README.md
        │   └── exercises/
        ├── pcap/            # Fișiere de captură .pcap
        ├── scripts/         # Scripturi de automatizare
        │   └── utils/       # Utilitare Docker și rețea
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă
        │   ├── apps/        # Aplicații demonstrative
        │   │   ├── backend_server.py
        │   │   ├── lb_proxy.py
        │   │   └── tcp_echo_server.py
        │   └── exercises/   # Exerciții laborator
        ├── tests/           # Teste automatizate
        └── README.md        # Acest fișier
```

> 💡 **Termen necunoscut?** Consultă [`docs/glosar.md`](docs/glosar.md) pentru definiții.

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
cd /mnt/d/RETELE/SAPT14/14roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor pentru Săptămâna 14

Navighează: **Home → local → Containers**

Vei vedea containerele specifice laboratorului:
- **week14_lb** - Load Balancer (172.20.0.10 / 172.21.0.10)
- **week14_app1** - Backend Server 1 (172.20.0.2)
- **week14_app2** - Backend Server 2 (172.20.0.3)
- **week14_echo** - Server Echo TCP (172.20.0.20)
- **week14_client** - Container client pentru teste (172.21.0.2)

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

### Vizualizarea Rețelelor

Navighează: **Networks**

Vei vedea două rețele pentru acest laborator:
- **week14_backend_net** (172.20.0.0/24) - Rețea pentru comunicarea LB ↔ Backend-uri
- **week14_frontend_net** (172.21.0.0/24) - Rețea pentru comunicarea Client ↔ LB

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a analiza distribuția round-robin a load balancer-ului
- Pentru analiza traficului TCP Echo

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
cd /mnt/d/RETELE/SAPT14/14roWSL

# Pornește mediul de laborator
python3 scripts/porneste_lab.py
```

#### 🔮 Exercițiu de Predicție #1: Load Balancer

**Înainte de a rula comanda de mai jos, răspunde:**
1. Câte răspunsuri diferite vei vedea? (app1, app2, sau ambele?)
2. În ce ordine vor apărea? (aleatoriu, alternativ, sau altceva?)
3. Ce se întâmplă dacă oprești un backend în timpul testului?

```bash
# Testează load balancer - observă distribuția!
for i in {1..10}; do curl -s http://localhost:8080/; echo; done
```

**După rulare:** Compară predicția cu rezultatul. Dacă ai ghicit alternare app1/app2, felicitări - ai înțeles round-robin!

#### 🔮 Exercițiu de Predicție #2: Echo Server

**Înainte de a rula:**
- Ce crezi că va returna serverul echo? Exact același text, sau cu modificări?

```bash
# Testează echo server
echo "Test Message" | nc localhost 9090
```

**Verifică:** Răspunsul trebuie să conțină exact "Test Message".

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 14

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

**Filtre pentru Load Balancer:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.port == 8080` | Trafic load balancer | Vezi cereri HTTP către LB |
| `http` | Tot traficul HTTP | Analiză generală HTTP |
| `http.request.method == "GET"` | Cereri GET | Vezi cererile clienților |
| `http.response.code == 200` | Răspunsuri OK | Verifică răspunsuri reușite |
| `http.request.uri contains "lb-status"` | Status LB | Verifică starea LB |

**Filtre pentru Backend-uri:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.port == 8001` | Backend 1 | Trafic către app1 |
| `tcp.port == 8002` | Backend 2 | Trafic către app2 |
| `tcp.port in {8001, 8002}` | Ambele backend-uri | Compară distribuția |
| `ip.addr == 172.20.0.2` | IP App1 | Trafic container app1 |
| `ip.addr == 172.20.0.3` | IP App2 | Trafic container app2 |

**Filtre pentru Echo Server:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.port == 9090` | Echo Server | Trafic TCP Echo |
| `tcp.stream` | Stream TCP | Urmărește conversație |
| `tcp.flags.syn == 1` | Conexiuni noi | Handshake TCP |
| `tcp.flags.fin == 1` | Închideri conexiuni | Terminare TCP |

**Filtre pentru Rețelele Laboratorului:**

| Filtru | Scop | Rețea |
|--------|------|-------|
| `ip.addr == 172.20.0.0/24` | Rețea backend | week14_backend_net |
| `ip.addr == 172.21.0.0/24` | Rețea frontend | week14_frontend_net |
| `ip.addr == 172.20.0.10` | Load Balancer (backend) | Interfața internă LB |
| `ip.addr == 172.21.0.10` | Load Balancer (frontend) | Interfața externă LB |

**Combinarea filtrelor:**
- ȘI: `tcp.port == 8080 && http.request.method == "GET"`
- SAU: `tcp.port == 8001 || tcp.port == 8002`
- NU: `!arp && !icmp`

### Analiza Distribuției Round-Robin

Pentru a observa distribuția round-robin:

1. **Pornește captura în Wireshark** (interfața vEthernet WSL)
2. **Generează trafic:**
   ```bash
   for i in {1..10}; do curl -s http://localhost:8080/ && sleep 0.5; done
   ```
3. **Oprește captura**
4. **Aplică filtru:** `tcp.port in {8001, 8002} && http`
5. **Observă:** Cererile alternează între 8001 și 8002

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP normal |
| Albastru deschis | Trafic UDP |
| Verde deschis | Trafic HTTP |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |
| Text negru, fundal roșu | Erori TCP, RST |
| Text negru, fundal galben | Avertismente, retransmisii |

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT14\14roWSL\pcap\`
3. Nume fișier conform exercițiului:
   - `captura_s14_lb_roundrobin.pcap` - Load balancing
   - `captura_s14_echo.pcap` - Echo TCP
   - `captura_s14_failover.pcap` - Test failover
4. Format: Wireshark/pcap sau pcapng (implicit)

---

## Prezentare Generală

Această sesiune de laborator reprezintă culminarea cursului de Rețele de Calculatoare, integrând concepte și competențe practice dezvoltate pe parcursul semestrului. Mediul de laborator constă într-o arhitectură web cu echilibrare de încărcare ce demonstrează principii fundamentale de rețelistică într-un context containerizat.

## Obiective de Învățare

La finalul acestei sesiuni, veți fi capabili să:

1. **Identificați** componentele unei arhitecturi web cu echilibrare de încărcare
2. **Explicați** funcționarea distribuției round-robin și comunicării reverse proxy
3. **Demonstrați** utilizarea instrumentelor de captură și analiză a pachetelor
4. **Analizați** comportamentul TCP/IP în scenarii client-server
5. **Construiți** scripturi pentru verificarea funcționalității serviciilor de rețea
6. **Evaluați** performanța sistemelor distribuite prin metrici practice

## Cerințe Preliminare

### Software Necesar

| Software | Versiune | Scop |
|----------|---------|------|
| Windows 10/11 | 21H2+ | Sistem de operare gazdă |
| WSL2 | Ubuntu 22.04+ | Mediu de execuție Linux |
| Docker Engine | 24.0+ | Rulare containere (în WSL) |
| Portainer CE | 2.19+ | Management vizual Docker (port 9000) |
| Python | 3.11+ | Execuție scripturi |
| Wireshark | 4.0+ | Analiză pachete |
| Git | 2.40+ | Control versiuni (opțional) |

### Hardware Minim
- 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc

## Pornire Rapidă

### 1. Verificare Mediu

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT14/14roWSL
python3 setup/verifica_mediu.py
```

### 2. Pornire Laborator

```bash
python3 scripts/porneste_lab.py
```

### 3. Accesare Servicii

| Serviciu | URL/Port | Descriere |
|----------|----------|-----------|
| Portainer | http://localhost:9000 | Management containere (stud/studstudstud) |
| Load Balancer | http://localhost:8080 | Punct intrare cereri HTTP |
| Backend App 1 | http://localhost:8001 | Server backend #1 |
| Backend App 2 | http://localhost:8002 | Server backend #2 |
| Server Echo | tcp://localhost:9090 | Server echo pentru teste TCP |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Structura Proiectului

```
14roWSL/
├── README.md                    # Acest fișier
├── CHANGELOG.md                 # Istoric modificări
├── LICENSE                      # Licență MIT
├── setup/                       # Configurare mediu
│   ├── verifica_mediu.py        # Verificare cerințe
│   └── requirements.txt         # Dependențe Python
├── docker/                      # Infrastructură Docker
│   ├── docker-compose.yml       # Definiție servicii
│   └── Dockerfile               # Imagine container
├── scripts/                     # Scripturi management
│   ├── porneste_lab.py          # Pornire laborator
│   ├── opreste_lab.py           # Oprire laborator
│   ├── curata.py                # Curățare resurse
│   ├── captura_trafic.py        # Captură pachete
│   ├── ruleaza_demo.py          # Demonstrații
│   └── utils/                   # Utilitare
├── src/                         # Cod sursă
│   ├── apps/                    # Aplicații
│   ├── exercises/               # Exerciții laborator
│   └── utils/                   # Funcții auxiliare
├── tests/                       # Teste
│   └── test_exercitii.py        # Verificare exerciții
├── docs/                        # Documentație
│   ├── rezumat_teoretic.md      # Rezumat concepte
│   └── depanare.md              # Ghid depanare
├── homework/                    # Teme pentru acasă
│   ├── README.md                # Instrucțiuni teme
│   └── exercises/               # Cod starter
├── pcap/                        # Capturi de pachete
└── artifacts/                   # Fișiere generate
```

## Exerciții de Laborator

### Exercițiul 1: Verificarea Mediului
Confirmarea funcționării corecte a infrastructurii.

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT14/14roWSL
python3 setup/verifica_mediu.py
python3 scripts/porneste_lab.py
```

### Exercițiul 2: Analiza Load Balancer-ului
Înțelegerea distribuției round-robin.

```bash
# Trimiteți cereri multiple și observați alternarea
for i in {1..10}; do curl -s http://localhost:8080/; echo; done
```

Observați cum răspunsurile alternează între `app1` și `app2`.

### Exercițiul 3: Testare Server Echo TCP
Verificarea comunicării TCP.

```bash
# Test simplu echo
echo "Salut Lume" | nc localhost 9090

# Test interactiv
nc localhost 9090
# Tastează mesaje și vezi răspunsurile
```

### Exercițiul 4: Captură și Analiză Pachete
Utilizarea Wireshark/tshark.

```bash
# Captură automată
python3 scripts/captura_trafic.py --durata 30 --lab

# Sau manual cu tshark
tshark -i any -f "tcp port 8080 or tcp port 9090" -w pcap/captura.pcap
```

### Verificare Exerciții

```bash
python3 tests/test_exercitii.py --toate
```

## Demonstrații

### Demo Complet
```bash
python3 scripts/ruleaza_demo.py --demo complet
```

### Demo Failover
```bash
python3 scripts/ruleaza_demo.py --demo failover
```

### Generare Trafic
```bash
python3 scripts/ruleaza_demo.py --demo trafic
```

## Captură Pachete

### Pornire Captură
```bash
python3 scripts/captura_trafic.py --durata 30 --iesire pcap/demo.pcap
```

### Filtre Wireshark Utile
```
http                               # Trafic HTTP
tcp.port == 8080                   # Trafic load balancer
tcp.port in {8080, 8001, 8002}     # Tot traficul HTTP laborator
tcp.port == 9090                   # Trafic echo server
tcp.flags.syn == 1                 # Pachete SYN
```

## Oprire și Curățare

### La Sfârșitul Sesiunii

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT14/14roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/opreste_lab.py

# Verifică - ar trebui să vezi doar portainer
docker ps
```

### Curățare Completă

```bash
python3 scripts/curata.py --complet
```

## Teme pentru Acasă

Consultați `homework/README.md` pentru detalii complete.

| Tema | Descriere | Fișier |
|------|-----------|--------|
| 1 | Protocol Echo Îmbunătățit | `tema_14_01_echo_avansat.py` |
| 2 | Load Balancer cu Ponderi | `tema_14_02_lb_ponderat.py` |
| 3 | Analizator PCAP Automat | `tema_14_03_analizator_pcap.py` |

## Arhitectură

```
┌─────────────────────────────────────────────┐
│           REȚEA FRONTEND 172.21.0.0/24      │
│                                             │
│    ┌─────────────┐    ┌─────────────┐      │
│    │   CLIENT    │    │     LB      │ ◄──── Port 8080
│    │ 172.21.0.2  │    │ 172.21.0.10 │      │
│    └─────────────┘    └──────┬──────┘      │
└──────────────────────────────┼──────────────┘
                               │
┌──────────────────────────────┼──────────────┐
│           REȚEA BACKEND 172.20.0.0/24       │
│                              │              │
│    ┌─────────────┐    ┌──────▼──────┐      │
│    │    APP1     │◄───┤     LB      │      │
│    │ 172.20.0.2  │    │ 172.20.0.10 │      │
│    └─────────────┘    └──────┬──────┘      │
│                              │              │
│    ┌─────────────┐           │              │
│    │    APP2     │◄──────────┘              │
│    │ 172.20.0.3  │                          │
│    └─────────────┘                          │
│                                             │
│    ┌─────────────┐                          │
│    │    ECHO     │ ◄──────────────── Port 9090
│    │ 172.20.0.20 │                          │
│    └─────────────┘                          │
└─────────────────────────────────────────────┘

Portainer (Management): http://localhost:9000
```

## Referințe

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.)
- Tanenbaum, A. S. & Wetherall, D. J. (2021). *Computer Networks* (6th ed.)
- Stevens, W. R. (2011). *TCP/IP Illustrated, Volume 1: The Protocols* (2nd ed.)
- Documentație Docker: https://docs.docker.com/
- Documentație Wireshark: https://www.wireshark.org/docs/

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

### Probleme Specifice Săptămânii 14

**Problemă:** Containerele Docker nu pornesc
```bash
# Verifică log-urile pentru fiecare container
docker logs week14_lb
docker logs week14_app1
docker logs week14_app2
docker logs week14_echo

# Verifică dacă porturile sunt ocupate
sudo ss -tlnp | grep -E "8080|8001|8002|9090"
```

**Problemă:** Port 9000 ocupat (conflict cu Portainer)
```bash
# Portul 9000 este REZERVAT pentru Portainer!
# Echo server-ul folosește portul 9090

# Verifică cine folosește portul 9000
sudo ss -tlnp | grep 9000
# Ar trebui să fie Portainer
```

**Problemă:** Load Balancer nu distribuie cererile
```bash
# Verifică starea backend-urilor
curl http://localhost:8001/health
curl http://localhost:8002/health

# Verifică status LB
curl http://localhost:8080/lb-status

# Repornește LB dacă e necesar
docker restart week14_lb
```

**Problemă:** Echo server nu răspunde
```bash
# Verifică dacă containerul rulează
docker ps | grep week14_echo

# Verifică portul
nc -vz localhost 9090

# Verifică log-urile
docker logs week14_echo
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețelele Docker
docker network ls
docker network inspect week14_backend_net
docker network inspect week14_frontend_net

# Verifică DNS în container
docker exec week14_client cat /etc/resolv.conf
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul
sudo ss -tlnp | grep 8080

# Oprește procesul sau modifică porturile în docker-compose.yml
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT14/14roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/opreste_lab.py

# Verifică - ar trebui să vezi doar portainer
docker ps
```

### Sfârșit de Săptămână (Completă)

```bash
# Curățare completă laborator
python3 scripts/curata.py --complet

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
docker stop $(docker ps -q --filter "name=week14_")

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

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
