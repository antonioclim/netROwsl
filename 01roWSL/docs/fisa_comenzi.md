# Fișa Comenzilor - Săptămâna 1

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## Configurare Interfețe de Rețea

### Afișare Interfețe

```bash
# Toate interfețele cu detalii complete
ip addr show
ip a                          # Formă scurtă

# Format compact (recomandat)
ip -br addr show
ip -br a

# O singură interfață
ip addr show eth0

# Doar adresele IPv4
ip -4 addr show

# Doar adresele IPv6
ip -6 addr show
```

### Tabela de Rutare

```bash
# Afișare completă
ip route show
ip r                          # Formă scurtă

# Doar ruta implicită (default gateway)
ip route show default

# Ruta către o destinație specifică
ip route get 8.8.8.8
```

### Vecinii ARP

```bash
# Tabelul ARP (vecini cunoscuți)
ip neigh show
ip n                          # Formă scurtă
```

## Testare Conectivitate

### Ping (ICMP Echo)

```bash
# Ping de bază (4 pachete)
ping -c 4 192.168.1.1

# Ping continuu (Ctrl+C pentru oprire)
ping 192.168.1.1

# Ping cu interval personalizat (0.5 secunde)
ping -i 0.5 -c 10 192.168.1.1

# Ping cu dimensiune pachet specificată
ping -s 1000 -c 4 192.168.1.1

# Ping rapid (flood) - necesită root
ping -f -c 100 192.168.1.1
```

### Rezolvare DNS

```bash
# Folosind getent (recomandat)
getent hosts google.com

# Folosind nslookup
nslookup google.com

# Folosind dig (mai detaliat)
dig google.com
dig google.com +short        # Doar adresa IP
dig @8.8.8.8 google.com      # Server DNS specific

# Rezolvare inversă
dig -x 8.8.8.8
```

### Traceroute

```bash
# Trasare rută (ICMP)
traceroute 8.8.8.8

# Cu TCP în loc de ICMP
traceroute -T 8.8.8.8

# Cu număr maxim de hopuri
traceroute -m 15 8.8.8.8
```

## Inspectare Socket-uri

### Comanda ss (înlocuiește netstat)

```bash
# Toate socket-urile TCP și UDP cu porturi numerice
ss -tunap

# Decodificarea opțiunilor:
#   -t  TCP
#   -u  UDP
#   -n  Numeric (nu rezolvă nume)
#   -a  All (toate stările)
#   -p  Process (arată PID și nume proces)
#   -l  Listen (doar socket-uri în ascultare)

# Doar socket-uri în ascultare
ss -tlnp

# Conexiuni TCP stabilite
ss -tn state established

# Socket-uri pe un port specific
ss -tlnp | grep :9090
ss -tlnp 'sport = :9090'

# Conexiuni către o adresă IP
ss -tn 'dst 192.168.1.1'
```

### Comanda netstat (legacy)

```bash
# Echivalent ss -tunap
netstat -tunap

# Socket-uri în ascultare
netstat -tlnp
```

## Netcat (nc) - Cuțitul Elvețian al Rețelelor

### Server și Client TCP

```bash
# Server TCP (ascultă pe port)
nc -l -p 9090

# Client TCP (conectare la server)
nc localhost 9090
nc 192.168.1.100 9090

# Trimite fișier
nc -l -p 9090 > fisier_primit.txt    # Server
nc localhost 9090 < fisier.txt        # Client

# Trimite mesaj și închide
echo "Salut!" | nc -q 1 localhost 9090
```

### Server și Client UDP

```bash
# Server UDP
nc -u -l -p 9091

# Client UDP
nc -u localhost 9091

# Trimite datagram și închide
echo "Test UDP" | nc -u -q 1 localhost 9091
```

### Scanare Porturi

```bash
# Verifică dacă un port este deschis
nc -zv localhost 9090

# Scanare interval de porturi
nc -zv localhost 80-90

# Timeout la scanare
nc -zv -w 2 192.168.1.1 22
```

## Captura de Pachete

### tcpdump

```bash
# Captură de bază pe interfață
tcpdump -i eth0
tcpdump -i any                # Toate interfețele

# Salvare în fișier PCAP
tcpdump -i eth0 -w captura.pcap

# Citire din fișier PCAP
tcpdump -r captura.pcap

# Captură cu detalii (verbose)
tcpdump -i eth0 -v
tcpdump -i eth0 -vv           # Foarte verbose
tcpdump -i eth0 -vvv          # Maxim verbose

# Limitare număr pachete
tcpdump -i eth0 -c 100

# Afișare conținut pachet (hex și ASCII)
tcpdump -i eth0 -X
tcpdump -i eth0 -XX           # Include header Ethernet
```

### tshark (Wireshark CLI)

```bash
# Captură de bază
tshark -i eth0

# Salvare în fișier
tshark -i eth0 -w captura.pcap

# Citire și afișare pachete
tshark -r captura.pcap

# Export câmpuri specifice
tshark -r captura.pcap \
    -T fields \
    -e frame.number \
    -e ip.src \
    -e ip.dst \
    -e tcp.port

# Statistici protocol
tshark -r captura.pcap -q -z io,phs

# Conversații IP
tshark -r captura.pcap -q -z conv,ip
```

### Filtre BPF (Berkeley Packet Filter)

```bash
# Filtrare după port
tcpdump -i eth0 port 80
tcpdump -i eth0 port 80 or port 443

# Filtrare după protocol
tcpdump -i eth0 tcp
tcpdump -i eth0 udp
tcpdump -i eth0 icmp

# Filtrare după adresă
tcpdump -i eth0 host 192.168.1.1
tcpdump -i eth0 src host 192.168.1.1
tcpdump -i eth0 dst host 192.168.1.1

# Filtrare după rețea
tcpdump -i eth0 net 192.168.1.0/24

# Combinații
tcpdump -i eth0 'tcp port 80 and host 192.168.1.1'
tcpdump -i eth0 'tcp and port 9090 and not host 127.0.0.1'
```

### Filtre Wireshark Display

```
# Filtre pentru Wireshark (nu pentru tcpdump)

# După protocol
tcp
udp
http
dns
icmp

# După port
tcp.port == 80
tcp.srcport == 443
tcp.dstport == 9090

# După adresă IP
ip.addr == 192.168.1.1
ip.src == 192.168.1.1
ip.dst == 192.168.1.1

# Flag-uri TCP
tcp.flags.syn == 1
tcp.flags.ack == 1
tcp.flags.syn == 1 and tcp.flags.ack == 0  # Doar SYN

# Conține text
http contains "password"
```

## Docker - Comenzi Esențiale

### Managementul Containerelor

```bash
# Afișare containere active
docker ps

# Toate containerele (inclusiv oprite)
docker ps -a

# Pornire container
docker start week1_lab

# Oprire container
docker stop week1_lab

# Repornire container
docker restart week1_lab

# Ștergere container
docker rm week1_lab
docker rm -f week1_lab        # Forțat

# Executare comandă în container
docker exec -it week1_lab bash
docker exec week1_lab ip addr
```

### Docker Compose

```bash
# Pornire servicii
docker compose up -d

# Oprire servicii
docker compose down

# Reconstruire imagini
docker compose build --no-cache

# Vizualizare jurnale
docker compose logs
docker compose logs -f        # Urmărire în timp real
docker compose logs week1_lab # Un singur serviciu

# Stare servicii
docker compose ps
```

## Python - One-Liners pentru Rețele

```bash
# Server TCP simplu (echo)
python -c "
import socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 9090))
s.listen(1)
print('Ascult pe :9090')
c, a = s.accept()
print(f'Conectat: {a}')
d = c.recv(1024)
print(f'Primit: {d}')
c.send(d)
c.close()
"

# Client TCP simplu
python -c "
import socket
s = socket.socket()
s.connect(('localhost', 9090))
s.send(b'Test')
print(s.recv(1024))
s.close()
"

# Server HTTP simplu
python -m http.server 8080
```

## Referință Rapidă

| Sarcină | Comandă |
|---------|---------|
| Interfețe de rețea | `ip -br a` |
| Tabelă rutare | `ip r` |
| Socket-uri în ascultare | `ss -tlnp` |
| Conexiuni active | `ss -tnp` |
| Test conectivitate | `ping -c 4 <ip>` |
| Rezolvare DNS | `dig <domeniu> +short` |
| Server TCP simplu | `nc -l -p <port>` |
| Client TCP | `nc <ip> <port>` |
| Captură trafic | `tcpdump -i <iface> -w <fisier.pcap>` |
| Analiză PCAP | `tshark -r <fisier.pcap>` |
| Acces container | `docker exec -it week1_lab bash` |

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
