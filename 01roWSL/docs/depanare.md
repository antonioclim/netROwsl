# Ghid de Depanare - Săptămâna 1

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## Probleme Docker

### Docker Desktop nu pornește

**Simptome:**
- Aplicația Docker Desktop nu răspunde
- Pictograma rămâne gri sau roșie
- Mesaj "Docker Desktop is starting..."

**Soluții:**

1. **Verificați cerințele de sistem:**
   ```powershell
   # Windows 10/11 64-bit
   systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
   ```

2. **Verificați virtualizarea:**
   ```powershell
   # Trebuie să afișeze "Virtualization Enabled In Firmware: Yes"
   systeminfo | findstr /i "Hyper-V"
   ```

3. **Reporniți serviciile Docker:**
   ```powershell
   # PowerShell ca Administrator
   Restart-Service docker
   Restart-Service com.docker.service
   ```

4. **Resetare completă:**
   - Închideți Docker Desktop
   - Ștergeți: `%APPDATA%\Docker\`
   - Reporniți Docker Desktop

---

### Eroare "Cannot connect to Docker daemon"

**Simptome:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
Is the docker daemon running?
```

**Soluții:**

1. **Verificați că Docker Desktop rulează:**
   - Căutați pictograma Docker în system tray
   - Așteptați până devine verde

2. **Reporniți Docker Desktop:**
   - Click dreapta pe pictogramă → Restart

3. **Verificați integrarea WSL2:**
   ```powershell
   wsl --list --verbose
   # Ar trebui să vedeți docker-desktop și docker-desktop-data
   ```

---

### Eroare la construirea imaginilor Docker

**Simptome:**
```
ERROR: failed to solve: python:3.12-slim: failed to resolve source metadata
```

**Soluții:**

1. **Verificați conexiunea la internet:**
   ```bash
   ping -c 2 hub.docker.com
   ```

2. **Curățați cache-ul Docker:**
   ```bash
   docker system prune -a
   docker builder prune
   ```

3. **Reconstruiți fără cache:**
   ```bash
   docker compose build --no-cache
   ```

---

### Spațiu pe disc insuficient

**Simptome:**
```
no space left on device
```

**Soluții:**

1. **Verificați utilizarea:**
   ```bash
   docker system df
   ```

2. **Curățați resursele neutilizate:**
   ```bash
   docker system prune -a --volumes
   ```

3. **Verificați dimensiunea imaginilor WSL2:**
   ```powershell
   wsl --list --verbose
   ```

---

## Probleme de Rețea

### "Address already in use"

**Simptome:**
```
OSError: [Errno 98] Address already in use
Bind for 0.0.0.0:9090 failed: port is already allocated
```

**Soluții:**

1. **Identificați procesul care folosește portul:**
   ```bash
   # În Linux/WSL
   ss -tlnp | grep :9090
   lsof -i :9090
   
   # În Windows PowerShell
   netstat -ano | findstr :9090
   ```

2. **Opriți procesul:**
   ```bash
   # Linux - cu PID-ul găsit
   kill <PID>
   kill -9 <PID>  # Forțat
   
   # Windows
   taskkill /PID <PID> /F
   ```

3. **Verificați containerele Docker:**
   ```bash
   docker ps | grep 9090
   docker stop <container_id>
   ```

---

### "Connection refused"

**Simptome:**
```
Connection refused
nc: connect to localhost port 9090 (tcp) failed: Connection refused
```

**Soluții:**

1. **Verificați că serverul rulează:**
   ```bash
   ss -tlnp | grep :9090
   ```

2. **Verificați firewall-ul:**
   ```bash
   # Linux
   sudo iptables -L -n | grep 9090
   
   # Windows - verificați Windows Defender Firewall
   ```

3. **Verificați adresa de bind:**
   - Serverul trebuie să asculte pe `0.0.0.0`, nu doar `127.0.0.1`

---

### Ping nu funcționează

**Simptome:**
```
ping: connect: Network is unreachable
Destination Host Unreachable
Request timed out
```

**Soluții:**

1. **Verificați configurația de rețea:**
   ```bash
   ip addr show
   ip route show
   ```

2. **Verificați gateway-ul:**
   ```bash
   ip route | grep default
   ping -c 2 $(ip route | grep default | awk '{print $3}')
   ```

3. **Verificați rezolvarea DNS:**
   ```bash
   cat /etc/resolv.conf
   nslookup google.com
   ```

4. **În Docker, verificați rețeaua:**
   ```bash
   docker network inspect week1_network
   ```

---

### Rezolvare DNS eșuată

**Simptome:**
```
Name or service not known
Temporary failure in name resolution
```

**Soluții:**

1. **Verificați configurația DNS:**
   ```bash
   cat /etc/resolv.conf
   ```

2. **Testați cu servere DNS publice:**
   ```bash
   nslookup google.com 8.8.8.8
   dig @1.1.1.1 google.com
   ```

3. **În container Docker:**
   ```bash
   # Verificați DNS-ul containerului
   docker exec week1_lab cat /etc/resolv.conf
   ```

---

## Probleme Python

### "ModuleNotFoundError"

**Simptome:**
```
ModuleNotFoundError: No module named 'docker'
```

**Soluții:**

1. **Instalați pachetul lipsă:**
   ```bash
   pip install docker --break-system-packages
   ```

2. **Verificați mediul Python:**
   ```bash
   which python
   python --version
   pip list | grep docker
   ```

3. **Verificați PATH-ul:**
   ```bash
   echo $PATH
   ```

---

### "Permission denied" pentru socket

**Simptome:**
```
PermissionError: [Errno 13] Permission denied
```

**Soluții:**

1. **Pentru socket-uri de rețea pe porturi <1024:**
   ```bash
   # Rulați cu sudo
   sudo python script.py
   
   # Sau folosiți port >1024
   ```

2. **Pentru socket Docker:**
   ```bash
   sudo usermod -aG docker $USER
   # Apoi relogați-vă
   ```

---

## Probleme cu Captura de Trafic

### "Permission denied" pentru tcpdump

**Simptome:**
```
tcpdump: eth0: You don't have permission to capture on that device
```

**Soluții:**

1. **În container Docker:**
   ```bash
   # Verificați capabilitățile
   docker inspect week1_lab | grep -A 10 "CapAdd"
   ```

2. **Rulați cu sudo:**
   ```bash
   sudo tcpdump -i eth0
   ```

3. **Adăugați capabilități la container:**
   ```yaml
   # În docker-compose.yml
   cap_add:
     - NET_ADMIN
     - NET_RAW
   ```

---

### Nu se capturează pachete

**Simptome:**
- tcpdump rulează dar nu afișează nimic

**Soluții:**

1. **Verificați interfața corectă:**
   ```bash
   ip link show
   tcpdump -D  # Listează interfețele disponibile
   ```

2. **Verificați dacă există trafic:**
   ```bash
   # Într-un terminal generați trafic
   ping -c 5 127.0.0.1
   ```

3. **Folosiți interfața loopback:**
   ```bash
   tcpdump -i lo
   ```

4. **Eliminați filtrul:**
   ```bash
   tcpdump -i any  # Toate interfețele, fără filtru
   ```

---

### Fișier PCAP corupt

**Simptome:**
```
tshark: The file "captura.pcap" isn't a capture file in a format TShark understands.
```

**Soluții:**

1. **Verificați fișierul:**
   ```bash
   file captura.pcap
   ls -la captura.pcap
   ```

2. **Capturați din nou cu opțiunile corecte:**
   ```bash
   tcpdump -i lo -w captura.pcap -U  # -U pentru scriere imediată
   ```

---

## Probleme WSL2

### WSL2 nu este instalat

**Simptome:**
```
WSL 2 is not installed
The Windows Subsystem for Linux has not been enabled
```

**Soluții:**

1. **Instalare WSL2:**
   ```powershell
   # PowerShell ca Administrator
   wsl --install
   ```

2. **Activare manuală:**
   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

3. **Setare versiune implicită:**
   ```powershell
   wsl --set-default-version 2
   ```

---

### Probleme de rețea în WSL2

**Simptome:**
- Nu se poate accesa internetul din WSL2
- DNS nu funcționează

**Soluții:**

1. **Resetare WSL2:**
   ```powershell
   wsl --shutdown
   # Așteptați 10 secunde, apoi reporniți
   ```

2. **Regenerare resolv.conf:**
   ```bash
   sudo rm /etc/resolv.conf
   sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
   ```

3. **Dezactivare generare automată:**
   ```bash
   sudo bash -c 'echo "[network]
   generateResolvConf = false" > /etc/wsl.conf'
   ```

---

## Comenzi de Diagnostic Rapid

```bash
# Verificare completă a stării sistemului
echo "=== INTERFEȚE ===" && ip -br a
echo "=== RUTE ===" && ip r
echo "=== SOCKET-URI ===" && ss -tlnp
echo "=== DNS ===" && cat /etc/resolv.conf | grep nameserver
echo "=== CONTAINERE ===" && docker ps 2>/dev/null || echo "Docker indisponibil"
```

---

## Obținerea Ajutorului

Dacă problema persistă:

1. **Verificați jurnalele:**
   ```bash
   docker compose logs
   journalctl -u docker
   ```

2. **Rulați testele de verificare:**
   ```bash
   python tests/test_mediu.py
   python tests/test_rapid.py
   ```

3. **Documentați problema:**
   - Mesajul de eroare complet
   - Pașii pentru reproducere
   - Configurația sistemului

4. **Resurse online:**
   - Stack Overflow
   - Docker Documentation
   - GitHub Issues

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
