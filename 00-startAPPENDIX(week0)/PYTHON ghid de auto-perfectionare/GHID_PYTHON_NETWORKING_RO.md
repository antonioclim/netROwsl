# 🐍 Python pentru Rețele de Calculatoare
## Ghid Elaborat de Auto-Studiu

> **Material complementar** pentru cursul de Rețele de Calculatoare  
> **Repository:** [github.com/antonioclim/netROwsl](https://github.com/antonioclim/netROwsl)  
> **Status:** Opțional, fără evaluare  
> **Mediu:** WSL2 + Ubuntu 22.04 + Docker + Portainer

---

## 📋 Cuprins

1. [Despre Acest Ghid](#despre-acest-ghid)
2. [Structura Repository-ului](#structura-repository-ului)
3. [Pașii de Învățare](#pașii-de-învățare)
   - [Pas 1: Citirea Codului Python](#pas-1-citirea-codului-python)
   - [Pas 2: Tipuri de Date pentru Networking](#pas-2-tipuri-de-date-pentru-networking)
   - [Pas 3: Socket Programming](#pas-3-socket-programming)
   - [Pas 4: Organizarea Codului](#pas-4-organizarea-codului)
   - [Pas 5: Interfețe CLI](#pas-5-interfețe-cli)
   - [Pas 6: Analiza Pachetelor](#pas-6-analiza-pachetelor)
   - [Pas 7: Concurență](#pas-7-concurență)
   - [Pas 8: HTTP și Protocoale Aplicație](#pas-8-http-și-protocoale-aplicație)
   - [Pas 9: Practici și Debugging](#pas-9-practici-și-debugging)
4. [Exerciții de Explorare pe Săptămâni](#exerciții-de-explorare-pe-săptămâni)
5. [Referință Rapidă Python-Networking](#referință-rapidă-python-networking)
6. [Resurse Suplimentare](#resurse-suplimentare)

---

## Despre Acest Ghid

Exercițiile de laborator la Rețele de Calculatoare folosesc **Python** ca instrument principal de implementare. Acest ghid **nu este obligatoriu** — laboratoarele pot fi parcurse și fără el.

### Pentru Cine Este?

- Studenți care vor să înțeleagă *de ce* codul arată într-un anumit fel
- Cei curioși să modifice sau să extindă exercițiile existente
- Programatori cu experiență în C/JavaScript/Java care vor tranziție rapidă la Python

### Cum să Folosești Ghidul

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SĂPTĂMÂNA DE LABORATOR                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Exerciții obligatorii (kit-ul săptămânii din XXroWSL/)              │   │
│  │ → Rulezi scripturile, completezi TODO-urile                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ OPȚIONAL: Pasul corespunzător din acest ghid                        │   │
│  │ → Înțelegi conceptele Python din spatele codului                    │   │
│  │ → Explorezi exerciții suplimentare de aprofundare                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Structura Repository-ului

Repository-ul `netROwsl` are o structură consistentă pentru fiecare săptămână:

```
netROwsl/
├── 01roWSL/                          # Săptămâna 1
│   ├── src/
│   │   ├── exercises/                # ← EXERCIȚIILE PRINCIPALE
│   │   │   ├── ex_1_01_latenta_ping.py
│   │   │   ├── ex_1_02_tcp_server_client.py
│   │   │   ├── ex_1_03_parsare_csv.py
│   │   │   ├── ex_1_04_statistici_pcap.py
│   │   │   └── ex_1_05_intarziere_transmisie.py
│   │   ├── apps/                     # Aplicații demonstrative complete
│   │   └── utils/                    # Funcții helper reutilizabile
│   │       └── net_utils.py
│   ├── scripts/                      # Scripturi de orchestrare
│   │   ├── porneste_lab.py
│   │   ├── opreste_lab.py
│   │   ├── captura_trafic.py
│   │   └── utils/
│   │       ├── docker_utils.py
│   │       ├── logger.py
│   │       └── network_utils.py
│   ├── docker/                       # Configurări Docker
│   │   ├── Dockerfile.lab
│   │   └── docker-compose.yml
│   ├── docs/                         # Documentație
│   │   ├── rezumat_teoretic.md
│   │   ├── fisa_comenzi.md
│   │   ├── depanare.md
│   │   └── lecturi_suplimentare.md
│   ├── tests/                        # Teste automate
│   │   ├── test_exercitii.py
│   │   ├── test_mediu.py
│   │   └── test_rapid.py
│   ├── homework/                     # Teme pentru acasă
│   └── README.md
├── 02roWSL/                          # Săptămâna 2
├── ...
└── 14roWSL/                          # Săptămâna 14
```

### Tabel de Corespondență Săptămâni

| Folder | Săptămână | Temă Networking | Pas Python Corelat |
|--------|-----------|-----------------|-------------------|
| `01roWSL` | S1-2 | Fundamentele rețelelor | Pas 1: Citirea codului |
| `02roWSL` | S2-3 | Socket programming TCP/UDP | Pas 2 + Pas 3: Tipuri + Sockets |
| `03roWSL` | S3 | Broadcast, Multicast, Tunnel | Pas 3: Sockets avansate |
| `04roWSL` | S4 | Physical/Data Link Layer | Pas 4: Organizare cod |
| `05roWSL` | S5 | Network Layer, IP, Subnetting | Pas 5: CLI argparse |
| `06roWSL` | S6 | NAT/PAT, SDN | Pas 6: Analiză pachete |
| `07roWSL` | S7 | Packet filtering, Firewall | Pas 6: Analiză (continuare) |
| `08roWSL` | S8 | Transport Layer, HTTP | Pas 7 + Pas 8 |
| `09roWSL` | S9 | Session/Presentation Layer | Pas 8: HTTP |
| `10roWSL` | S10 | Application Layer protocols | Pas 8: Protocoale aplicație |
| `11roWSL` | S11 | Load balancing, DNS | Pas 8: REST, DNS |
| `12roWSL` | S12 | Email, RPC | Pas 8: Protocoale aplicație |
| `13roWSL` | S13 | IoT, Security | Pas 7 + Pas 9 |
| `14roWSL` | S14 | Recap, Proiecte | Pas 9: Best practices |

---

## Pașii de Învățare

### Pas 1: Citirea Codului Python
**📅 Corelat cu:** Săptămânile 1-2 (`01roWSL`, `02roWSL`)

#### De Ce Contează

Înainte de a modifica scripturile din laborator, trebuie să le poți citi și înțelege. Exercițiile încep cu cod funcțional pe care îl vei adapta.

#### Fișiere de Referință

Deschide și studiază structura acestor fișiere:
- `01roWSL/src/exercises/ex_1_01_latenta_ping.py`
- `01roWSL/src/exercises/ex_1_02_tcp_server_client.py`

#### Concepte Cheie din Cod

**1. Shebang și Docstring**
```python
#!/usr/bin/env python3
"""
Exercițiul 1.01: Măsurarea Latenței cu Ping
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest exercițiu demonstrează măsurarea latenței rețelei...
"""
```
- Prima linie spune shell-ului ce interpretor să folosească
- Docstring-ul (între `"""`) documentează modulul

**2. Dataclasses — Structuri de Date**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class RezultatPing:
    """Stochează rezultatul unui singur ping."""
    secventa: int
    rtt_ms: Optional[float]
    reusit: bool
    mesaj: str = ""
```
Compară cu `struct` din C:
```c
// Echivalent C
typedef struct {
    int secventa;
    float rtt_ms;  // poate fi NULL?
    bool reusit;
    char mesaj[256];
} RezultatPing;
```

**3. Type Hints (Opționale dar Utile)**
```python
def masoara_latenta(gazda: str, numar: int = 3) -> float:
    """Măsoară latența medie către un host."""
    # implementare
    return media_ms
```
- `gazda: str` — parametrul este un string
- `numar: int = 3` — parametru opțional cu valoare implicită
- `-> float` — funcția returnează un float

**4. Comparație Rapidă Sintaxă**

| Concept | C/Java | JavaScript | Python |
|---------|--------|------------|--------|
| Declarare variabilă | `int x = 5;` | `let x = 5;` | `x = 5` |
| Funcție | `int f(int x) {...}` | `function f(x) {...}` | `def f(x):` |
| Condiție | `if (x > 0) {...}` | `if (x > 0) {...}` | `if x > 0:` |
| Buclă | `for (int i=0; i<n; i++)` | `for (let i=0; i<n; i++)` | `for i in range(n):` |
| Array | `int arr[] = {1,2,3}` | `let arr = [1,2,3]` | `arr = [1, 2, 3]` |
| Dicționar | `HashMap<>` | `{key: value}` | `{key: value}` |

#### Explorare Practică

1. **Rulează** `ex_1_01_latenta_ping.py`:
   ```bash
   cd /mnt/d/NETWORKING/netROwsl/01roWSL
   python3 src/exercises/ex_1_01_latenta_ping.py --gazda 127.0.0.1 --numar 5
   ```

2. **Identifică** în cod:
   - Ce face decoratorul `@dataclass`?
   - Ce înseamnă `Optional[float]`?
   - Cum funcționează `subprocess.run()`?

3. **Modifică** parametrul implicit pentru `--numar` de la 3 la 10 și rulează din nou.

---

### Pas 2: Tipuri de Date pentru Networking
**📅 Corelat cu:** Săptămânile 2-3 (`02roWSL`, `03roWSL`)

#### De Ce Contează

Rețelele transportă **bytes**, nu text. Python face diferența explicită între `str` (text) și `bytes` (date brute) — o distincție critică pentru networking.

#### Fișiere de Referință

- `02roWSL/src/exercises/ex_2_01_tcp.py`
- `02roWSL/src/exercises/ex_2_02_udp.py`

#### Concepte Cheie

**1. Bytes vs. Strings**
```python
# String (text pentru oameni)
mesaj_text = "GET /index.html HTTP/1.1"

# Bytes (ce se trimite efectiv pe rețea)
mesaj_bytes = b"GET /index.html HTTP/1.1"

# Conversie
mesaj_bytes = mesaj_text.encode('utf-8')
mesaj_text = mesaj_bytes.decode('utf-8')
```

**De ce contează?** Socket-urile trimit și primesc `bytes`. Consolă afișează `str`. Trebuie să convertești mereu.

**2. Dataclasses pentru Structuri Protocol**
```python
from dataclasses import dataclass

@dataclass
class InfoPachet:
    ip_sursa: str
    ip_dest: str
    protocol: int
    lungime: int

# Creare instanță
pkt = InfoPachet("192.168.1.1", "8.8.8.8", 6, 1500)
print(pkt.ip_sursa)  # 192.168.1.1
```

**3. List Comprehensions — Procesare Compactă**
```python
# Mod clasic (ca în C/Java)
porturi = []
for i in range(1, 101):
    if i % 2 == 0:
        porturi.append(i)

# Python idiomatic — o singură linie
porturi = [i for i in range(1, 101) if i % 2 == 0]
```

**4. Dict Comprehensions pentru Parsare**
```python
# Parsare headers HTTP într-o singură expresie
raw = "Host: localhost\r\nContent-Type: text/html"
headers = {
    cheie: valoare 
    for linie in raw.split('\r\n') 
    for cheie, valoare in [linie.split(': ')]
}
# Rezultat: {'Host': 'localhost', 'Content-Type': 'text/html'}
```

#### Explorare Practică

În `02roWSL/src/exercises/ex_2_01_tcp.py`:
1. Găsește unde se face conversia `encode()`/`decode()`
2. Observă cum se folosește `sendall()` vs `send()`
3. Ce se întâmplă dacă trimiți `str` în loc de `bytes`?

---

### Pas 3: Socket Programming
**📅 Corelat cu:** Săptămânile 2-4 (`02roWSL`, `03roWSL`, `04roWSL`)

#### De Ce Contează

Socket-urile sunt fundamentul comunicării în rețea. Exercițiile implementează servere și clienți TCP/UDP.

#### Fișiere de Referință

- `02roWSL/src/exercises/ex_2_01_tcp.py` — Server/Client TCP
- `02roWSL/src/exercises/ex_2_02_udp.py` — Server/Client UDP
- `03roWSL/src/exercises/ex_3_01_udp_broadcast.py` — UDP Broadcast
- `03roWSL/src/exercises/ex_3_02_udp_multicast.py` — UDP Multicast
- `03roWSL/src/exercises/ex_3_03_tcp_tunnel.py` — TCP Tunnel

#### Comparație C vs. Python

**Client TCP în C:**
```c
int sock = socket(AF_INET, SOCK_STREAM, 0);
struct sockaddr_in serv_addr;
serv_addr.sin_family = AF_INET;
serv_addr.sin_port = htons(8080);
inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);
connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
send(sock, "Hello", 5, 0);
char buffer[1024];
recv(sock, buffer, 1024, 0);
close(sock);
```

**Client TCP în Python:**
```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("127.0.0.1", 8080))
    sock.sendall(b"Hello")
    response = sock.recv(1024)
# Socket-ul se închide automat la ieșirea din 'with'
```

#### Context Managers (`with`)

`with` garantează că resursa se închide chiar dacă apare o excepție:
```python
# Fără with (risc de leak)
sock = socket.socket(...)
sock.connect(...)
data = sock.recv(1024)  # Dacă aici apare eroare?
sock.close()  # Nu se mai execută!

# Cu with (safe)
with socket.socket(...) as sock:
    sock.connect(...)
    data = sock.recv(1024)
# close() apelat automat, indiferent de erori
```

#### Server TCP Minimal

Din `02roWSL/src/exercises/ex_2_01_tcp.py`:
```python
def run_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        print(f"Server pornit pe {host}:{port}")
        
        while True:
            conn, addr = server.accept()
            with conn:
                data = conn.recv(1024)
                conn.sendall(b"OK: " + data.upper())
```

#### Diferențe TCP vs. UDP

| Aspect | TCP (`SOCK_STREAM`) | UDP (`SOCK_DGRAM`) |
|--------|--------------------|--------------------|
| Conexiune | `connect()` necesar | Nu necesită conexiune |
| Trimitere | `send()`, `sendall()` | `sendto(data, addr)` |
| Primire | `recv()` | `recvfrom()` → (data, addr) |
| Garantii | Ordonat, fără pierderi | Fără garantii |
| Overhead | Mai mare | Mai mic |

#### Explorare Practică

1. Rulează serverul și clientul TCP:
   ```bash
   # Terminal 1 - Server
   python3 02roWSL/src/exercises/ex_2_01_tcp.py server --port 9090
   
   # Terminal 2 - Client
   python3 02roWSL/src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "test"
   ```

2. Compară `ex_2_01_tcp.py` și `ex_2_02_udp.py`:
   - Ce metode diferă?
   - Ce se întâmplă când serverul UDP nu rulează?

---

### Pas 4: Organizarea Codului
**📅 Corelat cu:** Săptămâna 4 (`04roWSL`)

#### De Ce Contează

Kit-urile au o structură consistentă: `src/`, `scripts/`, `utils/`. Înțelegerea organizării te ajută să navighezi și să reutilizezi codul.

#### Fișiere de Referință

- `04roWSL/src/utils/protocol_utils.py`
- `04roWSL/src/apps/binary_proto_server.py`
- `04roWSL/src/apps/text_proto_client.py`

#### Structura Modulară

```
04roWSL/src/
├── __init__.py          # Face din src/ un "pachet" Python
├── exercises/
│   ├── __init__.py
│   ├── ex1_text_client.py
│   ├── ex2_binary_client.py
│   ├── ex3_udp_sensor.py
│   └── ex4_crc_detection.py
├── apps/                # Aplicații complete demonstrative
│   ├── __init__.py
│   ├── binary_proto_client.py
│   ├── binary_proto_server.py
│   ├── text_proto_client.py
│   ├── text_proto_server.py
│   ├── udp_sensor_client.py
│   └── udp_sensor_server.py
└── utils/               # Funcții helper reutilizabile
    ├── __init__.py
    └── protocol_utils.py
```

#### Ce Face `__init__.py`?

Transformă un folder într-un pachet Python importabil:
```python
# src/utils/__init__.py
from .protocol_utils import calculeaza_crc, valideaza_frame
from .net_utils import format_mac, parse_ip

__all__ = ['calculeaza_crc', 'valideaza_frame', 'format_mac', 'parse_ip']
```

Apoi poți importa:
```python
from src.utils import calculeaza_crc
```

#### Pattern de Import

```python
# Import din biblioteca standard
import socket
from dataclasses import dataclass

# Import din pachetele proiectului
from src.utils.protocol_utils import calculeaza_crc
from scripts.utils.logger import setup_logger
```

#### Explorare Practică

1. Deschide `04roWSL/src/utils/protocol_utils.py` și vezi funcțiile disponibile
2. Găsește unde sunt importate în exerciții
3. Adaugă o funcție nouă și importeaz-o într-un exercițiu

---

### Pas 5: Interfețe CLI
**📅 Corelat cu:** Săptămâna 5 (`05roWSL`)

#### De Ce Contează

Toate exercițiile acceptă parametri din linia de comandă (`--host`, `--port`, etc.). Modulul `argparse` gestionează acest lucru.

#### Fișiere de Referință

- `05roWSL/src/exercises/ex_5_01_cidr_flsm.py`
- `05roWSL/src/exercises/ex_5_02_vlsm_ipv6.py`
- `05roWSL/src/exercises/ex_5_03_generator_quiz.py`

#### CLI Simplu

```python
import argparse

parser = argparse.ArgumentParser(description="Calculator subrețele")
parser.add_argument("retea", help="Rețea în format CIDR (ex: 192.168.1.0/24)")
parser.add_argument("--subrerete", "-s", type=int, default=4, help="Număr subrețele")
parser.add_argument("--verbose", "-v", action="store_true", help="Afișare detaliată")

args = parser.parse_args()

print(f"Împart {args.retea} în {args.subrerete} subrețele")
if args.verbose:
    print("Mod detaliat activat")
```

Utilizare:
```bash
python calculator.py 192.168.1.0/24 --subrerete 8 -v
```

#### Subcomandă (Stil Git)

```python
parser = argparse.ArgumentParser(prog="netutil")
subparsers = parser.add_subparsers(dest="comanda", required=True)

# netutil scan ...
scan_parser = subparsers.add_parser("scan", help="Scanare porturi")
scan_parser.add_argument("target", help="IP țintă")
scan_parser.add_argument("--ports", default="1-1024")

# netutil calc ...
calc_parser = subparsers.add_parser("calc", help="Calculator subrețele")
calc_parser.add_argument("cidr", help="Rețea CIDR")

args = parser.parse_args()

if args.comanda == "scan":
    scaneaza(args.target, args.ports)
elif args.comanda == "calc":
    calculeaza(args.cidr)
```

#### Validare Personalizată

```python
import ipaddress

def valid_ip(value):
    """Validează că valoarea este o adresă IP validă."""
    try:
        ipaddress.ip_address(value)
        return value
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' nu este o adresă IP validă")

parser.add_argument("--ip", type=valid_ip, required=True)
```

#### Explorare Practică

1. Rulează `python3 ex_5_01_cidr_flsm.py --help` și examinează argumentele
2. Adaugă un argument nou `--output-format` cu opțiuni `text` sau `json`
3. Modifică output-ul să respecte formatul ales

---

### Pas 6: Analiza Pachetelor
**📅 Corelat cu:** Săptămânile 6-7 (`06roWSL`, `07roWSL`)

#### De Ce Contează

Laboratoarele de captură trafic și analiză pachete folosesc `struct` pentru parsing binar și topologii Mininet pentru simulare.

#### Fișiere de Referință

- `06roWSL/src/exercises/topo_nat.py` — Topologie NAT cu Mininet
- `06roWSL/src/exercises/topo_sdn.py` — Topologie SDN
- `07roWSL/src/exercises/ex_7_01_captura_referinta.py` — Captură baseline
- `07roWSL/src/apps/filtru_pachete.py` — Filtru de pachete

#### Modulul `struct` — Parsing Binar

Protocoalele de rețea au formate binare stricte. `struct` convertește între bytes și tipuri Python.

```python
import struct

# Format: ! = network byte order (big-endian)
#         H = unsigned short (2 bytes)
#         I = unsigned int (4 bytes)
#         B = unsigned char (1 byte)

# Parsare header TCP simplificat
data = b'\x00\x50\x1f\x90...'  # bytes de pe rețea
src_port, dst_port = struct.unpack('!HH', data[:4])
print(f"Port sursă: {src_port}, Port dest: {dst_port}")

# Construcție header
header = struct.pack('!HH', 8080, 443)
```

#### Tabel Formate struct

| Format | Tip C | Bytes | Python |
|--------|-------|-------|--------|
| `B` | unsigned char | 1 | int |
| `H` | unsigned short | 2 | int |
| `I` | unsigned int | 4 | int |
| `Q` | unsigned long long | 8 | int |
| `!` | network order | - | big-endian |
| `s` | char[] | n | bytes |

#### Parsare Header IP

```python
import struct
import socket

def parseaza_header_ip(raw: bytes) -> dict:
    """Extrage informații din header IP (20 bytes minim)."""
    if len(raw) < 20:
        raise ValueError("Header prea scurt")
    
    # Primii 20 bytes ai header-ului IP
    fields = struct.unpack('!BBHHHBBHII', raw[:20])
    
    version_ihl = fields[0]
    version = version_ihl >> 4      # Primii 4 biți
    ihl = (version_ihl & 0x0F) * 4  # Lungime header în bytes
    
    return {
        'version': version,
        'header_length': ihl,
        'total_length': fields[2],
        'ttl': fields[5],
        'protocol': fields[6],
        'src_ip': socket.inet_ntoa(struct.pack('!I', fields[8])),
        'dst_ip': socket.inet_ntoa(struct.pack('!I', fields[9])),
    }
```

#### Explorare Practică

1. În `07roWSL/src/apps/filtru_pachete.py`, vezi cum se filtrează pachetele
2. Extinde parserul să extragă și câmpul "Type of Service"
3. Testează cu capturi din directorul `pcap/`

---

### Pas 7: Concurență
**📅 Corelat cu:** Săptămânile 7-9 și 13 (`07roWSL`, `08roWSL`, `13roWSL`)

#### De Ce Contează

Scanarea porturilor, serverele multi-client și testele de load folosesc threading pentru paralelism.

#### Fișiere de Referință

- `13roWSL/src/exercises/ex_13_01_scanner_porturi.py` — Scanner cu ThreadPoolExecutor
- `08roWSL/src/exercises/ex_8_01_server_http.py` — Server HTTP
- `08roWSL/src/exercises/ex_8_02_proxy_invers.py` — Reverse Proxy

#### De Ce Threading pentru Rețele?

Operațiile de rețea sunt "I/O bound" — CPU-ul așteaptă răspunsuri. Threading permite procesarea simultană.

#### ThreadPoolExecutor

Din `13roWSL/src/exercises/ex_13_01_scanner_porturi.py`:
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket

def verifica_port(host: str, port: int) -> tuple[int, bool]:
    """Verifică dacă un port este deschis."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        result = sock.connect_ex((host, port))
        return (port, result == 0)
    finally:
        sock.close()

def scaneaza_porturi(host: str, porturi: list[int], workers: int = 100) -> list[int]:
    """Scanează porturile în paralel."""
    porturi_deschise = []
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Lansează toate verificările simultan
        futures = {executor.submit(verifica_port, host, p): p for p in porturi}
        
        # Colectează rezultatele pe măsură ce sosesc
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                porturi_deschise.append(port)
                print(f"Port {port} DESCHIS")
    
    return sorted(porturi_deschise)
```

#### Server cu Threading

```python
import threading

def gestioneaza_client(conn, addr):
    """Handler pentru un client."""
    try:
        data = conn.recv(1024)
        conn.sendall(b"OK: " + data.upper())
    finally:
        conn.close()

# În bucla principală:
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=gestioneaza_client, args=(conn, addr))
    thread.daemon = True  # Se oprește când main se oprește
    thread.start()
```

#### Explorare Practică

1. Rulează scanner-ul pe un target local:
   ```bash
   python3 13roWSL/src/exercises/ex_13_01_scanner_porturi.py \
       --target 127.0.0.1 --ports 1-1024 --workers 50
   ```

2. Experimentează cu diferite valori pentru `--workers` și măsoară timpul
3. Adaugă o bară de progres folosind `tqdm`

---

### Pas 8: HTTP și Protocoale Aplicație
**📅 Corelat cu:** Săptămânile 8-12 (`08roWSL` - `12roWSL`)

#### De Ce Contează

Multe exerciții implementează servere HTTP sau clienți REST. Înțelegerea protocolului la nivel de socket ajută la debugging.

#### Fișiere de Referință

- `08roWSL/src/exercises/ex_8_01_server_http.py` — Server HTTP minimal
- `08roWSL/src/exercises/ex_8_02_proxy_invers.py` — Reverse Proxy
- `10roWSL/src/exercises/ex_10_01_https.py` — HTTPS
- `10roWSL/src/exercises/ex_10_02_rest_levels.py` — Nivele REST
- `11roWSL/src/exercises/ex_11_01_backend.py` — Backend server
- `11roWSL/src/exercises/ex_11_02_loadbalancer.py` — Load Balancer
- `12roWSL/src/exercises/ex_01_smtp.py` — SMTP
- `12roWSL/src/exercises/ex_02_rpc.py` — RPC

#### Anatomia HTTP

```
GET /index.html HTTP/1.1\r\n
Host: localhost\r\n
Connection: close\r\n
\r\n
```
- Linia de request: `METHOD PATH VERSION`
- Headers: `Key: Value`
- Linie goală (`\r\n\r\n`) separă headers de body

#### Parsare Request (din `ex_8_01_server_http.py`)

```python
def parseaza_request(raw: bytes) -> tuple[str, str, str, dict[str, str]]:
    """
    Parsează un request HTTP.
    
    Returns:
        (method, path, version, headers_dict)
    """
    text = raw.decode('utf-8')
    linii = text.split('\r\n')
    
    # Prima linie: GET /path HTTP/1.1
    method, path, version = linii[0].split(' ')
    
    # Headers
    headers = {}
    for linie in linii[1:]:
        if ': ' in linie:
            cheie, valoare = linie.split(': ', 1)
            headers[cheie.lower()] = valoare
    
    return method, path, headers
```

#### Construcție Response

```python
def construieste_response(status: int, body: bytes, content_type: str = 'text/html') -> bytes:
    """Construiește un response HTTP."""
    status_text = {200: 'OK', 404: 'Not Found', 500: 'Internal Server Error'}
    
    headers = f"""HTTP/1.1 {status} {status_text.get(status, 'Unknown')}
Content-Type: {content_type}
Content-Length: {len(body)}
Connection: close

"""
    return headers.replace('\n', '\r\n').encode() + body
```

#### Biblioteca requests

```python
import requests

# GET simplu
response = requests.get('http://httpbin.org/get')
print(response.status_code)
print(response.json())

# POST cu JSON
response = requests.post(
    'http://httpbin.org/post',
    json={'cheie': 'valoare'},
    timeout=5.0
)
```

#### Explorare Practică

1. Completează TODO-urile din `ex_8_01_server_http.py`
2. Testează serverul cu `curl`:
   ```bash
   curl -v http://localhost:8080/index.html
   ```
3. Implementează metoda HEAD (returnează doar headers)

---

### Pas 9: Practici și Debugging
**📅 Corelat cu:** Săptămânile 11-14 (`11roWSL` - `14roWSL`)

#### De Ce Contează

Când extinzi exercițiile sau creezi propriile tool-uri, trebuie să scrii cod care funcționează și este ușor de depanat.

#### Fișiere de Referință

- `14roWSL/src/exercises/ex_14_01.py` — Exercițiu integrat
- `14roWSL/src/exercises/ex_14_02.py` — Load balancer avansat
- `14roWSL/src/exercises/ex_14_03.py` — Analizator PCAP
- Orice `tests/test_exercitii.py`

#### Logging în loc de print

```python
import logging

# Configurare
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Utilizare
logger.info(f"Conectare la {host}:{port}")
logger.debug(f"Date primite: {data!r}")  # debug nu apare implicit
logger.warning(f"Timeout la {host}")
logger.error(f"Conexiune eșuată: {e}")
```

#### Tratarea Excepțiilor de Rețea

```python
import socket

try:
    sock.connect((host, port))
    data = sock.recv(1024)
except socket.timeout:
    logger.warning(f"Timeout la {host}:{port}")
except ConnectionRefusedError:
    logger.warning(f"Conexiune refuzată de {host}:{port}")
except ConnectionResetError:
    logger.error(f"Conexiune resetată de {host}")
except OSError as e:
    logger.error(f"Eroare OS: {e}")
finally:
    sock.close()
```

#### Debugging Rapid

```python
# Afișare variabile cu context (Python 3.8+)
x = calcul_complex()
print(f"{x=}")  # Afișează: x=valoarea

# Breakpoint interactiv
import pdb; pdb.set_trace()  # Oprește execuția aici
# sau în Python 3.7+:
breakpoint()
```

#### Teste cu pytest

Din `tests/test_exercitii.py`:
```python
import pytest
from src.exercises.ex_8_01_server_http import parseaza_request

def test_parseaza_request_get():
    raw = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
    method, path, headers = parseaza_request(raw)
    
    assert method == "GET"
    assert path == "/index.html"
    assert headers["host"] == "localhost"

def test_parseaza_request_invalid():
    with pytest.raises(ValueError):
        parseaza_request(b"invalid request")
```

Rulare:
```bash
cd 08roWSL
python3 -m pytest tests/test_exercitii.py -v
```

#### Explorare Practică

1. Adaugă logging în `ex_14_01.py` pentru a urmări fluxul execuției
2. Scrie un test pentru o funcție existentă
3. Folosește `breakpoint()` pentru a inspecta starea în timpul execuției

---

## Exerciții de Explorare pe Săptămâni

### Săptămâna 1-2: Fundamentele

| Fișier | Ce să explorezi | Concept Python |
|--------|-----------------|----------------|
| `ex_1_01_latenta_ping.py` | `@dataclass`, `subprocess.run()` | Dataclasses, subprocese |
| `ex_1_02_tcp_server_client.py` | `socket`, `threading` | Sockets de bază |
| `ex_1_03_parsare_csv.py` | `csv` module, comprehensions | Procesare date |
| `ex_1_04_statistici_pcap.py` | Citire fișiere binare | I/O fișiere |
| `ex_1_05_intarziere_transmisie.py` | Calcule timing | Funcții matematice |

### Săptămâna 2-3: Sockets

| Fișier | Ce să explorezi | Concept Python |
|--------|-----------------|----------------|
| `ex_2_01_tcp.py` | `SOCK_STREAM`, `accept()` | TCP sockets |
| `ex_2_02_udp.py` | `SOCK_DGRAM`, `sendto()` | UDP sockets |
| `ex_3_01_udp_broadcast.py` | `SO_BROADCAST` | Socket options |
| `ex_3_02_udp_multicast.py` | `IP_ADD_MEMBERSHIP` | Multicast |
| `ex_3_03_tcp_tunnel.py` | Port forwarding | Threading + sockets |

### Săptămâna 4-5: Protocoale și CLI

| Fișier | Ce să explorezi | Concept Python |
|--------|-----------------|----------------|
| `ex_4_*.py` | Protocoale text/binare | `struct`, protocol design |
| `ex_5_01_cidr_flsm.py` | `ipaddress` module | IP manipulation |
| `ex_5_02_vlsm_ipv6.py` | IPv6 handling | Network calculations |
| `ex_5_03_generator_quiz.py` | CLI interactiv | `argparse` avansat |

### Săptămâna 6-9: NAT, Firewall, HTTP

| Fișier | Ce să explorezi | Concept Python |
|--------|-----------------|----------------|
| `topo_nat.py`, `topo_sdn.py` | Mininet integration | Network simulation |
| `ex_7_01_captura_referinta.py` | Packet capture | Binary parsing |
| `ex_8_01_server_http.py` | HTTP from scratch | Protocol implementation |
| `ex_8_02_proxy_invers.py` | Request forwarding | Proxy pattern |
| `ex_9_01_endianness.py` | Byte order | `struct` packing |
| `ex_9_02_pseudo_ftp.py` | FTP protocol | State machine |

### Săptămâna 10-14: Aplicații

| Fișier | Ce să explorezi | Concept Python |
|--------|-----------------|----------------|
| `ex_10_01_https.py` | TLS/SSL | `ssl` module |
| `ex_10_02_rest_levels.py` | REST architecture | HTTP methods |
| `ex_11_02_loadbalancer.py` | Round-robin | Load balancing |
| `ex_11_03_dns_client.py` | DNS queries | UDP protocol |
| `ex_12_*` | SMTP, RPC | Application protocols |
| `ex_13_01_scanner_porturi.py` | Parallel scanning | `concurrent.futures` |
| `ex_13_02_client_mqtt.py` | MQTT protocol | IoT messaging |
| `ex_14_*` | Integration | Toate conceptele |

---

## Referință Rapidă Python-Networking

### Biblioteci Esențiale

```python
# Networking de bază
import socket                    # Sockets TCP/UDP
import ssl                       # TLS/SSL wrapper
import struct                    # Binary packing/unpacking

# IP și adrese
import ipaddress                 # IP address manipulation

# CLI
import argparse                  # Command line arguments

# Concurență
import threading                 # Thread-based parallelism
from concurrent.futures import ThreadPoolExecutor

# HTTP (client)
import requests                  # pip install requests

# Logging
import logging

# JSON
import json

# Procese
import subprocess
```

### Socket Cheatsheet

```python
# TCP Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(5)
conn, addr = server.accept()
data = conn.recv(1024)
conn.sendall(b"response")
conn.close()

# TCP Client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))
client.sendall(b"request")
response = client.recv(1024)
client.close()

# UDP Server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 8080))
data, addr = server.recvfrom(1024)
server.sendto(b"response", addr)

# UDP Client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"request", ('127.0.0.1', 8080))
response, _ = client.recvfrom(1024)
```

### struct Format Codes

```python
# Network byte order (big-endian): prefix cu '!'
struct.pack('!H', 8080)         # unsigned short (2 bytes)
struct.pack('!I', 0xC0A80101)   # unsigned int (4 bytes)
struct.pack('!4s', b'\xC0\xA8\x01\x01')  # 4 bytes string

# Unpack
port, = struct.unpack('!H', data[:2])
ip_int, = struct.unpack('!I', data[2:6])
```

---

## Resurse Suplimentare

### Documentație Oficială
- [Python Socket HOWTO](https://docs.python.org/3/howto/sockets.html)
- [struct Module](https://docs.python.org/3/library/struct.html)
- [ipaddress Module](https://docs.python.org/3/library/ipaddress.html)
- [argparse Tutorial](https://docs.python.org/3/howto/argparse.html)

### Practică
- [Exercism Python Track](https://exercism.org/tracks/python)
- [Build Your Own X - Network Stack](https://github.com/codecrafters-io/build-your-own-x)

### Cărți (Opțional)
- "Black Hat Python" — Network security cu Python
- "Foundations of Python Network Programming"

---

## FAQ

**Î: Trebuie să parcurg toți pașii în ordine?**  
R: Nu. Poți sări la pasul relevant pentru laboratorul curent.

**Î: Ce fac dacă nu înțeleg ceva?**  
R: Rulează codul, modifică valori, observă ce se schimbă. Experimentarea e cel mai bun profesor.

**Î: Trebuie să memorez sintaxa?**  
R: Nu. Folosește documentația și exemplele din kit-uri.

**Î: Cum testez dacă am înțeles?**  
R: Încearcă să modifici un exercițiu existent sau să adaugi o funcționalitate nouă.

---

*Material realizat ca suport opțional pentru cursul de Rețele de Calculatoare.*  
*Repository: [github.com/antonioclim/netROwsl](https://github.com/antonioclim/netROwsl)*  
*Versiune: Ianuarie 2025*
