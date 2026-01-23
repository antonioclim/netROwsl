# 🖧 Rețele de Calculatoare — Kit-uri Complete de Laborator (Ediția WSL)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-28.2.2+-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![WSL2](https://img.shields.io/badge/WSL2-Ubuntu_22.04_LTS-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![Wireshark](https://img.shields.io/badge/Wireshark-4.4.x-1679A7?style=for-the-badge&logo=wireshark&logoColor=white)](https://wireshark.org)
[![Portainer](https://img.shields.io/badge/Portainer-2.33.6_LTS-13BEF9?style=for-the-badge&logo=portainer&logoColor=white)](https://portainer.io)
[![Licență](https://img.shields.io/badge/Licență-Educațională_Restrictivă-red?style=for-the-badge)](LICENSE.md)

> **© 2019–2026 Antonio Clim, Andrei Toma** | by Revolvix

---

## ⚡ QUICK START — Pornire în 5 minute

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# CLONEAZA_REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════════
git clone https://github.com/antonioclim/netROwsl.git
cd netROwsl

# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGHEAZA_LA_SAPTAMANA
# ═══════════════════════════════════════════════════════════════════════════════
cd 01roWSL  # sau orice altă săptămână (01-14)

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICA_MEDIUL
# ═══════════════════════════════════════════════════════════════════════════════
python3 setup/verifica_mediu.py

# ═══════════════════════════════════════════════════════════════════════════════
# PORNESTE_LABORATORUL
# ═══════════════════════════════════════════════════════════════════════════════
python3 scripts/porneste_lab.py

# ═══════════════════════════════════════════════════════════════════════════════
# ACCESEAZA_PORTAINER
# ═══════════════════════════════════════════════════════════════════════════════
# Deschide în browser: http://localhost:9000
# Credențiale: stud / studstudstud
```

### Credențiale Rapide

| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| **Ubuntu WSL** | `stud` | `stud` |
| **Portainer** | `stud` | `studstudstud` |

> 💭 **PREDICȚIE:** După `python3 scripts/porneste_lab.py`, câte containere crezi că vor porni pentru Săptămâna 1?


**Disciplină:** Rețele de Calculatoare (25.0205IF3.2-0003)  
**Program de studiu:** Informatică Economică, Anul III, Semestrul 2  
**Instituție:** Academia de Studii Economice din București (ASE), Facultatea de Cibernetică, Statistică și Informatică Economică (CSIE)  
**An universitar:** 2025–2026

---

## ⚠️ IMPORTANT: Două Repository-uri Disponibile

Materialele de laborator sunt disponibile în **două limbi**, organizate în repository-uri separate:

### Repository-uri Principale (Ediția WSL — Recomandate)

| Repository | Limbă | URL | Convenție Denumire |
|------------|-------|-----|-------------------|
| **netENwsl** | 🇬🇧 Engleză | https://github.com/antonioclim/netENwsl | `<N>enWSL` (ex: `1enWSL`, `14enWSL`) |
| **netROwsl** | 🇷🇴 Română | https://github.com/antonioclim/netROwsl | `<NN>roWSL` (ex: `01roWSL`, `14roWSL`) |

### Repository-uri Beta (Ediția VM Linux — Pentru Utilizatori Avansați)

| Repository | Limbă | URL | Status |
|------------|-------|-----|--------|
| **NETro** | 🇷🇴 Română | https://github.com/antonioclim/NETro | Beta — necesită VM Linux |
| **netEN** | 🇬🇧 Engleză | https://github.com/antonioclim/netEN | Beta — necesită VM Linux |

### Comparație Detaliată: Ediția WSL vs Ediția VM (Beta)

| Caracteristică | netROwsl / netENwsl (WSL) | NETro / netEN (Beta VM) |
|----------------|---------------------------|-------------------------|
| **Mediu de Execuție** | WSL2 + Docker + Portainer | VM Linux + Mininet |
| **Sistem de Operare Gazdă** | Windows 10/11 nativ | Orice OS cu VM (VirtualBox/VMware) |
| **Convenție Denumire** | `<NN>roWSL` / `<N>enWSL` | `WEEK<N>` |
| **Automatizare** | Scripturi Python | Makefile |
| **Interfață Vizuală** | Portainer (port 9000) | Doar CLI |
| **Simulare Rețea** | Rețele Docker bridge | Mininet (topologii complexe) |
| **Captură Trafic** | Wireshark nativ Windows | tcpdump în VM |
| **Complexitate Setup** | ⭐⭐ Accesibilă | ⭐⭐⭐⭐ Avansată |
| **Diagrame PlantUML** | ✗ | ✓ |
| **Slide-uri Prezentare** | ✗ | ✓ |
| **Completitudine** | 14 kit-uri complete | 14 săptămâni (structură variabilă) |
| **Documentație** | 2.400+ linii | ~1.000 linii |
| **Consum Resurse** | ~500MB RAM bază | ~2-4GB RAM (VM) |

### Avantajele Ediției WSL (Recomandate pentru Studenți)

1. **Fără VM separată** — Rulează direct pe Windows fără overhead de virtualizare
2. **Management vizual** — Portainer oferă interfață web pentru containere
3. **Scripturi Python moderne** — Mai ușor de înțeles decât Makefile
4. **Integrare Wireshark nativă** — Captură directă pe Windows
5. **Structură consistentă** — Toate cele 14 kit-uri au aceeași organizare
6. **Documentație extinsă** — README detaliat cu troubleshooting complet

### Când să Alegi Ediția Beta (VM)?

- Ai experiență cu Linux și preferi CLI
- Ai nevoie de topologii Mininet complexe
- Vrei să exersezi administrare Linux în VM
- Sistemul tău nu suportă WSL2

**Această documentație acoperă repository-urile WSL (netROwsl/netENwsl)**, cu instrucțiuni specifice pentru fiecare variantă lingvistică.

---

## 📋 Cuprins General

### Partea I — Introducere și Prezentare
- [1. Prezentare generală](#1-prezentare-generală)
- [2. Filosofia pedagogică](#2-filosofia-pedagogică)
- [3. Arhitectura sistemului](#3-arhitectura-sistemului)
- [4. Structura repository-urilor](#4-structura-repository-urilor)

### Partea II — Configurarea Mediului de Lucru
- [5. Cerințe de sistem](#5-cerințe-de-sistem)
- [6. Credențiale standard](#6-credențiale-standard)
- [7. Instalare pas cu pas](#7-instalare-pas-cu-pas)
- [8. Verificarea instalării](#8-verificarea-instalării)

### Partea III — Curricula Săptămânală Detaliată
- [9. Ghid rapid de pornire a laboratoarelor](#9-ghid-rapid-de-pornire-a-laboratoarelor)
- [10. Clonarea individuală a fiecărei săptămâni](#10-clonarea-individuală-a-fiecărei-săptămâni)
- [11. Săptămâna 1: Fundamente ale rețelelor](#11-săptămâna-1-fundamente-ale-rețelelor)
- [12. Săptămâna 2: Modele arhitecturale și programare socket](#12-săptămâna-2-modele-arhitecturale-și-programare-socket)
- [13. Săptămâna 3: Modele avansate de programare în rețea](#13-săptămâna-3-modele-avansate-de-programare-în-rețea)
- [14. Săptămâna 4: Nivelurile fizic și legătură de date](#14-săptămâna-4-nivelurile-fizic-și-legătură-de-date)
- [15. Săptămâna 5: Nivelul rețea și adresare IP](#15-săptămâna-5-nivelul-rețea-și-adresare-ip)
- [16. Săptămâna 6: NAT/PAT, protocoale suport și SDN](#16-săptămâna-6-natpat-protocoale-suport-și-sdn)
- [17. Săptămâna 7: Interceptare pachete, filtrare și securitate](#17-săptămâna-7-interceptare-pachete-filtrare-și-securitate)
- [18. Săptămâna 8: Nivelul transport, HTTP și proxy invers](#18-săptămâna-8-nivelul-transport-http-și-proxy-invers)
- [19. Săptămâna 9: Nivelurile sesiune și prezentare](#19-săptămâna-9-nivelurile-sesiune-și-prezentare)
- [20. Săptămâna 10: Protocoale de nivel aplicație](#20-săptămâna-10-protocoale-de-nivel-aplicație)
- [21. Săptămâna 11: Echilibrarea încărcării (Load Balancing)](#21-săptămâna-11-echilibrarea-încărcării-load-balancing)
- [22. Săptămâna 12: Protocoale email și RPC](#22-săptămâna-12-protocoale-email-și-rpc)
- [23. Săptămâna 13: IoT și securitatea rețelelor](#23-săptămâna-13-iot-și-securitatea-rețelelor)
- [24. Săptămâna 14: Recapitulare integrată și evaluare](#24-săptămâna-14-recapitulare-integrată-și-evaluare)

### Partea IV — Referințe și Suport
- [25. Structura standard a kit-urilor](#25-structura-standard-a-kit-urilor)
- [26. Planul de adresare IP](#26-planul-de-adresare-ip)
- [27. Convenții de alocare porturi](#27-convenții-de-alocare-porturi)
- [28. Tehnologii și instrumente utilizate](#28-tehnologii-și-instrumente-utilizate)
- [29. Ghid complet de depanare](#29-ghid-complet-de-depanare)
- [30. Comenzi esențiale — Fișă de referință rapidă](#30-comenzi-esențiale--fișă-de-referință-rapidă)
- [31. Exerciții de nivel superior (EVALUATE & CREATE)](#31-exerciții-de-nivel-superior-evaluate--create)
- [32. Ghid Live Coding pentru Instructori](#32-ghid-live-coding-pentru-instructori)
- [33. FAQ — Întrebări Frecvente](#33-faq--întrebări-frecvente)
- [34. Licență](#34-licență)

---

# PARTEA I — INTRODUCERE ȘI PREZENTARE

---

## 1. Prezentare generală

Acest repository conține **kit-uri complete de laborator** pentru disciplina **Rețele de Calculatoare**, acoperind exhaustiv toate cele **14 săptămâni** ale semestrului universitar. Materialele sunt proiectate și optimizate specific pentru implementare pe sisteme **Windows 10/11** utilizând **WSL2** (Windows Subsystem for Linux) cu containerizare **Docker** și management vizual prin **Portainer CE**, oferind studenților și profesorilor un mediu de laborator portabil, reproductibil, izolat și profesional.

### 1.1 Ce oferă acest repository?

Fiecare kit săptămânal constituie o **unitate educațională autonomă și completă**, cuprinzând:

| Componentă | Descriere |
|------------|-----------|
| **📚 Documentație structurată** | Fundamentele teoretice articulate clar, obiective de învățare explicite, ghiduri pas cu pas |
| **🐍 Exerciții Python** | Progresie graduală de la implementări ghidate la rezolvare independentă de probleme complexe |
| **🐳 Medii Docker Compose** | Topologii de rețea multi-container pre-configurate, gata de utilizare |
| **🖥️ Interfață Portainer** | Management vizual al containerelor și rețelelor Docker |
| **🧪 Framework-uri de testare** | Validare automată a completării exercițiilor și integrității mediului |
| **📡 Facilități de captură** | Scripturi pentru captură de pachete și analiză forensică a protocoalelor |
| **🦈 Ghiduri Wireshark** | Filtre specifice pentru fiecare protocol și săptămână |
| **📋 Fișe de referință** | Comenzi CLI esențiale consolidate pentru acces rapid |
| **📝 Teme pentru acasă** | Exerciții suplimentare cu soluții de referință pentru studiu individual |

### 1.2 Metodologia de învățare

Abordarea pedagogică pune accent pe **învățarea prin observație și experimentare directă**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CICLUL DE ÎNVĂȚARE EXPERIENȚIALĂ                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐            │
│    │  CONSTRUIEȘTE │ ──▶ │   GENEREAZĂ   │ ──▶ │   CAPTEAZĂ   │            │
│    │   servicii    │      │    trafic     │      │   pachete    │            │
│    │   de rețea    │      │    de rețea   │      │   PCAP       │            │
│    └──────────────┘      └──────────────┘      └──────┬───────┘            │
│           ▲                                           │                     │
│           │                                           ▼                     │
│    ┌──────┴───────┐                          ┌──────────────┐              │
│    │   APLICĂ     │ ◀────────────────────── │   ANALIZEAZĂ  │              │
│    │  cunoștințe  │                          │  protocoale   │              │
│    │   noi        │                          │  și comportam.│              │
│    └──────────────┘                          └──────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Această metodologie face punte între **modelele teoretice** și **realitatea operațională**, pregătind studenții pentru cariere în:

- 🌐 Ingineria rețelelor de calculatoare
- 🔒 Analiza și auditul de securitate cibernetică
- 🏗️ Dezvoltarea sistemelor distribuite
- ☁️ Administrarea infrastructurilor cloud
- 🔧 DevOps și Site Reliability Engineering

### 1.3 Pentru cine este acest repository?

| Public țintă | Beneficii |
|--------------|-----------|
| **Studenți** | Materiale complete pentru învățare independentă, exerciții practice, soluții de referință |
| **Profesori/Asistenți** | Kit-uri gata de utilizare pentru laborator, structură consistentă, framework de evaluare |
| **Autodidacți** | Curriculum complet de networking, de la fundamentals la advanced topics |
| **Profesioniști** | Refresh de concepte, sandbox pentru experimentare, referință tehnică |

---

## 2. Filosofia pedagogică

### 2.1 Modelul de progresie în învățare

Cursul urmează o **explorare arhitecturală de jos în sus** aliniată cu modelele de referință OSI/TCP-IP, începând cu concepte fundamentale și instrumente de diagnoză înainte de a urca prin stiva de protocoale:

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    TRAIECTORIA DE ÎNVĂȚARE — SEMESTRUL 2                       ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  Săpt. 14 ─┬─ INTEGRARE    ════════════════════════════════════════════════  ║
║            │                                                                  ║
║  Săpt. 13 ─┤                ┌───────────────────────────────────────────┐    ║
║  Săpt. 12 ─┤  NIVELUL       │  • IoT & MQTT (publish/subscribe)        │    ║
║  Săpt. 11 ─┤  APLICAȚIE     │  • Email (SMTP, POP3, IMAP)              │    ║
║  Săpt. 10 ─┘                │  • RPC (JSON-RPC, XML-RPC, gRPC)         │    ║
║                             │  • HTTP/HTTPS, REST APIs, DNS, SSH       │    ║
║                             │  • Load Balancing                        │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 9  ─┬─ SESIUNE &     ┌───────────────────────────────────────────┐    ║
║            │  PREZENTARE    │  • FTP Active/Passive modes               │    ║
║            │                │  • Serializare binară                     │    ║
║            │                │  • Gestionare stare sesiune               │    ║
║            └────────────────└───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 8  ─── TRANSPORT     ┌───────────────────────────────────────────┐    ║
║                             │  • TCP 3-way handshake                    │    ║
║                             │  • HTTP/1.1 server implementation         │    ║
║                             │  • Nginx reverse proxy & load balancing   │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 7  ─── SECURITATE    ┌───────────────────────────────────────────┐    ║
║              & FILTRARE     │  • iptables firewall rules                │    ║
║                             │  • Packet filtering (DROP/REJECT)         │    ║
║                             │  • Port scanning & reconnaissance         │    ║
║                             │  • tcpdump, tshark, Wireshark             │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 5  ─┬─ NIVELUL       ┌───────────────────────────────────────────┐    ║
║  Săpt. 6  ─┘  REȚEA         │  • Adresare IP, CIDR, VLSM                │    ║
║                             │  • NAT/PAT, SNAT, DNAT                    │    ║
║                             │  • ARP, DHCP, ICMP, NDP                   │    ║
║                             │  • Software-Defined Networking (SDN)      │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 4  ─── LEGĂTURĂ      ┌───────────────────────────────────────────┐    ║
║              DE DATE        │  • Ethernet frames, MAC addressing        │    ║
║                             │  • CRC32 error detection                  │    ║
║                             │  • Binary protocol design                 │    ║
║                             │  • Python struct pack/unpack              │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
║  Săpt. 1  ─┬─ FUNDAMENTE    ┌───────────────────────────────────────────┐    ║
║  Săpt. 2  ─┤                │  • CLI diagnostic tools (ip, ss, ping)    │    ║
║  Săpt. 3  ─┘                │  • Socket programming (TCP/UDP)           │    ║
║                             │  • Concurrent servers (threading)         │    ║
║                             │  • Packet capture & analysis              │    ║
║                             └───────────────────────────────────────────┘    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 2.2 Cadrul de dezvoltare a competențelor (Taxonomia Anderson-Bloom)

Fiecare sesiune de laborator vizează niveluri cognitive specifice, progresând de la simplu la complex:

| Nivel cognitiv | Verb cheie | Activități tipice | Metode de evaluare |
|----------------|------------|-------------------|-------------------|
| **1. A REȚINE** | Reamintește, Identifică, Listează | Sintaxa comenzilor, câmpurile protocoalelor, definițiile conceptelor | Completarea fișelor de referință, quiz-uri rapide |
| **2. A ÎNȚELEGE** | Explică, Descrie, Compară | Comportamentul protocoalelor, pattern-uri de trafic, fluxuri de date | Analiză scrisă, explicații verbale, diagrame |
| **3. A APLICA** | Demonstrează, Implementează, Utilizează | Folosirea instrumentelor în scenarii noi, adaptarea scripturilor | Implementări funcționale, log-uri, rapoarte |
| **4. A ANALIZA** | Examinează, Diferențiază, Investighează | Capturile de pachete, workflow-uri de depanare, root cause analysis | Adnotări PCAP, rapoarte cauză principală |
| **5. A EVALUA** | Evaluează, Critică, Justifică | Postura de securitate, trade-off-uri de design, alegeri arhitecturale | Recomandări tehnice, audituri, peer review |
| **6. A CREA** | Proiectează, Construiește, Dezvoltă | Implementări de protocoale, instrumente personalizate, soluții originale | Cod original, documentație, prezentări |

---

## 3. Arhitectura sistemului

### 3.1 De ce WSL2 + Docker (și nu Docker Desktop)?

Alegerea arhitecturii **WSL2 + Docker nativ în Ubuntu** (în loc de Docker Desktop) este fundamentată pe mai multe avantaje semnificative pentru mediul educațional:

| Criteriu | WSL2 + Docker nativ | Docker Desktop |
|----------|---------------------|----------------|
| **🚀 Performanță** | Kernel Linux nativ, I/O rapid | Overhead de virtualizare suplimentar |
| **💾 Consum resurse** | ~500MB bază, eficient | ~2GB+ bază, consum RAM ridicat |
| **🌐 Fidelitate rețea** | Stivă de rețea Linux completă | Abstractizare și limitări |
| **📁 Integrare fișiere** | Acces direct la sistemul de fișiere Windows | Montări cu overhead |
| **💰 Licențiere** | Complet gratuit | Restricții pentru întreprinderi (>250 angajați) |
| **🎓 Valoare educativă** | Competențe Linux reale, transferabile | Abstracție care ascunde complexitatea |
| **🔧 Control** | Control complet asupra configurației | Configurație limitată |

### 3.2 Diagrama arhitecturii complete

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              WINDOWS 10/11 HOST                                  │
│                                                                                  │
│  ┌────────────────┐   ┌────────────────┐   ┌────────────────┐   ┌────────────┐ │
│  │   Wireshark    │   │    Browser     │   │  PowerShell/   │   │  VS Code   │ │
│  │  (Analizor     │   │   (Portainer   │   │   Terminal     │   │   (IDE)    │ │
│  │   nativ Win)   │   │    :9000)      │   │   Windows      │   │            │ │
│  └───────┬────────┘   └───────┬────────┘   └───────┬────────┘   └─────┬──────┘ │
│          │                    │                    │                  │         │
│          │     ┌──────────────┴──────────────┬─────┴──────────────────┘         │
│          │     │                             │                                   │
│          ▼     ▼                             ▼                                   │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                    vEthernet (WSL) — Rețea Virtuală                        │  │
│  │              Interfața de bridge între Windows și Linux                    │  │
│  │                     IP dinamic: 172.x.x.x                                  │  │
│  └───────────────────────────────────────────┬───────────────────────────────┘  │
│                                              │                                   │
│  ┌───────────────────────────────────────────┴───────────────────────────────┐  │
│  │                         WSL2 (Mașină Virtuală Lightweight)                 │  │
│  │  ┌─────────────────────────────────────────────────────────────────────┐  │  │
│  │  │                        Ubuntu 22.04 LTS                              │  │  │
│  │  │                   Utilizator: stud | Parolă: stud                    │  │  │
│  │  │  ┌───────────────────────────────────────────────────────────────┐  │  │  │
│  │  │  │                      Docker Engine 28.2.2                      │  │  │  │
│  │  │  │                                                                │  │  │  │
│  │  │  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │  │  │  │
│  │  │  │   │  Container  │  │  Container  │  │     Portainer CE    │  │  │  │  │
│  │  │  │   │   Week N    │  │   Servicii  │  │     2.33.6 LTS      │  │  │  │  │
│  │  │  │   │    Lab      │  │   Backend   │  │  stud/studstudstud  │  │  │  │  │
│  │  │  │   │             │  │             │  │                     │  │  │  │  │
│  │  │  │   │ Porturi:    │  │ Porturi:    │  │ Port:               │  │  │  │  │
│  │  │  │   │ 9001-9099   │  │ 8080-8089   │  │ 9000 (HTTP)         │  │  │  │  │
│  │  │  │   │ (NU 9000!)  │  │             │  │ ⚠️ REZERVAT!        │  │  │  │  │
│  │  │  │   └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │  │  │  │
│  │  │  │          │                │                    │             │  │  │  │
│  │  │  │   ┌──────┴────────────────┴────────────────────┴──────────┐  │  │  │  │
│  │  │  │   │              Docker Bridge Network                     │  │  │  │  │
│  │  │  │   │        weekN_network (subnet dedicat/săptămână)       │  │  │  │  │
│  │  │  │   │              172.20.x.0/24 sau 10.x.x.0/24            │  │  │  │  │
│  │  │  │   └────────────────────────────────────────────────────────┘  │  │  │  │
│  │  │  │                                                                │  │  │  │
│  │  │  └────────────────────────────────────────────────────────────────┘  │  │  │
│  │  │                                                                       │  │  │
│  │  │  ┌─────────────────────────────────────────────────────────────────┐ │  │  │
│  │  │  │  INSTRUMENTE INSTALATE:                                          │ │  │  │
│  │  │  │  Python 3.11+ │ tcpdump │ tshark │ netcat │ nmap │ iperf3       │ │  │  │
│  │  │  │  git │ curl │ wget │ vim │ nano │ htop │ tree                   │ │  │  │
│  │  │  └─────────────────────────────────────────────────────────────────┘ │  │  │
│  │  │                                                                       │  │  │
│  │  └───────────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Fluxul de date în rețea

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         FLUXUL DE TRAFIC ÎN LABORATOR                            │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────┐                                              ┌─────────────┐   │
│  │  Container  │ ◀──────── Docker Bridge Network ──────────▶ │  Container  │   │
│  │     A       │           (comunicare internă)               │     B       │   │
│  └──────┬──────┘                                              └──────┬──────┘   │
│         │                                                            │          │
│         └──────────────────────┬─────────────────────────────────────┘          │
│                                │                                                 │
│                                ▼                                                 │
│                    ┌───────────────────────┐                                    │
│                    │   Docker NAT Gateway   │                                    │
│                    │   (docker0 / bridge)   │                                    │
│                    └───────────┬───────────┘                                    │
│                                │                                                 │
│                                ▼                                                 │
│                    ┌───────────────────────┐                                    │
│                    │   WSL2 eth0 Interface  │                                    │
│                    │   (IP dinamic Linux)   │                                    │
│                    └───────────┬───────────┘                                    │
│                                │                                                 │
│    ══════════════════════════════════════════════════════════════════════════   │
│                    GRANIȚA WSL2 ↔ WINDOWS                                        │
│    ══════════════════════════════════════════════════════════════════════════   │
│                                │                                                 │
│                                ▼                                                 │
│         ┌──────────────────────────────────────────────────────────────┐        │
│         │                vEthernet (WSL)                                │        │
│         │    ← Wireshark capturează aici traficul WSL →                │        │
│         └──────────────────────────────────────────────────────────────┘        │
│                                │                                                 │
│                                ▼                                                 │
│                    ┌───────────────────────┐                                    │
│                    │  Windows Network Stack │                                    │
│                    │   (Internet Access)    │                                    │
│                    └───────────────────────┘                                    │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Structura repository-urilor

### 4.1 Repository Engleză (netENwsl)

```
netENwsl/
│
├── 📁 00BEFOREanythingELSE/           # ⚠️ CITIȚI ÎNTÂI! Cerințe preliminare
│   ├── PREREQUISITES_EN.html          # Ghid interactiv HTML
│   ├── PrerequisitesEN.md             # Ghid Markdown
│   └── wireshark_capture_example.png  # Screenshot exemplu
│
├── 📁 1enWSL/                         # Săptămâna 1: Fundamente rețele
├── 📁 2enWSL/                         # Săptămâna 2: Modele & Socket-uri
├── 📁 3enWSL/                         # Săptămâna 3: Programare rețea
├── 📁 4enWSL/                         # Săptămâna 4: Fizic & Legătură date
├── 📁 5enWSL/                         # Săptămâna 5: Adresare IP & Subrețele
├── 📁 6enWSL/                         # Săptămâna 6: NAT/PAT, SDN
├── 📁 7enWSL/                         # Săptămâna 7: Filtrare & Securitate
├── 📁 8enWSL/                         # Săptămâna 8: Transport & HTTP
├── 📁 9enWSL/                         # Săptămâna 9: Sesiune & Prezentare
├── 📁 10enWSL/                        # Săptămâna 10: Protocoale Aplicație
├── 📁 11enWSL/                        # Săptămâna 11: Load Balancing
├── 📁 12enWSL/                        # Săptămâna 12: Email & RPC
├── 📁 13enWSL/                        # Săptămâna 13: IoT & Securitate
├── 📁 14enWSL/                        # Săptămâna 14: Recapitulare
│
├── 📄 README.md                       # Documentație principală (EN)
└── 📄 LICENSE                         # Licență MIT
```

### 4.2 Repository Română (netROwsl)

```
netROwsl/
│
├── 📁 00-startAPPENDIX(week0)/               # ⚠️ CITIȚI ÎNTÂI! Cerințe preliminare
│   ├── CERINTE_PRELIMINARE_RO.html    # Ghid interactiv HTML
│   ├── CerintePrelimRO.md             # Ghid Markdown
│   └── exemplu_captura_wireshark.png  # Screenshot exemplu
│
├── 📁 01roWSL/                        # Săptămâna 1: Fundamente rețele
├── 📁 02roWSL/                        # Săptămâna 2: Modele & Socket-uri
├── 📁 03roWSL/                        # Săptămâna 3: Programare rețea
├── 📁 04roWSL/                        # Săptămâna 4: Fizic & Legătură date
├── 📁 05roWSL/                        # Săptămâna 5: Adresare IP & Subrețele
├── 📁 06roWSL/                        # Săptămâna 6: NAT/PAT, SDN
├── 📁 07roWSL/                        # Săptămâna 7: Filtrare & Securitate
├── 📁 08roWSL/                        # Săptămâna 8: Transport & HTTP
├── 📁 09roWSL/                        # Săptămâna 9: Sesiune & Prezentare
├── 📁 10roWSL/                        # Săptămâna 10: Protocoale Aplicație
├── 📁 11roWSL/                        # Săptămâna 11: Load Balancing
├── 📁 12roWSL/                        # Săptămâna 12: Email & RPC
├── 📁 13roWSL/                        # Săptămâna 13: IoT & Securitate
├── 📁 14roWSL/                        # Săptămâna 14: Recapitulare
│
├── 📄 READMEro.md                     # Documentație principală (RO)
└── 📄 LICENSE                         # Licență MIT
```

### 4.3 Diferențe cheie între repository-uri

| Aspect | netENwsl (Engleză) | netROwsl (Română) |
|--------|-------------------|-------------------|
| **Convenție denumire** | `<N>enWSL` | `<NN>roWSL` (cu zero pentru 01-09) |
| **Documentație** | README.md, docstrings EN | READMEro.md, comentarii RO |
| **Numele scripturilor** | `start_lab.py`, `stop_lab.py` | `porneste_lab.py`, `opreste_lab.py` |
| **Mesaje în consolă** | Engleză | Română |
| **Structura internă** | Identică | Identică |
| **Compatibilitate** | Completă | Completă |

---

# PARTEA II — CONFIGURAREA MEDIULUI DE LUCRU

---

## 5. Cerințe de sistem

### 5.1 Cerințe hardware

| Componentă | Minim | Recomandat |
|------------|-------|------------|
| **Procesor** | Intel Core i5 / AMD Ryzen 5 | Intel Core i7 / AMD Ryzen 7 |
| **Memorie RAM** | 8 GB | 16 GB |
| **Spațiu disc** | 20 GB liber | 50 GB liber (SSD) |
| **Virtualizare** | VT-x / AMD-V activat | VT-x / AMD-V + IOMMU |

### 5.2 Cerințe software

| Software | Versiune minimă | Verificare |
|----------|-----------------|------------|
| **Windows** | 10 (build 19041+) sau 11 | `winver` |
| **WSL2** | Kernel 5.15+ | `wsl --status` |
| **Ubuntu** | 22.04 LTS | `lsb_release -a` |
| **Docker Engine** | 24.0+ | `docker --version` |
| **Docker Compose** | 2.20+ | `docker compose version` |
| **Python** | 3.11+ | `python3 --version` |
| **Wireshark** | 4.0+ | Despre → Wireshark |
| **Git** | 2.40+ | `git --version` |

---

## 6. Credențiale standard

### 6.1 Tabel centralizat credențiale

| Serviciu | Utilizator | Parolă | URL/Acces | Observații |
|----------|------------|--------|-----------|------------|
| **Ubuntu WSL** | `stud` | `stud` | Terminal WSL | Utilizator cu privilegii `sudo` |
| **Portainer** | `stud` | `studstudstud` | http://localhost:9000 | Parolă min. 12 caractere |
| **DVWA** (Săpt. 13) | `admin` | `password` | http://localhost:8080 | După configurare inițială |
| **FTP** (diverse săpt.) | `anonymous` | (gol) | localhost:2121 | Sau porturi specifice |

### 6.2 De ce aceste credențiale?

- **`stud/stud`** pentru Ubuntu — simplu de reținut, consistent cu mediul academic
- **`studstudstud`** pentru Portainer — Portainer impune o parolă de **minimum 12 caractere**
- **Credențiale consistente** — toate materialele de curs și scripturile sunt pre-configurate cu aceste valori

---

## 7. Instalare pas cu pas

### 7.1 Pasul 1: Activare WSL2

#### 7.1.1 Deschideți PowerShell ca Administrator

1. Apăsați `Win + X` sau click dreapta pe butonul Start
2. Selectați **"Windows Terminal (Admin)"** sau **"PowerShell (Admin)"**
3. Confirmați cu **"Da"** la promptul User Account Control

#### 7.1.2 Instalați WSL2

```powershell
wsl --install
```

**Ce face această comandă:**
- ✅ Activează funcția Windows Subsystem for Linux
- ✅ Activează funcția Virtual Machine Platform
- ✅ Descarcă și instalează kernel-ul Linux WSL2
- ✅ Setează WSL2 ca versiune implicită

#### 7.1.3 Reporniți calculatorul

```powershell
Restart-Computer
```

> 🔄 **Restart OBLIGATORIU!** Salvați toate documentele înainte de repornire.

#### 7.1.4 Verificați instalarea

După restart, deschideți PowerShell și verificați:

```powershell
wsl --status
```

**Output așteptat:**
```
Default Distribution: Ubuntu
Default Version: 2
Windows Subsystem for Linux was last updated on [date]
WSL automatic updates are on.
Kernel version: 5.15.x.x-microsoft-standard-WSL2
```

---

### 7.2 Pasul 2: Instalare Ubuntu 22.04

#### 7.2.1 Instalați Ubuntu

```powershell
wsl --install -d Ubuntu-22.04 --web-download
```

#### 7.2.2 Configurați utilizatorul

Când vi se cere, introduceți:

```
Enter new UNIX username: stud
New password: stud
Retype new password: stud
```

> 📝 **Notă:** Parola NU se afișează când o tastați — comportament normal Linux.

#### 7.2.3 Verificați instalarea

```powershell
wsl -l -v
```

**Output așteptat:**
```
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2
```

---

### 7.3 Pasul 3: Instalare Docker în WSL

#### 7.3.1 Deschideți terminalul Ubuntu

```powershell
wsl -d Ubuntu-22.04
```

#### 7.3.2 Actualizați sistemul

```bash
sudo apt update && sudo apt upgrade -y
```

#### 7.3.3 Instalați dependențele

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

#### 7.3.4 Adăugați cheia GPG Docker

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

#### 7.3.5 Adăugați repository-ul Docker

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### 7.3.6 Instalați Docker Engine

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### 7.3.7 Adăugați utilizatorul în grupul docker

```bash
sudo usermod -aG docker $USER
```

#### 7.3.8 Porniți serviciul Docker

```bash
sudo service docker start
```

#### 7.3.9 Aplicați modificările de grup

```bash
newgrp docker
```

#### 7.3.10 Verificați instalarea

```bash
docker --version
docker run hello-world
```

---

### 7.4 Pasul 4: Instalare Portainer CE

#### 7.4.1 Creați volumul pentru date persistente

```bash
docker volume create portainer_data
```

#### 7.4.2 Rulați containerul Portainer

```bash
docker run -d \
  -p 9000:9000 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

> ⚠️ **IMPORTANT:** Portainer folosește **EXCLUSIV portul 9000**. Niciun alt serviciu de laborator nu trebuie să utilizeze acest port!

#### 7.4.3 Configurați contul administrator

1. Deschideți browserul și navigați la: **http://localhost:9000**
2. Creați contul de administrator:
   - **Username:** `stud`
   - **Password:** `studstudstud`
3. Click pe **"Create user"**

> ⚠️ **ATENȚIE:** Aveți **5 minute** să creați contul după prima pornire. Dacă depășiți, trebuie să recreați containerul.

#### 7.4.4 Conectați-vă la mediul local Docker

1. Selectați **"Get Started"**
2. Alegeți **"local"** environment
3. Click pe **"Connect"**

---

### 7.5 Pasul 5: Instalare Wireshark (Windows)

#### 7.5.1 Descărcați Wireshark

Navigați la: **https://www.wireshark.org/download.html**

Descărcați versiunea pentru **Windows x64 Installer**.

#### 7.5.2 Instalați Wireshark

1. Rulați installer-ul descărcat
2. La componente, asigurați-vă că **Npcap** este selectat
3. La opțiunile Npcap:
   - ✅ Bifați **"Install Npcap in WinPcap API-compatible Mode"**
   - ✅ Bifați **"Support raw 802.11 traffic"** (opțional)
4. Finalizați instalarea

#### 7.5.3 Verificați instalarea

1. Lansați Wireshark
2. Verificați că vedeți interfața **"vEthernet (WSL)"** în lista de interfețe
3. WSL trebuie să ruleze pentru a vedea această interfață

---

### 7.6 Pasul 6: Instalare pachete Python

#### 7.6.1 În terminalul Ubuntu WSL

```bash
# Instalare pip dacă nu există
sudo apt install -y python3-pip python3-venv

# Instalare pachete necesare pentru laborator
pip3 install --break-system-packages \
    docker \
    scapy \
    dpkt \
    requests \
    flask \
    paramiko \
    pyftpdlib \
    paho-mqtt \
    dnspython \
    grpcio \
    grpcio-tools \
    protobuf \
    PyYAML \
    colorama \
    pytest
```

#### 7.6.2 Verificare instalare

```bash
python3 -c "import docker; print('docker:', docker.__version__)"
python3 -c "import scapy; print('scapy: OK')"
python3 -c "import dpkt; print('dpkt: OK')"
python3 -c "import requests; print('requests: OK')"
```

---

### 7.7 Pasul 7: Configurare auto-start Docker (opțional)

Pentru ca Docker să pornească automat când deschideți Ubuntu:

#### 7.7.1 Editați fișierul .bashrc

```bash
nano ~/.bashrc
```

#### 7.7.2 Adăugați la sfârșit

```bash
# Auto-start Docker service
if service docker status 2>&1 | grep -q "is not running"; then
    sudo service docker start > /dev/null 2>&1
fi
```

#### 7.7.3 Configurați sudo fără parolă pentru Docker

```bash
echo "$USER ALL=(ALL) NOPASSWD: /usr/sbin/service docker *" | sudo tee /etc/sudoers.d/docker-service
```

---

## 8. Verificarea instalării

> 💭 **PREDICȚIE:** Ce versiune minimă de Docker Compose este necesară? Ce va afișa `docker compose version` pe sistemul tău?


### 8.1 Script complet de verificare

Creați și rulați acest script în Ubuntu:

```bash
#!/bin/bash
# verify_lab_environment.sh
# Script de verificare completă a mediului de laborator

# ═══════════════════════════════════════════════════════════════════════════════
# DEFINIRE_CULORI_SI_CONTOARE
# ═══════════════════════════════════════════════════════════════════════════════
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# ═══════════════════════════════════════════════════════════════════════════════
# AFISARE_BANNER
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║        VERIFICARE MEDIU LABORATOR REȚELE DE CALCULATOARE                  ║"
echo "║              © 2019–2026 Antonio Clim, Andrei Toma                        ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# DEFINIRE_FUNCTII_VERIFICARE
# ═══════════════════════════════════════════════════════════════════════════════
check_required() {
    if eval "$2" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $1"
    else
        echo -e "  ${RED}✗${NC} $1"
        ((ERRORS++))
    fi
}

check_optional() {
    if eval "$2" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $1"
    else
        echo -e "  ${YELLOW}○${NC} $1 (opțional)"
        ((WARNINGS++))
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# AFISARE_INFORMATII_SISTEM
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}▶ INFORMAȚII SISTEM${NC}"
echo "  Hostname: $(hostname)"
echo "  Ubuntu: $(lsb_release -d 2>/dev/null | cut -f2)"
echo "  Kernel: $(uname -r)"
echo "  User: $(whoami)"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICARE_COMPONENTE_PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}▶ COMPONENTE PRINCIPALE${NC}"
check_required "Python 3.11+" "python3 --version | grep -E 'Python 3\.(1[1-9]|[2-9][0-9])'"
check_required "pip3" "pip3 --version"
check_required "Git" "git --version"
check_required "curl" "curl --version"
check_required "wget" "wget --version"
echo ""

echo -e "${BLUE}▶ DOCKER${NC}"
check_required "Docker Engine" "docker --version"
check_required "Docker Compose" "docker compose version"
check_required "Docker daemon activ" "docker info"
check_required "Docker fără sudo" "docker ps"
echo ""

echo -e "${BLUE}▶ PORTAINER (Port 9000)${NC}"
if docker ps | grep -q portainer; then
    echo -e "  ${GREEN}✓${NC} Portainer rulează pe portul 9000"
else
    echo -e "  ${YELLOW}○${NC} Portainer nu rulează (porniți manual dacă e necesar)"
    ((WARNINGS++))
fi
echo ""

echo -e "${BLUE}▶ CONTAINERE ACTIVE${NC}"
docker ps --format "  {{.Names}}: {{.Status}}" 2>/dev/null || echo "  (niciun container activ)"
echo ""

echo -e "${BLUE}▶ INSTRUMENTE REȚEA${NC}"
check_required "tcpdump" "which tcpdump"
check_optional "tshark" "which tshark"
check_required "netcat" "which nc"
check_optional "nmap" "which nmap"
check_optional "iperf3" "which iperf3"
echo ""

echo -e "${BLUE}▶ BIBLIOTECI PYTHON${NC}"
check_required "docker" "python3 -c 'import docker'"
check_required "scapy" "python3 -c 'import scapy.all'"
check_required "dpkt" "python3 -c 'import dpkt'"
check_required "requests" "python3 -c 'import requests'"
check_required "flask" "python3 -c 'import flask'"
check_optional "paramiko" "python3 -c 'import paramiko'"
check_optional "pyftpdlib" "python3 -c 'import pyftpdlib'"
check_optional "paho-mqtt" "python3 -c 'import paho.mqtt.client'"
check_optional "dnspython" "python3 -c 'import dns.resolver'"
check_optional "grpcio" "python3 -c 'import grpc'"
echo ""

echo "═══════════════════════════════════════════════════════════════════════════"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ TOATE COMPONENTELE NECESARE SUNT INSTALATE CORECT!${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}   ($WARNINGS componente opționale lipsesc)${NC}"
    fi
else
    echo -e "${RED}❌ $ERRORS COMPONENTĂ(E) NECESARĂ(E) LIPSEȘTE/LIPSESC${NC}"
fi
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

exit $ERRORS
```

### 8.2 Test rapid captură Wireshark

1. Deschideți **Wireshark** pe Windows
2. Selectați interfața **vEthernet (WSL)** și porniți captura
3. În terminalul Ubuntu, rulați:

```bash
docker run --rm alpine ping -c 5 8.8.8.8
```

4. În Wireshark, aplicați filtrul: `icmp`
5. Verificați că vedeți pachete **Echo request** și **Echo reply**

---

# PARTEA III — CURRICULA SĂPTĂMÂNALĂ DETALIATĂ

---

## 9. Ghid rapid de pornire a laboratoarelor

### 9.1 Workflow standard pentru fiecare săptămână

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW STANDARD LABORATOR                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. CLONARE              2. VERIFICARE           3. PORNIRE                  │
│  ┌──────────────┐       ┌──────────────┐       ┌──────────────┐             │
│  │ git clone    │  ──▶  │ python       │  ──▶  │ python       │             │
│  │ repository   │       │ verifica_    │       │ porneste_    │             │
│  │              │       │ mediu.py     │       │ lab.py       │             │
│  └──────────────┘       └──────────────┘       └──────────────┘             │
│                                                        │                     │
│                                                        ▼                     │
│  6. CURĂȚARE             5. ANALIZĂ             4. EXERCIȚII                │
│  ┌──────────────┐       ┌──────────────┐       ┌──────────────┐             │
│  │ python       │  ◀──  │ Wireshark    │  ◀──  │ Exerciții    │             │
│  │ opreste_     │       │ PCAP files   │       │ Python       │             │
│  │ lab.py       │       │              │       │              │             │
│  └──────────────┘       └──────────────┘       └──────────────┘             │
│                                                                              │
│  ⚠️ NOTĂ: Portainer (port 9000) rămâne MEREU activ între laboratoare!       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Comenzi standard disponibile în fiecare kit (versiunea română)

```bash
# Verificare mediu
python3 setup/verifica_mediu.py

# Pornire servicii laborator
python3 scripts/porneste_lab.py

# Verificare status servicii
python3 scripts/porneste_lab.py --status

# Rulare demonstrații
python3 scripts/ruleaza_demo.py --demo 1

# Captură trafic
python3 scripts/captura_trafic.py --durata 30 --iesire pcap/captura.pcap

# Oprire servicii (Portainer rămâne activ!)
python3 scripts/opreste_lab.py

# Curățare completă
python3 scripts/curata.py --complet
```

---

## 10. Clonarea individuală a fiecărei săptămâni

### 10.1 Structura directoarelor pentru studenți (Repository Română)

Fiecare student trebuie să-și organizeze laboratoarele într-o structură consistentă:

```
D:\RETELE\
├── SAPT1\          ← Conține conținutul 01roWSL
├── SAPT2\          ← Conține conținutul 02roWSL
├── SAPT3\          ← Conține conținutul 03roWSL
...
├── SAPT13\         ← Conține conținutul 13roWSL
└── SAPT14\         ← Conține conținutul 14roWSL
```

### 10.2 Comenzi de clonare pentru repository-ul Română (netROwsl)

> 📍 **Executați aceste comenzi în PowerShell sau Terminal Windows**

---

#### 📦 Clonare Săptămâna 1 — Fundamente ale rețelelor

```powershell
cd D:\RETELE
git clone https://github.com/antonioclim/netROwsl.git SAPT1
cd SAPT1\01roWSL
```

---

#### 📦 Clonare Săptămâna 11 — Echilibrarea încărcării

```powershell
cd D:\RETELE
git clone https://github.com/antonioclim/netROwsl.git SAPT11
cd SAPT11\11roWSL
```

---

#### 📦 Clonare Săptămâna 12 — Protocoale email și RPC

```powershell
cd D:\RETELE
git clone https://github.com/antonioclim/netROwsl.git SAPT12
cd SAPT12\12roWSL
```

---

#### 📦 Clonare Săptămâna 13 — IoT și securitatea rețelelor

```powershell
cd D:\RETELE
git clone https://github.com/antonioclim/netROwsl.git SAPT13
cd SAPT13\13roWSL
```

---

#### 📦 Clonare Săptămâna 14 — Recapitulare și evaluare

```powershell
cd D:\RETELE
git clone https://github.com/antonioclim/netROwsl.git SAPT14
cd SAPT14\14roWSL
```

---

### 10.3 Clonare completă a repository-ului

Dacă preferați să aveți toate săptămânile într-un singur loc:

**Pentru versiunea Română:**
```powershell
cd D:\RETELE
git clone https://github.com/antonioclim/netROwsl.git
cd netROwsl
```

**Pentru versiunea Engleză:**
```powershell
cd ~\Documents
git clone https://github.com/antonioclim/netENwsl.git
cd netENwsl
```

---

## 11. Săptămâna 1: Fundamente ale rețelelor

> 💭 **PREDICȚIE:** După `ping -c 4 google.com`, câte pachete vor fi trimise și câte primite în condiții normale?


**Director RO:** `01roWSL/` | **Director EN:** `1enWSL/`  
**Rețea Docker:** `172.20.1.0/24`  
**Porturi:** 9090 (TCP), 9091 (UDP), 9092 (Alternativ)

### 11.1 Sinopsis

Acest laborator introductiv stabilește competențele fundamentale în diagnosticarea rețelelor prin experimentare practică cu instrumente CLI esențiale. Studenții dezvoltă intuiție practică despre comportamentul rețelelor prin examinarea configurațiilor de interfață, validarea conectivității și capturarea traficului pentru analiza protocoalelor.

### 11.2 Obiective de învățare

| Nivel Bloom | Verb | Obiectiv concret |
|-------------|------|------------------|
| **A reține** | Reamintește | Comenzile Linux esențiale: `ip addr`, `ip route`, `ss`, `ping`, `netcat` |
| **A înțelege** | Explică | Scopul interfețelor de rețea, tabelelor de rutare și stărilor socket-urilor |
| **A aplica** | Demonstrează | Testarea conectivității folosind ICMP și interpretarea măsurătorilor de latență |
| **A aplica** | Implementează | Canale TCP/UDP de bază folosind netcat și socket-uri Python |
| **A analiza** | Examinează | Capturi de rețea pentru identificarea comportamentului protocoalelor |
| **A analiza** | Compară | Pattern-uri de comunicare TCP vs UDP prin examinarea pachetelor |
| **A evalua** | Diagnostichează | Probleme comune de conectivitate folosind depanare sistematică |

### 11.3 Tehnologii cheie

`ip`, `ss`, `ping`, `traceroute`, `netcat`, `tcpdump`, `tshark`, socket-uri Python

### 11.4 Exerciții

| Nr. | Titlu | Durată | Descriere |
|-----|-------|--------|-----------|
| 1 | Inspecție interfețe de rețea | 15 min | Enumerarea interfețelor, examinarea IP, documentarea routing |
| 2 | Testarea conectivității | 20 min | Teste ping progresive, măsurarea latenței |
| 3 | Comunicare TCP cu netcat | 25 min | Sesiuni bidirecționale, observarea stării conexiunii |
| 4 | Captură și analiză trafic | 30 min | TCP handshake, identificarea câmpurilor, export CSV |
| 5 | Analiză statistică PCAP | 20 min | Procesare programatică Python a capturilor |

---

## 12. Săptămâna 2: Modele arhitecturale și programare socket

> 💭 **PREDICȚIE:** La crearea unui socket TCP, ce tip de socket vei folosi: `SOCK_STREAM` sau `SOCK_DGRAM`?


**Director RO:** `02roWSL/` | **Director EN:** `2enWSL/`  
**Rețea Docker:** `10.0.2.0/24`

### 12.1 Sinopsis

Acest laborator explorează modelele de referință OSI și TCP/IP prin exerciții practice de programare cu socket-uri. Studenții implementează pattern-uri de comunicare client-server, înțelegând cum fluxul de date traversează stiva de protocoale.

### 12.2 Obiective de învățare

| Nivel Bloom | Obiectiv |
|-------------|----------|
| **A reține** | Identificarea celor 7 straturi OSI și 4 straturi TCP/IP cu PDU-urile respective |
| **A înțelege** | Explicarea procesului de încapsulare și transformările PDU |
| **A aplica** | Implementarea clienților și serverelor TCP/UDP folosind API-ul socket Python |
| **A aplica** | Demonstrarea pattern-urilor de server concurent cu threading |
| **A analiza** | Trasarea fluxului de date prin multiple straturi în capturi |
| **A evalua** | Compararea operațiunilor socket blocante vs non-blocante |

### 12.3 Tehnologii cheie

Python `socket`, `threading`, `concurrent.futures`, modelul OSI, modelul TCP/IP, `scapy`, `dpkt`

---

## 13. Săptămâna 3: Modele avansate de programare în rețea

> 💭 **PREDICȚIE:** Dacă trimiți un pachet UDP broadcast, câte dispozitive din rețeaua locală îl vor primi?

**Director RO:** `03roWSL/` | **Director EN:** `3enWSL/`  
**Rețea Docker:** `172.20.0.0/24`

### 13.1 Sinopsis

Laboratorul introduce pattern-uri avansate de programare incluzând UDP broadcast/multicast, tunelare TCP și design de protocoale la nivel aplicație.

### 13.2 Tehnologii cheie

UDP multicast, broadcast sockets, opțiuni socket (`SO_BROADCAST`, `IP_ADD_MEMBERSHIP`), `struct`

---

## 14. Săptămâna 4: Nivelurile fizic și legătură de date

> 💭 **PREDICȚIE:** Un cadru Ethernet are un câmp CRC. Ce se întâmplă dacă CRC-ul calculat nu corespunde cu cel primit?

**Director RO:** `04roWSL/` | **Director EN:** `4enWSL/`  
**Rețea Docker:** `172.28.0.0/16`

### 14.1 Sinopsis

Laboratorul coboară la cele mai jos straturi accesibile, examinând încadrarea Ethernet, adresarea MAC și construcția de protocoale binare cu CRC32.

### 14.2 Tehnologii cheie

`struct`, `binascii`, `zlib.crc32`, cadre Ethernet, adresare MAC, protocoale binare

---

## 15. Săptămâna 5: Nivelul rețea și adresare IP

> 💭 **PREDICȚIE:** Câte adrese IP utilizabile sunt în rețeaua `192.168.1.0/24`? (Hint: nu sunt 256)

**Director RO:** `05roWSL/` | **Director EN:** `5enWSL/`  
**Rețea Docker:** `10.5.0.0/24`

### 15.1 Sinopsis

Acoperire completă a adresării IP, metodologiilor de subrețele (CIDR, FLSM, VLSM) și fundamentelor IPv6.

### 15.2 Tehnologii cheie

Modulul `ipaddress`, notația CIDR, FLSM, VLSM, IPv4, IPv6, calculatoare de subrețele

---

## 16. Săptămâna 6: NAT/PAT, protocoale suport și SDN

> 💭 **PREDICȚIE:** Ce se întâmplă cu adresa IP sursă a unui pachet când trece prin NAT? Rămâne aceeași sau se schimbă?

**Director RO:** `06roWSL/` | **Director EN:** `6enWSL/`  
**Rețea Docker:** Topologie personalizată cu segmente multiple

### 16.1 Sinopsis

Network Address Translation, protocoale suport esențiale (ARP, DHCP, ICMP, NDP) și introducere în Software-Defined Networking.

### 16.2 Tehnologii cheie

`iptables`, NAT/PAT, ARP, DHCP, ICMP, NDP, Open vSwitch, os-ken (fork Ryu), Mininet

---

## 17. Săptămâna 7: Interceptare pachete, filtrare și securitate

> 💭 **PREDICȚIE:** Ce pachete va captura `tcpdump -i any port 80`? Doar HTTP sau și altele?


**Director RO:** `07roWSL/` | **Director EN:** `7enWSL/`  
**Rețea Docker:** `10.0.7.0/24`

### 17.1 Sinopsis

Competențe esențiale de securitate și forensică prin filtrarea pachetelor, configurarea firewall-ului și scanarea defensivă a porturilor.

### 17.2 Tehnologii cheie

`tcpdump`, `tshark`, filtre Wireshark, `iptables`, `nmap`, scanare porturi, Mininet

---

## 18. Săptămâna 8: Nivelul transport, HTTP și proxy invers

> 💭 **PREDICȚIE:** În TCP 3-way handshake, care este ordinea flag-urilor: SYN → ? → ?


**Director RO:** `08roWSL/` | **Director EN:** `8enWSL/`  
**Rețea Docker:** `172.28.8.0/24`  
**Porturi:** 8080 (HTTP)

### 18.1 Sinopsis

Mecanisme nivel transport (TCP handshake, flow control) și aplicarea în implementarea serverelor HTTP cu Nginx ca reverse proxy.

### 18.2 Tehnologii cheie

TCP handshake, HTTP/1.1, `http.server`, Nginx, reverse proxy, load balancing, Docker Compose

---

## 19. Săptămâna 9: Nivelurile sesiune și prezentare

> 💭 **PREDICȚIE:** În FTP, care mod (activ sau pasiv) funcționează mai bine când clientul este în spatele unui firewall?

**Director RO:** `09roWSL/` | **Director EN:** `9enWSL/`  
**Rețea Docker:** `172.29.9.0/24`

### 19.1 Sinopsis

Management sesiuni și prezentare date, cu focus pe FTP (moduri activ/pasiv) și serializare binară.

### 19.2 Tehnologii cheie

FTP (activ/pasiv), `ftplib`, `pyftpdlib`, încadrare binară, `struct`, gestionare stare sesiune

---

## 20. Săptămâna 10: Protocoale de nivel aplicație

> 💭 **PREDICȚIE:** Ce port folosește HTTPS implicit și de ce nu este același cu HTTP?

**Director RO:** `10roWSL/` | **Director EN:** `10enWSL/`  
**Rețea Docker:** `172.20.0.0/24`

### 20.1 Sinopsis

Survey protocoale critice: HTTP/HTTPS, REST API, DNS, SSH. Explorare TLS și operațiuni programatice.

### 20.2 Tehnologii cheie

HTTP/HTTPS, TLS/SSL, REST APIs, `requests`, DNS, `dnspython`, SSH, `paramiko`

---

## 21. Săptămâna 11: Echilibrarea încărcării (Load Balancing)

> 💭 **PREDICȚIE:** Cu round-robin load balancing și 3 backend-uri, al 4-lea request va ajunge la care server?


**Director RO:** `11roWSL/` | **Director EN:** `11enWSL/`  
**Rețea Docker:** `week11net` (10.0.11.0/24)  
**Porturi:** 8080 (Load Balancer), 8081-8083 (Backend-uri)

### 21.1 Sinopsis

Acest laborator explorează în profunzime strategiile de echilibrare a încărcării în sistemele distribuite, implementând și comparând algoritmi round-robin, weighted round-robin, least connections și IP hash folosind Nginx ca load balancer. Studenții vor configura health checks pentru failover automat și vor analiza distribuția traficului în timp real.

### 21.2 Arhitectura laboratorului

```
                    ┌─────────────────────────────────────────┐
                    │              CLIENT                      │
                    │         (Cereri HTTP)                    │
                    └─────────────────┬───────────────────────┘
                                      │
                                      ▼ Port 8080
                    ┌─────────────────────────────────────────┐
                    │         NGINX LOAD BALANCER              │
                    │           10.0.11.10                     │
                    │    ┌─────────────────────────────┐      │
                    │    │ Algoritmi:                   │      │
                    │    │ • Round Robin (implicit)     │      │
                    │    │ • Weighted Round Robin       │      │
                    │    │ • Least Connections          │      │
                    │    │ • IP Hash                    │      │
                    │    └─────────────────────────────┘      │
                    └───────┬───────────┬───────────┬─────────┘
                            │           │           │
                    ┌───────▼───┐ ┌─────▼─────┐ ┌───▼───────┐
                    │ Backend 1 │ │ Backend 2 │ │ Backend 3 │
                    │ 10.0.11.11│ │ 10.0.11.12│ │ 10.0.11.13│
                    │ Port 8081 │ │ Port 8082 │ │ Port 8083 │
                    └───────────┘ └───────────┘ └───────────┘
```

### 21.3 Servicii disponibile

| Serviciu | IP Container | Port Host | Descriere |
|----------|--------------|-----------|-----------|
| **nginx_lb** | 10.0.11.10 | 8080 | Load Balancer Nginx |
| **backend1** | 10.0.11.11 | 8081 | Server Flask #1 |
| **backend2** | 10.0.11.12 | 8082 | Server Flask #2 |
| **backend3** | 10.0.11.13 | 8083 | Server Flask #3 |
| **Portainer** | - | 9000 | Management containere (GLOBAL) |

### 21.4 Exerciții principale

| Nr. | Titlu | Descriere |
|-----|-------|-----------|
| 1 | Algoritm Round Robin | Implementare și verificare distribuție uniformă |
| 2 | Weighted Round Robin | Configurare ponderi diferite pentru backend-uri |
| 3 | Least Connections | Rutare către serverul cu cele mai puține conexiuni |
| 4 | Health Checks | Configurare verificări periodice și failover automat |
| 5 | Analiză distribuție | Vizualizare și statistici distribuție trafic |

### 21.5 Filtre Wireshark specifice

```
# Trafic Load Balancer
tcp.port == 8080

# Trafic către toate backend-urile
tcp.port in {8081, 8082, 8083}

# Analiza distribuției
http.request && tcp.port == 8080
```

### 21.6 Teme pentru acasă

1. **Sticky Sessions** — Implementare afinitate sesiune cu cookie-uri
2. **Rate Limiting** — Limitare cereri per client cu Nginx

---

## 22. Săptămâna 12: Protocoale email și RPC

**Director RO:** `12roWSL/` | **Director EN:** `12enWSL/`  
**Rețea Docker:** `week12net` (10.0.12.0/24)  
**Porturi:** 2525 (SMTP), 5000 (JSON-RPC), 5001 (XML-RPC), 50051 (gRPC)

### 22.1 Sinopsis

Acest laborator acoperă două domenii fundamentale ale comunicării în rețea: protocoalele de email (SMTP pentru trimitere, POP3/IMAP pentru recepție) și paradigmele Remote Procedure Call (RPC) care permit apelarea de funcții pe servere remote ca și cum ar fi locale.

### 22.2 Arhitectura laboratorului

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SĂPTĂMÂNA 12 - TOPOLOGIE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────┐     ┌───────────────┐     ┌───────────────┐             │
│  │  SMTP Server  │     │ JSON-RPC Srv  │     │  gRPC Server  │             │
│  │  10.0.12.10   │     │  10.0.12.20   │     │  10.0.12.30   │             │
│  │  Port: 2525   │     │  Port: 5000   │     │  Port: 50051  │             │
│  └───────────────┘     └───────────────┘     └───────────────┘             │
│                                                                             │
│  ┌───────────────┐     ┌───────────────┐                                   │
│  │ XML-RPC Srv   │     │    Client     │                                   │
│  │  10.0.12.21   │     │  10.0.12.100  │                                   │
│  │  Port: 5001   │     │               │                                   │
│  └───────────────┘     └───────────────┘                                   │
│                                                                             │
│                    Rețea: week12net (10.0.12.0/24)                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 22.3 Servicii disponibile

| Serviciu | IP Container | Port Host | Protocol | Descriere |
|----------|--------------|-----------|----------|-----------|
| **smtp_server** | 10.0.12.10 | 2525 | SMTP | Server email pentru teste |
| **jsonrpc_server** | 10.0.12.20 | 5000 | JSON-RPC | Calculator remote JSON |
| **xmlrpc_server** | 10.0.12.21 | 5001 | XML-RPC | Calculator remote XML |
| **grpc_server** | 10.0.12.30 | 50051 | gRPC | Serviciu gRPC modern |
| **client** | 10.0.12.100 | - | - | Container client teste |
| **Portainer** | - | 9000 | HTTP | Management containere (GLOBAL) |

### 22.4 Exerciții principale

| Nr. | Titlu | Descriere |
|-----|-------|-----------|
| 1 | Client SMTP | Trimitere email programatică cu `smtplib` |
| 2 | JSON-RPC Client | Apeluri proceduri remote cu JSON |
| 3 | XML-RPC Client | Apeluri proceduri remote cu XML |
| 4 | gRPC cu Protocol Buffers | Definire servicii și generare cod |
| 5 | Comparație RPC | Analiză performanță și overhead |

### 22.5 Filtre Wireshark specifice

```
# Trafic SMTP
tcp.port == 2525
smtp

# Trafic JSON-RPC (HTTP)
tcp.port == 5000 && http
http.request.method == "POST" && tcp.port == 5000

# Trafic XML-RPC
tcp.port == 5001 && http

# Trafic gRPC (HTTP/2)
tcp.port == 50051
http2
```

### 22.6 Teme pentru acasă

1. **Email cu atașamente** — Trimitere MIME multipart
2. **Serviciu gRPC complet** — Definire Protocol Buffers și implementare bidirecțional streaming

---

## 23. Săptămâna 13: IoT și securitatea rețelelor

**Director RO:** `13roWSL/` | **Director EN:** `13enWSL/`  
**Rețea Docker:** `week13net` (10.0.13.0/24)  
**Porturi:** 1883 (MQTT), 8883 (MQTT TLS), 8080 (DVWA), 2121 (FTP)

### 23.1 Sinopsis

Acest laborator combină două domenii critice: protocoalele Internet of Things (IoT) cu focus pe MQTT și fundamentele securității rețelelor incluzând scanare porturi, sniffing pachete și evaluarea vulnerabilităților.

### 23.2 Arhitectura laboratorului

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SĂPTĂMÂNA 13 - TOPOLOGIE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                     ARHITECTURA MQTT                                     │ │
│  │  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐             │ │
│  │  │ IoT Sensor  │────▶│  Mosquitto  │◀────│ IoT Control │             │ │
│  │  │  (Publish)  │     │   Broker    │     │ (Subscribe) │             │ │
│  │  └─────────────┘     │ 10.0.13.100 │     └─────────────┘             │ │
│  │                      │ :1883 :8883 │                                  │ │
│  │                      └─────────────┘                                  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                  SECURITY TESTING                                      │ │
│  │  ┌─────────────┐     ┌─────────────┐                                  │ │
│  │  │    DVWA     │     │   vsftpd    │                                  │ │
│  │  │ 10.0.13.11  │     │ 10.0.13.12  │                                  │ │
│  │  │  Port 8080  │     │ Port 2121   │                                  │ │
│  │  │ Vulnerable  │     │ +backdoor   │                                  │ │
│  │  └─────────────┘     └─────────────┘                                  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│                    Rețea: week13net (10.0.13.0/24)                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 23.3 Servicii disponibile

| Serviciu | IP Container | Port Host | Credențiale | Descriere |
|----------|--------------|-----------|-------------|-----------|
| **mosquitto** | 10.0.13.100 | 1883, 8883 | - | Broker MQTT (plain + TLS) |
| **dvwa** | 10.0.13.11 | 8080 | admin/password | Damn Vulnerable Web App |
| **vsftpd** | 10.0.13.12 | 2121, 6200 | anonymous | FTP cu backdoor simulat |
| **Portainer** | - | 9000 | stud/studstudstud | Management containere (GLOBAL) |

### 23.4 Exerciții principale

| Nr. | Titlu | Descriere |
|-----|-------|-----------|
| 1 | Scanner TCP Porturi | Implementare scanner concurrent Python |
| 2 | Client MQTT cu TLS | Publish/Subscribe securizat |
| 3 | Sniffer Pachete | Captură și analiză cu Scapy |
| 4 | Verificator Vulnerabilități | Evaluare securitate servicii |

### 23.5 Filtre Wireshark specifice

```
# MQTT plaintext
tcp.port == 1883
mqtt
mqtt.msgtype == 3  # PUBLISH messages

# MQTT TLS
tcp.port == 8883
tls.handshake.type

# DVWA HTTP
tcp.port == 8080 && http
http.request.method == "POST"

# FTP
tcp.port == 2121
ftp
ftp.request.command == "USER"

# Port scanning detection
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Toate serviciile laboratorului
tcp.port in {1883, 8883, 8080, 2121, 6200}
```

### 23.6 Teme pentru acasă

1. **Scanner Porturi Avansat** — Adăugare detectare OS și fingerprinting servicii
2. **Raport Securitate MQTT** — Best practices pentru implementări industriale IoT

> ⚠️ **AVERTISMENT SECURITATE:** Acest laborator conține servicii intenționat vulnerabile (DVWA, vsftpd cu backdoor) doar pentru scopuri educaționale. NU expuneți aceste servicii la internet și nu efectuați scanări/teste pe sisteme fără autorizație explicită!

---

## 24. Săptămâna 14: Recapitulare integrată și evaluare

> 💭 **PREDICȚIE:** Câte protocoale diferite ai studiat în acest semestru? Poți enumera minim 10?


**Director RO:** `14roWSL/` | **Director EN:** `14enWSL/`  
**Rețele Docker:** `week14_backend_net` (172.20.0.0/24), `week14_frontend_net` (172.21.0.0/24)  
**Porturi:** 8080 (Load Balancer), 8001-8002 (Backend-uri), 9090 (Echo Server)

> ⚠️ **NOTĂ IMPORTANTĂ:** Serverul Echo folosește portul **9090**, NU 9000! Portul 9000 este rezervat exclusiv pentru Portainer.

### 24.1 Sinopsis

Laboratorul de sinteză — construcția unei aplicații multi-tier complete cu load balancing, reverse proxy și validare completă. Această săptămână integrează toate conceptele studiate pe parcursul semestrului într-un proiect practic complex.

### 24.2 Arhitectura finală

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
│    │ 172.20.0.20 │   (NU 9000!)             │
│    └─────────────┘                          │
└─────────────────────────────────────────────┘

Portainer (Management Global): http://localhost:9000
```

### 24.3 Servicii disponibile

| Serviciu | IP Container | Port Host | Descriere |
|----------|--------------|-----------|-----------|
| **week14_lb** | 172.20.0.10 / 172.21.0.10 | 8080 | Load Balancer (dual-homed) |
| **week14_app1** | 172.20.0.2 | 8001 | Backend Server #1 |
| **week14_app2** | 172.20.0.3 | 8002 | Backend Server #2 |
| **week14_echo** | 172.20.0.20 | **9090** | Server Echo TCP |
| **week14_client** | 172.21.0.2 | - | Container client teste |
| **Portainer** | - | **9000** | Management containere (GLOBAL, REZERVAT!) |

### 24.4 Exerciții principale

| Nr. | Titlu | Descriere |
|-----|-------|-----------|
| 1 | Verificare Mediu | Confirmarea funcționării infrastructurii |
| 2 | Analiză Load Balancer | Înțelegerea distribuției round-robin |
| 3 | Testare Server Echo | Comunicare TCP bidirecțională |
| 4 | Captură și Analiză | Utilizarea Wireshark pentru trasare completă |

### 24.5 Filtre Wireshark specifice

```
# Load Balancer
tcp.port == 8080
http && tcp.port == 8080

# Backend-uri
tcp.port in {8001, 8002}

# Echo Server (PORT 9090, NU 9000!)
tcp.port == 9090

# Rețea Frontend
ip.addr == 172.21.0.0/24

# Rețea Backend
ip.addr == 172.20.0.0/24

# Tot traficul laboratorului (FĂRĂ Portainer)
tcp.port in {8080, 8001, 8002, 9090}
```

### 24.6 Teme pentru acasă

| Tema | Descriere | Fișier |
|------|-----------|--------|
| 1 | Protocol Echo Îmbunătățit | `tema_14_01_echo_avansat.py` |
| 2 | Load Balancer cu Ponderi | `tema_14_02_lb_ponderat.py` |
| 3 | Analizator PCAP Automat | `tema_14_03_analizator_pcap.py` |

### 24.7 Obiective finale

La finalul acestei săptămâni, studentul trebuie să poată:

- ✅ Sintetiza toate conceptele din semestru într-o arhitectură completă
- ✅ Configura și administra deployment-uri multi-container cu Docker Compose
- ✅ Trasa traficul HTTP complet prin multiple hop-uri
- ✅ Gestiona scenarii de eșec și failover
- ✅ Utiliza Portainer pentru management vizual eficient
- ✅ Captura și analiza traficul cu Wireshark

---

# PARTEA IV — REFERINȚE ȘI SUPORT

---

## 25. Structura standard a kit-urilor

Fiecare director de săptămână (`<NN>roWSL/` sau `<N>enWSL/`) urmează o organizare consistentă:

```
<NN>roWSL/
│
├── 📄 README.md                   # Prezentare săptămână, obiective, exerciții
├── 📄 CHANGELOG.md                # Istoricul versiunilor
├── 📄 LICENSE                     # Licență MIT
│
├── 📁 setup/                      # Configurare mediu
│   ├── requirements.txt           # Dependențe Python
│   └── verifica_mediu.py          # Validare mediu WSL
│
├── 📁 scripts/                    # Automatizare
│   ├── porneste_lab.py            # Pornire servicii (NU pornește Portainer)
│   ├── opreste_lab.py             # Oprire servicii (NU oprește Portainer)
│   ├── ruleaza_demo.py            # Demonstrații
│   ├── captura_trafic.py          # Captură pachete
│   ├── curata.py                  # Curățare completă
│   └── utils/                     # Module partajate
│
├── 📁 src/                        # Cod sursă
│   ├── __init__.py
│   ├── exercises/                 # Exerciții (ex_NN_XX_*.py)
│   ├── apps/                      # Aplicații complete
│   └── utils/                     # Module reutilizabile
│
├── 📁 docker/                     # Containerizare
│   ├── Dockerfile                 # Imagine container
│   ├── docker-compose.yml         # Orchestrare (FĂRĂ Portainer!)
│   ├── configs/                   # Configurări servicii
│   └── volumes/                   # Date persistente
│
├── 📁 docs/                       # Documentație
│   ├── rezumat_teoretic.md        # Fundamente teoretice
│   └── depanare.md                # Ghid depanare
│
├── 📁 tests/                      # Validare
│   ├── test_mediu.py              # Verificare mediu
│   ├── test_exercitii.py          # Verificare exerciții
│   └── test_rapid.py              # Smoke tests
│
├── 📁 homework/                   # Teme pentru acasă
│   ├── README.md                  # Descriere teme
│   ├── exercises/                 # Enunțuri
│   └── solutions/                 # Soluții
│
├── 📁 pcap/                       # Capturi pachete
│   └── README.md
│
└── 📁 artifacts/                  # Output-uri generate
    └── .gitkeep
```

---

## 26. Planul de adresare IP

### 26.1 Subrețele pe săptămâni

| Săpt. | Director RO | Director EN | Subrețea Docker | Gateway |
|-------|-------------|-------------|-----------------|---------|
| 1 | `01roWSL` | `1enWSL` | `172.20.1.0/24` | 172.20.1.1 |
| 2 | `02roWSL` | `2enWSL` | `10.0.2.0/24` | 10.0.2.1 |
| 3 | `03roWSL` | `3enWSL` | `172.20.0.0/24` | 172.20.0.1 |
| 4 | `04roWSL` | `4enWSL` | `172.28.0.0/16` | 172.28.0.1 |
| 5 | `05roWSL` | `5enWSL` | `10.5.0.0/24` | 10.5.0.1 |
| 6 | `06roWSL` | `6enWSL` | SDN custom | variabil |
| 7 | `07roWSL` | `7enWSL` | `10.0.7.0/24` | 10.0.7.1 |
| 8 | `08roWSL` | `8enWSL` | `172.28.8.0/24` | 172.28.8.1 |
| 9 | `09roWSL` | `9enWSL` | `172.29.9.0/24` | 172.29.9.1 |
| 10 | `10roWSL` | `10enWSL` | `172.20.0.0/24` | 172.20.0.1 |
| 11 | `11roWSL` | `11enWSL` | `10.0.11.0/24` | 10.0.11.1 |
| 12 | `12roWSL` | `12enWSL` | `10.0.12.0/24` | 10.0.12.1 |
| 13 | `13roWSL` | `13enWSL` | `10.0.13.0/24` | 10.0.13.1 |
| 14 | `14roWSL` | `14enWSL` | `172.20.0.0/24` + `172.21.0.0/24` | 172.20.0.1 / 172.21.0.1 |

---

## 27. Convenții de alocare porturi

### 27.1 Portul 9000 — REZERVAT EXCLUSIV PENTRU PORTAINER

> ⚠️ **ATENȚIE CRITICĂ:** Portul **9000** este **MEREU REZERVAT** pentru Portainer și nu trebuie folosit de niciun serviciu de laborator!

### 27.2 Tabel alocare porturi

| Port | Serviciu | Disponibilitate | Note |
|------|----------|-----------------|------|
| **9000** | **Portainer HTTP** | 🔴 REZERVAT PERMANENT | NU utilizați în laboratoare! |
| 8080-8089 | Servicii HTTP | ✅ Disponibile | Load balancers, proxies |
| 8001-8003 | Backend-uri HTTP | ✅ Disponibile | Servere aplicație |
| 9090-9099 | Servicii TCP/UDP test | ✅ Disponibile | Echo servers, etc. |
| 1883 | MQTT plaintext | ✅ Disponibil | Săptămâna 13 |
| 8883 | MQTT cu TLS | ✅ Disponibil | Săptămâna 13 |
| 2121 | FTP non-standard | ✅ Disponibil | Săptămâna 13 |
| 2525 | SMTP test | ✅ Disponibil | Săptămâna 12 |
| 5000-5999 | Aplicații Flask/RPC | ✅ Disponibile | Săptămâna 12 |
| 50051 | gRPC | ✅ Disponibil | Săptămâna 12 |

### 27.3 Exemplu conflict rezolvat — Săptămâna 14

În kit-ul original, serverul Echo folosea portul 9000, creând conflict cu Portainer. Soluția aplicată:

| Serviciu | Port Original | Port Corectat | Motiv |
|----------|--------------|---------------|-------|
| Echo Server | 9000 | **9090** | Conflict cu Portainer |
| Portainer | 9000 | 9000 | REZERVAT PERMANENT |

---

## 28. Tehnologii și instrumente utilizate

### 28.1 Runtime principal

| Tehnologie | Versiune | Scop |
|------------|----------|------|
| **Python** | 3.11+ | Limbaj principal programare |
| **Docker Engine** | 28.2.2+ | Runtime containere |
| **Docker Compose** | 2.x | Orchestrare multi-container |
| **Ubuntu** | 22.04 LTS | Distribuție Linux în WSL |

### 28.2 Instrumente analiză rețea

| Instrument | Scop | Instalare |
|------------|------|-----------|
| **tcpdump** | Captură pachete CLI | `apt install tcpdump` |
| **tshark** | CLI Wireshark | `apt install tshark` |
| **Wireshark** | Analizor grafic | Windows installer |
| **nmap** | Scanare și enumerare | `apt install nmap` |
| **netcat (nc)** | Tool universal TCP/UDP | `apt install netcat-openbsd` |
| **iperf3** | Testare performanță | `apt install iperf3` |
| **traceroute** | Trasare rută | `apt install traceroute` |

### 28.3 Biblioteci Python

| Bibliotecă | Scop | Instalare |
|------------|------|-----------|
| `socket` | Programare rețea low-level | Built-in |
| `scapy` | Manipulare și construire pachete | `pip install scapy` |
| `dpkt` | Parsare pachete și PCAP | `pip install dpkt` |
| `requests` | Client HTTP | `pip install requests` |
| `flask` | Server HTTP | `pip install flask` |
| `paramiko` | Implementare SSH | `pip install paramiko` |
| `pyftpdlib` | Server FTP | `pip install pyftpdlib` |
| `paho-mqtt` | Client MQTT | `pip install paho-mqtt` |
| `dnspython` | Interogări DNS | `pip install dnspython` |
| `grpcio` | Framework gRPC | `pip install grpcio` |
| `docker` | Client API Docker | `pip install docker` |

### 28.4 Servicii infrastructură

| Serviciu | Versiune | Scop | Port |
|----------|----------|------|------|
| **Portainer CE** | 2.33.6 LTS | Management vizual containere | **9000** (REZERVAT!) |
| **Nginx** | ultima | Reverse proxy, load balancer | 8080 |
| **Mosquitto** | ultima | Broker MQTT | 1883, 8883 |
| **DVWA** | ultima | Training vulnerability assessment | 8080 |

---

## 29. Ghid complet de depanare

### 29.1 Probleme WSL2

| Problemă | Cauză posibilă | Soluție |
|----------|----------------|---------|
| WSL2 nu pornește | Virtualizare dezactivată | Activați VT-x/AMD-V în BIOS |
| "Please enable Virtual Machine Platform" | Componentă Windows lipsă | `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart` |
| WSL2 foarte lent | Resurse insuficiente | Editați `.wslconfig`, alocați mai multă memorie |
| "Kernel needs update" | Kernel WSL vechi | `wsl --update` |
| Ubuntu nu apare | Instalare incompletă | `wsl --install -d Ubuntu-22.04` |
| Rețea inaccesibilă | Configurare IP greșită | `wsl --shutdown` apoi reporniți |

### 29.2 Probleme Docker

| Problemă | Cauză posibilă | Soluție |
|----------|----------------|---------|
| "Cannot connect to Docker daemon" | Serviciu Docker oprit | `sudo service docker start` |
| "Permission denied" la docker.sock | Utilizator nu e în grup | `sudo usermod -aG docker $USER` apoi logout/login |
| "Port already in use" | Container/proces vechi | `docker ps -a` + `docker rm -f <container>` |
| Imagini nu se descarcă | Conexiune internet | Verificați DNS: `ping 8.8.8.8` |
| Container-ul cade imediat | Eroare în aplicație | `docker logs <container>` |
| Spațiu insuficient | Imagini/volume vechi | `docker system prune -a` (ATENȚIE: protejați Portainer!) |

### 29.3 Probleme Portainer

| Problemă | Cauză posibilă | Soluție |
|----------|----------------|---------|
| Nu pot accesa localhost:9000 | Container oprit | `docker start portainer` |
| "Portainer already initialized" | Timeout 5 minute depășit | Ștergeți și recreați (vezi mai jos) |
| Parolă uitată | N/A | Recreați containerul |
| Portul 9000 ocupat de alt serviciu | Conflict port | Opriți serviciul care folosește 9000! |

**Recrearea Portainer:**
```bash
docker stop portainer
docker rm portainer
docker volume rm portainer_data
docker volume create portainer_data
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

### 29.4 Probleme Wireshark

| Problemă | Cauză posibilă | Soluție |
|----------|----------------|---------|
| Nu se văd interfețe | Npcap lipsă | Reinstalați Wireshark cu Npcap |
| "vEthernet (WSL)" lipsește | WSL nu rulează | Porniți Ubuntu (`wsl`) apoi reporniți Wireshark |
| Nu se capturează trafic | Interfață greșită | Selectați "vEthernet (WSL)" |
| "Permission denied" | Drepturi insuficiente | Rulați Wireshark ca Administrator |

### 29.5 Probleme Python

| Problemă | Cauză posibilă | Soluție |
|----------|----------------|---------|
| "Module not found" | Pachet neinstalat | `pip install <pachet> --break-system-packages` |
| "externally-managed-environment" | Policy Python modern | Adăugați `--break-system-packages` |
| Versiune Python greșită | Python vechi | `sudo apt install python3.11` |
| Import scapy eșuează | Dependențe lipsă | `sudo apt install python3-scapy` |

### 29.6 Probleme specifice laboratoarelor

**Săptămâna 11-14: Portainer nu răspunde după pornirea laboratorului**
```bash
# Verificați că Portainer nu a fost oprit accidental
docker ps | grep portainer

# Dacă nu apare, porniți-l
docker start portainer

# Verificați că portul 9000 e disponibil
sudo ss -tlnp | grep 9000
```

**Săptămâna 14: Echo Server nu răspunde pe portul 9000**
```bash
# CORECȚIE: Echo Server folosește portul 9090, NU 9000!
nc localhost 9090

# Portul 9000 este REZERVAT pentru Portainer
```

---

## 30. Comenzi esențiale — Fișă de referință rapidă

### 30.1 Comenzi WSL (PowerShell)

```powershell
# Status WSL
wsl --status

# Lista distribuții
wsl -l -v

# Oprire toate instanțele
wsl --shutdown

# Pornire Ubuntu
wsl -d Ubuntu-22.04

# Actualizare kernel
wsl --update

# Setare versiune implicită
wsl --set-default-version 2
```

### 30.2 Comenzi Docker

```bash
# Informații sistem
docker info
docker version

# Containere
docker ps                    # Active
docker ps -a                 # Toate
docker start <container>     # Pornire
docker stop <container>      # Oprire
docker rm <container>        # Ștergere
docker logs <container>      # Log-uri
docker exec -it <c> bash     # Shell în container

# Imagini
docker images                # Lista
docker pull <image>          # Descărcare
docker rmi <image>           # Ștergere

# Rețele
docker network ls            # Lista
docker network inspect <n>   # Detalii

# Curățare (ATENȚIE: protejați Portainer!)
docker system prune          # Resurse neutilizate
docker volume prune          # Volume neutilizate

# NU rulați: docker system prune -a (poate șterge Portainer!)
```

### 30.3 Comenzi Docker Compose

```bash
# Pornire servicii
docker compose up -d

# Oprire servicii
docker compose down

# Status
docker compose ps

# Log-uri
docker compose logs -f

# Rebuild
docker compose build --no-cache

# Oprire cu ștergere volume
docker compose down -v
```

### 30.4 Comenzi rețea Linux

```bash
# Interfețe
ip addr show
ip link show
ip -br a                     # Format scurt

# Rutare
ip route show
ip route get 8.8.8.8

# Conexiuni
ss -tulpn                    # Porturi deschise
ss -t state established      # Conexiuni active

# Testare
ping -c 4 <host>
traceroute <host>
curl -I <url>

# DNS
dig <domain>
nslookup <domain>

# Captură
sudo tcpdump -i any -n
sudo tcpdump -i eth0 port 80 -w capture.pcap
```

### 30.5 Filtre Wireshark utile

```
# Protocol
tcp
udp
icmp
http
dns
tls
mqtt

# Port
tcp.port == 80
udp.port == 53
tcp.dstport == 443
tcp.port == 9090            # Echo Server (Săpt. 14)

# NU folosiți tcp.port == 9000 pentru laboratoare
# (Portul 9000 este Portainer, nu laborator!)

# IP
ip.addr == 192.168.1.1
ip.src == 10.0.0.1
ip.dst == 8.8.8.8

# TCP flags
tcp.flags.syn == 1
tcp.flags.rst == 1
tcp.flags.fin == 1

# Combinații
tcp.port == 80 && ip.addr == 192.168.1.1
http.request.method == "GET"
dns.qry.name contains "google"

# Handshake TCP
tcp.flags.syn == 1 && tcp.flags.ack == 0    # SYN
tcp.flags.syn == 1 && tcp.flags.ack == 1    # SYN-ACK

# Filtre specifice laboratoarelor
tcp.port in {8080, 8081, 8082, 8083}        # Săpt. 11 - Load Balancing
tcp.port in {2525, 5000, 5001, 50051}       # Săpt. 12 - Email & RPC
tcp.port in {1883, 8883, 8080, 2121}        # Săpt. 13 - IoT & Security
tcp.port in {8080, 8001, 8002, 9090}        # Săpt. 14 - Recapitulare
```

### 30.6 Comenzi specifice laboratoarelor (versiunea română)

```bash
# Navigare la folder laborator (exemplu Săptămâna 14)
cd /mnt/d/RETELE/SAPT14/14roWSL

# Verificare mediu
python3 setup/verifica_mediu.py

# Pornire laborator (NU pornește Portainer - rulează deja!)
python3 scripts/porneste_lab.py

# Oprire laborator (NU oprește Portainer!)
python3 scripts/opreste_lab.py

# Verificare status
python3 scripts/porneste_lab.py --status

# Curățare
python3 scripts/curata.py --complet
```

---


---

## 31. Exerciții de nivel superior (EVALUATE & CREATE)

Aceste exerciții vizează **nivelurile cognitive superioare** din taxonomia Anderson-Bloom și sunt recomandate pentru studenții care doresc să aprofundeze materia.

### 31.1 Exerciții EVALUATE (Evaluare Critică)

#### E1. Evaluare Arhitectură Load Balancer (Săptămâna 11)

> 💭 **PREDICȚIE:** Care crezi că sunt cele mai importante criterii pentru alegerea unui algoritm de load balancing?

**Cerință:** Analizează configurația Nginx din `11roWSL/docker/configs/nginx.conf`.

1. Care sunt avantajele și dezavantajele algoritmului round-robin folosit?
2. Ce s-ar întâmpla dacă unul dintre backend-uri devine indisponibil?
3. Propune o îmbunătățire a configurației și justifică alegerea.
4. Compară round-robin cu least-connections — când ai folosi fiecare?

**Livrabil:** Raport de 1-2 pagini cu analiza și recomandările tale.

#### E2. Audit Securitate Setup IoT (Săptămâna 13)

> 💭 **PREDICȚIE:** Câte vulnerabilități potențiale crezi că există în setup-ul MQTT fără autentificare?

**Cerință:** Examinează setup-ul MQTT din `13roWSL/docker/`.

1. Identifică **minim 3 vulnerabilități** potențiale în configurația curentă.
2. Clasifică fiecare vulnerabilitate după severitate: CRITICAL / HIGH / MEDIUM / LOW.
3. Propune mitigări concrete pentru fiecare vulnerabilitate identificată.
4. Evaluează trade-off-ul între securitate și ușurința de utilizare în context educațional.

**Livrabil:** Tabel cu vulnerabilități, severități și mitigări.

#### E3. Comparație Protocoale RPC (Săptămâna 12)

**Cerință:** După ce ai experimentat cu JSON-RPC, XML-RPC și gRPC:

1. Compară cele 3 tehnologii din perspectiva: performanță, ușurință implementare, interoperabilitate.
2. Pentru ce tip de aplicație ai recomanda fiecare?
3. Care sunt dezavantajele gRPC față de JSON-RPC pentru un startup mic?

**Livrabil:** Tabel comparativ cu justificări.

---

### 31.2 Exerciții CREATE (Design Original)

#### C1. Design Protocol Binar Custom (Săptămânile 4 → 14)

> 💭 **PREDICȚIE:** De câți bytes ai nevoie minim pentru un header de protocol care să conțină: tip mesaj, lungime, și checksum?

**Cerință:** Proiectează un protocol binar pentru telemetrie IoT.

**Specificații:**
- Header fix de **8 bytes** conținând:
  - Versiune protocol (1 byte)
  - Tip mesaj (1 byte)
  - Lungime payload (2 bytes, big-endian)
  - Timestamp (4 bytes, UNIX epoch)
- Payload variabil (max 1024 bytes)
- CRC16 pentru verificare integritate (2 bytes la final)

**Livrabile:**
1. Documentație format protocol (diagramă + explicații)
2. Implementare Python encoder/decoder
3. Test cu minim 5 tipuri de mesaje diferite

#### C2. Arhitectură Microservicii (Săptămâna 14)

**Cerință:** Creează un `docker-compose.yml` original pentru o aplicație de tip "URL Shortener".

**Componente obligatorii:**
- API Gateway (Nginx) pe portul 8080
- 2 instanțe backend (Python/Flask sau Node.js)
- Bază de date (Redis sau SQLite în volum)
- Health checks pentru toate serviciile

**Livrabile:**
1. `docker-compose.yml` complet și funcțional
2. Cod sursă pentru backend
3. `README.md` cu instrucțiuni de utilizare
4. Justificarea alegerilor arhitecturale (1 pagină)

#### C3. Instrument de Diagnoză Rețea (Săptămânile 1-7)

**Cerință:** Dezvoltă un script Python care combină mai multe instrumente de diagnoză.

**Funcționalități:**
- Ping către o listă de host-uri
- Port scan pe range specificat
- Verificare DNS pentru domenii
- Export rezultate în format JSON și HTML

**Livrabile:**
1. Script Python cu argparse pentru parametri
2. Documentație utilizare
3. Exemple de output

---

## 32. Ghid Live Coding pentru Instructori

### 32.1 Principii de bază

Live coding-ul este o tehnică de predare în care instructorul scrie cod în fața studenților, explicând fiecare pas. Este **fundamental diferit** de a prezenta cod pre-scris.

### 32.2 Structura unei sesiuni de Live Coding

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CICLUL LIVE CODING (15-20 minute)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. CONTEXT (2 min)      Prezintă problema și obiectivul                   │
│         │                                                                   │
│         ▼                                                                   │
│  2. STRUCTURĂ (2 min)    Schițează structura generală a soluției           │
│         │                                                                   │
│         ▼                                                                   │
│  3. IMPLEMENTARE         Scrie cod în pași de 2-5 linii                    │
│     INCREMENTALĂ         ┌──────────────────────────────────────┐          │
│     (10-15 min)          │  a) Scrie 2-5 linii                  │          │
│                          │  b) ÎNTREABĂ: "Ce va afișa asta?"    │          │
│                          │  c) Rulează și verifică              │          │
│                          │  d) Repetă                           │          │
│                          └──────────────────────────────────────┘          │
│         │                                                                   │
│         ▼                                                                   │
│  4. RECAPITULARE (2 min) Rezumă ce am construit și de ce                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 32.3 Reguli de aur

1. **GREȘEȘTE INTENȚIONAT** — Fă o greșeală și arată cum o depanezi
2. **CERE PREDICȚII** — Înainte de fiecare `python3 script.py`, întreabă "Ce va afișa?"
3. **VORBEȘTE ÎN TIMP CE TASTEZI** — Explică fiecare linie
4. **NU TE GRĂBI** — Mai bine acoperi mai puțin, dar studenții înțeleg
5. **FOLOSEȘTE COMENTARII** — Adaugă comentarii explicative pe loc

### 32.4 Exemplu pentru Săptămâna 2 (Socket TCP)

```python
# PASUL 1: "Să creăm un socket TCP simplu"
import socket

# ÎNTREBARE: "Ce tip de socket folosim pentru TCP?"
# Răspuns așteptat: SOCK_STREAM

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket creat!")

# RULEAZĂ → verifică output

# PASUL 2: "Acum să ne conectăm la un server"
# ÎNTREBARE: "Ce se întâmplă dacă serverul nu rulează?"

sock.connect(('localhost', 8080))
print("Conectat!")

# RULEAZĂ → probabil eroare! → DEPANĂM ÎMPREUNĂ
```

### 32.5 Checklist pre-sesiune

- [ ] Am testat tot codul înainte?
- [ ] Am pregătit 2-3 greșeli intenționate de demonstrat?
- [ ] Am pregătit întrebări de predicție pentru fiecare pas?
- [ ] Fontul în terminal este suficient de mare (min 18pt)?
- [ ] Am dezactivat notificările pe ecran?

---

## 33. FAQ — Întrebări Frecvente

### Probleme de instalare și configurare

**Q: Primesc "Address already in use" când pornesc laboratorul.**

> **A:** Un alt proces folosește deja portul. Identifică-l și oprește-l:
> ```bash
> # Găsește procesul
> ss -tulpn | grep <port>
> # Sau pe Windows
> netstat -ano | findstr <port>
> ```
> Apoi oprește procesul sau schimbă portul în `docker-compose.yml`.

**Q: Docker nu pornește în WSL. Ce fac?**

> **A:** Pornește manual serviciul:
> ```bash
> sudo service docker start
> # Parolă: stud
> ```
> Dacă persistă, verifică dacă WSL2 este configurat corect: `wsl --status`

**Q: Portainer nu se deschide la http://localhost:9000.**

> **A:** Verifică dacă containerul Portainer rulează:
> ```bash
> docker ps | grep portainer
> ```
> Dacă nu rulează, pornește-l:
> ```bash
> docker start portainer
> # Sau recreează-l conform instrucțiunilor din Secțiunea 7
> ```

**Q: Nu am spațiu pe disc pentru imagini Docker.**

> **A:** Curăță resursele neutilizate:
> ```bash
> docker system prune -a
> # ATENȚIE: Șterge TOATE imaginile neutilizate!
> ```

### Probleme în timpul laboratoarelor

**Q: Containerul pornește dar serviciul nu răspunde.**

> **A:** Verifică log-urile containerului:
> ```bash
> docker logs <container_name>
> # Sau în Portainer: click pe container → Logs
> ```

**Q: Wireshark nu vede traficul din containere.**

> **A:** În WSL, traficul Docker trece prin interfața `docker0` sau bridge-ul specific. Folosește:
> ```bash
> # În Wireshark pe Windows, selectează "Adapter for loopback traffic capture"
> # Sau folosește tcpdump în WSL:
> sudo tcpdump -i any port <port> -w captura.pcap
> ```

**Q: Cum resetez complet un laborator?**

> **A:** Folosește scriptul de curățare:
> ```bash
> python3 scripts/curata.py --complet
> # Apoi repornește:
> python3 scripts/porneste_lab.py --rebuild
> ```

### Întrebări conceptuale

**Q: Care e diferența între Docker și o mașină virtuală?**

> **A:** Containerele Docker împart kernel-ul cu host-ul și sunt mult mai ușoare (~MB vs ~GB). 
> VM-urile au propriul kernel și oferă izolare completă dar cu overhead mai mare.

**Q: De ce folosim WSL2 și nu Docker Desktop?**

> **A:** WSL2 oferă:
> - Performanță mai bună (kernel Linux nativ)
> - Consum de resurse mai mic
> - Control complet asupra configurației
> - Competențe Linux transferabile
> - Licențiere complet gratuită

**Q: Portul 9000 e pentru laborator?**

> **A:** **NU!** Portul 9000 este **REZERVAT PERMANENT** pentru Portainer. 
> Laboratoarele folosesc alte porturi (8080, 8081, 9090, etc.).


## 34. Licență

Acest proiect este licențiat sub **Licență Educațională Restrictivă** (v5.0.0).

### Notificare privind Drepturile de Autor

**© 2019–2026 Antonio Clim, Andrei Toma. Toate drepturile rezervate.**

Materialele sunt protejate în conformitate cu legislația română (Legea nr. 8/1996), Directiva UE 2001/29/CE și tratatele internaționale aplicabile.

### Utilizări Permise

| Permis | Descriere |
|:------:|-----------|
| ✓ | **Studiu Personal** — Vizualizare, citire și studiu pentru beneficiu educațional propriu |
| ✓ | **Executare Cod** — Rulare exemple de cod pe dispozitive personale în scopuri de învățare |
| ✓ | **Modificare Locală** — Modificare cod local pentru experimentare și învățare personală |
| ✓ | **Note Personale** — Creare note derivate și adnotări doar pentru referință personală |
| ✓ | **Citare Academică** — Citare fragmente scurte în lucrări academice cu atribuire corectă |

### Utilizări Interzise (fără consimțământ scris)

| Interzis | Descriere |
|:--------:|-----------|
| ✗ | **Publicare** — Încărcare, postare, publicare sau partajare pe orice platformă |
| ✗ | **Predare** — Utilizare în cursuri, workshopuri, seminarii sau training fără autorizare |
| ✗ | **Prezentare** — Prezentare, demonstrare sau afișare către audiențe |
| ✗ | **Redistribuire** — Distribuire copii în orice formă, modificate sau nu |
| ✗ | **Lucrări Derivate** — Creare și distribuire lucrări derivate |
| ✗ | **Utilizare Comercială** — Orice scop comercial |

### Licențierea pentru Instituții de Învățământ

Instituțiile de învățământ care doresc să încorporeze aceste Materiale în curricula lor pot solicita o licență instituțională. Deschideți un issue cu tag-ul `[LICENCE]` pentru detalii.

### Atribuire

Când citați aceste Materiale în lucrări academice:

```
Clim, A., & Toma, A. (2026). Rețele de Calculatoare — Kit-uri Complete de Laborator 
(Ediție WSL, v5.0.0). Academia de Studii Economice București.
https://github.com/antonioclim/netROwsl
```

**Format BibTeX:**

```bibtex
@misc{clim2026retele,
  author       = {Clim, Antonio and Toma, Andrei},
  title        = {{netROwsl}: Rețele de Calculatoare — Kit-uri Complete de Laborator},
  year         = {2026},
  version      = {5.0.0},
  institution  = {Academia de Studii Economice București},
  howpublished = {\url{https://github.com/antonioclim/netROwsl}},
  note         = {Materiale curriculare educaționale pentru laboratorul 
                  de rețele de calculatoare}
}
```

**Licența completă:** [LICENSE.md](LICENSE.md)

**Declinare:** Materialele sunt furnizate „CA ATARE" fără garanție de orice fel.

---

## 🎓 Succes la laborator!

Dacă ați parcurs acest ghid și ați configurat mediul corect, sunteți pregătiți să:

- ✅ Rulați experimente de rețea izolate cu containere Docker
- ✅ Capturați și analizați traficul de rețea cu Wireshark
- ✅ Gestionați containerele prin interfața web Portainer (http://localhost:9000)
- ✅ Automatizați sarcini de rețea cu Python
- ✅ Înțelegeți în profunzime cum funcționează protocoalele de rețea
- ✅ Evitați conflictele de porturi (portul 9000 = Portainer!)

---

## 📊 Rezumat modificări principale (Ianuarie 2026)

Acest document a fost actualizat pentru a reflecta:

1. **Licență Educațională Restrictivă** — Înlocuirea MIT cu licență restrictivă pentru protecția materialelor
2. **Atribuire corectă** — © 2019–2026 Antonio Clim, Andrei Toma
3. **17 întrebări PREDICȚIE** — Prompt-uri de predicție pentru fiecare săptămână
4. **Două repository-uri separate** — netENwsl (Engleză) și netROwsl (Română)
5. **Convenții de denumire distincte** — `<N>enWSL` vs `<NN>roWSL`
6. **Structură directoare pentru studenți** — `D:\RETELE\SAPT<N>\<NN>roWSL`
7. **Portul 9000 REZERVAT PERMANENT** pentru Portainer
8. **Subgoal labels** — Comentarii structurate în cod pentru pedagogie
9. **Filtre Wireshark specifice** pentru fiecare săptămână
10. **Format BibTeX** pentru citări academice

---

> **© 2019–2026 Antonio Clim, Andrei Toma**  
> Laborator Rețele de Calculatoare — ASE București, CSIE  
> Versiune documentație: Ianuarie 2026
