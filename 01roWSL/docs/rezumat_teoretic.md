# Rezumat Teoretic - Săptămâna 1

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## 0. Analogii pentru Concepte Cheie (CPA)

Înainte de a intra în detalii tehnice, iată cum să-ți imaginezi conceptele. Metoda CPA (Concret-Pictorial-Abstract) te ajută să construiești intuiția pas cu pas.

| Concept | 🎯 Imaginează-ți că... | 📊 Vizual | 💻 În practică |
|---------|------------------------|-----------|----------------|
| **Container** | O cutie de transport maritim. Înăuntru e tot ce trebuie pentru a rula aplicația. Poți muta cutia oriunde, conținutul rămâne izolat. | `[App+Libs+Config]` | `docker run nginx` |
| **Imagine Docker** | Rețeta pentru o prăjitură. Poți face oricâte prăjituri (containere) din aceeași rețetă, toate identice. | `Dockerfile → Image → Container(s)` | `docker pull python:3.12` |
| **Volume** | Un hard disk extern pe care-l atașezi la laptop. Datele rămân pe disk chiar când laptopul e oprit. | `Host ←→ Container` | `-v /date:/app/date` |
| **Port Mapping** | Adresa unei clădiri (host) + numărul apartamentului (container). Vizitatorii vin la adresa clădirii, portarul îi trimite la apartament. | `Windows:8080 → Container:80` | `-p 8080:80` |
| **Network Bridge** | Un drum privat între case vecine. Doar casele de pe acest drum pot comunica direct între ele. Străinii nu văd drumul. | `Container A ↔ Bridge ↔ Container B` | `docker network create retea_mea` |
| **Docker Compose** | Dirijorul unei orchestre. Coordonează mai multe instrumente (containere) să cânte împreună, fiecare la momentul potrivit. | `YAML → Orchestrate → Services` | `docker compose up` |
| **TCP Handshake** | Când suni pe cineva: tu zici "Alo?" (SYN), el zice "Da, te aud, tu mă auzi?" (SYN-ACK), tu zici "Da, te aud" (ACK). Abia apoi vorbiți. | `SYN → SYN-ACK → ACK → DATA` | `connect() → accept()` |
| **UDP** | Trimiți o scrisoare fără confirmare de primire. Rapid, dar nu știi 100% dacă a ajuns. Bun pentru mesaje unde viteza contează mai mult decât certitudinea. | `Send → ? → Maybe received` | `socket.SOCK_DGRAM` |
| **Socket** | Priza din perete. Fiecare priză are o adresă (IP) și un număr (port). Conectezi "cablul" aplicației tale la priză pentru a comunica. | `App ← Socket(IP:Port) → Network` | `bind(('0.0.0.0', 9090))` |
| **Wireshark** | Camera de supraveghere pentru traficul de rețea. Vezi tot ce trece pe "drum" - cine trimite, cine primește, ce conțin pachetele. | `Capture → Filter → Analyze` | Captură pe `vEthernet (WSL)` |

**Cum să folosești acest tabel:**
1. Citește coloana "Imaginează-ți" pentru a înțelege conceptul intuitiv
2. Privește coloana "Vizual" pentru a-ți forma o imagine mentală
3. Exersează cu coloana "În practică" în terminal

---

## 1. Clasificarea Rețelelor de Calculatoare

### După Aria Geografică

| Tip | Denumire | Acoperire | Exemple |
|-----|----------|-----------|---------|
| **PAN** | Personal Area Network | 1-10 m | Bluetooth, USB |
| **LAN** | Local Area Network | 10m - 1km | Ethernet, WiFi |
| **MAN** | Metropolitan Area Network | 1-100 km | Rețele urbane |
| **WAN** | Wide Area Network | >100 km | Internet |

### Topologii de Rețea

Fiecare topologie are avantaje și dezavantaje:

- **Bus (Magistrală)**: Toate dispozitivele conectate la un cablu comun. Simplu dar vulnerabil la defecțiuni.
- **Stea (Star)**: Dispozitivele conectate la un nod central (switch/hub). Cel mai comun în LAN-uri moderne.
- **Inel (Ring)**: Fiecare dispozitiv conectat la două vecine. Folosit în rețele industriale.
- **Plasă (Mesh)**: Conexiuni multiple între dispozitive. Redundanță maximă, cost ridicat.
- **Arbore (Tree)**: Structură ierarhică. Folosită în rețele mari de enterprise.

## 2. Modelul TCP/IP

Modelul TCP/IP este arhitectura fundamentală a Internetului, organizată în patru straturi:

```
┌─────────────────────────────────────┐
│     Strat Aplicație                 │  HTTP, FTP, SMTP, DNS, SSH
├─────────────────────────────────────┤
│     Strat Transport                 │  TCP, UDP
├─────────────────────────────────────┤
│     Strat Internet (Rețea)          │  IP, ICMP, ARP
├─────────────────────────────────────┤
│     Strat Acces la Rețea            │  Ethernet, WiFi, PPP
└─────────────────────────────────────┘
```

### Funcțiile Straturilor

**Stratul Aplicație**
- Interfața cu utilizatorul și aplicațiile
- Protocoale specifice serviciilor (web, email, transfer fișiere)
- Exemple: HTTP/HTTPS, FTP, SMTP, DNS, SSH

**Stratul Transport**
- Comunicare proces-la-proces
- Segmentarea și reasamblarea datelor
- Control al fluxului și congestiei
- Protocoale: TCP (fiabil), UDP (nefiabil dar rapid)

**Stratul Internet (Rețea)**
- Adresare logică (adrese IP)
- Rutarea pachetelor între rețele
- Fragmentarea și reasamblarea
- Protocoale: IP, ICMP, ARP

**Stratul Acces la Rețea**
- Transmiterea fizică a biților
- Adresare hardware (MAC)
- Controlul accesului la mediu
- Tehnologii: Ethernet, WiFi, fibră optică

## 3. Adresarea IP (IPv4)

### Structura Adresei IPv4

O adresă IPv4 are 32 de biți, reprezentată ca 4 numere zecimale separate prin puncte:

```
Exemplu: 192.168.1.100

În binar:  11000000.10101000.00000001.01100100
           ────────────────── ────────────────
           Partea de rețea    Partea de gazdă
```

### Notația CIDR (Classless Inter-Domain Routing)

Notația CIDR specifică numărul de biți pentru partea de rețea:

```
192.168.1.0/24
          ───
          24 biți pentru rețea = mască 255.255.255.0
          8 biți pentru gazde = 254 adrese utilizabile
```

### Adrese IP Private (RFC 1918)

| Clasă | Interval | Notație CIDR | Utilizare |
|-------|----------|--------------|-----------|
| A | 10.0.0.0 - 10.255.255.255 | 10.0.0.0/8 | Rețele mari |
| B | 172.16.0.0 - 172.31.255.255 | 172.16.0.0/12 | Rețele medii |
| C | 192.168.0.0 - 192.168.255.255 | 192.168.0.0/16 | Rețele mici |

### Adrese IP Speciale

- **0.0.0.0**: Adresa "orice" sau "toate rețelele"
- **127.0.0.1**: Loopback (localhost) - datele nu părăsesc mașina
- **255.255.255.255**: Broadcast global
- **169.254.x.x**: Link-local (APIPA) - când DHCP nu funcționează

## 4. Protocoale de Transport

### TCP (Transmission Control Protocol)

**Caracteristici:**
- Orientat pe conexiune (connection-oriented)
- Fiabil - garantează livrarea și ordinea
- Control al fluxului și congestiei
- Full-duplex

**Handshake-ul în Trei Pași (Three-Way Handshake):**

```
Client                          Server
   │                               │
   │  ────── SYN (seq=x) ──────►   │  1. Client solicită conexiune
   │                               │
   │  ◄── SYN-ACK (seq=y, ack=x+1) │  2. Server confirmă și răspunde
   │                               │
   │  ────── ACK (ack=y+1) ─────►  │  3. Client confirmă
   │                               │
   │     CONEXIUNE STABILITĂ       │
```

**Stări TCP importante:**
- `LISTEN`: Serverul așteaptă conexiuni
- `SYN_SENT`: Clientul a trimis SYN
- `ESTABLISHED`: Conexiune activă
- `TIME_WAIT`: Așteaptă pachete întârziate (durează ~60s)
- `CLOSE_WAIT`: Așteaptă închiderea aplicației

### UDP (User Datagram Protocol)

**Caracteristici:**
- Fără conexiune (connectionless)
- Nefiabil - nu garantează livrarea
- Fără control al fluxului
- Overhead minim (8 octeți antet)
- Rapid și eficient pentru streaming

### Comparație TCP vs UDP

| Aspect | TCP | UDP |
|--------|-----|-----|
| Conexiune | Da | Nu |
| Fiabilitate | Garantată | Best-effort |
| Ordine pachete | Păstrată | Negarantată |
| Overhead antet | 20+ octeți | 8 octeți |
| Viteză | Mai lent | Mai rapid |
| Utilizare | Web, email, FTP | DNS, streaming, gaming |

## 5. Programarea Socket-urilor

### Ce Este un Socket?

Un socket este un endpoint pentru comunicarea bidirecțională între două programe care rulează în rețea. Este identificat prin:
- Adresa IP
- Numărul portului
- Protocolul (TCP/UDP)

### Model Client-Server

```
┌─────────────┐                    ┌─────────────┐
│   CLIENT    │                    │   SERVER    │
├─────────────┤                    ├─────────────┤
│ socket()    │                    │ socket()    │
│     │       │                    │     │       │
│     ▼       │                    │     ▼       │
│ connect()   │ ◄─── conexiune ──► │ bind()      │
│     │       │                    │     │       │
│     ▼       │                    │     ▼       │
│ send()      │ ──── date ───────► │ listen()    │
│     │       │                    │     │       │
│     ▼       │                    │     ▼       │
│ recv()      │ ◄─── răspuns ───── │ accept()    │
│     │       │                    │     │       │
│     ▼       │                    │     ▼       │
│ close()     │                    │ recv()/send()│
└─────────────┘                    │     │       │
                                   │     ▼       │
                                   │ close()     │
                                   └─────────────┘
```

### Exemplu Cod Python

```python
# Server TCP simplu
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9090))  # Ascultă pe toate interfețele
server.listen(1)  # Coadă de 1 conexiune

conn, addr = server.accept()  # Blochează până vine cineva
data = conn.recv(1024)
conn.send(b'Primit!')
conn.close()
```

```python
# Client TCP simplu
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9090))  # Conectare la server
client.send(b'Salut!')
response = client.recv(1024)
client.close()
```

## 6. Porturi Comune

| Port | Protocol | Serviciu |
|------|----------|----------|
| 20, 21 | TCP | FTP (date, control) |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 67, 68 | UDP | DHCP |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 143 | TCP | IMAP |
| 443 | TCP | HTTPS |
| 3306 | TCP | MySQL |
| 5432 | TCP | PostgreSQL |

## 7. Comenzi Esențiale Linux

### Configurare și Inspectare Rețea

```bash
# Afișare interfețe de rețea
ip addr show
ip -br addr show  # format scurt, mai ușor de citit

# Afișare tabelă de rutare
ip route show

# Afișare vecinii ARP
ip neigh show
```

### Testare Conectivitate

```bash
# Test ICMP - 4 pachete, ca la examen
ping -c 4 192.168.1.1

# Trasare rută - vezi prin ce noduri trec pachetele
traceroute 8.8.8.8

# Rezolvare DNS
nslookup google.com
dig google.com
```

### Inspectare Socket-uri

```bash
# Toate socket-urile (-t TCP, -u UDP, -n numeric, -a all, -p process)
ss -tunap

# Doar TCP în ascultare (-l listen)
ss -tln

# Cu informații despre proces
ss -tlnp
```

### Captura de Pachete

```bash
# Captură pe interfață
tcpdump -i eth0

# Salvare în fișier pentru Wireshark
tcpdump -i eth0 -w captura.pcap

# Filtrare după port
tcpdump -i eth0 port 80
```

## 8. Întârzierea în Rețele

### Componentele Întârzierii Totale

```
d_total = d_transmisie + d_propagare + d_procesare + d_așteptare
```

**Întârzierea de Transmisie (Transmission Delay)**
- Timpul pentru a pune biții pe mediu
- d_trans = L / R (L = dimensiune pachet, R = rată link)

**Întârzierea de Propagare (Propagation Delay)**
- Timpul pentru un bit să parcurgă distanța fizică
- d_prop = D / S (D = distanță, S = viteză în mediu)

**Întârzierea de Procesare**
- Timp pentru verificare erori, decizie rutare
- Tipic: microsecunde

**Întârzierea de Așteptare (Queuing Delay)**
- Timp petrecut în coada de așteptare
- Variabil, depinde de congestionarea rețelei

## Referințe

1. Kurose, J. F., & Ross, K. W. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.

2. Tanenbaum, A. S., & Wetherall, D. J. (2011). *Computer Networks* (5th ed.). Pearson.

3. Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.

4. Rhodes, B., & Goetzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.

5. RFC 791 - Internet Protocol (IP)
6. RFC 793 - Transmission Control Protocol (TCP)
7. RFC 768 - User Datagram Protocol (UDP)
8. RFC 1918 - Address Allocation for Private Internets

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
