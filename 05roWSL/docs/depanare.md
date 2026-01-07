# Ghid de Depanare – Săptămâna 5

> Laborator Rețele de Calculatoare – ASE, Informatică Economică
> realizat de Revolvix

## Probleme Frecvente și Soluții

### 1. Docker

#### Problemă: Docker Desktop nu pornește

**Simptome:**
- Pictograma Docker rămâne în starea "Starting..."
- Mesaj "Docker Desktop is starting..."

**Soluții:**
1. Reporniți Docker Desktop
2. Verificați că WSL2 este instalat și actualizat:
   ```powershell
   wsl --update
   ```
3. Verificați virtualizarea în BIOS (trebuie activată)
4. Reinstalați Docker Desktop

#### Problemă: Containerele nu pornesc

**Simptome:**
- `docker compose up` afișează erori
- Containerele sunt în starea "Exited"

**Soluții:**
1. Verificați jurnalele:
   ```powershell
   docker compose -f docker/docker-compose.yml logs
   ```
2. Verificați că porturile nu sunt ocupate:
   ```powershell
   netstat -an | findstr 9999
   ```
3. Reconstruiți imaginile:
   ```powershell
   docker compose -f docker/docker-compose.yml build --no-cache
   ```

#### Problemă: Eroare "network not found"

**Simptome:**
- Mesaj despre rețea inexistentă

**Soluții:**
```powershell
# Eliminați rețelele vechi
docker network prune

# Recreați
docker compose -f docker/docker-compose.yml up -d
```

### 2. Python

#### Problemă: ModuleNotFoundError

**Simptome:**
- `ModuleNotFoundError: No module named 'src'`

**Soluții:**
1. Rulați din directorul rădăcină al kitului:
   ```powershell
   cd WEEK5_WSLkit_RO
   python src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.10.14/26
   ```

2. Setați PYTHONPATH:
   ```powershell
   $env:PYTHONPATH = "."
   python src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.10.14/26
   ```

#### Problemă: Versiune Python incompatibilă

**Simptome:**
- Erori de sintaxă sau funcții lipsă

**Soluții:**
1. Verificați versiunea:
   ```powershell
   python --version
   ```
2. Dacă aveți mai multe versiuni, specificați explicit:
   ```powershell
   py -3.11 src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.10.14/26
   ```

### 3. Conectivitate Rețea

#### Problemă: Containerele nu comunică între ele

**Simptome:**
- `ping` între containere eșuează
- Conexiuni UDP respinse

**Soluții:**
1. Verificați că toate containerele sunt pe aceeași rețea:
   ```powershell
   docker network inspect week5_labnet
   ```

2. Verificați adresele IP:
   ```powershell
   docker exec week5_python ip addr
   docker exec week5_udp-server ip addr
   ```

3. Testați conectivitatea din container:
   ```powershell
   docker exec week5_python ping -c 3 10.5.0.20
   ```

#### Problemă: Nu se poate accesa Portainer

**Simptome:**
- https://localhost:9443 nu răspunde

**Soluții:**
1. Verificați că portul este disponibil:
   ```powershell
   netstat -an | findstr 9443
   ```

2. Încercați cu HTTP în loc de HTTPS (dacă certificatul nu este configurat)

3. Verificați firewall-ul Windows

### 4. Captură de Pachete

#### Problemă: tcpdump nu funcționează

**Simptome:**
- Eroare de permisiuni
- "Operation not permitted"

**Soluții:**
1. Verificați că containerul are capabilitățile necesare:
   ```yaml
   cap_add:
     - NET_ADMIN
     - NET_RAW
   ```

2. Reporniți containerele după modificarea docker-compose.yml

#### Problemă: Wireshark nu vede interfețele

**Simptome:**
- Lista de interfețe este goală

**Soluții:**
1. Instalați Npcap (vine cu Wireshark)
2. Rulați Wireshark ca Administrator
3. Reinstalați Wireshark cu opțiunea "Install Npcap"

### 5. WSL2

#### Problemă: WSL nu pornește

**Simptome:**
- Eroare la comanda `wsl`
- Docker raportează probleme cu backend-ul

**Soluții:**
1. Actualizați WSL:
   ```powershell
   wsl --update
   ```

2. Setați versiunea implicită:
   ```powershell
   wsl --set-default-version 2
   ```

3. Reporniți serviciul WSL:
   ```powershell
   wsl --shutdown
   ```

### 6. Erori de Calcul

#### Problemă: Rezultate CIDR incorecte

**Verificare:**
- Asigurați-vă că folosiți prefixul corect
- Verificați că adresa de intrare este validă

**Exemplu corect:**
```
192.168.10.14/26
- Adresa de rețea: 192.168.10.0 (NU 192.168.10.14)
- Broadcast: 192.168.10.63
- Gazde: 62 (NU 64)
```

#### Problemă: VLSM nu alocă suficiente adrese

**Verificare:**
- Asigurați-vă că rețeaua de bază este suficient de mare
- Verificați suma cerințelor vs. spațiul disponibil

## Comenzi de Diagnosticare

### Verificare Generală

```powershell
# Stare Docker
docker info

# Stare containere
docker ps -a

# Utilizare resurse
docker stats --no-stream

# Spațiu disc Docker
docker system df
```

### Verificare Rețea

```powershell
# Listează rețelele Docker
docker network ls

# Detalii rețea
docker network inspect week5_labnet

# Conectivitate
docker exec week5_python ping -c 1 10.5.0.20
```

### Verificare Jurnale

```powershell
# Jurnale toate serviciile
docker compose -f docker/docker-compose.yml logs

# Jurnale serviciu specific
docker compose -f docker/docker-compose.yml logs python

# Ultimele 50 linii
docker logs --tail 50 week5_python
```

## Resetare Completă

Dacă nimic nu funcționează, efectuați o resetare completă:

```powershell
# 1. Opriți totul
docker compose -f docker/docker-compose.yml down -v

# 2. Eliminați resursele week5
docker rm -f $(docker ps -aq --filter "name=week5")
docker network rm week5_labnet
docker volume rm $(docker volume ls -q --filter "name=week5")

# 3. Curățați sistemul
docker system prune -f

# 4. Reporniți
docker compose -f docker/docker-compose.yml up -d --build
```

## Obținere Ajutor

Dacă problema persistă:

1. **Verificați documentația**: Consultați README.md și docs/
2. **Colectați informații**:
   - Versiunea Python (`python --version`)
   - Versiunea Docker (`docker --version`)
   - Mesajele de eroare complete
   - Sistemul de operare

3. **Contactați asistentul de laborator** cu informațiile colectate

---

*Material didactic pentru Laborator Rețele de Calculatoare – ASE Bucuresti*
