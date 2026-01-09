# Python pentru Rețele de Calculatoare
## Ghid de Auto-Studiu Opțional

> **Material complementar** pentru cursul de Computer Networks  
> **Status:** Opțional, fără evaluare  
> **Scop:** Aprofundarea Python în contextul exercițiilor de laborator  
> **Audiență:** Studenți care doresc să înțeleagă mai bine codul Python din kit-urile de laborator

---

## Despre Acest Ghid

Exercițiile de laborator la Computer Networks folosesc Python ca instrument principal. Acest ghid **nu este obligatoriu** — poți parcurge laboratoarele și fără el. Este destinat celor care:

- Vor să înțeleagă *de ce* codul din exerciții arată așa cum arată
- Sunt curioși să modifice sau să extindă exercițiile existente
- Doresc să-și construiască propriile instrumente de diagnostic de rețea
- Au background în alte limbaje (C, JavaScript, Java) și vor să facă tranziția rapid

**Format:** Fiecare pas este corelat cu săptămânile de laborator și poate fi parcurs independent, în ritmul propriu.

---

## Cum să Folosești Acest Ghid

```
┌─────────────────────────────────────────────────────────────────┐
│  SĂPTĂMÂNA DE LABORATOR                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Exerciții obligatorii (kit-ul săptămânii)               │   │
│  │ → Rulezi scripturile, completezi TODO-urile             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ OPȚIONAL: Pasul corespunzător din acest ghid            │   │
│  │ → Înțelegi conceptele Python folosite                   │   │
│  │ → Explorezi exerciții suplimentare                      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Timp estimat per pas:** 2-4 ore (flexibil, în funcție de interesul personal)

---

## Corelația cu Săptămânile de Laborator

| Săptămână Lab | Temă Networking | Pas Python Corelat |
|---------------|-----------------|-------------------|
| S1-2 | Fundamentele rețelelor, Modele arhitecturale | Pas 1: Primii pași |
| S2-3 | Socket programming TCP/UDP | Pas 2: Tipuri de date + Pas 3: Sockets |
| S4 | Physical Layer, Data Link, Protocoale custom | Pas 4: Organizare cod |
| S5 | Network Layer, IP, Subnetting | Pas 5: CLI cu argparse |
| S6 | NAT/PAT, SDN | Pas 6: Analiza pachetelor |
| S7 | Packet filtering, Firewall | Pas 6: Analiza pachetelor (continuare) |
| S8 | Transport Layer, HTTP | Pas 7: Concurență + Pas 8: HTTP |
| S9 | Session/Presentation Layer | Pas 8: HTTP (continuare) |
| S10-11 | Application Layer, REST, DNS, FTP | Pas 8: HTTP & REST |
| S12 | Email, RPC | Pas 8: Protocoale aplicație |
| S13 | IoT, Security | Pas 9: Best practices |
| S14 | Recap, Proiecte | Pas 9: Best practices |

---

## PASUL 1: Primii Pași — Citirea Codului Python
**Corelat cu:** Săptămânile 1-2 (Fundamentele rețelelor)

### De ce contează

În kit-urile de laborator vei întâlni scripturi precum `ex_1_01_ping_latency.py`. Înainte de a le modifica, trebuie să le poți citi.

### Ce vei învăța

- Structura unui script Python
- Diferențele sintactice față de C/JavaScript
- Cum să rulezi și să modifici parametrii scripturilor

### Concepte cheie explicate

**Shebang și encoding:**
```python
#!/usr/bin/env python3
"""Docstring - descrierea modulului."""
```
Prima linie spune shell-ului ce interpretor să folosească. Ghilimelele triple sunt docstring-uri (documentație).

**Tipuri fără declarație explicită:**
```python
# C/Java
int port = 8080;
String host = "localhost";

# Python - tipul se deduce automat
port = 8080
host = "localhost"
```

**Indentarea definește blocurile:**
```python
# Python folosește indentare, nu acolade
if port > 1024:
    print("Port neprivilegiat")
    print("Poate fi folosit fără sudo")
else:
    print("Port privilegiat")
```

**Funcții și type hints (opționale dar utile):**
```python
def measure_latency(host: str, count: int = 3) -> float:
    """Măsoară latența medie către un host."""
    # implementare
    return average_ms
```
Type hints (`host: str`, `-> float`) nu sunt obligatorii dar ajută la înțelegere.

### Exercițiu de explorare

Deschide `1enWSL/src/exercises/ex_1_01_ping_latency.py` și identifică:
1. Ce face decoratorul `@dataclass`?
2. Ce înseamnă `float | None`?
3. Cum funcționează `subprocess.run()`?

### Resurse suplimentare

- [Python for Programmers](https://docs.python.org/3/tutorial/) — tutorial oficial
- Compară sintaxa: [Learn X in Y minutes - Python](https://learnxinyminutes.com/docs/python/)

---

## PASUL 2: Tipuri de Date pentru Networking
**Corelat cu:** Săptămânile 2-3 (Socket programming)

### De ce contează

Rețelele transportă **bytes**, nu text. Python face diferența explicită între `str` (text) și `bytes` (date brute).

### Concepte cheie explicate

**Bytes vs. Strings:**
```python
# String (text pentru oameni)
mesaj_text = "GET /index.html HTTP/1.1"

# Bytes (ce se trimite efectiv pe rețea)
mesaj_bytes = b"GET /index.html HTTP/1.1"

# Conversie
mesaj_bytes = mesaj_text.encode('utf-8')
mesaj_text = mesaj_bytes.decode('utf-8')
```

**De ce contează?** Când primești date de pe un socket, primești `bytes`. Când afișezi în consolă, ai nevoie de `str`.

**Dataclasses — struct-uri moderne:**
```python
from dataclasses import dataclass

@dataclass
class PacketInfo:
    src_ip: str
    dst_ip: str
    protocol: int
    length: int

# Creare instanță
pkt = PacketInfo("192.168.1.1", "8.8.8.8", 6, 1500)
print(pkt.src_ip)  # 192.168.1.1
```
Similar cu `struct` din C, dar cu mai multe facilități automate.

**List comprehensions — procesare compactă:**
```python
# Mod clasic (ca în C/Java)
ports = []
for i in range(1, 101):
    if i % 2 == 0:
        ports.append(i)

# Python idiomatic
ports = [i for i in range(1, 101) if i % 2 == 0]
```

**Dict comprehensions pentru parsare:**
```python
# Parsare headers HTTP într-o singură expresie
raw = "Host: localhost\r\nContent-Type: text/html"
headers = {
    k: v 
    for line in raw.split('\r\n') 
    for k, v in [line.split(': ')]
}
# {'Host': 'localhost', 'Content-Type': 'text/html'}
```

### Exercițiu de explorare

În `2enWSL/src/exercises/`, găsește cum se face conversia între bytes și string în codul TCP/UDP.

---

## PASUL 3: Socket Programming în Python
**Corelat cu:** Săptămânile 2-4 (TCP/UDP, Comunicare în rețea)

### De ce contează

Exercițiile de laborator implementează servere și clienți TCP/UDP. Înțelegerea API-ului de sockets din Python te ajută să modifici comportamentul lor.

### Concepte cheie explicate

**Comparație C vs. Python:**

```c
// C - TCP Client (multe linii, gestionare manuală)
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

```python
# Python - TCP Client (compact, cleanup automat)
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("127.0.0.1", 8080))
    sock.sendall(b"Hello")
    response = sock.recv(1024)
# Socket-ul se închide automat la ieșirea din 'with'
```

**Context managers (`with`):**

`with` garantează că resursa se închide chiar dacă apare o excepție. Este echivalentul RAII din C++ sau try-with-resources din Java.

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

**Server TCP minimal:**
```python
import socket

def run_server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        print(f"Listening on {host}:{port}")
        
        while True:
            conn, addr = server.accept()
            with conn:
                data = conn.recv(1024)
                conn.sendall(b"OK: " + data.upper())
```

### Exercițiu de explorare

Compară `ex_2_01_tcp.py` și `ex_2_02_udp.py`. Ce diferențe observi între `SOCK_STREAM` (TCP) și `SOCK_DGRAM` (UDP)?

---

## PASUL 4: Organizarea Codului
**Corelat cu:** Săptămâna 4 (Physical Layer, Protocoale custom)

### De ce contează

Kit-urile de laborator au o structură consistentă: `src/`, `scripts/`, `utils/`. Înțelegerea organizării te ajută să navighezi și să reutilizezi codul.

### Concepte cheie explicate

**Structura unui kit de laborator:**
```
week_N/
├── src/
│   ├── __init__.py      ← face din src/ un "pachet" Python
│   ├── exercises/       ← exercițiile principale
│   │   ├── __init__.py
│   │   └── ex_N_01.py
│   └── utils/           ← funcții helper reutilizabile
│       ├── __init__.py
│       └── net_utils.py
├── scripts/             ← scripturi de orchestrare (start_lab, etc.)
├── docker/              ← configurări container
└── tests/               ← teste automate
```

**Importuri:**
```python
# Import din biblioteca standard
import socket
from dataclasses import dataclass

# Import din pachetele proiectului
from src.utils.net_utils import format_mac
from src.utils.logger import log
```

**`__init__.py` — ce face?**

Face dintr-un folder un "pachet" Python importabil. Poate fi gol sau poate exporta funcții:
```python
# src/utils/__init__.py
from .net_utils import format_mac, parse_ip
from .logger import log

__all__ = ['format_mac', 'parse_ip', 'log']
```

### Exercițiu de explorare

Deschide `scripts/utils/` din orice săptămână și vezi cum sunt organizate funcțiile helper.

---

## PASUL 5: Interfețe CLI cu argparse
**Corelat cu:** Săptămâna 5 (Network Layer, IP, Subnetting)

### De ce contează

Toate exercițiile acceptă parametri din linia de comandă (`--host`, `--port`, etc.). Modulul `argparse` gestionează acest lucru.

### Concepte cheie explicate

**CLI simplu:**
```python
import argparse

parser = argparse.ArgumentParser(description="Scanner de porturi")
parser.add_argument("target", help="Adresa IP țintă")
parser.add_argument("--port", "-p", type=int, default=80, help="Port (default: 80)")
parser.add_argument("--timeout", type=float, default=1.0)
parser.add_argument("--verbose", "-v", action="store_true")

args = parser.parse_args()

print(f"Scanez {args.target}:{args.port}")
if args.verbose:
    print(f"Timeout: {args.timeout}s")
```

```bash
# Utilizare
python scanner.py 192.168.1.1 --port 443 -v
```

**Subcomandă (stil git):**
```python
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True)

# python tool.py scan ...
scan_parser = subparsers.add_parser("scan")
scan_parser.add_argument("target")

# python tool.py discover ...
discover_parser = subparsers.add_parser("discover")
discover_parser.add_argument("--network")

args = parser.parse_args()
if args.command == "scan":
    do_scan(args.target)
elif args.command == "discover":
    do_discover(args.network)
```

**Help automat:**
```bash
python scanner.py --help
# Afișează descrierea și toate argumentele
```

### Exercițiu de explorare

Rulează `python3 ex_5_01_cidr_flsm.py --help` și examinează cum sunt definite argumentele în cod.

---

## PASUL 6: Analiza Pachetelor și Date Binare
**Corelat cu:** Săptămânile 6-7 (NAT, Firewall, Packet filtering)

### De ce contează

Laboratoarele de captură trafic și analiză pachete folosesc `struct` pentru parsing binar și uneori `scapy` pentru analiză avansată.

### Concepte cheie explicate

**Modulul struct — parsing binar:**

Protocoalele de rețea au formate binare stricte. `struct` convertește între bytes și tipuri Python.

```python
import struct

# Format: ! = network byte order (big-endian)
#         H = unsigned short (2 bytes)
#         I = unsigned int (4 bytes)

# Parsare header simplificat
data = b'\x00\x50\x1f\x90...'  # bytes de pe rețea

src_port, dst_port = struct.unpack('!HH', data[:4])
print(f"Port sursă: {src_port}, Port dest: {dst_port}")

# Construcție header
header = struct.pack('!HH', 8080, 443)
```

**Tabel formate struct:**
| Format | Tip C | Bytes | Python |
|--------|-------|-------|--------|
| `B` | unsigned char | 1 | int |
| `H` | unsigned short | 2 | int |
| `I` | unsigned int | 4 | int |
| `Q` | unsigned long long | 8 | int |
| `!` | network order | - | big-endian |

**Parsare header IP (exemplu simplificat):**
```python
def parse_ip_header(raw: bytes) -> dict:
    """Extrage informații din header IP."""
    if len(raw) < 20:
        raise ValueError("Header prea scurt")
    
    # Primii 20 bytes ai header-ului IP
    fields = struct.unpack('!BBHHHBBHII', raw[:20])
    
    version_ihl = fields[0]
    version = version_ihl >> 4  # Primii 4 biți
    
    return {
        'version': version,
        'ttl': fields[5],
        'protocol': fields[6],
        'src_ip': socket.inet_ntoa(struct.pack('!I', fields[8])),
        'dst_ip': socket.inet_ntoa(struct.pack('!I', fields[9])),
    }
```

**Scapy (dacă este instalat):**
```python
from scapy.all import rdpcap, IP, TCP

# Citire fișier PCAP
packets = rdpcap('capture.pcap')

for pkt in packets:
    if IP in pkt:
        print(f"{pkt[IP].src} -> {pkt[IP].dst}")
```

### Exercițiu de explorare

În `7enWSL/src/exercises/`, vezi cum se face captura și filtrarea pachetelor.

---

## PASUL 7: Concurență pentru Operații de Rețea
**Corelat cu:** Săptămânile 7-9 (Firewall, HTTP, Transport Layer)

### De ce contează

Scanarea porturilor, serverele multi-client și testele de load folosesc threading pentru paralelism.

### Concepte cheie explicate

**De ce threading pentru rețele?**

Operațiile de rețea sunt "I/O bound" — CPU-ul așteaptă răspunsuri. Threading permite procesarea simultană a mai multor conexiuni.

**ThreadPoolExecutor — paralelism simplu:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket

def check_port(host: str, port: int) -> tuple[int, bool]:
    """Verifică dacă un port este deschis."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        result = sock.connect_ex((host, port))
        return (port, result == 0)
    finally:
        sock.close()

def scan_ports(host: str, ports: list[int]) -> list[int]:
    """Scanează porturile în paralel."""
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        # Lansează toate verificările simultan
        futures = {executor.submit(check_port, host, p): p for p in ports}
        
        # Colectează rezultatele pe măsură ce sosesc
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
                print(f"Port {port} OPEN")
    
    return sorted(open_ports)

# Utilizare
open_ports = scan_ports("192.168.1.1", range(1, 1025))
```

**Server cu threading:**
```python
import threading

def handle_client(conn, addr):
    """Handler pentru un client."""
    try:
        data = conn.recv(1024)
        conn.sendall(b"OK")
    finally:
        conn.close()

# În bucla principală a serverului:
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.daemon = True  # Se oprește când programul principal se oprește
    thread.start()
```

### Exercițiu de explorare

În `13enWSL/src/exercises/ex_13_01_port_scanner.py`, observă cum se folosește `ThreadPoolExecutor` pentru scanare paralelă.

---

## PASUL 8: HTTP și Protocoale de Aplicație
**Corelat cu:** Săptămânile 8-12 (HTTP, REST, DNS, FTP, Email)

### De ce contează

Multe exerciții implementează servere HTTP sau clienți REST. Înțelegerea protocolului la nivel de socket ajută la debugging.

### Concepte cheie explicate

**Anatomia unui request HTTP:**
```
GET /index.html HTTP/1.1\r\n
Host: localhost\r\n
Connection: close\r\n
\r\n
```
- Linia de request: `METHOD PATH VERSION`
- Headers: `Key: Value`
- Linie goală (`\r\n\r\n`) separă headers de body

**Parsare request (din exercițiile S8):**
```python
def parse_request(raw: bytes) -> tuple[str, str, dict]:
    """Parsează request HTTP."""
    text = raw.decode('utf-8')
    lines = text.split('\r\n')
    
    # Prima linie: GET /path HTTP/1.1
    method, path, version = lines[0].split(' ')
    
    # Headers
    headers = {}
    for line in lines[1:]:
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key.lower()] = value
    
    return method, path, headers
```

**Construcție response:**
```python
def build_response(status: int, body: bytes, content_type: str = 'text/html') -> bytes:
    """Construiește response HTTP."""
    status_texts = {200: 'OK', 404: 'Not Found', 500: 'Internal Server Error'}
    
    headers = f"""HTTP/1.1 {status} {status_texts.get(status, 'Unknown')}
Content-Type: {content_type}
Content-Length: {len(body)}
Connection: close

"""
    return headers.replace('\n', '\r\n').encode() + body
```

**Biblioteca requests pentru clienți:**
```python
import requests

# GET simplu
response = requests.get('http://httpbin.org/get')
print(response.status_code)
print(response.json())

# POST cu JSON
response = requests.post(
    'http://httpbin.org/post',
    json={'key': 'value'},
    timeout=5.0
)
```

### Exercițiu de explorare

Completează TODO-urile din `8enWSL/src/exercises/ex_8_01_http_server.py` pentru a înțelege cum funcționează un server HTTP minimal.

---

## PASUL 9: Practici de Cod și Debugging
**Corelat cu:** Săptămânile 11-14 (Proiecte, Recapitulare)

### De ce contează

Când extinzi exercițiile sau creezi propriile tool-uri, trebuie să scrii cod care funcționează și este ușor de depanat.

### Concepte cheie explicate

**Logging în loc de print:**
```python
import logging

# Configurare
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Utilizare
logger.info(f"Conectare la {host}:{port}")
logger.debug(f"Date primite: {data!r}")  # debug nu apare implicit
logger.error(f"Conexiune eșuată: {e}")
```

**Tratarea excepțiilor de rețea:**
```python
import socket

try:
    sock.connect((host, port))
except socket.timeout:
    logger.warning(f"Timeout la {host}:{port}")
except ConnectionRefusedError:
    logger.warning(f"Conexiune refuzată de {host}:{port}")
except OSError as e:
    logger.error(f"Eroare OS: {e}")
finally:
    sock.close()
```

**Debugging rapid:**
```python
# Afișare variabile cu context
x = some_complex_expression()
print(f"{x=}")  # Afișează: x=valoarea_lui_x

# Breakpoint interactiv
import pdb; pdb.set_trace()  # Oprește execuția aici
# sau în Python 3.7+:
breakpoint()
```

**Type hints pentru claritate:**
```python
from typing import Optional, List, Tuple

def scan_host(
    target: str,
    ports: List[int],
    timeout: float = 0.5
) -> Tuple[List[int], int]:
    """
    Scanează porturile unui host.
    
    Returns:
        Tuple cu (porturi_deschise, porturi_închise)
    """
    ...
```

---

## Biblioteci Utile

| Bibliotecă | Scop | Instalare |
|------------|------|-----------|
| `socket` | Socket programming | *inclusă în Python* |
| `struct` | Parsing binar | *inclusă în Python* |
| `argparse` | CLI | *inclusă în Python* |
| `ipaddress` | Validare IP/CIDR | *inclusă în Python* |
| `threading` | Concurență | *inclusă în Python* |
| `concurrent.futures` | Thread pools | *inclusă în Python* |
| `logging` | Logging structurat | *inclusă în Python* |
| `scapy` | Packet crafting | `pip install scapy` |
| `requests` | HTTP client | `pip install requests` |

---

## Resurse pentru Continuare

### Documentație
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
- [Scapy Documentation](https://scapy.readthedocs.io/)

### Practică
- [Exercism Python Track](https://exercism.org/tracks/python) — exerciții progresive
- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x#build-your-own-network-stack) — proiecte hands-on

### Cărți (opțional)
- "Black Hat Python" — networking security cu Python
- "Foundations of Python Network Programming" — referință completă

---

## Întrebări Frecvente

**Q: Trebuie să parcurg toate pașii în ordine?**  
A: Nu. Poți sări la pasul relevant pentru săptămâna curentă de laborator.

**Q: Ce fac dacă nu înțeleg ceva?**  
A: Încearcă să rulezi codul și să modifici valorile. Experimentarea e cel mai bun profesor. Poți pune și întrebări în laboratoare.

**Q: Trebuie să memorez sintaxa?**  
A: Nu. Folosește documentația și exemplele din kit-uri. Cu timpul devine naturală.

**Q: Cum testez dacă am înțeles?**  
A: Încearcă să modifici un exercițiu existent sau să adaugi o funcționalitate nouă.

---

*Material realizat ca suport opțional pentru cursul de Computer Networks.*  
*Versiune: Ianuarie 2025*
