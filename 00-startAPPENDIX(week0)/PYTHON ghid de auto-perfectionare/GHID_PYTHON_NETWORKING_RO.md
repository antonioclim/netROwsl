# 🐍 Python pentru Rețele de Calculatoare
## Ghid Elaborat de Auto-Studiu

> **Material complementar** pentru cursul de Rețele de Calculatoare  
> **Repository:** [github.com/antonioclim/netROwsl](https://github.com/antonioclim/netROwsl)  
> **Status:** Opțional, fără evaluare  
> **Mediu:** WSL2 + Ubuntu 22.04 + Docker + Portainer  
> **Versiune:** 3.0 — Ianuarie 2025 (cu îmbunătățiri pedagogice CPA, PI și CREATE)

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
4. [Exerciții CREATE — Proiectare Independentă](#exerciții-create--proiectare-independentă)
5. [Verificare Înțelegere (Peer Instruction)](#verificare-înțelegere-peer-instruction)
6. [Exercițiu în Perechi (Pair Programming)](#exercițiu-în-perechi-pair-programming)
7. [Exerciții Parsons (Rearanjare Cod)](#exerciții-parsons-rearanjare-cod)
8. [Exerciții Code Tracing](#exerciții-code-tracing-urmărire-execuție)
9. [Exercițiu EVALUATE: Alege Arhitectura](#exercițiu-evaluate-alege-arhitectura)
10. [Diagrame de Referință](#diagrame-de-referință)
11. [Exerciții de Explorare pe Săptămâni](#exerciții-de-explorare-pe-săptămâni)
12. [Referință Rapidă Python-Networking](#referință-rapidă-python-networking)
13. [FAQ Extins](#faq-extins)
14. [Resurse Suplimentare](#resurse-suplimentare)
15. [Checklist de Auto-Evaluare](#-checklist-de-auto-evaluare)

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

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_ȘI_ANALOGIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 🎯 OBIECTIVE_ȘI_REFERINȚE
#### ═══════════════════════════════════════════════════════════════

#### De Ce Contează

Înainte de a modifica scripturile din laborator, trebuie să le poți citi și înțelege. Exercițiile încep cu cod funcțional pe care îl vei adapta.

#### Fișiere de Referință

Deschide și studiază structura acestor fișiere:
- `01roWSL/src/exercises/ex_1_01_latenta_ping.py`
- `01roWSL/src/exercises/ex_1_02_tcp_server_client.py`

#### ═══════════════════════════════════════════════════════════════
#### 📖 CONCEPTE_CHEIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 🔍 EXPLICAȚII_DETALIATE
#### ═══════════════════════════════════════════════════════════════

#### 🔍 De Ce Funcționează Așa?

**Întrebare:** De ce Python nu are `{` și `}` ca C sau Java?

**Explicație:** Python folosește **indentarea** (spații sau tab-uri) pentru a defini blocurile de cod. Asta forțează codul să fie citibil — nu poți scrie totul pe o linie. E o decizie de design a limbajului.

**Consecință practică:** Dacă amesteci tab-uri cu spații, vei primi `IndentationError`. Configurează editorul să folosească 4 spații.

#### ═══════════════════════════════════════════════════════════════
#### 🔮 PREDICȚIE_ȘI_PRACTICĂ
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_ȘI_ANALOGIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📖 CONCEPTE_CHEIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 🔮 PREDICȚIE_ȘI_PRACTICĂ
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_ȘI_ANALOGIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📖 CONCEPTE_CHEIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 🔮 PREDICȚIE_ȘI_PRACTICĂ
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_ȘI_ANALOGIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📖 CONCEPTE_CHEIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_ȘI_ANALOGIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📖 CONCEPTE_CHEIE
#### ═══════════════════════════════════════════════════════════════

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

Folosire:
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

- usage: linia de folosire
- description: descrierea programului
- positional arguments: argumente obligatorii
- options: argumente opționale cu explicații

</details>

---

### Pas 6: Analiza Pachetelor

**📅 Corelat cu:** Săptămânile 6-7 (`06roWSL`, `07roWSL`)

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_ȘI_ANALOGIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📖 CONCEPTE_CHEIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_ȘI_ANALOGIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📖 CONCEPTE_CHEIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_ȘI_ANALOGIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📖 CONCEPTE_CHEIE
#### ═══════════════════════════════════════════════════════════════

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

#### ═══════════════════════════════════════════════════════════════
#### 📋 CONTEXT_ȘI_ANALOGIE
#### ═══════════════════════════════════════════════════════════════

#### 💡 Analogie: Debugging ca Detectiv

| Tehnică Debug | Echivalent Detectiv |
|---------------|---------------------|
| **print()** | Lași notițe în locuri cheie |
| **logging** | Cameră de filmat care înregistrează tot |
| **breakpoint()** | Oprești timpul și examinezi scena |
| **Stack trace** | Cronologia evenimentelor |
| **Unit tests** | Verifici alibiul fiecărui suspect |

#### ═══════════════════════════════════════════════════════════════
#### 📖 CONCEPTE_CHEIE
#### ═══════════════════════════════════════════════════════════════

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

## Exerciții CREATE — Proiectare Independentă

Aceste exerciții îți cer să **proiectezi** și **construiești** soluții de la zero, nu doar să completezi cod existent.

### 🛠️ CREATE #1: Proiectează un Protocol de Chat

**Nivel Bloom:** CREATE  
**Timp estimat:** 45-60 minute  
**Mod:** Individual sau în perechi

#### Sarcină

Proiectează și implementează un protocol binar simplu pentru un sistem de mesagerie.

#### Specificații Protocol

| Câmp | Dimensiune | Descriere |
|------|:----------:|-----------|
| Versiune | 1 byte | Versiunea protocolului (0x01) |
| Tip mesaj | 1 byte | 0x01=text, 0x02=imagine, 0x03=status |
| Lungime | 2 bytes | Lungimea payload-ului (big-endian) |
| Timestamp | 4 bytes | Unix timestamp (secunde) |
| Payload | variabil | Conținutul mesajului |

#### Diagrama Protocolului

```
┌─────────┬──────────┬──────────┬────────────┬─────────────────┐
│ Version │ Msg Type │  Length  │ Timestamp  │    Payload      │
│ (1B)    │  (1B)    │  (2B)    │   (4B)     │  (0-65535 B)    │
└─────────┴──────────┴──────────┴────────────┴─────────────────┘
```

#### Livrabile

**1. Cod Python — completează funcțiile:**

```python
import struct
import time

def pack_message(msg_type: int, payload: bytes) -> bytes:
    """Împachetează un mesaj conform protocolului.
    
    Args:
        msg_type: Tipul mesajului (1=text, 2=imagine, 3=status)
        payload: Conținutul mesajului ca bytes
        
    Returns:
        Mesajul complet împachetat (header + payload)
    """
    # TODO: Implementează cu struct.pack
    # Hint: formatul e '!BBHI' + payload
    pass

def unpack_message(data: bytes) -> tuple[int, int, int, bytes]:
    """Despachează un mesaj și extrage câmpurile.
    
    Args:
        data: Mesajul complet (header + payload)
        
    Returns:
        Tuplu: (version, msg_type, timestamp, payload)
        
    Raises:
        ValueError: Dacă header-ul e invalid sau date insuficiente
    """
    # TODO: Implementează cu struct.unpack
    pass
```

**2. Teste — minim 3:**

```python
def test_roundtrip():
    """Verifică pack → unpack returnează datele originale."""
    original = b"Salut!"
    packed = pack_message(0x01, original)
    version, msg_type, timestamp, payload = unpack_message(packed)
    assert payload == original
    assert msg_type == 0x01

def test_empty_payload():
    """Verifică că funcționează cu payload gol."""
    # TODO

def test_max_payload():
    """Verifică payload de dimensiune maximă (65535 bytes)."""
    # TODO
```

#### Criterii de Evaluare

- [ ] Header-ul are exact 8 bytes
- [ ] Câmpurile sunt în network byte order (big-endian)
- [ ] Funcționează pentru payload gol
- [ ] Funcționează pentru payload maxim (65535 bytes)
- [ ] Timestamp-ul e valid (nu 0)
- [ ] Codul are docstrings complete
- [ ] Minim 3 teste unitare

---

### 🛠️ CREATE #2: Proiectează un Port Scanner

**Nivel Bloom:** CREATE  
**Timp estimat:** 30-45 minute

#### Sarcină

Proiectează un port scanner cu următoarele cerințe:

**Funcționalități obligatorii:**
1. Scanează un range de porturi (ex: 1-1000)
2. Detectează porturi deschise (TCP connect)
3. Timeout configurabil per port
4. Output în format JSON

**Bonus:**
- Paralelizare cu ThreadPoolExecutor
- Detectare serviciu (HTTP, SSH, FTP)

#### Schelet de Pornire

```python
#!/usr/bin/env python3
"""
Port Scanner - Exercițiu CREATE
Proiectează și implementează un scanner de porturi TCP.
"""
import socket
import json
import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict

@dataclass
class ScanResult:
    """Rezultatul scanării unui port."""
    port: int
    status: str  # "open", "closed", "filtered"
    service: str = ""  # opțional: "http", "ssh", etc.

def scan_port(host: str, port: int, timeout: float = 1.0) -> ScanResult:
    """Scanează un singur port.
    
    TODO: Implementează logica de scanare TCP connect.
    """
    pass

def scan_range(host: str, start: int, end: int, 
               workers: int = 10, timeout: float = 1.0) -> list[ScanResult]:
    """Scanează un range de porturi în paralel.
    
    TODO: Folosește ThreadPoolExecutor pentru paralelizare.
    """
    pass

def main():
    # TODO: Implementează CLI cu argparse
    # Exemplu: python scanner.py 192.168.1.1 --ports 1-100 --timeout 0.5
    pass

if __name__ == "__main__":
    main()
```

---

### 🛠️ CREATE #3: Proiectează un Load Balancer Simplu

**Nivel Bloom:** CREATE  
**Timp estimat:** 60-90 minute

#### Sarcină

Proiectează un load balancer TCP care distribuie conexiunile către multiple backend-uri.

**Algoritmi de implementat (alege unul):**
1. **Round Robin** — ciclează prin backend-uri
2. **Random** — alege aleator
3. **Least Connections** — alege backend-ul cu cele mai puține conexiuni

#### Arhitectură

```
                    ┌─────────────────┐
                    │  LOAD BALANCER  │
   Client ─────────►│   (port 8080)   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   ┌──────────┐        ┌──────────┐        ┌──────────┐
   │ Backend1 │        │ Backend2 │        │ Backend3 │
   │ :8081    │        │ :8082    │        │ :8083    │
   └──────────┘        └──────────┘        └──────────┘
```

#### Livrabile

Fișier `load_balancer.py` funcțional cu:
- Configurare backend-uri din command line
- Logging al distribuției conexiunilor
- Health check periodic (opțional)

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

### 🗳️ PI #6: Căi Fișiere WSL

**Scenariu:**
```bash
# Creezi un fișier în Ubuntu WSL:
echo "test" > /home/stud/date.txt

# Apoi vrei să-l deschizi din Windows.
```

**Întrebare:** Care e calea corectă în Windows Explorer?

**Opțiuni:**
- A) `C:\home\stud\date.txt`
- B) `\\wsl$\Ubuntu\home\stud\date.txt`
- C) `D:\WSL\Ubuntu\home\stud\date.txt`
- D) Nu poți accesa fișiere WSL din Windows

<details>
<summary>🔑 Răspuns și Explicație</summary>

**Corect: B**

Sistemul de fișiere WSL e accesibil din Windows prin calea de rețea `\\wsl$\<distro>\`.

**De ce nu A:** WSL nu montează `/home` pe C:\  
**De ce nu C:** Nu există folder D:\WSL\ implicit  
**De ce nu D:** Windows 10/11 poate accesa fișierele WSL nativ

**Atenție:** Editarea fișierelor WSL cu aplicații Windows poate cauza probleme de permisiuni. Folosește VS Code cu extensia Remote - WSL.

</details>

---

### 🗳️ PI #7: recv() Buffering

**Scenariu:**
```python
# Server trimite:
conn.sendall(b"HELLO WORLD FROM SERVER!")  # 24 bytes

# Client primește:
data = sock.recv(10)
print(data)
```

**Întrebare:** Ce afișează clientul?

**Opțiuni:**
- A) `b'HELLO WORLD FROM SERVER!'`
- B) `b'HELLO WORL'`
- C) Eroare — buffer prea mic
- D) Nimic — recv() așteaptă 24 bytes

<details>
<summary>🔑 Răspuns și Explicație</summary>

**Corect: B**

`recv(10)` returnează **maxim** 10 bytes, nu exact 10 și nu tot mesajul.

**De ce nu A:** recv() nu așteaptă tot mesajul  
**De ce nu C:** Buffer-ul e doar limita superioară, nu cerință  
**De ce nu D:** recv() returnează ce e disponibil, nu așteaptă mai mult

**Implicație:** Pentru mesaje mai lungi, trebuie să apelezi recv() în buclă sau să folosești un protocol cu length prefix.

</details>

---

### 🗳️ PI #8: bind() Address

**Scenariu:**
```python
server.bind(('0.0.0.0', 8080))
# vs
server.bind(('127.0.0.1', 8080))
```

**Întrebare:** Care e diferența practică?

**Opțiuni:**
- A) Nicio diferență, ambele funcționează la fel
- B) 0.0.0.0 acceptă conexiuni doar locale, 127.0.0.1 de oriunde
- C) 0.0.0.0 acceptă conexiuni de oriunde, 127.0.0.1 doar locale
- D) 127.0.0.1 e mai rapid pentru conexiuni locale

<details>
<summary>🔑 Răspuns și Explicație</summary>

**Corect: C**

- `0.0.0.0` = ascultă pe **toate** interfețele (localhost, LAN, WAN)
- `127.0.0.1` = ascultă **doar** pe loopback (local)

**De ce nu A:** Diferența e semnificativă pentru securitate  
**De ce nu B:** E invers  
**De ce nu D:** Performanța e identică pentru conexiuni locale

**Regulă de securitate:** În producție, bind pe IP-ul specific al interfeței dorite. 0.0.0.0 expune serverul la toată rețeaua!

</details>

---

### 🗳️ PI #9: Docker Network Default

**Scenariu:**
```yaml
# docker-compose.yml
services:
  web:
    image: nginx
  api:
    image: python:3.11
```

**Întrebare:** Poate containerul `web` să acceseze `api` folosind numele `api`?

**Opțiuni:**
- A) Da, Docker Compose creează automat o rețea comună
- B) Nu, trebuie să definești explicit o rețea în compose
- C) Da, dar doar dacă adaugi `links: [api]`
- D) Nu, containerele nu pot comunica niciodată prin nume

<details>
<summary>🔑 Răspuns și Explicație</summary>

**Corect: A**

Docker Compose v2+ creează automat o rețea `<project>_default` și containerele se pot accesa prin numele serviciului.

**De ce nu B:** Rețeaua implicită e suficientă pentru compose  
**De ce nu C:** `links` e deprecated în Compose v2+  
**De ce nu D:** DNS-ul Docker rezolvă numele serviciilor

**Testare:**
```bash
docker exec web ping api  # funcționează!
```

</details>

---

### 🗳️ PI #10: SO_REUSEADDR Timing

**Scenariu:**
```python
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # ← aici
server.listen(5)
```

**Întrebare:** Funcționează codul de mai sus?

**Opțiuni:**
- A) Da, ordinea nu contează
- B) Nu, setsockopt trebuie apelat înainte de bind
- C) Nu, setsockopt trebuie apelat după listen
- D) Depinde de sistemul de operare

<details>
<summary>🔑 Răspuns și Explicație</summary>

**Corect: B**

`SO_REUSEADDR` trebuie setat **înainte** de `bind()` pentru a avea efect.

**Ordine corectă:**
```python
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(5)
```

**De ce contează:** Opțiunea afectează cum bind() gestionează porturile în TIME_WAIT.

</details>

---

## Exercițiu în Perechi (Pair Programming)

### 👥 Debug Mystery Server

**Durată:** 20-25 minute  
**Mod:** Perechi (Driver + Navigator)

#### Roluri

| Rol | Responsabilități |
|-----|------------------|
| **Driver** | Scrie codul, execută comenzile, partajează ecranul |
| **Navigator** | Verifică logica, sugerează direcții, caută în documentație |

**Regulă principală:** Navigator-ul NU atinge tastatura. Comunicarea e cheia!

#### Sarcină

Serverul TCP de mai jos are **3 bug-uri ascunse**. Găsiți-le și reparați-le împreună.

```python
#!/usr/bin/env python3
"""Mystery Server — găsește cele 3 bug-uri!"""
import socket

def server(port=8080):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', port))  # Bug #1: ???
    s.listen()
    print(f"Server pe {port}")
    
    while True:
        conn, addr = s.accept()
        print(f"Client: {addr}")
        
        data = conn.recv(1024)
        response = "Echo: " + data  # Bug #2: ???
        conn.send(response)  # Bug #3: ???
        conn.close()

if __name__ == "__main__":
    server()
```

#### Indicii (dezvăluie pe rând)

<details>
<summary>💡 Indiciu #1 (după 5 minute)</summary>

Bug #1: Ce se întâmplă dacă oprești și repornești serverul rapid?
</details>

<details>
<summary>💡 Indiciu #2 (după 10 minute)</summary>

Bug #2: Ce tip de date returnează `conn.recv()`? Ce tip acceptă operatorul `+` cu string?
</details>

<details>
<summary>💡 Indiciu #3 (după 15 minute)</summary>

Bug #3: `send()` vs `sendall()` — care garantează trimiterea completă?
</details>

#### Soluție

<details>
<summary>🔑 Soluție completă</summary>

```python
#!/usr/bin/env python3
"""Mystery Server — REPARAT"""
import socket

def server(port=8080):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # FIX #1: Adaugă SO_REUSEADDR pentru restart rapid
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    s.bind(('0.0.0.0', port))  # 0.0.0.0 pentru acces din rețea
    s.listen(5)
    print(f"Server pe {port}")
    
    while True:
        conn, addr = s.accept()
        print(f"Client: {addr}")
        
        data = conn.recv(1024)
        
        # FIX #2: Decode bytes înainte de concatenare cu string
        response = "Echo: " + data.decode('utf-8')
        
        # FIX #3: sendall() + encode() pentru trimitere completă
        conn.sendall(response.encode('utf-8'))
        
        conn.close()

if __name__ == "__main__":
    server()
```

</details>

#### Debrief

După exercițiu, discutați:
1. Care bug a fost cel mai greu de găsit? De ce?
2. Cum a ajutat colaborarea la debugging?
3. Ce strategii de debugging ați aplicat?

---

## Exerciții Parsons (Rearanjare Cod)

Exercițiile Parsons te ajută să înțelegi **logica și ordinea operațiilor** fără să scrii cod de la zero. Rearanjează blocurile în ordinea corectă.

### 🧩 PARSONS #1: Server TCP Minimal

Rearanjează blocurile pentru a crea un server TCP funcțional:

```
# BLOCURI (în ordine amestecată):

conn.sendall(b"Hello!")
server.listen(5)
server.bind(('0.0.0.0', 8080))
import socket
conn, addr = server.accept()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.close()
```

<details>
<summary>🔑 Soluție</summary>

```python
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.listen(5)
conn, addr = server.accept()
conn.sendall(b"Hello!")
conn.close()
```

**Pattern memorabil:** SOCKET → BIND → LISTEN → ACCEPT → COMMUNICATE → CLOSE

</details>

---

### 🧩 PARSONS #2: Client TCP

Rearanjează pentru client TCP:

```
# BLOCURI (în ordine amestecată):

response = client.recv(1024)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.close()
import socket
client.connect(('127.0.0.1', 8080))
client.sendall(b"Hello server!")
```

<details>
<summary>🔑 Soluție</summary>

```python
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))
client.sendall(b"Hello server!")
response = client.recv(1024)
client.close()
```

**Pattern memorabil:** SOCKET → CONNECT → SEND → RECEIVE → CLOSE

</details>

---

### 🧩 PARSONS #3: Struct Pack/Unpack

Rearanjează pentru a crea și parsa un header de 4 bytes:

```
# BLOCURI (în ordine amestecată):

port, flags = struct.unpack('!HH', header)
import struct
header = struct.pack('!HH', port, flags)
port = 8080
print(f"Port: {port}, Flags: {flags}")
flags = 0x0001
```

<details>
<summary>🔑 Soluție</summary>

```python
import struct
port = 8080
flags = 0x0001
header = struct.pack('!HH', port, flags)
port, flags = struct.unpack('!HH', header)
print(f"Port: {port}, Flags: {flags}")
```

**Concept cheie:** Variabilele trebuie definite înainte de pack(), iar unpack() suprascrie valorile.

</details>

---

## Exerciții Code Tracing (Urmărire Execuție)

Urmărirea manuală a codului îți dezvoltă **modelul mental** al execuției — esențial pentru debugging.

### 🔍 TRACE #1: Transformare Bytes

```python
data = b"HELLO"
result = []
for i, byte in enumerate(data):
    if i % 2 == 0:
        result.append(chr(byte).lower())
    else:
        result.append(chr(byte))
print("".join(result))
```

**🔮 PREDICȚIE:** Ce va afișa? Completează tabelul pas cu pas:

| i | byte (decimal) | chr(byte) | i % 2 == 0? | result (după acest pas) |
|---|----------------|-----------|-------------|-------------------------|
| 0 | 72 | 'H' | Da | ['h'] |
| 1 | ? | ? | ? | ? |
| 2 | ? | ? | ? | ? |
| 3 | ? | ? | ? | ? |
| 4 | ? | ? | ? | ? |

<details>
<summary>🔑 Soluție completă</summary>

| i | byte | chr(byte) | i % 2 == 0? | result |
|---|------|-----------|-------------|--------|
| 0 | 72 | 'H' | Da | ['h'] |
| 1 | 69 | 'E' | Nu | ['h', 'E'] |
| 2 | 76 | 'L' | Da | ['h', 'E', 'l'] |
| 3 | 76 | 'L' | Nu | ['h', 'E', 'l', 'L'] |
| 4 | 79 | 'O' | Da | ['h', 'E', 'l', 'L', 'o'] |

**Output:** `hElLo`

**De reținut:** `b"HELLO"` conține codurile ASCII: H=72, E=69, L=76, L=76, O=79

</details>

---

### 🔍 TRACE #2: Network Byte Order

```python
import struct
value = 0x1234
packed = struct.pack('!H', value)  # Network order (big-endian)
print(f"Bytes: {packed.hex()}")
print(f"Byte 0: {packed[0]:02x}")
print(f"Byte 1: {packed[1]:02x}")
```

**🔮 PREDICȚIE (scrie ÎNAINTE de a rula):**
- `packed.hex()` = ____________
- `packed[0]` (hex) = ____________
- `packed[1]` (hex) = ____________

<details>
<summary>🔑 Răspuns</summary>

- `packed.hex()` = `"1234"`
- `packed[0]` = `0x12` (18 în decimal) — **MSB first** (big-endian)
- `packed[1]` = `0x34` (52 în decimal)

**Concept cheie:** Network byte order = Big-endian = Most Significant Byte FIRST

Dacă ai fi folosit little-endian (`'<H'`), ordinea ar fi fost inversată: `0x34`, `0x12`.

</details>

---

### 🔍 TRACE #3: Socket Accept Loop

```python
connections = 0
while connections < 3:
    conn, addr = server.accept()  # Presupunem că vin 3 clienți
    print(f"Client #{connections}: {addr[1]}")
    connections += 1
    conn.close()
print(f"Total: {connections}")
```

**🔮 PREDICȚIE:** Dacă vin 3 clienți de pe porturile 50001, 50002, 50003, ce afișează?

<details>
<summary>🔑 Răspuns</summary>

```
Client #0: 50001
Client #1: 50002
Client #2: 50003
Total: 3
```

**Atenție la off-by-one:** Primul client e `#0`, nu `#1`. Dacă vrei numerotare de la 1, folosește `connections + 1` în print.

</details>

---

## Exercițiu EVALUATE: Alege Arhitectura

### 🎯 EVALUATE: Sistem de Logging Centralizat

**Scenariu:** Construiești un sistem de logging pentru 50 de containere Docker într-un cluster.

**Opțiuni arhitecturale:**

| Opțiune | Descriere | Pro | Contra |
|---------|-----------|-----|--------|
| **A** | Fiecare container scrie în fișier local | Simplu, fără dependențe | Fragmentat, greu de agregat |
| **B** | Toate trimit UDP la server central | Rapid, non-blocant | Posibilă pierdere mesaje |
| **C** | Toate trimit TCP la server central | Livrare garantată | Poate bloca dacă serverul e lent |
| **D** | Message broker (Redis/Kafka) | Decuplat, scalabil, persistent | Complexitate adăugată |

**Sarcini:**

1. **Context dezvoltare** (5 containere, 1 dezvoltator): Care opțiune alegi și de ce?

2. **Context producție** (50 containere, 1000 req/s): Care opțiune și de ce?

3. **Context IoT** (100 dispozitive pe rețea instabilă): Care opțiune și de ce?

<details>
<summary>🔑 Analiză</summary>

**Dezvoltare:** Opțiunea **A** sau **B** — simplitatea primează, pierderea unor log-uri nu e critică.

**Producție:** Opțiunea **D** — decuplarea și persistența sunt esențiale la scală. TCP (C) ar crea bottleneck.

**IoT:** Opțiunea **B** (UDP) cu retry logic local — rețeaua instabilă face TCP problematic (reconectări constante).

**Lecție cheie:** Nu există soluție "corect universal" — depinde de context, scale și toleranță la pierderi.

</details>

---

## Diagrame de Referință

### Diagrama: TCP Three-Way Handshake

```
     CLIENT                                 SERVER
        │                                      │
        │ ────────── SYN (seq=100) ─────────► │
        │        "Vreau să mă conectez"        │
        │                                      │
        │ ◄──── SYN-ACK (seq=300,ack=101) ─── │
        │     "OK, te-am auzit, ești acolo?"   │
        │                                      │
        │ ────────── ACK (ack=301) ──────────► │
        │            "Da, sunt aici"           │
        │                                      │
        │         ═══ CONEXIUNE ═══            │
        │         ═══ STABILITĂ ═══            │
        ▼                                      ▼
```

---

### Diagrama: Docker Port Mapping

```
┌─────────────────────────────────────────────────────────────────────┐
│ WINDOWS HOST                                                        │
│                                                                     │
│   Browser ──► http://localhost:8080                                 │
│                        │                                            │
│   ┌────────────────────┼────────────────────────────────────────┐   │
│   │ WSL2 (Ubuntu)      │                                        │   │
│   │                    │                                        │   │
│   │   ┌────────────────▼────────────────────────────────────┐   │   │
│   │   │ Docker Engine                                       │   │   │
│   │   │                                                     │   │   │
│   │   │   ports: "8080:80"                                  │   │   │
│   │   │      ▲         │                                    │   │   │
│   │   │      │         ▼                                    │   │   │
│   │   │   ┌──┴──────────────────────────────┐               │   │   │
│   │   │   │ Container: nginx                │               │   │   │
│   │   │   │                                 │               │   │   │
│   │   │   │   nginx ascultă pe port 80 ◄───┘               │   │   │
│   │   │   │   (intern, nu expus direct)                    │   │   │
│   │   │   └─────────────────────────────────┘               │   │   │
│   │   └─────────────────────────────────────────────────────┘   │   │
│   └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘

LEGENDĂ: 8080 = port HOST (Windows vede asta)
         80   = port CONTAINER (nginx vede asta)
```

---

### Diagrama: Socket Lifecycle (Server TCP)

```
          socket()
             │
             ▼
    ┌─────────────────┐
    │  SOCKET CREAT   │
    │  (file descriptor)
    └────────┬────────┘
             │
         bind(addr, port)
             │
             ▼
    ┌─────────────────┐
    │  SOCKET LEGAT   │
    │  la adresă:port │
    └────────┬────────┘
             │
         listen(backlog)
             │
             ▼
    ┌─────────────────┐
    │  ASCULTĂ        │◄──────────────┐
    │  (waiting)      │               │
    └────────┬────────┘               │
             │                        │
         accept() ◄─── client se conectează
             │                        │
             ▼                        │
    ┌─────────────────┐               │
    │  CONEXIUNE      │               │
    │  conn, addr     │               │
    └────────┬────────┘               │
             │                        │
       recv() / send()                │
             │                        │
         close(conn) ─────────────────┘
             │
    (serverul continuă să asculte)
```

---

### Diagrama: bytes ↔ str Conversion

```
    ┌─────────────────┐                    ┌─────────────────┐
    │      str        │                    │     bytes       │
    │  "Salut! 👋"    │                    │  b'Salut! \xf0' │
    │                 │                    │   \x9f\x91\x8b' │
    │  (text uman)    │                    │  (date binare)  │
    └────────┬────────┘                    └────────┬────────┘
             │                                      │
             │                                      │
             │ ───── .encode('utf-8') ────────────► │
             │                                      │
             │ ◄──── .decode('utf-8') ───────────── │
             │                                      │
             ▼                                      ▼
    
    PYTHON                                    REȚEA
    (procesare text)                     (transmisie date)
    
    
    ⚠️  REGULĂ: socket.send() acceptă DOAR bytes, NU str!
    
    Greșit:  sock.send("Hello")        → TypeError!
    Corect:  sock.send(b"Hello")       → OK
    Corect:  sock.send("Hello".encode()) → OK
```

---

### Diagrama: struct.pack / struct.unpack

```
                    struct.pack('!HH', 8080, 443)
                                │
    ┌───────────────────────────┴───────────────────────────┐
    │                                                       │
    │  8080 (decimal) ──► 0x1F90 ──► bytes: \x1f\x90       │
    │   443 (decimal) ──► 0x01BB ──► bytes: \x01\xbb       │
    │                                                       │
    │  Rezultat: b'\x1f\x90\x01\xbb' (4 bytes)             │
    │                                                       │
    └───────────────────────────────────────────────────────┘
    
    
                    struct.unpack('!HH', data)
                                │
    ┌───────────────────────────┴───────────────────────────┐
    │                                                       │
    │  data = b'\x1f\x90\x01\xbb'                           │
    │                                                       │
    │  \x1f\x90 ──► 0x1F90 ──► 8080 (decimal)              │
    │  \x01\xbb ──► 0x01BB ──►  443 (decimal)              │
    │                                                       │
    │  Rezultat: (8080, 443) ← tuplu Python                │
    │                                                       │
    └───────────────────────────────────────────────────────┘
    
    FORMAT CODES:
    ┌────┬───────────────────┬───────────┐
    │ !  │ network byte order│ big-endian│
    │ H  │ unsigned short    │ 2 bytes   │
    │ I  │ unsigned int      │ 4 bytes   │
    │ B  │ unsigned char     │ 1 byte    │
    │ 4s │ char array        │ 4 bytes   │
    └────┴───────────────────┴───────────┘
```

---

### Diagrama: OSI vs TCP/IP

```
┌─────────────────────────────────────────────────────────────────────┐
│                    OSI MODEL vs TCP/IP MODEL                        │
├─────────────────────────────────┬───────────────────────────────────┤
│          OSI (7 layers)         │        TCP/IP (4 layers)          │
├─────────────────────────────────┼───────────────────────────────────┤
│  7. Application    ─┐           │                                   │
│  6. Presentation   ─┼──────────►│  4. Application (HTTP, DNS, SSH)  │
│  5. Session        ─┘           │                                   │
├─────────────────────────────────┼───────────────────────────────────┤
│  4. Transport      ────────────►│  3. Transport (TCP, UDP)          │
├─────────────────────────────────┼───────────────────────────────────┤
│  3. Network        ────────────►│  2. Internet (IP, ICMP)           │
├─────────────────────────────────┼───────────────────────────────────┤
│  2. Data Link      ─┐           │                                   │
│  1. Physical       ─┴──────────►│  1. Network Access (Ethernet)     │
└─────────────────────────────────┴───────────────────────────────────┘
```

---

### Diagrama: Client-Server Exchange

```
    ┌────────────────┐                    ┌────────────────┐
    │     CLIENT     │                    │     SERVER     │
    │   (inițiază)   │                    │   (ascultă)    │
    └───────┬────────┘                    └───────┬────────┘
            │                                     │
            │                              bind(port=8080)
            │                              listen()
            │                                     │
            │ ──────── connect() ───────────────► │ accept()
            │                                     │
            │ ──────── send("GET /") ───────────► │
            │                                     │
            │                              recv() → procesează
            │                                     │
            │ ◄─────── send("<html>...") ──────── │
            │                                     │
         recv()                                   │
            │                                     │
            │ ──────── close() ─────────────────► │ close(conn)
            │                                     │
            ▼                                     │
       [terminat]                          [așteaptă next]
```

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

## FAQ Extins

**Î: Trebuie să parcurg toți pașii în ordine?**  
R: Nu. Poți sări la pasul relevant pentru laboratorul curent. Folosește tabelul de corespondență.

**Î: Ce fac dacă nu înțeleg ceva?**  
R: Rulează codul, modifică valori, observă ce se schimbă. Experimentarea e cel mai bun profesor.

**Î: Trebuie să memorez sintaxa?**  
R: Nu. Folosește documentația și cheatsheet-ul. Programatorii profesioniști caută constant în docs.

**Î: Cum testez dacă am înțeles?**  
R: Încearcă să modifici un exercițiu existent sau să adaugi o funcționalitate nouă fără să te uiți la soluție.

**Î: Docker Desktop sau Docker Engine nativ în WSL?**  
R: Pentru acest curs, Docker Engine nativ în WSL2 e suficient și consumă mai puține resurse. Docker Desktop e opțional.

**Î: De ce primesc "Permission denied" la comenzi docker?**  
R: Adaugă userul la grupul docker:
```bash
sudo usermod -aG docker $USER
```
Apoi logout și login din nou (sau `newgrp docker`).

**Î: Cum verific că am WSL2, nu WSL1?**  
R: Rulează în PowerShell:
```powershell
wsl --list --verbose
```
Coloana VERSION trebuie să arate `2`.

**Î: Ce fac dacă Portainer nu pornește?**  
R: Verifică statusul:
```bash
docker ps -a | grep portainer
```
Dacă e stopped: `docker start portainer`. Dacă nu există, recreează-l.

**Î: Cum resetez parola Portainer dacă am uitat-o?**  
R: Șterge volume-ul de date și recreează:
```bash
docker stop portainer
docker rm portainer
docker volume rm portainer_data
# Apoi recreează containerul
```

**Î: De ce socket-ul meu "blochează" la recv()?**  
R: `recv()` e blocant implicit — așteaptă date. Soluții:
```python
sock.settimeout(5.0)  # timeout de 5 secunde
# sau
sock.setblocking(False)  # non-blocking (cu select/poll)
```

**Î: Pot rula aplicații GUI din WSL?**  
R: Da, WSL2 pe Windows 11 suportă WSLg nativ. Pe Windows 10 ai nevoie de X server (VcXsrv). Dar pentru acest curs, Wireshark rulează nativ în Windows, nu în WSL.

**Î: De ce primesc "Address already in use" când repornesc serverul?**  
R: Portul e încă în TIME_WAIT. Soluții:
1. Așteaptă ~60 secunde
2. Adaugă înainte de bind():
```python
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```
3. Folosește alt port temporar

**Î: Cum văd ce porturi sunt ocupate?**  
R: 
```bash
# În WSL:
ss -tlnp | grep 8080

# În Windows PowerShell:
netstat -ano | findstr :8080
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

## ✅ Checklist de Auto-Evaluare

Înainte de a considera acest ghid parcurs, verifică progresul tău:

### Nivel REMEMBER (Reamintire)
- [ ] Pot enumera cele 5 operații socket server în ordine (socket → bind → listen → accept → close)
- [ ] Știu diferența principală dintre TCP și UDP
- [ ] Recunosc sintaxa `struct.pack('!H', port)` și știu ce face

### Nivel UNDERSTAND (Înțelegere)
- [ ] Pot explica de ce `bytes ≠ str` în Python 3
- [ ] Înțeleg ce face `SO_REUSEADDR` și de ce e util
- [ ] Pot descrie fluxul TCP three-way handshake

### Nivel APPLY (Aplicare)
- [ ] Am rulat cu succes cel puțin 3 exemple din acest ghid
- [ ] Am completat corect cel puțin 1 exercițiu Parsons
- [ ] Am răspuns corect la >70% din întrebările Peer Instruction

### Nivel ANALYSE (Analiză)
- [ ] Am depanat cel puțin 1 problemă de rețea (port ocupat, conexiune refuzată, etc.)
- [ ] Am analizat output-ul unui `docker logs` pentru debugging
- [ ] Am completat corect cel puțin 1 exercițiu Code Tracing

### Nivel EVALUATE (Evaluare)
- [ ] Pot argumenta alegerea între TCP și UDP pentru un scenariu dat
- [ ] Am completat exercițiul EVALUATE privind arhitectura de logging

### Nivel CREATE (Creare)
- [ ] Am implementat cel puțin 1 exercițiu CREATE (protocol chat, port scanner, sau load balancer)
- [ ] Am modificat un exemplu existent pentru a adăuga funcționalitate nouă

---

### 📊 Interpretare Scor

| Bifări | Nivel | Recomandare |
|:------:|-------|-------------|
| 0-5 | Începător | Revizuiește secțiunile de bază, rulează mai multe exemple |
| 6-10 | Satisfăcător | Ești pregătit pentru laboratoarele standard |
| 11-14 | Bun | Poți aborda exerciții avansate |
| 15-17 | Foarte bun | Pregătit pentru proiecte independente |

---

*Material realizat ca suport opțional pentru cursul de Rețele de Calculatoare.*  
*Repository: [github.com/antonioclim/netROwsl](https://github.com/antonioclim/netROwsl)*  
*Versiune: 3.1 — Ianuarie 2025 (cu Parsons Problems, Code Tracing și Checklist auto-evaluare)*
