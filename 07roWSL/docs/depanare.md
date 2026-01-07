# Ghid de Depanare

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest document oferă soluții pentru problemele frecvent întâlnite în laboratorul Săptămânii 7.

## Probleme Docker

### Docker Desktop nu pornește

**Simptome:**
- Pictograma Docker rămâne în starea "Starting..."
- Mesaj de eroare despre WSL2

**Soluții:**

1. Verificați că WSL2 este instalat și actualizat:
   ```powershell
   wsl --update
   wsl --set-default-version 2
   ```

2. Reporniți serviciul Docker:
   ```powershell
   # Opriți Docker Desktop din System Tray
   # Apoi reporniți aplicația
   ```

3. Verificați că virtualizarea este activată în BIOS:
   - Reporniți calculatorul
   - Intrați în BIOS/UEFI
   - Activați "Intel VT-x" sau "AMD-V"

### Containerele nu pornesc

**Simptome:**
- `docker compose up` returnează eroare
- Containerele se opresc imediat după pornire

**Soluții:**

1. Verificați logurile containerului:
   ```powershell
   docker compose -f docker/docker-compose.yml logs server_tcp
   ```

2. Verificați că porturile nu sunt ocupate:
   ```powershell
   netstat -ano | findstr :9090
   netstat -ano | findstr :9091
   ```

3. Dacă porturile sunt ocupate, identificați procesul:
   ```powershell
   # Găsiți PID-ul din coloana finală a netstat
   tasklist | findstr <PID>
   # Opriți procesul dacă este necesar
   taskkill /PID <PID> /F
   ```

4. Reconstruiți containerele:
   ```powershell
   docker compose -f docker/docker-compose.yml down
   docker compose -f docker/docker-compose.yml up -d --build
   ```

### Rețeaua Docker nu funcționează

**Simptome:**
- Containerele nu pot comunica între ele
- Eroare "network not found"

**Soluții:**

1. Recreați rețeaua:
   ```powershell
   docker network rm week7net
   docker network create --subnet=10.0.7.0/24 week7net
   ```

2. Reporniți Docker Desktop complet

## Probleme Wireshark

### Wireshark nu vede traficul Docker

**Simptome:**
- Filtrul este aplicat dar nu apar pachete
- Captură goală

**Soluții:**

1. Selectați interfața corectă:
   - Pe Windows cu WSL2, folosiți `vEthernet (WSL)` sau `Ethernet`
   - Nu folosiți `Loopback` pentru traficul Docker

2. Verificați că traficul există:
   ```powershell
   python src/apps/client_tcp.py --host localhost --port 9090 --mesaj "test"
   ```

3. Simplificați filtrul:
   - Începeți fără filtru pentru a vedea tot traficul
   - Adăugați filtre treptat

### Eroare "No interfaces found"

**Simptome:**
- Wireshark nu afișează nicio interfață
- Mesaj despre Npcap/WinPcap

**Soluții:**

1. Reinstalați Npcap:
   - Dezinstalați Npcap din Control Panel
   - Descărcați ultima versiune de la https://npcap.com
   - Instalați cu opțiunea "WinPcap API-compatible Mode"

2. Rulați Wireshark ca Administrator

## Probleme Python

### Eroare "ModuleNotFoundError"

**Simptome:**
- `ModuleNotFoundError: No module named 'docker'`
- Script-ul nu rulează

**Soluții:**

1. Instalați dependențele:
   ```powershell
   pip install -r setup/requirements.txt
   ```

2. Verificați că folosiți Python-ul corect:
   ```powershell
   python --version
   where python
   ```

3. Dacă aveți multiple instalări Python:
   ```powershell
   py -3.11 -m pip install -r setup/requirements.txt
   py -3.11 scripts/porneste_lab.py
   ```

### Eroare de permisiuni

**Simptome:**
- "Permission denied" la rularea script-urilor
- Eroare la accesarea fișierelor

**Soluții:**

1. Pe Windows, rulați PowerShell ca Administrator

2. Verificați politica de execuție:
   ```powershell
   Get-ExecutionPolicy
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

## Probleme de Conectivitate

### Server TCP nu răspunde

**Simptome:**
- `Connection refused` sau timeout
- Echo nu funcționează

**Soluții:**

1. Verificați că containerul rulează:
   ```powershell
   docker ps | findstr week7_server_tcp
   ```

2. Testați din interiorul containerului:
   ```powershell
   docker exec -it week7_server_tcp python -c "import socket; s=socket.socket(); s.connect(('localhost',9090)); print('OK')"
   ```

3. Verificați maparea porturilor:
   ```powershell
   docker port week7_server_tcp
   ```

### UDP pare să nu funcționeze

**Simptome:**
- Niciun răspuns de la receptor
- Nu se poate verifica dacă mesajul a ajuns

**Notă importantă:**
UDP este un protocol fără conexiune. Lipsa răspunsului poate însemna:
- Mesajul a ajuns dar receptorul nu trimite răspuns (comportament normal)
- Mesajul a fost eliminat de firewall (DROP)
- Receptorul nu rulează

**Soluții:**

1. Verificați logurile receptorului:
   ```powershell
   docker compose -f docker/docker-compose.yml logs receptor_udp
   ```

2. Asigurați-vă că receptorul rulează:
   ```powershell
   docker ps | findstr week7_receptor_udp
   ```

## Probleme cu Profilele de Firewall

### Profilul nu se aplică

**Simptome:**
- Traficul nu este blocat conform așteptărilor
- Mesaj de eroare la aplicarea profilului

**Soluții:**

1. Verificați că rulați în container cu privilegii:
   ```powershell
   docker exec -it --privileged week7_demo bash
   ```

2. Verificați că iptables este disponibil:
   ```bash
   which iptables
   iptables -L
   ```

3. Rulați cu drepturi root în container:
   ```bash
   sudo python src/apps/firewallctl.py aplica blocare_tcp_9090
   ```

## Curățare și Resetare

### Resetare completă a mediului

Dacă nimic nu funcționează, efectuați o resetare completă:

```powershell
# Opriți și eliminați totul
docker compose -f docker/docker-compose.yml down -v
docker system prune -f
docker network prune -f

# Reporniți Docker Desktop

# Recreați mediul
python scripts/porneste_lab.py
```

### Curățare spațiu pe disc

```powershell
# Eliminați imagini neutilizate
docker image prune -a

# Eliminați volume neutilizate
docker volume prune

# Verificați spațiul utilizat
docker system df
```

## Obținerea Ajutorului

Dacă problemele persistă:

1. Verificați că ați urmat toți pașii din README.md
2. Rulați scriptul de verificare: `python setup/verifica_mediu.py`
3. Colectați informații de diagnostic:
   ```powershell
   docker version
   docker compose version
   python --version
   wsl --status
   ```
4. Consultați documentația oficială Docker și Wireshark

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
