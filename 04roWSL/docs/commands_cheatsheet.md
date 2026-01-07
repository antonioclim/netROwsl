# Fișă de Comenzi: Analiză Trafic de Rețea

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

## Cuprins
1. [tcpdump](#tcpdump)
2. [tshark](#tshark)
3. [netcat (nc)](#netcat-nc)
4. [Filtre Wireshark](#filtre-wireshark)
5. [Docker Networking](#docker-networking)
6. [Python Socket](#python-socket)

---

## tcpdump

### Capturare de Bază

```bash
# Capturare pe toate interfețele
sudo tcpdump -i any

# Capturare pe interfață specifică
sudo tcpdump -i eth0

# Salvare în fișier
sudo tcpdump -i eth0 -w captura.pcap

# Citire din fișier
tcpdump -r captura.pcap
```

### Filtrare după Port

```bash
# Filtrare port specific
sudo tcpdump -i any port 5400

# Filtrare porturi multiple
sudo tcpdump -i any port 5400 or port 5401

# Filtrare interval de porturi
sudo tcpdump -i any portrange 5400-5402
```

### Filtrare după Protocol

```bash
# Doar TCP
sudo tcpdump -i any tcp

# Doar UDP
sudo tcpdump -i any udp

# TCP pe port specific
sudo tcpdump -i any tcp port 5400
```

### Filtrare după Adresă

```bash
# Filtrare după gazdă
sudo tcpdump -i any host 192.168.1.100

# Doar sursa
sudo tcpdump -i any src host 192.168.1.100

# Doar destinația
sudo tcpdump -i any dst host 192.168.1.100
```

### Opțiuni de Afișare

```bash
# Afișare conținut ASCII
sudo tcpdump -i any -A port 5400

# Afișare conținut hex și ASCII
sudo tcpdump -i any -X port 5400

# Afișare timestamp detaliat
sudo tcpdump -i any -tttt port 5400

# Limitare număr pachete
sudo tcpdump -i any -c 100 port 5400

# Verbose (detaliat)
sudo tcpdump -i any -v port 5400
sudo tcpdump -i any -vv port 5400  # și mai detaliat
```

---

## tshark

### Capturare de Bază

```bash
# Listare interfețe
tshark -D

# Capturare pe interfață
tshark -i eth0

# Salvare în fișier
tshark -i eth0 -w captura.pcap

# Capturare cu durată limitată
tshark -i eth0 -a duration:60
```

### Filtrare Capturare

```bash
# Filtru de capturare (BPF)
tshark -i eth0 -f "port 5400"

# Filtru de afișare
tshark -r captura.pcap -Y "tcp.port == 5400"
```

### Extragere Date

```bash
# Afișare câmpuri specifice
tshark -r captura.pcap -T fields -e ip.src -e ip.dst -e tcp.port

# Afișare date payload
tshark -r captura.pcap -T fields -e data

# Afișare ca JSON
tshark -r captura.pcap -T json

# Urmărire flux TCP
tshark -r captura.pcap -z follow,tcp,ascii,0
```

### Statistici

```bash
# Statistici conversații
tshark -r captura.pcap -q -z conv,tcp

# Statistici protocoale
tshark -r captura.pcap -q -z io,phs

# Statistici endpoint-uri
tshark -r captura.pcap -q -z endpoints,tcp
```

---

## netcat (nc)

### Client TCP

```bash
# Conectare la server
nc localhost 5400

# Cu timeout
nc -w 5 localhost 5400

# Mod verbose
nc -v localhost 5400
```

### Server TCP

```bash
# Ascultare pe port
nc -l 5400

# Ascultare continuă (reutilizare)
nc -l -k 5400
```

### Client/Server UDP

```bash
# Client UDP
nc -u localhost 5402

# Server UDP
nc -u -l 5402
```

### Transfer Fișiere

```bash
# Server (receptor)
nc -l 5400 > fisier_primit.txt

# Client (emițător)
nc localhost 5400 < fisier_trimis.txt
```

### Scanare Porturi

```bash
# Scanare port
nc -zv localhost 5400

# Scanare interval
nc -zv localhost 5400-5402
```

---

## Filtre Wireshark

### Filtre de Bază

```
# După port TCP
tcp.port == 5400

# După port sursă
tcp.srcport == 5400

# După port destinație
tcp.dstport == 5400

# După adresă IP
ip.addr == 192.168.1.100

# După IP sursă
ip.src == 192.168.1.100

# După IP destinație
ip.dst == 192.168.1.100
```

### Filtre Protocol

```
# Doar TCP
tcp

# Doar UDP
udp

# UDP pe port specific
udp.port == 5402

# TCP handshake
tcp.flags.syn == 1

# TCP FIN
tcp.flags.fin == 1
```

### Filtre Conținut

```
# TCP conținând text
tcp contains "PING"

# UDP conținând bytes
udp contains 4e:50

# Orice pachet cu pattern
frame contains "SET"
```

### Filtre Combinate

```
# AND logic
tcp.port == 5400 and ip.src == 127.0.0.1

# OR logic
tcp.port == 5400 or tcp.port == 5401

# NOT logic
not tcp.port == 22

# Combinație complexă
(tcp.port == 5400 or tcp.port == 5401) and ip.addr == 127.0.0.1
```

### Filtre Laborator Săptămâna 4

```
# Protocol TEXT
tcp.port == 5400

# Protocol BINAR
tcp.port == 5401

# Senzor UDP
udp.port == 5402

# Toate protocoalele laboratorului
tcp.port == 5400 or tcp.port == 5401 or udp.port == 5402

# Comenzi PING
tcp.port == 5400 and tcp contains "PING"

# Mesaje SET
tcp contains "SET"
```

---

## Docker Networking

### Informații Rețea

```bash
# Listare rețele
docker network ls

# Detalii rețea
docker network inspect week4_network

# Listare containere în rețea
docker network inspect -f '{{range .Containers}}{{.Name}} {{end}}' week4_network
```

### Depanare

```bash
# IP container
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' week4-lab

# Porturi mapate
docker port week4-lab

# Jurnale container
docker logs week4-lab
docker logs -f week4-lab  # urmărire în timp real
```

### Execuție în Container

```bash
# Shell în container
docker exec -it week4-lab bash

# Comandă în container
docker exec week4-lab tcpdump -i eth0 port 5400

# tcpdump în container
docker exec week4-lab tcpdump -i any -w /shared/captura.pcap
```

---

## Python Socket

### Client TCP

```python
import socket

# Creare socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectare
sock.connect(('localhost', 5400))

# Trimitere
sock.sendall(b'4 PING\n')

# Recepție
raspuns = sock.recv(1024)
print(raspuns.decode())

# Închidere
sock.close()
```

### Server TCP

```python
import socket

# Creare socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Legare și ascultare
server.bind(('0.0.0.0', 5400))
server.listen(5)

# Acceptare conexiuni
while True:
    client, adresa = server.accept()
    print(f"Conexiune de la {adresa}")
    date = client.recv(1024)
    client.sendall(b'4 PONG')
    client.close()
```

### Client UDP

```python
import socket

# Creare socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Trimitere datagramă
sock.sendto(datagrama, ('localhost', 5402))

# Recepție (opțional)
sock.settimeout(2)
try:
    raspuns, adresa = sock.recvfrom(1024)
except socket.timeout:
    print("Niciun răspuns")

sock.close()
```

### Server UDP

```python
import socket

# Creare socket UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 5402))

# Recepție datagrame
while True:
    date, adresa = server.recvfrom(1024)
    print(f"Primit de la {adresa}: {date.hex()}")
```

---

## Comenzi Utile Suplimentare

### Verificare Porturi

```bash
# Linux/WSL
netstat -tulpn | grep 5400
ss -tulpn | grep 5400
lsof -i :5400

# Windows PowerShell
netstat -ano | findstr 5400
Get-NetTCPConnection -LocalPort 5400
```

### Informații Rețea

```bash
# Adrese IP
ip addr
ifconfig

# Rută implicită
ip route
route -n

# Conexiuni active
netstat -an
ss -s
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
