# Săptămâna 1: Fundamentele Rețelelor de Calculatoare

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | Laborator
>
> by Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl

---

## Verificare Mediu

Înainte de a începe acest laborator, verificați că mediul este configurat corect.

### Din Windows PowerShell:

```powershell
# Verificați starea WSL - Ubuntu-22.04 ar trebui să fie implicit
wsl --status
# Așteptat: Default Distribution: Ubuntu-22.04

# Verificați accesul la Docker prin WSL
wsl docker ps
# Așteptat: Cel puțin containerul "portainer" rulând

# Verificați accesibilitatea Portainer
curl http://localhost:9000
# Așteptat: Răspuns HTML (interfața Portainer)
```

### Din Terminalul Ubuntu (WSL):

```bash
# Porniți serviciul Docker dacă nu rulează
sudo service docker start

# Verificați că Portainer rulează
docker ps --filter name=portainer
# Așteptat: container portainer cu status "Up"

# Verificați versiunea Docker
docker --version
# Așteptat: Docker version 28.x sau mai recent
```

### Puncte de Acces

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| **Portainer** | http://localhost:9000 | `stud` / `studstudstud` |
| Container Lab | Shell prin Docker | N/A |
| Server Test TCP | localhost:9090 | N/A |
| Server Test UDP | localhost:9091 | N/A |

> **Notă:** Portainer rulează ca serviciu global (nu per-laborator). Este mereu disponibil pe portul 9000.

---

## Prezentare Generală

Această sesiune de laborator introduce conceptele fundamentale ale rețelelor de calculatoare, concentrându-se pe instrumentele de diagnostic și tehnicile de analiză esențiale pentru înțelegerea comunicării în rețea. Studenții vor dobândi experiență practică cu utilitare de rețea la nivel de linie de comandă, captură de pachete și paradigme de programare a socket-urilor.

Laboratorul acoperă stiva TCP/IP de la o perspectivă practică, demonstrând modul în care datele traversează straturile rețelei și cum pot fi observate, capturate și analizate diferitele protocoale. Această cunoaștere fundamentală formează baza pentru toate sesiunile de laborator ulterioare.

---

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** interfețele de rețea, adresele IP și tabelele de rutare folosind utilitare Linux
2. **Explicați** diferențele dintre protocoalele TCP și UDP în ceea ce privește stabilirea conexiunii și fiabilitatea
3. **Demonstrați** conectivitatea de bază a rețelei folosind ping, netcat și socket-uri Python
4. **Analizați** traficul de rețea capturat folosind tcpdump, tshark și Wireshark
5. **Construiți** aplicații simple client-server folosind socket-uri TCP în Python
6. **Evaluați** modelele de trafic de rețea prin analiza fișierelor PCAP

---

## Cerințe Preliminare

### Cunoștințe Necesare

- Operarea de bază în linia de comandă Linux
- Cunoștințe elementare de programare Python
- Înțelegerea numerotării binare și hexazecimale
- Familiaritate cu modelul stratificat TCP/IP

### Cerințe Software (Pre-instalate)

Mediul dvs. ar trebui să aibă deja:

- ✅ Windows 10/11 cu WSL2 activat
- ✅ Ubuntu 22.04 LTS (distribuția WSL implicită)
- ✅ Docker Engine în WSL (NU Docker Desktop)
- ✅ Portainer CE rulând pe portul 9000
- ✅ Wireshark (aplicație Windows nativă)
- ✅ Python 3.11+ cu pachetele: docker, scapy, dpkt

Dacă lipsește ceva, consultați [Documentația Cerințelor Preliminare](../PREREQUISITES_RO.md).

### Credențiale Standard

| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

---

## Pornire Rapidă

### Pasul 1: Deschideți Terminalul Ubuntu

Din Windows, fie:
- Click pe "Ubuntu" în meniul Start, sau
- În PowerShell, tastați: `wsl`

### Pasul 2: Navigați la Directorul Laboratorului

```bash
# Dacă ați clonat în D:/RETELE/
cd /mnt/d/RETELE/SAPT1
```

### Pasul 3: Verificați Cerințele Preliminare

```bash
python setup/verifica_mediu.py
```

Toate verificările ar trebui să treacă. Dacă vreuna eșuează, rezolvați înainte de a continua.

### Pasul 4: Porniți Laboratorul

```bash
# Asigurați-vă că Docker rulează
sudo service docker start

# Porniți containerele de laborator
python scripts/porneste_lab.py
```

### Pasul 5: Verificați că Totul Rulează

```bash
# Verificați containerele de laborator
docker ps

# Output așteptat - ar trebui să vedeți:
# - week1_lab (containerul de laborator)
# - portainer (interfața de management global)
```

---

## Arhitectura Laboratorului

```
┌─────────────────────────────────────────────────────────────────┐
│                         WINDOWS 11                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Wireshark     │  │    Browser      │  │   PowerShell    │  │
│  │   (Captură)     │  │  (Portainer)    │  │   (Comenzi)     │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
│           │              localhost:9000             │           │
│           ▼                    ▼                    ▼           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              vEthernet (WSL) - Rețea Virtuală               ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌───────────────────────────┴───────────────────────────────┐  │
│  │                        WSL2                                │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                  Ubuntu 22.04 LTS                    │  │  │
│  │  │  ┌─────────────────────────────────────────────┐    │  │  │
│  │  │  │              Docker Engine                   │    │  │  │
│  │  │  │                                              │    │  │  │
│  │  │  │  ┌──────────────┐    ┌──────────────┐      │    │  │  │
│  │  │  │  │  week1_lab   │    │  portainer   │      │    │  │  │
│  │  │  │  │  Container   │    │  (global)    │      │    │  │  │
│  │  │  │  │              │    │  :9000       │      │    │  │  │
│  │  │  │  │ Porturi:     │    └──────────────┘      │    │  │  │
│  │  │  │  │ 9090 (TCP)   │                          │    │  │  │
│  │  │  │  │ 9091 (UDP)   │                          │    │  │  │
│  │  │  │  │ 9092 (alt)   │                          │    │  │  │
│  │  │  │  └──────────────┘                          │    │  │  │
│  │  │  │                                              │    │  │  │
│  │  │  │         Rețele Docker                       │    │  │  │
│  │  │  │   week1_network (172.20.1.0/24)            │    │  │  │
│  │  │  └─────────────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

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
python tests/test_exercitii.py --exercitiu 1
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
   python ex_1_01_latenta_ping.py
   ```

**Ce să observați:**
- Timpii de răspuns (RTT - Round Trip Time)
- Variația în latență
- Pierderi de pachete (dacă există)

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 2
```

---

### Exercițiul 3: Comunicarea TCP

**Obiectiv:** Stabiliți o conexiune TCP și observați stările socket-urilor.

**Durată:** 25 minute

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
   python ex_1_02_tcp_server_client.py
   ```

**Ce să observați:**
- Procesul de handshake în trei pași (SYN, SYN-ACK, ACK)
- Stările socket-urilor: LISTEN, ESTABLISHED, TIME_WAIT
- Transferul bidirecțional de date

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 3
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

5. Opțional - Deschideți fișierul PCAP în Wireshark pe Windows.

**Analiză Wireshark (Windows):**

Deschideți Wireshark, porniți captura pe interfața `vEthernet (WSL)`, apoi generați trafic ca mai sus. Folosiți filtrul: `tcp.port == 9090`

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 4
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
   python ex_1_03_parsare_csv.py
   python ex_1_04_statistici_pcap.py
   ```

3. Calculați statistici:
   - Număr total de pachete
   - Dimensiunea medie a pachetelor
   - Durata conversației
   - Distribuția pe porturi

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 5
```

---

## Demonstrații

### Demo 1: Diagnostic de Rețea

Demonstrație automatizată a comenzilor de diagnostic:

```bash
python scripts/ruleaza_demo.py --demo 1
```

**Ce să observați:**
- Progresie logică: interfețe → rute → socket-uri → conectivitate
- Formatarea și interpretarea ieșirilor
- Depanarea sistematică a problemelor de rețea

### Demo 2: Comparație TCP vs UDP

Demonstrație paralelă a protocoalelor TCP și UDP:

```bash
python scripts/ruleaza_demo.py --demo 2
```

**Ce să observați:**
- Overhead-ul handshake-ului TCP
- Diferențele în numărul de pachete
- Comportamentul la pierdere de pachete

---

## Captura și Analiza Pachetelor

### Captură în Container

```bash
# Pornirea capturii
python scripts/captura_trafic.py --interfata lo --output pcap/captura_saptamana1.pcap

# Sau folosiți tcpdump direct
docker exec week1_lab tcpdump -i any -w /work/pcap/capture.pcap
```

### Captură cu Wireshark (Windows)

1. Deschideți Wireshark din meniul Start
2. Selectați interfața: **vEthernet (WSL)** sau **vEthernet (WSL) (Hyper-V firewall)**
3. Porniți captura
4. Generați trafic în containerul de laborator
5. Opriți captura și analizați

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

---

## Curățare

După finalizarea laboratorului, curățați resursele:

```bash
# Opriți containerele de laborator (Portainer rămâne activ!)
docker-compose -f docker/docker-compose.yml down

# Eliminați rețelele de laborator (dacă au fost create)
docker network prune -f

# Eliminați imaginile de laborator (opțional, economisește spațiu)
docker image prune -f
```

**⚠️ Important:** Păstrați mereu Portainer rulând pentru alte laboratoare!

```bash
# NU faceți NICIODATĂ asta (decât dacă vreți să opriți Portainer):
# docker stop portainer

# Verificați că Portainer încă rulează:
docker ps --filter name=portainer
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```bash
# Eliminați toate containerele, rețelele pentru această săptămână
python scripts/curatare.py --complet

# Verificați curățarea
docker system df
```

---

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de făcut acasă.

### Tema 1: Raport de Configurare a Rețelei

Documentați configurația completă a rețelei pe calculatorul personal.

### Tema 2: Analiza Protocoalelor TCP/UDP

Capturați și comparați traficul TCP și UDP, identificând diferențele.

---

## Depanare

### Probleme Frecvente

#### Problemă: Serviciul Docker nu rulează în WSL
**Soluție:**
```bash
sudo service docker start
docker ps  # Verificați că funcționează
```

#### Problemă: "Cannot connect to Docker daemon"
**Soluție:** Serviciul Docker nu rulează. Porniți-l:
```bash
sudo service docker start
```

#### Problemă: Permisiuni refuzate la rularea docker
**Soluție:** Utilizatorul nu este în grupul docker:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

#### Problemă: Portainer nu este accesibil la localhost:9000
**Soluție:** Containerul Portainer ar putea fi oprit:
```bash
docker start portainer
# Sau reinstalați dacă nu există:
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

#### Problemă: Containerul de laborator nu pornește
**Soluție:** Verificați conflicte de porturi:
```bash
docker ps -a
netstat -tlnp | grep -E "9090|9091|9092"
```

#### Problemă: Portul este deja utilizat
**Soluție:** Identificați procesul cu `ss -tlnp | grep PORT` și opriți-l sau folosiți alt port.

#### Problemă: Nu se capturează pachete în Wireshark
**Soluție:**
- Asigurați-vă că capturați pe interfața `vEthernet (WSL)`
- Generați trafic în timp ce capturați
- Verificați că filtrul de afișare nu e prea restrictiv

Consultați `docs/depanare.md` pentru mai multe soluții.

---

## Fundament Teoretic

### Modelul TCP/IP

Rețelele moderne operează conform unei arhitecturi pe straturi, unde fiecare strat oferă servicii stratului de deasupra. Acest laborator se concentrează pe Stratul de Transport (TCP/UDP) și Stratul de Rețea (IP).

### Handshake-ul în Trei Pași

Stabilirea conexiunii TCP urmează o secvență precisă:
1. **SYN** - Clientul inițiază cererea de conexiune
2. **SYN-ACK** - Serverul confirmă și răspunde
3. **ACK** - Clientul confirmă, conexiunea este stabilită

### Stările Socket-urilor

Socket-urile de rețea tranziționează prin stări definite:
- **LISTEN** - Serverul așteaptă conexiuni
- **ESTABLISHED** - Comunicare bidirecțională activă
- **TIME_WAIT** - Conexiune închisă, așteaptă timeout
- **CLOSE_WAIT** - Partea remote a inițiat închiderea

---

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Tanenbaum, A. S. & Wetherall, D. J. (2011). *Computer Networks* (5th ed.). Pearson.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*

*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
