# Glosar de Termeni - Săptămâna 7

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix
> 
> Referință rapidă pentru terminologia utilizată în laborator

---

## A-D

| Termen | Definiție | Context |
|--------|-----------|---------|
| **ACK** | Acknowledge — confirmare de primire în TCP | Handshake, transfer date |
| **BPF** | Berkeley Packet Filter — limbaj pentru filtre de captură | tcpdump, Wireshark capture filter |
| **Bridge** | Rețea virtuală Docker care conectează containere | `docker network create` |
| **DROP** | Acțiune iptables: elimină pachetul silențios, fără răspuns | Firewall "stealth" |
| **DESCHIS** | Stare port: serviciu activ, acceptă conexiuni | Rezultat sondare: SYN-ACK |

## F-I

| Termen | Definiție | Context |
|--------|-----------|---------|
| **FILTRAT** | Stare port: firewall blochează, nu se poate determina dacă e serviciu | Rezultat sondare: timeout |
| **FIN** | Flag TCP pentru închiderea grațioasă a conexiunii | Terminare conexiune |
| **Handshake** | Secvența SYN → SYN-ACK → ACK pentru stabilirea conexiunii TCP | Începutul oricărei conexiuni TCP |
| **ICMP** | Internet Control Message Protocol — mesaje de eroare și diagnostic | ping, traceroute, REJECT |
| **ÎNCHIS** | Stare port: niciun serviciu, dar sistemul răspunde cu RST | Rezultat sondare: RST |
| **iptables** | Utilitar Linux pentru configurarea regulilor Netfilter | `iptables -A INPUT -j DROP` |

## L-P

| Termen | Definiție | Context |
|--------|-----------|---------|
| **Layer 7** | Nivelul Aplicație din modelul OSI — HTTP, DNS, FTP | Filtrare conținut, WAF |
| **Netfilter** | Framework de filtrare pachete în kernelul Linux | Backend pentru iptables |
| **PCAP** | Packet Capture — format standard pentru salvarea capturilor | Fișiere `.pcap`, `.pcapng` |
| **Portainer** | Interfață web pentru gestionarea Docker | http://localhost:9000 |
| **Proxy** | Intermediar care inspectează și poate modifica traficul | Filtru nivel aplicație |

## R-Z

| Termen | Definiție | Context |
|--------|-----------|---------|
| **REJECT** | Acțiune iptables: respinge pachetul cu răspuns explicit (RST/ICMP) | Firewall "polite" |
| **RST** | Reset — flag TCP care termină brusc conexiunea | REJECT, port închis |
| **Sondare** | Tehnica de identificare a serviciilor active pe un sistem | nmap, sonda_porturi.py |
| **SYN** | Synchronize — primul pas în handshake-ul TCP | Inițiere conexiune |
| **tshark** | Versiunea CLI a Wireshark pentru scripturi și automatizare | Captură în terminal |
| **Wireshark** | Analizor grafic de protocoale de rețea | Interfață GUI principală |
| **WSL** | Windows Subsystem for Linux — Linux în Windows | Mediul de laborator |

---

## Comenzi Frecvente

| Comandă | Descriere |
|---------|-----------|
| `docker ps` | Listează containerele active |
| `docker logs <container>` | Afișează jurnalele containerului |
| `docker exec -it <container> bash` | Intră în shell-ul containerului |
| `iptables -L -n` | Listează regulile firewall |
| `iptables -F` | Șterge toate regulile |
| `tcpdump -i eth0` | Captură pachete pe interfață |
| `tcpdump -w fisier.pcap` | Salvează captura în fișier |
| `nc -zv host port` | Test conectivitate TCP |
| `nc -u host port` | Conexiune UDP |

---

## Filtre Wireshark Utile

### Filtre de Bază

| Filtru | Scop |
|--------|------|
| `tcp.port == 9090` | Trafic pe portul TCP 9090 |
| `udp.port == 9091` | Trafic pe portul UDP 9091 |
| `ip.addr == 10.0.7.100` | Trafic de la/către IP specificat |
| `tcp or udp` | Tot traficul TCP și UDP |

### Filtre pentru Handshake TCP

| Filtru | Scop |
|--------|------|
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Doar SYN inițial |
| `tcp.flags.syn == 1` | SYN și SYN-ACK |
| `tcp.flags.fin == 1` | Pachete de închidere conexiune |

### Filtre pentru Diagnosticare

| Filtru | Scop |
|--------|------|
| `tcp.flags.reset == 1` | Pachete RST (REJECT sau eroare) |
| `icmp.type == 3` | ICMP Destination Unreachable |
| `tcp.analysis.retransmission` | Retransmisii (indiciu de DROP) |
| `tcp.analysis.duplicate_ack` | ACK-uri duplicate |

### Filtre Combinate

| Filtru | Scop |
|--------|------|
| `tcp.port == 9090 or udp.port == 9091` | Tot traficul laboratorului |
| `tcp.port == 9090 && tcp.flags.syn` | Handshake-uri pe portul echo |
| `!arp && !dns && !mdns` | Exclude traficul de fundal |

---

## Stări Porturi (Rezultate Sondare)

| Stare | Răspuns Primit | Interpretare |
|-------|----------------|--------------|
| **DESCHIS** | SYN-ACK | Serviciu activ, acceptă conexiuni |
| **ÎNCHIS** | RST | Niciun serviciu, niciun firewall |
| **FILTRAT** | Timeout sau ICMP | Firewall DROP sau REJECT |

---

## Acțiuni iptables

| Acțiune | Efect | Răspuns Trimis | Când să Folosești |
|---------|-------|----------------|-------------------|
| **ACCEPT** | Permite pachetul | - | Trafic legitimate |
| **DROP** | Elimină silențios | Niciunul | Securitate maximă |
| **REJECT** | Respinge explicit | RST/ICMP | Depanare, rețea internă |

---

## Resurse Externe

- [Documentație Wireshark](https://www.wireshark.org/docs/)
- [Manual iptables](https://netfilter.org/documentation/)
- [Referință tcpdump](https://www.tcpdump.org/manpages/tcpdump.1.html)
- [Docker Networking](https://docs.docker.com/network/)

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
