# Ghid de Depanare: Laborator Săptămâna 4

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

## Cuprins
1. [Probleme Docker](#probleme-docker)
2. [Probleme Rețea](#probleme-rețea)
3. [Probleme Protocol](#probleme-protocol)
4. [Probleme WSL2](#probleme-wsl2)
5. [Probleme Wireshark](#probleme-wireshark)

---

## Probleme Docker

### Docker Desktop nu pornește

**Simptome:**
- Docker Desktop se blochează la pornire
- Mesaj "Docker Desktop is starting..."

**Soluții:**

1. **Reporniți Docker Desktop**
   ```powershell
   # Opriți Docker Desktop din system tray
   # Sau folosiți Task Manager
   taskkill /F /IM "Docker Desktop.exe"
   
   # Reporniți
   Start-Process "Docker Desktop"
   ```

2. **Verificați WSL2**
   ```powershell
   wsl --status
   wsl --update
   ```

3. **Resetați Docker Desktop**
   - Settings → Troubleshoot → Reset to factory defaults
   - **ATENȚIE:** Aceasta șterge toate containerele și imaginile

4. **Verificați Hyper-V/WSL**
   ```powershell
   # Ca Administrator
   bcdedit /set hypervisorlaunchtype auto
   # Reporniți calculatorul
   ```

### Eroare "Cannot connect to Docker daemon"

**Simptome:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Soluții:**

1. **Verificați că Docker Desktop rulează**
   - Căutați pictograma Docker în system tray
   - Ar trebui să fie verde (nu galbenă sau roșie)

2. **Reporniți serviciul Docker**
   ```powershell
   # PowerShell ca Administrator
   Restart-Service docker
   ```

3. **În WSL, verificați integrarea**
   ```bash
   # În terminalul WSL
   docker info
   ```
   Dacă nu funcționează:
   - Docker Desktop → Settings → Resources → WSL Integration
   - Activați pentru distribuția voastră

### Container-ul nu pornește

**Simptome:**
- `docker compose up` eșuează
- Container-ul se oprește imediat

**Diagnoză:**
```bash
# Verificați jurnalele
docker logs week4-lab

# Verificați starea
docker ps -a

# Verificați detalii
docker inspect week4-lab
```

**Soluții comune:**

1. **Port deja în uz**
   ```powershell
   # Găsiți procesul
   netstat -ano | findstr :5400
   
   # Opriți-l sau folosiți alt port
   ```

2. **Eroare de imagine**
   ```bash
   # Reconstruiți imaginea
   docker compose build --no-cache
   docker compose up -d
   ```

3. **Eroare de volum**
   ```bash
   # Ștergeți volumele vechi
   docker compose down -v
   docker compose up -d
   ```

---

## Probleme Rețea

### "Connection refused" pe localhost

**Simptome:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Soluții:**

1. **Verificați că serverul rulează**
   ```bash
   # Verificați starea containerului
   docker ps
   
   # Sau procesele
   netstat -tulpn | grep 5400
   ```

2. **Verificați portul corect**
   - Protocol TEXT: 5400
   - Protocol BINAR: 5401
   - Senzor UDP: 5402

3. **Verificați firewall-ul Windows**
   ```powershell
   # Listați regulile
   Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*Docker*" }
   
   # Adăugați excepție (ca Administrator)
   New-NetFirewallRule -DisplayName "Week4 Lab" -Direction Inbound -Protocol TCP -LocalPort 5400-5402 -Action Allow
   ```

### Timeout la conexiune

**Simptome:**
- Conexiunea durează mult și apoi eșuează
- `socket.timeout` în Python

**Soluții:**

1. **Verificați că serviciul răspunde**
   ```bash
   # Test simplu
   nc -zv localhost 5400
   ```

2. **Măriți timeout-ul în cod**
   ```python
   sock.settimeout(10)  # 10 secunde
   ```

3. **Verificați rețeaua Docker**
   ```bash
   docker network inspect week4_network
   ```

### UDP nu primește răspuns

**Simptome:**
- Mesajele UDP sunt trimise dar nu se primește nimic

**Explicație:**
UDP este un protocol fără conexiune. Serverul poate să nu trimită răspunsuri.

**Verificări:**
```bash
# Verificați că serverul ascultă
netstat -ulpn | grep 5402

# Capturați traficul
sudo tcpdump -i any udp port 5402
```

---

## Probleme Protocol

### CRC32 nu se potrivește

**Simptome:**
- Serverul respinge mesajele cu eroare CRC
- "CRC mismatch" sau similar

**Cauze și Soluții:**

1. **Ordinea octeților greșită**
   ```python
   # GREȘIT: Fără specificare ordine
   struct.pack('I', valoare)
   
   # CORECT: Big-endian (rețea)
   struct.pack('!I', valoare)
   ```

2. **CRC calculat peste date greșite**
   - CRC trebuie calculat ÎNAINTE de a fi adăugat la mesaj
   - Include toate câmpurile antetului EXCEPT CRC-ul în sine

3. **Verificare corectă:**
   ```python
   import binascii
   import struct
   
   # Construire mesaj
   antet_fara_crc = struct.pack('!2sBBHI', b'NP', 1, 0x01, 0, 1)
   crc = binascii.crc32(antet_fara_crc) & 0xFFFFFFFF
   mesaj = antet_fara_crc + struct.pack('!I', crc)
   ```

### Protocol TEXT - Parsare eșuează

**Simptome:**
- Erori de parsare la citirea răspunsului
- Lungimea nu se potrivește

**Cauze:**

1. **Newline lipsă sau în plus**
   ```python
   # Trimitere cu newline
   sock.sendall(b'4 PING\n')
   
   # Sau fără, depinde de implementare
   sock.sendall(b'4 PING')
   ```

2. **Buffer-ul nu conține mesajul complet**
   ```python
   # Citiți până când aveți totul
   date = b''
   while len(date) < lungime_asteptata:
       date += sock.recv(1024)
   ```

### Protocol BINAR - Antet invalid

**Simptome:**
- "Invalid magic number"
- "Unknown message type"

**Verificări:**

1. **Magic corect**
   ```python
   magic = b'NP'  # Exact 2 octeți
   ```

2. **Dimensiune antet corectă (14 octeți)**
   ```python
   antet = struct.pack('!2sBBHII', magic, versiune, tip, lungime, secventa, crc)
   assert len(antet) == 14
   ```

3. **Tip mesaj valid**
   - 0x01: PING
   - 0x02: PONG
   - 0x03: SET
   - 0x04: GET
   - 0x05: DELETE
   - 0x06: RESPONSE
   - 0xFF: ERROR

---

## Probleme WSL2

### WSL nu pornește

**Simptome:**
```
WslRegisterDistribution failed with error
```

**Soluții:**

1. **Actualizați WSL**
   ```powershell
   wsl --update
   wsl --shutdown
   wsl
   ```

2. **Resetați distribuția**
   ```powershell
   wsl --unregister Ubuntu
   wsl --install -d Ubuntu
   ```

3. **Verificați virtualizarea**
   - BIOS: Activați Intel VT-x sau AMD-V
   - Windows Features: Activați "Virtual Machine Platform"

### Rețeaua nu funcționează în WSL

**Simptome:**
- Nu se poate accesa internetul din WSL
- Docker nu poate descărca imagini

**Soluții:**

1. **Resetați rețeaua WSL**
   ```powershell
   wsl --shutdown
   netsh winsock reset
   netsh int ip reset
   # Reporniți calculatorul
   ```

2. **Verificați DNS**
   ```bash
   # În WSL
   cat /etc/resolv.conf
   
   # Dacă e gol, adăugați
   echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
   ```

### Permisiuni fișiere în WSL

**Simptome:**
- "Permission denied" când rulați scripturi
- Fișierele create nu pot fi accesate

**Soluții:**

1. **Setați permisiuni**
   ```bash
   chmod +x script.py
   chmod -R 755 director/
   ```

2. **Probleme de mount Windows**
   ```bash
   # Adăugați în /etc/wsl.conf
   [automount]
   options = "metadata,umask=22,fmask=11"
   ```

---

## Probleme Wireshark

### Nu se văd interfețele

**Simptome:**
- Lista de interfețe e goală
- "No interfaces found"

**Soluții:**

1. **Reinstalați Npcap**
   - Descărcați de pe npcap.com
   - Instalați cu opțiunea "WinPcap API-compatible Mode"

2. **Rulați ca Administrator**
   - Click dreapta pe Wireshark → "Run as administrator"

3. **Verificați serviciul Npcap**
   ```powershell
   Get-Service npcap
   Start-Service npcap
   ```

### Nu se capturează pachete localhost

**Simptome:**
- Traficul pe localhost nu apare
- Capturarea e goală

**Soluții:**

1. **Folosiți interfața Loopback**
   - În Wireshark, selectați "Adapter for loopback traffic capture"
   - Sau "Npcap Loopback Adapter"

2. **Alternativă: RawCap**
   - Descărcați RawCap pentru capturare localhost
   - Sau folosiți tcpdump în WSL/container

### Filtre nu funcționează

**Simptome:**
- Filtrul devine roșu
- Eroare de sintaxă

**Cauze comune:**

1. **Sintaxă greșită**
   ```
   # GREȘIT
   tcp.port = 5400
   
   # CORECT
   tcp.port == 5400
   ```

2. **Confuzie filtru capturare vs. afișare**
   - Filtru capturare (BPF): `port 5400`
   - Filtru afișare: `tcp.port == 5400`

3. **Câmp inexistent pentru protocolul curent**
   - `tcp.port` nu funcționează pentru pachete UDP

---

## Verificări Rapide

### Script de Diagnosticare

Rulați acest script pentru a verifica mediul:

```python
#!/usr/bin/env python3
"""Script rapid de diagnosticare."""

import socket
import subprocess
import sys

def verifica_port(port, protocol='tcp'):
    try:
        if protocol == 'tcp':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        rezultat = s.connect_ex(('localhost', port))
        s.close()
        return rezultat == 0
    except:
        return False

def verifica_docker():
    try:
        rezultat = subprocess.run(['docker', 'info'], capture_output=True, timeout=10)
        return rezultat.returncode == 0
    except:
        return False

print("=== Diagnosticare Rapidă ===\n")

print("Docker:", "✓" if verifica_docker() else "✗")
print("Port 5400 (TEXT):", "✓" if verifica_port(5400) else "✗")
print("Port 5401 (BINAR):", "✓" if verifica_port(5401) else "✗")
print("Port 5402 (UDP):", "✓" if verifica_port(5402, 'udp') else "✗")
print("Port 9443 (Portainer):", "✓" if verifica_port(9443) else "✗")
```

---

## Ajutor Suplimentar

Dacă problemele persistă:

1. **Verificați jurnalele**
   ```bash
   docker logs week4-lab
   ```

2. **Resetați complet**
   ```bash
   python scripts/cleanup.py --full
   python scripts/start_lab.py --rebuild
   ```

3. **Consultați documentația Docker**
   - https://docs.docker.com/desktop/troubleshoot/

4. **Postați pe forum/Moodle**
   - Includeți output-ul comenzilor de diagnosticare
   - Descrieți pașii reproduși

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
