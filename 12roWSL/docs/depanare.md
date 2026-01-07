# Ghid de Depanare - Săptămâna 12

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

## Cuprins

1. [Probleme Docker](#probleme-docker)
2. [Probleme de Conectivitate](#probleme-de-conectivitate)
3. [Probleme SMTP](#probleme-smtp)
4. [Probleme JSON-RPC](#probleme-json-rpc)
5. [Probleme XML-RPC](#probleme-xml-rpc)
6. [Probleme gRPC](#probleme-grpc)
7. [Probleme Wireshark](#probleme-wireshark)

---

## Probleme Docker

### Docker Desktop nu pornește

**Simptome:**
- Pictograma Docker rămâne gri
- Mesaj "Docker Desktop is starting..."

**Soluții:**
1. Verificați că virtualizarea este activată în BIOS (VT-x/AMD-V)
2. Reporniți serviciul Docker:
   ```powershell
   Restart-Service docker
   ```
3. Resetați Docker Desktop la setările implicite:
   - Deschideți Docker Desktop > Settings > Troubleshoot > Reset to factory defaults

### Containerele nu pornesc

**Simptome:**
- `docker compose up` returnează erori
- Containerele sunt în starea "Exited"

**Diagnostic:**
```powershell
# Verificați jurnalele
docker compose logs

# Verificați starea containerelor
docker ps -a
```

**Soluții frecvente:**
1. Conflict de porturi - verificați dacă porturile sunt deja ocupate:
   ```powershell
   netstat -ano | findstr :1025
   netstat -ano | findstr :6200
   ```
2. Resurse insuficiente - verificați memoria disponibilă
3. Reconstruiți imaginile:
   ```powershell
   python scripts/porneste_lab.py --rebuild
   ```

### Eroare "port already allocated"

**Cauză:** Un alt proces sau container folosește portul.

**Soluție:**
```powershell
# Identificați procesul
netstat -ano | findstr :<port>

# Opriți procesul (înlocuiți <pid>)
taskkill /PID <pid> /F

# Sau opriți toate containerele
docker stop $(docker ps -q)
```

---

## Probleme de Conectivitate

### Nu pot conecta la servicii

**Simptome:**
- "Connection refused" sau "Connection timeout"
- Serviciile nu răspund

**Verificări:**
```powershell
# Verificați că containerele rulează
docker ps

# Verificați porturile expuse
docker port week12_lab

# Testați conectivitatea
Test-NetConnection -ComputerName localhost -Port 1025
```

**Soluții:**
1. Asigurați-vă că Docker Desktop are integrare WSL2 activă
2. Verificați firewall-ul Windows
3. Reporniți Docker Desktop

### Wireshark nu vede traficul

**Cauză:** Interfața greșită selectată.

**Soluție:**
- Pentru trafic local Docker, selectați:
  - `Adapter for loopback traffic capture` (Npcap Loopback)
  - Sau `\Device\NPF_Loopback`
- Pentru WSL2, poate fi necesară interfața `vEthernet (WSL)`

---

## Probleme SMTP

### Conexiune refuzată la portul 1025

**Verificare:**
```bash
nc -zv localhost 1025
```

**Soluții:**
1. Verificați că serverul SMTP rulează:
   ```bash
   docker exec week12_lab ps aux | grep smtp
   ```
2. Reporniți serviciul:
   ```bash
   docker exec week12_lab pkill -f smtp_server.py
   docker exec week12_lab python src/email/smtp_server.py &
   ```

### Eroare "550 Mailbox not found"

**Cauză:** Adresa destinatarului este invalidă sau restricționată.

**Soluție:** Serverul educațional acceptă orice adresă. Verificați sintaxa:
```
RCPT TO:<adresa@domeniu.ro>
```

### Mesajele nu apar în spool

**Verificare:**
```bash
docker exec week12_lab ls -la /app/spool/
```

**Soluții:**
1. Verificați permisiunile directorului:
   ```bash
   docker exec week12_lab chmod 777 /app/spool
   ```
2. Verificați că DATA a fost terminat corect (linie cu doar `.`)

---

## Probleme JSON-RPC

### Eroare "Connection refused" pe portul 6200

**Verificare:**
```bash
curl http://localhost:6200
```

**Soluții:**
1. Verificați procesul serverului:
   ```bash
   docker exec week12_lab ps aux | grep jsonrpc
   ```
2. Testați din interiorul containerului:
   ```bash
   docker exec week12_lab curl localhost:6200
   ```

### Eroare "Parse error" (-32700)

**Cauză:** JSON malformat în cerere.

**Verificare:**
```bash
# JSON valid
echo '{"jsonrpc":"2.0","method":"add","params":[1,2],"id":1}' | python -m json.tool
```

**Soluții:**
- Verificați ghilimelele (trebuie să fie duble `"`)
- Verificați virgulele și parantezele

### Eroare "Method not found" (-32601)

**Cauză:** Metoda nu există pe server.

**Verificare metodelor disponibile:**
```bash
curl -X POST http://localhost:6200 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"get_server_info","id":1}'
```

### Eroare "Invalid params" (-32602)

**Cauză:** Parametrii nu corespund semnăturii metodei.

**Soluții:**
- Verificați numărul de parametri
- Verificați tipurile de date
- Consultați documentația metodei

---

## Probleme XML-RPC

### Eroare "Connection refused" pe portul 6201

Similar cu JSON-RPC. Verificați:
```bash
docker exec week12_lab ps aux | grep xmlrpc
```

### Eroare de parsare XML

**Cauză:** XML malformat.

**Verificare:**
```bash
# Validare XML
echo '<?xml version="1.0"?><methodCall>...</methodCall>' | xmllint --format -
```

**Probleme frecvente:**
- Tag-uri neînchise
- Caractere speciale neescapate (`<`, `>`, `&`)
- Encoding incorect

### Introspecția nu funcționează

**Cauză:** Introspecția poate fi dezactivată pe server.

**Verificare:**
```python
import xmlrpc.client
proxy = xmlrpc.client.ServerProxy("http://localhost:6201")
print(proxy.system.listMethods())
```

---

## Probleme gRPC

### Eroare de import grpcio

**Simptome:**
```
ModuleNotFoundError: No module named 'grpc'
```

**Soluție:**
```bash
pip install grpcio grpcio-tools --break-system-packages
```

### Fișierele _pb2.py lipsesc

**Cauză:** Stub-urile gRPC nu au fost generate.

**Soluție:**
```bash
cd src/apps/rpc/grpc
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
```

### Eroare "failed to connect to all addresses"

**Cauze posibile:**
1. Serverul gRPC nu rulează
2. Port greșit
3. Probleme de rețea

**Diagnostic:**
```bash
# Verificați procesul
docker exec week12_lab ps aux | grep grpc

# Testați portul
nc -zv localhost 6251
```

### Eroare de deserializare Protocol Buffers

**Cauză:** Versiuni incompatibile ale fișierelor .proto.

**Soluție:** Regenerați stub-urile pe ambele părți (client și server).

---

## Probleme Wireshark

### Nu se capturează pachete

**Soluții:**
1. Rulați Wireshark ca Administrator
2. Verificați că Npcap este instalat corect
3. Selectați interfața corectă (vezi secțiunea Conectivitate)

### Traficul gRPC nu este decodat

**Cauză:** HTTP/2 nu este recunoscut automat.

**Soluție:**
1. Wireshark > Analyze > Decode As
2. Selectați portul 6251
3. Setați protocolul ca HTTP2

### Filtrele nu funcționează

**Probleme frecvente:**
- Sintaxă greșită (folosiți `==` nu `=`)
- Filtre de captură vs filtre de afișare
- Protocol nesuportat

**Exemple corecte:**
```
tcp.port == 1025
http.request.method == "POST"
ip.addr == 172.28.12.10
```

---

## Comenzi Utile de Diagnostic

### Verificare Generală

```powershell
# Starea completă
python scripts/porneste_lab.py --status

# Jurnale Docker
docker compose logs --tail=50

# Resurse Docker
docker system df
docker stats --no-stream
```

### Verificare Rețea

```bash
# Din interiorul containerului
docker exec -it week12_lab bash

# Verificare porturi ascultate
netstat -tlnp

# Test conectivitate
nc -zv localhost 1025
curl -v http://localhost:6200
```

### Resetare Completă

```powershell
# Oprire și curățare completă
python scripts/curata.py --complet --prune

# Repornire de la zero
python scripts/porneste_lab.py --rebuild
```

---

## Contactați Asistența

Dacă problemele persistă după parcurgerea acestui ghid:

1. Documentați eroarea exactă (copie ecran sau text)
2. Includeți jurnalele relevante (`docker compose logs`)
3. Specificați sistemul de operare și versiunile
4. Contactați tutorele sau postați pe forumul cursului

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
