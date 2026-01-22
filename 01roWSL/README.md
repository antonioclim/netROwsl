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

**🔮 PREDICȚIE:** Ce va afișa `docker ps` dacă totul e OK?

```bash
docker ps
```

**Output așteptat:**
```
CONTAINER ID   IMAGE                    STATUS          NAMES
abc123...      portainer/portainer-ce   Up 2 hours      portainer
```

Dacă vezi `portainer` în listă, mediul este pregătit!

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
2. **Explici** diferențele dintre TCP și UDP
3. **Demonstrezi** conectivitate folosind ping, netcat și socket-uri Python
4. **Analizezi** trafic capturat cu tcpdump, tshark și Wireshark
5. **Construiești** aplicații simple client-server cu socket-uri TCP
6. **Evaluezi** modele de trafic prin analiza fișierelor PCAP

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

2. **🔮 PREDICȚIE:** Câte interfețe de rețea crezi că vei vedea? (Hint: gândește-te la loopback + interfața Docker)

   ```bash
   ip -br addr show
   ```

   **Output așteptat:**
   ```
   lo               UNKNOWN        127.0.0.1/8 ::1/128
   eth0@if123       UP             172.20.1.2/24 fe80::42:acff:fe14:102/64
   ```
   
   **Ce să verifici:**
   - `lo` = loopback, mereu prezent în orice sistem Linux
   - `eth0` = interfața principală, IP-ul e cel din docker-compose.yml (172.20.1.2)
   - `UP` = interfața funcționează corect

3. **🔮 PREDICȚIE:** Care va fi gateway-ul implicit? (Hint: subrețeaua e 172.20.1.0/24)

   ```bash
   ip route show
   ```

   **Output așteptat:**
   ```
   default via 172.20.1.1 dev eth0
   172.20.1.0/24 dev eth0 proto kernel scope link src 172.20.1.2
   ```

4. Vizualizează socket-urile active:
   ```bash
   ss -tunap
   ```

---

### Exercițiul 2: Testarea Conectivității

**Obiectiv:** Testează conectivitatea și măsoară latența.

**Durată:** 20 minute

**Pași:**

1. **🔮 PREDICȚIE:** Ce RTT (Round Trip Time) te aștepți pentru loopback? (Hint: datele nu părăsesc mașina)

   ```bash
   ping -c 4 127.0.0.1
   ```

   **Output așteptat:**
   ```
   PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
   64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.034 ms
   64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.041 ms
   ...
   --- 127.0.0.1 ping statistics ---
   4 packets transmitted, 4 received, 0% packet loss
   rtt min/avg/max/mdev = 0.034/0.038/0.041/0.003 ms
   ```
   
   **Interpretare:** RTT < 0.1ms pentru loopback e normal - datele nu ies din mașină!

2. **🔮 PREDICȚIE:** RTT către gateway va fi mai mare sau mai mic decât loopback?

   ```bash
   ping -c 4 172.20.1.1
   ```

3. Rulează exercițiul Python:
   ```bash
   cd /work/src/exercises
   python3 ex_1_01_latenta_ping.py
   ```

---

### Exercițiul 3: Comunicarea TCP

**Obiectiv:** Stabilește o conexiune TCP și observă stările socket-urilor.

**Durată:** 25 minute

**Pregătire Wireshark:** Deschide Wireshark pe Windows și pornește captura pe `vEthernet (WSL)` ÎNAINTE de a începe!

**Pași:**

1. **🔮 PREDICȚIE:** După `nc -l -p 9090`, în ce stare va fi socket-ul? (Hint: serverul așteaptă...)

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

4. **🔮 PREDICȚIE:** Câte pachete vei vedea în Wireshark doar pentru handshake (înainte de orice date)?

   ```bash
   # Terminal 3: Verifică socket-urile
   ss -tnp | grep 9090
   ```

   **Output așteptat:**
   ```
   ESTAB    0    0    127.0.0.1:9090    127.0.0.1:54321    users:(("nc",pid=1234,fd=4))
   ```
   
   **Răspuns predicție:** 3 pachete pentru handshake (SYN, SYN-ACK, ACK)

5. Rulează exercițiul Python:
   ```bash
   python3 ex_1_02_tcp_server_client.py
   ```

---

### Exercițiul 4: Captura de Trafic

**Obiectiv:** Capturează și salvează traficul de rețea.

**Durată:** 25 minute

**Pași:**

1. **🔮 PREDICȚIE:** Dacă capturezi pe `lo` și trimiți date pe portul 9090, vei vedea pachete?

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

   **Output așteptat pentru flag-uri:**
   ```
   ··········S·    (SYN)
   ·······A··S·    (SYN-ACK)
   ·······A····    (ACK)
   ·······AP···    (ACK + PUSH - date)
   ```

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

**Filtre handshake:**
| Filtru | Ce arată |
|--------|----------|
| `tcp.flags.syn == 1` | Pachete SYN |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Doar conexiuni noi |
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

- `docs/rezumat_teoretic.md` - Teorie + analogii CPA
- `docs/intrebari_peer_instruction.md` - 5 întrebări pentru auto-evaluare
- `docs/fisa_comenzi.md` - Referință rapidă comenzi
- `docs/depanare.md` - Soluții probleme comune

---

## Referințe

- Kurose & Ross (2016). *Computer Networking: A Top-Down Approach* (7th ed.)
- Stevens (1994). *TCP/IP Illustrated, Volume 1*
- Rhodes & Goetzen (2014). *Foundations of Python Network Programming*

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
