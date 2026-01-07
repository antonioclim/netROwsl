# Săptămâna 6: Lectură suplimentară

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Cărți

### Fundamente de rețelistică

- **Kurose, J. & Ross, K.** (2016). *Computer Networking: A Top-Down Approach* (ediția a 7-a). Pearson.
  - Capitolele despre stratul de rețea, în special secțiunile NAT și ICMP
  - Explicații clare cu exemple practice

- **Tanenbaum, A. & Wetherall, D.** (2011). *Computer Networks* (ediția a 5-a). Pearson.
  - Acoperire comprehensivă a protocoalelor de rețea
  - Discuție detaliată despre adresarea IP și rutare

### Programare de rețea

- **Rhodes, B. & Goetzen, J.** (2014). *Foundations of Python Network Programming* (ediția a 3-a). Apress.
  - Exemple practice în Python pentru aplicații de rețea
  - Programare cu socket-uri și implementare de protocoale

### Rețele definite prin software

- **Goransson, P. & Black, C.** (2014). *Software Defined Networks: A Comprehensive Approach*. Morgan Kaufmann.
  - Excelentă introducere în arhitectura SDN
  - Detalii despre protocolul OpenFlow

- **Nadeau, T. & Gray, K.** (2013). *SDN: Software Defined Networks*. O'Reilly Media.
  - Perspectiva industriei asupra adoptării SDN
  - Considerații practice de implementare

## RFC-uri (Request for Comments)

### NAT și adresare

- **RFC 1918** - Alocarea adreselor pentru rețele private
  - Definește intervalele de adrese private (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
  - https://datatracker.ietf.org/doc/html/rfc1918

- **RFC 3022** - Translatorul tradițional de adrese de rețea IP
  - Definește terminologia și operarea NAT de bază
  - https://datatracker.ietf.org/doc/html/rfc3022

- **RFC 5737** - Blocuri de adrese IPv4 rezervate pentru documentație
  - Definește adresele TEST-NET (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24)
  - https://datatracker.ietf.org/doc/html/rfc5737

### Protocoale suport

- **RFC 826** - Address Resolution Protocol (ARP)
  - Specificația originală ARP
  - https://datatracker.ietf.org/doc/html/rfc826

- **RFC 2131** - Dynamic Host Configuration Protocol (DHCP)
  - Operarea DHCP și formatele mesajelor
  - https://datatracker.ietf.org/doc/html/rfc2131

- **RFC 792** - Internet Control Message Protocol (ICMP)
  - Tipuri de mesaje ICMP și gestionarea erorilor
  - https://datatracker.ietf.org/doc/html/rfc792

- **RFC 4861** - Neighbor Discovery pentru IPv6 (NDP)
  - Rezoluția adreselor IPv6 și descoperirea routerelor
  - https://datatracker.ietf.org/doc/html/rfc4861

## Standarde OpenFlow și SDN

- **OpenFlow Switch Specification 1.3.5** - Open Networking Foundation
  - Specificația protocolului pentru comunicarea controller-switch
  - https://opennetworking.org/wp-content/uploads/2014/10/openflow-spec-v1.3.5.pdf

- **OpenFlow Table Type Patterns** - Recomandare tehnică ONF
  - Cele mai bune practici pentru proiectarea tabelelor de flux

## Resurse online

### Mininet

- **Site-ul oficial Mininet**
  - http://mininet.org/
  - Tutoriale, documentație și exemple

- **Mininet Walkthrough**
  - http://mininet.org/walkthrough/
  - Introducere pas cu pas

- **Repository GitHub Mininet**
  - https://github.com/mininet/mininet
  - Cod sursă și tracker de probleme

### Open vSwitch

- **Documentație Open vSwitch**
  - https://docs.openvswitch.org/
  - Referință comprehensivă pentru OVS

- **Pagini de manual OVS**
  - Referințe pentru comenzile ovs-ofctl, ovs-vsctl
  - Disponibile via `man ovs-ofctl`

### OS-Ken (Fork Ryu)

- **Documentație OS-Ken**
  - https://osrg.github.io/os-ken/
  - Ghid de dezvoltare controller

- **Repository GitHub OS-Ken**
  - https://github.com/faucetsdn/os-ken
  - Cod sursă și exemple

### Wireshark

- **Ghidul utilizatorului Wireshark**
  - https://www.wireshark.org/docs/wsug_html_chunked/
  - Documentație completă de utilizare

- **Referință filtre de afișare Wireshark**
  - https://www.wireshark.org/docs/dfref/
  - Sintaxa filtrelor pentru toate protocoalele

## Resurse video

### Stanford Online

- **Introduction to Computer Networking** (CS144)
  - Curs gratuit care acoperă fundamentele rețelelor
  - https://online.stanford.edu/courses/cs144-introduction-computer-networking

### Canale YouTube

- **Computerphile**
  - Explicații accesibile ale conceptelor de rețea
  - Explicații NAT, rutare și protocoale

- **David Bombal**
  - Tutoriale practice de rețelistică
  - Conținut SDN și automatizare

## Platforme de practică

### GNS3

- Platformă de simulare rețea
- https://www.gns3.com/

### Packet Tracer

- Instrument de simulare rețea Cisco
- Bun pentru practică de rutare și switching

### Kathará

- Emulare de rețea bazată pe containere
- https://www.kathara.org/

## Articole academice

### Traversare NAT

- **Ford, B., Srisuresh, P., & Kegel, D.** (2005). "Peer-to-Peer Communication Across Network Address Translators". USENIX ATC.
  - Tehnici de traversare NAT pentru aplicații P2P

### Cercetare SDN

- **McKeown, N., et al.** (2008). "OpenFlow: Enabling Innovation in Campus Networks". ACM SIGCOMM CCR.
  - Articol fondator despre OpenFlow

- **Kreutz, D., et al.** (2015). "Software-Defined Networking: A Comprehensive Survey". Proceedings of the IEEE.
  - Privire de ansamblu comprehensivă asupra peisajului SDN

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
