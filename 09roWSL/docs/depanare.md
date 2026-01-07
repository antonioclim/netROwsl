# Ghid de Depanare: Săptămâna 9

> Soluții pentru Probleme Frecvente
> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

---

## Probleme Docker

### Docker Desktop nu pornește

**Simptome:**
- Iconiță gri în system tray
- Mesaj "Docker Desktop is starting..."
- Containerele nu pot fi pornite

**Soluții:**

1. **Verificați WSL2:**
   ```powershell
   wsl --status
   wsl --update
   ```

2. **Reporniți serviciul Docker:**
   ```powershell
   # În PowerShell ca Administrator
   Stop-Service docker
   Start-Service docker
   ```

3. **Resetați Docker Desktop:**
   - Click dreapta pe iconița Docker → Troubleshoot → Reset to factory defaults

4. **Verificați virtualizarea:**
   - Task Manager → Performance → CPU → Virtualization: Enabled
   - Dacă e dezactivată, activați din BIOS

---

### Containerele nu pornesc

**Simptome:**
- `docker compose up` eșuează
- Containerele intră în restart loop

**Diagnosticare:**
```bash
# Verifică log-urile
docker logs s9_ftp-server

# Verifică starea detaliată
docker inspect s9_ftp-server
```

**Soluții:**

1. **Reconstruiți imaginile:**
   ```bash
   docker compose build --no-cache
   docker compose up -d
   ```

2. **Curățați resursele vechi:**
   ```bash
   docker compose down -v
   docker system prune -f
   docker compose up -d
   ```

---

### Portul 2121 este ocupat

**Simptome:**
- Eroare: "port is already allocated"
- Serverul FTP nu pornește

**Diagnosticare:**
```powershell
# Windows
netstat -ano | findstr :2121

# Linux/WSL
lsof -i :2121
```

**Soluții:**

1. **Opriți procesul care ocupă portul:**
   ```powershell
   # Găsiți PID-ul
   netstat -ano | findstr :2121
   
   # Opriți procesul
   taskkill /PID <pid> /F
   ```

2. **Schimbați portul în docker-compose.yml:**
   ```yaml
   ports:
     - "2122:21"  # Folosiți alt port
   ```

---

## Probleme FTP

### Conexiunea FTP eșuează

**Simptome:**
- "Connection refused"
- "Connection timed out"
- Client-ul nu se poate conecta

**Soluții:**

1. **Verificați că serverul rulează:**
   ```bash
   docker ps | grep ftp-server
   docker logs s9_ftp-server
   ```

2. **Testați conexiunea:**
   ```bash
   # Din WSL sau container
   nc -zv localhost 2121
   
   # Cu telnet
   telnet localhost 2121
   ```

3. **Verificați firewall-ul Windows:**
   - Setări → Firewall → Permiteți o aplicație
   - Adăugați Docker Desktop

---

### Autentificare eșuată (530)

**Simptome:**
- Cod răspuns 530
- "Login incorrect"

**Soluții:**

1. **Verificați credențialele:**
   - Utilizator: `test`
   - Parolă: `12345`

2. **Verificați configurația serverului:**
   ```bash
   docker logs s9_ftp-server | grep -i auth
   ```

---

### Mod pasiv nu funcționează

**Simptome:**
- Conexiunea de control funcționează
- LIST/RETR eșuează
- "425 Can't open data connection"

**Soluții:**

1. **Verificați porturile passive:**
   ```bash
   # Trebuie să fie deschise 60000-60010
   docker port s9_ftp-server
   ```

2. **Verificați în docker-compose.yml:**
   ```yaml
   ports:
     - "60000-60010:60000-60010"
   ```

3. **Testați manual:**
   ```python
   from ftplib import FTP
   ftp = FTP()
   ftp.connect('localhost', 2121)
   ftp.login('test', '12345')
   ftp.set_pasv(True)  # Forțează mod pasiv
   ftp.retrlines('LIST')
   ```

---

## Probleme Python struct

### struct.error: unpack requires a buffer

**Cauză:** Date insuficiente pentru format

**Soluție:**
```python
# Verificați lungimea înainte de despachetare
format_header = ">4sII"
dimensiune_header = struct.calcsize(format_header)

if len(date) >= dimensiune_header:
    rezultat = struct.unpack(format_header, date[:dimensiune_header])
else:
    raise ValueError(f"Date insuficiente: {len(date)} < {dimensiune_header}")
```

---

### Valori greșite la despachetare

**Cauză:** Ordine octeți incorectă

**Soluție:**
```python
# Asigurați-vă că folosiți aceeași ordine
# La împachetare
date = struct.pack(">I", 0x12345678)  # Big-endian

# La despachetare - TREBUIE să fie același
valoare = struct.unpack(">I", date)[0]  # Big-endian

# NU amestecați!
# Greșit: struct.unpack("<I", date)  # Little-endian
```

---

### Eroare la împachetare string

**Cauză:** String-ul trebuie să fie bytes, nu str

**Soluție:**
```python
# Greșit
struct.pack("4s", "TEST")  # TypeError

# Corect
struct.pack("4s", b"TEST")
struct.pack("4s", "TEST".encode('utf-8'))
```

---

## Probleme WSL2

### WSL2 nu este instalat

**Soluție:**
```powershell
# În PowerShell ca Administrator
wsl --install

# Reporniți calculatorul

# Verificați
wsl --status
```

---

### Probleme de rețea între Windows și WSL

**Simptome:**
- Nu se poate accesa localhost din Windows
- Containerele nu sunt accesibile

**Soluții:**

1. **Verificați IP-ul WSL:**
   ```bash
   # În WSL
   ip addr show eth0
   ```

2. **Folosiți IP-ul explicit în loc de localhost:**
   ```python
   ftp.connect('172.x.x.x', 2121)  # IP-ul din WSL
   ```

3. **Reporniți WSL:**
   ```powershell
   wsl --shutdown
   wsl
   ```

---

## Probleme Wireshark

### Nu se vede traficul Docker

**Soluții:**

1. **Selectați interfața corectă:**
   - Windows: `\\.\pipe\docker_engine` sau `vEthernet (WSL)`
   - Interfețe care încep cu `br-` (bridge)

2. **Capturați din interior container:**
   ```bash
   docker exec -it s9_ftp-server tcpdump -i eth0 -w /tmp/captura.pcap
   docker cp s9_ftp-server:/tmp/captura.pcap ./
   ```

---

### Traficul apare criptat

**Cauză:** FTPS sau conexiune TLS

**Soluție:**
- Pentru laborator, folosim FTP necriptat
- Verificați că nu folosiți portul 990 (FTPS implicit)

---

## Verificări Rapide

### Lista de Control Diagnosticare

```bash
# 1. Docker rulează?
docker info

# 2. Containerele sunt active?
docker ps

# 3. Rețeaua există?
docker network ls | grep week9

# 4. Porturile sunt deschise?
netstat -an | findstr 2121

# 5. Serverul răspunde?
curl -v telnet://localhost:2121

# 6. Log-uri de erori?
docker logs s9_ftp-server 2>&1 | tail -20
```

---

## Contactați Asistența

Dacă problemele persistă:

1. **Colectați informații:**
   ```bash
   docker version > diagnosticare.txt
   docker compose version >> diagnosticare.txt
   docker logs s9_ftp-server >> diagnosticare.txt 2>&1
   python --version >> diagnosticare.txt
   ```

2. **Descrieți problema:**
   - Ce încercați să faceți?
   - Ce eroare primiți (text exact)?
   - Ce pași ați încercat deja?

3. **Trimiteți la:**
   - Forum curs
   - Email instructor
   - Sesiune de laborator

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
