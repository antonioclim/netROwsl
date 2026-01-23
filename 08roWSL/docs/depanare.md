# Ghid de Depanare — Săptămâna 8

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix
>
> **Vezi și:** [README principal](../README.md) | [Rezumat teoretic](rezumat_teoretic.md) | [Fișa de comenzi](fisa_comenzi.md)

---

## 🚨 Diagnostic Rapid

Înainte de a căuta problema specifică, rulează aceste comenzi pentru diagnostic:

```bash
# 1. Docker rulează?
docker ps

# 2. Containerele laboratorului sunt pornite?
docker ps --filter "name=week8"

# 3. Porturile sunt disponibile?
sudo ss -tlnp | grep -E "8080|8443|9000"

# 4. nginx răspunde?
curl -I http://localhost:8080/
```

**🔮 PREDICȚIE:** Ce output aștepți de la fiecare comandă dacă totul funcționează corect?

---

## Probleme Docker

### Docker daemon nu pornește

**Simptome:**
- Eroare "Cannot connect to the Docker daemon"
- `docker ps` returnează eroare

**Soluții:**

```bash
# Pornește serviciul Docker în WSL
sudo service docker start
# Parolă: stud

# Verifică statusul
sudo service docker status

# Dacă încă nu merge, verifică log-urile
sudo cat /var/log/docker.log | tail -20
```

**🔮 PREDICȚIE:** După `sudo service docker start`, ce mesaj aștepți să vezi?

### Permisiune refuzată la rularea docker

**Simptome:**
- Eroare "permission denied while trying to connect to the Docker daemon socket"

**Soluții:**

```bash
# Adaugă utilizatorul la grupul docker
sudo usermod -aG docker $USER

# Aplică modificările (alege una din opțiuni):
# Opțiunea 1: Activează grupul în sesiunea curentă
newgrp docker

# Opțiunea 2: Deconectează-te și reconectează-te
exit
wsl
```

### Portul 8080 este ocupat

**Simptome:**
- Eroare "Bind for 0.0.0.0:8080 failed: port is already allocated"

**Soluții:**

```bash
# Identifică procesul care folosește portul
sudo ss -tlnp | grep 8080

# Sau în Windows PowerShell:
netstat -ano | findstr :8080

# Oprește procesul sau schimbă portul în docker-compose.yml
```

### Containerele nu pornesc

**Simptome:**
- Eroare la `docker compose up`
- Containere în starea "Exited"

**Soluții:**

```bash
# Verifică jurnalele pentru erori specifice
docker logs week8-nginx-proxy
docker logs week8-backend-1

# Reconstruiește imaginile
docker compose build --no-cache

# Curățare completă și repornire
python3 scripts/curatare.py --complet
python3 scripts/porneste_laborator.py
```

---

## Probleme Portainer

### Nu pot accesa http://localhost:9000

**Simptome:**
- Browser afișează "Connection refused" sau "This site can't be reached"

**Soluții:**

```bash
# Verifică dacă containerul Portainer există și rulează
docker ps -a | grep portainer

# Dacă e oprit, pornește-l
docker start portainer

# Dacă nu există, creează-l
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest

# Verifică log-urile
docker logs portainer
```

### Am uitat parola Portainer

**⚠️ ATENȚIE:** Aceasta resetează Portainer (pierde setările dar NU containerele)

```bash
docker stop portainer
docker rm portainer
docker volume rm portainer_data

# Recreează cu comanda de mai sus
# La prima accesare, setează parola nouă: studstudstud
```

---

## Probleme de Conectivitate

### localhost:8080 nu este accesibil

**Simptome:**
- Browser afișează "Connection refused"
- curl returnează eroare de conectare

**🔮 PREDICȚIE:** Care dintre următoarele comenzi va ajuta să identifici problema?

**Soluții:**

```bash
# 1. Verifică că containerele rulează
docker ps

# 2. Verifică porturile
docker compose ps

# 3. Testează conectivitatea verbose
curl -v http://localhost:8080/

# 4. Verifică rețeaua Docker
docker network inspect week8-laboratory-network
```

### nginx returnează 502 Bad Gateway

**Cauze posibile:**
- Backend-urile nu rulează
- Configurație nginx incorectă
- Probleme de rețea internă

**Soluții:**

```bash
# 1. Verifică starea backend-urilor
docker ps | grep backend

# 2. Verifică configurația nginx
docker exec week8-nginx-proxy nginx -t

# 3. Consultă jurnalele nginx
docker logs week8-nginx-proxy --tail 50

# 4. Testează direct un backend
docker exec week8-nginx-proxy curl http://backend1:8080/health
```

### Backend-urile nu răspund

**Simptome:**
- nginx returnează 502 Bad Gateway
- Cererile expiră

**Soluții:**

```bash
# Verifică fiecare backend individual
docker exec week8-nginx-proxy curl http://backend1:8080/health
docker exec week8-nginx-proxy curl http://backend2:8080/health
docker exec week8-nginx-proxy curl http://backend3:8080/health

# Verifică log-urile backend-urilor
docker logs week8-backend-1 --tail 20
docker logs week8-backend-2 --tail 20
docker logs week8-backend-3 --tail 20

# Repornește backend-urile
docker restart week8-backend-1 week8-backend-2 week8-backend-3
```

### Echilibrarea nu funcționează corect

**Simptome:**
- Toate cererile merg la același backend
- Distribuție neuniformă

**Soluții:**

```bash
# Testează distribuția manual
for i in {1..9}; do
  echo "Cerere $i:"
  curl -s http://localhost:8080/ | grep -o "Backend-[A-Za-z]*"
done
```

**🔮 PREDICȚIE:** Pentru 9 cereri cu round-robin și 3 backend-uri, ce distribuție aștepți?
(Hint: fiecare backend ar trebui să primească exact 3 cereri)

---

## Probleme Wireshark

### Nu se capturează pachete

**Simptome:**
- Wireshark nu afișează trafic
- Lista de pachete este goală

**Verificări:**
- ✅ Interfața corectă selectată? → `vEthernet (WSL)`
- ✅ Traficul este generat ÎN TIMPUL capturii?
- ✅ Filtrul de afișare nu ascunde pachetele? (șterge filtrul temporar)
- ✅ Modul promiscuous activat? → Capture → Options → bifează

**🔮 PREDICȚIE:** Dacă selectezi interfața greșită (Ethernet în loc de vEthernet WSL), 
vei vedea pachetele de la containerele Docker?

### Erori de permisiune Wireshark

**Simptome:**
- "You don't have permission to capture"

**Soluții:**
- Pe Windows: rulează Wireshark ca Administrator (click dreapta → Run as administrator)
- Reinstalează Npcap cu opțiunea "WinPcap API-compatible Mode" bifată

---

## Probleme cu Scripturile Python

### ModuleNotFoundError

**Simptome:**
- Eroare "No module named 'docker'" sau similar

**Soluții:**

```bash
# Instalează dependențele
pip install -r setup/requirements.txt --break-system-packages

# Verifică instalarea
pip list | grep docker
```

### Permisiuni insuficiente

**Simptome:**
- Eroare "Permission denied"

**Soluții:**
- Pe Windows, rulează PowerShell ca Administrator
- În WSL, folosește `sudo` dacă e necesar
- Verifică permisiunile fișierelor: `ls -la scripts/`

---

## Comenzi de Recuperare

### Resetare completă

```bash
# Oprește toate containerele week8
docker stop $(docker ps -q --filter "name=week8")

# Elimină containerele week8
docker rm $(docker ps -aq --filter "name=week8")

# Elimină rețelele week8
docker network rm $(docker network ls -q --filter "name=week8")

# Elimină volumele week8
docker volume rm $(docker volume ls -q --filter "name=week8")

# Pornire curată
python3 scripts/porneste_laborator.py --reconstruieste
```

### Repornire rapidă

```bash
python3 scripts/opreste_laborator.py
python3 scripts/porneste_laborator.py
```

### Verificare post-curățare

```bash
# Ce ar trebui să rămână:
docker ps        # Doar: portainer
docker images    # Imaginile descărcate
docker network ls  # bridge, host, none (implicite)
docker volume ls   # portainer_data
```

---

## Tabel Rapid de Referință

| Problemă | Comandă de Diagnostic | Soluție Rapidă |
|----------|----------------------|----------------|
| Docker nu merge | `sudo service docker status` | `sudo service docker start` |
| Portainer nu răspunde | `docker ps -a \| grep portainer` | `docker start portainer` |
| nginx 502 | `docker logs week8-nginx-proxy` | `docker restart week8-backend-*` |
| Port ocupat | `sudo ss -tlnp \| grep 8080` | Oprește procesul sau schimbă portul |
| Wireshark gol | Verifică interfața | Selectează `vEthernet (WSL)` |

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
