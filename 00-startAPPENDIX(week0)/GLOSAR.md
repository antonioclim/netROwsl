# 📖 Glosar de Termeni — Rețele de Calculatoare

> **Referință rapidă** pentru terminologia folosită în laborator  
> **Convenție:** Termenii tehnici sunt păstrați în engleză conform standardelor industriei

---

## A

**ACK (Acknowledgment)**  
Pachet sau flag care confirmă primirea cu succes a datelor. În TCP, fiecare segment trimis trebuie confirmat cu ACK.

**ARP (Address Resolution Protocol)**  
Protocol pentru maparea adreselor IP la adrese MAC în rețelele locale. Funcționează la nivelul Data Link.

**argparse**  
Modul Python pentru procesarea argumentelor din linia de comandă. Generează automat `--help`.

---

## B

**Bind**  
Operația de asociere a unui socket cu o adresă IP și port specific. Necesar pentru servere înainte de `listen()`.

**Bridge Network**  
Rețea Docker implicită care permite comunicarea între containere pe același host. Containerele primesc IP-uri din range-ul 172.17.0.0/16.

**Broadcast**  
Transmisie către toate dispozitivele dintr-o rețea. Adresa de broadcast IPv4: 255.255.255.255 sau ultima adresă din subnet.

**Bytes**  
Tip de date Python pentru date binare brute. Prefixat cu `b` (ex: `b"Hello"`). Necesar pentru operații de rețea.

---

## C

**CIDR (Classless Inter-Domain Routing)**  
Notație pentru specificarea intervalelor de adrese IP. Format: `IP/prefix` (ex: `192.168.1.0/24`).

**Container**  
Instanță izolată a unei imagini Docker, rulând unul sau mai multe procese. Împarte kernel-ul cu host-ul.

**Context Manager**  
Construct Python (`with`) care garantează eliberarea resurselor (fișiere, socket-uri) chiar dacă apare o excepție.

**Checksum**  
Valoare calculată pentru detectarea erorilor de transmisie. Header-ele IP și TCP includ checksum-uri.

---

## D

**Daemon**  
Proces care rulează în background. Docker daemon (`dockerd`) gestionează containerele.

**Dataclass**  
Decorator Python (`@dataclass`) care generează automat `__init__`, `__repr__`, `__eq__` pentru clase de date.

**DHCP (Dynamic Host Configuration Protocol)**  
Protocol pentru alocarea automată a adreselor IP și configurării de rețea.

**DNS (Domain Name System)**  
Sistem pentru traducerea numelor de domenii în adrese IP. Portul standard: 53 (UDP/TCP).

**Docker Compose**  
Instrument pentru definirea și rularea aplicațiilor multi-container. Configurare prin `docker-compose.yml`.

**Docstring**  
Șir de documentare în Python, încadrat de `"""`. Accesibil prin `help()` sau `__doc__`.

---

## E

**Encoding**  
Procesul de conversie text (str) în bytes. În Python: `"text".encode('utf-8')`.

**Endpoint**  
Punct de acces pentru un serviciu de rețea, specificat ca adresă IP + port.

---

## F

**Frame**  
Unitate de date la nivelul Data Link (Layer 2). Conține header Ethernet, payload și FCS.

**FTP (File Transfer Protocol)**  
Protocol pentru transferul fișierelor. Port control: 21, Port date: 20 (activ) sau dinamic (pasiv).

---

## G

**Gateway**  
Dispozitiv care conectează rețele diferite, de obicei routerul default care trimite pachetele în afara rețelei locale.

---

## H

**Handshake**  
Secvență de mesaje pentru stabilirea unei conexiuni. TCP folosește 3-way handshake: SYN → SYN-ACK → ACK.

**Header**  
Metadate adăugate la începutul unui pachet. Conține informații pentru rutare și procesare (adrese, porturi, flags).

**HTTP (Hypertext Transfer Protocol)**  
Protocol de nivel aplicație pentru transferul resurselor web. Port standard: 80 (HTTP), 443 (HTTPS).

---

## I

**ICMP (Internet Control Message Protocol)**  
Protocol pentru mesaje de diagnostic și eroare. Folosit de `ping` și `traceroute`.

**IHL (Internet Header Length)**  
Câmp în header-ul IP care specifică lungimea header-ului în unități de 4 bytes. Valoare minimă: 5 (20 bytes).

**Image (Docker)**  
Template read-only pentru crearea containerelor. Construită din layers (straturi).

---

## L

**Latency**  
Timpul de întârziere într-o rețea, de obicei măsurat ca RTT (Round-Trip Time).

**Listen**  
Operație socket care pregătește serverul să accepte conexiuni. Specifică dimensiunea cozii de conexiuni în așteptare.

**Localhost**  
Adresa de loopback care se referă la mașina locală: 127.0.0.1 (IPv4) sau ::1 (IPv6).

**Logging**  
Înregistrarea evenimentelor pentru debugging și monitorizare. Modul Python: `logging`.

---

## M

**MAC (Media Access Control)**  
Adresă hardware unică de 48 biți pentru interfețele de rețea. Format: `XX:XX:XX:XX:XX:XX`.

**Multicast**  
Transmisie către un grup de destinatari care s-au abonat. Range IPv4: 224.0.0.0 - 239.255.255.255.

---

## N

**NAT (Network Address Translation)**  
Tehnica de traducere a adreselor IP private în adrese publice, permițând mai multor dispozitive să împărtășească o singură adresă publică.

**Network Byte Order**  
Big-endian, ordinea standard pentru transmisia datelor în rețea. În Python: `struct.pack('!H', port)`.

---

## O

**OSI Model**  
Model de referință cu 7 straturi: Physical, Data Link, Network, Transport, Session, Presentation, Application.

---

## P

**Packet**  
Unitate de date la nivelul Network (Layer 3). În IP, conține header IP și payload.

**Payload**  
Datele utile transportate de un pachet, fără header-e.

**Port**  
Număr de 16 biți (0-65535) care identifică un serviciu sau aplicație. Porturi well-known: 0-1023.

**Portainer**  
Interfață web pentru gestionarea containerelor Docker. Port default: 9000.

---

## R

**RTT (Round-Trip Time)**  
Timpul total pentru ca un pachet să ajungă la destinație și răspunsul să revină.

---

## S

**Socket**  
Endpoint pentru comunicare în rețea, definit de IP + port + protocol. API pentru programarea de rețea.

**struct**  
Modul Python pentru conversie între bytes și tipuri native. Esențial pentru parsing protocoale binare.

**Subnet**  
Subdiviziune logică a unei rețele IP, definită de mască de subrețea.

---

## T

**TCP (Transmission Control Protocol)**  
Protocol de transport orientat pe conexiune, cu garantii de livrare ordonată și fără pierderi. Port-urile HTTP, HTTPS, SSH folosesc TCP.

**Thread**  
Unitate de execuție în cadrul unui proces. Python: `threading` module sau `ThreadPoolExecutor`.

**TLS (Transport Layer Security)**  
Protocol criptografic pentru securizarea comunicațiilor. Succesorul SSL.

**TTL (Time To Live)**  
Câmp în header-ul IP care limitează durata de viață a unui pachet (număr de hop-uri). Decrementat de fiecare router.

**Type Hints**  
Adnotări opționale în Python pentru specificarea tipurilor: `def func(x: int) -> str:`.

---

## U

**UDP (User Datagram Protocol)**  
Protocol de transport fără conexiune, fără garantii de livrare. Folosit pentru DNS, streaming, gaming.

**UTF-8**  
Encoding standard pentru text Unicode, compatibil cu ASCII. Recomandare: folosește mereu UTF-8.

---

## V

**VLAN (Virtual LAN)**  
Rețea logică independentă de topologia fizică, creată prin segmentare la Layer 2.

**VLSM (Variable Length Subnet Masking)**  
Tehnica de alocare a subrețelelor cu măști de lungimi diferite pentru optimizarea spațiului de adrese.

**Volume (Docker)**  
Mecanism pentru persistența datelor în afara ciclului de viață al containerului.

---

## W

**Wireshark**  
Analizor de protocoale de rețea. Captează și afișează pachete în timp real sau din fișiere `.pcap`.

**WSL2 (Windows Subsystem for Linux 2)**  
Subsistem care permite rularea unui kernel Linux complet în Windows, cu performanță nativă.

---

## Simboluri și Notații

| Simbol | Semnificație |
|--------|-------------|
| `0.0.0.0` | Toate interfețele (bind) |
| `127.0.0.1` | Localhost |
| `/24` | Mască de subrețea 255.255.255.0 |
| `:8080` | Port 8080 |
| `→` | Direcția fluxului de date |

---

*Glosar pentru cursul de Rețele de Calculatoare*  
*ASE București — CSIE*  
*Versiune: Ianuarie 2025*
