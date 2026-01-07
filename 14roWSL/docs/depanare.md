# Ghid de Depanare

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix
>
> Săptămâna 14: Recapitulare Integrată și Evaluare Proiect

Acest document prezintă soluții pentru problemele frecvente întâlnite în laboratorul Săptămânii 14.

---

## Cuprins

1. [Probleme Docker](#probleme-docker)
2. [Probleme WSL2](#probleme-wsl2)
3. [Probleme de Conectivitate](#probleme-de-conectivitate)
4. [Probleme de Captură Pachete](#probleme-de-captură-pachete)
5. [Probleme de Aplicație](#probleme-de-aplicație)
6. [Probleme Python](#probleme-python)
7. [Probleme de Performanță](#probleme-de-performanță)

---

## Probleme Docker

### Daemon-ul Docker Nu Rulează

**Simptome:**
- Mesaj "Cannot connect to the Docker daemon"
- Comanda `docker info` returnează eroare

**Soluții:**
1. Verificați că Docker Desktop este pornit în system tray
2. Reporniți Docker Desktop
3. Verificați serviciul în Windows Services:
   - Apăsați Win+R, tastați `services.msc`
   - Căutați "Docker Desktop Service"
   - Asigurați-vă că este pornit

4. Reporniți WSL:
   ```powershell
   wsl --shutdown
   # Așteptați 10 secunde
   # Reporniți Docker Desktop
   ```

### Portul Este Deja Utilizat

**Simptome:**
- Eroare "bind: address already in use"
- Eroare "port is already allocated"

**Soluții:**
1. Găsiți procesul care folosește portul:
   ```powershell
   netstat -ano | findstr :8080
   ```

2. Identificați procesul după PID:
   ```powershell
   tasklist | findstr <PID>
   ```

3. Opriți procesul sau schimbați portul în `docker-compose.yml`:
   ```yaml
   ports:
     - "8081:8080"  # Folosiți alt port extern
   ```

4. Opriți containerele anterioare:
   ```powershell
   docker compose down
   python scripts/curata.py --complet
   ```

### Containerul Se Oprește Imediat

**Simptome:**
- Containerul are status "Exited"
- Eroare "Container exited with code 1"

**Soluții:**
1. Verificați log-urile containerului:
   ```bash
   docker logs week14_app1 --tail 100
   ```

2. Verificați health check-ul:
   ```bash
   docker inspect --format='{{.State.Health}}' week14_app1
   ```

3. Porniți containerul interactiv pentru debugging:
   ```bash
   docker run -it --entrypoint /bin/bash <imagine>
   ```

4. Verificați că fișierele Python nu au erori de sintaxă:
   ```powershell
   python -m py_compile src/apps/backend_server.py
   ```

### Rețeaua Nu Poate Fi Creată

**Simptome:**
- Eroare "network with name already exists"
- Eroare "failed to create network"

**Soluții:**
1. Eliminați rețeaua existentă:
   ```bash
   docker network rm week14_backend_net
   docker network rm week14_frontend_net
   ```

2. Rulați curățarea completă:
   ```powershell
   python scripts/curata.py --complet
   ```

3. Reporniți Docker Desktop

4. Verificați rețelele existente:
   ```bash
   docker network ls
   ```

---

## Probleme WSL2

### WSL2 Nu Este Disponibil

**Simptome:**
- Eroare "WSL 2 is not available"
- Docker Desktop cere WSL2

**Soluții:**
1. Instalați WSL2:
   ```powershell
   wsl --install
   ```

2. Setați versiunea implicită:
   ```powershell
   wsl --set-default-version 2
   ```

3. Verificați starea:
   ```powershell
   wsl --status
   ```

4. Activați caracteristicile Windows necesare:
   - Control Panel > Programs > Turn Windows features on or off
   - Bifați: "Virtual Machine Platform"
   - Bifați: "Windows Subsystem for Linux"

### Sistem de Fișiere Lent

**Simptome:**
- Operațiunile cu fișiere sunt foarte lente
- Docker build durează foarte mult

**Soluții:**
1. Mutați proiectul în sistemul de fișiere Linux:
   ```bash
   # În WSL
   cp -r /mnt/c/Users/nume/proiect ~/proiect
   cd ~/proiect
   ```

2. Evitați accesul la `/mnt/c/` din containere

3. Folosiți volume Docker în loc de bind mounts pentru date temporare

---

## Probleme de Conectivitate

### Nu Pot Accesa Containerele

**Simptome:**
- `curl localhost:8080` returnează "Connection refused"
- Serviciile nu răspund

**Soluții:**
1. Verificați că containerele rulează:
   ```bash
   docker ps
   ```

2. Verificați health check-urile:
   ```bash
   docker inspect week14_lb --format='{{.State.Health.Status}}'
   ```

3. Verificați maparea porturilor:
   ```bash
   docker port week14_lb
   ```

4. Testați din interiorul containerului:
   ```bash
   docker exec week14_client curl http://lb:8080/
   ```

5. Verificați firewall-ul Windows:
   - Permiteți Docker Desktop în Windows Firewall

### Containerele Nu Comunică Între Ele

**Simptome:**
- Eroare "Name or service not known"
- Ping între containere eșuează

**Soluții:**
1. Verificați că sunt în aceeași rețea:
   ```bash
   docker network inspect week14_backend_net
   ```

2. Verificați rezoluția DNS:
   ```bash
   docker exec week14_client nslookup app1
   ```

3. Verificați conectivitatea:
   ```bash
   docker exec week14_client ping -c 3 app1
   ```

4. Reporniți containerele:
   ```powershell
   python scripts/opreste_lab.py
   python scripts/porneste_lab.py
   ```

### Health Check-urile Eșuează

**Simptome:**
- Container în starea "unhealthy"
- Load balancer nu rutează cereri

**Soluții:**
1. Verificați endpoint-ul de sănătate:
   ```bash
   docker exec week14_app1 curl http://localhost:8001/health
   ```

2. Verificați log-urile pentru erori:
   ```bash
   docker logs week14_app1
   ```

3. Verificați configurația health check în docker-compose.yml

4. Măriți intervalul și timeout-ul health check-ului

---

## Probleme de Captură Pachete

### Wireshark Nu Vede Traficul Docker

**Simptome:**
- Nu apare trafic în captură
- Interfața docker nu este vizibilă

**Soluții:**
1. Selectați interfața corectă în Wireshark:
   - Pe Windows: "Local Area Connection" sau adaptorul vEthernet

2. Folosiți tcpdump din interiorul containerului:
   ```bash
   docker exec week14_client tcpdump -i any -w /app/captura.pcap
   ```

3. Capturați pe porturile expuse:
   ```bash
   tshark -i any -f "port 8080 or port 8001 or port 8002"
   ```

### tshark Nu Este Găsit

**Simptome:**
- Eroare "tshark: command not found"
- Scriptul de captură eșuează

**Soluții:**
1. Instalați Wireshark complet (include tshark)

2. Adăugați Wireshark la PATH:
   ```powershell
   $env:PATH += ";C:\Program Files\Wireshark"
   ```

3. Folosiți calea completă:
   ```powershell
   & "C:\Program Files\Wireshark\tshark.exe" -v
   ```

---

## Probleme de Aplicație

### Load Balancer-ul Trimite Doar Către Un Backend

**Simptome:**
- Toate cererile merg la același backend
- Distribuția nu este echilibrată

**Soluții:**
1. Verificați că ambele backend-uri sunt sănătoase:
   ```bash
   curl http://localhost:8080/status
   ```

2. Verificați starea individuală:
   ```bash
   curl http://localhost:8001/health
   curl http://localhost:8002/health
   ```

3. Reporniți load balancer-ul:
   ```bash
   docker restart week14_lb
   ```

4. Verificați log-urile pentru erori:
   ```bash
   docker logs week14_lb
   ```

### Serverul Echo Nu Răspunde

**Simptome:**
- Timeout la conectare
- Conexiune refuzată

**Soluții:**
1. Verificați că serverul rulează:
   ```bash
   docker ps | grep echo
   ```

2. Testați din container:
   ```bash
   docker exec week14_client nc -v echo 9000
   ```

3. Verificați log-urile:
   ```bash
   docker logs week14_echo
   ```

4. Reporniți serviciul:
   ```bash
   docker restart week14_echo
   ```

---

## Probleme Python

### Modul Negăsit

**Simptome:**
- Eroare "ModuleNotFoundError: No module named 'xyz'"

**Soluții:**
1. Instalați pachetele lipsă:
   ```powershell
   pip install -r setup/requirements.txt
   ```

2. Verificați mediul virtual (dacă folosiți unul):
   ```powershell
   # Activați mediul virtual
   .\venv\Scripts\Activate
   pip install -r setup/requirements.txt
   ```

3. Verificați că folosiți Python corect:
   ```powershell
   python --version
   python -m pip list
   ```

### Versiune Python Incompatibilă

**Simptome:**
- Erori de sintaxă pentru cod valid
- Funcții moderne nu sunt recunoscute

**Soluții:**
1. Verificați versiunea Python:
   ```powershell
   python --version
   ```

2. Instalați Python 3.11+:
   - Descărcați de pe python.org
   - Bifați "Add to PATH" la instalare

3. Folosiți `py` launcher pe Windows:
   ```powershell
   py -3.11 scripts/porneste_lab.py
   ```

---

## Probleme de Performanță

### Pornire Lentă

**Simptome:**
- Containerele durează mult să pornească
- Docker build foarte lent

**Soluții:**
1. Verificați resursele alocate Docker Desktop:
   - Settings > Resources > Advanced
   - Creșteți memoria la 4-8 GB
   - Creșteți CPU-urile la 2-4

2. Folosiți cache pentru build:
   ```bash
   # Nu folosiți --no-cache decât când e necesar
   docker compose build
   ```

3. Opriți antivirusul pentru directorul Docker

4. Mutați fișierele în sistemul de fișiere Linux (WSL)

### Utilizare CPU Ridicată

**Simptome:**
- Docker Desktop consumă mult CPU
- Ventilatoarele pornesc constant

**Soluții:**
1. Limitați resursele containerelor în docker-compose.yml:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.5'
         memory: 256M
   ```

2. Opriți containerele neutilizate:
   ```powershell
   python scripts/opreste_lab.py
   ```

3. Curățați resursele Docker neutilizate:
   ```bash
   docker system prune
   ```

---

## Diagnostic Rapid

### Lista de Verificare

Când ceva nu funcționează, verificați în ordine:

1. ✓ Docker Desktop rulează?
2. ✓ Containerele sunt pornite? (`docker ps`)
3. ✓ Health check-urile trec? (`docker inspect`)
4. ✓ Porturile sunt libere? (`netstat -ano | findstr :PORT`)
5. ✓ Rețelele există? (`docker network ls`)
6. ✓ Log-urile arată erori? (`docker logs <container>`)

### Comandă de Diagnostic Complet

```powershell
# Rulați pentru a vedea starea completă
docker ps -a
docker network ls
docker system df
python scripts/porneste_lab.py --status
```

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
