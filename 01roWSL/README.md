# Săptămâna 1: Fundamentele Rețelelor de Calculatoare

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | Laborator
>
> by Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `01roWSL`

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

# Clonează Săptămâna 1
git clone https://github.com/antonioclim/netROwsl.git SAPT1
cd SAPT1
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 01roWSL/
cd 01roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT1\
    └── 01roWSL\
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
cd /mnt/d/RETELE/SAPT1/01roWSL

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

1. Navighează: **Networks → week1_network**
2. Vezi configurația IPAM curentă (ex: 172.20.1.0/24)
3. Pentru a modifica:
   - Oprește containerele care folosesc rețeaua
   - Editează fișierul `docker/docker-compose.yml`:
     ```yaml
     networks:
       week1_network:
         ipam:
           config:
             - subnet: 172.20.1.0/24  # Modifică subrețeaua aici
               gateway: 172.20.1.1    # Modifică gateway-ul aici
     ```
   - Recreează mediul:
     ```bash
     cd /mnt/d/RETELE/SAPT1/01roWSL
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
docker exec -it week1_lab bash

# Rulează comenzi de rețea în container
ping 172.20.1.1
nc -l -p 9090  # Pornește server TCP
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

| Filtru | Scop | Exemplu Utilizare |
|--------|------|-------------------|
| `tcp` | Tot traficul TCP | Analiză TCP generală |
| `udp` | Tot traficul UDP | Analiză DNS, DHCP |
| `tcp.port == 9090` | Port specific | Trafic exerciții laborator |
| `ip.addr == 172.20.1.2` | IP specific | Trafic container |
| `tcp.flags.syn == 1` | Pachete TCP SYN | Inițieri conexiuni |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Doar SYN inițial | Doar conexiuni noi |
| `tcp.flags.fin == 1` | Pachete TCP FIN | Terminări conexiuni |
| `http` | Trafic HTTP | Trafic web |
| `icmp` | ICMP (ping) | Teste conectivitate |
| `tcp.analysis.retransmission` | Retransmisii | Probleme rețea |
| `frame.len > 100` | Pachete mari | Transfer date |
| `tcp.stream eq 0` | Primul stream TCP | Urmărește o singură conversație |

**Combinarea filtrelor:**
- ȘI: `tcp.port == 9090 && ip.addr == 172.20.1.2`
- SAU: `tcp.port == 9090 || tcp.port == 9091`
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

Caută această secvență de pachete:
1. **SYN**: Client → Server (Flags: SYN) - "Vreau să mă conectez"
2. **SYN-ACK**: Server → Client (Flags: SYN, ACK) - "Accept, și eu vreau să mă conectez"
3. **ACK**: Client → Server (Flags: ACK) - "Confirmat, suntem conectați"

Filtru pentru a vedea doar handshake-uri: `tcp.flags.syn == 1`

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT1\01roWSL\pcap\`
3. Nume fișier sugestiv: `captura_exercitiu_3.pcap`
4. Format: Wireshark/pcap sau pcapng (implicit)

### Exportarea Datelor pentru Analiză

1. **File → Export Packet Dissections → As CSV**
2. Selectează câmpurile de exportat
3. Salvează în folderul `artifacts/` pentru procesare Python

---

## Prezentare Generală

Această sesiune de laborator introduce conceptele fundamentale ale rețelelor de calculatoare, concentrându-se pe instrumentele de diagnostic și tehnicile de analiză esențiale pentru înțelegerea comunicării în rețea. Studenții vor dobândi experiență practică cu utilitare de rețea la nivel de linie de comandă, captură de pachete și paradigme de programare a socket-urilor.

Laboratorul acoperă stiva TCP/IP de la o perspectivă practică, demonstrând modul în care datele traversează straturile rețelei și cum pot fi observate, capturate și analizate diferitele protocoale. Această cunoaștere fundamentală formează baza pentru toate sesiunile de laborator ulterioare.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** interfețele de rețea, adresele IP și tabelele de rutare folosind utilitare Linux
2. **Explicați** diferențele dintre protocoalele TCP și UDP în ceea ce privește stabilirea conexiunii și fiabilitatea
3. **Demonstrați** conectivitatea de bază a rețelei folosind ping, netcat și socket-uri Python
4. **Analizați** traficul de rețea capturat folosind tcpdump, tshark și Wireshark
5. **Construiți** aplicații simple client-server folosind socket-uri TCP în Python
6. **Evaluați** modelele de trafic de rețea prin analiza fișierelor PCAP

## Cerințe Preliminare

### Cunoștințe Necesare

- Operarea de bază în linia de comandă Linux
- Cunoștințe elementare de programare Python
- Înțelegerea numerotării binare și hexazecimale
- Familiaritate cu modelul stratificat TCP/IP

### Cerințe Software

- Windows 10/11 cu WSL2 activat
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (nativ Windows)
- Python 3.11 sau mai recent
- Git

### Cerințe Hardware

- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate de rețea

## Pornire Rapidă

### Configurare Inițială (Rulați o Singură Dată)

```bash
# Deschideți terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT1/01roWSL

# Verificați cerințele preliminare
python3 setup/verifica_mediu.py

# Dacă apar probleme, rulați asistentul de instalare
python3 setup/instaleaza_prerequisite.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT1/01roWSL

# Porniți toate serviciile
python3 scripts/porneste_lab.py

# Verificați că totul rulează
python3 scripts/porneste_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Container Lab | localhost:9090 (TCP) | N/A |
| Container Lab | localhost:9091 (UDP) | N/A |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Arhitectura Laboratorului

```
┌─────────────────────────────────────────────────────────────────┐
│                        Windows 10/11                            │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │   Wireshark  │  │  PowerShell  │  │   Windows Terminal    │  │
│  │  (Analiză)   │  │  (Scripturi) │  │      (WSL2)           │  │
│  └──────────────┘  └──────────────┘  └───────────────────────┘  │
│         │                 │                      │              │
│         └─────────────────┼──────────────────────┘              │
│                           │                                     │
├───────────────────────────┼─────────────────────────────────────┤
│                    WSL2 (Ubuntu 22.04)                          │
│  ┌────────────────────────┴────────────────────────────────┐    │
│  │                    Docker Engine                         │    │
│  │  ┌───────────────────────────────────────────────────┐  │    │
│  │  │              week1_network (172.20.1.0/24)        │  │    │
│  │  │  ┌─────────────────────┐                          │  │    │
│  │  │  │    week1_lab        │   ┌──────────────────┐   │  │    │
│  │  │  │  ├─ Python 3.12     │   │    portainer     │   │  │    │
│  │  │  │  ├─ tcpdump/tshark  │   │  (global :9000)  │   │  │    │
│  │  │  │  ├─ netcat          │   └──────────────────┘   │  │    │
│  │  │  │  └─ iproute2        │                          │  │    │
│  │  │  │  :9090 (TCP)        │                          │  │    │
│  │  │  │  :9091 (UDP)        │                          │  │    │
│  │  │  └─────────────────────┘                          │  │    │
│  │  └───────────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Exerciții de Laborator

### Exercițiul 1: Inspectarea Interfețelor de Rețea

**Obiectiv:** Identificați și documentați toate interfețele de rețea și configurările acestora.

**Durată:** 15 minute

**Pași:**

1. Conectați-vă la containerul de laborator:
   ```bash
   docker exec -it week1_lab bash
   ```

2. Afișați toate interfețele de rețea:
   ```bash
   ip addr show
   ip -br addr show  # format scurt
   ```

3. Examinați tabela de rutare:
   ```bash
   ip route show
   ```

4. Vizualizați socket-urile active:
   ```bash
   ss -tunap
   ```

**Ce să observați:**

- Adrese IPv4 și IPv6 pe fiecare interfață
- Stările interfețelor (UP/DOWN)
- Gateway-ul implicit în tabela de rutare
- Porturi în starea LISTEN

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 1
```

---

### Exercițiul 2: Testarea Conectivității

**Obiectiv:** Testați conectivitatea rețelei folosind ICMP și măsurați latența.

**Durată:** 20 minute

**Pași:**

1. Testați conectivitatea loopback:
   ```bash
   ping -c 4 127.0.0.1
   ping -c 4 localhost
   ```

2. Testați conectivitatea la gateway:
   ```bash
   # Aflați gateway-ul
   ip route | grep default
   
   # Pingați gateway-ul (înlocuiți cu adresa voastră)
   ping -c 4 172.20.1.1
   ```

3. Rulați exercițiul Python de măsurare a latenței:
   ```bash
   cd /work/src/exercises
   python3 ex_1_01_latenta_ping.py
   ```

**Ce să observați:**

- Timpii de răspuns (RTT - Round Trip Time)
- Variația în latență
- Pierderi de pachete (dacă există)

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 2
```

---

### Exercițiul 3: Comunicarea TCP

**Obiectiv:** Stabiliți o conexiune TCP și observați stările socket-urilor.

**Durată:** 25 minute

**Pregătire Wireshark:** Deschide Wireshark pe Windows și pornește captura pe interfața `vEthernet (WSL)` ÎNAINTE de a începe exercițiul.

**Pași:**

1. Porniți un server TCP cu netcat:
   ```bash
   # Terminal 1: Pornește serverul
   nc -l -p 9090
   ```

2. Conectați-vă de la un alt terminal:
   ```bash
   # Terminal 2: Conectează clientul
   nc localhost 9090
   ```

3. Trimiteți mesaje în ambele direcții și observați.

4. Într-un al treilea terminal, vizualizați starea conexiunii:
   ```bash
   # Terminal 3: Verifică socket-urile
   ss -tnp | grep 9090
   ```

5. Rulați exercițiul Python server-client:
   ```bash
   cd /work/src/exercises
   python3 ex_1_02_tcp_server_client.py
   ```

**Ce să observați:**

- Procesul de handshake în trei pași (SYN, SYN-ACK, ACK) în Wireshark
- Stările socket-urilor: LISTEN, ESTABLISHED, TIME_WAIT
- Transferul bidirecțional de date

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 3
```

---

### Exercițiul 4: Captura de Trafic

**Obiectiv:** Capturați și salvați traficul de rețea pentru analiză.

**Durată:** 25 minute

**Pași:**

1. Porniți captura de trafic:
   ```bash
   # În containerul lab
   tcpdump -i lo -w /work/pcap/captura_tcp.pcap port 9090 &
   ```

2. Generați trafic TCP (ca în exercițiul 3).

3. Opriți captura:
   ```bash
   pkill tcpdump
   ```

4. Analizați captura:
   ```bash
   # Afișare rezumat
   tshark -r /work/pcap/captura_tcp.pcap
   
   # Numărare pachete
   tshark -r /work/pcap/captura_tcp.pcap | wc -l
   
   # Afișare flag-uri TCP
   tshark -r /work/pcap/captura_tcp.pcap -Y tcp -T fields -e tcp.flags.str
   ```

5. Opțional - Deschideți fișierul PCAP în Wireshark pe Windows:
   ```powershell
   # În PowerShell
   & "C:\Program Files\Wireshark\Wireshark.exe" "D:\RETELE\SAPT1\01roWSL\pcap\captura_tcp.pcap"
   ```

**Ce să observați:**

- Structura pachetelor TCP
- Secvența handshake-ului
- Numerele de secvență și acknowledgement

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 4
```

---

### Exercițiul 5: Analiza Fișierelor PCAP

**Obiectiv:** Extrageți și procesați date statistice din capturi de trafic.

**Durată:** 25 minute

**Pași:**

1. Exportați datele capturii în format CSV:
   ```bash
   tshark -r /work/pcap/captura_tcp.pcap \
       -T fields \
       -e frame.number \
       -e frame.time_relative \
       -e ip.src \
       -e ip.dst \
       -e tcp.srcport \
       -e tcp.dstport \
       -e frame.len \
       -E header=y \
       -E separator=, > /work/pcap/captura.csv
   ```

2. Procesați CSV-ul cu Python:
   ```bash
   cd /work/src/exercises
   python3 ex_1_03_parsare_csv.py
   python3 ex_1_04_statistici_pcap.py
   ```

3. Calculați statistici:
   - Număr total de pachete
   - Dimensiunea medie a pachetelor
   - Durata conversației
   - Distribuția pe porturi

**Ce să observați:**

- Structura datelor exportate
- Modele de trafic
- Corelația între dimensiunea pachetelor și protocol

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 5
```

## Demonstrații

### Demo 1: Diagnostic de Rețea

Demonstrație automatizată a comenzilor de diagnostic:

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT1/01roWSL
python3 scripts/ruleaza_demo.py --demo 1
```

**Ce să observați:**

- Progresie logică: interfețe → rute → socket-uri → conectivitate
- Formatarea și interpretarea ieșirilor
- Depanarea sistematică a problemelor de rețea

### Demo 2: Comparație TCP vs UDP

Demonstrație paralelă a protocoalelor TCP și UDP:

```bash
python3 scripts/ruleaza_demo.py --demo 2
```

**Ce să observați:**

- Overhead-ul handshake-ului TCP
- Diferențele în numărul de pachete
- Comportamentul la pierdere de pachete

### Demo 3: Socket-uri Python

Execuție live a exercițiilor cu socket-uri:

```bash
python3 scripts/ruleaza_demo.py --demo 3
```

**Ce să observați:**

- Procesul de bind/listen/accept (server)
- Procesul de connect/send/recv (client)
- Tratarea erorilor și timeout-urile

## Captura și Analiza Pachetelor

### Capturarea Traficului

```bash
# Pornirea capturii din container
python3 scripts/captura_trafic.py --interfata lo --output pcap/captura_saptamana1.pcap

# Sau folosiți Wireshark direct pe Windows
# Selectați interfața vEthernet (WSL)
```

### Filtre Wireshark Sugerate

```
# Trafic TCP pe portul specific
tcp.port == 9090

# Doar pachete SYN (începutul conexiunii)
tcp.flags.syn == 1 and tcp.flags.ack == 0

# Handshake complet
tcp.flags.syn == 1 or (tcp.flags.syn == 1 and tcp.flags.ack == 1)

# Trafic UDP
udp

# Pachete ICMP (ping)
icmp

# Trafic de la/către o adresă IP specifică
ip.addr == 172.20.1.2
```

## Oprire și Curățare

### Sfârșit de Sesiune

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT1/01roWSL

# Opriți toate containerele de laborator (Portainer rămâne activ!)
python3 scripts/opreste_lab.py

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

Consultați directorul `homework/` pentru exercițiile de făcut acasă.

### Tema 1: Raport de Configurare a Rețelei

Documentați configurația completă a rețelei pe calculatorul personal.

### Tema 2: Analiza Protocoalelor TCP/UDP

Capturați și comparați traficul TCP și UDP, identificând diferențele.

## Depanare

### Probleme Frecvente

#### Problemă: Docker nu pornește

**Soluție:** În WSL2, porniți serviciul Docker manual:
```bash
sudo service docker start
# Parolă: stud
```

#### Problemă: Permisiuni insuficiente pentru captură

**Soluție:** Rulați comanda cu sudo în container sau verificați capabilitățile NET_ADMIN.

#### Problemă: Portul este deja utilizat

**Soluție:** Identificați procesul cu `ss -tlnp | grep PORT` și opriți-l sau folosiți alt port.

Consultați `docs/depanare.md` pentru mai multe soluții.

## Fundament Teoretic

Această săptămână acoperă fundamentele rețelelor, inclusiv:

- **Modelul TCP/IP**: Arhitectura pe patru straturi și funcțiile fiecărui strat
- **Adresarea IP**: Structura adreselor IPv4, notația CIDR și subrețele
- **Protocoale de transport**: TCP (orientat pe conexiune) vs UDP (fără conexiune)
- **Socket-uri**: Endpoints pentru comunicarea în rețea
- **Instrumente de diagnostic**: ip, ss, ping, netcat, tcpdump, tshark

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Tanenbaum, A. S. & Wetherall, D. J. (2011). *Computer Networks* (5th ed.). Pearson.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.

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
- Exemple corecte: `tcp.port == 9090`, `ip.addr == 172.20.1.2`

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week1_network

# Verifică DNS în container
docker exec week1_lab cat /etc/resolv.conf

# Testează conectivitatea
docker exec week1_lab ping -c 2 8.8.8.8
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
docker logs week1_lab

# Verifică dacă imaginea există
docker images | grep week1

# Reconstruiește imaginea
cd /mnt/d/RETELE/SAPT1/01roWSL
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
cd /mnt/d/RETELE/SAPT1/01roWSL
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT1/01roWSL

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

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
