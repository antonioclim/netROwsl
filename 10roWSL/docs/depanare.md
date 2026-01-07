# Ghid de Depanare

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Cuprins

1. [Probleme Docker](#probleme-docker)
2. [Probleme de Rețea](#probleme-de-rețea)
3. [Probleme cu Serviciile](#probleme-cu-serviciile)
4. [Probleme Python](#probleme-python)
5. [Mesaje de Eroare Comune](#mesaje-de-eroare-comune)

---

## Probleme Docker

### Docker Desktop nu pornește

**Simptome:** Docker Desktop nu se deschide sau rămâne blocat la pornire.

**Soluții:**
1. Reporniți Windows
2. Verificați că virtualizarea este activată în BIOS
3. Rulați PowerShell ca Administrator:
   ```powershell
   wsl --update
   wsl --shutdown
   ```

### Containerele nu pornesc

**Simptome:** `docker compose up` afișează erori.

**Verificare:**
```powershell
# Verificați că Docker rulează
docker info

# Verificați resursele disponibile
docker system df

# Curățați resurse neutilizate
docker system prune -f
```

### Eroare: "Cannot connect to the Docker daemon"

**Soluție:**
1. Deschideți Docker Desktop
2. Așteptați să pornească complet (iconița devine verde)
3. Sau reporniți serviciul:
   ```powershell
   Restart-Service docker
   ```

### Eroare: "Ports are not available"

**Simptome:** Port deja utilizat de alt proces.

**Verificare și rezolvare:**
```powershell
# Găsiți ce folosește portul 8000
netstat -ano | findstr :8000

# Opriți procesul cu PID-ul găsit
taskkill /PID <pid> /F
```

---

## Probleme de Rețea

### Nu pot accesa serviciile pe localhost

**Verificare:**
```powershell
# Testați conexiunea HTTP
curl http://localhost:8000

# Verificați containerele active
docker ps

# Verificați porturile containerului
docker port week10_web
```

### Containerele nu comunică între ele

**Soluție:**
```powershell
# Verificați rețeaua Docker
docker network ls
docker network inspect week10_labnet

# Reconectați containerele la rețea
docker network disconnect week10_labnet week10_web
docker network connect week10_labnet week10_web
```

### DNS nu funcționează

**Verificare:**
```bash
# Din containerul debug
docker exec -it week10_debug dig @dns-server -p 5353 web.lab.local

# Sau din sistem
dig @localhost -p 5353 web.lab.local
```

**Dacă `dig` nu este disponibil:**
```powershell
# Windows - folosiți nslookup
nslookup -port=5353 web.lab.local localhost
```

---

## Probleme cu Serviciile

### Server HTTP nu răspunde

**Verificare:**
```powershell
# Verificați containerul
docker logs week10_web

# Reporniți containerul
docker restart week10_web
```

### Server SSH refuză conexiunea

**Eroare:** "Connection refused" sau "Host key verification failed"

**Soluții:**
```bash
# Verificați că serverul SSH rulează
docker logs week10_ssh

# Ștergeți vechea cheie din known_hosts
ssh-keygen -R "[localhost]:2222"

# Conectați-vă din nou
ssh -p 2222 labuser@localhost
```

### Server FTP nu acceptă conexiuni

**Verificare:**
```powershell
# Verificați porturile
docker logs week10_ftp

# Testați conexiunea
telnet localhost 2121
```

**Probleme mod pasiv:**
- Verificați că porturile 30000-30009 sunt disponibile
- Firewall-ul Windows ar putea bloca conexiunile

---

## Probleme Python

### ModuleNotFoundError

**Eroare:** `No module named 'flask'`

**Soluție:**
```powershell
# Instalați pachetele lipsă
pip install -r setup/requirements.txt

# Sau individual
pip install flask paramiko dnslib
```

### Eroare de sintaxă cu match/case

**Eroare:** `SyntaxError: invalid syntax` la declarații `match`

**Cauză:** Versiune Python < 3.10

**Soluție:**
```powershell
# Verificați versiunea
python --version

# Instalați Python 3.11+ de pe python.org
```

### SSL Certificate Verify Failed

**Soluție pentru certificate auto-semnate:**
```bash
# Cu curl
curl -k https://localhost:4443/

# Cu Python
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
```

---

## Mesaje de Eroare Comune

### "Permission denied"

**Cauze posibile:**
- Rulați fără drepturi de administrator
- Docker Desktop necesită repornire
- WSL2 necesită actualizare

### "Network is unreachable"

**Soluție:**
```powershell
# Reporniți Docker
Restart-Service docker

# Sau reporniți rețeaua
docker network rm week10_labnet
python scripts/porneste_lab.py
```

### "Image not found"

**Soluție:**
```powershell
# Construiți imaginile
docker compose -f docker/docker-compose.yml build
```

### "Container already exists"

**Soluție:**
```powershell
# Ștergeți containerul existent
docker rm -f week10_web

# Sau curățați tot
python scripts/curata.py --complet
```

---

## Instrumente Utile de Diagnosticare

### Din PowerShell/CMD

```powershell
# Starea Docker
docker info
docker system df

# Containere și log-uri
docker ps -a
docker logs <container>

# Rețele
docker network ls
docker network inspect week10_labnet

# Intrare în container
docker exec -it week10_debug /bin/sh
```

### Din containerul debug

```bash
# Teste HTTP
curl -v http://web:8000/

# Teste DNS
dig @dns-server -p 5353 web.lab.local

# Teste conectivitate
ping ssh-server
nc -zv ftp-server 2121

# Captură pachete
tcpdump -i any port 8000
```

---

## Contact și Suport

Dacă problemele persistă:

1. Verificați mesajele din consolă
2. Căutați eroarea exactă online
3. Consultați documentația Docker: https://docs.docker.com
4. Postați pe forumurile de programare

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
