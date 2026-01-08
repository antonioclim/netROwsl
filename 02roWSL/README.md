# Săptămâna 2: Modele Arhitecturale și Programare Socket

> Laborator Rețele de Calculatoare - ASE, Informatică Economică
> 
> by Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `02roWSL`

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

# Clonează Săptămâna 2
git clone https://github.com/antonioclim/netROwsl.git SAPT2
cd SAPT2
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 02roWSL/
cd 02roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT2\
    └── 02roWSL\
        ├── artifacts/       # Rezultate generate
        ├── docker/          # Configurație Docker
        ├── docs/            # Documentație suplimentară
        ├── homework/        # Teme pentru acasă
        ├── pcap/            # Fișiere de captură
        ├── scripts/         # Scripturi de automatizare
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă exerciții
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
cd /mnt/d/RETELE/SAPT2/02roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor

Navighează: **Home → local → Containers**

Vei vedea un tabel cu toate containerele care include:
- **Nume** - Identificatorul containerului
- **Stare** - Running/Stopped/Paused
- **Imagine** - Imaginea Docker folosită
- **Creat** - Data creării
- **Adresă IP** - Adresa IP în rețeaua Docker
- **Porturi** - Mapările de porturi host:container

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

### Modificarea Adresei IP a Containerului

1. Navighează: **Networks → week2_network**
2. Vezi configurația IPAM curentă (ex: 10.0.2.0/24)
3. Pentru a modifica:
   - Oprește containerele care folosesc rețeaua
   - Editează fișierul `docker/docker-compose.yml`:
     ```yaml
     networks:
       week2_network:
         ipam:
           config:
             - subnet: 10.0.2.0/24  # Modifică subrețeaua aici
               gateway: 10.0.2.1    # Modifică gateway-ul aici
     ```
   - Recreează mediul:
     ```bash
     cd /mnt/d/RETELE/SAPT2/02roWSL
     docker-compose -f docker/docker-compose.yml down
     docker-compose -f docker/docker-compose.yml up -d
     ```
   - Verifică în Portainer: Networks → vezi noua configurație

### Modificarea Porturilor Containerului

1. În Portainer: selectează containerul → "Inspect" → derulează la "HostConfig.PortBindings"
2. Pentru a modifica permanent, editează `docker/docker-compose.yml`:
   ```yaml
   ports:
     - "9090:9090"   # Format: "port_host:port_container"
     - "9095:9091"   # Exemplu: mapează container 9091 la host 9095
   ```
3. Recreează containerul:
   ```bash
   docker-compose -f docker/docker-compose.yml down
   docker-compose -f docker/docker-compose.yml up -d
   ```
4. Verifică: Noile porturi apar în lista de containere din Portainer

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru demonstrații care necesită vizualizarea traficului în timp real
- Când vrei să înțelegi ce se întâmplă "pe fir" în comunicarea rețea

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

Cu Wireshark capturând (vei vedea pachete apărând în timp real), rulează exercițiile de laborator:

```bash
# În terminalul Ubuntu
docker exec -it week2_lab bash

# Rulează comenzi de rețea în container
python /app/exercises/ex_2_01_tcp.py client --message "test"
python /app/exercises/ex_2_02_udp.py client --command "ping"
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 2

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

| Filtru | Scop | Exemplu Utilizare |
|--------|------|-------------------|
| `tcp.port == 9090` | Server TCP laborator | Trafic TCP exercițiu 1 |
| `udp.port == 9091` | Server UDP laborator | Trafic UDP exercițiu 2 |
| `tcp.flags.syn == 1` | Pachete TCP SYN | Inițieri conexiuni TCP |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Doar SYN inițial | Doar conexiuni noi |
| `tcp.flags.fin == 1` | Pachete TCP FIN | Terminări conexiuni |
| `tcp.analysis.retransmission` | Retransmisii TCP | Probleme de rețea |
| `ip.addr == 10.0.2.10` | IP container | Trafic container lab |
| `tcp.port == 9090 \|\| udp.port == 9091` | Tot traficul lab | Combinație TCP+UDP |

**Combinarea filtrelor:**
- ȘI: `tcp.port == 9090 && ip.addr == 10.0.2.10`
- SAU: `tcp.port == 9090 || udp.port == 9091`
- NU: `!arp && !dns`

### Înțelegerea Coloanelor Wireshark

| Coloană | Semnificație | Ce să Cauți |
|---------|--------------|-------------|
| No. | Număr secvență pachet | Ordinea capturii |
| Time | Secunde de la începutul capturii | Analiză timing |
| Source | Adresa IP sursă | Cine a trimis |
| Destination | Adresa IP destinație | Cine primește |
| Protocol | Numele protocolului | TCP, UDP, HTTP, etc. |
| Length | Dimensiune pachet (octeți) | Cantitate date |
| Info | Detalii protocol | Flag-uri, numere secvență, etc. |

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP |
| Albastru deschis | Trafic UDP |
| Verde deschis | Trafic HTTP |
| Text negru, fundal roșu | Erori, checksum-uri greșite |
| Text negru, fundal galben | Avertismente, retransmisii |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |

### Urmărirea unei Conversații TCP

1. Găsește orice pachet din conversația pe care vrei să o examinezi
2. Click dreapta → **Follow → TCP Stream**
3. O fereastră arată conversația completă în text lizibil
   - Text roșu: Date trimise de client
   - Text albastru: Date trimise de server
4. Folosește dropdown-ul pentru a comuta între vizualizări ASCII/Hex/Raw
5. Închide fereastra pentru a reveni la lista de pachete (filtru auto-aplicat)

### Analiza Handshake-ului TCP în Trei Pași

Caută această secvență de pachete (relevantă pentru Exercițiul 1):
1. **SYN**: Client → Server (Flags: SYN) - "Vreau să mă conectez"
2. **SYN-ACK**: Server → Client (Flags: SYN, ACK) - "Accept, și eu vreau să mă conectez"
3. **ACK**: Client → Server (Flags: ACK) - "Confirmat, suntem conectați"

Filtru pentru a vedea doar handshake-uri: `tcp.flags.syn == 1`

### Comparație TCP vs UDP în Wireshark

**TCP (portul 9090):**
- Vei vedea: SYN → SYN-ACK → ACK → PSH-ACK (date) → ... → FIN-ACK
- Fiecare pachet are confirmare (ACK)
- Numerele de secvență cresc

**UDP (portul 9091):**
- Vei vedea: doar datagrame de date
- Fără SYN, ACK sau FIN
- Fiecare pachet este independent

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT2\02roWSL\pcap\`
3. Nume fișier sugestiv: `captura_tcp_udp_ex2.pcap`
4. Format: Wireshark/pcap sau pcapng (implicit)

### Exportarea Datelor pentru Analiză

1. **File → Export Packet Dissections → As CSV**
2. Selectează câmpurile de exportat
3. Salvează în folderul `artifacts/` pentru procesare Python

---

## Prezentare Generală

Această săptămână explorează fundamentele arhitecturale ale rețelelor de calculatoare, concentrându-se pe două modele esențiale: **modelul OSI** (Open Systems Interconnection) cu cele 7 straturi ale sale și **modelul TCP/IP** cu 4 straturi, care reprezintă baza practică a Internetului contemporan.

Componenta practică introduce **programarea socket-urilor**, mecanismul fundamental prin care aplicațiile comunică prin rețea. Veți implementa servere TCP concurente și servere UDP cu protocoale personalizate, observând diferențele comportamentale dintre comunicația orientată pe conexiune (TCP) și cea fără conexiune (UDP).

Laboratorul pune accent pe observarea practică a traficului de rețea folosind Wireshark, permițându-vă să vizualizați handshake-ul TCP în trei pași, schimbul de date și terminarea conexiunii, consolidând astfel înțelegerea teoretică prin experiență directă.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** și **enumerați** cele 7 straturi ale modelului OSI și cele 4 straturi ale modelului TCP/IP
2. **Explicați** diferențele fundamentale dintre TCP (orientat pe conexiune, fiabil) și UDP (fără conexiune, best-effort)
3. **Implementați** un server TCP concurent folosind thread-uri în Python
4. **Construiți** un protocol de aplicație personalizat peste UDP cu comenzi multiple
5. **Analizați** traficul de rețea în Wireshark, identificând handshake-ul TCP și schimbul UDP
6. **Evaluați** scenariile în care TCP sau UDP reprezintă alegerea optimă

## Cerințe Preliminare

### Cunoștințe Necesare

- Concepte de bază ale rețelelor (adrese IP, porturi)
- Programare Python la nivel intermediar
- Familiaritate cu linia de comandă

### Cerințe Software

- Windows 10/11 cu WSL2 activat
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau mai recent
- Git (opțional, recomandat)

### Cerințe Hardware

- Minimum 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conexiune la rețea

## Pornire Rapidă

### Prima Configurare (O Singură Dată)

```bash
# Deschideți terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT2/02roWSL

# Verificați cerințele preliminare
python3 setup/verify_environment.py

# Dacă apar probleme, rulați asistentul de instalare
python3 setup/install_prerequisites.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT2/02roWSL

# Porniți toate serviciile
python3 scripts/start_lab.py

# Verificați că totul funcționează
python3 scripts/start_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Server TCP | localhost:9090 | - |
| Server UDP | localhost:9091 | - |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Exerciții de Laborator

### Exercițiul 1: Server TCP Concurent

**Obiectiv:** Implementarea și testarea unui server TCP care poate gestiona mai mulți clienți simultan folosind thread-uri.

**Durată estimată:** 30-40 minute

**Pregătire Wireshark:** Deschide Wireshark pe Windows și pornește captura pe interfața `vEthernet (WSL)` cu filtrul `tcp.port == 9090` ÎNAINTE de a începe exercițiul.

**Descrierea Protocolului:**
- Clientul trimite un mesaj text
- Serverul răspunde cu textul convertit la majuscule, prefixat cu "OK: "
- Conexiunea rămâne deschisă pentru mesaje multiple

**Pași:**

1. **Porniți serverul în modul threaded:**
   ```bash
   # În containerul Docker
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server --mode threaded
   ```

2. **Conectați un client:**
   ```bash
   # Într-un alt terminal
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py client --message "salut lume"
   ```

3. **Testați concurența cu mai mulți clienți:**
   ```bash
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py load --clients 5 --messages 10
   ```

4. **Comparați cu modul iterativ:**
   ```bash
   # Opriți serverul anterior (Ctrl+C), apoi:
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server --mode iterative
   # Rulați din nou testul de încărcare și observați diferența
   ```

**Ce să observați:**
- În modul threaded, clienții primesc răspunsuri în paralel
- În modul iterativ, clienții sunt procesați secvențial
- Wireshark: identificați cele 3 pachete ale handshake-ului TCP (SYN, SYN-ACK, ACK)

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 1
```

---

### Exercițiul 2: Server UDP cu Protocol Personalizat

**Obiectiv:** Construirea unui server UDP care implementează un protocol de aplicație cu comenzi multiple.

**Durată estimată:** 25-35 minute

**Pregătire Wireshark:** Schimbă filtrul la `udp.port == 9091` pentru a observa traficul UDP.

**Comenzile Protocolului:**
| Comandă | Descriere | Exemplu |
|---------|-----------|---------|
| `ping` | Verifică disponibilitatea | Răspuns: `PONG` |
| `upper:text` | Convertește la majuscule | `upper:salut` → `SALUT` |
| `lower:TEXT` | Convertește la minuscule | `lower:SALUT` → `salut` |
| `reverse:text` | Inversează textul | `reverse:abc` → `cba` |
| `echo:text` | Returnează textul neschimbat | `echo:test` → `test` |
| `time` | Returnează ora serverului | Răspuns: `2025-01-06 14:30:45` |
| `help` | Listează comenzile disponibile | - |

**Pași:**

1. **Porniți serverul UDP:**
   ```bash
   docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py server
   ```

2. **Testați în modul interactiv:**
   ```bash
   docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py client --interactive
   ```
   
   În modul interactiv, introduceți comenzi direct:
   ```
   > ping
   PONG
   > upper:rețele de calculatoare
   REȚELE DE CALCULATOARE
   > time
   2025-01-06 14:30:45
   > quit
   ```

3. **Trimiteți comenzi individuale:**
   ```bash
   docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py client --command "reverse:Python"
   ```

**Ce să observați:**
- UDP nu are handshake - datagramele sunt trimise direct
- Fiecare cerere-răspuns este independentă (fără stare)
- În Wireshark: observați că nu există SYN/ACK, doar pachete de date

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 2
```

---

### Exercițiul 3: Capturarea și Analiza Traficului

**Obiectiv:** Utilizarea Wireshark pentru capturarea și analiza traficului TCP și UDP.

**Durată estimată:** 20-30 minute

**Pași:**

1. **Porniți captura:**
   ```bash
   python3 scripts/capture_traffic.py --interface any --output pcap/week2_capture.pcap
   ```

2. **Generați trafic TCP:**
   ```bash
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py client --message "test captură"
   ```

3. **Generați trafic UDP:**
   ```bash
   docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py client --command "ping"
   ```

4. **Opriți captura (Ctrl+C) și deschideți în Wireshark:**
   ```powershell
   # În PowerShell
   & "C:\Program Files\Wireshark\Wireshark.exe" "D:\RETELE\SAPT2\02roWSL\pcap\week2_capture.pcap"
   ```

5. **Aplicați filtre Wireshark:**
   - Pentru TCP: `tcp.port == 9090`
   - Pentru UDP: `udp.port == 9091`
   - Pentru handshake: `tcp.flags.syn == 1`

**Ce să identificați în Wireshark:**
- **TCP:** SYN → SYN-ACK → ACK (handshake), PSH-ACK (date), FIN-ACK (terminare)
- **UDP:** Doar pachete de date, fără confirmare

## Demonstrații

### Demo 1: Comparație TCP vs UDP

Demonstrație automatizată care evidențiază diferențele comportamentale dintre cele două protocoale.

```bash
python3 scripts/run_demo.py --demo 1
```

**Ce veți observa:**
- TCP: Latență inițială mai mare (handshake), dar livrare garantată
- UDP: Răspuns imediat, dar fără garanții de livrare
- Statistici comparative în timp real

### Demo 2: Gestionarea Clienților Concurenți

Demonstrație a modului în care un server threaded gestionează conexiuni multiple simultan.

```bash
python3 scripts/run_demo.py --demo 2
```

**Ce veți observa:**
- 10 clienți conectați simultan
- Răspunsuri intercalate (nu secvențiale)
- Timpul total vs. timpul cumulativ

## Capturarea și Analiza Pachetelor

### Pornirea Capturii

```bash
# Capturare cu filtrare
python3 scripts/capture_traffic.py --filter "port 9090 or port 9091" --output pcap/week2_lab.pcap

# Sau folosiți Wireshark direct pe Windows
# Selectați interfața vEthernet (WSL)
```

### Filtre Wireshark Recomandate

```
# Trafic TCP pe portul serverului
tcp.port == 9090

# Trafic UDP pe portul serverului
udp.port == 9091

# Doar pachete SYN (inițiere conexiune TCP)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Doar pachete FIN (terminare conexiune TCP)
tcp.flags.fin == 1

# Retransmisii TCP (probleme de rețea)
tcp.analysis.retransmission

# Combinație: tot traficul laboratorului
tcp.port == 9090 || udp.port == 9091
```

## Oprire și Curățare

### Sfârșitul Sesiunii

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT2/02roWSL

# Opriți toate containerele de laborator (Portainer rămâne activ!)
python3 scripts/stop_lab.py

# Verificați oprirea
docker ps
# Ar trebui să vezi doar: portainer
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```bash
# Eliminați toate containerele, rețelele și volumele pentru această săptămână
python3 scripts/cleanup.py --full

# Verificați curățarea
docker system df
```

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de lucru individual.

### Tema 1: Server TCP cu Protocol de Autentificare
Extindeți serverul TCP pentru a suporta autentificare simplă (utilizator/parolă) înainte de procesarea comenzilor.

### Tema 2: Client UDP cu Retry și Timeout
Implementați un client UDP robust care reîncearcă automat trimiterea dacă nu primește răspuns în 2 secunde.

## Depanare

### Probleme Frecvente

#### Problema: Portul este deja în uz

**Soluție:** 
```bash
# În WSL, găsiți procesul care folosește portul
sudo ss -tlnp | grep 9090

# Sau folosiți curățarea
python3 scripts/cleanup.py --full
```

#### Problema: Docker nu pornește

**Soluție:**
```bash
# Porniți serviciul Docker în WSL
sudo service docker start
# Parolă: stud

# Verificați statusul
sudo service docker status
```

#### Problema: Conexiune refuzată la server

**Soluție:**
```bash
# Verificați că serverul rulează
docker ps

# Verificați logurile
docker logs week2_lab
```

#### Problema: Wireshark nu vede traficul Docker

**Soluție:**
- Selectați interfața `vEthernet (WSL)`, nu `Ethernet` sau `Wi-Fi`
- Asigurați-vă că containerele sunt pe rețea bridge, nu host
- Alternativ, capturați din interiorul containerului cu `tcpdump`

Consultați `docs/troubleshooting.md` pentru mai multe soluții.

## Fundamente Teoretice

### Modelul OSI (7 Straturi)

| Nr. | Strat | Funcție | Exemple |
|-----|-------|---------|---------|
| 7 | Aplicație | Interfață cu utilizatorul | HTTP, FTP, SMTP |
| 6 | Prezentare | Formatare, criptare | SSL/TLS, JPEG |
| 5 | Sesiune | Gestiunea dialogului | NetBIOS, RPC |
| 4 | Transport | Livrare end-to-end | TCP, UDP |
| 3 | Rețea | Rutare, adresare logică | IP, ICMP |
| 2 | Legătură de Date | Acces la mediu, cadre | Ethernet, Wi-Fi |
| 1 | Fizic | Biți pe mediu fizic | Cabluri, semnale |

### Modelul TCP/IP (4 Straturi)

| Nr. | Strat TCP/IP | Echivalent OSI | Protocoale |
|-----|--------------|----------------|------------|
| 4 | Aplicație | 5, 6, 7 | HTTP, FTP, DNS |
| 3 | Transport | 4 | TCP, UDP |
| 2 | Internet | 3 | IP, ICMP, ARP |
| 1 | Acces la Rețea | 1, 2 | Ethernet, Wi-Fi |

### TCP vs UDP

| Caracteristică | TCP | UDP |
|----------------|-----|-----|
| Conexiune | Orientat pe conexiune | Fără conexiune |
| Fiabilitate | Garantată (ACK, retransmisie) | Best-effort |
| Ordine | Păstrată | Nu este garantată |
| Control flux | Da (fereastră glisantă) | Nu |
| Overhead | Mai mare (header 20+ bytes) | Mai mic (header 8 bytes) |
| Utilizare | Web, email, transfer fișiere | Streaming, DNS, jocuri |

## Diagrama Arhitecturii

```
┌─────────────────────────────────────────────────────────────────┐
│                         Windows Host                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │   PowerShell    │    │    Wireshark    │    │   Browser    │ │
│  │   (scripturi)   │    │  (analiză pcap) │    │  (Portainer) │ │
│  └────────┬────────┘    └────────┬────────┘    └──────┬───────┘ │
│           │                      │                     │         │
│  ─────────┴──────────────────────┴─────────────────────┴──────── │
│                              WSL2                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                     Docker Network                           │ │
│  │                    (week2_network)                           │ │
│  │                     10.0.2.0/24                              │ │
│  │  ┌─────────────────────────────────────────────────────┐    │ │
│  │  │              Container: week2_lab                    │    │ │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │    │ │
│  │  │  │ Server TCP  │  │ Server UDP  │  │   tcpdump   │  │    │ │
│  │  │  │  :9090      │  │   :9091     │  │  (captură)  │  │    │ │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  │    │ │
│  │  └─────────────────────────────────────────────────────┘    │ │
│  │                                                              │ │
│  │  ┌─────────────────────────────────────────────────────┐    │ │
│  │  │              Container: portainer (global)           │    │ │
│  │  │                     :9000                            │    │ │
│  │  └─────────────────────────────────────────────────────┘    │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

Handshake TCP (3-Way):
┌────────┐                              ┌────────┐
│ Client │                              │ Server │
└───┬────┘                              └───┬────┘
    │                                       │
    │  ──────── SYN (seq=x) ─────────────►  │
    │                                       │
    │  ◄─────── SYN-ACK (seq=y, ack=x+1) ── │
    │                                       │
    │  ──────── ACK (ack=y+1) ────────────► │
    │                                       │
    │        [Conexiune stabilită]          │
    │                                       │

Schimb UDP (fără handshake):
┌────────┐                              ┌────────┐
│ Client │                              │ Server │
└───┬────┘                              └───┬────┘
    │                                       │
    │  ──────── Datagramă cerere ────────►  │
    │                                       │
    │  ◄─────── Datagramă răspuns ───────── │
    │                                       │
    │    [Fără confirmare de primire]       │
```

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1*. Addison-Wesley.
- Documentația Python: [socket — Low-level networking interface](https://docs.python.org/3/library/socket.html)

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

**Problemă:** Portainer afișează "No endpoint available"
1. În interfața Portainer, click pe "Environments"
2. Click pe "Add environment"
3. Selectează "Docker" → "Connect via socket"
4. Lasă calea implicită: `/var/run/docker.sock`
5. Click "Connect"

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

**Problemă:** Filtrul devine roșu (sintaxă invalidă)
- Verifică ghilimelele și parantezele
- `==` pentru egalitate, nu `=`
- Exemple corecte: `tcp.port == 9090`, `udp.port == 9091`

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week2_network

# Verifică DNS în container
docker exec week2_lab cat /etc/resolv.conf

# Testează conectivitatea
docker exec week2_lab ping -c 2 8.8.8.8
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 9090

# Sau
sudo netstat -tlnp | grep 9090

# Oprește procesul sau folosește alt port în docker-compose.yml
```

**Problemă:** Containerul nu pornește
```bash
# Verifică log-urile containerului
docker logs week2_lab

# Verifică dacă imaginea există
docker images | grep week2

# Reconstruiește imaginea
cd /mnt/d/RETELE/SAPT2/02roWSL
docker-compose -f docker/docker-compose.yml build --no-cache
```

### Probleme WSL

**Problemă:** WSL nu pornește sau este lent
```powershell
# În PowerShell ca Administrator
wsl --shutdown
wsl --update
wsl
```

**Problemă:** Nu găsesc fișierele în WSL
```bash
# Drive-urile Windows sunt montate în /mnt/
ls /mnt/c    # C:
ls /mnt/d    # D:

# Calea corectă pentru laborator
cd /mnt/d/RETELE/SAPT2/02roWSL
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT2/02roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
docker-compose -f docker/docker-compose.yml down

# Verifică - ar trebui să arate încă portainer
docker ps
# OUTPUT așteptat:
# CONTAINER ID   IMAGE                    NAMES
# abc123...      portainer/portainer-ce   portainer
```

### Sfârșit de Săptămână (Completă)

```bash
# Elimină containerele și rețelele acestei săptămâni
docker-compose -f docker/docker-compose.yml down --volumes

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
docker ps -q | xargs -I {} sh -c 'docker inspect --format="{{.Name}}" {} | grep -v portainer && docker stop {}' 2>/dev/null

# Metodă alternativă mai sigură:
docker stop $(docker ps -q --filter "name=week")

# Elimină containerele oprite (nu Portainer)
docker container prune -f

# Elimină imaginile nefolosite
docker image prune -a -f

# Elimină rețelele nefolosite  
docker network prune -f

# Elimină volumele nefolosite (ATENȚIE: nu portainer_data!)
docker volume ls | grep -v portainer | awk 'NR>1 {print $2}' | xargs -r docker volume rm

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
