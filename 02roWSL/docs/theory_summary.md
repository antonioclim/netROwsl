# Rezumat Teoretic - Săptămâna 2

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Modele Arhitecturale de Rețea

### Modelul OSI (Open Systems Interconnection)

Modelul OSI este un model conceptual cu 7 straturi, creat de ISO pentru standardizarea comunicațiilor în rețea.

| Strat | Nume | Funcție | Unitate de Date | Exemple |
|-------|------|---------|-----------------|---------|
| 7 | Aplicație | Interfață cu utilizatorul, servicii de rețea | Date | HTTP, FTP, SMTP, DNS |
| 6 | Prezentare | Formatare, criptare, compresie | Date | SSL/TLS, JPEG, ASCII |
| 5 | Sesiune | Gestiunea dialogului, sincronizare | Date | NetBIOS, RPC, PPTP |
| 4 | Transport | Livrare end-to-end, segmentare | Segment | TCP, UDP |
| 3 | Rețea | Rutare, adresare logică | Pachet | IP, ICMP, ARP |
| 2 | Legătură de Date | Acces la mediu, adresare fizică | Cadru | Ethernet, Wi-Fi, PPP |
| 1 | Fizic | Transmisie biți pe mediu | Bit | Cabluri, hub-uri, semnale |

**Mnemonică pentru memorare (de jos în sus):** "**P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way"

### Modelul TCP/IP (Internet Protocol Suite)

Modelul TCP/IP este mai pragmatic și reprezintă arhitectura reală a Internetului.

| Strat TCP/IP | Echivalent OSI | Protocoale |
|--------------|----------------|------------|
| Aplicație | Straturi 5, 6, 7 | HTTP, FTP, SMTP, DNS, SSH |
| Transport | Strat 4 | TCP, UDP, SCTP |
| Internet | Strat 3 | IP, ICMP, ARP, RARP |
| Acces la Rețea | Straturi 1, 2 | Ethernet, Wi-Fi, Token Ring |

## Protocoale de Transport

### TCP (Transmission Control Protocol)

**Caracteristici fundamentale:**
- **Orientat pe conexiune** - necesită stabilirea unei conexiuni înainte de transfer
- **Fiabil** - garantează livrarea datelor prin mecanisme de confirmare (ACK)
- **Ordine garantată** - datele ajung în ordinea în care au fost trimise
- **Control al fluxului** - previne supraîncărcarea receptorului (fereastră glisantă)
- **Control al congestiei** - adaptează rata de transmisie la condițiile rețelei

**Handshake-ul în Trei Pași (Three-Way Handshake):**

```
Client                                  Server
   |                                      |
   |  -------- SYN (seq=x) ----------->   |  Pasul 1: Client inițiază
   |                                      |
   |  <--- SYN-ACK (seq=y, ack=x+1) ----  |  Pasul 2: Server confirmă și răspunde
   |                                      |
   |  -------- ACK (ack=y+1) ---------->  |  Pasul 3: Client confirmă
   |                                      |
   |        [Conexiune stabilită]         |
```

**Terminarea Conexiunii (Four-Way Handshake):**

```
Client                                  Server
   |                                      |
   |  -------- FIN ------------------>    |  Client vrea să închidă
   |                                      |
   |  <------- ACK -------------------    |  Server confirmă
   |                                      |
   |  <------- FIN -------------------    |  Server vrea să închidă
   |                                      |
   |  -------- ACK ------------------>    |  Client confirmă
   |                                      |
   |        [Conexiune închisă]           |
```

**Header TCP (20-60 bytes):**
- Port sursă (16 biți)
- Port destinație (16 biți)
- Număr secvență (32 biți)
- Număr confirmare (32 biți)
- Flag-uri: SYN, ACK, FIN, RST, PSH, URG
- Dimensiune fereastră
- Checksum
- Opțiuni (variabil)

### UDP (User Datagram Protocol)

**Caracteristici fundamentale:**
- **Fără conexiune** - nu necesită stabilirea prealabilă a unei conexiuni
- **Best-effort** - nu garantează livrarea
- **Fără ordine** - datagramele pot ajunge în orice ordine
- **Overhead minim** - header de doar 8 bytes
- **Rapid** - fără întârzieri de handshake sau confirmare

**Header UDP (8 bytes):**
- Port sursă (16 biți)
- Port destinație (16 biți)
- Lungime (16 biți)
- Checksum (16 biți)

**Schimb UDP:**

```
Client                                  Server
   |                                      |
   |  -------- Datagramă cerere ------>   |  Fără handshake prealabil
   |                                      |
   |  <------- Datagramă răspuns ------   |  Fără confirmare
   |                                      |
```

### Comparație TCP vs UDP

| Aspect | TCP | UDP |
|--------|-----|-----|
| Tip conexiune | Orientat pe conexiune | Fără conexiune |
| Fiabilitate | Garantată | Best-effort |
| Ordine | Păstrată | Nu este garantată |
| Viteză | Mai lent (overhead) | Mai rapid |
| Overhead header | 20-60 bytes | 8 bytes |
| Control flux | Da | Nu |
| Control congestie | Da | Nu |
| Utilizare | Web, email, fișiere | Streaming, DNS, jocuri |

## Programarea Socket-urilor

### Ce este un Socket?

Un **socket** este un punct terminal de comunicare bidirecțională. Este abstracția software care permite programelor să comunice prin rețea.

**Tipuri de socket-uri:**
- `SOCK_STREAM` - pentru TCP (flux de octeți)
- `SOCK_DGRAM` - pentru UDP (datagrame)
- `SOCK_RAW` - acces direct la stratul IP

### API Socket în Python

**Import:**
```python
import socket
```

**Creare socket TCP:**
```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

**Creare socket UDP:**
```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

### Fluxul Server TCP

```python
# 1. Creare socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Legare la adresă (bind)
server_socket.bind(('0.0.0.0', 9090))

# 3. Ascultare conexiuni
server_socket.listen(5)  # backlog = 5

# 4. Acceptare conexiune
client_socket, client_addr = server_socket.accept()

# 5. Comunicare
data = client_socket.recv(1024)
client_socket.send(response)

# 6. Închidere
client_socket.close()
server_socket.close()
```

### Fluxul Client TCP

```python
# 1. Creare socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Conectare la server
client_socket.connect(('localhost', 9090))

# 3. Comunicare
client_socket.send(message)
response = client_socket.recv(1024)

# 4. Închidere
client_socket.close()
```

### Fluxul Server UDP

```python
# 1. Creare socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Legare la adresă
server_socket.bind(('0.0.0.0', 9091))

# 3. Recepție datagrame (nu există accept!)
data, client_addr = server_socket.recvfrom(1024)

# 4. Trimitere răspuns
server_socket.sendto(response, client_addr)

# 5. Închidere
server_socket.close()
```

### Fluxul Client UDP

```python
# 1. Creare socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Trimitere datagramă (nu există connect!)
client_socket.sendto(message, ('localhost', 9091))

# 3. Recepție răspuns
response, server_addr = client_socket.recvfrom(1024)

# 4. Închidere
client_socket.close()
```

## Concurența în Servere

### Server Iterativ (Secvențial)

- Procesează un singur client la un moment dat
- Clienții noi așteaptă în coadă
- Simplu de implementat
- Nepotrivit pentru servere cu mulți clienți

### Server Concurent (Threaded)

- Procesează mai mulți clienți simultan
- Fiecare client are propriul thread
- Mai complex, necesită sincronizare
- Scalabil pentru mai mulți clienți

**Exemplu server threaded:**
```python
import threading

def handle_client(client_socket, address):
    # Procesare client
    pass

while True:
    client_socket, address = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, address))
    thread.start()
```

## Porturi și Adrese

### Porturi Cunoscute

| Port | Protocol | Serviciu |
|------|----------|----------|
| 20, 21 | TCP | FTP |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | UDP/TCP | DNS |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |

### Intervale de Porturi

- **0-1023**: Porturi de sistem (necesită privilegii root)
- **1024-49151**: Porturi înregistrate (pentru aplicații)
- **49152-65535**: Porturi dinamice/private

### Adrese Speciale

- **127.0.0.1**: Localhost (loopback)
- **0.0.0.0**: Toate interfețele (pentru bind)
- **255.255.255.255**: Broadcast

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
