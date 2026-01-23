# Săptămâna 8: Nivelul Transport — Server HTTP și Proxy Invers

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică
> 
> de Revolvix

---

## 📑 Cuprins

- [Notificare Mediu](#️-notificare-mediu)
- [Clonarea Laboratorului](#-clonarea-laboratorului-acestei-săptămâni)
- [Configurarea Inițială](#-configurarea-inițială-a-mediului-doar-prima-dată)
- [Portainer](#️-înțelegerea-interfeței-portainer)
- [Wireshark](#-configurarea-și-utilizarea-wireshark)
- [Teorie](#prezentare-generală)
  - [TCP vs UDP](#tcp-vs-udp)
  - [Proxy Invers](#arhitectura-proxy-invers)
- [Exerciții de Laborator](#exerciții-de-laborator)
  - [Ex. 1: Server HTTP](#exercițiul-1-server-http-de-bază)
  - [Ex. 2: Proxy Invers](#exercițiul-2-proxy-invers-cu-echilibrare-round-robin)
- [Peer Instruction](#-secțiune-peer-instruction)
- [Demonstrații](#demonstrații)
- [Depanare](#-depanare-extinsă)
- [Curățare](#-procedura-completă-de-curățare)

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

**🔮 PREDICȚIE:** Ce foldere și fișiere te aștepți să vezi după clonare? Notează cel puțin 5 foldere pe care le anticipezi.

```powershell
dir
# Ar trebui să vezi: 08roWSL/
cd 08roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, www/, README.md, etc.
```

**Verificare:** Compară cu predicția ta. Ai găsit toate folderele așteptate? Lipsește vreunul?

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

**🔮 PREDICȚIE:** Câte containere crezi că vor apărea în output-ul `docker ps` dacă Docker tocmai a pornit?

```bash
# Pornește Docker (necesar după fiecare restart Windows)
sudo service docker start
# Parolă: stud

# Verifică că Docker rulează
docker ps
```

**Verificare:** Ai văzut containerul `portainer`? Dacă nu, consultă secțiunea Depanare.

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

### 💡 De la Concret la Abstract: Portainer

**CONCRET (analogie):**
> Portainer este ca un **panou de control pentru un terminal de containere maritime**. În loc să mergi fizic la fiecare container să verifici ce e înăuntru, stai într-o cameră de control cu ecrane care îți arată starea tuturor containerelor: care sunt încărcate (running), care sunt goale (stopped), ce conțin (logs), și poți trimite comenzi către oricare dintre ele.

**PICTORIAL:**
```
┌────────────────────────────────────────────────────────────┐
│                    PORTAINER (localhost:9000)              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  📦 week8-nginx-proxy     [▶ Running]  [Logs] [Stop] │  │
│  │  📦 week8-backend-1       [▶ Running]  [Logs] [Stop] │  │
│  │  📦 week8-backend-2       [▶ Running]  [Logs] [Stop] │  │
│  │  📦 week8-backend-3       [▶ Running]  [Logs] [Stop] │  │
│  └──────────────────────────────────────────────────────┘  │
│  [Networks]  [Volumes]  [Images]  [Stacks]                 │
└────────────────────────────────────────────────────────────┘
```

**ABSTRACT:**
```bash
# Portainer face vizual ce aceste comenzi fac în terminal:
docker ps                    # Lista containere
docker logs <container>      # Vizualizare jurnale
docker stop <container>      # Oprire container
docker network ls            # Lista rețele
```

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor pentru Săptămâna 8

Navighează: **Home → local → Containers**

**🔮 PREDICȚIE:** Înainte de a naviga, câte containere crezi că vei vedea pentru laborator? Ce nume vor avea?

Vei vedea containerele specifice laboratorului:
- **week8-nginx-proxy** - Proxy invers nginx (172.28.8.10:8080/8443)
- **week8-backend-1** - Backend Alpha (172.28.8.21:8080 intern)
- **week8-backend-2** - Backend Beta (172.28.8.22:8080 intern)
- **week8-backend-3** - Backend Gamma (172.28.8.23:8080 intern)

**Verificare:** Ai ghicit corect numărul și numele? Toate sunt în starea "Running"?

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

### Pasul 2: Selectează Interfața de Captură

**CRITIC:** Selectează interfața corectă pentru traficul WSL:

| Numele Interfeței | Când să Folosești |
|-------------------|-------------------|
| **vEthernet (WSL)** | ✅ Cel mai frecvent - capturează traficul Docker WSL |
| **Loopback Adapter** | Doar pentru trafic localhost (127.0.0.1) |

### Pasul 3: Generează Trafic

**🔮 PREDICȚIE:** Câte pachete TCP crezi că vor fi necesare pentru a stabili o conexiune HTTP? (Hint: gândește-te la handshake)

Cu Wireshark capturând, rulează:

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT8/08roWSL

# Test proxy HTTP
curl -i http://localhost:8080/
```

**Verificare:** Ai văzut cele 3 pachete de handshake (SYN, SYN-ACK, ACK) urmate de cererea HTTP?

### Filtre Wireshark Esențiale pentru Săptămâna 8

**Filtre pentru Trafic HTTP:**

| Filtru | Scop |
|--------|------|
| `http` | Tot traficul HTTP |
| `http.request` | Doar cereri HTTP |
| `http.response` | Doar răspunsuri HTTP |
| `http.response.code == 200` | Răspunsuri OK |

**Filtre pentru Analiza TCP:**

| Filtru | Ce să observi |
|--------|---------------|
| `tcp.flags.syn == 1` | Pachete SYN |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Doar SYN inițial |
| `tcp.flags.syn == 1 && tcp.flags.ack == 1` | SYN-ACK |
| `tcp.flags.fin == 1` | Închidere conexiuni |

### 💡 De la Concret la Abstract: TCP Three-Way Handshake

**CONCRET (analogie):**
> Ca un apel telefonic politicos:
> 1. **Tu:** "Alo, mă auzi?" (SYN)
> 2. **Ei:** "Da, te aud. Tu mă auzi?" (SYN-ACK)
> 3. **Tu:** "Da, te aud." (ACK)
> 
> Acum puteți vorbi. Nimeni nu începe să vorbească până nu confirmă că celălalt ascultă.

**PICTORIAL:**
```
Client                              Server
  │                                    │
  │ ──── SYN (seq=100) ──────────────► │  "Vreau să vorbim"
  │                                    │
  │ ◄──── SYN-ACK (seq=300, ack=101) ─ │  "OK, și eu vreau"
  │                                    │
  │ ──── ACK (ack=301) ───────────────►│  "Perfect, începem"
  │                                    │
  │ ════════ CONEXIUNE STABILITĂ ══════│
  │                                    │
  │ ──── HTTP GET / ──────────────────►│  Cererea ta
  │ ◄──── HTTP 200 OK ─────────────────│  Răspunsul
```

**ABSTRACT (filtru Wireshark):**
```
tcp.flags.syn == 1 && tcp.flags.ack == 0   → Pachet #1 (SYN)
tcp.flags.syn == 1 && tcp.flags.ack == 1   → Pachet #2 (SYN-ACK)  
tcp.flags.syn == 0 && tcp.flags.ack == 1   → Pachet #3+ (ACK, date)
```

---

## Prezentare Generală

Nivelul transport reprezintă fundamentul comunicării fiabile între aplicații în rețelele de calculatoare. Acest nivel asigură transferul de date între procesele care rulează pe gazde diferite, oferind servicii de multiplexare, demultiplexare și, în cazul TCP, transfer fiabil de date cu control al fluxului și al congestiei.

În cadrul acestei sesiuni de laborator, vom studia implementarea practică a protocoalelor de nivel transport prin construirea unui server HTTP de la zero și configurarea unui proxy invers cu echilibrare a încărcării. Aceste exerciții demonstrează modul în care protocoalele de nivel aplicație se bazează pe serviciile oferite de TCP pentru a realiza comunicarea client-server.

Infrastructura de laborator folosește Docker pentru a crea un mediu izolat și reproductibil, cu nginx ca proxy invers și mai multe servere backend Python. Această arhitectură reflectă configurațiile reale din producție și oferă experiență practică cu algoritmi de echilibrare a încărcării.

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

**🔮 PREDICȚIE:** Câte containere crezi că vor porni? Ce nume vor avea?

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT8/08roWSL

# Porniți toate serviciile
python3 scripts/porneste_laborator.py

# Verificați că totul funcționează
python3 scripts/porneste_laborator.py --status
```

**Verificare:** Ai văzut 4 containere (nginx + 3 backend-uri)? Dacă nu, consultă secțiunea Depanare.

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Proxy HTTP | http://localhost:8080 | - |
| Proxy HTTPS | https://localhost:8443 | Certificat auto-semnat |
| Backend 1 | intern: 172.28.8.21:8080 | - |
| Backend 2 | intern: 172.28.8.22:8080 | - |
| Backend 3 | intern: 172.28.8.23:8080 | - |

**🔮 PREDICȚIE:** De ce crezi că backend-urile nu au porturi expuse direct (precum 8081, 8082, 8083)? Ce avantaj oferă accesul doar prin proxy?

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

---

## 🗳️ SECȚIUNE PEER INSTRUCTION

### PI-1: TCP Three-Way Handshake

**Scenariu:**
Un client dorește să stabilească o conexiune TCP cu un server web.

**Întrebare:**
Care este ordinea corectă a flag-urilor TCP în three-way handshake?

**Opțiuni:**
- A) ACK → SYN-ACK → SYN
- B) SYN → ACK → SYN-ACK
- C) SYN → SYN-ACK → ACK
- D) SYN → SYN → ACK

<details>
<summary>📋 Note Instructor</summary>

**Răspuns corect:** C

**Țintă:** ~50% corect la primul vot

**Analiza distractorilor:**
- **A:** Studenții care inversează ordinea (confundă cine începe)
- **B:** Studenții care confundă pozițiile ACK și SYN-ACK
- **D:** Studenții care cred că serverul trimite SYN simplu, nu SYN-ACK

**După discuție:** Desenează diagrama cu săgeți și explică de ce serverul răspunde cu SYN-ACK (confirmă SYN-ul clientului ȘI trimite propriul SYN).

**Timing:** Prezentare (1 min) → Vot (1 min) → Discuție (3 min) → Revot (30 sec)
</details>

---

### PI-2: Docker Port Mapping

**Scenariu:**
```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

**Întrebare:**
Pentru a accesa nginx din browser pe Windows, ce URL folosești?

**Opțiuni:**
- A) http://localhost:80
- B) http://localhost:8080
- C) http://nginx:80
- D) http://172.28.8.10:80

<details>
<summary>📋 Note Instructor</summary>

**Răspuns corect:** B

**Analiza distractorilor:**
- **A:** Confundă portul containerului (80) cu portul expus (8080)
- **C:** Crede că numele serviciului se rezolvă din afara Docker
- **D:** Încearcă să folosească IP-ul intern Docker din Windows

**După discuție:** Desenează: `Windows:8080 ──► Container:80`
</details>

---

### PI-3: Proxy Headers (X-Forwarded-For)

**Scenariu:**
```
Client (IP: 192.168.1.100) ──► nginx proxy ──► backend server
```

**Întrebare:**
Fără header-ul X-Forwarded-For, ce IP vede backend-ul în cererea HTTP?

**Opțiuni:**
- A) 192.168.1.100 (IP-ul clientului original)
- B) IP-ul proxy-ului nginx
- C) 127.0.0.1 (localhost)
- D) Nu se poate determina

<details>
<summary>📋 Note Instructor</summary>

**Răspuns corect:** B

**Concept cheie:** Proxy-ul rescrie cererea. Backend-ul vede conexiunea venind de la proxy, nu de la client.

**De aceea există X-Forwarded-For:** Pentru a păstra IP-ul original al clientului.
</details>

---

### PI-4: Round-Robin Load Balancing

**Scenariu:**
3 backend-uri configurate: Alpha, Beta, Gamma
Algoritm: round-robin (fără ponderi)

**Întrebare:**
Dacă trimiți 7 cereri consecutive, care backend primește cererea #7?

**Opțiuni:**
- A) Alpha (primul)
- B) Beta (al doilea)
- C) Gamma (al treilea)
- D) Aleatoriu, depinde de încărcare

<details>
<summary>📋 Note Instructor</summary>

**Răspuns corect:** A

**Calcul:** 
- Cereri 1,4,7 → Alpha
- Cereri 2,5 → Beta  
- Cereri 3,6 → Gamma
- 7 mod 3 = 1 → Alpha

**Distractori:**
- **D:** Confundă round-robin cu random sau least-connections
</details>

---

### PI-5: HTTP Response Codes (Security)

**Scenariu:**
Serverul tău HTTP primește cererea:
```
GET /../../../etc/passwd HTTP/1.1
Host: localhost
```

**Întrebare:**
Ce cod HTTP ar trebui să returneze un server securizat?

**Opțiuni:**
- A) 404 Not Found
- B) 403 Forbidden
- C) 400 Bad Request
- D) 500 Internal Server Error

<details>
<summary>📋 Note Instructor</summary>

**Răspuns corect:** B (403 Forbidden)

**Analiza:**
- **A:** Incorect — fișierul poate exista, dar accesul e interzis
- **B:** Corect — path traversal = acces interzis din motive de securitate
- **C:** Incorect — cererea e validă din punct de vedere sintactic
- **D:** Incorect — nu e o eroare de server, e o decizie de securitate

**Concept cheie:** Diferența între "nu există" (404) și "nu ai voie" (403).
</details>

---

### PI-6: Health Check și Failover

**Scenariu:**
Load balancer cu 3 backend-uri. Backend-2 devine indisponibil (crashed).

**Întrebare:**
Ce se întâmplă cu cererile care ar fi mers la Backend-2?

**Opțiuni:**
- A) Returnează eroare 503 Service Unavailable
- B) Se redistribuie automat la Backend-1 și Backend-3
- C) Așteaptă până când Backend-2 revine online
- D) Toate cererile merg doar la Backend-1

<details>
<summary>📋 Note Instructor</summary>

**Răspuns corect:** B

**Concept cheie:** Health check-urile detectează backend-uri nesănătoase și le exclud temporar din rotație.

**Distractori:**
- **A:** Ar fi adevărat doar dacă TOATE backend-urile ar fi down
- **C:** Ar bloca toate cererile — design foarte prost
- **D:** Ignoră existența Backend-3
</details>

---

### PI-7: TCP vs UDP pentru Streaming

**Scenariu:**
Dezvolți o aplicație de video streaming live.

**Întrebare:**
Ce protocol de transport este mai potrivit?

**Opțiuni:**
- A) TCP, pentru că garantează livrarea tuturor pachetelor
- B) UDP, pentru că tolerează pierderi și are latență mai mică
- C) TCP, pentru că streaming-ul necesită ordonare strictă
- D) HTTP/3, care folosește TCP pentru fiabilitate

<details>
<summary>📋 Note Instructor</summary>

**Răspuns corect:** B

**Analiza:**
- La streaming LIVE, un frame pierdut de acum 2 secunde e irelevant
- Retransmisia TCP ar introduce lag inacceptabil
- E mai bine să pierzi un frame decât să întârzii toate următoarele

**Notă:** HTTP/3 folosește QUIC care e peste UDP, nu TCP!
</details>

---

### PI-8: Docker Network Isolation

**Scenariu:**
```yaml
services:
  frontend:
    networks: [webnet]
  backend:
    networks: [webnet, dbnet]
  database:
    networks: [dbnet]
```

**Întrebare:**
Poate containerul `frontend` să comunice direct cu containerul `database`?

**Opțiuni:**
- A) Da, sunt în același docker-compose.yml
- B) Da, folosind IP-ul containerului database
- C) Nu, sunt pe rețele Docker diferite fără suprapunere
- D) Depinde de configurația firewall-ului

<details>
<summary>📋 Note Instructor</summary>

**Răspuns corect:** C

**Concept cheie:** 
- `frontend` e doar pe `webnet`
- `database` e doar pe `dbnet`
- Nu există nicio rețea comună → nu pot comunica direct

**Diagrama:**
```
webnet:    [frontend] ←→ [backend]
dbnet:                   [backend] ←→ [database]
```

`backend` e pe ambele rețele, deci poate fi "punte", dar direct frontend↔database nu merge.
</details>

---

## Exerciții de Laborator

### Exercițiul 1: Server HTTP de Bază

**Obiectiv:** Implementarea unui server HTTP simplu care servește fișiere statice.

**Durată:** 45-60 minute

**Fișier:** `src/exercises/ex_8_01_server_http.py`

#### 💡 De la Concret la Abstract: Server HTTP

**CONCRET (analogie):**
> Un server HTTP e ca un **bibliotecar**. 
> - Clientul (tu) vine și cere o carte (fișier): "Vreau cartea 'index.html'"
> - Bibliotecarul verifică dacă ai voie să o iei (securitate)
> - Caută cartea pe raft (sistem de fișiere)
> - Dacă există, ți-o dă (200 OK + conținut)
> - Dacă nu există, îți spune "Nu avem" (404 Not Found)
> - Dacă e în secțiunea restricționată, îți spune "Nu ai acces" (403 Forbidden)

**PICTORIAL:**
```
┌─────────────────────────────────────────────────────────┐
│                    SERVER HTTP                          │
│                                                         │
│   Cerere GET /hello.txt                                │
│        │                                                │
│        ▼                                                │
│   ┌─────────────┐    ┌─────────────┐    ┌───────────┐  │
│   │ Parsează    │ → │ Verifică    │ → │ Citește   │  │
│   │ cererea     │    │ securitatea │    │ fișierul  │  │
│   └─────────────┘    └─────────────┘    └───────────┘  │
│        │                   │                   │        │
│        ▼                   ▼                   ▼        │
│   Metoda: GET         Cale sigură?       Fișier există? │
│   Cale: /hello.txt    ✓ Da / ✗ 403      ✓ 200 / ✗ 404  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**ABSTRACT:**
```python
def handle_request(raw_request: bytes, docroot: str) -> bytes:
    method, path, version, headers = parse_request(raw_request)
    
    if not is_safe_path(path, docroot):
        return build_response(403, {}, b"Forbidden")
    
    status, headers, body = serve_file(path, docroot)
    return build_response(status, headers, body)
```

#### Pași de Implementare

1. Deschideți fișierul exercițiului și examinați structura codului
2. Implementați funcția `parse_request()` pentru a extrage metoda, calea și versiunea HTTP
3. Implementați funcția `is_safe_path()` pentru a preveni traversarea directoarelor
4. Implementați funcția `serve_file()` pentru a citi și returna conținutul fișierelor
5. Implementați funcția `build_response()` pentru a formata răspunsul HTTP
6. Testați serverul cu curl și browser

#### Verificare

**🔮 PREDICȚIE:** Ce cod HTTP aștepți pentru `/hello.txt`? Dar pentru `/../etc/passwd`?

```bash
# Porniți serverul
python3 src/exercises/ex_8_01_server_http.py

# Într-un alt terminal, testați
curl -i http://localhost:8888/hello.txt
curl -I http://localhost:8888/index.html
curl -i http://localhost:8888/../../../etc/passwd
```

**Verificare:** Ai obținut 200 pentru hello.txt, 200 pentru index.html, și 403 pentru path traversal?

**Rezultat Așteptat:**
- Răspuns 200 OK pentru fișiere existente
- Răspuns 404 Not Found pentru fișiere inexistente
- Răspuns 403 Forbidden pentru încercări de traversare a directoarelor

---

### 👥 EXERCIȚIU ÎN PERECHI: Implementare parse_request()

**Timp:** 15 minute
**Roluri:** Driver (scrie cod) | Navigator (ghidează, verifică)

#### Instrucțiuni
1. Decideți cine e Driver și cine e Navigator
2. La jumătatea timpului (7 min), schimbați rolurile
3. Navigatorul NU atinge tastatura, doar ghidează verbal

#### Sarcina Driver (prima jumătate)
Implementează pașii 1-3 din funcția `parse_request()`:
- Decodifică bytes în string
- Split pe `\r\n` pentru a obține liniile
- Parsează prima linie (request line): metodă, cale, versiune

#### Sarcina Navigator (verifică)
- [ ] Codul tratează cereri invalide (linii insuficiente)?
- [ ] Decodificarea folosește `utf-8`?
- [ ] Split-ul e pe `\r\n`, nu pe `\n`?

#### Schimbare Roluri (după 7 minute)

#### Sarcina Driver (a doua jumătate)
Implementează pașii 4-5:
- Parsează headers în dicționar (key: value)
- Normalizează cheile la lowercase

#### Discuție Finală (2 minute)
- Ce a fost mai greu: să scrii sau să ghidezi?
- Ce edge cases ați descoperit împreună?

---

### Exercițiul 2: Proxy Invers cu Echilibrare Round-Robin

**Obiectiv:** Implementarea unui proxy invers care distribuie cererile între mai multe backend-uri.

**Durată:** 60-75 minute

**Fișier:** `src/exercises/ex_8_02_proxy_invers.py`

#### 💡 De la Concret la Abstract: Reverse Proxy

**CONCRET (analogie):**
> Imaginează-ți un **recepționer la un hotel mare** cu 3 lifturi identice.
> - Oaspeții (clienții) vin la recepție și cer să urce
> - Recepționerul (proxy) nu-i lasă să aleagă lift-ul
> - Îi direcționează pe rând: primul la liftul 1, al doilea la liftul 2, al treilea la liftul 3, al patrulea iar la liftul 1...
> - Dacă un lift e defect (backend down), recepționerul nu mai trimite pe nimeni acolo

**PICTORIAL:**
```
   Clienți             Recepționer              Lifturi (Backend-uri)
   ┌─────┐                                     ┌─────────────────┐
   │ 👤1 │ ────────►  ┌─────────────┐  ──1──► │ Lift 1 (Alpha)  │
   │ 👤2 │            │   nginx     │          │                 │
   │ 👤3 │ ◄────────  │  (proxy)    │  ──2──► │ Lift 2 (Beta)   │
   │ 👤4 │            │  :8080      │          │                 │
   │ 👤5 │            └─────────────┘  ──3──► │ Lift 3 (Gamma)  │
   └─────┘               ▲    │                └─────────────────┘
                         │    │
                    cerere    răspuns
                    
   Distribuție: 👤1→Lift1, 👤2→Lift2, 👤3→Lift3, 👤4→Lift1, 👤5→Lift2...
```

**ABSTRACT:**
```python
class RoundRobinBalancer:
    def __init__(self, backends):
        self.backends = backends
        self.current = 0
    
    def next_backend(self):
        backend = self.backends[self.current]
        self.current = (self.current + 1) % len(self.backends)
        return backend
```

#### Pași de Implementare

1. Examinați clasa `RoundRobinBalancer` și înțelegeți algoritmul
2. Implementați metoda `next_backend()` pentru selecția ciclică
3. Implementați funcția `forward_request()` pentru proxy-ul către backend
4. Adăugați antetul `X-Forwarded-For` pentru a păstra IP-ul clientului original
5. Testați distribuția cererilor

#### Verificare

**🔮 PREDICȚIE:** Dacă trimiți 6 cereri, în ce ordine vor răspunde backend-urile?

```bash
# Porniți 3 servere backend (în terminale separate)
python3 -m http.server 8001 --directory www/
python3 -m http.server 8002 --directory www/
python3 -m http.server 8003 --directory www/

# Porniți proxy-ul
python3 src/exercises/ex_8_02_proxy_invers.py

# Testați distribuția
for i in {1..6}; do echo "Cerere $i:"; curl -s http://localhost:8000/ | head -1; done
```

**Verificare:** Ai văzut pattern-ul 1→2→3→1→2→3? Dacă nu, verifică implementarea `next_backend()`.

---

### 👥 EXERCIȚIU ÎN PERECHI: Debug Health Check

**Timp:** 15 minute
**Roluri:** Driver (scrie cod) | Navigator (testează)

#### Instrucțiuni
1. Decideți cine e Driver și cine e Navigator
2. Driver-ul implementează, Navigator-ul testează în paralel
3. La jumătatea timpului, schimbați rolurile

#### Sarcina Driver (prima jumătate)
Implementează funcția `check_backend_health()`:
- Creează socket TCP
- Setează timeout 2 secunde
- Trimite `HEAD / HTTP/1.1\r\n\r\n`
- Returnează True dacă primește răspuns

#### Sarcina Navigator (testează)
Pornește/oprește un backend și verifică:
- [ ] Health check returnează True când backend-ul rulează?
- [ ] Health check returnează False după oprirea backend-ului?
- [ ] Timeout-ul de 2 secunde funcționează?

#### Schimbare Roluri (după 7 minute)

#### Sarcina Driver (a doua jumătate)
Adaugă logging pentru debugging:
```python
print(f"[HEALTH] Checking {backend}...")
print(f"[HEALTH] Result: {'healthy' if result else 'unhealthy'}")
```

---

## 💡 De la Concret la Abstract: Port Mapping Docker

**CONCRET (analogie):**
> Imaginează-ți un **bloc de apartamente** (host-ul Windows).
> - Adresa blocului = IP-ul host-ului (`localhost`)
> - Fiecare apartament are un număr = portul containerului (`80`)
> - Dar cutia poștală de la intrare are alt număr = portul expus (`8080`)
> - Când trimiți o scrisoare la "Bloc, cutia 8080", portarul o duce la "Apartamentul 80"

**PICTORIAL:**
```
┌─────────────────────────────────────────────────────────┐
│              BLOC (Windows Host - localhost)            │
│                                                         │
│   Intrare (porturi expuse)        Apartamente (containere)
│   ┌─────────────────┐             ┌─────────────────┐   │
│   │ Cutia 8080 ─────────────────► │ Apt 80 (nginx)  │   │
│   │ Cutia 8443 ─────────────────► │ Apt 443 (nginx) │   │
│   │ Cutia 9000 ─────────────────► │ Apt 9000 (Port.)│   │
│   └─────────────────┘             └─────────────────┘   │
│                                                         │
│   Din exterior accesezi                                 │
│   localhost:8080                                        │
│   care ajunge la                                        │
│   container:80                                          │
└─────────────────────────────────────────────────────────┘
```

**ABSTRACT:**
```yaml
ports:
  - "8080:80"      # host_port:container_port
  - "8443:443"     # HTTPS
  
# Formatul: "PORT_EXPUS:PORT_INTERN"
# Din Windows: localhost:8080
# În container: aplicația ascultă pe :80
```

---

## Demonstrații

### Demo 1: Proxy nginx cu Docker

**🔮 PREDICȚIE:** Dacă oprești Backend-2 în timpul testării, ce se întâmplă cu cererile? Vor eșua sau vor merge la alte backend-uri? Dacă oprești toate backend-urile, ce cod HTTP va returna nginx?

```bash
python3 scripts/ruleaza_demo.py --demo docker-nginx
```

**Ce să observați:**
- Distribuția uniformă a cererilor între cele 3 backend-uri
- Antetele X-Backend-ID și X-Backend-Name în răspunsuri
- Contorul de cereri pentru fiecare backend

**Verificare:** Încearcă să oprești un backend (`docker stop week8-backend-2`) și observă comportamentul.

### Demo 2: Algoritmi de Echilibrare

```bash
python3 scripts/ruleaza_demo.py --demo echilibrare
```

**🔮 PREDICȚIE:** La weighted round-robin cu ponderi 5:3:1, din 9 cereri câte va primi fiecare backend?

**Ce să observați:**
- Round-robin: distribuție egală (1→2→3→1→2→3)
- Weighted: distribuție proporțională (5:3:1)
- Least-connections: rutare dinamică
- IP-hash: persistența sesiunii

**Verificare:** Pentru weighted 5:3:1 și 9 cereri: Backend1=5, Backend2=3, Backend3=1

### Demo 3: Handshake TCP

```bash
python3 scripts/ruleaza_demo.py --demo handshake
```

**🔮 PREDICȚIE:** În Wireshark, ce porturi sursă și destinație vei vedea pentru pachetul SYN? Portul sursă va fi fix sau aleatoriu? De ce?

**Ce să observați în Wireshark:**
- Pachetul SYN inițial de la client (port sursă aleatoriu, destinație 8080)
- Răspunsul SYN-ACK de la server (inversare porturi)
- Confirmarea ACK de la client

**🔮 PREDICȚIE BONUS:** Dacă clientul trimite o cerere HTTP după handshake, câte pachete TCP în total vor fi schimbate pentru o singură cerere GET simplă? (Hint: handshake + cerere + răspuns + închidere)

---

## Concepte Teoretice

### TCP vs UDP

**🔮 PREDICȚIE:** Înainte de a citi tabelul, încearcă să răspunzi: Care protocol (TCP sau UDP) ar fi mai potrivit pentru un joc multiplayer online? De ce?

| Caracteristică | TCP | UDP |
|----------------|-----|-----|
| Tip conexiune | Orientat pe conexiune | Fără conexiune |
| Fiabilitate | Garantată (retransmisii) | Best-effort (fără garanții) |
| Ordonare | Garantată | Nu e garantată |
| Control flux | Da (fereastră glisantă) | Nu |
| Control congestie | Da | Nu |
| Overhead | Mai mare | Mai mic |
| Cazuri de utilizare | HTTP, FTP, SSH | DNS, VoIP, streaming |

**Verificare:** Ai ghicit corect? Jocurile folosesc adesea UDP pentru că latența e mai importantă decât fiabilitatea perfectă.

### HTTP peste TCP

HTTP folosește TCP ca protocol de transport deoarece necesită:
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

> Pentru ghidul complet de depanare, consultați [`docs/depanare.md`](docs/depanare.md).

### Probleme Frecvente (Rezumat Rapid)

**🔮 PREDICȚIE:** Dacă `curl http://localhost:8080/` returnează "Connection refused", care crezi că e cea mai probabilă cauză? (a) nginx nu rulează, (b) portul e greșit, (c) firewall blochează, (d) backend-urile sunt oprite?

**Docker nu pornește?**
```bash
sudo service docker start
# Parolă: stud
```

**Port ocupat?**
```bash
sudo ss -tlnp | grep 8080
```

**🔮 PREDICȚIE:** Ce proces crezi că ar putea ocupa portul 8080 dacă nu e Docker?

**nginx returnează 502?**
```bash
docker ps | grep backend
docker logs week8-nginx-proxy
```

**Wireshark nu capturează?**
- Verifică interfața: `vEthernet (WSL)`
- Verifică că generezi trafic ÎN TIMPUL capturii

---

## 🧹 Procedura Completă de Curățare

**🔮 PREDICȚIE:** După curățarea completă a laboratorului, ce containere ar trebui să rămână în `docker ps`? (Hint: un serviciu rulează global)

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

# Verifică utilizarea discului
docker system df
```

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
