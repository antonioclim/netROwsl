# Ghid de Depanare - Săptămâna 2

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Probleme Frecvente și Soluții

### 1. Docker nu pornește

**Simptome:**
- Eroare "Docker daemon is not running"
- Comenzile docker returnează erori de conexiune

**Soluții:**

1. **Verificați că Docker Desktop rulează:**
   - Căutați pictograma Docker în system tray (colț dreapta jos)
   - Dacă nu este prezentă, porniți Docker Desktop din Start Menu

2. **Reporniți Docker Desktop:**
   ```powershell
   # Închideți Docker Desktop
   # Apoi redeschideți-l din Start Menu
   ```

3. **Verificați WSL2:**
   ```powershell
   wsl --status
   # Asigurați-vă că Default Version este 2
   ```

4. **Reporniți serviciul WSL:**
   ```powershell
   wsl --shutdown
   # Așteptați câteva secunde, apoi porniți Docker Desktop
   ```

### 2. Portul este deja în uz

**Simptome:**
- Eroare "Address already in use"
- Eroare "Bind failed: port 9090"

**Soluții:**

1. **Identificați procesul care folosește portul:**
   ```powershell
   # Windows
   netstat -ano | findstr :9090
   
   # Rezultatul arată PID-ul în ultima coloană
   ```

2. **Opriți procesul:**
   ```powershell
   # Opriți procesul cu PID-ul găsit
   taskkill /PID <pid> /F
   ```

3. **Sau curățați containerele anterioare:**
   ```powershell
   python scripts/cleanup.py --full
   ```

4. **Sau folosiți un alt port:**
   ```powershell
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server --port 9095
   ```

### 3. Conexiune refuzată la server

**Simptome:**
- Eroare "Connection refused"
- Clientul nu se poate conecta

**Soluții:**

1. **Verificați că serverul rulează:**
   ```powershell
   docker exec week2_lab ps aux | grep python
   ```

2. **Verificați că containerul este activ:**
   ```powershell
   docker ps
   # Căutați week2_lab în listă
   ```

3. **Porniți serverul dacă nu rulează:**
   ```powershell
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server
   ```

4. **Verificați porturile expuse:**
   ```powershell
   docker port week2_lab
   ```

### 4. Wireshark nu vede traficul Docker

**Simptome:**
- Wireshark nu capturează pachete de la/către containere
- Interfața de rețea nu arată trafic

**Soluții:**

1. **Selectați interfața corectă:**
   - Încercați "vEthernet (WSL)" sau "vEthernet (Default Switch)"
   - Sau selectați "any" pentru toate interfețele

2. **Capturați din interiorul containerului:**
   ```powershell
   docker exec week2_lab tcpdump -i any -w /app/pcap/captura.pcap port 9090
   ```

3. **Instalați Npcap cu suport loopback:**
   - Reinstalați Wireshark
   - La instalarea Npcap, bifați "Support loopback traffic"

4. **Folosiți scriptul de captură:**
   ```powershell
   python scripts/capture_traffic.py --interface any
   ```

### 5. Timeout la conexiune

**Simptome:**
- Clientul așteaptă și primește timeout
- Serverul nu răspunde

**Soluții:**

1. **Verificați că ați pornit serverul corect:**
   - Serverul TCP și UDP trebuie pornite manual
   - Containerul doar oferă mediul, nu pornește serverele automat

2. **Verificați firewall-ul Windows:**
   ```powershell
   # Dezactivați temporar firewall-ul pentru testare
   # Sau adăugați o excepție pentru Docker Desktop
   ```

3. **Testați conectivitatea:**
   ```powershell
   # Test TCP
   Test-NetConnection -ComputerName localhost -Port 9090
   
   # Din container
   docker exec week2_lab nc -zv localhost 9090
   ```

### 6. Erori de encoding/caractere

**Simptome:**
- Caractere ciudate în output
- Erori UnicodeDecodeError

**Soluții:**

1. **Asigurați-vă că folosiți UTF-8:**
   ```python
   # În cod Python
   data.decode('utf-8')
   message.encode('utf-8')
   ```

2. **Setați encoding în PowerShell:**
   ```powershell
   [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
   ```

3. **Verificați setările terminalului:**
   - În Windows Terminal: Setări → Profiles → Defaults → Font
   - Alegeți un font care suportă caractere Unicode

### 7. Containerul se oprește imediat

**Simptome:**
- Containerul pornește și se oprește instant
- `docker ps` nu arată containerul

**Soluții:**

1. **Verificați logurile:**
   ```powershell
   docker logs week2_lab
   ```

2. **Porniți containerul interactiv:**
   ```powershell
   docker start -ai week2_lab
   ```

3. **Reconstruiți imaginea:**
   ```powershell
   cd docker
   docker compose build --no-cache
   docker compose up -d
   ```

### 8. Memoria sau CPU insuficiente

**Simptome:**
- Docker este lent sau se blochează
- Erori "out of memory"

**Soluții:**

1. **Creșteți resursele WSL2:**
   - Creați fișierul `%UserProfile%\.wslconfig`:
   ```ini
   [wsl2]
   memory=4GB
   processors=2
   ```
   - Reporniți WSL: `wsl --shutdown`

2. **Curățați resursele Docker neutilizate:**
   ```powershell
   docker system prune -af
   ```

### 9. Python nu găsește modulele

**Simptome:**
- ImportError sau ModuleNotFoundError
- Modulele din scripts/utils nu sunt găsite

**Soluții:**

1. **Rulați din directorul corect:**
   ```powershell
   cd WEEK2_WSLkit_RO
   python scripts/start_lab.py
   ```

2. **Instalați dependențele:**
   ```powershell
   pip install -r setup/requirements.txt
   ```

3. **Verificați versiunea Python:**
   ```powershell
   python --version
   # Trebuie să fie 3.11 sau mai recent
   ```

### 10. Portainer nu se încarcă

**Simptome:**
- https://localhost:9443 nu funcționează
- Eroare de certificat SSL

**Soluții:**

1. **Acceptați certificatul self-signed:**
   - În browser, faceți clic pe "Avansat" → "Continuați către site"

2. **Verificați că containerul rulează:**
   ```powershell
   docker ps | findstr portainer
   ```

3. **Reporniți Portainer:**
   ```powershell
   docker restart week2_portainer
   ```

## Comenzi de Diagnostic

### Verificare Completă a Mediului

```powershell
# Verificare Python
python --version

# Verificare Docker
docker version
docker info

# Verificare WSL
wsl --status
wsl --list --verbose

# Verificare containere
docker ps -a

# Verificare rețele Docker
docker network ls

# Verificare volume Docker
docker volume ls

# Spațiu folosit de Docker
docker system df
```

### Colectare Informații pentru Raportare

```powershell
# Rulați această comandă pentru a colecta informații de diagnostic
python setup/verify_environment.py > diagnostic.txt
docker version >> diagnostic.txt
docker compose version >> diagnostic.txt
wsl --status >> diagnostic.txt
docker ps -a >> diagnostic.txt
docker logs week2_lab >> diagnostic.txt 2>&1
```

## Obținere Ajutor

Dacă problemele persistă:

1. **Verificați documentația:**
   - `README.md` - Instrucțiuni generale
   - `docs/theory_summary.md` - Concepte teoretice
   - `docs/commands_cheatsheet.md` - Comenzi rapide

2. **Colectați informații de diagnostic:**
   - Rulați comenzile de mai sus
   - Notați mesajele de eroare exacte
   - Salvați output-ul comenzilor

3. **Contactați asistentul de laborator:**
   - Descrieți problema clar
   - Atașați informațiile de diagnostic
   - Menționați ce pași ați încercat deja

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
