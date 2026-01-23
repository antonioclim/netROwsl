# 🚀 Python Rapid pentru C/JavaScript Programatori

## Echivalențe Sintactice

| C/JavaScript | Python | Note |
|--------------|--------|------|
| `int x = 5;` | `x = 5` | Fără declarație de tip |
| `if (x > 0) { }` | `if x > 0:` | Indentare în loc de acolade |
| `for (int i=0; i<n; i++)` | `for i in range(n):` | range() generează secvența |
| `while (cond) { }` | `while cond:` | Fără paranteze |
| `true / false` | `True / False` | Prima literă mare |
| `null` | `None` | Valoarea nulă |
| `&&` / `||` / `!` | `and` / `or` / `not` | Operatori logici în cuvinte |
| `arr.length` | `len(arr)` | Funcție globală |
| `arr.push(x)` | `arr.append(x)` | Adăugare la listă |
| `dict[key]` | `dict[key]` sau `dict.get(key)` | get() returnează None dacă nu există |

---

## Socket TCP Minimal

```python
import socket

# Server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8080))
    s.listen(5)
    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
        conn.sendall(b"OK")

# Client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 8080))
    s.sendall(b"Hello")
    response = s.recv(1024)
```

---

## bytes vs str

```python
# String → Bytes (pentru trimitere pe rețea)
text = "Hello"
octeti = text.encode('utf-8')  # b'Hello'

# Bytes → String (pentru afișare)
octeti = b"Hello"
text = octeti.decode('utf-8')  # 'Hello'

# Caractere românești
text_ro = "Ștefan"
octeti_ro = text_ro.encode('utf-8')  # mai mulți bytes decât caractere!
```

---

## struct pentru Binary Parsing

```python
import struct

# ! = network byte order (big-endian)
# H = unsigned short (2 bytes)
# I = unsigned int (4 bytes)
# B = unsigned char (1 byte)

# Pack
header = struct.pack('!HH', 8080, 443)  # src_port, dst_port

# Unpack
src_port, dst_port = struct.unpack('!HH', data[:4])

# Tabel formate
# B = 1 byte, H = 2 bytes, I = 4 bytes, Q = 8 bytes
```

---

## argparse Minimal

```python
import argparse

parser = argparse.ArgumentParser(description="Tool")
parser.add_argument("target", help="Țintă")
parser.add_argument("--port", "-p", type=int, default=80)
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()

print(f"{args.target}:{args.port}")
```

---

## ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def task(x):
    return x * 2

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(task, i): i for i in range(100)}
    for future in as_completed(futures):
        result = future.result()
```

---

## HTTP Request Manual

```python
# Request format
request = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"

# Response format
response = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello"
```

---

## 🐛 Debugging Rapid

```python
# Print debugging cu context
import sys
print(f"DEBUG [{__name__}:{sys._getframe().f_lineno}] var={var}")

# Breakpoint interactiv (Python 3.7+)
breakpoint()  # sau: import pdb; pdb.set_trace()

# Logging în loc de print
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"var={var}")

# Inspecție obiect
print(dir(obj))       # atribute și metode
print(vars(obj))      # dicționar atribute
print(type(obj))      # tipul obiectului
```

---

## ⚠️ Erori Comune și Soluții

| Eroare | Cauză | Soluție |
|--------|-------|---------|
| `TypeError: a bytes-like object is required` | Ai trimis str în loc de bytes | `data.encode()` |
| `OSError: Address already in use` | Portul e ocupat | `SO_REUSEADDR` sau alt port |
| `ConnectionRefusedError` | Server nu rulează | Pornește serverul |
| `socket.timeout` | Server nu răspunde | Verifică firewall, adresă |
| `UnicodeDecodeError` | Bytes invalide pentru encoding | `errors='replace'` |
| `BrokenPipeError` | Client deconectat în timp ce scriai | Try/except, verifică conexiunea |
| `ConnectionResetError` | Peer a închis brusc | Try/except, log și continuă |
| `struct.error: unpack requires...` | Lungime buffer greșită | Verifică len(data) |

---

## 🔧 One-Liners Utile

```python
import socket

# IP local
socket.gethostbyname(socket.gethostname())

# Verifică dacă portul e liber
socket.socket().connect_ex(('localhost', 8080)) != 0

# Bytes to hex și invers
data.hex()                      # bytes → hex string
bytes.fromhex('48454c4c4f')     # hex → bytes

# Pretty print dict/list
import json
print(json.dumps(obj, indent=2, ensure_ascii=False))

# IP string ↔ int
import ipaddress
int(ipaddress.IPv4Address('192.168.1.1'))  # → 3232235777
str(ipaddress.IPv4Address(3232235777))     # → '192.168.1.1'

# Verificare IP valid
try:
    ipaddress.ip_address('192.168.1.1')
    print("Valid")
except ValueError:
    print("Invalid")

# Port random disponibil
def get_free_port():
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]
```

---

## 📋 Context Managers Personalizate

```python
from contextlib import contextmanager

@contextmanager
def tcp_connection(host, port):
    """Context manager pentru conexiune TCP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        yield sock
    finally:
        sock.close()

# Folosire
with tcp_connection('localhost', 8080) as conn:
    conn.sendall(b"Hello")
    response = conn.recv(1024)
```

---

## 🔍 Verificare Tip Date

```python
# Verificare bytes vs str
isinstance(data, bytes)   # True pentru b"hello"
isinstance(data, str)     # True pentru "hello"

# Conversie sigură
def ensure_bytes(data):
    if isinstance(data, str):
        return data.encode('utf-8')
    return data

def ensure_str(data):
    if isinstance(data, bytes):
        return data.decode('utf-8', errors='replace')
    return data
```

---

## 📊 Logging Config Complet

```python
import logging

# Setup pentru debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
    datefmt='%H:%M:%S'
)

# Logger specific
logger = logging.getLogger(__name__)

# Folosire
logger.debug("Detalii interne")
logger.info("Informație generală")
logger.warning("Ceva suspect")
logger.error("Eroare!")
logger.exception("Eroare cu stack trace")  # în except block
```

---

## 🎯 Pattern-uri Comune

### Echo Server

```python
def echo_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            with conn:
                while data := conn.recv(1024):
                    conn.sendall(data)
```

### Length-Prefixed Protocol

```python
def send_message(sock, data: bytes):
    """Trimite mesaj cu length prefix (4 bytes)."""
    length = struct.pack('!I', len(data))
    sock.sendall(length + data)

def recv_message(sock) -> bytes:
    """Primește mesaj cu length prefix."""
    length_data = sock.recv(4)
    if len(length_data) < 4:
        raise ConnectionError("Incomplete length")
    length, = struct.unpack('!I', length_data)
    return sock.recv(length)
```

---

*Cheatsheet v2.0 — Ianuarie 2025*
