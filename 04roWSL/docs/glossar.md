# Glossar Tehnic: Săptămâna 4

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest glossar conține termenii tehnici folosiți în laboratorul de protocoale personalizate.

---

## Termeni de Bază

| Termen | Definiție | Exemplu/Context |
|--------|-----------|-----------------|
| **Antet (Header)** | Metadate adăugate la începutul unui mesaj | Antetul BINAR are 14 octeți |
| **Big-endian** | Ordinea bytes cu MSB (Most Significant Byte) primul | 0x1234 → `[0x12][0x34]` |
| **Little-endian** | Ordinea bytes cu LSB (Least Significant Byte) primul | 0x1234 → `[0x34][0x12]` |
| **Network byte order** | Convenție de ordonare bytes în rețea (big-endian) | `struct.pack('!I', val)` |

---

## Protocoale și Comunicare

| Termen | Definiție | Exemplu/Context |
|--------|-----------|-----------------|
| **CRC32** | Cyclic Redundancy Check pe 32 biți | `binascii.crc32(date)` |
| **Checksum** | Sumă de verificare pentru detectarea erorilor | IP header checksum |
| **Datagrama** | Unitate de date UDP, auto-conținută | Mesaj senzor de 23 bytes |
| **Frame (Cadru)** | Unitate de date la nivelul legătură | Ethernet frame |
| **Framing** | Tehnica de delimitare a mesajelor în flux | Prefix lungime, delimitatori |
| **Handshake** | Schimb inițial de mesaje pentru stabilirea conexiunii | TCP 3-way handshake |
| **Payload** | Datele utile ale unui mesaj (fără antet) | Conținutul după cei 14 bytes antet |

---

## Identificatori și Adresare

| Termen | Definiție | Exemplu/Context |
|--------|-----------|-----------------|
| **Magic number** | Bytes de identificare la începutul unui protocol | `b'NP'` în protocolul BINAR |
| **Port** | Identificator numeric pentru o aplicație/serviciu | TCP:5400, UDP:5402 |
| **Secvență** | Număr pentru ordonarea și urmărirea mesajelor | Câmpul de 4 bytes din antet |
| **Socket** | Endpoint de comunicare (IP + port + protocol) | `socket.socket()` |

---

## Rețelistică și Transport

| Termen | Definiție | Exemplu/Context |
|--------|-----------|-----------------|
| **ACK** | Acknowledgment — confirmarea primirii | TCP ACK flag |
| **Broadcast** | Transmisie către toate nodurile din rețea | 255.255.255.255 |
| **Conexiune** | Asociere logică între doi parteneri (TCP) | Client ↔ Server |
| **Latență** | Timpul de parcurs al unui mesaj | Ping RTT |
| **Overhead** | Date suplimentare necesare protocolului | Antet TCP ~40 bytes |
| **RTT** | Round-Trip Time — dus-întors | Timp PING + PONG |
| **Timeout** | Limită de timp pentru o operație | `sock.settimeout(5.0)` |

---

## Docker și Containere

| Termen | Definiție | Exemplu/Context |
|--------|-----------|-----------------|
| **Container** | Instanță izolată a unei aplicații | `saptamana4-text` |
| **Image** | Template pentru crearea containerelor | `python:3.11-slim` |
| **Port mapping** | Maparea porturilor host ↔ container | `-p 5400:5400` |
| **Volume** | Stocare persistentă pentru containere | `portainer_data` |
| **Compose** | Orchestrare multi-container | `docker-compose.yml` |
| **Bridge network** | Rețea virtuală Docker pentru containere | `retea_saptamana4` |

---

## Python și Programare

| Termen | Definiție | Exemplu/Context |
|--------|-----------|-----------------|
| **struct.pack** | Împachetare date în format binar | `struct.pack('!I', 123)` |
| **struct.unpack** | Despachetare date din format binar | `struct.unpack('!I', data)` |
| **bytes** | Secvență de octeți imutabilă | `b'NP'`, `b'\x01\x02'` |
| **bytearray** | Secvență de octeți mutabilă | `bytearray(14)` |
| **encode/decode** | Conversie string ↔ bytes | `'text'.encode('utf-8')` |

---

## Formate struct

| Format | Tip Python | Dimensiune | Descriere |
|--------|------------|------------|-----------|
| `B` | int | 1 byte | unsigned char |
| `H` | int | 2 bytes | unsigned short |
| `I` | int | 4 bytes | unsigned int |
| `f` | float | 4 bytes | float |
| `s` | bytes | variabil | string de bytes |
| `!` | - | - | network byte order (big-endian) |
| `<` | - | - | little-endian |
| `>` | - | - | big-endian (explicit) |

---

## Wireshark

| Termen | Definiție | Exemplu/Context |
|--------|-----------|-----------------|
| **Capture filter** | Filtru aplicat la capturare (BPF) | `tcp port 5401` |
| **Display filter** | Filtru aplicat după captură | `tcp.port == 5401` |
| **Dissector** | Modul de parsare protocol | Wireshark TCP dissector |
| **Follow stream** | Vizualizare conversație completă | Click dreapta → Follow TCP Stream |
| **PCAP** | Format fișier captură pachete | `capture.pcapng` |

---

## Acronime

| Acronim | Expansiune | Traducere/Explicație |
|---------|------------|---------------------|
| **ACK** | Acknowledgment | Confirmare |
| **ARP** | Address Resolution Protocol | Protocol de rezoluție adrese |
| **CRC** | Cyclic Redundancy Check | Verificare redundanță ciclică |
| **DHCP** | Dynamic Host Configuration Protocol | Protocol configurare dinamică |
| **DNS** | Domain Name System | Sistem de nume de domenii |
| **FIN** | Finish | Flag TCP pentru închidere |
| **IoT** | Internet of Things | Internetul lucrurilor |
| **ISN** | Initial Sequence Number | Număr secvență inițial |
| **LAN** | Local Area Network | Rețea locală |
| **MAC** | Media Access Control | Control acces la mediu |
| **MSB** | Most Significant Byte | Byte-ul cel mai semnificativ |
| **LSB** | Least Significant Byte | Byte-ul cel mai puțin semnificativ |
| **OSI** | Open Systems Interconnection | Model de referință |
| **RTT** | Round-Trip Time | Timp dus-întors |
| **SYN** | Synchronize | Flag TCP pentru sincronizare |
| **TCP** | Transmission Control Protocol | Protocol orientat conexiune |
| **UDP** | User Datagram Protocol | Protocol fără conexiune |
| **WSL** | Windows Subsystem for Linux | Subsistem Windows pentru Linux |

---

## Valori Standard din Laborator

| Valoare | Semnificație |
|---------|--------------|
| `b'NP'` | Magic number protocol BINAR |
| `0x01` | Tip mesaj PING |
| `0x02` | Tip mesaj PONG |
| `0xFF` | Tip mesaj ERROR |
| `5400` | Port protocol TEXT |
| `5401` | Port protocol BINAR |
| `5402` | Port protocol Senzor UDP |
| `9000` | Port Portainer |
| `14` | Dimensiune antet BINAR (bytes) |
| `23` | Dimensiune datagramă senzor (bytes) |

---

## Vezi și

- [Rezumat Teoretic](theory_summary.md) — Explicații detaliate
- [Fișa de Comenzi](commands_cheatsheet.md) — Referință rapidă comenzi
- [FAQ](faq.md) — Întrebări frecvente

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
