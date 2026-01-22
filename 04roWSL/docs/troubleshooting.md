# Ghid de Depanare (Troubleshooting)

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest ghid acoperă problemele comune și soluțiile lor pentru laboratorul de rețele.

Pentru debugging detaliat pas-cu-pas, consultă [Ghid Debugging](debugging_guide.md).
Pentru întrebări frecvente, vezi [FAQ](faq.md).

---

## Cuprins
1. [Probleme Docker](#probleme-docker)
2. [Probleme Portainer](#probleme-portainer)
3. [Probleme Wireshark](#probleme-wireshark)
4. [Probleme Protocoale](#probleme-protocoale)
5. [Probleme Conexiune](#probleme-conexiune)
6. [Probleme Python](#probleme-python)

---

## Probleme Docker

### "Cannot connect to the Docker daemon"

**Simptome:**
- Comanda `docker ps` returnează eroare
- Mesajul "Is the docker daemon running?"

**Cauză:** Serviciul Docker nu rulează în WSL.

**Soluție:**
```bash
# Pornește serviciul Docker
sudo service docker start
# Parolă: stud

# Verifică statusul
sudo service docker status

# Testează funcționarea
docker ps
```

**Dacă problema persistă:**
```bash
# Verifică log-urile Docker
sudo cat /var/log/docker.log | tail -20

# Repornește complet
sudo service docker restart
```

---

### "permission denied while trying to connect to Docker"

**Simptome:**
- Docker funcționează cu `sudo`, dar nu fără
- Mesajul "Got permission denied"

**Cauză:** Utilizatorul nu face parte din grupul `docker`.

**Soluție:**
```bash
# Adaugă utilizatorul la grupul docker
sudo usermod -aG docker $USER

# Aplică modificările
newgrp docker

# Sau deconectează-te și reconectează-te
exit
wsl
```

---

### Containerele nu pornesc

**Simptome:**
- `docker compose up` afișează erori
- Containerele rămân în starea "Exited"

**Diagnosticare:**
```bash
# Verifică statusul containerelor
docker ps -a

# Citește log-urile containerului problematic
docker logs saptamana4-text
docker logs saptamana4-binar
docker logs saptamana4-senzor
```

**Soluții comune:**

1. **Port ocupat:**
   ```bash
   # Găsește ce ocupă portul
   sudo ss -tlnp | grep 5400
   
   # Oprește procesul sau schimbă portul în docker-compose.yml
   ```

2. **Imagine coruptă:**
   ```bash
   # Reconstruiește imaginea
   docker compose -f docker/docker-compose.yml build --no-cache
   docker compose -f docker/docker-compose.yml up -d
   ```

3. **Resurse insuficiente:**
   ```bash
   # Verifică utilizarea resurselor
   docker system df
   
   # Curăță resursele neutilizate
   docker system prune -f
   ```

---

### "No space left on device"

**Simptome:**
- Docker refuză să creeze containere sau imagini
- Eroarea "no space left on device"

**Soluție:**
```bash
# Verifică utilizarea spațiului
docker system df

# Curăță imaginile nefolosite
docker image prune -a -f

# Curăță volume orfane
docker volume prune -f

# Curăță totul (ATENȚIE: șterge și cache-ul!)
docker system prune -a --volumes -f
```

---

## Probleme Portainer

### Nu pot accesa http://localhost:9000

**Diagnosticare:**
```bash
# Verifică dacă Portainer rulează
docker ps | grep portainer

# Verifică portul
nc -zv localhost 9000
```

**Soluții:**

1. **Containerul nu rulează:**
   ```bash
   docker start portainer
   ```

2. **Containerul nu există:**
   ```bash
   docker run -d -p 9000:9000 --name portainer --restart=always \
     -v /var/run/docker.sock:/var/run/docker.sock \
     -v portainer_data:/data portainer/portainer-ce:latest
   ```

3. **Portul e ocupat de alt proces:**
   ```bash
   sudo ss -tlnp | grep 9000
   # Oprește procesul care ocupă portul
   ```

---

### Am uitat parola Portainer

**Soluție:** Resetează Portainer complet:
```bash
docker stop portainer
docker rm portainer
docker volume rm portainer_data

# Recreează - prima accesare cere parolă nouă
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

---

### Portainer nu vede containerele

**Cauză:** Portainer nu are acces la socket-ul Docker.

**Soluție:**
```bash
# Verifică montarea socket-ului
docker inspect portainer | grep -A5 Mounts

# Recreează cu montarea corectă
docker rm -f portainer
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

---

## Probleme Wireshark

### Nu se capturează pachete

**Verificări:**

1. **Interfața corectă:**
   - Selectează "vEthernet (WSL)" pentru trafic Docker
   - NU selecta "Loopback Adapter" decât pentru 127.0.0.1 direct

2. **Captura pornită:**
   - Butonul albastru (aripioara) trebuie să fie activ
   - Butonul roșu oprește captura

3. **Filtrul prea restrictiv:**
   - Șterge filtrul și verifică dacă vezi pachete
   - Dacă da, filtrul ascunde pachetele dorite

4. **Traficul generat în timpul capturii:**
   - Pornește captura ÎNTÂI
   - Apoi rulează clientul
   - Oprește captura DUPĂ

---

### Filtrul devine roșu (sintaxă invalidă)

**Greșeli comune:**

| Greșit | Corect |
|--------|--------|
| `tcp.port = 5400` | `tcp.port == 5400` |
| `port == 5400` | `tcp.port == 5400` |
| `tcp contains 'PING'` | `tcp contains "PING"` |
| `TCP.port == 5400` | `tcp.port == 5400` |

---

### Nu văd conținutul pachetelor

**Cauză:** Pachetele TCP sunt reassemblate.

**Soluție:**
1. Click dreapta pe un pachet
2. "Follow" → "TCP Stream"
3. Vezi conversația completă în format text

---

## Probleme Protocoale

### CRC32 invalid

**Verificări:**

1. **Network Byte Order:**
   ```python
   # GREȘIT
   struct.pack('I', crc)
   
   # CORECT
   struct.pack('!I', crc)
   ```

2. **Date corecte pentru CRC:**
   ```python
   # Pentru protocol BINAR:
   # CRC = crc32(antet_fara_crc + payload)
   # Antet fără CRC = primii 10 bytes
   
   crc = binascii.crc32(mesaj[0:10] + payload) & 0xFFFFFFFF
   ```

3. **Mascare 32-bit:**
   ```python
   # GREȘIT (poate fi negativ pe unele sisteme)
   crc = binascii.crc32(date)
   
   # CORECT
   crc = binascii.crc32(date) & 0xFFFFFFFF
   ```

---

### Mesajele nu sunt primite

**Verificări:**

1. **Conexiune activă:**
   ```python
   # Verifică înainte de send
   if sock.fileno() == -1:
       print("Socket închis!")
   ```

2. **Buffer complet trimis:**
   ```python
   # GREȘIT (poate trimite parțial)
   sock.send(mesaj)
   
   # CORECT (garantează trimiterea completă)
   sock.sendall(mesaj)
   ```

3. **Recepție completă:**
   ```python
   # recv() poate returna mai puțin decât ai cerut!
   date = b''
   while len(date) < lungime_asteptata:
       chunk = sock.recv(lungime_asteptata - len(date))
       if not chunk:
           break  # Conexiunea s-a închis
       date += chunk
   ```

---

### Protocol TEXT nu funcționează

**Format corect:**
```
<LUNGIME> <COMANDĂ> [ARGUMENTE]
```

**Exemple:**
```python
# CORECT
mesaj = "4 PING"           # Lungime "PING" = 4
mesaj = "13 SET cheie val" # Lungime "SET cheie val" = 13

# GREȘIT
mesaj = "PING"             # Lipsește lungimea
mesaj = "5 PING"           # Lungime greșită (4, nu 5)
```

---

## Probleme Conexiune

### "Connection refused"

**Cauză:** Serverul nu ascultă pe portul respectiv.

**Verificări:**
```bash
# Containerul rulează?
docker ps | grep saptamana4

# Portul ascultă?
nc -zv localhost 5400
```

**Soluții:**
1. Pornește containerele: `docker compose up -d`
2. Verifică maparea porturilor în `docker-compose.yml`

---

### "Connection timed out"

**Cauze posibile:**
- Firewall blochează conexiunea
- Adresa sau portul greșit
- Serverul nu răspunde

**Verificări:**
```bash
# Firewall WSL
sudo ufw status

# Ping la gazdă
ping localhost

# Verifică routarea
ip route
```

---

### "Address already in use"

**Cauză:** Alt proces ocupă portul.

**Soluție:**
```bash
# Găsește procesul
sudo ss -tlnp | grep 5400

# Oprește-l sau folosește alt port
kill -9 <PID>
```

---

## Probleme Python

### ModuleNotFoundError

**Soluție:**
```bash
# Instalează modulul lipsă
pip install <modul> --break-system-packages

# Sau în mediu virtual
python -m venv venv
source venv/bin/activate
pip install <modul>
```

---

### struct.error: unpack requires a buffer of X bytes

**Cauză:** Nu ai primit suficiente date.

**Soluție:**
```python
date = sock.recv(1024)
if len(date) < 14:  # Verifică înainte de unpack
    print(f"Insuficient: {len(date)} bytes")
else:
    header = struct.unpack('!2sBBHII', date[:14])
```

---

### Socket timeout

**Soluție:**
```python
sock.settimeout(10.0)  # Mărește timeout-ul

try:
    date = sock.recv(1024)
except socket.timeout:
    print("Serverul nu a răspuns în 10 secunde")
```

---

## Checklist General

Când ceva nu funcționează, verifică în ordine:

```
□ Docker rulează?              sudo service docker status
□ Containerele sunt Up?        docker ps
□ Porturile răspund?           nc -zv localhost 5400
□ Log-uri container?           docker logs <container>
□ Wireshark pe interfața bună? vEthernet (WSL)
□ Network byte order?          '!' în struct.pack
□ CRC include datele corecte?  antet[0:10] + payload
```

---

## Când Nimic Nu Funcționează

1. **Repornește totul:**
   ```bash
   docker compose -f docker/docker-compose.yml down
   sudo service docker restart
   docker compose -f docker/docker-compose.yml up -d
   ```

2. **Verifică versiunile:**
   ```bash
   docker --version
   python3 --version
   ```

3. **Citește log-urile complet:**
   ```bash
   docker logs saptamana4-text 2>&1 | less
   ```

4. **Cere ajutor:** Include în cerere:
   - Ce ai încercat să faci
   - Ce ai așteptat să se întâmple
   - Ce s-a întâmplat de fapt
   - Output-ul complet al erorilor

---

## Referințe

- [README principal](../README.md)
- [Ghid Debugging](debugging_guide.md)
- [FAQ](faq.md)
- [Documentația Docker](https://docs.docker.com/)

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
