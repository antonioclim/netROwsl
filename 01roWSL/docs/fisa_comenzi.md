# Fișa Comenzilor - Săptămâna 1

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

---

## Diferențe PowerShell vs Bash

Când lucrezi cu WSL, e important să știi în ce shell te afli. Comenzile diferă!

### Cum să Știi Unde Ești

| Indicator | PowerShell (Windows) | Bash (WSL/Linux) |
|-----------|---------------------|------------------|
| **Prompt** | `PS C:\Users\stud>` | `stud@PC:~$` |
| **Căi** | `C:\Users\stud` | `/home/stud` |
| **Separator cale** | `\` (backslash) | `/` (slash) |

**Regulă de aur:** Dacă vezi `C:\` sau `D:\`, ești în Windows. Dacă vezi `/home/` sau `/mnt/`, ești în Linux.

### Comenzi Echivalente

| Acțiune | PowerShell (Windows) | Bash (WSL/Linux) |
|---------|---------------------|------------------|
| Afișează directorul curent | `Get-Location` sau `pwd` | `pwd` |
| Listează fișiere | `Get-ChildItem` sau `dir` | `ls -la` |
| Schimbă director | `cd D:\RETELE` | `cd /mnt/d/RETELE` |
| Creează director | `mkdir D:\RETELE` | `mkdir -p /mnt/d/RETELE` |
| Șterge fișier | `Remove-Item file.txt` | `rm file.txt` |
| Copiază fișier | `Copy-Item src dest` | `cp src dest` |
| Variabilă de mediu | `$env:PATH` | `$PATH` |
| Comentariu | `# comentariu` | `# comentariu` |
| Continuare linie | `` ` `` (backtick) | `\` (backslash) |
| Pipe | `\|` (obiecte .NET) | `\|` (text) |

### Căi Cross-Platform

| Din | Către | Cale |
|-----|-------|------|
| Windows | D:\RETELE | `D:\RETELE` |
| WSL | D:\RETELE | `/mnt/d/RETELE` |
| Windows | /home/stud | `\\wsl$\Ubuntu\home\stud` |
| WSL | /home/stud | `/home/stud` |

---

## Configurare Interfețe de Rețea

### Afișare Interfețe

```bash
# Toate interfețele cu detalii complete
ip addr show
ip a                          # Formă scurtă

# Format compact (recomandat pentru verificare rapidă)
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
# Tabelul ARP (vecini cunoscuți la Layer 2)
ip neigh show
ip n                          # Formă scurtă
```

---

## Testare Conectivitate

### Ping (ICMP Echo)

```bash
# Ping de bază (4 pachete — ca la examen)
ping -c 4 192.168.1.1

# Ping continuu (Ctrl+C pentru oprire)
ping 192.168.1.1

# Ping cu interval personalizat (0.5 secunde)
ping -i 0.5 -c 10 192.168.1.1

# Ping cu dimensiune pachet specificată (testare MTU)
ping -s 1000 -c 4 192.168.1.1

# Ping rapid (flood) — necesită root
sudo ping -f -c 100 192.168.1.1
```

### Rezolvare DNS

```bash
# Metodă rapidă
getent hosts google.com

# Folosind nslookup
nslookup google.com

# Folosind dig (mai detaliat)
dig google.com
dig google.com +short        # Doar adresa IP
dig @8.8.8.8 google.com      # Server DNS specific

# Rezolvare inversă (IP → nume)
dig -x 8.8.8.8
```

### Traceroute

```bash
# Trasare rută (ICMP implicit)
traceroute 8.8.8.8

# Cu TCP în loc de ICMP (trece prin firewall-uri)
traceroute -T 8.8.8.8

# Cu număr maxim de hopuri
traceroute -m 15 8.8.8.8
```

---

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

# Doar socket-uri în ascultare (servere)
ss -tlnp

# Conexiuni TCP stabilite
ss -tn state established

# Socket-uri pe un port specific
ss -tlnp | grep :9090
ss -tlnp 'sport = :9090'

# Conexiuni către o adresă IP
ss -tn 'dst 192.168.1.1'
```

### Comanda netstat (legacy, dar încă utilă)

```bash
# Echivalent ss -tunap
netstat -tunap

# Socket-uri în ascultare
netstat -tlnp
```

---

## Netcat (nc) — Cuțitul Elvețian al Rețelelor

### Server și Client TCP

```bash
# Server TCP (ascultă pe port)
nc -l -p 9090

# Client TCP (conectare la server)
nc localhost 9090
nc 192.168.1.100 9090

# Trimite fișier prin rețea
nc -l -p 9090 > fisier_primit.txt    # Server (receptor)
nc localhost 9090 < fisier.txt        # Client (emițător)

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

# Cu timeout (util pentru servere lente)
nc -zv -w 2 192.168.1.1 22
```

---

## Captura de Pachete

### tcpdump

```bash
# Captură de bază pe interfață
tcpdump -i eth0
tcpdump -i any                # Toate interfețele

# Salvare în fișier PCAP (pentru Wireshark)
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

# Scriere imediată (fără buffering)
tcpdump -i eth0 -w captura.pcap -U
```

### tshark (Wireshark CLI)

```bash
# Captură de bază
tshark -i eth0

# Salvare în fișier
tshark -i eth0 -w captura.pcap

# Citire și afișare pachete
tshark -r captura.pcap

# Export câmpuri specifice (util pentru analiză)
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

Funcționează cu tcpdump și tshark pentru captură:

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

Funcționează în Wireshark pentru vizualizare (sintaxă diferită de BPF!):

```
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

# Flag-uri TCP (important pentru handshake)
tcp.flags.syn == 1
tcp.flags.ack == 1
tcp.flags.syn == 1 and tcp.flags.ack == 0  # Doar SYN (conexiuni noi)
tcp.flags.fin == 1

# Conține text
http contains "password"
```

---

## Docker — Comenzi Esențiale

### Managementul Containerelor

```bash
# Afișare containere active
docker ps

# Toate containerele (inclusiv oprite)
docker ps -a

# Pornire container existent
docker start week1_lab

# Oprire container
docker stop week1_lab

# Repornire container
docker restart week1_lab

# Ștergere container
docker rm week1_lab
docker rm -f week1_lab        # Forțat (chiar dacă rulează)

# Executare comandă în container
docker exec -it week1_lab bash
docker exec week1_lab ip addr
```

### Docker Compose

```bash
# Pornire servicii (în fundal)
docker compose up -d

# Oprire servicii
docker compose down

# Reconstruire imagini (fără cache)
docker compose build --no-cache

# Vizualizare jurnale
docker compose logs
docker compose logs -f        # Urmărire în timp real
docker compose logs week1_lab # Un singur serviciu

# Stare servicii
docker compose ps
```

### Diagnosticare Docker

```bash
# Informații despre un container
docker inspect week1_lab

# Rețele Docker
docker network ls
docker network inspect week1_network

# Spațiu utilizat
docker system df

# Curățare resurse neutilizate
docker system prune -a
```

---

## Python — One-Liners pentru Rețele

```bash
# Server TCP simplu (echo)
python3 -c "
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
python3 -c "
import socket
s = socket.socket()
s.connect(('localhost', 9090))
s.send(b'Test')
print(s.recv(1024))
s.close()
"

# Server HTTP simplu (servește fișierele din directorul curent)
python3 -m http.server 8080
```

---

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
| Pornire lab | `docker compose up -d` |
| Oprire lab | `docker compose down` |

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix | 2025*
