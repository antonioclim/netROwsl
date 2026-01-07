# Cheatsheet Comenzi - Săptămâna 3

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Comenzi Rapide

### Pornire și Oprire

```powershell
# Pornește laboratorul
python scripts/porneste_lab.py

# Pornește cu toate serviciile
python scripts/porneste_lab.py --broadcast --portainer

# Verifică statusul
python scripts/porneste_lab.py --status

# Oprește laboratorul
python scripts/opreste_lab.py

# Curățare completă
python scripts/curata.py --complet
```

---

## Docker

### Gestionare Containere

```bash
# Listează containerele active
docker ps

# Listează toate containerele (inclusiv oprite)
docker ps -a

# Pornește/oprește un container
docker start week3_server
docker stop week3_server

# Repornește un container
docker restart week3_server

# Accesează shell-ul unui container
docker exec -it week3_client bash
docker exec -it week3_server bash

# Rulează o comandă într-un container
docker exec week3_client ping -c 3 172.20.0.10
```

### Log-uri și Diagnosticare

```bash
# Vezi log-urile unui container
docker logs week3_server
docker logs -f week3_server      # Urmărește în timp real
docker logs --tail 50 week3_server  # Ultimele 50 linii

# Inspectează un container
docker inspect week3_server

# Vezi utilizarea resurselor
docker stats
```

### Rețele Docker

```bash
# Listează rețelele
docker network ls

# Inspectează rețeaua week3
docker network inspect week3_network

# Vezi IP-urile containerelor
docker network inspect week3_network --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}'
```

### Docker Compose

```bash
# Din directorul docker/
cd docker

# Pornește serviciile
docker compose up -d

# Oprește serviciile
docker compose down

# Reconstruiește imaginile
docker compose build --no-cache

# Vezi log-urile tuturor serviciilor
docker compose logs -f
```

---

## Instrumente de Rețea în Containere

### Testare Conectivitate

```bash
# Ping
docker exec week3_client ping -c 3 172.20.0.10

# Test port TCP cu netcat
docker exec week3_client nc -zv 172.20.0.10 8080

# Test echo server
echo "test" | docker exec -i week3_client nc 172.20.0.10 8080

# Test tunel
echo "test tunel" | docker exec -i week3_client nc 172.20.0.254 9090

# Traceroute
docker exec week3_client traceroute 172.20.0.10
```

### Verificare Porturi și Conexiuni

```bash
# Porturi deschise (listening)
docker exec week3_server ss -tlnp

# Conexiuni active
docker exec week3_server ss -tnp

# Toate conexiunile
docker exec week3_client netstat -an
```

### Verificare IGMP și Multicast

```bash
# Grupuri multicast pe sistem
docker exec week3_client cat /proc/net/igmp

# Adrese multicast pe interfață
docker exec week3_client ip maddr show dev eth0

# Rute multicast
docker exec week3_client ip route show table local | grep multicast
```

---

## Captură și Analiză Trafic

### Script de Captură

```powershell
# Captură de bază
python scripts/captureaza_trafic.py --container server --durata 30

# Cu filtru
python scripts/captureaza_trafic.py --container client --filtru "port 5007" --output captura.pcap

# Din container specific
python scripts/captureaza_trafic.py --container router --durata 60
```

### tcpdump în Container

```bash
# Captură de bază
docker exec week3_client tcpdump -i eth0

# Salvare în fișier
docker exec week3_client tcpdump -i eth0 -w /tmp/captura.pcap

# Filtru port
docker exec week3_client tcpdump -i eth0 port 5007

# Filtru UDP
docker exec week3_client tcpdump -i eth0 udp

# Filtru broadcast
docker exec week3_client tcpdump -i eth0 broadcast

# Filtru multicast
docker exec week3_client tcpdump -i eth0 multicast

# Filtru IGMP
docker exec week3_client tcpdump -i eth0 igmp

# Filtru host specific
docker exec week3_client tcpdump -i eth0 host 172.20.0.10

# Verbose cu payload
docker exec week3_client tcpdump -i eth0 -vvX port 8080
```

### Copierea Capturilor din Container

```bash
# Copiază fișierul din container
docker cp week3_client:/tmp/captura.pcap ./captura.pcap
```

---

## Filtre Wireshark

### Filtre de Afișare

```
# Trafic broadcast
eth.dst == ff:ff:ff:ff:ff:ff

# Trafic UDP broadcast
udp and eth.dst == ff:ff:ff:ff:ff:ff

# Trafic multicast
ip.dst >= 224.0.0.0 and ip.dst <= 239.255.255.255

# Grup multicast specific
ip.dst == 239.0.0.1

# Mesaje IGMP
igmp

# IGMP Membership Report
igmp.type == 0x16

# IGMP Leave Group
igmp.type == 0x17

# Trafic TCP pe port
tcp.port == 8080

# Tunel TCP
tcp.port == 9090 or tcp.port == 8080

# Tot traficul laboratorului
ip.addr == 172.20.0.0/24

# Exclude trafic specific
not arp and not icmp

# Combinații
udp.port == 5007 and ip.src == 172.20.0.10
```

### Filtre de Captură

```
# Pentru tcpdump sau Wireshark la captură
port 5007
host 172.20.0.10
net 172.20.0.0/24
tcp
udp
broadcast
multicast
```

---

## Exerciții - Comenzi Rapide

### Exercițiul 1: Broadcast

```bash
# Terminal 1 - Receptor
docker exec -it week3_client python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod receiver

# Terminal 2 - Emițător
docker exec -it week3_server python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod sender --numar 5
```

### Exercițiul 2: Multicast

```bash
# Terminal 1 - Receptor 1
docker exec -it week3_client python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod receiver

# Terminal 2 - Receptor 2 (dacă receiver este pornit)
docker exec -it week3_receiver python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod receiver

# Terminal 3 - Emițător
docker exec -it week3_server python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod sender --numar 5
```

### Exercițiul 3: Tunel TCP

```bash
# Test conexiune directă
echo "direct" | docker exec -i week3_client nc 172.20.0.10 8080

# Test conexiune prin tunel
echo "tunel" | docker exec -i week3_client nc 172.20.0.254 9090

# Test interactiv
docker exec -it week3_client nc 172.20.0.254 9090
```

---

## Python Socket - Referință Rapidă

### Broadcast UDP

```python
import socket

# Emițător
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(b"mesaj", ('255.255.255.255', 5007))

# Receptor
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 5007))
date, adresa = sock.recvfrom(1024)
```

### Multicast UDP

```python
import socket
import struct

# Înscriere în grup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 5008))

mreq = struct.pack('4s4s',
    socket.inet_aton('239.0.0.1'),
    socket.inet_aton('0.0.0.0'))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Transmisie multicast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
sock.sendto(b"mesaj", ('239.0.0.1', 5008))
```

### TCP Client/Server

```python
import socket

# Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(5)
client, addr = server.accept()

# Client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))
client.sendall(b"mesaj")
raspuns = client.recv(1024)
```

---

## Depanare Rapidă

```bash
# Verifică dacă un port este ocupat
docker exec week3_client ss -tlnp | grep 5007

# Verifică procesele Python
docker exec week3_client ps aux | grep python

# Oprește toate procesele Python
docker exec week3_client pkill python

# Verifică rutele de rețea
docker exec week3_client ip route

# Verifică configurația IP
docker exec week3_client ip addr show eth0

# Verifică DNS
docker exec week3_client cat /etc/resolv.conf
```

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
