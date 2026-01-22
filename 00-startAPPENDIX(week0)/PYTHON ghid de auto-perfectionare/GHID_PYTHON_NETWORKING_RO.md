# 🐍 Python pentru Rețele de Calculatoare
## Ghid Elaborat de Auto-Studiu

> **Material complementar** pentru cursul de Rețele de Calculatoare  
> **Repository:** [github.com/antonioclim/netROwsl](https://github.com/antonioclim/netROwsl)  
> **Status:** Opțional, fără evaluare  
> **Mediu:** WSL2 + Ubuntu 22.04 + Docker + Portainer  
> **Versiune:** 2.0 — Ianuarie 2025

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
4. [Verificare Înțelegere (Peer Instruction)](#verificare-înțelegere-peer-instruction)
5. [Exerciții de Explorare pe Săptămâni](#exerciții-de-explorare-pe-săptămâni)
6. [Referință Rapidă Python-Networking](#referință-rapidă-python-networking)
7. [Resurse Suplimentare](#resurse-suplimentare)

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
│   │   │   └── ...
│   │   ├── apps/                     # Aplicații demonstrative complete
│   │   └── utils/                    # Funcții helper reutilizabile
│   ├── scripts/                      # Scripturi de orchestrare
│   ├── docker/                       # Configurări Docker
│   ├── docs/                         # Documentație
│   ├── tests/                        # Teste automate
│   └── README.md
├── 02roWSL/ ... 14roWSL/
```

### Tabel de Corespondență Săptămâni

| Folder | Săptămână | Temă Networking | Pas Python Corelat |
|--------|-----------|-----------------|-------------------|
| `01roWSL` | S1-2 | Fundamentele rețelelor | Pas 1: Citirea codului |
| `02roWSL` | S2-3 | Socket programming TCP/UDP | Pas 2 + Pas 3 |
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

#### 💡 Analogie: Codul Python ca Rețetă de Bucătărie

Citirea codului Python e ca citirea unei rețete înainte să gătești:

| Element Cod | Echivalent Rețetă |
|-------------|-------------------|
| **Importurile** (`import socket`) | Lista de ingrediente — ce ai nevoie înainte să începi |
| **Funcțiile** (`def server():`) | Pașii rețetei — instrucțiuni de urmat în ordine |
| **Variabilele** (`port = 8080`) | Bolurile și castroanele — unde ții ingredientele temporar |
| **Returnul** (`return rezultat`) | Farfuria servită — rezultatul final |
| **Comentariile** (`# explicație`) | Notițele bucătarului — sfaturi pentru următoarea încercare |

**De ce contează:** Nimeni nu gătește citind rețeta cuvânt cu cuvânt în timp ce lucrează. Mai întâi o parcurgi să înțelegi fluxul, apoi execuți.

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

#### 🔍 De Ce Funcționează Așa?

**Întrebare:** De ce Python nu are `{` și `}` ca C sau Java?

**Explicație:** Python folosește **indentarea** (spații sau tab-uri) pentru a defini blocurile de cod. Asta forțează codul să fie citibil — nu poți scrie totul pe o linie. E o decizie de design a limbajului.

**Consecință practică:** Dacă amesteci tab-uri cu spații, vei primi `IndentationError`. Configurează editorul să folosească 4 spații.

#### 🔮 PREDICȚIE: Explorare Practică

Înainte să rulezi comanda de mai jos, răspunde:
1. Ce output te aștepți să vezi?
2. Ce se întâmplă dacă gazda nu există?

```bash
cd /mnt/d/NETWORKING/netROwsl/01roWSL
python3 src/exercises/ex_1_01_latenta_ping.py --gazda 127.0.0.1 --numar 5
```

<details>
<summary>✅ Verifică predicția</summary>

**Output așteptat:** 5 rezultate ping cu RTT în milisecunde către localhost.

**Dacă gazda nu există:** Ping-urile vor eșua cu timeout sau "Host unreachable".

</details>

**Identifică** în cod:
- Ce face decoratorul `@dataclass`?
- Ce înseamnă `Optional[float]`?
- Cum funcționează `subprocess.run()`?

---

### Pas 2: Tipuri de Date pentru Networking
**📅 Corelat cu:** Săptămânile 2-3 (`02roWSL`, `03roWSL`)

#### 💡 Analogie: Bytes și Strings ca Scrisori și Telegrame

| Concept | Echivalent din Viața Reală |
|---------|---------------------------|
| **String** (`str`) | Scrisoare în română pe care o citești direct |
| **Bytes** (`bytes`) | Telegramă codificată în Morse — trebuie decodată |
| **encode()** | A traduce scrisoarea în Morse pentru transmisie |
| **decode()** | A traduce Morse-ul înapoi în text lizibil |

**De ce contează:** Rețeaua "vorbește" doar în Morse (bytes). Calculatorul tău "gândește" în text (strings). Trebuie mereu să traduci.

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

#### 🔍 De Ce Funcționează Așa?

**Întrebare:** De ce Python 3 a separat strict `bytes` de `str`?

**Explicație:** În Python 2, strings erau bytes implicit, ceea ce cauza bug-uri subtile cu caractere non-ASCII (românești, chinezești, emoji). Python 3 forțează programatorul să fie explicit despre encoding, prevenind coruperea datelor.

**Consecință practică:** Dacă trimiți `str` pe un socket în loc de `bytes`, primești `TypeError`. E un reminder că rețeaua nu înțelege text direct.

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

#### 🔮 PREDICȚIE: Explorare Practică

În `02roWSL/src/exercises/ex_2_01_tcp.py`:

**Înainte să te uiți la cod, prezice:**
1. Unde se face conversia `encode()`?
2. Ce eroare apare dacă trimiți `str` în loc de `bytes`?

<details>
<summary>✅ Verifică</summary>

1. La `send()` sau `sendall()` — datele trebuie să fie bytes
2. `TypeError: a bytes-like object is required, not 'str'`

</details>

---

### Pas 3: Socket Programming
**📅 Corelat cu:** Săptămânile 2-4 (`02roWSL`, `03roWSL`, `04roWSL`)

#### 💡 Analogie: Socket-ul ca Telefon Fix

| Operație Socket | Echivalent Telefon |
|-----------------|-------------------|
| `socket()` | Cumperi un telefon nou |
| `bind()` | Îți aloci un număr de telefon (port) |
| `listen()` | Pui telefonul în priză, aștepți apeluri |
| `accept()` | Ridici receptorul când sună |
| `connect()` | Formezi numărul cuiva |
| `send()/recv()` | Vorbești / Asculți |
| `close()` | Închizi telefonul |

**TCP vs UDP:**
- **TCP** = convorbire telefonică (confirmi că celălalt e pe fir, vorbești pe rând)
- **UDP** = mesaj vocal pe robot (trimiți și speri că ajunge, fără confirmare)

#### De Ce Contează

Socket-urile sunt fundamentul comunicării în rețea. Exercițiile implementează servere și clienți TCP/UDP.

#### Fișiere de Referință

- `02roWSL/src/exercises/ex_2_01_tcp.py` — Server/Client TCP
- `02roWSL/src/exercises/ex_2_02_udp.py` — Server/Client UDP
- `03roWSL/src/exercises/ex_3_01_udp_broadcast.py` — UDP Broadcast

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

#### 🔍 De Ce Funcționează Așa?

**Întrebare:** De ce avem nevoie de `SO_REUSEADDR`?

**Explicație:** Când un server se oprește, sistemul de operare ține portul "rezervat" ~60 secunde (TIME_WAIT). Fără `SO_REUSEADDR`, nu poți reporni serverul imediat — primești "Address already in use".

**Consecință practică:** Mereu adaugă această linie înainte de `bind()`:
```python
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

#### Context Managers (`with`)

`with` garantează că resursa se închide chiar dacă apare o excepție:
```python
# Fără with (risc de resource leak)
sock = socket.socket(...)
sock.connect(...)
data = sock.recv(1024)  # Dacă aici apare eroare?
sock.close()  # Nu se mai execută!

# Cu with (sigur)
with socket.socket(...) as sock:
    sock.connect(...)
    data = sock.recv(1024)
# close() apelat automat, indiferent de erori
```

#### Server TCP Minimal

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

#### 🔮 PREDICȚIE: Explorare Practică

**Înainte să rulezi:**
```bash
# Terminal 1 - Server
python3 02roWSL/src/exercises/ex_2_01_tcp.py server --port 9090
```

**Prezice:**
1. Ce mesaj va apărea?
2. Ce se întâmplă dacă portul 9090 e deja ocupat?
3. Ce se întâmplă dacă rulezi comanda a doua oară în alt terminal?

<details>
<summary>✅ Verifică</summary>

1. "Server pornit pe 0.0.0.0:9090" sau similar
2. `OSError: Address already in use`
3. Același lucru — un singur proces poate asculta pe un port

</details>

---

### Pas 4: Organizarea Codului
**📅 Corelat cu:** Săptămâna 4 (`04roWSL`)

#### 💡 Analogie: Module Python ca Sertare într-un Dulap

| Element Cod | Echivalent Dulap |
|-------------|------------------|
| **Fișierul `.py`** | Un sertar cu un scop specific |
| **`import`** | Deschizi sertarul și iei ce ai nevoie |
| **`from X import Y`** | Deschizi sertarul X și iei doar obiectul Y |
| **`utils/`** | Sertarul cu unelte generale (șurubelnițe, bandă) |
| **`exercises/`** | Sertarul cu proiectele în lucru |
| **`__init__.py`** | Eticheta de pe sertar care spune ce conține |

**De ce contează:** Un dulap bine organizat = un proiect ușor de navigat. Găsești rapid ce cauți.

#### De Ce Contează

Kit-urile au o structură consistentă: `src/`, `scripts/`, `utils/`. Înțelegerea organizării te ajută să navighezi și să reutilizezi codul.

#### Structura Modulară

```
04roWSL/src/
├── __init__.py          # Face din src/ un "pachet" Python
├── exercises/
│   ├── __init__.py
│   ├── ex1_text_client.py
│   └── ...
├── apps/                # Aplicații complete demonstrative
│   └── ...
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

#### 🔍 De Ce Funcționează Așa?

**Întrebare:** De ce avem nevoie de `__init__.py` gol în fiecare folder?

**Explicație:** Fără el, Python nu recunoaște folderul ca pachet și nu poți face `import` din el. În Python 3.3+ poți folosi "namespace packages" fără `__init__.py`, dar explicit e mai clar.

**Consecință practică:** Când creezi un folder nou pentru module, adaugă mereu un `__init__.py` (poate fi gol).

---

### Pas 5: Interfețe CLI
**📅 Corelat cu:** Săptămâna 5 (`05roWSL`)

#### 💡 Analogie: argparse ca Meniu de Restaurant

| Element CLI | Echivalent Restaurant |
|-------------|----------------------|
| **Comanda** (`python script.py`) | Intri în restaurant |
| **Argumente poziționale** (`192.168.1.0`) | Comanda principală (obligatorie) |
| **Opțiuni** (`--verbose`) | Preferințe (cu/fără ardei) |
| **Valori default** (`port=8080`) | Porția standard dacă nu specifici |
| **`--help`** | Meniul cu explicații |

**De ce contează:** Ca la restaurant — comenzile clare evită confuzia. `--help` e mereu disponibil.

#### De Ce Contează

Toate exercițiile acceptă parametri din linia de comandă (`--host`, `--port`, etc.). Modulul `argparse` gestionează acest lucru.

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

#### 🔮 PREDICȚIE

**Înainte să rulezi:**
```bash
python3 ex_5_01_cidr_flsm.py --help
```

**Prezice:** Ce secțiuni va avea output-ul?

<details>
<summary>✅ Verifică</summary>

- usage: linia de utilizare
- description: descrierea programului
- positional arguments: argumente obligatorii
- options: argumente opționale cu explicații

</details>

---

### Pas 6: Analiza Pachetelor
**📅 Corelat cu:** Săptămânile 6-7 (`06roWSL`, `07roWSL`)

#### 💡 Analogie: Pachetele de Rețea ca Scrisori Poștale

| Element Pachet | Element Scrisoare |
|----------------|-------------------|
| **Header IP** | Plicul cu adrese (expeditor, destinatar) |
| **Header TCP** | Ștampila și numărul de înregistrare |
| **Payload** | Conținutul scrisorii din plic |
| **Checksum** | Sigiliul de ceară (verifică integritatea) |
| **TTL** | "Returnează după 30 zile dacă nu ajunge" |

**Wireshark** = camera de supraveghere de la oficiul poștal — vezi tot ce trece.

**struct.unpack()** = deschizi plicul și citești adresele în format standard.

#### De Ce Contează

Laboratoarele de captură trafic și analiză pachete folosesc `struct` pentru parsing binar.

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

#### 🔍 De Ce Funcționează Așa?

**Întrebare:** De ce folosim `!` (network byte order) și nu formatul nativ?

**Explicație:** Diferite procesoare stochează numerele diferit (little-endian vs big-endian). Rețelele folosesc mereu big-endian (standardizat în RFC-uri). `!` garantează că datele tale vor fi citite corect de orice mașină.

**Consecință practică:** Fără `!`, un pachet creat pe Windows (little-endian) ar fi citit greșit pe o mașină big-endian.

#### Tabel Formate struct

| Format | Tip C | Bytes | Python |
|--------|-------|-------|--------|
| `B` | unsigned char | 1 | int |
| `H` | unsigned short | 2 | int |
| `I` | unsigned int | 4 | int |
| `Q` | unsigned long long | 8 | int |
| `!` | network order | - | big-endian |
| `s` | char[] | n | bytes |

---

### Pas 7: Concurență
**📅 Corelat cu:** Săptămânile 7-9 și 13

#### 💡 Analogie: Threading ca Bucătari într-o Bucătărie

| Element Concurență | Echivalent Bucătărie |
|--------------------|---------------------|
| **Thread** | Un bucătar individual |
| **ThreadPool** | Echipa de bucătari |
| **Task/Future** | O comandă de la o masă |
| **Lock** | Un singur cuțit mare — doar unul îl poate folosi |
| **as_completed()** | Farfuriile gata, în ordinea în care sunt finalizate |

**De ce threading pentru rețele:** Când un bucătar așteaptă să fiarbă apa, altul poate tăia legume. Similar, când un thread așteaptă răspuns de la server, altele pot lucra.

#### De Ce Contează

Scanarea porturilor, serverele multi-client și testele de load folosesc threading pentru paralelism.

#### ThreadPoolExecutor

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
        futures = {executor.submit(verifica_port, host, p): p for p in porturi}
        
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                porturi_deschise.append(port)
                print(f"Port {port} DESCHIS")
    
    return sorted(porturi_deschise)
```

#### 🔍 De Ce Funcționează Așa?

**Întrebare:** De ce `max_workers=100` și nu 1000?

**Explicație:** Fiecare thread consumă memorie (~8MB stack). 1000 de thread-uri = 8GB RAM doar pentru stack-uri. 100 e un compromis bun între viteză și resurse. Pentru I/O-bound tasks (rețea), threading e eficient; pentru CPU-bound, folosești `ProcessPoolExecutor`.

---

### Pas 8: HTTP și Protocoale Aplicație
**📅 Corelat cu:** Săptămânile 8-12

#### 💡 Analogie: HTTP ca Conversație la Bancă

| Element HTTP | Echivalent Bancă |
|--------------|------------------|
| **Request** | Completezi un formular de cerere |
| **GET** | "Vreau să văd soldul" (doar citești) |
| **POST** | "Vreau să depun bani" (trimiți date) |
| **PUT** | "Vreau să actualizez adresa" (înlocuiești complet) |
| **DELETE** | "Vreau să închid contul" |
| **Headers** | Antetul formularului (nume, data, semnătura) |
| **Body** | Conținutul cererii (suma, detalii) |
| **Response 200** | "Cerere aprobată" |
| **Response 404** | "Nu găsim acest cont" |
| **Response 500** | "Sistemul nostru are probleme" |

#### HTTP de la Zero

```python
import socket

def http_get(host: str, path: str, port: int = 80) -> str:
    """Execută un GET HTTP manual."""
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
    
    return response.decode('utf-8', errors='replace')
```

---

### Pas 9: Practici și Debugging
**📅 Corelat cu:** Săptămâna 14 (`14roWSL`)

#### 💡 Analogie: Debugging ca Detectiv

| Tehnică Debug | Echivalent Detectiv |
|---------------|---------------------|
| **print()** | Lași notițe în locuri cheie |
| **logging** | Cameră de filmat care înregistrează tot |
| **breakpoint()** | Oprești timpul și examinezi scena |
| **Stack trace** | Cronologia evenimentelor |
| **Unit tests** | Verifici alibiul fiecărui suspect |

#### Logging vs Print

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# În loc de print(), folosește:
logger.debug("Detalii pentru debugging")
logger.info("Informații generale")
logger.warning("Ceva suspect")
logger.error("Problemă!")
```

#### Debugger Integrat

```python
def functie_complexa(data):
    rezultat = proceseaza(data)
    breakpoint()  # Oprește aici — poți inspecta 'rezultat'
    return rezultat
```

---

## Verificare Înțelegere (Peer Instruction)

### 🗳️ PI #1: Bytes vs Strings

**Scenariu:**
```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8080))
s.send("Hello")
```

**Întrebare:** Ce se întâmplă când rulezi acest cod?

**Opțiuni:**
- A) Mesajul "Hello" este trimis cu succes
- B) `TypeError: a bytes-like object is required, not 'str'`
- C) Mesajul este trimis dar corupt
- D) Socket-ul se blochează în așteptare

<details>
<summary>🔑 Răspuns și Explicație</summary>

**Corect: B**

Socket-urile Python 3 acceptă DOAR bytes, nu strings.

**De ce nu A:** Python 3 a separat strict bytes de str  
**De ce nu C:** Nu se trimite nimic, eroarea apare înainte  
**De ce nu D:** Eroarea e imediată, nu blocaj

**Cod corect:** `s.send(b"Hello")` sau `s.send("Hello".encode())`

</details>

---

### 🗳️ PI #2: Port Binding

**Scenariu:**
- Terminal 1: `python server.py` (ascultă pe 8080)
- Terminal 2: `python server.py` (același script)

**Întrebare:** Ce se întâmplă în Terminal 2?

**Opțiuni:**
- A) Al doilea server pornește și ambele funcționează
- B) `OSError: Address already in use`
- C) Al doilea server îl înlocuiește pe primul
- D) Sistemul alege automat alt port (8081)

<details>
<summary>🔑 Răspuns și Explicație</summary>

**Corect: B**

Un port poate avea UN SINGUR listener la un moment dat.

**De ce nu A:** Două procese nu pot asculta pe același port  
**De ce nu C:** OS-ul protejează porturile ocupate  
**De ce nu D:** Nu există auto-alocare (cu excepția portului 0)

**Soluție:** `SO_REUSEADDR` pentru restart rapid, sau port diferit.

</details>

---

### 🗳️ PI #3: struct.unpack

**Scenariu:**
```python
import struct
data = b'\x00\x50'
port, = struct.unpack('!H', data)
print(port)
```

**Întrebare:** Ce afișează?

**Opțiuni:**
- A) 80
- B) 20480
- C) `b'\x00\x50'`
- D) `(80,)`

<details>
<summary>🔑 Răspuns și Explicație</summary>

**Corect: A**

`!H` = network byte order (big-endian), unsigned short (2 bytes)
`0x0050` în big-endian = 80 în decimal

**De ce nu B:** Ar fi 20480 dacă era little-endian (`<H`)  
**De ce nu C:** `unpack` returnează numere, nu bytes  
**De ce nu D:** Virgula după `port` extrage valoarea din tuplu

</details>

---

### 🗳️ PI #4: Docker Port Mapping

**Scenariu:**
```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

**Întrebare:** Ce URL folosești din Windows pentru a accesa nginx?

**Opțiuni:**
- A) `http://localhost:80`
- B) `http://localhost:8080`
- C) `http://172.17.0.2:80`
- D) `http://nginx:80`

<details>
<summary>🔑 Răspuns și Explicație</summary>

**Corect: B**

`8080:80` = portul 8080 de pe host se mapează la portul 80 din container.

**De ce nu A:** 80 e portul din container, nu de pe host  
**De ce nu C:** IP-ul intern Docker nu e accesibil direct din Windows  
**De ce nu D:** Numele serviciului se rezolvă doar în rețeaua Docker

</details>

---

### 🗳️ PI #5: Context Managers

**Scenariu:**
```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('google.com', 80))
sock.send(b'GET / HTTP/1.0\r\n\r\n')
raise Exception("Eroare!")
sock.close()
```

**Întrebare:** Ce se întâmplă cu socket-ul?

**Opțiuni:**
- A) Se închide normal înainte de excepție
- B) Rămâne deschis (resource leak)
- C) Python îl închide automat
- D) OS-ul îl închide imediat

<details>
<summary>🔑 Răspuns și Explicație</summary>

**Corect: B**

`sock.close()` nu se execută niciodată din cauza excepției.

**De ce nu A:** Excepția apare înainte de close()  
**De ce nu C:** Python nu are garbage collection pentru sockets  
**De ce nu D:** OS-ul îl închide eventual, dar nu imediat

**Soluție:** Folosește `with socket.socket(...) as sock:`

</details>

---

## Exerciții de Explorare pe Săptămâni

### Săptămâna 1-2: Fundamentele

| Fișier | Ce să explorezi | Concept Python |
|--------|-----------------|----------------|
| `ex_1_01_latenta_ping.py` | `@dataclass`, `subprocess.run()` | Dataclasses, subprocese |
| `ex_1_02_tcp_server_client.py` | `socket`, `threading` | Sockets de bază |
| `ex_1_03_parsare_csv.py` | `csv` module, comprehensions | Procesare date |

### Săptămâna 2-3: Sockets

| Fișier | Ce să explorezi | Concept Python |
|--------|-----------------|----------------|
| `ex_2_01_tcp.py` | `SOCK_STREAM`, `accept()` | TCP sockets |
| `ex_2_02_udp.py` | `SOCK_DGRAM`, `sendto()` | UDP sockets |
| `ex_3_01_udp_broadcast.py` | `SO_BROADCAST` | Socket options |

### Săptămâna 4-14: Avansate

Consultă tabelul complet din secțiunea [Structura Repository-ului](#structura-repository-ului).

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

# Extragere
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
*Versiune: 2.0 — Ianuarie 2025 (cu îmbunătățiri pedagogice CPA și PI)*
