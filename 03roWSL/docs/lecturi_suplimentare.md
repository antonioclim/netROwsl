# Lecturi Suplimentare - Săptămâna 3

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## RFC-uri (Request for Comments)

### Broadcast

| RFC | Titlu | Descriere |
|-----|-------|-----------|
| RFC 919 | Broadcasting Internet Datagrams | Specificația de bază pentru broadcast |
| RFC 922 | Broadcasting Internet Datagrams in the Presence of Subnets | Extindere pentru rețele cu subnetting |

### Multicast

| RFC | Titlu | Descriere |
|-----|-------|-----------|
| RFC 1112 | Host Extensions for IP Multicasting | Specificația de bază pentru multicast IP |
| RFC 2236 | Internet Group Management Protocol, Version 2 | IGMPv2 cu mesaje Leave |
| RFC 3376 | Internet Group Management Protocol, Version 3 | IGMPv3 cu Source-Specific Multicast |
| RFC 5771 | IANA Guidelines for IPv4 Multicast Address Assignments | Ghid pentru alocarea adreselor multicast |

### Protocoale de Transport

| RFC | Titlu | Descriere |
|-----|-------|-----------|
| RFC 793 | Transmission Control Protocol | Specificația TCP |
| RFC 768 | User Datagram Protocol | Specificația UDP |

---

## Cărți și Manuale

### Fundamental

1. **Kurose, J. & Ross, K.** (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson.
   - Capitolul 4: Stratul de Rețea - Planul de Date
   - Excelent pentru înțelegerea conceptelor de rutare și forwarding

2. **Stevens, W. R., Fenner, B., & Rudoff, A.** (2004). *UNIX Network Programming, Vol. 1: The Sockets Networking API* (ed. 3). Addison-Wesley.
   - Capitolul 21: Multicasting
   - Referință definitiv pentru programarea socket-urilor

3. **Rhodes, B. & Goetzen, J.** (2014). *Foundations of Python Network Programming* (ed. 3). Apress.
   - Capitolul 3: UDP
   - Exemple practice în Python

### Avansat

4. **Tanenbaum, A. & Wetherall, D.** (2011). *Computer Networks* (ed. 5). Pearson.
   - Perspectivă detaliată asupra protocoalelor de rețea

5. **Comer, D.** (2013). *Internetworking with TCP/IP, Vol. 1* (ed. 6). Pearson.
   - Tratare riguroasă a stivei TCP/IP

---

## Resurse Online

### Documentație Oficială

- **Python socket module**: https://docs.python.org/3/library/socket.html
- **Python struct module**: https://docs.python.org/3/library/struct.html
- **Docker Networking**: https://docs.docker.com/network/
- **Wireshark User Guide**: https://www.wireshark.org/docs/

### Tutoriale și Ghiduri

- **Beej's Guide to Network Programming**: https://beej.us/guide/bgnet/
  - Ghid clasic pentru programarea socket-urilor (C, dar conceptele se aplică)

- **Real Python - Socket Programming**: https://realpython.com/python-sockets/
  - Tutorial modern pentru Python

---

## Articole Academice

### Multicast

1. **Deering, S.** (1988). *Host Extensions for IP Multicasting*. RFC 1112.
   - Lucrarea fundamentală pentru multicast IP

2. **Holbrook, H. & Cain, B.** (2006). *Source-Specific Multicast for IP*. RFC 4607.
   - SSM pentru securitate îmbunătățită

### Protocoale de Descoperire

3. **Cheshire, S. & Krochmal, M.** (2013). *Multicast DNS*. RFC 6762.
   - Baza pentru Bonjour/Avahi

---

## Concepte Înrudite pentru Studiu

### Protocoale de Descoperire Servicii

- **mDNS (Multicast DNS)**: Rezoluție de nume în rețele locale fără server DNS
- **DNS-SD (DNS Service Discovery)**: Descoperirea serviciilor peste DNS
- **SSDP (Simple Service Discovery Protocol)**: Folosit de UPnP

### Protocoale de Configurare Automată

- **BOOTP**: Bootstrap Protocol (predecesor DHCP)
- **DHCP**: Dynamic Host Configuration Protocol
- **APIPA**: Automatic Private IP Addressing (169.254.x.x)

### Multicast în Aplicații

- **RTP/RTCP**: Real-time Transport Protocol pentru streaming
- **PGM/NORM**: Protocoale multicast fiabile
- **PIM-SM**: Protocol Independent Multicast - Sparse Mode

### Tunelare și VPN

- **SSH Tunneling**: Port forwarding prin SSH
- **SOCKS5**: Proxy protocol cu suport UDP
- **WireGuard**: VPN modern și eficient
- **OpenVPN**: VPN bazat pe SSL/TLS

### Încapsulare și Overlay Networks

- **VXLAN**: Virtual Extensible LAN
- **GRE**: Generic Routing Encapsulation
- **IPsec**: IP Security pentru VPN-uri

---

## Instrumente și Biblioteci

### Analiză și Captură

| Instrument | Descriere |
|------------|-----------|
| Wireshark | Analizor de protocoale cu interfață grafică |
| tcpdump | Captură de pachete în linia de comandă |
| tshark | Versiunea CLI a Wireshark |
| Scapy | Manipulare pachete în Python |

### Testare Rețea

| Instrument | Descriere |
|------------|-----------|
| netcat (nc) | "Swiss army knife" pentru rețea |
| nmap | Scanner de porturi și rețele |
| iperf3 | Testare throughput |
| hping3 | Generare pachete personalizate |

### Simulare și Emulare

| Instrument | Descriere |
|------------|-----------|
| Mininet | Emulator de rețele SDN |
| GNS3 | Simulator de rețele complexe |
| Docker | Containere pentru izolarea mediilor |

---

## Proiecte Practice Recomandate

### Nivel Începător

1. **Chat LAN cu Broadcast**
   - Implementați un chat simplu folosind broadcast UDP
   - Extindeți cu nickname-uri și timestamps

2. **VPN Simplu**
   - Creați un tunel TCP care criptează traficul
   - Folosiți biblioteca `cryptography` pentru criptare

### Nivel Intermediar

3. **Service Discovery**
   - Implementați un protocol de descoperire servicii
   - Folosiți multicast pentru anunțuri

4. **File Sharing P2P**
   - Distribuție de fișiere folosind multicast
   - Confirmări și retransmisii pentru fiabilitate

### Nivel Avansat

5. **Load Balancer**
   - Extindeți tunelul TCP pentru a distribui conexiunile
   - Implementați round-robin sau least-connections

6. **Network Monitor**
   - Captură și analiză trafic în timp real
   - Statistici și alertare pe anomalii

---

## Exerciții de Gândire

1. **De ce broadcast-ul nu traversează routere?**
   - Răspuns: Routerele nu transmit pachete broadcast pentru a limita domeniile de broadcast și a preveni storm-urile de broadcast.

2. **Care este avantajul multicast-ului față de transmisii multiple unicast?**
   - Răspuns: Emițătorul trimite o singură copie, rețeaua duplică doar unde este necesar.

3. **De ce TTL=1 pentru trafic multicast local?**
   - Răspuns: Previne propagarea accidentală a traficului în afara rețelei locale.

4. **Ce probleme rezolvă un tunel TCP?**
   - Răspuns: NAT traversal, securitate (când e criptat), abstractizare endpoint, load balancing.

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
