# Fișă de Comenzi - Săptămâna 2

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Comenzi Kit de Laborator

### Pornire și Oprire

```powershell
# Pornire laborator
python scripts/start_lab.py

# Verificare stare
python scripts/start_lab.py --status

# Oprire laborator (păstrează datele)
python scripts/stop_lab.py

# Curățare completă
python scripts/cleanup.py --full
```

### Rulare Exerciții

```powershell
# Server TCP (în container)
docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server --mode threaded

# Client TCP
docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py client --message "test"

# Server UDP (în container)
docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py server

# Client UDP
docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py client --command "ping"
```

### Demonstrații

```powershell
# Lista demonstrațiilor
python scripts/run_demo.py --list

# Demo comparație TCP vs UDP
python scripts/run_demo.py --demo 1

# Demo clienți concurenți
python scripts/run_demo.py --demo 2

# Toate demonstrațiile
python scripts/run_demo.py --all
```

### Teste

```powershell
# Smoke test
python tests/smoke_test.py

# Teste Exercițiul 1 (TCP)
python tests/test_exercises.py --exercise 1

# Teste Exercițiul 2 (UDP)
python tests/test_exercises.py --exercise 2

# Toate testele
python tests/test_exercises.py
```

## Comenzi Docker

### Management Containere

```powershell
# Listare containere active
docker ps

# Listare toate containerele
docker ps -a

# Pornire container
docker start week2_lab

# Oprire container
docker stop week2_lab

# Repornire container
docker restart week2_lab

# Acces shell în container
docker exec -it week2_lab bash

# Vizualizare loguri
docker logs week2_lab

# Vizualizare loguri în timp real
docker logs -f week2_lab
```

### Docker Compose

```powershell
# Schimbare în directorul docker
cd docker

# Pornire servicii
docker compose up -d

# Oprire servicii
docker compose down

# Reconstruire imagine
docker compose build --no-cache

# Vizualizare status
docker compose ps

# Vizualizare loguri
docker compose logs -f
```

### Curățare Docker

```powershell
# Eliminare containere oprite
docker container prune -f

# Eliminare imagini neutilizate
docker image prune -f

# Eliminare volume neutilizate
docker volume prune -f

# Curățare completă sistem
docker system prune -f
```

## Comenzi Rețea

### Testare Conectivitate

```powershell
# Ping (Windows)
ping localhost

# Test port TCP (PowerShell)
Test-NetConnection -ComputerName localhost -Port 9090

# Listare porturi deschise (Windows)
netstat -ano | findstr :9090

# Din container - ping
docker exec week2_lab ping -c 3 8.8.8.8

# Din container - verificare DNS
docker exec week2_lab nslookup google.com
```

### Netcat (în container)

```bash
# Conectare TCP
nc localhost 9090

# Ascultare TCP pe un port
nc -l -p 9099

# Trimitere UDP
echo "ping" | nc -u localhost 9091

# Verificare port deschis
nc -zv localhost 9090
```

### Captură Trafic

```powershell
# Script captură
python scripts/capture_traffic.py --output captura.pcap

# Captură cu filtru
python scripts/capture_traffic.py --filter "port 9090"

# Din container - tcpdump
docker exec week2_lab tcpdump -i any port 9090

# Din container - tcpdump cu salvare
docker exec week2_lab tcpdump -i any -w /app/pcap/captura.pcap port 9090
```

## Filtre Wireshark

### Filtre de Captură (BPF)

```
# Trafic pe port specific
port 9090

# Doar TCP
tcp port 9090

# Doar UDP
udp port 9091

# Combinație
tcp port 9090 or udp port 9091

# Trafic către/de la host
host 10.0.2.10
```

### Filtre de Afișare

```
# Trafic TCP pe port
tcp.port == 9090

# Trafic UDP pe port
udp.port == 9091

# Pachete SYN (inițiere conexiune)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Pachete SYN-ACK
tcp.flags.syn == 1 && tcp.flags.ack == 1

# Pachete FIN (terminare conexiune)
tcp.flags.fin == 1

# Pachete cu date (PSH)
tcp.flags.push == 1

# Retransmisii TCP
tcp.analysis.retransmission

# Pachete de la adresă specifică
ip.src == 10.0.2.10

# Pachete către adresă specifică
ip.dst == 10.0.2.10
```

## Python Socket - Referință Rapidă

### Import și Creare

```python
import socket

# Socket TCP
sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Socket UDP
sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

### Server TCP

```python
# Permitere reutilizare adresă
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Legare la adresă
sock.bind(('0.0.0.0', 9090))

# Ascultare
sock.listen(5)

# Acceptare conexiune
client_sock, client_addr = sock.accept()

# Recepție date
data = client_sock.recv(1024)

# Trimitere date
client_sock.send(b"raspuns")
client_sock.sendall(b"raspuns complet")
```

### Client TCP

```python
# Conectare
sock.connect(('localhost', 9090))

# Timeout
sock.settimeout(5.0)

# Trimitere și recepție
sock.send(b"mesaj")
response = sock.recv(1024)
```

### UDP

```python
# Trimitere datagramă
sock.sendto(b"mesaj", ('localhost', 9091))

# Recepție datagramă
data, addr = sock.recvfrom(1024)
```

### Context Manager

```python
# Închidere automată a socket-ului
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', 9090))
    sock.send(b"mesaj")
    response = sock.recv(1024)
# Socket închis automat aici
```

## Scurtături Utile

### PowerShell

```powershell
# Alias pentru docker exec
function week2 { docker exec -it week2_lab $args }

# Utilizare
week2 python /app/exercises/ex_2_01_tcp.py server
```

### Bash (în container)

```bash
# Alias-uri
alias server-tcp='python /app/exercises/ex_2_01_tcp.py server'
alias server-udp='python /app/exercises/ex_2_02_udp.py server'
```

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
