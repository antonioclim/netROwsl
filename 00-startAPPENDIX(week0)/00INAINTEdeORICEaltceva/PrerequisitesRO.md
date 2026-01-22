# 🖧 Laborator Rețele de Calculatoare — Ghid de Configurare a Mediului

> **Documentație Completă pentru Cerințe Prealabile**  
> Academia de Studii Economice, București — Facultatea de Cibernetică, Statistică și Informatică Economică  
> *Programele Informatică Economică & IA în Economie și Afaceri*

---

## 📋 Cuprins

1. [Introducere](#1-introducere)
2. [Prezentare Generală a Arhitecturii](#2-prezentare-generală-a-arhitecturii)
3. [Credențiale Standard](#3-credențiale-standard)
4. [Pasul 1: Activare WSL2](#4-pasul-1-activare-wsl2)
5. [Pasul 2: Instalare Ubuntu 22.04](#5-pasul-2-instalare-ubuntu-2204)
6. [Pasul 3: Instalare Docker în WSL](#6-pasul-3-instalare-docker-în-wsl)
7. [Pasul 4: Instalare Portainer CE](#7-pasul-4-instalare-portainer-ce)
8. [Pasul 5: Instalare Wireshark](#8-pasul-5-instalare-wireshark)
9. [Pasul 6: Pachete Python](#9-pasul-6-pachete-python)
10. [Pasul 7: Configurare Auto-start](#10-pasul-7-configurare-auto-start-opțional)
11. [Verificare Finală](#11-verificare-finală)
12. [Depanare](#12-depanare)
13. [Fișă de Referință Rapidă](#13-fișă-de-referință-rapidă)

---

## 1. Introducere

### 1.1 Scopul Acestui Ghid

Acest ghid complet vă conduce prin configurarea unui mediu complet de laborator pentru rețele pe Windows. La final, veți avea un mediu containerizat complet funcțional capabil de:

- **Rularea experimentelor de rețea izolate** folosind containere Docker
- **Capturarea și analiza traficului de rețea** cu Wireshark
- **Gestionarea vizuală a containerelor** prin interfața web Portainer
- **Automatizarea interacțiunilor de rețea** folosind Python

### 1.2 De Ce Această Arhitectură?

Folosim **WSL2 + Docker în Ubuntu** în loc de Docker Desktop din mai multe motive convingătoare:

| Aspect | WSL2 + Docker | Docker Desktop |
|--------|---------------|----------------|
| **Performanță** | Kernel Linux nativ, I/O mai rapid | Overhead de virtualizare |
| **Consum Resurse** | Amprentă mai mică de memorie | Consum RAM mai mare |
| **Acces Rețea** | Stack de rețea Linux complet | Rețea abstractizată |
| **Valoare Educativă** | Mediu Linux real | Abstracție Windows |
| **Cost** | Complet gratuit | Licențiere pentru întreprinderi |

### 1.3 Ce Veți Instala

| Component | Versiune | Scop |
|-----------|----------|------|
| WSL2 | 2.x | Windows Subsystem for Linux |
| Ubuntu | 22.04 LTS | Distribuție Linux |
| Docker | 28.2.2 | Runtime pentru containere |
| Docker Compose | 1.29.x | Orchestrare multi-container |
| Portainer CE | 2.33.6 LTS | Management containere prin web |
| Wireshark | 4.4.x | Analizor de protocoale de rețea |
| Pachete Python | Ultima versiune | docker, scapy, dpkt |

### 1.4 Estimare Timp

- **Timp total de instalare:** 30-45 minute
- **Necesită restart:** Da (după instalarea WSL2)
- **Conexiune internet:** Necesară pentru descărcări

---

## 2. Prezentare Generală a Arhitecturii

### 2.1 Diagrama Arhitecturii Sistemului

```
┌─────────────────────────────────────────────────────────────────┐
│                         WINDOWS 11                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Wireshark     │  │    Browser      │  │   PowerShell    │  │
│  │   (Captură)     │  │  (Portainer)    │  │   (Comenzi)     │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
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
│  │  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │    │  │  │
│  │  │  │  │Container│ │Container│ │Portainer│       │    │  │  │
│  │  │  │  │   A     │ │   B     │ │  :9000  │       │    │  │  │
│  │  │  │  └─────────┘ └─────────┘ └─────────┘       │    │  │  │
│  │  │  │         Rețea Docker (bridge)               │    │  │  │
│  │  │  └─────────────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Fluxul Rețelei

1. **Containerele Docker** comunică prin rețeaua bridge internă Docker
2. **Traficul iese** prin interfața de rețea virtuală WSL2
3. **Wireshark pe Windows** capturează traficul pe `vEthernet (WSL)`
4. **Portainer** este accesibil via `localhost:9000` din browserul Windows

### 2.3 Maparea Porturilor

| Serviciu | Port Container | Port Gazdă | URL Acces |
|----------|----------------|------------|-----------|
| Portainer | 9000 | 9000 | http://localhost:9000 |
| Portainer HTTPS | 9443 | 9443 | https://localhost:9443 |
| Portainer Edge | 8000 | 8000 | (Comunicare Agent) |

---

## 3. Credențiale Standard

> ⚠️ **Important:** Folosiți exact aceste credențiale pentru toate exercițiile de laborator pentru a asigura consistența.

### 3.1 Utilizator Ubuntu WSL

| Câmp | Valoare |
|------|---------|
| **Nume utilizator** | `stud` |
| **Parolă** | `stud` |

Acest utilizator este creat în timpul instalării Ubuntu și are privilegii `sudo`.

### 3.2 Administrator Portainer

| Câmp | Valoare |
|------|---------|
| **Nume utilizator** | `stud` |
| **Parolă** | `studstudstud` |
| **URL Acces** | http://localhost:9000 |

> 📝 **Notă:** Portainer necesită o parolă de minim 12 caractere, de aceea `studstudstud`.

---

## 4. Pasul 1: Activare WSL2

### 4.1 Ce Este WSL2?

**Windows Subsystem for Linux 2 (WSL2)** este un strat de compatibilitate care permite rularea unui kernel Linux autentic direct pe Windows. Spre deosebire de WSL1, care traducea apelurile de sistem Linux, WSL2 rulează un kernel Linux complet într-o mașină virtuală ușoară, oferind:

- Compatibilitate completă cu apelurile de sistem
- Performanță dramatic îmbunătățită a sistemului de fișiere
- Suport complet Docker fără emulare
- Capabilități native de rețea Linux

### 4.2 Cerințe de Sistem

- **Sistem de Operare:** Windows 10 versiunea 2004+ sau Windows 11
- **Arhitectură:** Procesor 64-bit cu suport pentru virtualizare
- **RAM:** Minim 4GB (8GB+ recomandat)
- **BIOS:** Virtualizare activată (VT-x/AMD-V)

### 4.3 Pași de Instalare

#### Pasul 1: Deschideți PowerShell ca Administrator

1. Apăsați `Win + X` sau click dreapta pe butonul Start
2. Selectați **"Windows Terminal (Admin)"** sau **"PowerShell (Admin)"**
3. Click **"Da"** la promptul User Account Control

#### Pasul 2: Instalați WSL2

Executați următoarea comandă:

```powershell
wsl --install
```

**Ce face această comandă:**
- Activează funcția opțională WSL
- Activează funcția Virtual Machine Platform
- Descarcă și instalează kernel-ul Linux
- Setează WSL2 ca versiune implicită

#### Pasul 3: Reporniți Calculatorul

> 🔄 **Este necesar un restart.** Salvați tot lucrul înainte de a continua.

```powershell
Restart-Computer
```

Sau reporniți manual prin meniul Start.

#### Pasul 4: Verificați Instalarea

După restart, deschideți PowerShell și verificați:

```powershell
wsl --status
```

**Output așteptat:**
```
Default Distribution: Ubuntu
Default Version: 2

Windows Subsystem for Linux a fost actualizat ultima dată pe [dată]
Actualizările automate WSL sunt activate.

Versiune kernel: 5.15.x.x-microsoft-standard-WSL2
```

### 4.4 Lista de Verificare

- [ ] `wsl --status` arată "Default Version: 2"
- [ ] Nicio eroare despre virtualizare
- [ ] Serviciul WSL rulează

---

## 5. Pasul 2: Instalare Ubuntu 22.04

### 5.1 De Ce Ubuntu 22.04 LTS?

**Ubuntu 22.04 LTS (Jammy Jellyfish)** este distribuția noastră aleasă deoarece:

- **Suport pe Termen Lung (LTS):** Actualizări de securitate până în Aprilie 2027
- **Stabilitate:** Pachete testate temeinic, gata pentru producție
- **Compatibilitate:** Suport și documentație excelente pentru Docker
- **Comunitate:** Cea mai mare comunitate Linux pentru depanare

### 5.2 Pași de Instalare

#### Pasul 1: Instalați Ubuntu din PowerShell

Deschideți PowerShell ca Administrator și executați:

```powershell
wsl --install -d Ubuntu-22.04 --web-download
```

**Explicația comenzii:**
- `wsl --install`: Invocă instalatorul WSL
- `-d Ubuntu-22.04`: Specifică distribuția
- `--web-download`: Descarcă de pe serverele Microsoft (mai fiabil)

#### Pasul 2: Configurare Inițială

După finalizarea descărcării, Ubuntu va porni automat. Veți vedea:

```
Se instalează, aceasta poate dura câteva minute...
Vă rugăm să creați un cont de utilizator UNIX implicit. Numele de utilizator nu trebuie să coincidă cu cel din Windows.
Pentru mai multe informații vizitați: https://aka.ms/wslusers
Introduceți noul nume de utilizator UNIX:
```

#### Pasul 3: Creați Contul de Utilizator

> ⚠️ **Critic:** Folosiți credențialele standard!

```
Introduceți noul nume de utilizator UNIX: stud
Parolă nouă: stud
Reintroduceți parola nouă: stud
```

**Notă:** Parola nu se va afișa în timp ce tastați - aceasta este comportamentul normal Linux.

#### Pasul 4: Verificați Instalarea

```powershell
wsl -l -v
```

**Output așteptat:**
```
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2
```

### 5.3 Înțelegerea Mediului Ubuntu

Când deschideți Ubuntu, sunteți într-un mediu Linux complet:

```
stud@HOSTNAME:~$
```

- `stud` — Numele vostru de utilizator
- `HOSTNAME` — Numele calculatorului vostru
- `~` — Directorul curent (folderul home: `/home/stud`)
- `$` — Prompt utilizator obișnuit (vs `#` pentru root)

### 5.4 Lista de Verificare

- [ ] Ubuntu apare în `wsl -l -v` cu VERSION 2
- [ ] Vă puteți autentifica ca utilizator `stud`
- [ ] Directorul home este `/home/stud`

---

## 6. Pasul 3: Instalare Docker în WSL

### 6.1 Ce Este Docker?

**Docker** este o platformă pentru dezvoltarea, livrarea și rularea aplicațiilor în containere. Un container este un pachet ușor, autonom, executabil care include tot ce este necesar pentru a rula software:

- Codul aplicației
- Mediul de rulare
- Unelte și biblioteci de sistem
- Setări de configurare

### 6.2 De Ce Docker în WSL (Nu Docker Desktop)?

| Aspect | Docker în WSL | Docker Desktop |
|--------|---------------|----------------|
| **Licențiere** | Gratuit pentru toate utilizările | Plătit pentru companii mari |
| **Performanță** | Performanță Linux nativă | Strat adițional de abstracție |
| **Învățare** | Mediu Docker Linux real | Comportament specific Windows |
| **Rețea** | Rețea Linux standard | Stack de rețea personalizat |

### 6.3 Pași de Instalare

#### Pasul 1: Deschideți Terminalul Ubuntu

Fie:
- Click pe "Ubuntu" în meniul Start, sau
- Tastați `wsl` în PowerShell

#### Pasul 2: Actualizați Pachetele de Sistem

```bash
sudo apt update && sudo apt upgrade -y
```

**Ce face aceasta:**
- `sudo`: Execută ca superutilizator (administrator)
- `apt update`: Reîmprospătează lista de pachete
- `apt upgrade -y`: Instalează toate actualizările disponibile (`-y` = da la toate)

**Durată așteptată:** 2-5 minute în funcție de viteza internetului.

#### Pasul 3: Instalați Docker și Docker Compose

```bash
sudo apt install -y docker.io docker-compose
```

**Pachete instalate:**
- `docker.io`: Runtime-ul pentru containere Docker
- `docker-compose`: Unealtă pentru definirea aplicațiilor multi-container

#### Pasul 4: Adăugați Utilizatorul în Grupul Docker

Implicit, Docker necesită `sudo`. Pentru a rula comenzi Docker fără `sudo`:

```bash
sudo usermod -aG docker $USER
```

**Explicația comenzii:**
- `usermod`: Modifică contul de utilizator
- `-aG docker`: Adaugă la grupul `docker`
- `$USER`: Numele de utilizator curent (se expandează la `stud`)

#### Pasul 5: Porniți Serviciul Docker

```bash
sudo service docker start
```

**Notă:** În WSL2, serviciile nu pornesc automat implicit. Vom configura acest lucru mai târziu.

#### Pasul 6: Aplicați Modificările de Grup

Pentru ca modificarea de grup să aibă efect:

```bash
newgrp docker
```

Sau delogați-vă și relogați-vă:
```bash
exit
wsl
```

#### Pasul 7: Verificați Instalarea

```bash
# Verificați versiunea Docker
docker --version

# Verificați versiunea Docker Compose
docker-compose --version

# Testați funcționalitatea Docker
docker run hello-world
```

**Output așteptat versiune Docker:**
```
Docker version 28.2.2, build e6534b4
```

**Output așteptat hello-world:**
```
Hello from Docker!
Acest mesaj arată că instalarea voastră pare să funcționeze corect.
...
```

### 6.4 Înțelegerea Componentelor Docker

```
┌─────────────────────────────────────────────────────────────┐
│                     Arhitectura Docker                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                                            │
│  │ Docker CLI  │ ◄── Comenzile pe care le tastați          │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │Docker Daemon│ ◄── Serviciu în fundal (dockerd)          │
│  │  (dockerd)  │                                            │
│  └──────┬──────┘                                            │
│         │                                                    │
│    ┌────┴────┬─────────────┐                                │
│    ▼         ▼             ▼                                │
│ ┌──────┐ ┌──────┐    ┌──────────┐                          │
│ │Imagini│ │Conta-│    │ Rețele   │                          │
│ │       │ │inere │    │          │                          │
│ └──────┘ └──────┘    └──────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### 6.5 Lista de Verificare

- [ ] `docker --version` arată versiunea 28.x sau mai mare
- [ ] `docker run hello-world` reușește fără `sudo`
- [ ] `docker ps` rulează fără erori de permisiuni

---

## 7. Pasul 4: Instalare Portainer CE

### 7.1 Ce Este Portainer?

**Portainer Community Edition** este o interfață de management ușoară care vă permite să gestionați ușor mediile Docker. Funcționalități incluse:

- Management vizual al containerelor
- Management imagini și volume
- Configurare rețele
- Vizualizare log-uri
- Acces la consolă container
- Deployment stacks cu docker-compose

### 7.2 De Ce Portainer?

Pentru scopuri educaționale, Portainer oferă:
- **Feedback vizual** asupra stărilor containerelor
- **Depanare ușoară** prin consola integrată
- **Acces la log-uri** fără complexitatea liniei de comandă
- **Vizualizare rețele** pentru înțelegerea comunicării între containere

### 7.3 Pași de Instalare

#### Pasul 1: Creați Volum Persistent

Volumele Docker persistă datele dincolo de ciclul de viață al containerului:

```bash
docker volume create portainer_data
```

**Ce face aceasta:** Creează un volum numit `portainer_data` care va stoca configurația, utilizatorii și setările Portainer.

#### Pasul 2: Deployați Containerul Portainer

```bash
docker run -d \
  -p 9000:9000 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

**Explicația comenzii:**

| Flag | Scop |
|------|------|
| `-d` | Rulează în mod detașat (fundal) |
| `-p 9000:9000` | Mapează portul 9000 din container la gazdă |
| `--name portainer` | Denumește containerul "portainer" |
| `--restart=always` | Repornește containerul dacă se oprește sau la reboot |
| `-v /var/run/docker.sock:...` | Dă Portainer acces la daemon-ul Docker |
| `-v portainer_data:/data` | Persistă datele Portainer |
| `portainer/portainer-ce:latest` | Folosește ultima imagine Portainer CE |

#### Pasul 3: Verificați Deployment-ul

```bash
docker ps
```

**Output așteptat:**
```
CONTAINER ID   IMAGE                           COMMAND        CREATED          STATUS          PORTS                                        NAMES
44b61d00ab18   portainer/portainer-ce:latest   "/portainer"   10 seconds ago   Up 9 seconds    8000/tcp, 9443/tcp, 0.0.0.0:9000->9000/tcp   portainer
```

### 7.4 Configurarea Inițială Portainer

> ⏱️ **Important:** Trebuie să finalizați configurarea inițială în 5 minute de la deployment!

#### Pasul 1: Accesați Portainer

Deschideți browserul Windows și navigați la:

```
http://localhost:9000
```

#### Pasul 2: Creați Contul de Administrator

Pe ecranul de configurare inițială:

| Câmp | Valoare |
|------|---------|
| Username | `stud` |
| Password | `studstudstud` |
| Confirm password | `studstudstud` |

Click **"Create user"**

#### Pasul 3: Conectați-vă la Docker Local

Pe ecranul "Environment Wizard":
1. Click **"Get Started"** pentru a folosi mediul local
2. Sau selectați **"Docker"** → **"Connect"** dacă este afișat

#### Pasul 4: Explorați Dashboard-ul

Ar trebui să vedeți acum dashboard-ul Portainer cu mediul Docker local conectat.

### 7.5 Prezentare Interfață Portainer

```
┌─────────────────────────────────────────────────────────────┐
│  PORTAINER.io                    [Notificări] [stud ▼]     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────────────────────────┐  │
│  │ Home        │  │  Environment: local                 │  │
│  │ Environments│  │  ┌─────────────────────────────────┐│  │
│  │             │  │  │ Containere: 1   Rulează: 1     ││  │
│  │ ─────────── │  │  │ Imagini: 2      Volume: 1      ││  │
│  │ Containere  │  │  │ Rețele: 3                       ││  │
│  │ Imagini     │  │  └─────────────────────────────────┘│  │
│  │ Rețele      │  │                                     │  │
│  │ Volume      │  │                                     │  │
│  │ Stacks      │  │                                     │  │
│  └─────────────┘  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 7.6 Lista de Verificare

- [ ] `docker ps` arată containerul portainer rulând
- [ ] http://localhost:9000 se încarcă în browserul Windows
- [ ] Vă puteți autentifica cu stud/studstudstud
- [ ] Dashboard-ul arată mediul Docker "local"

---

## 8. Pasul 5: Instalare Wireshark

### 8.1 Ce Este Wireshark?

**Wireshark** este cel mai important și mai utilizat analizor de protocoale de rețea din lume. Vă permite să:

- **Capturați** trafic de rețea în timp real
- **Inspectați** pachete la mai multe niveluri de protocol
- **Filtrați** traficul după diverse criterii
- **Analizați** comportamentul rețelei și depanați probleme
- **Exportați** capturi pentru analiză ulterioară

### 8.2 De Ce Wireshark pe Windows?

Instalăm Wireshark pe Windows (nu în WSL) deoarece:

1. **Performanță GUI:** Aplicație Windows nativă cu grafică mai bună
2. **Acces la Interfețe:** Acces direct la interfețele de rețea Windows
3. **Trafic WSL:** Interfața `vEthernet (WSL)` capturează tot traficul WSL
4. **Integrare:** Salvare și partajare ușoară a fișierelor pe Windows

### 8.3 Pași de Instalare

#### Pasul 1: Descărcați Wireshark

1. Vizitați: https://www.wireshark.org/download.html
2. Click pe **"Windows x64 Installer"**
3. Salvați fișierul installer

#### Pasul 2: Rulați Installer-ul

1. Double-click pe fișierul `.exe` descărcat
2. Click **"Da"** la promptul User Account Control
3. Urmați wizard-ul de instalare cu opțiunile implicite

#### Pasul 3: Instalați Npcap

> ⚠️ **Critic:** Npcap este necesar pentru captura pachetelor!

În timpul instalării Wireshark, vi se va cere să instalați Npcap:

1. Click **"Install"** când vi se cere Npcap
2. În installer-ul Npcap, asigurați-vă că aceste opțiuni sunt bifate:
   - ✅ **Install Npcap in WinPcap API-compatible Mode**
   - ✅ **Support raw 802.11 traffic (for wireless packet capture)**
3. Finalizați instalarea Npcap
4. Continuați cu instalarea Wireshark

#### Pasul 4: Finalizați Instalarea

1. Terminați installer-ul Wireshark
2. Opțional, reporniți calculatorul dacă vi se cere

### 8.4 Selectarea Interfeței Wireshark

Când deschideți Wireshark, veți vedea o listă de interfețe de rețea. Pentru capturarea traficului Docker/WSL:

| Interfață | Descriere | Folosire Pentru |
|-----------|-----------|-----------------|
| **vEthernet (WSL)** | Rețea virtuală WSL2 | Trafic containere Docker |
| **vEthernet (WSL) (Hyper-V firewall)** | Aceeași, cu firewall | Trafic containere Docker |
| Ethernet | Placă de rețea fizică | Trafic extern |
| Wi-Fi | Adaptor wireless | Trafic wireless extern |

### 8.5 Utilizare de Bază Wireshark

#### Pornirea unei Capturi

1. Deschideți Wireshark din meniul Start
2. Double-click pe interfața **"vEthernet (WSL)"**
3. Captura începe imediat

#### Filtre de Afișare Utile

| Filtru | Scop |
|--------|------|
| `icmp` | Arată doar pachetele ping (ICMP) |
| `tcp` | Arată doar pachetele TCP |
| `http` | Arată doar traficul HTTP |
| `dns` | Arată doar interogările DNS |
| `ip.addr == 172.17.0.2` | Filtrare după adresă IP |
| `tcp.port == 80` | Filtrare după port |

#### Oprirea unei Capturi

- Click pe butonul roșu **Stop** din bara de unelte
- Sau apăsați `Ctrl + E`

### 8.6 Lista de Verificare

- [ ] Wireshark pornește din meniul Start
- [ ] Interfețele de rețea sunt vizibile
- [ ] Interfața "vEthernet (WSL)" este prezentă
- [ ] Puteți porni și opri o captură

---

## 9. Pasul 6: Pachete Python

### 9.1 De Ce Python pentru Rețelistică?

Python este utilizat pe scară largă pentru automatizarea și analiza rețelelor:

- **docker**: Management programatic al containerelor
- **scapy**: Manipulare și creare pachete
- **dpkt**: Parsare rapidă a pachetelor

### 9.2 Cerințe Prealabile

Asigurați-vă că Python 3.11+ este instalat pe Windows:

```powershell
python --version
```

Dacă nu este instalat, descărcați de la: https://www.python.org/downloads/

### 9.3 Pași de Instalare

Deschideți PowerShell sau Command Prompt:

```powershell
# Instalați Docker SDK
pip install docker

# Instalați pachete de analiză rețea
pip install scapy dpkt

# Verificați instalarea
python -c "import docker; print('Docker SDK: OK')"
python -c "import scapy; print('Scapy: OK')"
python -c "import dpkt; print('dpkt: OK')"
```

### 9.4 Prezentare Pachete

#### docker (Python Docker SDK)

```python
import docker
client = docker.from_env()

# Listare containere
for container in client.containers.list():
    print(container.name, container.status)

# Rulare container
container = client.containers.run("alpine", "echo hello", detach=True)
```

#### scapy (Manipulare Pachete)

```python
from scapy.all import *

# Creare și trimitere pachet ping
packet = IP(dst="8.8.8.8")/ICMP()
response = sr1(packet, timeout=2)
print(response.summary())
```

#### dpkt (Parsare Pachete)

```python
import dpkt

# Parsare fișier pcap
with open('capture.pcap', 'rb') as f:
    pcap = dpkt.pcap.Reader(f)
    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        print(eth)
```

### 9.5 Lista de Verificare

- [ ] `pip show docker` afișează informații despre pachet
- [ ] `pip show scapy` afișează informații despre pachet
- [ ] `pip show dpkt` afișează informații despre pachet
- [ ] Instrucțiunile import funcționează fără erori

---

## 10. Pasul 7: Configurare Auto-start (Opțional)

### 10.1 De Ce Auto-start?

Implicit, WSL2 nu pornește serviciile automat. De fiecare dată când deschideți Ubuntu, ar trebui să:

```bash
sudo service docker start
```

Configurarea auto-start elimină acest pas manual.

### 10.2 Pași de Configurare

#### Pasul 1: Adăugați Auto-start în Profilul Bash

Deschideți terminalul Ubuntu și executați:

```bash
cat >> ~/.bashrc << 'EOF'

# Auto-start serviciu Docker
if ! pgrep -x "dockerd" > /dev/null; then
    sudo service docker start > /dev/null 2>&1
fi
EOF
```

**Ce face aceasta:**
- Adaugă cod la `~/.bashrc` (executat la fiecare deschidere de terminal)
- Verifică dacă `dockerd` rulează (`pgrep`)
- Dacă nu rulează, pornește serviciul Docker

#### Pasul 2: Permiteți Pornirea Docker Fără Parolă

Creați o excepție sudoers:

```bash
echo 'stud ALL=(ALL) NOPASSWD: /usr/sbin/service docker start' | sudo tee /etc/sudoers.d/docker-start
sudo chmod 440 /etc/sudoers.d/docker-start
```

**Ce face aceasta:**
- Creează fișierul `/etc/sudoers.d/docker-start`
- Permite utilizatorului `stud` să ruleze `service docker start` fără parolă
- Setează permisiuni securizate (doar citire pentru root și sudoers)

#### Pasul 3: Testați Auto-start

```powershell
# În PowerShell, opriți WSL complet
wsl --shutdown

# Redeschideți Ubuntu
wsl

# Docker ar trebui să pornească automat
docker ps
```

### 10.3 Lista de Verificare

- [ ] Docker pornește automat când deschideți Ubuntu
- [ ] Niciun prompt de parolă pentru serviciul Docker
- [ ] `docker ps` funcționează imediat după deschiderea Ubuntu

---

## 11. Verificare Finală

### 11.1 Test Complet al Sistemului

#### Test 1: Docker și Portainer

```bash
# În terminalul Ubuntu
docker ps
```

**Așteptat:** Containerul Portainer rulând.

#### Test 2: Captură Wireshark

1. Deschideți Wireshark pe Windows
2. Porniți captura pe **vEthernet (WSL)**
3. În Ubuntu, rulați:

```bash
docker run --rm alpine ping -c 5 8.8.8.8
```

4. În Wireshark, aplicați filtrul: `icmp`
5. Verificați că vedeți pachetele ICMP Echo Request și Reply

**Output Așteptat Wireshark:**

| Nr. | Timp | Sursă | Destinație | Protocol | Info |
|-----|------|-------|------------|----------|------|
| 1 | 0.000 | 172.27.159.165 | 8.8.8.8 | ICMP | Echo request |
| 2 | 0.087 | 8.8.8.8 | 172.27.159.165 | ICMP | Echo reply |

#### Test 3: Integrare Python

```powershell
# În PowerShell
python -c "import docker; c = docker.from_env(); print(f'Containere: {len(c.containers.list())}')"
```

**Așteptat:** `Containere: 1` (sau mai multe)

### 11.2 Sumar Componente

| Component | Versiune | Verificare Status |
|-----------|----------|-------------------|
| WSL2 | 2.x | `wsl --status` |
| Ubuntu | 22.04 LTS | `lsb_release -a` |
| Docker | 28.2.2 | `docker --version` |
| Docker Compose | 1.29.x | `docker-compose --version` |
| Portainer | 2.33.6 LTS | http://localhost:9000 |
| Wireshark | 4.4.x | Lansare aplicație |
| Python docker | 7.1.0 | `pip show docker` |
| Python scapy | 2.7.0 | `pip show scapy` |
| Python dpkt | 1.9.8 | `pip show dpkt` |

### 11.3 Script Rapid de Verificare

Creați și rulați acest script de verificare:

```bash
#!/bin/bash
echo "=== Status WSL ==="
wsl.exe --status 2>/dev/null || echo "Rulați din Windows"

echo ""
echo "=== Versiune Ubuntu ==="
lsb_release -d

echo ""
echo "=== Versiune Docker ==="
docker --version

echo ""
echo "=== Versiune Docker Compose ==="
docker-compose --version

echo ""
echo "=== Containere Active ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "=== Status Portainer ==="
docker ps --filter name=portainer --format "{{.Status}}"

echo ""
echo "=== Rețele Docker ==="
docker network ls

echo ""
echo "✅ Toate verificările complete!"
```

---

## 12. Depanare

### 12.1 Probleme WSL

#### "WSL 2 necesită o actualizare a componentei kernel"

```powershell
wsl --update
```

#### "Vă rugăm activați funcția Virtual Machine Platform"

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
Reporniți calculatorul după.

#### WSL nu pornește

```powershell
# Resetați WSL
wsl --shutdown
wsl
```

### 12.2 Probleme Docker

#### "Nu se poate conecta la daemon-ul Docker"

```bash
# Porniți serviciul Docker
sudo service docker start

# Verificați dacă dockerd rulează
ps aux | grep dockerd
```

#### "Permisiune refuzată la conectarea la socket-ul daemon-ului Docker"

```bash
# Adăugați utilizatorul în grupul docker
sudo usermod -aG docker $USER

# Aplicați modificările
newgrp docker
# Sau delogați-vă și relogați-vă
```

#### "docker: command not found" în PowerShell

Aceasta este normal. Docker este instalat în WSL, nu Windows. Folosiți:

```powershell
wsl docker ps
```

### 12.3 Probleme Portainer

#### Nu pot accesa http://localhost:9000

1. Verificați dacă containerul rulează:
```bash
docker ps | grep portainer
```

2. Dacă nu rulează, verificați log-urile:
```bash
docker logs portainer
```

3. Reporniți Portainer:
```bash
docker restart portainer
```

#### "Portainer a fost deja inițializat"

Dacă ați ratat fereastra de 5 minute:

```bash
# Ștergeți Portainer și volumul
docker stop portainer
docker rm portainer
docker volume rm portainer_data

# Redeployați
docker volume create portainer_data
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

### 12.4 Probleme Wireshark

#### Nu se văd interfețele

- Asigurați-vă că Npcap este instalat
- Rulați Wireshark ca Administrator
- Reinstalați Npcap de la https://npcap.com/

#### "vEthernet (WSL)" nu apare

- WSL trebuie să ruleze
- Încercați: `wsl` în PowerShell, apoi reporniți Wireshark

#### Nu se capturează trafic

- Asigurați-vă că captura este pe interfața corectă
- Generați trafic: `docker run --rm alpine ping -c 3 8.8.8.8`
- Verificați că filtrul de afișare nu este prea restrictiv

---

## 13. Fișă de Referință Rapidă

### Comenzi Esențiale

```bash
# Management WSL (PowerShell)
wsl --status           # Verifică status WSL
wsl --shutdown         # Oprește toate instanțele WSL
wsl                    # Deschide distribuția implicită
wsl -l -v              # Listează distribuțiile

# Docker (Terminal Ubuntu)
docker ps              # Listează containerele active
docker ps -a           # Listează toate containerele
docker images          # Listează imaginile
docker logs <n>        # Vizualizează log-uri container
docker exec -it <n> sh # Shell în container
docker stop <n>        # Oprește container
docker rm <n>          # Șterge container

# Management Servicii (Terminal Ubuntu)
sudo service docker start   # Pornește Docker
sudo service docker status  # Verifică status Docker
sudo service docker stop    # Oprește Docker
```

### URL-uri Importante

| Serviciu | URL |
|----------|-----|
| Portainer | http://localhost:9000 |
| Docker Docs | https://docs.docker.com/ |
| Wireshark Docs | https://www.wireshark.org/docs/ |
| WSL Docs | https://learn.microsoft.com/en-us/windows/wsl/ |

### Credențiale

| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | stud | stud |
| Portainer | stud | studstudstud |

---

## 🎉 Configurare Completă!

Mediul vostru de laborator este complet configurat. Acum puteți:

- ✅ Rula experimente de rețea izolate cu containere Docker
- ✅ Captura și analiza traficul cu Wireshark
- ✅ Gestiona containerele prin interfața web Portainer
- ✅ Automatiza sarcini de rețea cu Python

**Pași Următori:**
- Explorați interfața Portainer
- Încercați să creați rețele Docker personalizate
- Exersați filtrarea în Wireshark
- Rulați primul exercițiu de laborator

---

*Laborator Rețele de Calculatoare — ASE București, CSIE*  
*Versiune documentație: Ianuarie 2026*
