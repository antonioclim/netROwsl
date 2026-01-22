# Săptămâna 5: Nivelul Rețea – Adresare IPv4/IPv6, Subrețele și VLSM

> Laborator Rețele de Calculatoare – ASE, Informatică Economică
> 
> realizat de Revolvix

---

## Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl  
**Folderul Acestei Săptămâni:** `05roWSL`

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

git clone https://github.com/antonioclim/netROwsl.git SAPT5
cd SAPT5
```

### Pasul 3: Verifică Clonarea

```powershell
dir
cd 05roWSL
dir
```

### Structura Completă a Directoarelor

```
D:\RETELE\
└── SAPT5\
    └── 05roWSL\
        ├── artifacts/       # Rezultate generate
        ├── docker/          # Configurație Docker
        ├── docs/            # Documentație
        │   ├── api_reference.md
        │   ├── arhitectura.md
        │   ├── depanare.md
        │   ├── exemple_utilizare.md
        │   ├── exercitii_perechi.md
        │   ├── exercitii_trace.md
        │   ├── fisa_comenzi.md
        │   ├── peer_instruction.md
        │   └── rezumat_teorie.md
        ├── homework/        # Teme pentru acasă
        ├── pcap/            # Fișiere de captură
        ├── scripts/         # Scripturi de automatizare
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă exerciții
        │   ├── apps/
        │   ├── exercises/
        │   └── utils/
        ├── tests/           # Teste automatizate
        ├── CHANGELOG.md
        ├── CONTRIBUTING.md
        └── README.md
```

---

## Configurarea Inițială a Mediului

### Pasul 1: Deschide Terminalul Ubuntu

Din Windows: Click pe "Ubuntu" în meniul Start, sau în PowerShell tastează `wsl`

### Pasul 2: Pornește Serviciul Docker

```bash
sudo service docker start
# Parolă: stud

docker ps
```

**Output așteptat:** Containerul `portainer` în listă.

### Pasul 3: Verifică Accesul la Portainer

1. Deschide browser-ul web
2. Navighează la: **http://localhost:9000**
3. Credențiale: `stud` / `studstudstud`

**Dacă Portainer nu răspunde:**
```bash
docker ps -a | grep portainer
docker start portainer
```

### Pasul 4: Navighează la Folderul Laboratorului

```bash
cd /mnt/d/RETELE/SAPT5/05roWSL
ls -la
```

---

## Prezentare Generală

Laboratorul 5 acoperă **Nivelul Rețea** din modelul TCP/IP: cum funcționează adresele IP, cum împarți o rețea în subrețele și când alegi FLSM vs VLSM.

**În practică vei:**
- Calcula adrese de rețea, broadcast și intervale de gazde
- Împărți blocuri de adrese pentru departamente cu cerințe diferite
- Compara eficiența FLSM vs VLSM pe scenarii reale
- Observa pachete IP în Wireshark pe containere Docker

**Mediul:** 3 containere pe rețeaua `week5_labnet` (10.5.0.0/24), gestionate prin Portainer la http://localhost:9000.

## Obiective

După laborator vei putea:

1. **Identifica** ce face Nivelul Rețea în OSI și TCP/IP
2. **Explica** diferențele IPv4 vs IPv6 (notație, structură, tipuri adrese)
3. **Calcula** adresa de rețea, broadcast și gazde utilizabile pentru orice CIDR
4. **Aplica** FLSM și VLSM pentru a împărți rețele conform cerințelor
5. **Proiecta** o schemă de adresare eficientă pentru o organizație
6. **Evalua** când FLSM e suficient și când ai nevoie de VLSM

## Cerințe Preliminare

### Cunoștințe Necesare

- Sisteme de numerație binară și hexazecimală
- Concepte de bază ale rețelelor (săptămânile 1-4)
- Familiaritate cu operațiile de linie de comandă

### Cerințe Software

- Windows 10/11 cu WSL2 activat
- Docker Engine (în WSL2)
- Portainer CE (portul 9000)
- Wireshark (Windows)
- Python 3.11+
- Git

### Cerințe Hardware

- Minim 8GB RAM (recomandat 16GB)
- 10GB spațiu liber pe disc

## Pornire Rapidă

### Configurare Inițială

```bash
cd /mnt/d/RETELE/SAPT5/05roWSL
python3 setup/verifica_mediu.py
```

### Pornirea Laboratorului

```bash
python3 scripts/porneste_laborator.py
python3 scripts/porneste_laborator.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Container Python | 10.5.0.10 | docker exec |
| Server UDP | 10.5.0.20:9999 | - |
| Client UDP | 10.5.0.30 | docker exec |

---

## Exerciții de Laborator

### Exercițiul 1: Analiză CIDR și Subnetare FLSM

**Obiectiv:** Analizezi blocuri CIDR și aplici FLSM pentru subrețele egale.

**Durată:** 25-30 minute

```bash
cd /mnt/d/RETELE/SAPT5/05roWSL

# Analiză standard
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.10.14/26

# Mod învățare cu predicții (recomandat!)
python3 src/exercises/ex_5_01_cidr_flsm.py invata 192.168.10.14/26

# Subnetare FLSM
python3 src/exercises/ex_5_01_cidr_flsm.py flsm 10.0.0.0/16 4
```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 1
```

---

### Exercițiul 2: Alocare VLSM și Operații IPv6

**Obiectiv:** Implementezi VLSM pentru cerințe variabile și operații IPv6.

**Durată:** 30-35 minute

```bash
# VLSM standard
python3 src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/16 --cerinte 500,120,60,30,2

# Mod învățare VLSM
python3 src/exercises/ex_5_02_vlsm_ipv6.py invata-vlsm 192.168.0.0/24 --cerinte 60,20,10,2

# Operații IPv6
python3 src/exercises/ex_5_02_vlsm_ipv6.py ipv6-comprimare "2001:0db8:0000:0000:0000:0000:0000:0001"
python3 src/exercises/ex_5_02_vlsm_ipv6.py ipv6-expandare "2001:db8::1"
```

---

### Exercițiul 3: Quiz Interactiv

**Obiectiv:** Testezi cunoștințele de adresare IP și subnetare.

**Durată:** 15-20 minute

```bash
# Quiz standard
python3 src/exercises/ex_5_03_generator_quiz.py

# Quiz scurt
python3 src/exercises/ex_5_03_generator_quiz.py --intrebari 5 --dificultate usor

# Pregătire examen
python3 src/exercises/ex_5_03_generator_quiz.py --intrebari 20 --dificultate greu
```

---

## Documentație

| Document | Descriere |
|----------|-----------|
| [Rezumat Teoretic](docs/rezumat_teorie.md) | Concepte IPv4, IPv6, CIDR, VLSM |
| [Fișa de Comenzi](docs/fisa_comenzi.md) | Referință rapidă pentru laborator |
| [Depanare](docs/depanare.md) | Soluții pentru probleme comune |
| [Referință API](docs/api_reference.md) | Documentație funcții Python |
| [Exemple Utilizare](docs/exemple_utilizare.md) | Scenarii complete |
| [Arhitectura Cod](docs/arhitectura.md) | Structura și design-ul codului |
| [Peer Instruction](docs/peer_instruction.md) | Întrebări MCQ pentru seminarii |
| [Exerciții Perechi](docs/exercitii_perechi.md) | Activități pair programming |
| [Exerciții Trace](docs/exercitii_trace.md) | Exerciții non-coding |

---

## Teme pentru Acasă

| Temă | Descriere | Durată | Nivel Bloom |
|------|-----------|--------|-------------|
| [Tema 1](homework/exercises/tema1_retea_corporativa.md) | Rețea corporativă TechVision SRL | 2-3h | APPLY |
| [Tema 2](homework/exercises/tema2_migrare_ipv6.md) | Plan migrare IPv6 | 2-3h | ANALYZE |
| [Tema 3](homework/exercises/tema3_design_startup.md) | Design rețea startup | 3-4h | CREATE |

---

## Utilizarea Wireshark

### Selectarea Interfeței

| Interfață | Când să folosești |
|-----------|-------------------|
| **vEthernet (WSL)** | Trafic Docker WSL (cel mai frecvent) |
| **Loopback** | Trafic localhost |

### Filtre Utile

| Filtru | Scop |
|--------|------|
| `ip.addr == 10.5.0.0/24` | Trafic rețeaua laborator |
| `udp.port == 9999` | Server UDP Echo |
| `ip.addr == 10.5.0.10` | Container Python |
| `icmp` | Pachete ping |

### Salvarea Capturilor

Salvează în `pcap/` cu nume descriptiv: `udp_echo_demo.pcap`

---

## Context Teoretic

### Arhitectura IPv4

Adresele IPv4 au 32 de biți în notație zecimală cu punct (192.168.1.1).

**Clase de adrese:**
- Clasa A: 1.0.0.0 – 126.255.255.255 (/8 implicit)
- Clasa B: 128.0.0.0 – 191.255.255.255 (/16 implicit)
- Clasa C: 192.0.0.0 – 223.255.255.255 (/24 implicit)

**Adrese private (RFC 1918):** 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

### FLSM vs VLSM

**FLSM** împarte o rețea în subrețele egale — simplu de administrat dar risipește adrese.

**VLSM** permite subrețele de dimensiuni diferite — eficient dar necesită planificare atentă.

### IPv6

Adrese de 128 biți în notație hexazecimală (2001:db8::1).

Gândește-te la adrese IP ca la coduri poștale:
- **IPv4** = cod poștal românesc (6 cifre): 010011 — ~4.3 miliarde combinații (toate ocupate)
- **IPv6** = cod poștal universal galactic (32 cifre hex) — 340 undecilioane de combinații

---

## Diagramă de Arhitectură

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEEK5_WSLkit Environment                     │
│                    Rețea: week5_labnet (10.5.0.0/24)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  week5_python   │  │ week5_udp-server│  │ week5_udp-client│ │
│  │  IP: 10.5.0.10  │  │  IP: 10.5.0.20  │  │  IP: 10.5.0.30  │ │
│  │  • Python 3.11  │  │  Port: 9999     │  │  • Client UDP   │ │
│  │  • Exerciții    │  │  • Server Echo  │  │  • Testare      │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
│           └────────────────────┼────────────────────┘          │
│                    ┌───────────┴───────────┐                   │
│                    │   Docker Bridge Net   │                   │
│                    │    10.5.0.0/24        │                   │
│                    └───────────────────────┘                   │
├─────────────────────────────────────────────────────────────────┤
│  Portainer: http://localhost:9000 (stud/studstudstud)          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Depanare Rapidă

### Docker nu pornește
```bash
sudo service docker start
docker ps
```

### Portainer nu răspunde
```bash
docker start portainer
```

### ModuleNotFoundError
```bash
cd /mnt/d/RETELE/SAPT5/05roWSL
export PYTHONPATH=.
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.1.0/24
```

Pentru probleme detaliate, consultă [docs/depanare.md](docs/depanare.md).

---

## Referințe

- Kurose & Ross. *Computer Networking: A Top-Down Approach* (7th ed.)
- RFC 791 — Internet Protocol (IPv4)
- RFC 8200 — Internet Protocol, Version 6 (IPv6)
- RFC 4632 — Classless Inter-domain Routing (CIDR)

---

*Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix*
