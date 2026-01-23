# Ghid de Depanare

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

> 📚 **Documente înrudite:**
> - [Fișă Comenzi](./commands_cheatsheet.md) — Referință rapidă
> - [Rezumat Teorie](./theory_summary.md) — Concepte fundamentale
> - [Analogii Concepte](./analogii_concepte.md) — Explicații vizuale
> - [Glosar](./glosar.md) — Termeni și definiții

---

## Probleme Docker

### Containerele nu pornesc

**Simptome:**
- `docker compose up` eșuează
- Containerele apar și dispar imediat

**Verificări și soluții:**

1. **Verificați că Docker Desktop rulează**
   ```powershell
   docker info
   ```
   Dacă nu răspunde, porniți Docker Desktop din meniul Start.

2. **Verificați resursele alocate**
   - Docker Desktop → Settings → Resources
   - Minim: 2 CPU, 4GB RAM
   - Recomandat: 4 CPU, 8GB RAM

3. **Verificați jurnalele**
   ```powershell
   docker compose logs
   ```

4. **Reconstruiți imaginile**
   ```powershell
   docker compose build --no-cache
   docker compose up -d
   ```

5. **Curățare completă și repornire**
   ```powershell
   docker compose down -v
   docker system prune -a
   docker compose up -d
   ```

---

### Portul 8080 este ocupat

**Simptome:**
- Eroare "bind: address already in use"
- "Port is already allocated"

**Soluții:**

1. **Identificați procesul (Windows)**
   ```powershell
   netstat -ano | findstr :8080
   ```
   Notați PID-ul din ultima coloană.

2. **Opriți procesul**
   ```powershell
   taskkill /PID <PID> /F
   ```

3. **Sau schimbați portul în docker-compose.yml**
   ```yaml
   ports:
     - "8090:80"  # În loc de 8080:80
   ```

---

### Docker Compose nu este recunoscut

**Simptome:**
- "'docker-compose' is not recognized"
- "docker compose: command not found"

**Soluții:**

1. **Folosiți sintaxa nouă**
   ```powershell
   # Nou (recomandat)
   docker compose up -d
   
   # Vechi (depreciat)
   docker-compose up -d
   ```

2. **Actualizați Docker Desktop**
   - Descărcați ultima versiune de pe docker.com

---

## Probleme de Rețea

### Echiliborul nu distribuie uniform

**Simptome:**
- Toate cererile merg la un singur backend
- Distribuție neașteptată

**Verificări și soluții:**

1. **Verificați algoritmul în nginx.conf**
   ```nginx
   upstream backend_pool {
       # Pentru round-robin (implicit), nu adăugați nimic
       # least_conn;  # Decomentați pentru least connections
       # ip_hash;     # Decomentați pentru IP hash
       
       server web1:80;
       server web2:80;
       server web3:80;
   }
   ```

2. **Reporniți Nginx după modificări**
   ```powershell
   docker compose restart nginx
   ```

3. **Verificați că toate backend-urile sunt sănătoase**
   ```powershell
   docker ps
   # Toate containerele s11_backend_* ar trebui să fie "Up"
   ```

> 💡 Pentru înțelegerea algoritmilor de echilibrare, vezi [Analogii Concepte](./analogii_concepte.md#6-round-robin-vs-least-connections).

---

### Connection refused

**Simptome:**
- `curl: (7) Failed to connect to localhost port 8080`
- "Connection refused"

**Verificări și soluții:**

1. **Verificați că serviciile rulează**
   ```powershell
   docker ps
   ```

2. **Verificați porturile**
   ```powershell
   docker compose ps
   # Ar trebui să vedeți "0.0.0.0:8080->80/tcp"
   ```

3. **Verificați firewall-ul Windows**
   - Windows Security → Firewall → Allow an app
   - Asigurați-vă că Docker Desktop este permis

4. **Testați accesul direct la container**
   ```powershell
   docker exec s11_nginx_lb wget -qO- http://localhost/health
   ```

> 💡 Pentru înțelegerea port mapping-ului, vezi [Analogii Concepte](./analogii_concepte.md#4-port-mapping).

---

### Timeout la cereri

**Simptome:**
- Cererile durează foarte mult
- "Operation timed out"

**Verificări și soluții:**

1. **Verificați încărcarea containerelor**
   ```powershell
   docker stats
   ```

2. **Creșteți timeout-urile în nginx.conf**
   ```nginx
   proxy_connect_timeout 10s;
   proxy_read_timeout 60s;
   proxy_send_timeout 60s;
   ```

3. **Verificați DNS-ul**
   ```powershell
   docker exec s11_nginx_lb nslookup web1
   ```

---

## Probleme Python

### ModuleNotFoundError

**Simptome:**
- `ModuleNotFoundError: No module named 'requests'`

**Soluții:**

1. **Instalați dependențele**
   ```powershell
   pip install -r setup/requirements.txt
   ```

2. **Sau instalați individual**
   ```powershell
   pip install requests pyyaml dnspython paramiko
   ```

3. **Verificați mediul Python**
   ```powershell
   python --version
   pip list
   ```

---

### SyntaxError cu Python < 3.11

**Simptome:**
- `SyntaxError: invalid syntax` pe linii cu `match` sau `|`

**Soluții:**

1. **Actualizați Python**
   - Descărcați Python 3.11+ de pe python.org

2. **Sau folosiți mediu virtual**
   ```powershell
   py -3.11 -m venv venv
   .\venv\Scripts\activate
   pip install -r setup/requirements.txt
   ```

---

### Permission denied pe socket

**Simptome:**
- `OSError: [Errno 13] Permission denied`

**Soluții:**

1. **Rulați ca Administrator (Windows)**
   - Click dreapta pe PowerShell → "Run as Administrator"

2. **Sau folosiți porturi > 1024**
   - Porturile sub 1024 necesită privilegii speciale

---

## Probleme Wireshark

### Nicio interfață disponibilă

**Simptome:**
- Lista de interfețe este goală
- "No interfaces found"

**Soluții:**

1. **Instalați Npcap**
   - Descărcați de pe npcap.org
   - Sau reinstalați Wireshark și selectați opțiunea Npcap

2. **Rulați Wireshark ca Administrator**

---

### Nu se captează trafic Docker

**Simptome:**
- Captura este goală
- Traficul containerelor nu apare

**Soluții:**

1. **Captați pe interfața corectă**
   - "vEthernet (WSL)" pentru trafic WSL
   - "Loopback Adapter" pentru localhost

2. **Folosiți filtru de captură**
   ```
   port 8080
   ```

3. **Captați din interiorul containerului**
   ```powershell
   docker exec s11_nginx_lb tcpdump -i eth0 -w /tmp/capture.pcap
   docker cp s11_nginx_lb:/tmp/capture.pcap .
   ```

---

## Probleme WSL

### WSL nu pornește

**Simptome:**
- "The virtual machine could not be started"
- "WSL 2 requires an update"

**Soluții:**

1. **Actualizați kernel-ul WSL**
   ```powershell
   wsl --update
   ```

2. **Reporniți serviciul**
   ```powershell
   wsl --shutdown
   wsl
   ```

3. **Activați virtualizarea în BIOS**
   - Reporniți în BIOS/UEFI
   - Activați "Intel VT-x" sau "AMD-V"

---

### Docker nu se conectează la WSL

**Simptome:**
- "Cannot connect to the Docker daemon"
- Integrarea WSL nu funcționează

**Soluții:**

1. **Activați integrarea WSL în Docker Desktop**
   - Settings → Resources → WSL Integration
   - Activați pentru distribuția Ubuntu

2. **Reporniți Docker Desktop**

3. **Verificați din WSL**
   ```bash
   docker ps
   ```

---

## Depanare Generală

### Colectați informații de diagnostic

```powershell
# Versiuni
docker --version
docker compose version
python --version

# Stare containere
docker ps -a

# Jurnale
docker compose logs > logs.txt

# Rețele Docker
docker network ls

# Spațiu disc
docker system df
```

### Resetare completă

Dacă nimic nu funcționează, încercați o resetare completă:

```powershell
# Opriți totul
docker compose down -v
docker system prune -a --volumes

# Reporniți Docker Desktop
# (Închideți din system tray și reporniți)

# Reconstruiți
docker compose build --no-cache
docker compose up -d
```

---

## Obținere Ajutor

Dacă problemele persistă:

1. **Verificați documentația oficială**
   - Docker: https://docs.docker.com/
   - Nginx: https://nginx.org/en/docs/

2. **Căutați pe Stack Overflow**
   - Căutați mesajul de eroare exact

3. **Contactați instructorul**
   - Includeți mesajele de eroare
   - Includeți output-ul de la `docker compose logs`

---

## Navigare Rapidă

- [← Înapoi la README](../README.md)
- [Comenzi Utile →](./commands_cheatsheet.md)
- [Rezumat Teorie →](./theory_summary.md)
- [Glosar →](./glosar.md)

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
