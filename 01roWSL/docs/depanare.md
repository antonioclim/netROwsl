# Ghid de Depanare - Săptămâna 1

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Aici găsești soluții pentru cele mai frecvente probleme. Dacă ceva nu merge, verifică mai întâi lista de aici înainte de a cere ajutor — sunt șanse mari să fie o problemă cunoscută.

---

## Probleme Docker

### Docker Desktop nu pornește

**Simptome:**
- Aplicația Docker Desktop nu răspunde
- Pictograma rămâne gri sau roșie
- Mesaj "Docker Desktop is starting..." care nu dispare

**Ce să încerci:**

1. **Verifică virtualizarea** (fără asta, nimic nu merge):
   ```powershell
   systeminfo | findstr /i "Hyper-V"
   # Trebuie să vezi "Virtualization Enabled In Firmware: Yes"
   ```

2. **Repornește serviciile Docker:**
   ```powershell
   # PowerShell ca Administrator
   Restart-Service docker
   Restart-Service com.docker.service
   ```

3. **Resetare completă** (ultima soluție — pierzi imaginile locale):
   - Închide Docker Desktop
   - Șterge: `%APPDATA%\Docker\`
   - Repornește Docker Desktop

💡 **Sfat:** 90% din probleme sunt la punctul 1. Verifică în BIOS că virtualizarea e pornită!

---

### Eroare "Cannot connect to Docker daemon"

**Simptome:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
Is the docker daemon running?
```

**Cauza:** Docker daemon-ul nu rulează. În WSL2, trebuie pornit manual după fiecare restart Windows.

**Soluție rapidă:**
```bash
sudo service docker start
# Parolă: stud
```

Dacă tot nu merge, verifică integrarea WSL2:
```powershell
wsl --list --verbose
# Ar trebui să vezi docker-desktop și docker-desktop-data
```

---

### Eroare la construirea imaginilor

**Simptome:**
```
ERROR: failed to solve: python:3.12-slim: failed to resolve source metadata
```

**Ce să încerci (în ordinea asta):**

1. **Verifică internetul:**
   ```bash
   ping -c 2 hub.docker.com
   ```

2. **Curăță cache-ul:**
   ```bash
   docker system prune -a
   docker builder prune
   ```

3. **Reconstruiește fără cache:**
   ```bash
   docker compose build --no-cache
   ```

De obicei e o problemă temporară de rețea — încearcă din nou după 5 minute.

---

### Spațiu pe disc insuficient

**Simptome:**
```
no space left on device
```

**Soluția e simplă:**
```bash
# Vezi cât ocupă Docker
docker system df

# Curăță tot ce nu folosești (containere oprite, imagini vechi)
docker system prune -a --volumes
```

⚠️ **Atenție:** Comanda de sus șterge și volume-urile neutilizate. Dacă ai date importante în volume, omite `--volumes`.

---

## Probleme de Rețea

### "Address already in use"

**Simptome:**
```
OSError: [Errno 98] Address already in use
Bind for 0.0.0.0:9090 failed: port is already allocated
```

**Cauza:** Altcineva folosește deja portul. Poate un container vechi, poate alt proces.

**Soluție:**

1. **Găsește cine folosește portul:**
   ```bash
   # În Linux/WSL
   ss -tlnp | grep :9090
   
   # În Windows PowerShell
   netstat -ano | findstr :9090
   ```

2. **Oprește-l:**
   ```bash
   # Linux - cu PID-ul găsit mai sus
   kill <PID>
   
   # Sau dacă e container Docker
   docker stop <container_id>
   ```

---

### "Connection refused"

**Simptome:**
```
Connection refused
nc: connect to localhost port 9090 (tcp) failed: Connection refused
```

**Cauze posibile (și soluții):**

| Cauză | Cum verifici | Soluție |
|-------|-------------|---------|
| Serverul nu rulează | `ss -tlnp \| grep :9090` | Pornește serverul |
| Port greșit | Verifică documentația | Folosește portul corect |
| Bind pe 127.0.0.1 | `ss -tlnp` arată doar 127.0.0.1 | Schimbă la 0.0.0.0 |

---

### Ping nu funcționează

**Simptome:**
```
ping: connect: Network is unreachable
Destination Host Unreachable
Request timed out
```

**Diagnostic rapid:**
```bash
# 1. Ai interfață configurată?
ip -br addr show

# 2. Ai rută către destinație?
ip route get 8.8.8.8

# 3. DNS funcționează?
nslookup google.com
```

Dacă ești în container și nu merge ping-ul extern, verifică că rețeaua Docker există:
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

**Soluție rapidă:** Testează cu DNS public
```bash
nslookup google.com 8.8.8.8
```

Dacă merge cu 8.8.8.8 dar nu fără, problema e în `/etc/resolv.conf`:
```bash
# Fix temporar
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

---

## Probleme Specifice Laboratorului Săptămânii 1

### Container week1_lab nu pornește

**Simptome:**
```
docker compose up -d
Error response from daemon: Conflict. Container name "/week1_lab" already in use
```

**Cauza:** Un container vechi cu același nume există deja (probabil oprit, nu șters).

**Soluție:**
```bash
# Șterge containerul vechi
docker rm -f week1_lab

# Apoi repornește
docker compose up -d
```

---

### Wireshark nu vede traficul containerelor

**Simptome:**
- Captura pe `vEthernet (WSL)` e goală
- Filtrul `tcp.port == 9090` nu arată nimic

**Cauze și soluții:**

1. **Traficul e pe loopback** (127.0.0.1 → 127.0.0.1)
   
   Wireshark din Windows nu vede loopback-ul containerului. Soluție: capturează din container:
   ```bash
   docker exec -it week1_lab tcpdump -i lo -w /work/pcap/captura.pcap port 9090
   ```

2. **Captura a pornit DUPĂ trafic**
   
   Pornește captura ÎNAINTE de a genera trafic. Ordinea contează!

3. **Interfața greșită**
   
   Pentru trafic între containere: `vEthernet (WSL)` sau `any`
   Pentru loopback în container: capturează cu tcpdump din container

---

### Python: ModuleNotFoundError

**Simptome:**
```
ModuleNotFoundError: No module named 'scapy'
```

**Context:** Pachetele Python sunt instalate în container, nu în WSL.

**Soluții:**

```bash
# Opțiunea 1: Rulează scriptul ÎN container (recomandat)
docker exec -it week1_lab python3 /work/src/exercises/script.py

# Opțiunea 2: Instalează în WSL (dacă chiar ai nevoie)
pip install scapy --break-system-packages
```

---

### Fișierul PCAP apare gol sau corupt

**Simptome:**
- Wireshark spune că fișierul nu e valid
- `tshark -r captura.pcap` dă eroare

**Cauze comune:**

1. **tcpdump oprit prea devreme** — așteaptă să se genereze trafic înainte de Ctrl+C

2. **Permisiuni** — verifică că poți scrie în folder:
   ```bash
   ls -la /work/pcap/
   ```

3. **Proces tcpdump zombie** — omoară-l și încearcă din nou:
   ```bash
   pkill -9 tcpdump
   ```

**Captură corectă:**
```bash
# -U = scrie imediat în fișier (nu bufferează)
tcpdump -i lo -w /work/pcap/captura.pcap -U port 9090
```

---

## Probleme Python

### "Permission denied" pentru socket

**Simptome:**
```
PermissionError: [Errno 13] Permission denied
```

**Cauza:** Porturi sub 1024 necesită root.

**Soluții:**
```bash
# Opțiunea 1: Folosește port > 1024 (recomandat)
# Schimbă PORT = 80 în PORT = 8080

# Opțiunea 2: Rulează cu sudo (nu recomandat pentru producție)
sudo python3 script.py
```

---

### Socket-ul Docker nu e accesibil

**Simptome:**
```
docker.errors.DockerException: Error while fetching server API version
```

**Soluție:**
```bash
# Adaugă userul la grupul docker
sudo usermod -aG docker $USER

# IMPORTANT: trebuie să te reloghezi după
exit
# Apoi deschide un terminal nou
```

---

## Probleme cu Captura de Trafic

### tcpdump: permission denied

**Simptome:**
```
tcpdump: eth0: You don't have permission to capture on that device
```

**Soluții:**

1. **În container Docker:** Verifică că ai capabilitățile necesare în docker-compose.yml:
   ```yaml
   cap_add:
     - NET_ADMIN
     - NET_RAW
   ```

2. **În WSL:** Rulează cu sudo:
   ```bash
   sudo tcpdump -i eth0
   ```

---

### tcpdump rulează dar nu afișează nimic

**Checklist rapid:**

1. **Interfața corectă?**
   ```bash
   tcpdump -D  # Listează interfețele disponibile
   ```

2. **Filtrul prea restrictiv?** Încearcă fără filtru:
   ```bash
   tcpdump -i any -c 10
   ```

3. **Chiar există trafic?** Generează ceva:
   ```bash
   ping -c 3 127.0.0.1
   ```

---

## Probleme WSL2

### WSL2 nu e instalat

**Simptome:**
```
WSL 2 is not installed
```

**Soluție:**
```powershell
# PowerShell ca Administrator
wsl --install
# Repornește calculatorul
```

---

### Probleme de rețea în WSL2

**Simptome:**
- Nu merge internetul din WSL
- DNS nu funcționează

**Soluții în ordinea probabilității:**

1. **Repornește WSL:**
   ```powershell
   wsl --shutdown
   # Așteaptă 10 secunde, apoi deschide Ubuntu din nou
   ```

2. **Fixează DNS-ul:**
   ```bash
   sudo rm /etc/resolv.conf
   echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
   ```

3. **Dezactivează generarea automată** (fix permanent):
   ```bash
   sudo bash -c 'echo "[network]
   generateResolvConf = false" > /etc/wsl.conf'
   ```
   Apoi `wsl --shutdown` și repornește.

---

## Diagnostic Rapid — Script All-in-One

Rulează asta când ceva nu merge și nu știi de unde să începi:

```bash
echo "=== INTERFEȚE ===" && ip -br a
echo ""
echo "=== RUTE ===" && ip r
echo ""
echo "=== SOCKET-URI LISTEN ===" && ss -tlnp
echo ""
echo "=== DNS ===" && cat /etc/resolv.conf | grep nameserver
echo ""
echo "=== CONTAINERE ===" && docker ps 2>/dev/null || echo "Docker indisponibil"
echo ""
echo "=== SPAȚIU DISC ===" && df -h / | tail -1
```

---

## Obținerea Ajutorului

Dacă problema persistă după ce ai încercat soluțiile de aici:

1. **Verifică jurnalele:**
   ```bash
   docker compose logs
   journalctl -u docker --no-pager | tail -50
   ```

2. **Rulează testele de verificare:**
   ```bash
   python3 tests/test_mediu.py
   python3 tests/test_rapid.py
   ```

3. **Documentează problema** (pentru a cere ajutor):
   - Mesajul de eroare complet (copy-paste, nu screenshot)
   - Ce ai încercat deja
   - Output-ul scriptului de diagnostic de mai sus

4. **Resurse online:**
   - Stack Overflow (căutare în engleză)
   - Docker Documentation
   - GitHub Issues pentru tool-ul specific

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix | 2025*
