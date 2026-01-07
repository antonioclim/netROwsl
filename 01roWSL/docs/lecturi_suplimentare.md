# Lecturi Suplimentare - Săptămâna 1

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## Cărți Recomandate

### Fundamentele Rețelelor

| Titlu | Autori | Descriere |
|-------|--------|-----------|
| *Computer Networking: A Top-Down Approach* | Kurose & Ross | Abordare de sus în jos a stivei de protocoale. Excelentă pentru începători. |
| *Computer Networks* | Tanenbaum & Wetherall | Referință clasică și completă. Acoperire detaliată a tuturor aspectelor. |
| *TCP/IP Illustrated, Vol. 1* | W. Richard Stevens | Analiza în detaliu a protocoalelor TCP/IP. Standard în industrie. |

### Programarea Rețelelor în Python

| Titlu | Autori | Descriere |
|-------|--------|-----------|
| *Foundations of Python Network Programming* | Rhodes & Goetzen | Ghid complet pentru programarea socket-urilor în Python. |
| *Black Hat Python* | Justin Seitz | Programare de securitate și rețele. Proiecte practice. |

## Cursuri Online

### Gratuite

- **Stanford - Introduction to Computer Networking**
  - Platformă: Stanford Online
  - Nivel: Intermediar
  - URL: https://online.stanford.edu/

- **Cisco Networking Academy (NetAcad)**
  - Platformă: NetAcad.com
  - Nivel: Începător → Avansat
  - Certificări: CCNA
  - URL: https://www.netacad.com/

### Resurse Video

- **Computerphile (YouTube)**
  - Explicații simple ale conceptelor complexe
  - Subiecte: DNS, TCP, Routing, Security

- **Ben Eater (YouTube)**
  - Explicații hardware și low-level
  - Proiecte DIY de rețele

## Documente RFC Esențiale

RFC-urile (Request for Comments) sunt specificațiile oficiale ale protocoalelor Internet.

| RFC | Protocol | Descriere |
|-----|----------|-----------|
| RFC 791 | IP | Internet Protocol - adresarea și rutarea |
| RFC 793 | TCP | Transmission Control Protocol |
| RFC 768 | UDP | User Datagram Protocol |
| RFC 826 | ARP | Address Resolution Protocol |
| RFC 792 | ICMP | Internet Control Message Protocol |
| RFC 1918 | - | Adresele IP private |
| RFC 2616 | HTTP/1.1 | Hypertext Transfer Protocol |

**Unde să citiți RFC-uri:**
- https://www.rfc-editor.org/
- https://datatracker.ietf.org/

## Documentații Instrumente

### Wireshark

- **Ghid utilizator oficial**: https://www.wireshark.org/docs/wsug_html/
- **Wiki Wireshark**: https://wiki.wireshark.org/
- **Sample captures**: https://wiki.wireshark.org/SampleCaptures

### iproute2 (ip, ss)

- **Manual ip**: `man ip`
- **Manual ss**: `man ss`
- **Documentație oficială**: https://wiki.linuxfoundation.org/networking/iproute2

### tcpdump

- **Manual tcpdump**: `man tcpdump`
- **Ghid practic**: https://danielmiessler.com/study/tcpdump/
- **Filtre BPF**: `man pcap-filter`

### Python socket

- **Documentație oficială**: https://docs.python.org/3/library/socket.html
- **HOWTO Socket**: https://docs.python.org/3/howto/sockets.html

### Scapy

- **Documentație oficială**: https://scapy.readthedocs.io/
- **Tutorial interactiv**: https://scapy.readthedocs.io/en/latest/usage.html

## Platforme de Practică

### Capturi de Rețea

- **Wireshark Sample Captures**
  - https://wiki.wireshark.org/SampleCaptures
  - Capturi reale pentru analiză

- **Malware Traffic Analysis**
  - https://www.malware-traffic-analysis.net/
  - Capturi de trafic malware (pentru analiză de securitate)

### Simulatoare de Rețea

- **GNS3**
  - Emulator de echipamente de rețea
  - https://www.gns3.com/

- **Cisco Packet Tracer**
  - Simulator de rețele Cisco
  - Gratuit prin NetAcad

- **Mininet**
  - Simulator SDN (Software Defined Networking)
  - http://mininet.org/

### CTF (Capture The Flag)

- **PicoCTF**: https://picoctf.org/
- **OverTheWire**: https://overthewire.org/wargames/

## Bloguri și Articole

### Bloguri Recomandate

- **Julia Evans** (jvns.ca)
  - Explicații vizuale ale conceptelor de rețea
  - Zine-uri despre networking

- **The TCP/IP Guide**
  - http://www.tcpipguide.com/
  - Referință completă și gratuită

- **Beej's Guide to Network Programming**
  - https://beej.us/guide/bgnet/
  - Clasic pentru programare socket în C

### Articole Academice

- **End-to-End Arguments in System Design**
  - Saltzer, Reed, Clark (1984)
  - Principiul de bază al designului Internet

- **The Design Philosophy of the DARPA Internet Protocols**
  - David D. Clark (1988)
  - Istoria și principiile Internetului

## Resurse în Limba Română

### Cărți

- **Rețele de Calculatoare** - Tanenbaum (traducere)
- **Protocoale de Comunicație** - diverse universități

### Materiale Online

- **Wikipedia în română**: articole despre TCP/IP, Ethernet, etc.
- **Cursuri universitare**: ASE, UPB, Unibuc

## Parcurs Recomandat pentru Săptămâna 1

1. **Primul pas**: Citiți capitolele 1-2 din Kurose & Ross
2. **Aprofundare**: Studiați RFC 791 (IP) și RFC 793 (TCP)
3. **Practică**: Folosiți Wireshark pentru a analiza traficul real
4. **Programare**: Parcurgeți documentația Python socket
5. **Proiect**: Implementați un server-client simplu

## Următorii Pași

După finalizarea Săptămânii 1, continuați cu:

- **Săptămâna 2**: Protocoale de nivel aplicație (HTTP, DNS)
- **Săptămâna 3**: Rutare și switching
- **Săptămâna 4**: Securitatea rețelelor

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
