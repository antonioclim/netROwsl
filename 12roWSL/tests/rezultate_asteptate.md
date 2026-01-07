# Rezultate Așteptate - Săptămâna 12

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Acest document prezintă rezultatele așteptate pentru fiecare exercițiu, permițându-vă să verificați dacă implementările funcționează corect.

---

## SMTP (Exercițiul 1)

### Dialog SMTP Reușit

```
Conectare la localhost:1025...
← 220 week12-lab SMTP Educational Server Ready

→ HELO client.local
← 250 week12-lab Hello client.local

→ MAIL FROM:<expeditor@exemplu.ro>
← 250 OK

→ RCPT TO:<destinatar@exemplu.ro>
← 250 OK

→ DATA
← 354 Start mail input; end with <CRLF>.<CRLF>

→ Subject: Test
→ From: expeditor@exemplu.ro
→ To: destinatar@exemplu.ro
→ 
→ Corpul mesajului.
→ .
← 250 OK: Message accepted for delivery

→ LIST
← 250 Messages in spool:
←   - msg_20240115_143000_001.eml

→ QUIT
← 221 Bye
```

### Coduri de Răspuns SMTP Așteptate

| Cod | Semnificație |
|-----|--------------|
| 220 | Serviciu pregătit (banner) |
| 250 | Cerere completată cu succes |
| 354 | Începeți introducerea datelor |
| 221 | Canelul de serviciu se închide |
| 550 | Acțiune cerută nu a fost realizată |
| 500 | Eroare de sintaxă |

---

## JSON-RPC (Exercițiul 2)

### Cerere și Răspuns Standard

**Cerere:**
```json
{
    "jsonrpc": "2.0",
    "method": "add",
    "params": [10, 20],
    "id": 1
}
```

**Răspuns:**
```json
{
    "jsonrpc": "2.0",
    "result": 30,
    "id": 1
}
```

### Apel cu Parametri Numiți

**Cerere:**
```json
{
    "jsonrpc": "2.0",
    "method": "subtract",
    "params": {"a": 100, "b": 42},
    "id": 2
}
```

**Răspuns:**
```json
{
    "jsonrpc": "2.0",
    "result": 58,
    "id": 2
}
```

### Apel în Lot (Batch)

**Cerere:**
```json
[
    {"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1},
    {"jsonrpc": "2.0", "method": "multiply", "params": [3, 4], "id": 2},
    {"jsonrpc": "2.0", "method": "get_time", "id": 3}
]
```

**Răspuns:**
```json
[
    {"jsonrpc": "2.0", "result": 3, "id": 1},
    {"jsonrpc": "2.0", "result": 12, "id": 2},
    {"jsonrpc": "2.0", "result": "2024-01-15T14:30:00.000000", "id": 3}
]
```

### Erori JSON-RPC

**Metodă inexistentă:**
```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32601,
        "message": "Method not found"
    },
    "id": 1
}
```

**Împărțire la zero:**
```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32602,
        "message": "Invalid params: Division by zero"
    },
    "id": 1
}
```

---

## XML-RPC (Exercițiul 3)

### Introspecție - Listare Metode

**Cerere:**
```xml
<?xml version="1.0"?>
<methodCall>
    <methodName>system.listMethods</methodName>
</methodCall>
```

**Răspuns:**
```xml
<?xml version="1.0"?>
<methodResponse>
    <params>
        <param>
            <value>
                <array>
                    <data>
                        <value><string>add</string></value>
                        <value><string>subtract</string></value>
                        <value><string>multiply</string></value>
                        <value><string>divide</string></value>
                        <value><string>system.listMethods</string></value>
                        <value><string>system.methodHelp</string></value>
                    </data>
                </array>
            </value>
        </param>
    </params>
</methodResponse>
```

### Apel de Calcul

**Cerere:**
```xml
<?xml version="1.0"?>
<methodCall>
    <methodName>multiply</methodName>
    <params>
        <param><value><int>7</int></value></param>
        <param><value><int>8</int></value></param>
    </params>
</methodCall>
```

**Răspuns:**
```xml
<?xml version="1.0"?>
<methodResponse>
    <params>
        <param>
            <value><int>56</int></value>
        </param>
    </params>
</methodResponse>
```

---

## gRPC (Exercițiul 4)

### Ieșire Client Python

```
Conectare la localhost:6251...
Apelare Add(10, 20)...
Rezultat: 30

Apelare Subtract(100, 42)...
Rezultat: 58

Apelare Echo("Salut!")...
Răspuns: Salut!

Apelare GetStats()...
Statistici server:
  - Total cereri: 42
  - Cereri pe secundă: 3.5
  - Timp mediu răspuns: 0.5ms
```

### Erori gRPC

```
grpc.RpcError: <_InactiveRpcError of RPC that terminated with:
    status = StatusCode.UNAVAILABLE
    details = "failed to connect to all addresses"
>
```

---

## Benchmark RPC (Exercițiul 5)

### Rezultate Așteptate (Orientative)

```
=== Benchmark RPC - Laboratorul Săptămânii 12 ===

Configurație:
  - Operație: add(10, 20)
  - Număr iterații: 1000
  - Warmup: 100 iterații

Rezultate:
┌────────────┬───────────────┬──────────────┬─────────────┐
│ Protocol   │ Cereri/sec    │ Latență medie│ Latență p99 │
├────────────┼───────────────┼──────────────┼─────────────┤
│ JSON-RPC   │ 800-2000      │ 0.5-2.0 ms   │ 2-5 ms      │
│ XML-RPC    │ 500-1500      │ 0.7-3.0 ms   │ 3-8 ms      │
│ gRPC       │ 1500-5000     │ 0.2-0.8 ms   │ 1-3 ms      │
└────────────┴───────────────┴──────────────┴─────────────┘

Dimensiuni mesaje (operație add):
  - JSON-RPC: ~60 bytes cerere, ~40 bytes răspuns
  - XML-RPC:  ~180 bytes cerere, ~120 bytes răspuns
  - gRPC:     ~20 bytes cerere, ~10 bytes răspuns
```

**Notă:** Valorile pot varia semnificativ în funcție de:
- Configurația hardware
- Încărcarea sistemului
- Latența rețelei (chiar și pe localhost)
- Versiunea Python și a bibliotecilor

---

## Capturi Wireshark

### Ce să Căutați în Capturi

**SMTP:**
- Handshake TCP (SYN, SYN-ACK, ACK)
- Banner-ul 220
- Comenzi în text clar (HELO, MAIL FROM, etc.)
- Răspunsuri numerice

**JSON-RPC:**
- Cereri HTTP POST
- Content-Type: application/json
- Payload JSON în corpul cererii
- Răspuns HTTP 200 cu JSON

**XML-RPC:**
- Cereri HTTP POST
- Content-Type: text/xml
- Structuri XML în payload
- Răspuns cu `<methodResponse>`

**gRPC:**
- HTTP/2 streams
- Frame-uri HEADERS și DATA
- Compresie (dacă activată)
- Multiple cereri pe aceeași conexiune

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
