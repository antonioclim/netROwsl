# Săptămâna 1: Fundamentele Rețelelor de Calculatoare

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | Laborator
>
> by Revolvix | 2025

---

## Cuprins

- [Notificare Mediu](#️-notificare-mediu)
- [Clonarea Laboratorului](#-clonarea-laboratorului)
- [Configurarea Inițială](#-configurarea-inițială-doar-prima-dată)
- [Despre Laborator](#despre-laborator)
- [Obiective de Învățare](#obiective-de-învățare)
- [Pornire Rapidă](#pornire-rapidă)
- [Exerciții de Laborator](#exerciții-de-laborator)
  - [Exercițiul 1: Inspectarea Interfețelor](#exercițiul-1-inspectarea-interfețelor-de-rețea)
  - [Exercițiul 2: Testarea Conectivității](#exercițiul-2-testarea-conectivității)
  - [Exercițiul 3: Comunicarea TCP](#exercițiul-3-comunicarea-tcp)
  - [Exercițiul 4: Captura de Trafic](#exercițiul-4-captura-de-trafic)
  - [Exercițiul 5: Trace Handshake](#exercițiul-5-trace-tcp-handshake-fără-cod)
- [Filtre Wireshark](#-filtre-wireshark-esențiale)
- [Oprire și Curățare](#oprire-și-curățare)
- [Depanare Rapidă](#depanare-rapidă)
- [Resurse Suplimentare](#resurse-suplimentare)
- [Referințe](#referințe)

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

## 📥 Clonarea Laboratorului

### Pasul 1: Deschide PowerShell (Windows)

Apasă `Win + X` → Selectează "Windows Terminal" sau "PowerShell"

### Pasul 2: Navighează și Clonează

```powershell
# Creează folderul de rețele dacă nu există
mkdir D:\RETELE -ErrorAction SilentlyContinue
cd D:\RETELE

# Clonează Săptămâna 1
git clone https://github.com/antonioclim/netROwsl.git SAPT1
cd SAPT1\01roWSL
```

### Structura Directoarelor

```
D:\RETELE\SAPT1\01roWSL\
├── artifacts/       # Rezultate generate
├── docker/          # Configurație Docker
├── docs/            # Documentație + întrebări Peer Instruction
├── homework/        # Teme pentru acasă
├── pcap/            # Fișiere de captură
├── scripts/         # Scripturi de automatizare
├── src/             # Cod sursă exerciții
├── tests/           # Teste automatizate
└── README.md        # Acest fișier
```

---

## 🔧 Configurarea Inițială (Doar Prima Dată)

### Pasul 1: Deschide Terminalul Ubuntu

Din Windows: Click pe "Ubuntu" în meniul Start, sau în PowerShell tastează: `wsl`

### Pasul 2: Pornește Docker

```bash
# Pornește Docker (necesar după fiecare restart Windows)
sudo service docker start
# Parolă: stud
```

┌─────────────────────────────────────────────────────────────┐
│  🔮 PAUZĂ PENTRU PREDICȚIE                                  │
│                                                             │
│  Ce va afișa `docker ps` dacă totul e configurat corect?   │
│  Gândește-te ce containere ar trebui să ruleze permanent.  │
│                                                             │
│  (Formulează răspunsul înainte de a continua!)             │
└─────────────────────────────────────────────────────────────┘

```bash
docker ps
```

<details>
<summary>🔍 Verifică răspunsul</summary>

```
CONTAINER ID   IMAGE                    STATUS          NAMES
abc123...      portainer/portainer-ce   Up 2 hours      portainer
```

Dacă vezi `portainer` în listă, mediul este pregătit! Portainer e singurul container care rulează permanent — celelalte le pornești tu pentru fiecare laborator.

</details>

### Pasul 3: Verifică Portainer

Deschide browser-ul și navighează la: **http://localhost:9000**
- User: `stud`
- Parolă: `studstudstud`

---

## Despre Laborator

În acest laborator vei lucra practic cu stiva TCP/IP. Vei vedea cum datele trec prin fiecare strat și vei captura pachete reale cu Wireshark și tcpdump pentru a le analiza.

## Obiective de Învățare

La finalul laboratorului vei fi capabil să:

1. **Identifici** interfețele de rețea, adresele IP și tabelele de rutare
2. **Explici** diferențele dintre TCP și UDP și când folosești fiecare
3. **Demonstrezi** conectivitate folosind ping, netcat și socket-uri Python
4. **Analizezi** trafic capturat cu tcpdump, tshark și Wireshark
5. **Construiești** aplicații simple client-server cu socket-uri TCP
6. **Evaluezi** modele de trafic prin analiza fișierelor PCAP
7. **Proiectezi** o soluție de comunicare pentru un scenariu dat (tema pentru acasă)

---

## Pornire Rapidă

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT1/01roWSL

# Pornește laboratorul
python3 scripts/porneste_lab.py

# Verifică statusul
python3 scripts/porneste_lab.py --status
```

**Acces servicii:**
| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Container Lab | localhost:9090 (TCP) | N/A |

---

## Exerciții de Laborator

### Exercițiul 1: Inspectarea Interfețelor de Rețea

**Obiectiv:** Identifică și documentează toate interfețele de rețea.

**Durată:** 15 minute

**Pași:**

1. Conectează-te la container:
   ```bash
   docker exec -it week1_lab bash
   ```

2. Înainte de a rula comanda următoare:

┌─────────────────────────────────────────────────────────────┐
│  🔮 PAUZĂ PENTRU PREDICȚIE                                  │
│                                                             │
│  Câte interfețe de rețea crezi că vei vedea?               │
│  (Hint: gândește-te la loopback + interfața Docker)        │
│                                                             │
│  Răspunsul tău: ____                                       │
└─────────────────────────────────────────────────────────────┘

   ```bash
   ip -br addr show
   ```

<details>
<summary>🔍 Output așteptat și explicație</summary>

```
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0@if123       UP             172.20.1.2/24 fe80::42:acff:fe14:102/64
```

**Ce să verifici:**
- `lo` = loopback, mereu prezent în orice sistem Linux
- `eth0` = interfața principală, IP-ul e cel din docker-compose.yml (172.20.1.2)
- `UP` = interfața funcționează corect

Răspuns: 2 interfețe (loopback + eth0)

</details>

3. Acum gândește-te:

┌─────────────────────────────────────────────────────────────┐
│  🔮 PAUZĂ PENTRU PREDICȚIE                                  │
│                                                             │
│  Care va fi gateway-ul implicit?                           │
│  (Hint: subrețeaua e 172.20.1.0/24, gateway-ul e de        │
│  obicei prima sau ultima adresă utilizabilă)               │
│                                                             │
│  Răspunsul tău: ____                                       │
└─────────────────────────────────────────────────────────────┘

   ```bash
   ip route show
   ```

<details>
<summary>🔍 Output așteptat</summary>

```
default via 172.20.1.1 dev eth0
172.20.1.0/24 dev eth0 proto kernel scope link src 172.20.1.2
```

Gateway-ul e 172.20.1.1 — prima adresă din subrețea, așa cum Docker configurează implicit.

</details>

4. Vizualizează socket-urile active:
   ```bash
   ss -tunap
   ```

**⚠️ Ce poate merge greșit:**

| Simptom | Cauză probabilă | Soluție rapidă |
|---------|-----------------|----------------|
| `docker exec` eșuează | Container-ul nu rulează | `docker compose up -d` în folderul docker/ |
| `command not found: ip` | Imagine Docker incompletă | Reconstruiește: `docker compose build --no-cache` |
| Nu vezi eth0 | Problemă de rețea Docker | `docker network inspect week1_network` |

---

### Exercițiul 2: Testarea Conectivității

**Obiectiv:** Testează conectivitatea și măsoară latența.

**Durată:** 20 minute

**Pași:**

1. Gândește-te înainte de a rula:

┌─────────────────────────────────────────────────────────────┐
│  🔮 PAUZĂ PENTRU PREDICȚIE                                  │
│                                                             │
│  Ce RTT (Round Trip Time) te aștepți pentru loopback?      │
│  a) < 0.1 ms                                               │
│  b) 1-10 ms                                                │
│  c) 10-50 ms                                               │
│  d) > 100 ms                                               │
│                                                             │
│  De ce? (Hint: datele părăsesc mașina fizic?)              │
└─────────────────────────────────────────────────────────────┘

   ```bash
   ping -c 4 127.0.0.1
   ```

<details>
<summary>🔍 Output așteptat și explicație</summary>

```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.034 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.041 ms
...
--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max/mdev = 0.034/0.038/0.041/0.003 ms
```

**Răspuns corect: a) < 0.1 ms**

RTT < 0.1ms pentru loopback e normal — datele NU ies din mașină! Totul se întâmplă în memoria kernel-ului.

</details>

2. Acum compară cu gateway-ul:

┌─────────────────────────────────────────────────────────────┐
│  🔮 PAUZĂ PENTRU PREDICȚIE                                  │
│                                                             │
│  RTT către gateway (172.20.1.1) va fi:                     │
│  □ Mai mic decât loopback                                  │
│  □ Aproximativ la fel                                      │
│  □ Puțin mai mare (dar tot sub 1ms)                       │
│  □ Semnificativ mai mare (>10ms)                          │
└─────────────────────────────────────────────────────────────┘

   ```bash
   ping -c 4 172.20.1.1
   ```

<details>
<summary>🔍 Verifică răspunsul</summary>

De obicei RTT către gateway-ul Docker e tot sub 1ms, dar puțin mai mare decât loopback (de ex. 0.1-0.5ms). Diferența vine din procesarea suplimentară în stiva de rețea Docker.

</details>

3. Rulează exercițiul Python:
   ```bash
   cd /work/src/exercises
   python3 ex_1_01_latenta_ping.py
   ```

**⚠️ Ce poate merge greșit:**

| Simptom | Cauză probabilă | Soluție rapidă |
|---------|-----------------|----------------|
| `ping: connect: Network is unreachable` | Rețeaua Docker nu există | `docker compose up -d` |
| RTT foarte mare (>100ms) | WSL overloaded sau container supraîncărcat | Repornește WSL: `wsl --shutdown` din PowerShell |
| `python3: command not found` | Nu ești în container | `docker exec -it week1_lab bash` |

---

### Exercițiul 3: Comunicarea TCP

**Obiectiv:** Stabilește o conexiune TCP și observă stările socket-urilor.

**Durată:** 25 minute

**Pregătire Wireshark:** Deschide Wireshark pe Windows și pornește captura pe `vEthernet (WSL)` ÎNAINTE de a începe!

**Pași:**

1. Înainte de a porni serverul:

┌─────────────────────────────────────────────────────────────┐
│  🔮 PAUZĂ PENTRU PREDICȚIE                                  │
│                                                             │
│  După `nc -l -p 9090`, în ce stare va fi socket-ul?        │
│                                                             │
│  □ CLOSED                                                  │
│  □ LISTEN                                                  │
│  □ ESTABLISHED                                             │
│  □ TIME_WAIT                                               │
│                                                             │
│  (Hint: serverul așteaptă pe cineva...)                    │
└─────────────────────────────────────────────────────────────┘

   ```bash
   # Terminal 1: Pornește serverul
   nc -l -p 9090
   ```

2. Conectează-te de la alt terminal:
   ```bash
   # Terminal 2: Conectează clientul
   nc localhost 9090
   ```

3. Trimite mesaje și observă în Wireshark.

4. Acum întrebarea importantă:

┌─────────────────────────────────────────────────────────────┐
│  🔮 PAUZĂ PENTRU PREDICȚIE                                  │
│                                                             │
│  Câte pachete vei vedea în Wireshark DOAR pentru           │
│  handshake (înainte de orice date)?                        │
│                                                             │
│  Răspunsul tău: ____                                       │
└─────────────────────────────────────────────────────────────┘

   ```bash
   # Terminal 3: Verifică socket-urile
   ss -tnp | grep 9090
   ```

<details>
<summary>🔍 Output așteptat și răspunsuri</summary>

```
ESTAB    0    0    127.0.0.1:9090    127.0.0.1:54321    users:(("nc",pid=1234,fd=4))
```

**Răspunsuri predicții:**
- Socket-ul serverului inițial: **LISTEN** (așteaptă conexiuni)
- După conectare: **ESTABLISHED** (conexiune activă)
- Pachete handshake: **3** (SYN, SYN-ACK, ACK)

</details>

5. Rulează exercițiul Python:
   ```bash
   python3 ex_1_02_tcp_server_client.py
   ```

**⚠️ Ce poate merge greșit:**

| Simptom | Cauză probabilă | Soluție rapidă |
|---------|-----------------|----------------|
| `nc: Connection refused` | Serverul nu rulează sau port greșit | Verifică cu `ss -tlnp \| grep 9090` |
| Wireshark nu vede pachete | Trafic pe loopback, nu pe WSL | Capturează în container cu tcpdump |
| `Address already in use` | Port ocupat de altcineva | `ss -tlnp \| grep 9090`, apoi `kill PID` |

---

### Exercițiul 4: Captura de Trafic

**Obiectiv:** Capturează și salvează traficul de rețea.

**Durată:** 25 minute

**Pași:**

1. Gândește-te:

┌─────────────────────────────────────────────────────────────┐
│  🔮 PAUZĂ PENTRU PREDICȚIE                                  │
│                                                             │
│  Dacă capturezi pe interfața `lo` (loopback) și trimiți    │
│  date pe portul 9090 către localhost, vei vedea pachete?   │
│                                                             │
│  □ Da, loopback vede tot traficul local                    │
│  □ Nu, trebuie să capturez pe eth0                         │
└─────────────────────────────────────────────────────────────┘

   ```bash
   tcpdump -i lo -w /work/pcap/captura_tcp.pcap port 9090 &
   ```

2. Generează trafic TCP (ca în exercițiul 3).

3. Oprește captura:
   ```bash
   pkill tcpdump
   ```

4. Analizează:
   ```bash
   tshark -r /work/pcap/captura_tcp.pcap -Y tcp -T fields -e tcp.flags.str
   ```

<details>
<summary>🔍 Output așteptat pentru flag-uri TCP</summary>

```
··········S·    (SYN)
·······A··S·    (SYN-ACK)
·······A····    (ACK)
·······AP···    (ACK + PUSH - date)
```

**Răspuns predicție:** Da, loopback vede traficul către localhost. Traficul către 127.0.0.1 trece prin interfața `lo`.

</details>

**⚠️ Ce poate merge greșit:**

| Simptom | Cauză probabilă | Soluție rapidă |
|---------|-----------------|----------------|
| `tcpdump: permission denied` | Lipsă capabilități | Verifică `cap_add: NET_RAW` în compose |
| Fișier PCAP gol | Captura oprită înainte de trafic | Generează trafic ÎNAINTE de `pkill` |
| `tshark` nu găsește fișierul | Cale greșită | Folosește calea completă `/work/pcap/...` |

---

### Exercițiul 5: Trace TCP Handshake (FĂRĂ COD)

**Obiectiv:** Analizează o captură existentă fără a scrie cod.

**Durată:** 15 minute

**Nivel Bloom:** ANALYSE

Acest exercițiu dezvoltă abilitatea de a citi și interpreta capturi de pachete — esențială pentru debugging în lumea reală.

**Pași:**

1. Rulează scriptul care afișează instrucțiunile:
   ```bash
   python3 ex_1_06_trace_handshake.py
   ```

2. Folosește captura din exercițiul 4 sau generează una nouă.

3. Răspunde la întrebările pe hârtie, apoi verifică cu colegul.

Acest exercițiu nu are "răspuns corect" fix — depinde de captura ta. Important e să înțelegi CE vezi și DE CE.

---

## 🦈 Filtre Wireshark Esențiale

**Filtre de bază:**
| Filtru | Scop |
|--------|------|
| `tcp` | Tot traficul TCP |
| `udp` | Tot traficul UDP |
| `icmp` | Pachete ping |

**Filtre pentru laborator:**
| Filtru | Scop |
|--------|------|
| `tcp.port == 9090` | Portul exercițiilor TCP |
| `ip.addr == 172.20.1.2` | Trafic container lab |

**Filtre handshake (de memorat pentru examen):**
| Filtru | Ce arată |
|--------|----------|
| `tcp.flags.syn == 1` | Pachete SYN |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Doar conexiuni noi (SYN fără ACK) |
| `tcp.flags.fin == 1` | Închideri conexiuni |

---

## Oprire și Curățare

### Sfârșit de Sesiune

```bash
# Oprește containerele (Portainer rămâne activ!)
python3 scripts/opreste_lab.py

# Verifică - ar trebui să vezi doar portainer
docker ps
```

### Curățare Completă

```bash
python3 scripts/curatare.py --complet
```

---

## Depanare Rapidă

**Docker nu pornește:**
```bash
sudo service docker start
# Parolă: stud
```

**Portainer nu răspunde:**
```bash
docker start portainer
```

**Port deja utilizat:**
```bash
ss -tlnp | grep PORT
# Găsește procesul și oprește-l
```

Pentru mai multe soluții, vezi `docs/depanare.md`.

---

## Resurse Suplimentare

- `docs/rezumat_teoretic.md` — Teorie + analogii CPA (citește ÎNAINTE de laborator)
- `docs/intrebari_peer_instruction.md` — 5 întrebări pentru auto-evaluare
- `docs/fisa_comenzi.md` — Referință rapidă comenzi (include diferențe PowerShell vs Bash)
- `docs/depanare.md` — Soluții probleme comune

---

## Referințe

1. Kurose, J.F. & Ross, K.W. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
2. Stevens, W.R. (1994). *TCP/IP Illustrated, Volume 1*. Addison-Wesley.
3. Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix | 2025*
