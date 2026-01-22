# Săptămâna 6: NAT/PAT, Protocoale de Suport și Rețele Definite prin Software

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | Laborator Rețele de Calculatoare
> 
> de ing. dr. Antonio Clim

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

## Clonarea Laboratorului

### Pasul 1: Deschide PowerShell (Windows)

Apasă `Win + X` → Selectează "Windows Terminal" sau "PowerShell"

### Pasul 2: Navighează și Clonează

```powershell
mkdir D:\RETELE -ErrorAction SilentlyContinue
cd D:\RETELE
git clone https://github.com/antonioclim/netROwsl.git SAPT6
cd SAPT6
```

### Pasul 3: Verifică Clonarea

```powershell
dir
cd 06roWSL
dir
```

### Structura Directoarelor

```
D:\RETELE\
└── SAPT6\
    └── 06roWSL\
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

## 🔧 Configurarea Inițială a Mediului

### Pasul 1: Deschide Terminalul Ubuntu

Din Windows:
- Click pe "Ubuntu" în meniul Start, SAU
- În PowerShell tastează: `wsl`, SAU
- În Windows Terminal selectează tab-ul "Ubuntu"

### Pasul 2: Pornește Serviciul Docker

```bash
sudo service docker start
docker ps
```

**Output așteptat:**
```
CONTAINER ID   IMAGE                    STATUS          NAMES
abc123...      portainer/portainer-ce   Up 2 hours      portainer
```

### Pasul 3: Verifică Accesul la Portainer

Navighează la: **http://localhost:9000**
- Utilizator: `stud`
- Parolă: `studstudstud`

### Pasul 4: Navighează la Folderul Laboratorului

```bash
cd /mnt/d/RETELE/SAPT6/06roWSL
ls -la
```

---

## Prezentare generală

Această sesiune de laborator integrează două domenii complementare ale arhitecturii moderne de rețea: mecanismele de traducere a adreselor care susțin ciclul de viață extins al IPv4, și rețelele definite prin software (SDN) care decuplează logica de control de hardware-ul de redirecționare.

Prima componentă examinează Network Address Translation (NAT) și varianta sa cu multiplexare de porturi (PAT/NAPT). Studenții vor configura reguli MASQUERADE bazate pe iptables pe un router Linux, vor observa procesul bidirecțional de traducere și vor analiza modul în care alocarea de porturi efemere permite mai multor hosturi interne să partajeze o singură adresă publică.

A doua componentă introduce arhitectura SDN prin OpenFlow 1.3, demonstrând separarea fundamentală dintre planul de control și planul de date. Folosind OS-Ken ca framework de controller și Open vSwitch ca switch programabil, studenții vor implementa și observa politici bazate pe fluxuri.

## Obiective de învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Reamintească** scopul și clasificarea variantelor NAT (static, dinamic, PAT) și rolul protocoalelor auxiliare (ARP, DHCP, ICMP, NDP)
2. **Explice** cum tabelele de traducere PAT mențin starea bidirecțională a sesiunii
3. **Implementeze** reguli NAT/MASQUERADE folosind iptables pe un router Linux multi-homed
4. **Demonstreze** instalarea fluxurilor SDN prin observarea comunicării controller-switch
5. **Analizeze** diferențele comportamentale dintre traficul permis și cel blocat într-o topologie SDN
6. **Compare** rutarea distribuită tradițională cu controlul SDN centralizat
7. **Proiecteze** politici OpenFlow personalizate care implementează controlul accesului

## Cerințe preliminare

### Cerințe de cunoștințe

- Înțelegerea adresării IPv4, subnetting-ului și notației CIDR (Săptămânile 4-5)
- Familiarizare cu conceptele de programare socket TCP/UDP (Săptămânile 2-3)
- Competențe de bază în linia de comandă Linux

### Cerințe software

- Windows 10/11 cu WSL2 activat (Ubuntu 22.04 sau ulterior)
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație nativă Windows)
- Python 3.11 sau ulterior

---

## Pornire rapidă

### Configurare inițială

```bash
cd /mnt/d/RETELE/SAPT6/06roWSL
python3 setup/verify_environment.py
python3 setup/install_prerequisites.py
```

### Pornirea laboratorului

```bash
python3 scripts/start_lab.py
python3 scripts/start_lab.py --status
```

---

### 🤔 PREDICȚIE: Containere Docker

După `python3 scripts/start_lab.py`, câte containere vor rula?

- [ ] 1 (doar week6_lab)
- [ ] 2 (week6_lab + week6_controller)
- [ ] 3 (include și Portainer)

💡 Hint: Portainer rulează global și nu este gestionat de scriptul de laborator.

Verifică cu `docker ps` după pornire.

---

### Accesarea serviciilor

| Serviciu | URL/Port | Scop |
|----------|----------|------|
| Portainer | http://localhost:9000 | Panou de administrare containere |
| Controller SDN | localhost:6633 | Endpoint controller OpenFlow |
| Router NAT | 203.0.113.1 | Gateway NAT cu interfață publică |
| Observator NAT | Port 5000 | Demonstrație traducere PAT |
| Echo TCP | Port 9090 | Testare conectivitate SDN |
| Echo UDP | Port 9091 | Testare politici specifice protocolului |

---

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
| NAT public | 203.0.113.1 | Interfața routerului (partea publică) |
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

---

## Exerciții de laborator

> 💡 **Recomandare:** Lucrează în perechi (driver/navigator) pentru exercițiile practice. Schimbă rolurile la fiecare 15 minute.

### Exercițiul 1: Configurarea și observarea NAT/PAT

**Obiectiv:** Configurarea NAT MASQUERADE pe un router Linux și observarea traducerii adreselor de port în acțiune.

**Durată:** 40 minute

**Context:** Când hosturile private comunică cu serverele publice, NAT rescrie adresele sursă la adresa IP publică a routerului. PAT extinde acest lucru traducând și porturile sursă.

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

---

### 🤔 PREDICȚIE: Traducere NAT

Înainte de a rula clientul de pe h1, gândește-te:

1. **Ce adresă IP sursă** va vedea serverul h3 în pachetul primit?
   - [ ] 192.168.1.10 (IP-ul original al lui h1)
   - [ ] 203.0.113.1 (IP-ul public al routerului NAT)
   - [ ] 192.168.1.1 (IP-ul privat al routerului)

2. **Ce port sursă** va vedea h3?
   - [ ] Același port folosit de h1
   - [ ] Un port diferit, ales de routerul NAT
   - [ ] Portul 5000 (portul serverului)

📝 Notează predicțiile tale, apoi rulează comanda și compară.

---

4. De pe hosturile private, inițiază conexiuni:
   ```bash
   h1 python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Salut de la h1"
   h2 python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Salut de la h2"
   ```

5. Observă output-ul serverului - notează că ambele conexiuni par să provină de la 203.0.113.1 cu porturi sursă diferite.

6. Verifică traducerile NAT:
   ```bash
   rnat conntrack -L 2>/dev/null || rnat cat /proc/net/nf_conntrack
   ```

---

### 🤔 PREDICȚIE: Tabela Conntrack

Dacă h1 și h2 au trimis ambele câte un mesaj către h3:

1. Câte intrări vor fi în tabela conntrack? __________
2. Ce protocol va fi listat pentru fiecare? __________
3. Ce stare vor avea conexiunile? __________

---

**Observații așteptate:**
- Adresele private (192.168.1.x) nu sunt niciodată vizibile pe partea publică
- Fiecare conexiune de la hosturi interne diferite folosește un port tradus unic
- Tabela NAT menține starea bidirecțională pentru traficul de retur

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 1
```

---

## 🗳️ PEER INSTRUCTION: Tabela de Traducere NAT

### Scenariu

Hostul h1 (192.168.1.10) inițiază o conexiune TCP către serverul h3 (203.0.113.2:5000).
Routerul NAT are IP public 203.0.113.1.

Output din `conntrack -L`:
```
tcp  ESTABLISHED src=192.168.1.10 dst=203.0.113.2 sport=45678 dport=5000 
                 src=203.0.113.2 dst=203.0.113.1 sport=5000 dport=50001
```

### Întrebare

Ce port sursă vede serverul h3 în pachetele primite de la h1?

### Opțiuni

| Opțiune | Răspuns |
|---------|---------|
| **A** | 45678 — portul original folosit de h1 |
| **B** | 5000 — portul pe care ascultă serverul |
| **C** | 50001 — portul tradus de routerul NAT |
| **D** | 9000 — portul Portainer |

<details>
<summary>🎯 Click pentru răspuns și explicație (după discuție)</summary>

**Răspuns corect: C (50001)**

**Explicație:**
Output-ul conntrack arată două perspective:
- **Linia 1:** Perspectiva clientului → src=192.168.1.10:45678 dst=203.0.113.2:5000
- **Linia 2:** Perspectiva răspunsului → src=203.0.113.2:5000 dst=**203.0.113.1:50001**

Serverul h3 vede doar ce este în linia 2: pachetele vin de la 203.0.113.1:50001.

**Analiza distractorilor:**
- **A (45678):** Misconceptie că NAT păstrează portul sursă original
- **B (5000):** Confuzie între portul sursă și destinație
- **D (9000):** Portul Portainer nu are legătură cu exercițiul

</details>

---

### Exercițiul 2: Topologie SDN și observarea fluxurilor

**Obiectiv:** Implementarea unei topologii SDN cu un controller OpenFlow și observarea redirecționării pachetelor bazate pe fluxuri.

**Durată:** 35 minute

**Context:** SDN separă planul de control de planul de date. Controller-ul instalează reguli de flux în switch-uri care definesc perechi match-action.

**Pași:**

1. Pornește topologia SDN cu reguli de flux:
   ```bash
   python3 scripts/run_demo.py --demo sdn
   ```

---

### 🤔 PREDICȚIE: Politici SDN

Conform politicii controller-ului (h1↔h2: PERMITE, *→h3: BLOCHEAZĂ):

| Test | Predicție | Rezultat real |
|------|-----------|---------------|
| `h1 ping -c 3 h2` | □ Funcționează / □ Eșuează | __________ |
| `h1 ping -c 3 h3` | □ Funcționează / □ Eșuează | __________ |
| `h2 ping -c 3 h3` | □ Funcționează / □ Eșuează | __________ |
| `h3 ping -c 3 h1` | □ Funcționează / □ Eșuează | __________ |

📝 Gândește-te la direcția traficului și la regulile instalate.

---

2. În CLI-ul Mininet, verifică conectivitatea:
   ```bash
   h1 ping -c 3 h2
   h1 ping -c 3 h3
   h2 ping -c 3 h3
   ```

---

### 🤔 PREDICȚIE: Tabele de Fluxuri

Ce reguli te aștepți să vezi în tabela de fluxuri a switch-ului s1?

- [ ] O singură regulă table-miss (actions=CONTROLLER)
- [ ] Reguli specifice pentru fiecare pereche de hosturi
- [ ] Reguli separate pentru ARP și IPv4
- [ ] Reguli cu prioritate 0, 10, 20, 30

Rulează `ovs-ofctl -O OpenFlow13 dump-flows s1` și numără regulile.

---

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
   h1 python3 src/apps/tcp_echo.py client --host 10.0.6.12
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

---

## 🗳️ PEER INSTRUCTION: Prioritate Fluxuri OpenFlow

### Scenariu

Controller-ul a instalat următoarele reguli în switch-ul s1:

```
priority=30, ip, nw_dst=10.0.6.13, actions=drop
priority=10, ip, nw_src=10.0.6.11, nw_dst=10.0.6.12, actions=output:2
priority=0,  actions=CONTROLLER
```

### Întrebare

h1 (10.0.6.11) trimite un pachet ICMP către h3 (10.0.6.13). Ce se întâmplă cu pachetul?

### Opțiuni

| Opțiune | Răspuns |
|---------|---------|
| **A** | Pachetul ajunge la h3 — a doua regulă permite traficul de la h1 |
| **B** | Pachetul este trimis la controller — nu există regulă specifică pentru ICMP |
| **C** | Pachetul este aruncat (DROP) — prima regulă are prioritate mai mare |
| **D** | Pachetul este trimis în flood pe toate porturile |

<details>
<summary>🎯 Click pentru răspuns și explicație (după discuție)</summary>

**Răspuns corect: C (DROP)**

**Explicație:**
OpenFlow verifică regulile în ordinea **priorității**, nu în ordinea listării:
1. **priority=30** (nw_dst=10.0.6.13) → SE POTRIVEȘTE → actions=**drop**
2. priority=10 și priority=0 nu mai sunt verificate

Pachetul este aruncat deoarece destinația (10.0.6.13 = h3) se potrivește cu regula de blocare care are prioritate 30.

**Concept cheie:** Prioritate mai mare = verificată prima. Nu contează ordinea în listă!

**Întrebare follow-up:** Ce prioritate ar trebui o regulă care permite DOAR ICMP de la h1 la h3?

</details>

---

### Exercițiul 3: Modificarea politicilor SDN

**Obiectiv:** Modificarea politicilor controller-ului pentru a schimba comportamentul de acces la nivel de protocol.

**Durată:** 30 minute

**Pași:**

1. Examinează codul controller-ului:
   ```bash
   code src/apps/sdn_policy_controller.py
   ```

2. Localizează secțiunea de definire a politicilor și modifică pentru a permite UDP pe portul 9091 la h3

---

### 🤔 PREDICȚIE: Modificare Politici SDN

După ce activezi `ALLOW_UDP_TO_H3 = True` în controller:

| Test | Predicție | Motivație |
|------|-----------|-----------|
| `h1 ping h3` (ICMP) | □ Funcționează / □ Eșuează | ________________ |
| `h1 → h3` UDP port 9091 | □ Funcționează / □ Eșuează | ________________ |
| `h1 → h3` TCP port 9090 | □ Funcționează / □ Eșuează | ________________ |

💡 Gândește-te: ICMP ≠ UDP ≠ TCP. Fiecare are propriile reguli.

---

3. Repornește controller-ul și testează noua politică:
   ```bash
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

---

## 🗳️ PEER INSTRUCTION: Izolarea Rețelelor Docker

### Scenariu

```yaml
services:
  week6-lab:
    networks:
      - lab_network
  
  database:
    networks:
      - db_network

networks:
  lab_network:
  db_network:
```

### Întrebare

Poate containerul `week6-lab` să comunice cu containerul `database` folosind numele serviciului?

### Opțiuni

| Opțiune | Răspuns |
|---------|---------|
| **A** | Da — toate containerele din același docker-compose.yml pot comunica automat |
| **B** | Da — Docker rezolvă automat numele între toate rețelele |
| **C** | Nu — sunt pe rețele Docker diferite, fără suprapunere |
| **D** | Nu — trebuie să folosească adrese IP, numele nu funcționează niciodată |

<details>
<summary>🎯 Click pentru răspuns</summary>

**Răspuns corect: C (Nu, rețele diferite)**

Docker creează izolare la nivel de rețea. Containerele comunică doar în cadrul aceleiași rețele.

</details>

---

## Oprirea laboratorului

### Oprire standard

```bash
cd /mnt/d/RETELE/SAPT6/06roWSL
python3 scripts/stop_lab.py
docker ps
```

### Curățare completă

```bash
python3 scripts/cleanup.py --full --prune
```

---

## Teme pentru acasă

Consultă directorul `homework/` pentru exercițiile de lucru individual.

---

## 🔧 Depanare

### Probleme frecvente

#### Problemă: Erori la curățarea Mininet
**Soluție:**
```bash
python3 scripts/cleanup.py --force
sudo mn -c
```

#### Problemă: Switch-ul OVS nu se conectează la controller
**Soluție:**
```bash
ss -ltn | grep 6633
ovs-vsctl show
```

#### Problemă: NAT nu traduce pachetele
**Soluție:**
```bash
sysctl net.ipv4.ip_forward
sudo sysctl -w net.ipv4.ip_forward=1
```

#### Problemă: Ping-urile în topologia SDN sunt lente
**Soluție:**
```bash
ovs-ofctl -O OpenFlow13 dump-flows s1
```

Consultă `docs/troubleshooting.md` pentru soluții suplimentare.

---

## Fundamente teoretice

### NAT și PAT

Network Address Translation a apărut ca răspuns la epuizarea adreselor IPv4, permițând organizațiilor să folosească intervale de adrese private intern, în timp ce partajează adrese publice limitate extern. Port Address Translation extinde acest lucru prin multiplexarea conexiunilor prin numere de port.

Procesul de traducere implică:
1. **Ieșire:** Rescrierea IP-ului sursă la adresa publică a dispozitivului NAT
2. **Urmărirea stării:** Menținerea unei tabele de traducere
3. **Intrare:** Traducerea inversă folosind starea stocată

---

### 🏢 Analogie: Port Mapping ca Sistem de Apartamente

Imaginează-ți o **clădire de birouri** (routerul NAT):

| Concept tehnic | Analogie |
|----------------|----------|
| IP public (203.0.113.1) | Adresa clădirii (Str. Victoriei nr. 10) |
| Port tradus (50001) | Numărul apartamentului |
| Conexiune internă (192.168.1.10:45678) | Locatarul din apartament |
| Tabela NAT | Lista de locatari a portarului |

**Scenariul:**
1. Un curier (pachet de răspuns) vine cu un colet pentru "Str. Victoriei 10, Ap. 50001"
2. Portarul (routerul NAT) verifică lista: "Ap. 50001 = Firma ABC din camera 10"
3. Coletul ajunge la destinația corectă

**De aceea serverul extern vede doar adresa clădirii (IP public), nu și camera originală (IP privat)!**

---

### 📋 Analogie: Conntrack ca Registru de Vizitatori

Routerul NAT ține un **registru ca la recepția unui hotel**:

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  REGISTRUL RECEPȚIEI (conntrack table)                                    ║
╠═══════════╦═══════════════════════════╦═══════════════════════╦══════════╣
║  Camera   ║  Oaspete intern           ║  Vizitator extern     ║  Status  ║
╠═══════════╬═══════════════════════════╬═══════════════════════╬══════════╣
║  50001    ║  h1 (192.168.1.10:45678)  ║  h3 (203.0.113.2:5000)║  ACTIV   ║
║  50002    ║  h2 (192.168.1.20:34567)  ║  h3 (203.0.113.2:5000)║  ACTIV   ║
╚═══════════╩═══════════════════════════╩═══════════════════════╩══════════╝
```

---

### Rețele definite prin software

SDN reprezintă o schimbare arhitecturală fundamentală de la controlul distribuit la controlul centralizat al rețelei. Principiile cheie includ:
1. **Separarea responsabilităților:** Logica de control distinctă de redirecționare
2. **Programabilitate:** Comportamentul rețelei definit prin API-uri software
3. **Viziune centralizată:** Controller-ul menține starea globală a rețelei
4. **Redirecționare bazată pe fluxuri:** Pachetele sunt potrivite cu reguli și se aplică acțiuni

---

### 🚦 Analogie: Tabela de Fluxuri ca Regulament de Trafic

Switch-ul OpenFlow funcționează ca un **agent de circulație** cu un caiet de reguli:

```
╔════════════════════════════════════════════════════════════════════╗
║  CAIETUL AGENTULUI DE CIRCULAȚIE                                   ║
╠════════════════════════════════════════════════════════════════════╣
║  Pagina 30 (URGENTĂ):                                              ║
║    Dacă vezi mașină spre Strada H3 → OPREȘTE-O!                    ║
║                                                                    ║
║  Pagina 10:                                                        ║
║    Dacă vezi mașină de pe H1 spre H2 → Lasă să treacă pe banda 2   ║
║                                                                    ║
║  Ultima pagină (dacă nimic altceva):                               ║
║    Sună la dispecerat (controller) și întreabă ce să faci         ║
╚════════════════════════════════════════════════════════════════════╝
```

**Regula cheie:** Agentul verifică paginile în ordinea **numărului** (priorității), NU în ordinea în care au fost scrise!

---

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ediția a 7-a). Pearson.
- RFC 1918 – Alocarea adreselor pentru rețele private
- RFC 5737 – Blocuri de adrese IPv4 rezervate pentru documentație
- Open Networking Foundation (2015). *OpenFlow Switch Specification* Versiunea 1.3.5

---

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

### Fluxul Traducerii NAT

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        FLUXUL TRADUCERII NAT                            │
├─────────────────────────────────────────────────────────────────────────┤
│  h1 (192.168.1.10)              Router NAT              h3 (203.0.113.2)│
│        │                            │                          │        │
│        │  1. SYN                    │                          │        │
│        │  src=192.168.1.10:45678    │                          │        │
│        ├───────────────────────────►│                          │        │
│        │                            │                          │        │
│        │                   2. Traducere SNAT                   │        │
│        │                   src=203.0.113.1:50001               │        │
│        │                            ├─────────────────────────►│        │
│        │                            │                          │        │
│        │                            │  3. SYN-ACK              │        │
│        │                            │◄─────────────────────────┤        │
│        │                            │                          │        │
│        │  4. Traducere inversă      │                          │        │
│        │◄───────────────────────────┤                          │        │
└─────────────────────────────────────────────────────────────────────────┘
```

### Topologia SDN
```
                          ┌─────────────────────────────┐
                          │      Controller SDN         │
                          │       (OS-Ken)              │
                          │  ┌──────────────────────┐   │
                          │  │  Motor de politici   │   │
                          │  │  • h1↔h2: PERMITE    │   │
                          │  │  • *→h3: BLOCHEAZĂ   │   │
                          │  └──────────────────────┘   │
                          └─────────────┬───────────────┘
                                        │ OpenFlow 1.3
    ┌───────────────────────────────────┼───────────────────────────────────┐
    │                           ┌───────┴───────┐                           │
    │                           │      s1       │                           │
    │                           │   (OVS)       │                           │
    │                           └───┬───┬───┬───┘                           │
    │                    ┌──────────┘   │   └──────────┐                    │
    │              ┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐              │
    │              │    h1     │  │    h2     │  │    h3     │              │
    │              │10.0.6.11  │  │10.0.6.12  │  │10.0.6.13  │              │
    │              │ [ACCES    │  │  [SERVER] │  │  [ACCES   │              │
    │              │  COMPLET] │  │           │  │RESTRICȚ.] │              │
    │              └───────────┘  └───────────┘  └───────────┘              │
    │                        Rețea SDN: 10.0.6.0/24                         │
    └───────────────────────────────────────────────────────────────────────┘
```

---

## 🧹 Procedura de Curățare

### Sfârșit de Sesiune

```bash
python3 scripts/stop_lab.py
sudo mn -c 2>/dev/null
docker ps
```

### Curățare Completă

```bash
python3 scripts/cleanup.py --full
docker image prune -f
docker network prune -f
```

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
