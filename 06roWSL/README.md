# Săptămâna 6: NAT/PAT, Protocoale de Suport pentru Rețele și Rețele Definite prin Software

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | Laborator Rețele de Calculatoare
> 
> de Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `06roWSL`

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

# Clonează Săptămâna 6
git clone https://github.com/antonioclim/netROwsl.git SAPT6
cd SAPT6
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 06roWSL/
cd 06roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT6\
    └── 06roWSL\
        ├── artifacts/       # Rezultate generate (capturi, loguri)
        ├── docker/          # Configurație Docker și Dockerfile
        │   ├── configs/     # Configurații suplimentare
        │   └── volumes/     # Volume persistente
        ├── docs/            # Documentație suplimentară
        │   ├── commands_cheatsheet.md  # Fișă comenzi
        │   ├── further_reading.md      # Lectură suplimentară
        │   ├── theory_summary.md       # Rezumat teorie
        │   └── troubleshooting.md      # Depanare
        ├── homework/        # Teme pentru acasă
        ├── pcap/            # Fișiere de captură
        ├── scripts/         # Scripturi de automatizare
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă exerciții
        │   ├── apps/        # Aplicații (NAT observer, SDN controller, echo)
        │   ├── exercises/   # Topologii (NAT, SDN)
        │   └── utils/       # Utilitare de rețea
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
cd /mnt/d/RETELE/SAPT6/06roWSL

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
- **Nume** - Identificatorul containerului (week6_lab, week6_controller)
- **Stare** - Running/Stopped/Paused
- **Imagine** - Imaginea Docker folosită
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

### Vizualizarea Rețelelor

1. Navighează: **Networks**
2. Observă rețelele disponibile:
   - **week6_network** - Rețea bridge pentru laborator
   - **bridge**, **host**, **none** - Rețele Docker implicite

### Modificarea Configurației (pentru NAT/SDN)

Pentru laboratorul Săptămânii 6, configurațiile de rețea sunt gestionate prin:
- **Mininet** - Pentru topologii NAT și SDN (în interiorul containerului)
- **Docker networks** - Pentru izolarea containerelor

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a examina traducerea NAT și fluxurile SDN
- Pentru a observa instalarea regulilor OpenFlow

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
cd /mnt/d/RETELE/SAPT6/06roWSL

# Rulează demonstrația NAT
python3 scripts/run_demo.py --demo nat

# Sau demonstrația SDN
python3 scripts/run_demo.py --demo sdn
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 6

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

**Filtre pentru NAT/PAT:**

| Filtru | Scop | Exemplu Utilizare |
|--------|------|-------------------|
| `ip.addr == 192.168.1.0/24` | Rețea privată NAT | Trafic hosturi interne |
| `ip.addr == 203.0.113.0/24` | Rețea publică TEST-NET-3 | Trafic tradus |
| `tcp.port == 5000` | Observer NAT | Aplicație demonstrație |
| `tcp.flags.syn == 1` | Conexiuni noi | Observă NAT la inițiere |
| `ip.src == 192.168.1.10 && ip.dst == 203.0.113.2` | Trafic h1→h3 | Înainte de traducere |
| `ip.src == 203.0.113.1` | Trafic tradus | După MASQUERADE |

**Filtre pentru SDN/OpenFlow:**

| Filtru | Scop | Exemplu Utilizare |
|--------|------|-------------------|
| `ip.addr == 10.0.6.0/24` | Rețea SDN | Tot traficul topologiei |
| `ip.addr == 10.0.6.11` | Host h1 | Trafic h1 (acces complet) |
| `ip.addr == 10.0.6.12` | Host h2 | Trafic h2 (server) |
| `ip.addr == 10.0.6.13` | Host h3 | Trafic h3 (restricționat) |
| `tcp.port == 6633` | OpenFlow legacy | Comunicare controller-switch |
| `tcp.port == 6653` | OpenFlow standard | Comunicare controller-switch |
| `tcp.port == 9090` | TCP Echo | Testare conectivitate |
| `udp.port == 9091` | UDP Echo | Testare politici protocol |
| `openflow_v4` | Mesaje OpenFlow 1.3 | Instalare fluxuri |
| `icmp` | Ping | Teste conectivitate SDN |

**Combinarea filtrelor:**
- ȘI: `ip.addr == 10.0.6.11 && tcp.port == 9090`
- SAU: `tcp.port == 6633 || tcp.port == 6653`
- NU: `!arp && !dns`

### Analiza Traducerii NAT în Wireshark

1. Capturează trafic cu filtrul pentru ambele rețele
2. Observă pachetul original de la 192.168.1.x
3. Găsește pachetul tradus cu IP sursă 203.0.113.1
4. Compară:
   - **Înainte NAT:** Source: 192.168.1.10:port_efemer → Dest: 203.0.113.2:5000
   - **După NAT:** Source: 203.0.113.1:port_tradus → Dest: 203.0.113.2:5000

### Analiza Fluxurilor SDN în Wireshark

1. Activează filtrul `openflow_v4` pentru a vedea mesaje OpenFlow
2. Observă mesajele:
   - **PACKET_IN** - Switch trimite pachet la controller
   - **FLOW_MOD** - Controller instalează regulă de flux
   - **PACKET_OUT** - Controller trimite pachet înapoi
3. Corelează cu regulile din `ovs-ofctl dump-flows s1`

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

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT6\06roWSL\pcap\`
3. Nume fișier sugestiv: `nat_translation.pcap` sau `sdn_flows.pcap`
4. Format: Wireshark/pcap sau pcapng (implicit)

### Exportarea Datelor pentru Analiză

1. **File → Export Packet Dissections → As CSV**
2. Selectează câmpurile de exportat
3. Salvează în folderul `artifacts/` pentru procesare Python

---

## Prezentare generală

Această sesiune de laborator integrează două domenii complementare ale arhitecturii moderne de rețea: mecanismele de traducere a adreselor care susțin ciclul de viață extins al IPv4, și schimbarea de paradigmă către rețelele definite prin software (SDN) care decuplează logica de control de hardware-ul de redirecționare.

Prima componentă examinează Network Address Translation (NAT) și varianta sa cu multiplexare de porturi (PAT/NAPT), protocoale care au devenit o infrastructură indispensabilă pentru maparea adreselor private la cele publice. Studenții vor configura reguli MASQUERADE bazate pe iptables pe un router Linux, vor observa procesul bidirecțional de traducere și vor analiza modul în care alocarea de porturi efemere permite mai multor hosturi interne să partajeze o singură adresă publică.

A doua componentă introduce arhitectura SDN prin OpenFlow 1.3, demonstrând separarea fundamentală dintre planul de control (luarea deciziilor centralizate) și planul de date (redirecționarea distribuită a pachetelor). Utilizând OS-Ken ca framework de controller și Open vSwitch ca switch programabil, studenții vor implementa și observa politici bazate pe fluxuri care permit sau blochează selectiv traficul pe baza criteriilor de sursă, destinație și protocol.

## Obiective de învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Reamintească** scopul și clasificarea variantelor NAT (static, dinamic, PAT) și rolul protocoalelor auxiliare (ARP, DHCP, ICMP, NDP)
2. **Explice** cum tabelele de traducere PAT mențin starea bidirecțională a sesiunii și de ce acest mecanism creează provocări pentru conexiunile de intrare
3. **Implementeze** reguli NAT/MASQUERADE folosind iptables pe un router Linux multi-homed într-o topologie simulată
4. **Demonstreze** instalarea fluxurilor SDN prin observarea comunicării controller-switch și inspectarea tabelelor de fluxuri cu ovs-ofctl
5. **Analizeze** diferențele comportamentale dintre traficul permis și cel blocat într-o topologie SDN, corelând rezultatele pachetelor cu regulile de flux instalate
6. **Compare** rutarea distribuită tradițională cu controlul SDN centralizat, articulând compromisurile în scalabilitate, flexibilitate și domenii de defecțiune
7. **Proiecteze** politici OpenFlow personalizate care implementează controlul accesului per-host, per-protocol într-o rețea definită prin software

## Cerințe preliminare

### Cerințe de cunoștințe

- Înțelegerea adresării IPv4, subnetting-ului și notației CIDR (Săptămânile 4-5)
- Familiarizare cu conceptele de programare socket TCP/UDP (Săptămânile 2-3)
- Competențe de bază în linia de comandă Linux (navigare fișiere, gestionare procese)
- Înțelegerea conceptuală a modelelor OSI și TCP/IP

### Cerințe software

- Windows 10/11 cu WSL2 activat (Ubuntu 22.04 sau ulterior)
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație nativă Windows)
- Python 3.11 sau ulterior
- Git (opțional, pentru controlul versiunilor)

### Cerințe hardware

- Minim 8GB RAM (16GB recomandat pentru execuție paralelă de containere)
- 10GB spațiu liber pe disc
- Conectivitate de rețea (pentru instalarea inițială a pachetelor)

## Pornire rapidă

### Configurare inițială (Se rulează o singură dată)

```bash
# Deschide terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT6/06roWSL

# Verifică dacă cerințele preliminare sunt instalate
python3 setup/verify_environment.py

# Dacă vreo verificare eșuează, rulează helper-ul de instalare
python3 setup/install_prerequisites.py
```

### Pornirea laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT6/06roWSL

# Pornește toate serviciile (containere Docker, configurare rețea)
python3 scripts/start_lab.py

# Verifică dacă serviciile rulează
python3 scripts/start_lab.py --status

# Pentru reconstruirea containerelor după modificări
python3 scripts/start_lab.py --rebuild
```

### Accesarea serviciilor

| Serviciu | URL/Port | Scop |
|----------|----------|------|
| Portainer | http://localhost:9000 | Panou de administrare containere |
| Controller SDN | localhost:6633 | Endpoint controller OpenFlow |
| Router NAT (rnat) | 203.0.113.1 | Gateway NAT cu interfață publică |
| Observator NAT | Port 5000 | Demonstrație traducere PAT |
| Echo TCP | Port 9090 | Testare conectivitate SDN |
| Echo UDP | Port 9091 | Testare politici specifice protocolului |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Topologia rețelei

### Planul de adrese IP Săptămâna 6

| Resursă | Adresă | Scop |
|---------|--------|------|
| Subrețea SDN | 10.0.6.0/24 | Rețea internă topologie SDN |
| h1 | 10.0.6.11 | Host SDN (acces complet la h2) |
| h2 | 10.0.6.12 | Host SDN (server) |
| h3 | 10.0.6.13 | Host SDN (acces restricționat) |
| Subrețea privată | 192.168.1.0/24 | Rețea internă topologie NAT |
| NAT privat | 192.168.1.1 | Interfața routerului (partea privată) |
| NAT public | 203.0.113.1 | Interfața routerului (partea publică, TEST-NET-3) |
| h3 (NAT) | 203.0.113.2 | Server public în topologia NAT |

### Planul de porturi

| Port | Protocol | Utilizare |
|------|----------|-----------|
| 9090 | TCP | Aplicație server/client echo |
| 9091 | UDP | Aplicație server/client echo |
| 6633 | TCP | Controller OpenFlow (legacy) |
| 6653 | TCP | Controller OpenFlow (standard) |
| 5000 | TCP | Aplicație observator NAT |
| 5600-5699 | - | Interval porturi personalizate Săptămâna 6 |

## Exerciții de laborator

### Exercițiul 1: Configurarea și observarea NAT/PAT

**Obiectiv:** Configurarea NAT MASQUERADE pe un router Linux și observarea traducerii adreselor de port în acțiune.

**Durată:** 40 minute

**Context:** Când hosturile private (adrese RFC 1918) comunică cu serverele publice, NAT rescrie adresele sursă la adresa IP publică a routerului. PAT extinde acest lucru traducând și porturile sursă, permițând mai multor hosturi interne să partajeze o singură adresă publică.

**Pregătire Wireshark:** Deschide Wireshark pe Windows și pornește captura pe interfața `vEthernet (WSL)` ÎNAINTE de a începe exercițiul.

**Pași:**

1. Pornește topologia NAT:
   ```bash
   python3 scripts/run_demo.py --demo nat
   ```

2. În CLI-ul Mininet, verifică configurația interfețelor:
   ```bash
   rnat ifconfig
   rnat iptables -t nat -L -n -v
   ```

3. Pornește observatorul NAT pe serverul public (h3):
   ```bash
   h3 python3 src/apps/nat_observer.py server --bind 203.0.113.2 --port 5000
   ```

4. De pe hosturile private, inițiază conexiuni:
   ```bash
   h1 python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Salut de la h1"
   h2 python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Salut de la h2"
   ```

5. Observă output-ul serverului - notează că ambele conexiuni par să provină de la 203.0.113.1 (IP-ul public NAT) cu porturi sursă diferite.

6. Verifică traducerile NAT:
   ```bash
   rnat conntrack -L 2>/dev/null || rnat cat /proc/net/nf_conntrack
   ```

**Observații așteptate:**
- Adresele private (192.168.1.x) nu sunt niciodată vizibile pe partea publică
- Fiecare conexiune de la hosturi interne diferite folosește un port tradus unic
- Tabela NAT menține starea bidirecțională pentru traficul de retur

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 1
```

### Exercițiul 2: Topologie SDN și observarea fluxurilor

**Obiectiv:** Implementarea unei topologii SDN cu un controller OpenFlow și observarea redirecționării pachetelor bazate pe fluxuri.

**Durată:** 35 minute

**Context:** SDN separă planul de control (unde se iau deciziile de redirecționare) de planul de date (unde pachetele sunt efectiv redirecționate). Controller-ul instalează reguli de flux în switch-uri care definesc perechi match-action.

**Pași:**

1. Pornește topologia SDN cu reguli de flux:
   ```bash
   python3 scripts/run_demo.py --demo sdn
   ```

2. În CLI-ul Mininet, verifică conectivitatea:
   ```bash
   # Ar trebui să funcționeze (h1 ↔ h2 PERMITE)
   h1 ping -c 3 h2
   
   # Ar trebui să eșueze (h1 → h3 BLOCHEAZĂ)
   h1 ping -c 3 h3
   
   # Ar trebui să funcționeze (h2 → h3 PERMITE)
   h2 ping -c 3 h3
   ```

3. Inspectează tabelele de fluxuri instalate:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1
   ```

4. Pornește serverele de testare pe h2 și h3:
   ```bash
   h2 python3 src/apps/tcp_echo.py server &
   h3 python3 src/apps/tcp_echo.py server &
   ```

5. Testează politicile la nivel de protocol:
   ```bash
   # TCP de la h1 la h2 (ar trebui să funcționeze)
   h1 python3 src/apps/tcp_echo.py client --host 10.0.6.12
   
   # TCP de la h1 la h3 (ar trebui să eșueze)
   h1 python3 src/apps/tcp_echo.py client --host 10.0.6.13
   ```

**Observații așteptate:**
- Tabelele de fluxuri conțin reguli match-action
- Traficul permis primește răspunsuri
- Traficul blocat timeout-ează sau este rejectat
- Numărul de potriviri în fluxuri crește cu traficul

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 2
```

### Exercițiul 3: Modificarea politicilor SDN

**Obiectiv:** Modificarea politicilor controller-ului pentru a schimba comportamentul de acces la nivel de protocol.

**Durată:** 30 minute

**Pași:**

1. Examinează codul controller-ului:
   ```bash
   # Deschide controller-ul de politici în editorul tău
   code src/apps/sdn_policy_controller.py
   ```

2. Localizează secțiunea de definire a politicilor și modifică pentru a permite UDP pe portul 9091 la h3

3. Repornește controller-ul și testează noua politică:
   ```bash
   # În Mininet
   h3 python3 src/apps/udp_echo.py server &
   h1 python3 src/apps/udp_echo.py client --host 10.0.6.13
   ```

4. Verifică noile reguli de flux:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1 | grep udp
   ```

**Criterii de succes:**
- Traficul UDP la h3 funcționează conform noii politici
- Regulile de flux reflectă filtrul specific protocolului
- Alte politici rămân neafectate

## Oprirea laboratorului

### Oprire standard

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT6/06roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/stop_lab.py

# Verifică - ar trebui să vezi doar portainer
docker ps
```

### Curățare completă (resetare totală)

```bash
python3 scripts/cleanup.py --full --prune
```

## Teme pentru acasă

Consultă directorul `homework/` pentru exercițiile de lucru individual.

### Tema 1: Analiză extinsă NAT

Documentează procesul de traducere NAT pentru următorul scenariu:
- Trei hosturi interne conectându-se simultan la același server extern
- Fiecare host face două conexiuni (HTTP și HTTPS)
- Capturează și analizează starea tabelei NAT

**Livrabil:** `homework/exercises/hw_6_01_analiza_nat.md`

### Tema 2: Implementare politici SDN personalizate

Proiectează și implementează o politică SDN care:
- Permite HTTP (port 80) și HTTPS (port 443) de la toate hosturile la h3
- Blochează tot ICMP către h3 cu excepția celui de la h2
- Permite SSH (port 22) doar de la h1 la h2

**Livrabil:** `homework/exercises/hw_6_02_politica_sdn.py`

## Depanare

### Probleme frecvente

#### Problemă: Erori la curățarea Mininet ("File exists")
**Soluție:** Rulează curățarea cu flag-ul force:
```bash
python3 scripts/cleanup.py --force
# Sau manual în WSL:
sudo mn -c
```

#### Problemă: Switch-ul OVS nu se conectează la controller
**Soluție:** Verifică dacă controller-ul rulează și portul este accesibil:
```bash
ss -ltn | grep 6633
ovs-vsctl show
```

#### Problemă: Containerele Docker nu pornesc în modul privilegiat
**Soluție:** Asigură-te că Docker este configurat corect în WSL2:
```bash
sudo service docker start
docker info | grep "Security Options"
```

#### Problemă: NAT nu traduce pachetele
**Soluție:** Verifică dacă IP forwarding-ul este activat:
```bash
sysctl net.ipv4.ip_forward
# Ar trebui să fie 1; dacă nu:
sudo sysctl -w net.ipv4.ip_forward=1
```

#### Problemă: Ping-urile în topologia SDN sunt lente sau expiră
**Soluție:** Verifică dacă regulile de flux sunt instalate:
```bash
ovs-ofctl -O OpenFlow13 dump-flows s1
```
Dacă este gol sau există doar regula table-miss, controller-ul poate să nu funcționeze corect.

Consultă `docs/troubleshooting.md` pentru soluții suplimentare.

## Fundamente teoretice

### NAT și PAT

Network Address Translation a apărut ca răspuns la epuizarea adreselor IPv4, permițând organizațiilor să utilizeze intervale de adrese private (RFC 1918: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) intern, în timp ce partajează adrese publice limitate extern. Port Address Translation extinde acest lucru prin multiplexarea conexiunilor prin numere de port, permițând mii de hosturi interne să partajeze un singur IP public.

Procesul de traducere implică:
1. **Ieșire:** Rescrierea IP-ului sursă (și portului în PAT) la adresa publică a dispozitivului NAT
2. **Urmărirea stării:** Menținerea unei tabele de traducere care mapează tuplurile interne la cele externe
3. **Intrare:** Traducerea inversă folosind starea stocată

### Rețele definite prin software

SDN reprezintă o schimbare arhitecturală fundamentală de la controlul distribuit la controlul centralizat al rețelei. Principiile cheie includ:
1. **Separarea responsabilităților:** Logica de control (controller) distinctă de redirecționare (switch-uri)
2. **Programabilitate:** Comportamentul rețelei definit prin API-uri software
3. **Viziune centralizată:** Controller-ul menține starea globală a rețelei
4. **Redirecționare bazată pe fluxuri:** Pachetele sunt potrivite cu reguli și se aplică acțiuni

OpenFlow oferă interfața southbound între controller și switch-uri, definind modul în care tabelele de fluxuri sunt populate și interogate.

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ediția a 7-a). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 1918 – Alocarea adreselor pentru rețele private
- RFC 5737 – Blocuri de adrese IPv4 rezervate pentru documentație
- RFC 4861 – Neighbor Discovery pentru IP versiunea 6 (IPv6)
- Open Networking Foundation (2015). *OpenFlow Switch Specification* Versiunea 1.3.5

## Diagrame de arhitectură

### Topologia NAT
```
    ┌─────────────────────────────────────────────────────────────┐
    │                    Rețea privată                            │
    │                    192.168.1.0/24                           │
    │                                                             │
    │   ┌───────────┐              ┌───────────┐                  │
    │   │    h1     │              │    h2     │                  │
    │   │.10        │              │.20        │                  │
    │   └─────┬─────┘              └─────┬─────┘                  │
    │         │                          │                        │
    │         └──────────┬───────────────┘                        │
    │                    │                                        │
    │              ┌─────┴─────┐                                   │
    │              │    s1     │                                   │
    │              └─────┬─────┘                                   │
    └────────────────────┼────────────────────────────────────────┘
                         │ eth0: 192.168.1.1
                   ┌─────┴─────┐
                   │   rnat    │  ← NAT/MASQUERADE
                   │  (router) │
                   └─────┬─────┘
                         │ eth1: 203.0.113.1
    ┌────────────────────┼────────────────────────────────────────┐
    │                    │                                        │
    │              ┌─────┴─────┐                                   │
    │              │    s2     │                                   │
    │              └─────┬─────┘                                   │
    │                    │                                        │
    │              ┌─────┴─────┐                                   │
    │              │    h3     │                                   │
    │              │.2         │                                   │
    │              └───────────┘                                   │
    │                                                             │
    │                    Rețea publică                            │
    │                    203.0.113.0/24 (TEST-NET-3)              │
    └─────────────────────────────────────────────────────────────┘
```

### Topologia SDN
```
                          ┌─────────────────────────────┐
                          │      Controller SDN         │
                          │       (OS-Ken)              │
                          │                             │
                          │  ┌──────────────────────┐   │
                          │  │  Motor de politici   │   │
                          │  │  • h1↔h2: PERMITE    │   │
                          │  │  • *→h3: BLOCHEAZĂ   │   │
                          │  │  • UDP→h3: CONFIG    │   │
                          │  └──────────────────────┘   │
                          └─────────────┬───────────────┘
                                        │ OpenFlow 1.3
                                        │ (port 6633)
    ┌───────────────────────────────────┼───────────────────────────────────┐
    │                                   │                                   │
    │                           ┌───────┴───────┐                           │
    │                           │      s1       │                           │
    │                           │   (OVS)       │                           │
    │                           │               │                           │
    │                           │ ┌───────────┐ │                           │
    │                           │ │Tabel flux │ │                           │
    │                           │ └───────────┘ │                           │
    │                           └───┬───┬───┬───┘                           │
    │                               │   │   │                               │
    │                    ┌──────────┘   │   └──────────┐                    │
    │                    │              │              │                    │
    │              ┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐              │
    │              │    h1     │  │    h2     │  │    h3     │              │
    │              │10.0.6.11  │  │10.0.6.12  │  │10.0.6.13  │              │
    │              │           │  │           │  │           │              │
    │              │ [✓ ACCES  │  │  [SERVER] │  │  [ACCES   │              │
    │              │  COMPLET] │  │           │  │RESTRICȚ.] │              │
    │              └───────────┘  └───────────┘  └───────────┘              │
    │                                                                       │
    │                        Rețea SDN: 10.0.6.0/24                         │
    └───────────────────────────────────────────────────────────────────────┘
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

### Probleme Mininet și OVS

**Problemă:** Erori la curățarea Mininet
```bash
# Curățare forțată
sudo mn -c

# Verifică procese reziduale
ps aux | grep -E "(ovs|mn)"

# Oprește OVS dacă e necesar
sudo service openvswitch-switch stop
sudo service openvswitch-switch start
```

**Problemă:** Controller-ul SDN nu primește conexiuni
```bash
# Verifică portul 6633
ss -tlnp | grep 6633

# Verifică configurația OVS
ovs-vsctl show

# Setează controller-ul manual
ovs-vsctl set-controller s1 tcp:127.0.0.1:6633
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week6_network

# Verifică DNS în container
docker exec week6_lab cat /etc/resolv.conf
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 6633

# Oprește procesul sau folosește alt port
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT6/06roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/stop_lab.py

# Curăță Mininet dacă a fost folosit
sudo mn -c 2>/dev/null

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
docker stop $(docker ps -q --filter "name=week6")

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

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
