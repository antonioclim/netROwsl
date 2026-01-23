# Rezumat Teoretic

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix
>
> Săptămâna 14: Recapitulare Integrată și Evaluare Proiect

Acest document prezintă conceptele teoretice cheie acoperite pe parcursul cursului de Rețele de Calculatoare, cu accent pe elementele demonstrate în laboratorul Săptămânii 14.

---

## Cuprins

1. [Stiva TCP/IP](#stiva-tcpip)
2. [Protocolul TCP](#protocolul-tcp)
3. [Protocolul HTTP](#protocolul-http)
4. [Echilibrarea Încărcării](#echilibrarea-încărcării)
5. [NAT în Docker](#nat-în-docker)
6. [Analiza Pachetelor](#analiza-pachetelor)
7. [Programare Socket](#programare-socket)
8. [Rețele Docker](#rețele-docker)

---

## Stiva TCP/IP

### Modelul OSI vs TCP/IP

| Nivel OSI | Nivel TCP/IP | Protocoale | PDU |
|-----------|--------------|------------|-----|
| 7. Aplicație | Aplicație | HTTP, FTP, DNS, SMTP | Date |
| 6. Prezentare | Aplicație | SSL/TLS, MIME | Date |
| 5. Sesiune | Aplicație | NetBIOS, RPC | Date |
| 4. Transport | Transport | TCP, UDP | Segment/Datagramă |
| 3. Rețea | Internet | IP, ICMP, ARP | Pachet |
| 2. Legătură Date | Acces Rețea | Ethernet, Wi-Fi | Cadru |
| 1. Fizic | Acces Rețea | Cabluri, Semnale | Biți |

### Încapsulare și Decapsulare

Datele parcurg stiva de protocoale, fiecare nivel adăugând propriul antet:

```
[Date Aplicație]
     ↓ HTTP adaugă antet
[Antet HTTP | Date]
     ↓ TCP adaugă antet
[Antet TCP | Antet HTTP | Date]
     ↓ IP adaugă antet
[Antet IP | Antet TCP | Antet HTTP | Date]
     ↓ Ethernet adaugă antet și trailer
[Antet Eth | Antet IP | Antet TCP | Antet HTTP | Date | FCS]
```

---

## Protocolul TCP

### Handshake-ul în Trei Pași

#### 🧱 CONCRET (Analogie)

Imaginează-ți un apel telefonic internațional:

1. **Tu suni** → "Alo, mă auzi?" (SYN)
2. **Prietenul răspunde** → "Te aud! Tu mă auzi?" (SYN-ACK)
3. **Tu confirmi** → "Da, te aud perfect!" (ACK)

Abia după aceste trei schimburi puteți vorbi în siguranță.

#### 🖼️ PICTORIAL (Diagramă)

Stabilirea unei conexiuni TCP necesită un schimb de trei segmente:

```
Client                          Server
   |                               |
   |-------- SYN (seq=x) -------->|  ← "Vreau să vorbim, numărul meu e X"
   |                               |
   |<----- SYN-ACK (seq=y, -------|  ← "OK, numărul meu e Y, am primit X"
   |       ack=x+1)               |
   |                               |
   |-------- ACK (seq=x+1, ------>|  ← "Confirmat, am primit Y"
   |       ack=y+1)               |
   |                               |
   |===== Conexiune Stabilită ====|
```

#### 🔣 ABSTRACT (Wireshark)

În Wireshark, aplică filtrul `tcp.flags.syn == 1` pentru a vedea doar pachetele SYN.

**De observat:**
- Câmpul `Sequence Number` crește cu fiecare segment
- `Acknowledgment Number` = Sequence primit + 1
- Flags: `[SYN]`, `[SYN, ACK]`, `[ACK]`

### Flag-uri TCP

| Flag | Nume | Descriere |
|------|------|-----------|
| SYN | Synchronize | Inițiază conexiune |
| ACK | Acknowledge | Confirmă recepție |
| FIN | Finish | Termină conexiune |
| RST | Reset | Resetează conexiune |
| PSH | Push | Livrare imediată |
| URG | Urgent | Date urgente |

### Terminarea Conexiunii

#### 🧱 CONCRET

Ca la sfârșitul unui apel telefonic politicos:
1. Tu: "Trebuie să închid" (FIN)
2. Prietenul: "OK, am înțeles" (ACK)
3. Prietenul: "Și eu trebuie să închid" (FIN)  
4. Tu: "OK, pa!" (ACK)

#### 🖼️ PICTORIAL

```
Client                          Server
   |                               |
   |-------- FIN ---------------->|  ← "Am terminat de trimis"
   |<------- ACK -----------------|  ← "Am primit, OK"
   |                               |
   |<------- FIN -----------------|  ← "Și eu am terminat"
   |-------- ACK ---------------->|  ← "OK, conexiune închisă"
   |                               |
   |===== Conexiune Închisă ======|
```

---

## Protocolul HTTP

### Structura Cererii HTTP

```http
GET /api/resursa HTTP/1.1
Host: exemplu.com
User-Agent: Mozilla/5.0
Accept: application/json
Connection: keep-alive

[Corp cerere - opțional pentru POST/PUT]
```

### Structura Răspunsului HTTP

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 42
Server: nginx/1.18.0

{"status": "succes", "date": {...}}
```

### Coduri de Stare HTTP

| Categorie | Interval | Semnificație |
|-----------|----------|--------------|
| 1xx | 100-199 | Informațional |
| 2xx | 200-299 | Succes |
| 3xx | 300-399 | Redirecționare |
| 4xx | 400-499 | Eroare Client |
| 5xx | 500-599 | Eroare Server |

Coduri frecvente:
- **200 OK**: Cerere reușită
- **201 Created**: Resursă creată
- **301 Moved Permanently**: Redirecționare permanentă
- **400 Bad Request**: Cerere invalidă
- **404 Not Found**: Resursă negăsită
- **500 Internal Server Error**: Eroare server
- **503 Service Unavailable**: Serviciu indisponibil

---

## Echilibrarea Încărcării

### 🧱 CONCRET (Analogie)

Un load balancer funcționează ca un **ospătar-șef** într-un restaurant:
- Clienții (cereri HTTP) sosesc la intrare
- Ospătarul-șef (LB) îi direcționează către mese libere (backend-uri)
- Dacă un chelner (backend) e ocupat, clientul merge la altul
- Dacă un chelner e bolnav (unhealthy), nu mai primește clienți

### 🖼️ PICTORIAL (Diagramă)

```
                                    ┌─────────────┐
                                 ┌─►│  Backend 1  │ (app1:8001)
┌─────────┐      ┌────────────┐  │  └─────────────┘
│ Client  │─────►│ Load       │──┤
└─────────┘      │ Balancer   │  │  ┌─────────────┐
                 └────────────┘  └─►│  Backend 2  │ (app2:8001)
                    :8080           └─────────────┘
```

### 🔣 ABSTRACT (Algoritmi)

**Round-Robin**
- Distribuie cererile secvențial, ciclic: A → B → A → B → ...
- Simplu de implementat
- Presupune capacitate egală a serverelor

**Round-Robin Ponderat**
- Fiecare server are o pondere (greutate)
- Serverele puternice primesc mai multe cereri
- Exemplu: app1(weight=3), app2(weight=1) → 75% / 25%

**Least Connections**
- Direcționează către serverul cu cele mai puține conexiuni active
- Potrivit pentru cereri cu durată variabilă

**IP Hash**
- Folosește IP-ul clientului pentru a determina serverul
- Asigură persistența sesiunii

### Verificări de Sănătate (Health Checks)

Load balancer-ul monitorizează periodic starea backend-urilor:

```python
# Exemplu verificare sănătate
def verifica_sanatate(backend):
    try:
        raspuns = requests.get(f"http://{backend}/health", timeout=5)
        return raspuns.status_code == 200
    except:
        return False
```

### Headere de Forwarding

Load balancer-ul adaugă headere pentru a transmite informații despre clientul original:

- **X-Forwarded-For**: IP-ul original al clientului
- **X-Forwarded-Proto**: Protocol original (http/https)
- **X-Forwarded-Host**: Host-ul cerut original

---

## NAT în Docker

### Rețele Bridge

Docker folosește NAT pentru a permite containerelor să comunice:

```
┌─────────────────────────────────────────────┐
│                 GAZDĂ                        │
│                                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │Container│ │Container│ │Container│       │
│  │ 172.17. │ │ 172.17. │ │ 172.17. │       │
│  │  0.2    │ │  0.3    │ │  0.4    │       │
│  └────┬────┘ └────┬────┘ └────┬────┘       │
│       │           │           │             │
│  ┌────┴───────────┴───────────┴────┐       │
│  │         docker0 (bridge)         │       │
│  │           172.17.0.1             │       │
│  └──────────────┬──────────────────┘       │
│                 │ NAT                       │
│  ┌──────────────┴──────────────────┐       │
│  │           eth0 (gazdă)           │       │
│  │          192.168.1.100           │       │
│  └──────────────────────────────────┘       │
└─────────────────────────────────────────────┘
```

### Mapare Porturi

```yaml
# docker-compose.yml
ports:
  - "8080:80"  # gazdă:container
```

Conexiunile către `localhost:8080` sunt traduse către `container:80`.

---

## Analiza Pachetelor

### Puncte de Captură

```
┌─────────┐         ┌──────────┐         ┌─────────┐
│ Client  │◄───────►│  Switch  │◄───────►│ Server  │
└─────────┘    ▲    └──────────┘    ▲    └─────────┘
               │                    │
           Punct 1              Punct 2
          (client)             (server)
```

### Filtre Wireshark Utile

```
# Filtre de afișare
tcp.port == 8080                    # Trafic pe port specific
http.request.method == "GET"        # Cereri GET
ip.addr == 192.168.1.1              # Trafic de la/către IP
tcp.flags.syn == 1                  # Pachete SYN
http.response.code >= 400           # Răspunsuri cu erori

# Filtre de captură (BPF)
port 8080                           # Captură pe port
host 192.168.1.1                    # Captură pentru IP
tcp and port 80                     # TCP pe port 80
```

### Urmărirea Streamurilor TCP

Wireshark permite urmărirea unei conversații TCP complete:

1. Click dreapta pe pachet
2. Follow > TCP Stream
3. Vizualizare date schimbate

---

## Programare Socket

### Model Client-Server TCP

**Server:**
```python
import socket

# Creare socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind la adresă și port
server.bind(('0.0.0.0', 9090))

# Ascultă conexiuni
server.listen(5)

while True:
    # Acceptă conexiune
    client, adresa = server.accept()
    
    # Primește date
    date = client.recv(1024)
    
    # Procesează și răspunde
    client.send(b"Răspuns")
    
    # Închide conexiunea
    client.close()
```

**Client:**
```python
import socket

# Creare socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectare la server
client.connect(('localhost', 9090))

# Trimite date
client.send(b"Mesaj")

# Primește răspuns
raspuns = client.recv(1024)

# Închide conexiunea
client.close()
```

### Familia de Adrese

| Constantă | Descriere |
|-----------|-----------|
| AF_INET | IPv4 |
| AF_INET6 | IPv6 |
| AF_UNIX | Socket Unix local |

### Tipuri de Socket

| Constantă | Protocol | Caracteristici |
|-----------|----------|----------------|
| SOCK_STREAM | TCP | Fiabil, ordonat, conexiune |
| SOCK_DGRAM | UDP | Nefiabil, fără conexiune |

---

## Rețele Docker

### Tipuri de Rețele

| Tip | Descriere | Utilizare |
|-----|-----------|-----------|
| bridge | Rețea izolată, NAT | Implicit, containere pe aceeași gazdă |
| host | Folosește stiva rețea a gazdei | Performanță maximă |
| overlay | Rețea multi-gazdă | Docker Swarm |
| none | Fără rețea | Izolare completă |

### Descoperirea Serviciilor

În rețelele Docker definite de utilizator, containerele se pot găsi prin nume:

```yaml
# docker-compose.yml
services:
  app:
    networks:
      - retea_backend
  db:
    networks:
      - retea_backend

networks:
  retea_backend:
```

Containerul `app` poate accesa `db` prin `http://db:port`.

### Comunicare Inter-Container

```
┌─────────────────────────────────────────────┐
│           Rețea Docker: backend_net         │
│                                             │
│  ┌─────────┐   DNS    ┌─────────┐          │
│  │  app1   │◄────────►│  app2   │          │
│  │172.20.  │   ping   │172.20.  │          │
│  │  0.10   │◄────────►│  0.11   │          │
│  └─────────┘          └─────────┘          │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Referințe

1. Kurose, J. F. & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.

2. Tanenbaum, A. S. & Wetherall, D. J. (2021). *Computer Networks* (6th ed.). Pearson.

3. Stevens, W. R. (2011). *TCP/IP Illustrated, Volume 1: The Protocols* (2nd ed.). Addison-Wesley.

4. RFC 793 - Transmission Control Protocol

5. RFC 7230-7235 - HTTP/1.1

6. Documentație Docker Networking: https://docs.docker.com/network/

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
