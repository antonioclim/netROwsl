# Ghid de Depanare

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Probleme Docker

### Docker Desktop nu pornește

**Simptome:**
- Eroare "Cannot connect to the Docker daemon"
- Aplicația Docker Desktop nu răspunde

**Soluții:**

1. Reporniți Docker Desktop din meniul Start Windows
2. Așteptați 1-2 minute pentru inițializarea completă
3. Verificați că WSL2 este activat:
   ```powershell
   wsl --status
   ```
4. Dacă persistă, reporniți computerul

### Backend WSL2 nu funcționează

**Simptome:**
- Docker Desktop afișează eroare WSL2
- Containerele nu pornesc

**Soluții:**

1. Actualizați kernel-ul WSL2:
   ```powershell
   wsl --update
   ```

2. Setați versiunea WSL2 ca implicită:
   ```powershell
   wsl --set-default-version 2
   ```

3. Reporniți serviciul WSL:
   ```powershell
   wsl --shutdown
   ```

### Portul 8080 este ocupat

**Simptome:**
- Eroare "Bind for 0.0.0.0:8080 failed: port is already allocated"

**Soluții:**

1. Identificați procesul care folosește portul:
   ```powershell
   netstat -ano | findstr :8080
   ```

2. Opriți procesul:
   ```powershell
   taskkill /PID <pid> /F
   ```

3. Sau modificați portul în `docker-compose.yml`:
   ```yaml
   ports:
     - "8081:80"  # Schimbat de la 8080
   ```

### Containerele nu pornesc

**Simptome:**
- Eroare la `docker compose up`
- Containere în starea "Exited"

**Soluții:**

1. Verificați jurnalele:
   ```bash
   docker logs week8-nginx-1
   docker logs week8-backend1-1
   ```

2. Reconstruiți imaginile:
   ```bash
   docker compose build --no-cache
   ```

3. Curățare completă și repornire:
   ```bash
   python scripts/curatare.py --complet
   python scripts/porneste_laborator.py
   ```

## Probleme de Conectivitate

### localhost:8080 nu este accesibil

**Simptome:**
- Browser afișează "Connection refused"
- curl returnează eroare de conectare

**Soluții:**

1. Verificați că containerele rulează:
   ```bash
   docker ps
   ```

2. Verificați porturile:
   ```bash
   docker compose ps
   ```

3. Testați conectivitatea:
   ```bash
   curl -v http://localhost:8080/
   ```

### Backend-urile nu răspund

**Simptome:**
- nginx returnează 502 Bad Gateway
- Cererile expire

**Soluții:**

1. Verificați starea backend-urilor:
   ```bash
   docker exec week8-nginx-1 curl http://backend1:8080/health
   ```

2. Verificați rețeaua Docker:
   ```bash
   docker network inspect week8-laboratory-network
   ```

3. Reporniți backend-urile:
   ```bash
   docker restart week8-backend1-1 week8-backend2-1 week8-backend3-1
   ```

### Rezoluție DNS în containere

**Simptome:**
- Containerele nu pot comunica după nume
- Erori "Name or service not known"

**Soluții:**

1. Verificați că containerele sunt în aceeași rețea:
   ```bash
   docker network inspect week8-laboratory-network
   ```

2. Testați rezoluția DNS:
   ```bash
   docker exec week8-nginx-1 nslookup backend1
   ```

## Probleme HTTP/Proxy

### Eroare 502 Bad Gateway

**Cauze posibile:**
- Backend-urile nu rulează
- Configurație nginx incorectă
- Probleme de rețea internă

**Soluții:**

1. Verificați starea backend-urilor
2. Verificați configurația nginx:
   ```bash
   docker exec week8-nginx-1 nginx -t
   ```
3. Consultați jurnalele nginx:
   ```bash
   docker logs week8-nginx-1 --tail 50
   ```

### Eroare 504 Gateway Timeout

**Cauze posibile:**
- Backend-urile răspund prea lent
- Timeout configurat prea scurt

**Soluții:**

1. Măriți timeout-ul în configurația nginx
2. Verificați performanța backend-urilor
3. Verificați resursele containerelor:
   ```bash
   docker stats
   ```

### Echilibrarea nu funcționează corect

**Simptome:**
- Toate cererile merg la același backend
- Distribuție neuniformă

**Soluții:**

1. Verificați configurația upstream în nginx
2. Asigurați-vă că toate backend-urile sunt sănătoase
3. Testați fiecare backend individual:
   ```bash
   docker exec week8-nginx-1 curl http://backend1:8080/health
   docker exec week8-nginx-1 curl http://backend2:8080/health
   docker exec week8-nginx-1 curl http://backend3:8080/health
   ```

## Probleme cu Scripturile Python

### ModuleNotFoundError

**Simptome:**
- Eroare "No module named 'docker'" sau similar

**Soluții:**

1. Instalați dependențele:
   ```bash
   pip install -r setup/requirements.txt --break-system-packages
   ```

2. Verificați instalarea:
   ```bash
   pip list | grep docker
   ```

### Permisiuni insuficiente

**Simptome:**
- Eroare "Permission denied"

**Soluții:**

1. Pe Windows, rulați PowerShell ca Administrator
2. Verificați permisiunile fișierelor
3. Asigurați-vă că Docker Desktop rulează

## Probleme Wireshark

### Nu se capturează pachete

**Simptome:**
- Wireshark nu afișează trafic
- Lista de pachete este goală

**Soluții:**

1. Selectați interfața corectă:
   - Pentru localhost: "Loopback: lo" sau "Adapter for loopback"
   
2. Verificați filtrul de captură:
   - Folosiți: `port 8080`
   
3. Generați trafic în timpul capturii:
   ```bash
   curl http://localhost:8080/
   ```

### Erori de permisiune Wireshark

**Simptome:**
- "You don't have permission to capture"

**Soluții:**

1. Pe Windows: rulați Wireshark ca Administrator
2. Pe Linux: adăugați utilizatorul la grupul wireshark:
   ```bash
   sudo usermod -aG wireshark $USER
   ```

## Probleme de Performanță

### Pornire lentă

**Cauze posibile:**
- Resurse insuficiente
- Imagini Docker mari

**Soluții:**

1. Alocați mai multe resurse în Docker Desktop Settings
2. Curățați imaginile nefolosite:
   ```bash
   docker system prune -a
   ```

### Utilizare mare de memorie

**Soluții:**

1. Limitați resursele în docker-compose.yml:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 256M
   ```

2. Opriți containerele când nu le folosiți:
   ```bash
   python scripts/opreste_laborator.py
   ```

## Comenzi de Recuperare

### Resetare completă

```bash
# Oprire toate containerele
docker stop $(docker ps -aq)

# Eliminare containere week8
docker rm $(docker ps -aq --filter "name=week8")

# Eliminare rețele week8
docker network rm $(docker network ls -q --filter "name=week8")

# Eliminare volume week8
docker volume rm $(docker volume ls -q --filter "name=week8")

# Pornire curată
python scripts/porneste_laborator.py --reconstruieste
```

### Repornire rapidă

```bash
python scripts/opreste_laborator.py
python scripts/porneste_laborator.py
```

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
