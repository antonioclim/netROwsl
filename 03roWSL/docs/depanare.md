# Ghid de Depanare - Săptămâna 3

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Cuprins

1. [Probleme Socket și Broadcast](#probleme-socket-și-broadcast)
2. [Probleme Multicast](#probleme-multicast)
3. [Probleme Tunel TCP](#probleme-tunel-tcp)
4. [Probleme Docker](#probleme-docker)
5. [Probleme Wireshark](#probleme-wireshark)
6. [Probleme Conectivitate](#probleme-conectivitate)

---

## Probleme Socket și Broadcast

### Eroare: `OSError: [Errno 10013] Permission denied`

**Cauză:** Pe Windows, transmisia broadcast necesită privilegii de Administrator.

**Soluție:**
```powershell
# Opțiunea 1: Rulați PowerShell ca Administrator
# Click dreapta pe PowerShell → Run as Administrator

# Opțiunea 2: Folosiți containerele Docker (recomandat)
docker exec -it week3_client python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod sender
```

---

### Eroare: `OSError: [Errno 98] Address already in use`

**Cauză:** Un alt proces folosește deja portul.

**Soluție:**
```bash
# Verificați ce folosește portul
docker exec week3_client ss -tlnp | grep 5007

# Opriți procesul anterior
docker exec week3_client pkill -f "ex_3_01"

# Sau reporniți containerul
docker restart week3_client
```

---

### Mesajele broadcast nu sunt primite

**Verificări:**
1. Receptorul este legat la `0.0.0.0`, nu la o adresă specifică
2. Emițătorul are opțiunea `SO_BROADCAST` activată
3. Portul este același la emițător și receptor

```bash
# Verificați că receptorul ascultă
docker exec week3_client ss -ulnp | grep 5007

# Verificați traficul cu tcpdump
docker exec week3_client tcpdump -i eth0 port 5007
```

---

## Probleme Multicast

### Eroare: `OSError: [Errno 19] No such device`

**Cauză:** Interfața de rețea specificată nu există sau nu suportă multicast.

**Soluție:**
```python
# Folosiți '0.0.0.0' pentru a lega la toate interfețele
mreq = struct.pack('4s4s',
    socket.inet_aton('239.0.0.1'),
    socket.inet_aton('0.0.0.0')  # ← Toate interfețele
)
```

---

### Mesajele multicast nu sunt primite

**Verificări:**

1. **Confirmați înscrierea în grup:**
```bash
docker exec week3_client cat /proc/net/igmp | grep -i ef000001
# ef000001 este 239.0.0.1 în hex (little-endian)
```

2. **Verificați TTL-ul:**
```python
# TTL trebuie să fie cel puțin 1 pentru rețeaua locală
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
```

3. **Verificați traficul IGMP:**
```bash
docker exec week3_client tcpdump -i eth0 igmp
```

---

### IGMP Join nu funcționează

**Cauză:** Containerul sau sistemul nu suportă multicast.

**Verificare:**
```bash
# Verificați suportul multicast pe interfață
docker exec week3_client ip link show eth0 | grep MULTICAST
```

**Soluție:**
```bash
# Dacă MULTICAST nu apare, activați-l
docker exec week3_client ip link set eth0 multicast on
```

---

## Probleme Tunel TCP

### Eroare: `ConnectionRefusedError: [Errno 111] Connection refused`

**Cauză:** Serverul țintă nu rulează sau portul este greșit.

**Verificări:**
```bash
# Verificați că serverul echo rulează
docker exec week3_server ss -tlnp | grep 8080

# Verificați că tunelul rulează
docker exec week3_router ss -tlnp | grep 9090

# Testați conexiunea directă
docker exec week3_client nc -zv 172.20.0.10 8080
```

---

### Datele nu ajung prin tunel

**Verificări:**

1. **Verificați conexiunile active:**
```bash
docker exec week3_router ss -tnp | grep -E "(8080|9090)"
```

2. **Verificați log-urile tunelului:**
```bash
docker logs week3_router
```

3. **Testați manual:**
```bash
# Conexiune directă la server
echo "test direct" | docker exec -i week3_client nc 172.20.0.10 8080

# Conexiune prin tunel
echo "test tunel" | docker exec -i week3_client nc 172.20.0.254 9090
```

---

### Eroare: `BrokenPipeError`

**Cauză:** Cealaltă parte a închis conexiunea înainte de terminarea transmisiei.

**Soluție:**
```python
# Tratați excepția în codul de relay
try:
    destinatie.sendall(date)
except BrokenPipeError:
    # Conexiunea a fost închisă de cealaltă parte
    break
```

---

### Blocaj la relay bidirecțional

**Cauză:** Nu folosiți thread-uri pentru cele două direcții.

**Soluție:**
```python
import threading

# Thread pentru client → server
thread1 = threading.Thread(target=relay, args=(client, server))

# Thread pentru server → client
thread2 = threading.Thread(target=relay, args=(server, client))

thread1.start()
thread2.start()
```

---

## Probleme Docker

### Containerele nu pornesc

**Verificări:**
```bash
# Verificați statusul Docker
docker info

# Verificați log-urile compose
cd docker && docker compose logs

# Verificați configurația
docker compose config
```

**Soluții comune:**
```bash
# Reconstruiți imaginile
docker compose build --no-cache

# Eliminați rețele vechi conflictuale
docker network prune

# Reporniți Docker Desktop
```

---

### Eroare: `network week3_network not found`

**Soluție:**
```bash
# Creați rețeaua manual
docker network create --subnet=172.20.0.0/24 week3_network

# Sau reporniți compose
cd docker && docker compose down && docker compose up -d
```

---

### Conflict de subnet

**Cauză:** Subnet-ul 172.20.0.0/24 este deja folosit.

**Verificare:**
```bash
docker network ls
docker network inspect bridge
```

**Soluție:**
Modificați subnet-ul în `docker-compose.yml`:
```yaml
networks:
  week3_network:
    ipam:
      config:
        - subnet: 172.21.0.0/24  # ← Schimbați subnet-ul
```

---

### Probleme DNS în containere

**Verificare:**
```bash
docker exec week3_client cat /etc/resolv.conf
docker exec week3_client ping -c 1 google.com
```

**Soluție:**
Adăugați DNS explicit în `docker-compose.yml`:
```yaml
services:
  client:
    dns:
      - 8.8.8.8
      - 8.8.4.4
```

---

### Line endings (CRLF vs LF)

**Cauză:** Fișierele au fost editate pe Windows și au terminații de linie Windows.

**Simptom:**
```
/bin/bash^M: bad interpreter
```

**Soluție:**
```bash
# Convertește la LF
sed -i 's/\r$//' script.py

# Sau în Git
git config --global core.autocrlf input
```

---

## Probleme Wireshark

### Nu se vede traficul

**Verificări:**

1. **Selectați interfața corectă:**
   - Pentru Docker Desktop pe Windows: `\Device\NPF_{...}` (Ethernet)
   - Sau interfața WSL

2. **Verificați că capturați pe interfața corectă:**
```bash
# Listați interfețele în Wireshark
# Capture → Options → Manage Interfaces
```

---

### Filtru de afișare nu funcționează

**Erori comune:**

| Greșit | Corect |
|--------|--------|
| `ip.addr = 172.20.0.10` | `ip.addr == 172.20.0.10` |
| `port 8080` | `tcp.port == 8080` |
| `broadcast` | `eth.dst == ff:ff:ff:ff:ff:ff` |

---

### Captură goală

**Verificări:**
```bash
# Verificați că există trafic
docker exec week3_client tcpdump -i eth0 -c 5

# Rulați exercițiile în timpul capturii
```

---

## Probleme Conectivitate

### Ping nu funcționează între containere

**Verificări:**
```bash
# Verificați adresele IP
docker exec week3_client ip addr

# Verificați rutarea
docker exec week3_client ip route

# Verificați conectivitatea
docker exec week3_client ping -c 3 172.20.0.10
```

---

### Port nu este accesibil din Windows

**Verificări:**
```bash
# Verificați port forwarding în compose
docker port week3_server

# Testați din Windows
Test-NetConnection -ComputerName localhost -Port 8080
```

**Soluție:**
Asigurați-vă că porturile sunt publicate în `docker-compose.yml`:
```yaml
ports:
  - "8080:8080"
```

---

### Pierdere de pachete

**Verificări:**
```bash
# Test cu ping
docker exec week3_client ping -c 100 172.20.0.10

# Verificați statistici de rețea
docker exec week3_client netstat -s
```

---

## Referință Rapidă Diagnostic

### Comenzi de Diagnostic

```bash
# Stare containere
docker ps -a

# Log-uri container
docker logs week3_server --tail 50

# Procese în container
docker exec week3_client ps aux

# Porturi în ascultare
docker exec week3_client ss -tlnp

# Conexiuni active
docker exec week3_client ss -tnp

# Configurație rețea
docker exec week3_client ip addr
docker exec week3_client ip route

# Test conectivitate
docker exec week3_client ping -c 3 172.20.0.10
docker exec week3_client nc -zv 172.20.0.10 8080

# Trafic în timp real
docker exec week3_client tcpdump -i eth0
```

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
