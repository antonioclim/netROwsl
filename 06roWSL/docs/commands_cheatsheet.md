# Săptămâna 6: Fișă de comenzi

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Gestionarea laboratorului

### Pornirea mediului

```powershell
# Pornește toate serviciile
python scripts/start_lab.py

# Pornește cu controller SDN
python scripts/start_lab.py --controller

# Pornește cu Portainer
python scripts/start_lab.py --portainer

# Verifică starea
python scripts/start_lab.py --status
```

### Oprire și curățare

```powershell
# Oprire grațioasă (păstrează datele)
python scripts/stop_lab.py

# Curățare completă (elimină totul)
python scripts/cleanup.py --full

# Simulare (arată ce s-ar elimina)
python scripts/cleanup.py --full --dry-run
```

### Rularea demonstrațiilor

```powershell
# Listează demonstrațiile disponibile
python scripts/run_demo.py --list

# Rulează demonstrația NAT
python scripts/run_demo.py --demo nat

# Rulează demonstrația SDN
python scripts/run_demo.py --demo sdn
```

## Comenzi Mininet

### Operații de bază

```bash
# Pornește CLI-ul Mininet
sudo mn

# Pornește cu topologie specifică
sudo python3 topo_nat.py --cli
sudo python3 topo_sdn.py --cli

# Curăță Mininet
sudo mn -c
```

### În CLI-ul Mininet

```bash
# Listează nodurile
nodes

# Listează interfețele de rețea
net

# Testează conectivitatea
pingall

# Rulează comandă pe host
h1 ifconfig
h1 ping 10.0.6.12

# Deschide terminal pe host
xterm h1

# Afișează informații despre hosturi
dump
```

## Comenzi NAT/iptables

### Vizualizarea configurației NAT

```bash
# Afișează regulile NAT
iptables -t nat -L -n -v

# Afișează tabela conntrack
conntrack -L
cat /proc/net/nf_conntrack

# Afișează starea IP forwarding
sysctl net.ipv4.ip_forward
```

### Configurarea NAT

```bash
# Activează IP forwarding
sysctl -w net.ipv4.ip_forward=1

# Adaugă regulă MASQUERADE
iptables -t nat -A POSTROUTING -o eth1 -s 192.168.1.0/24 -j MASQUERADE

# Permite forwarding
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT

# Golește regulile NAT
iptables -t nat -F
```

## Comenzi Open vSwitch

### Operații de bază

```bash
# Afișează configurația OVS
ovs-vsctl show

# Listează bridge-urile
ovs-vsctl list-br

# Listează porturile pe bridge
ovs-vsctl list-ports s1

# Șterge bridge
ovs-vsctl del-br s1
```

### Gestionarea tabelelor de fluxuri (OpenFlow 1.3)

```bash
# Afișează toate fluxurile
ovs-ofctl -O OpenFlow13 dump-flows s1

# Afișează fluxurile sortate după pachete
ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=n_packets

# Adaugă o regulă de flux
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,icmp,nw_src=10.0.6.11,actions=drop"

# Șterge flux specific
ovs-ofctl -O OpenFlow13 del-flows s1 "priority=100,icmp,nw_src=10.0.6.11"

# Șterge toate fluxurile
ovs-ofctl -O OpenFlow13 del-flows s1

# Afișează descrierea switch-ului
ovs-ofctl -O OpenFlow13 dump-desc s1
```

### Sintaxa regulilor de flux

```bash
# Câmpuri de potrivire
priority=N              # Prioritatea regulii (mai mare = verificată prima)
in_port=N               # Numărul portului de intrare
eth_type=0x0800         # IPv4
eth_type=0x0806         # ARP
ip_proto=1              # ICMP
ip_proto=6              # TCP
ip_proto=17             # UDP
nw_src=IP               # IP sursă
nw_dst=IP               # IP destinație
tp_src=PORT             # Port sursă (TCP/UDP)
tp_dst=PORT             # Port destinație (TCP/UDP)

# Acțiuni
actions=output:N        # Ieșire pe portul N
actions=drop            # Aruncă pachetul
actions=NORMAL          # Folosește învățarea L2 normală
actions=CONTROLLER      # Trimite la controller
actions=flood           # Flood pe toate porturile
```

## Capturarea pachetelor

### tcpdump

```bash
# Capturează trafic ICMP
tcpdump -i eth0 icmp

# Capturează cu detalii
tcpdump -i eth0 -n -v icmp

# Salvează în fișier
tcpdump -i eth0 -w captura.pcap

# Filtrează după host
tcpdump -i eth0 host 10.0.6.11

# Filtrează după port
tcpdump -i eth0 port 9090
```

### tshark

```bash
# Capturează și afișează
tshark -i eth0

# Filtrează după protocol
tshark -i eth0 -f "icmp"

# Afișează câmpuri specifice
tshark -i eth0 -T fields -e ip.src -e ip.dst

# Citește fișier pcap
tshark -r captura.pcap

# Trafic OpenFlow
tshark -i lo -f "port 6633"
```

## Comenzi Docker

### Gestionarea containerelor

```bash
# Listează containerele care rulează
docker ps

# Listează toate containerele
docker ps -a

# Intră în shell-ul containerului
docker exec -it week6_lab bash

# Vizualizează logurile containerului
docker logs week6_lab

# Oprește containerul
docker stop week6_lab

# Elimină containerul
docker rm week6_lab
```

### Docker Compose

```bash
# Construiește imaginile
docker compose build

# Pornește serviciile
docker compose up -d

# Oprește serviciile
docker compose down

# Vizualizează logurile
docker compose logs -f

# Execută comandă în serviciu
docker compose exec week6-lab bash
```

## Diagnosticare rețea

### Testarea conectivității

```bash
# Ping de bază
ping -c 3 10.0.6.12

# Ping cu interfață specifică
ping -I eth0 10.0.6.12

# Traceroute
traceroute -n 10.0.6.12

# Verifică porturile în ascultare
ss -ltn

# Verifică conexiunile de rețea
ss -tn
```

### Configurarea interfețelor

```bash
# Afișează toate interfețele
ip addr show

# Afișează tabela de rutare
ip route show

# Adaugă rută statică
ip route add 10.0.6.0/24 via 192.168.1.1

# Afișează cache-ul ARP
ip neigh show
```

## Aplicații Săptămâna 6

### Echo TCP

```bash
# Server
python3 src/apps/tcp_echo.py server --bind 0.0.0.0 --port 9090

# Client
python3 src/apps/tcp_echo.py client --dst 10.0.6.12 --port 9090 --message "Salut"
```

### Echo UDP

```bash
# Server
python3 src/apps/udp_echo.py server --bind 0.0.0.0 --port 9091

# Client
python3 src/apps/udp_echo.py client --dst 10.0.6.12 --port 9091 --message "Salut"
```

### Observator NAT

```bash
# Server (pe hostul public)
python3 src/apps/nat_observer.py server --bind 203.0.113.2 --port 5000

# Client (de pe hostul privat)
python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Test"
```

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
