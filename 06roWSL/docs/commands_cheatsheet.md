# Săptămâna 6: Fișă de comenzi

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim

## Gestionarea laboratorului

### Pornirea mediului

```bash
python3 scripts/start_lab.py
python3 scripts/start_lab.py --controller
python3 scripts/start_lab.py --status
python3 scripts/start_lab.py --rebuild
```

### Oprire și curățare

```bash
python3 scripts/stop_lab.py
python3 scripts/cleanup.py --full
python3 scripts/cleanup.py --full --dry-run
```

### Rularea demonstrațiilor

```bash
python3 scripts/run_demo.py --list
python3 scripts/run_demo.py --demo nat
python3 scripts/run_demo.py --demo sdn
```

---

## Comenzi Mininet

### Operații de bază

```bash
sudo mn
sudo python3 topo_nat.py --cli
sudo python3 topo_sdn.py --cli
sudo mn -c
```

### În CLI-ul Mininet

```bash
nodes
net
pingall
h1 ifconfig
h1 ping 10.0.6.12
xterm h1
dump
exit
```

---

## Comenzi NAT/iptables

### Vizualizare

```bash
iptables -t nat -L -n -v
iptables -t nat -L -n -v --line-numbers
conntrack -L
cat /proc/net/nf_conntrack
sysctl net.ipv4.ip_forward
conntrack -C
```

### Configurare

```bash
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -o eth1 -s 192.168.1.0/24 -j MASQUERADE
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -t nat -F
```

### Debugging avansat

```bash
conntrack -L -n
conntrack -L -p tcp
conntrack -E
cat /proc/net/stat/nf_conntrack
```

---

## Comenzi Open vSwitch

### Operații de bază

```bash
ovs-vsctl show
ovs-vsctl list-br
ovs-vsctl list-ports s1
ovs-vsctl del-br s1
```

### Gestionarea fluxurilor (OpenFlow 1.3)

```bash
ovs-ofctl -O OpenFlow13 dump-flows s1
ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=n_packets
ovs-ofctl -O OpenFlow13 add-flow s1 "priority=100,icmp,nw_src=10.0.6.11,actions=drop"
ovs-ofctl -O OpenFlow13 del-flows s1 "priority=100,icmp,nw_src=10.0.6.11"
ovs-ofctl -O OpenFlow13 del-flows s1
ovs-ofctl -O OpenFlow13 dump-desc s1
```

### Debugging avansat

```bash
ovs-ofctl -O OpenFlow13 dump-ports-desc s1
ovs-ofctl -O OpenFlow13 dump-aggregate s1
ovs-ofctl -O OpenFlow13 snoop s1
ovs-vsctl get-controller s1
```

### Sintaxa regulilor de flux

```bash
# Câmpuri de potrivire
priority=N              # Prioritatea regulii
in_port=N               # Portul de intrare
eth_type=0x0800         # IPv4
eth_type=0x0806         # ARP
ip_proto=1              # ICMP
ip_proto=6              # TCP
ip_proto=17             # UDP
nw_src=IP               # IP sursă
nw_dst=IP               # IP destinație
tp_src=PORT             # Port sursă
tp_dst=PORT             # Port destinație

# Acțiuni
actions=output:N        # Ieșire pe portul N
actions=drop            # Aruncă pachetul
actions=NORMAL          # Învățare L2 normală
actions=CONTROLLER      # Trimite la controller
actions=flood           # Flood pe toate porturile
```

---

## Capturarea pachetelor

### tcpdump

```bash
tcpdump -i eth0 icmp
tcpdump -i eth0 -n -v icmp
tcpdump -i eth0 -w captura.pcap
tcpdump -i eth0 host 10.0.6.11
tcpdump -i eth0 port 9090
tcpdump -i eth0 net 192.168.1.0/24
tcpdump -i eth0 'host 10.0.6.11 and port 9090'
```

### tshark

```bash
tshark -i eth0
tshark -i eth0 -f "icmp"
tshark -i eth0 -T fields -e ip.src -e ip.dst
tshark -r captura.pcap
tshark -i lo -f "port 6633"
```

---

## Comenzi Docker

### Gestionarea containerelor

```bash
docker ps
docker ps -a
docker exec -it week6_lab bash
docker logs week6_lab
docker logs -f week6_lab
docker stop week6_lab
docker rm week6_lab
docker stats week6_lab
```

### Docker Compose

```bash
docker compose build
docker compose up -d
docker compose down
docker compose logs -f
docker compose exec week6-lab bash
```

### Debugging

```bash
docker network inspect week6_network
docker inspect week6_lab
docker system df
docker system prune -f
```

---

## Diagnosticare rețea

### Testare conectivitate

```bash
ping -c 3 10.0.6.12
ping -I eth0 10.0.6.12
traceroute -n 10.0.6.12
ss -ltn
ss -tn
ss -ltn | grep 6633
```

### Configurare interfețe

```bash
ip addr show
ip route show
ip route add 10.0.6.0/24 via 192.168.1.1
ip neigh show
ip -s link show eth0
```

---

## Aplicații Săptămâna 6

### Echo TCP

```bash
python3 src/apps/tcp_echo.py server --bind 0.0.0.0 --port 9090
python3 src/apps/tcp_echo.py client --host 10.0.6.12 --port 9090 --message "Salut"
```

### Echo UDP

```bash
python3 src/apps/udp_echo.py server --bind 0.0.0.0 --port 9091
python3 src/apps/udp_echo.py client --host 10.0.6.12 --port 9091 --message "Salut"
```

### Observator NAT

```bash
python3 src/apps/nat_observer.py server --bind 203.0.113.2 --port 5000
python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Test"
```

---

## Referință rapidă: Porturi

| Port | Protocol | Utilizare |
|------|----------|-----------|
| 9000 | TCP | Portainer (NU MODIFICA!) |
| 9090 | TCP | Echo TCP |
| 9091 | UDP | Echo UDP |
| 6633 | TCP | OpenFlow (legacy) |
| 6653 | TCP | OpenFlow (standard) |
| 5000 | TCP | Observator NAT |

## Referință rapidă: Adrese IP

| Host | IP SDN | IP NAT |
|------|--------|--------|
| h1 | 10.0.6.11 | 192.168.1.10 |
| h2 | 10.0.6.12 | 192.168.1.20 |
| h3 | 10.0.6.13 | 203.0.113.2 |
| rnat | - | 192.168.1.1 / 203.0.113.1 |

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim*
