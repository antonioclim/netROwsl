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

## bytes vs str

```python
# String → Bytes (pentru trimitere pe rețea)
text = "Hello"
octeti = text.encode('utf-8')  # b'Hello'

# Bytes → String (pentru afișare)
octeti = b"Hello"
text = octeti.decode('utf-8')  # 'Hello'
```

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
```

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

## HTTP Request Manual

```python
# Request format
request = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"

# Response format
response = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello"
```
