# Fișă de Comenzi - Săptămâna 12

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

## Comenzi Docker

### Gestionare Containere

```bash
# Pornire laborator
python scripts/porneste_lab.py

# Oprire laborator
python scripts/opreste_lab.py

# Verificare stare
docker ps
docker compose ps

# Vizualizare jurnale
docker compose logs
docker compose logs -f             # Urmărire în timp real
docker compose logs week12_lab     # Doar un serviciu

# Intrare în container
docker exec -it week12_lab bash

# Repornire serviciu
docker compose restart week12_lab

# Reconstruire imagini
docker compose build --no-cache
python scripts/porneste_lab.py --rebuild
```

### Curățare

```bash
# Oprire și eliminare containere
docker compose down

# Cu eliminare volume
docker compose down --volumes

# Curățare completă
python scripts/curata.py --complet

# Curățare resurse neutilizate
docker system prune -f
docker volume prune -f
```

---

## Comenzi SMTP

### Dialog Manual cu Netcat

```bash
# Conectare
nc localhost 1025

# Secvență comenzi
HELO client.local
MAIL FROM:<expeditor@exemplu.ro>
RCPT TO:<destinatar@exemplu.ro>
DATA
Subject: Test
From: expeditor@exemplu.ro
To: destinatar@exemplu.ro

Corpul mesajului.
.
LIST
QUIT
```

### Testare cu Telnet

```bash
telnet localhost 1025
```

### Verificare Email-uri Stocate

```bash
docker exec week12_lab ls -la /app/spool/
docker exec week12_lab cat /app/spool/<fisier>.eml
```

---

## Comenzi JSON-RPC

### Apel Simplu cu curl

```bash
# Operație de adunare
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"add","params":[10,20],"id":1}'

# Parametri numiți
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"subtract","params":{"a":100,"b":42},"id":2}'

# Informații server
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"get_server_info","id":3}'

# Statistici
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"get_stats","id":4}'
```

### Apel în Lot (Batch)

```bash
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '[
    {"jsonrpc":"2.0","method":"add","params":[1,2],"id":1},
    {"jsonrpc":"2.0","method":"multiply","params":[3,4],"id":2},
    {"jsonrpc":"2.0","method":"get_time","id":3}
  ]'
```

### Client Python

```python
import json
import urllib.request

def apel_jsonrpc(metoda, parametri=None, id=1):
    cerere = {
        "jsonrpc": "2.0",
        "method": metoda,
        "id": id
    }
    if parametri:
        cerere["params"] = parametri
    
    req = urllib.request.Request(
        "http://localhost:6200",
        data=json.dumps(cerere).encode(),
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req) as raspuns:
        return json.loads(raspuns.read())

# Utilizare
print(apel_jsonrpc("add", [10, 20]))
```

---

## Comenzi XML-RPC

### Apel cu curl

```bash
# Adunare
curl -X POST http://localhost:6201 \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
  <methodCall>
    <methodName>add</methodName>
    <params>
      <param><value><int>10</int></value></param>
      <param><value><int>20</int></value></param>
    </params>
  </methodCall>'

# Listare metode
curl -X POST http://localhost:6201 \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
  <methodCall>
    <methodName>system.listMethods</methodName>
  </methodCall>'
```

### Client Python

```python
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:6201")

# Apeluri
print(proxy.add(10, 20))
print(proxy.multiply(5, 6))

# Introspecție
print(proxy.system.listMethods())
print(proxy.system.methodHelp("add"))
```

---

## Comenzi gRPC

### Client Python

```python
import grpc
import calculator_pb2
import calculator_pb2_grpc

# Creare canal
canal = grpc.insecure_channel("localhost:6251")
stub = calculator_pb2_grpc.CalculatorServiceStub(canal)

# Apeluri
cerere = calculator_pb2.BinaryOpRequest(a=10, b=20)
raspuns = stub.Add(cerere)
print(f"Rezultat: {raspuns.result}")

# Echo
cerere_echo = calculator_pb2.EchoRequest(message="Salut!")
raspuns_echo = stub.Echo(cerere_echo)
print(f"Echo: {raspuns_echo.message}")

canal.close()
```

### Regenerare Stub-uri

```bash
cd src/apps/rpc/grpc
python -m grpc_tools.protoc -I. \
  --python_out=. \
  --grpc_python_out=. \
  calculator.proto
```

---

## Comenzi Wireshark / tcpdump

### Captură cu tcpdump

```bash
# Tot traficul laboratorului
tcpdump -i any -w captura.pcap port 1025 or port 6200 or port 6201 or port 6251

# Doar SMTP
tcpdump -i any -w smtp.pcap port 1025

# Doar RPC HTTP
tcpdump -i any -w rpc_http.pcap port 6200 or port 6201

# Cu afișare în timp real
tcpdump -i any -A port 6200
```

### Script de Captură

```bash
python scripts/captura_trafic.py --protocol smtp --durata 60
python scripts/captura_trafic.py --protocol toate --output pcap/sesiune.pcap
```

### Filtre Wireshark

```
# SMTP
tcp.port == 1025
smtp
smtp.req.command == "DATA"
smtp.response.code >= 400

# JSON-RPC / XML-RPC
tcp.port == 6200 or tcp.port == 6201
http.request.method == "POST"
http contains "jsonrpc"
http contains "methodCall"

# gRPC
tcp.port == 6251
http2

# Analiză TCP
tcp.analysis.retransmission
tcp.analysis.duplicate_ack
tcp.flags.syn == 1
```

---

## Comenzi Python

### Verificare Mediu

```bash
# Verificare cerințe
python setup/verifica_mediu.py

# Instalare dependențe
pip install -r setup/requirements.txt --break-system-packages

# Rulare teste
python -m pytest tests/
python tests/smoke_test.py
```

### Demonstrații

```bash
# Toate demonstrațiile
python scripts/ruleaza_demo.py --demo all

# Demo specific
python scripts/ruleaza_demo.py --demo smtp
python scripts/ruleaza_demo.py --demo jsonrpc
python scripts/ruleaza_demo.py --demo rpc-compara

# Fără pauze interactive
python scripts/ruleaza_demo.py --demo all --fara-pauze
```

### Benchmark

```bash
python src/apps/rpc/benchmark_rpc.py
```

---

## Comenzi de Rețea

### Verificare Porturi

```powershell
# Windows
netstat -ano | findstr :1025
Test-NetConnection -ComputerName localhost -Port 6200

# Linux/WSL
ss -tlnp | grep 1025
nc -zv localhost 6200
```

### Diagnostic DNS

```bash
nslookup localhost
host localhost
dig localhost
```

---

## Scurtături Utile

| Acțiune | Comandă |
|---------|---------|
| Pornire laborator | `python scripts/porneste_lab.py` |
| Oprire laborator | `python scripts/opreste_lab.py` |
| Stare servicii | `python scripts/porneste_lab.py --status` |
| Curățare completă | `python scripts/curata.py --complet` |
| Jurnale live | `docker compose logs -f` |
| Intrare container | `docker exec -it week12_lab bash` |
| Test rapid | `python tests/smoke_test.py` |

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
