# Săptămâna 6: Ghid de depanare

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim

## Matrice de Diagnostic Rapid

| Simptom | Verificare 1 | Verificare 2 | Verificare 3 |
|---------|--------------|--------------|--------------|
| Container nu pornește | `docker logs <n>` | `docker inspect <n>` | `docker system df` |
| NAT nu funcționează | `sysctl net.ipv4.ip_forward` | `iptables -t nat -L` | `conntrack -L` |
| SDN timeout | `ss -ltn \| grep 6633` | `ovs-vsctl show` | `ovs-ofctl dump-flows s1` |
| Wireshark gol | Interfața corectă? | Filtru prea restrictiv? | Trafic generat? |
| Ping lent | Verifică ARP | Verifică fluxuri | Verifică controller logs |

---

## Probleme Docker

### Docker nu pornește

**Soluții:**
1. Asigură-te că Docker Desktop rulează
2. Verifică integrarea WSL2: Docker Desktop → Settings → Resources → WSL Integration

### Erori la containerele privilegiate

**Soluții:**
1. Verifică că `privileged: true` este setat în docker-compose.yml
2. Repornește Docker Desktop

---

## Probleme Mininet

### Eroare "File exists" la pornire

**Soluții:**
```bash
sudo mn -c
sudo ip link delete s1-eth1 2>/dev/null
sudo pkill -9 ovs
```

### "OVS switch failed to connect"

**Soluții:**
1. Verifică dacă controller-ul rulează:
   ```bash
   ss -ltn | grep 6633
   ```
2. Verifică configurația OVS:
   ```bash
   ovs-vsctl show
   ```

### Ping foarte lent sau timeout

**Soluții:**
1. Verifică dacă regulile de flux sunt instalate:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1
   ```
2. Asigură-te că ARP funcționează

---

## Arbore de Decizie: "Nu merge ping-ul în SDN"

```
ping h1 → h2 eșuează
│
├─► ARP funcționează?
│   ├─► NU: ovs-ofctl dump-flows s1 | grep arp
│   └─► DA: Continuă ↓
│
├─► Există flux pentru IP?
│   ├─► NU: Verifică logurile controller-ului
│   └─► DA: Verifică prioritatea regulilor
│
└─► Traficul ajunge la destinație?
    tcpdump -i s1-eth2 icmp
```

---

## Probleme NAT

### NAT nu traduce pachetele

**Soluții:**
1. Verifică IP forwarding:
   ```bash
   sysctl net.ipv4.ip_forward
   sudo sysctl -w net.ipv4.ip_forward=1
   ```

2. Verifică regula MASQUERADE:
   ```bash
   iptables -t nat -L -n -v | grep MASQUERADE
   ```

3. Verifică rutarea pe hosturile private:
   ```bash
   ip route
   ```

### Arbore de Decizie: "NAT nu funcționează"

```
h1 (privat) nu poate ajunge la h3 (public)
│
├─► IP forwarding activat?
│   sysctl net.ipv4.ip_forward
│   ├─► 0: sudo sysctl -w net.ipv4.ip_forward=1
│   └─► 1: Continuă ↓
│
├─► Există regulă MASQUERADE?
│   iptables -t nat -L POSTROUTING -n -v
│   ├─► NU: Adaugă regula
│   └─► DA: Continuă ↓
│
└─► Pachetele ajung la router?
    tcpdump -i eth0 -n host 192.168.1.10
```

---

## Probleme SDN

### Controller-ul nu primește evenimente packet-in

**Soluții:**
1. Verifică conexiunea switch-controller:
   ```bash
   ovs-vsctl show
   ```

2. Verifică versiunea OpenFlow:
   ```bash
   ovs-vsctl get bridge s1 protocols
   ```

### Fluxurile nu potrivesc traficul

**Soluții:**
1. Verifică criteriile de potrivire
2. Verifică prioritatea regulilor:
   ```bash
   ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=priority
   ```

---

## Comenzi de Debugging Avansate

### NAT

```bash
conntrack -L -n
conntrack -L -p tcp
conntrack -E
cat /proc/net/stat/nf_conntrack
iptables -t nat -L -n -v --line-numbers
```

### OpenFlow

```bash
ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=n_packets
ovs-ofctl -O OpenFlow13 dump-ports-desc s1
ovs-ofctl -O OpenFlow13 dump-aggregate s1
ovs-ofctl -O OpenFlow13 snoop s1
ovs-vsctl show
```

### Docker

```bash
docker network inspect week6_network
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' week6_lab
docker logs -f week6_lab
docker exec -it week6_lab bash
docker stats week6_lab
```

---

## Obținerea ajutorului

1. Verifică mesajul de eroare cu atenție
2. Caută pe forumurile cursului
3. Verifică logurile:
   ```bash
   docker compose logs
   journalctl -u openvswitch-switch
   ```
4. Întreabă în timpul orelor de laborator

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim*
