# Glosar de Termeni - Rețele de Calculatoare

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix
>
> Săptămâna 14: Recapitulare Integrată

Acest document conține definițiile termenilor tehnici folosiți în materialele de laborator.

---

## A

### ACK (Acknowledgment)
Flag TCP care confirmă primirea datelor. În handshake, `ACK=x+1` înseamnă "am primit până la numărul de secvență x".

### ARP (Address Resolution Protocol)
Protocol care rezolvă adrese IP în adrese MAC în rețeaua locală. Folosește broadcast pentru a întreba "Cine are IP-ul X?".

---

## B

### Backend
Server care procesează efectiv cererile, ascuns în spatele unui load balancer sau proxy. În laboratorul nostru: `week14_app1`, `week14_app2`.

### Bridge Network
Tip de rețea Docker care izolează containerele dar le permite să comunice între ele. Implicit, Docker creează rețeaua `bridge`.

### Broadcast
Transmisie către toate dispozitivele din rețea. Adresa de broadcast pentru 192.168.1.0/24 este 192.168.1.255.

---

## C

### CIDR (Classless Inter-Domain Routing)
Notație pentru adrese IP cu prefix de rețea. Exemplu: `192.168.1.0/24` = primii 24 biți sunt adresa de rețea.

### Container
Unitate de execuție izolată care împarte kernel-ul cu host-ul. Nu este o mașină virtuală - e mai ușor și pornește mai rapid.

### Connection Refused
Eroare TCP care apare când portul destinație nu are niciun proces care să asculte. Returnează RST imediat.

---

## D

### Daemon
Proces care rulează în fundal. `dockerd` este daemon-ul Docker.

### DHCP (Dynamic Host Configuration Protocol)
Protocol care atribuie automat adrese IP dispozitivelor din rețea.

### DNS (Domain Name System)
Sistem care traduce nume de domenii (ex: google.com) în adrese IP. Folosește portul 53.

### Docker Compose
Instrument pentru definirea și rularea aplicațiilor Docker multi-container folosind fișiere YAML.

### Dockerfile
Fișier text cu instrucțiuni pentru construirea unei imagini Docker.

---

## E

### Echo Server
Server care returnează exact datele primite. Folosit pentru testarea conectivității. RFC 862.

### Ephemeral Port
Port temporar alocat automat de sistem pentru conexiuni client (de obicei 49152-65535).

---

## F

### FIN (Finish)
Flag TCP care semnalează terminarea transmisiei. Inițiază închiderea grațioasă a conexiunii.

### Firewall
Sistem care filtrează traficul de rețea bazat pe reguli predefinite.

### Frame
Unitatea de date la nivelul Data Link (Layer 2). Include adrese MAC și FCS.

---

## G

### Gateway
Dispozitiv care conectează două rețele diferite. Default gateway = router prin care iese traficul din rețeaua locală.

---

## H

### Handshake (TCP)
Procesul de stabilire a conexiunii TCP în 3 pași: SYN → SYN-ACK → ACK.

### Health Check
Verificare periodică a stării unui serviciu. Load balancer-ul folosește health checks pentru a detecta backend-uri defecte.

### Host
Calculatorul pe care rulează containerele Docker. În WSL2, host-ul este Ubuntu.

### HTTP (Hypertext Transfer Protocol)
Protocol de nivel aplicație pentru transferul resurselor web. Folosește TCP port 80 (sau 443 pentru HTTPS).

---

## I

### ICMP (Internet Control Message Protocol)
Protocol pentru mesaje de control și erori în rețea. `ping` folosește ICMP Echo Request/Reply.

### Image (Docker)
Template read-only pentru crearea containerelor. Conține sistemul de fișiere și configurația.

### IP Address
Adresă logică de 32 biți (IPv4) sau 128 biți (IPv6) pentru identificarea dispozitivelor în rețea.

---

## L

### Layer (OSI/TCP-IP)
Nivel în modelul de rețea. OSI are 7 nivele, TCP/IP are 4.

### Load Balancer
Dispozitiv/software care distribuie traficul între mai multe servere backend.

### Localhost
Adresa de loopback (127.0.0.1) care referă propria mașină.

---

## M

### MAC Address
Adresă hardware de 48 biți, unică pentru fiecare interfață de rețea. Format: `00:1A:2B:3C:4D:5E`.

### Mount (Volume)
Atașarea unui director/fișier de pe host la un container Docker.

### MTU (Maximum Transmission Unit)
Dimensiunea maximă a unui pachet care poate fi transmis fără fragmentare. Ethernet standard: 1500 bytes.

---

## N

### NAT (Network Address Translation)
Tehnică de traducere a adreselor IP, permițând mai multor dispozitive să împartă o adresă IP publică.

### Netmask
Mască care separă partea de rețea de partea de host într-o adresă IP. Ex: 255.255.255.0 pentru /24.

---

## P

### Packet
Unitatea de date la nivelul Network (Layer 3). Include header IP și payload.

### Port
Număr de 16 biți (0-65535) care identifică un serviciu/proces pe un host. Well-known ports: 0-1023.

### Portainer
Interfață web pentru gestionarea containerelor Docker. Accesibil la http://localhost:9000.

### Proxy
Intermediar între client și server. Reverse proxy stă în fața serverelor, forward proxy în fața clienților.

---

## R

### RFC (Request for Comments)
Document care definește standarde și protocoale Internet. Ex: RFC 793 = TCP.

### Round-Robin
Algoritm de distribuție care alternează secvențial între destinații: A → B → A → B → ...

### RST (Reset)
Flag TCP care resetează forțat conexiunea. Indică de obicei o eroare.

### RTT (Round-Trip Time)
Timpul necesar unui pachet să ajungă la destinație și să primească răspuns.

---

## S

### Segment
Unitatea de date la nivelul Transport (Layer 4) pentru TCP.

### Socket
Endpoint de comunicație definit de (IP, port, protocol). În Python: `socket.socket()`.

### Subnet
Subdiviziune a unei rețele IP. Permite organizarea și izolarea traficului.

### SYN (Synchronize)
Flag TCP care inițiază o nouă conexiune.

---

## T

### TCP (Transmission Control Protocol)
Protocol de transport orientat conexiune, fiabil, cu livrare ordonată.

### Timeout
Timp maxim de așteptare pentru un răspuns înainte de a considera operația eșuată.

### TTL (Time To Live)
Număr de hop-uri maxime permise pentru un pachet. Decrementat la fiecare router.

---

## U

### UDP (User Datagram Protocol)
Protocol de transport fără conexiune, nefiabil, dar rapid. Folosit pentru DNS, streaming, gaming.

---

## V

### VLAN (Virtual LAN)
Rețea logică care grupează dispozitive indiferent de locația fizică.

### Volume (Docker)
Mecanism de persistență a datelor în afara ciclului de viață al containerului.

---

## W

### Wireshark
Analizor de protocoale de rețea cu interfață grafică. Capturează și disecă pachete.

### WSL2 (Windows Subsystem for Linux 2)
Subsistem Windows care rulează un kernel Linux real în mașină virtuală ușoară.

---

## Simboluri și Abrevieri Comune

| Simbol | Semnificație |
|--------|--------------|
| `→` | Transmisie de la sursă la destinație |
| `←` | Transmisie de la destinație la sursă |
| `:` | Separator host:port (ex: localhost:8080) |
| `/` | Prefix CIDR (ex: /24) sau cale URL |
| `0.0.0.0` | Toate interfețele (bind) |
| `127.0.0.1` | Loopback/localhost |

---

## Porturi Importante

| Port | Protocol/Serviciu |
|------|-------------------|
| 22 | SSH |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 8080 | HTTP alternativ / Load Balancer (lab) |
| 9000 | Portainer |
| 9090 | Echo Server (lab) |

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
