# Ghid de Depanare

> Laborator Săptămâna 13 - IoT și Securitate în Rețelele de Calculatoare
>
> Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Acest document acoperă problemele frecvente și soluțiile lor.

---

## Probleme Docker

### Containerele nu pornesc

**Simptome:**
```
Cannot connect to the Docker daemon
Error response from daemon: driver failed programming external connectivity
```

**Soluții:**

1. **Verificați că Docker Desktop rulează:**
   - Deschideți Docker Desktop din Start Menu
   - Așteptați până când iconița din System Tray devine verde

2. **Verificați backend-ul WSL2:**
   ```powershell
   # În PowerShell
   wsl --status
   ```
   Ar trebui să vedeți "Default Version: 2"

3. **Reporniți Docker:**
   ```powershell
   # Opriți Docker
   Stop-Service docker
   # Așteptați 10 secunde
   Start-Service docker
   ```

4. **Reporniți WSL:**
   ```powershell
   wsl --shutdown
   # Așteptați 5 secunde, apoi deschideți o nouă fereastră WSL
   ```

### Porturile sunt deja ocupate

**Simptome:**
```
Bind for 0.0.0.0:1883 failed: port is already allocated
```

**Soluții:**

1. **Identificați procesul care ocupă portul:**
   ```powershell
   netstat -ano | findstr :1883
   ```

2. **Opriți procesul:**
   ```powershell
   taskkill /PID <PID_gasit> /F
   ```

3. **Sau modificați porturile în .env:**
   ```bash
   # Editați .env
   MQTT_PLAIN_PORT=11883
   MQTT_TLS_PORT=18883
   ```

4. **Verificați containere vechi:**
   ```powershell
   docker ps -a
   docker rm -f week13_mosquitto week13_dvwa week13_vsftpd
   ```

### Eroare la construirea imaginii

**Simptome:**
```
failed to solve: dockerfile parse error
```

**Soluții:**

1. **Verificați sintaxa Dockerfile:**
   ```powershell
   docker build -t test -f docker/Dockerfile.vulnerable docker/
   ```

2. **Curățați cache-ul Docker:**
   ```powershell
   docker system prune -f
   docker builder prune -f
   ```

---

## Probleme de Rețea

### Nu se poate conecta la servicii

**Simptome:**
- Scanner-ul arată toate porturile ca "filtrate"
- Nu se poate conecta la broker-ul MQTT

**Soluții:**

1. **Verificați că serviciile rulează:**
   ```powershell
   docker ps
   python scripts/porneste_lab.py --status
   ```

2. **Verificați rețeaua Docker:**
   ```powershell
   docker network ls
   docker network inspect week13net
   ```

3. **Testați conectivitatea:**
   ```powershell
   # Din PowerShell
   Test-NetConnection -ComputerName localhost -Port 1883
   
   # Din WSL
   nc -zv localhost 1883
   ```

4. **Verificați firewall-ul Windows:**
   - Deschideți Windows Defender Firewall
   - Asigurați-vă că Docker Desktop are permisiuni

### Erori DNS în containere

**Simptome:**
```
Could not resolve hostname
```

**Soluții:**

1. **Verificați configurarea DNS în Docker:**
   ```powershell
   docker run --rm alpine nslookup google.com
   ```

2. **Adăugați DNS explicit în docker-compose.yml:**
   ```yaml
   services:
     mosquitto:
       dns:
         - 8.8.8.8
         - 8.8.4.4
   ```

---

## Probleme TLS/Certificate

### Eroare de verificare certificat

**Simptome:**
```
SSL: CERTIFICATE_VERIFY_FAILED
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Soluții:**

1. **Regenerați certificatele:**
   ```powershell
   python setup/configureaza_docker.py --regen-certs
   ```

2. **Verificați că certificatele există:**
   ```powershell
   dir docker/configs/certs/
   # Ar trebui să vedeți: ca.crt, ca.key, server.crt, server.key
   ```

3. **Verificați permisiunile:**
   ```powershell
   # În WSL
   chmod 644 docker/configs/certs/*.crt
   chmod 600 docker/configs/certs/*.key
   ```

4. **Verificați calea certificatului în comandă:**
   ```powershell
   python src/exercises/ex_13_02_client_mqtt.py --tls --ca-cert docker/configs/certs/ca.crt
   ```

### Certificat expirat

**Simptome:**
```
certificate has expired
```

**Soluții:**

1. **Verificați data expirării:**
   ```powershell
   openssl x509 -in docker/configs/certs/server.crt -noout -dates
   ```

2. **Regenerați certificatele:**
   ```powershell
   python setup/configureaza_docker.py --regen-certs
   ```

3. **Reporniți serviciile:**
   ```powershell
   python scripts/opreste_lab.py
   python scripts/porneste_lab.py
   ```

---

## Probleme Python

### Modul nu a fost găsit

**Simptome:**
```
ModuleNotFoundError: No module named 'paho'
```

**Soluții:**

1. **Instalați pachetul lipsă:**
   ```powershell
   pip install paho-mqtt
   ```

2. **Sau instalați toate dependențele:**
   ```powershell
   pip install docker requests pyyaml paho-mqtt scapy
   ```

3. **Verificați mediul Python:**
   ```powershell
   python --version
   pip list | findstr paho
   ```

### Permisiuni insuficiente pentru Scapy

**Simptome:**
```
PermissionError: [Errno 1] Operation not permitted
```

**Soluții:**

1. **În Windows, rulați ca Administrator:**
   - Click dreapta pe PowerShell → Run as Administrator

2. **În WSL, folosiți sudo:**
   ```bash
   sudo python src/exercises/ex_13_03_sniffer_pachete.py
   ```

3. **Verificați capabilitățile (Linux):**
   ```bash
   sudo setcap cap_net_raw+ep $(which python3)
   ```

---

## Probleme Wireshark

### Nu capturează trafic Docker

**Simptome:**
- Wireshark nu arată pachete din containere
- Interfața Docker nu apare

**Soluții:**

1. **Selectați interfața corectă:**
   - În Wireshark, căutați interfețele care încep cu `vEthernet` sau `docker`
   - Sau selectați "any" pentru a captura de pe toate

2. **Verificați interfețele disponibile:**
   ```powershell
   Get-NetAdapter | Where-Object {$_.InterfaceDescription -like "*Docker*" -or $_.Name -like "*vEthernet*"}
   ```

3. **Utilizați captură din container:**
   ```powershell
   docker exec -it week13_mosquitto tcpdump -i eth0 -w /tmp/capture.pcap
   docker cp week13_mosquitto:/tmp/capture.pcap ./capture.pcap
   ```

### Filtru BPF invalid

**Simptome:**
```
Invalid filter expression
```

**Soluții:**

1. **Verificați sintaxa filtrului:**
   ```
   # Corect
   tcp port 1883
   host 10.0.13.100 and port 1883
   
   # Incorect
   tcp.port == 1883  (aceasta e sintaxă display filter, nu capture filter)
   ```

2. **Testați filtrul:**
   ```powershell
   tcpdump -d "tcp port 1883"
   ```

---

## Comenzi Utile de Diagnostic

### Verificare stare generală

```powershell
# Starea Docker
docker info
docker ps -a
docker network ls

# Starea serviciilor
python scripts/porneste_lab.py --status

# Conectivitate
python -c "import socket; print(socket.create_connection(('localhost', 1883)))"
```

### Loguri servicii

```powershell
# Toate logurile
docker compose -f docker/docker-compose.yml logs

# Loguri specifice
docker logs week13_mosquitto
docker logs week13_dvwa
docker logs week13_vsftpd

# Urmărire în timp real
docker logs -f week13_mosquitto
```

### Curățare completă

```powershell
# Oprește și elimină totul
python scripts/curata.py --complet

# Curățare Docker agresivă (ATENȚIE: afectează TOATE containerele!)
docker system prune -a --volumes -f
```

---

## Obținerea Ajutorului

Dacă problemele persistă:

1. **Verificați documentația:**
   - README.md principal
   - docs/sumar_teorie.md

2. **Colectați informații de diagnostic:**
   ```powershell
   python setup/verifica_mediu.py > diagnostic.txt 2>&1
   docker info >> diagnostic.txt 2>&1
   docker ps -a >> diagnostic.txt 2>&1
   ```

3. **Contactați instructorul** cu fișierul de diagnostic

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix*
