# Lectură Suplimentară: Nivelul Fizic și Legătură de Date

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

## Cuprins
1. [Cărți de Referință](#cărți-de-referință)
2. [Standarde și RFC-uri](#standarde-și-rfc-uri)
3. [Articole Academice](#articole-academice)
4. [Resurse Online](#resurse-online)
5. [Tutoriale Python](#tutoriale-python)
6. [Aprofundare CRC](#aprofundare-crc)
7. [Provocări Avansate](#provocări-avansate)

---

## Cărți de Referință

### Principale

**Computer Networking: A Top-Down Approach**
- Autori: James F. Kurose, Keith W. Ross
- Ediția: 7 sau 8
- Capitol relevant: Capitolul 5 - Link Layer
- ISBN: 978-0133594140
- *Abordare modernă, de la aplicație spre fizic*

**Computer Networks**
- Autori: Andrew S. Tanenbaum, David J. Wetherall
- Ediția: 5
- Capitole relevante: 3 (Data Link Layer), 4 (MAC Sublayer)
- ISBN: 978-0132126953
- *Clasic, foarte detaliat tehnic*

**Foundations of Python Network Programming**
- Autori: Brandon Rhodes, John Goerzen
- Ediția: 3
- Capitole relevante: 2-5 (Socket Programming)
- ISBN: 978-1430258544
- *Excelent pentru implementare practică în Python*

### Suplimentare

**TCP/IP Illustrated, Volume 1: The Protocols**
- Autor: W. Richard Stevens
- Ediția: 2 (actualizată de Kevin R. Fall)
- *Referință definitivă pentru protocoale TCP/IP*

**Unix Network Programming, Volume 1: Sockets Networking API**
- Autor: W. Richard Stevens
- *Pentru înțelegerea profundă a API-ului socket*

---

## Standarde și RFC-uri

### Protocoale de Bază

**RFC 768 - User Datagram Protocol (UDP)**
- https://www.rfc-editor.org/rfc/rfc768
- Doar 3 pagini, esențial pentru înțelegerea UDP
- Definește structura datagramei UDP

**RFC 793 - Transmission Control Protocol (TCP)**
- https://www.rfc-editor.org/rfc/rfc793
- Protocol complex, ~85 pagini
- Esențial pentru înțelegerea TCP în profunzime

**RFC 1122 - Requirements for Internet Hosts**
- https://www.rfc-editor.org/rfc/rfc1122
- Cerințele pentru implementarea TCP/IP

### Detectarea Erorilor

**RFC 1071 - Computing the Internet Checksum**
- https://www.rfc-editor.org/rfc/rfc1071
- Algoritmul de checksum folosit în IP, TCP, UDP

**RFC 3309 - Stream Control Transmission Protocol Checksum Change**
- https://www.rfc-editor.org/rfc/rfc3309
- Discuție despre CRC-32c vs. Adler-32

### Ethernet

**IEEE 802.3 - Ethernet Standard**
- https://standards.ieee.org/standard/802_3-2018.html
- Standard complet pentru Ethernet
- Include specificații pentru CRC-32

---

## Articole Academice

### Proiectare Protocoale

**"End-to-End Arguments in System Design"**
- Autori: J.H. Saltzer, D.P. Reed, D.D. Clark
- ACM Transactions on Computer Systems, 1984
- *Principiul fundamental al proiectării rețelelor*

**"The Design Philosophy of the DARPA Internet Protocols"**
- Autor: David D. Clark
- SIGCOMM 1988
- *De ce internetul arată așa cum arată*

### Performanță și Fiabilitate

**"Congestion Avoidance and Control"**
- Autor: Van Jacobson
- SIGCOMM 1988
- *Algoritmi fundamentali pentru TCP*

**"An Analysis of TCP Processing Overhead"**
- IEEE Communications Magazine
- *Înțelegerea costurilor de procesare*

---

## Resurse Online

### Documentație Python

**Modulul socket**
- https://docs.python.org/3/library/socket.html
- Documentație oficială pentru programarea socket

**Modulul struct**
- https://docs.python.org/3/library/struct.html
- Împachetare/despachetare date binare

**Modulul binascii**
- https://docs.python.org/3/library/binascii.html
- Include funcția crc32()

### Tutoriale și Ghiduri

**Beej's Guide to Network Programming**
- https://beej.us/guide/bgnet/
- Ghid clasic, inițial pentru C, concepte universale

**Real Python - Socket Programming**
- https://realpython.com/python-sockets/
- Tutorial modern și accesibil

### Instrumente

**Wireshark User's Guide**
- https://www.wireshark.org/docs/wsug_html/
- Documentație completă pentru Wireshark

**tcpdump Manual**
- https://www.tcpdump.org/manpages/tcpdump.1.html
- Referință pentru tcpdump

---

## Tutoriale Python

### Programare Socket de Bază

```python
# Exemplu complet client TCP
import socket

def client_tcp_simplu(host: str, port: int, mesaj: str) -> str:
    """
    Client TCP simplu care trimite un mesaj și primește răspuns.
    
    Args:
        host: Adresa serverului
        port: Portul serverului
        mesaj: Mesajul de trimis
    
    Returns:
        Răspunsul serverului
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Conectare
        sock.connect((host, port))
        
        # Setare timeout
        sock.settimeout(5.0)
        
        # Trimitere
        sock.sendall(mesaj.encode())
        
        # Recepție
        raspuns = sock.recv(4096)
        
        return raspuns.decode()


# Utilizare
raspuns = client_tcp_simplu('localhost', 5400, '4 PING\n')
print(f"Răspuns: {raspuns}")
```

### Lucru cu Date Binare

```python
import struct
import binascii

def construieste_mesaj_binar(tip: int, payload: bytes, secventa: int) -> bytes:
    """
    Construiește un mesaj în format binar.
    
    Structura:
    - Magic: 2 octeți ('NP')
    - Versiune: 1 octet
    - Tip: 1 octet
    - Lungime: 2 octeți (big-endian)
    - Secvență: 4 octeți (big-endian)
    - CRC32: 4 octeți (big-endian)
    - Payload: variabil
    """
    magic = b'NP'
    versiune = 1
    lungime = len(payload)
    
    # Împachetare fără CRC
    antet_partial = struct.pack('!2sBBHI',
        magic,
        versiune,
        tip,
        lungime,
        secventa
    )
    
    # Calculare CRC peste antet + payload
    crc = binascii.crc32(antet_partial + payload) & 0xFFFFFFFF
    
    # Mesaj complet
    mesaj = struct.pack('!2sBBHII',
        magic,
        versiune,
        tip,
        lungime,
        secventa,
        crc
    ) + payload
    
    return mesaj


def parseaza_mesaj_binar(date: bytes) -> dict:
    """
    Parsează un mesaj binar și verifică CRC.
    """
    if len(date) < 14:
        raise ValueError("Mesaj prea scurt")
    
    # Extrage antetul
    magic, versiune, tip, lungime, secventa, crc = struct.unpack(
        '!2sBBHII', date[:14]
    )
    
    # Verifică magic
    if magic != b'NP':
        raise ValueError(f"Magic invalid: {magic}")
    
    # Extrage payload
    payload = date[14:14+lungime]
    
    # Verifică CRC
    antet_fara_crc = date[:10]
    crc_calculat = binascii.crc32(antet_fara_crc + payload) & 0xFFFFFFFF
    
    if crc != crc_calculat:
        raise ValueError(f"CRC invalid: așteptat {crc_calculat:08X}, primit {crc:08X}")
    
    return {
        'versiune': versiune,
        'tip': tip,
        'lungime': lungime,
        'secventa': secventa,
        'crc': crc,
        'payload': payload
    }
```

---

## Aprofundare CRC

### Principiul Matematic

CRC tratează datele ca un polinom cu coeficienți binari și efectuează împărțire modulară.

**Date:** `11010011101100`
**Polinom generator CRC-3:** `1011` (x³ + x + 1)

```
Procesul:
1. Adaugă n zerouri la date (n = gradul polinomului)
2. Împarte prin XOR
3. Restul = CRC
```

### Implementare Manuală CRC32

```python
def crc32_manual(date: bytes) -> int:
    """
    Implementare manuală a CRC32 pentru înțelegere.
    Utilizați binascii.crc32() în practică.
    """
    # Polinom CRC-32 IEEE 802.3
    POLINOM = 0xEDB88320
    
    crc = 0xFFFFFFFF
    
    for octet in date:
        crc ^= octet
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLINOM
            else:
                crc >>= 1
    
    return crc ^ 0xFFFFFFFF


# Verificare
import binascii

date_test = b"Hello, World!"
crc_manual = crc32_manual(date_test)
crc_biblioteca = binascii.crc32(date_test) & 0xFFFFFFFF

print(f"CRC manual:     0x{crc_manual:08X}")
print(f"CRC bibliotecă: 0x{crc_biblioteca:08X}")
print(f"Potrivire: {crc_manual == crc_biblioteca}")
```

### Proprietăți CRC32

| Proprietate | Valoare |
|-------------|---------|
| Lungime | 32 biți |
| Polinom | 0x04C11DB7 (normal) / 0xEDB88320 (reflectat) |
| Detecție bit singur | 100% |
| Detecție biți multipli | Foarte ridicată |
| Detecție rafală ≤32 biți | 100% |
| Rezistență criptografică | NULĂ |

---

## Provocări Avansate

### 1. Protocol de Retransmisie

Implementați ARQ (Automatic Repeat reQuest):
- Trimiteți mesaje cu numere de secvență
- Așteptați confirmări (ACK)
- Retransmiteți după timeout
- Gestionați ACK-uri duplicate

### 2. Fereastră Glisantă

Extindeți protocolul cu fereastră glisantă:
- Permiteți mai multe mesaje în zbor
- Implementați controlul fluxului
- Gestionați recepția în afara ordinii

### 3. Transfer Fiabil peste UDP

Construiți un protocol de transfer de fișiere fiabil:
- Fragmentare și reasamblare
- Detectarea erorilor cu CRC32
- Retransmisie selectivă
- Verificare integritate SHA-256

### 4. Protocol Binar Comprimat

Extindeți protocolul BINAR:
- Adăugați câmp de flaguri pentru compresie
- Implementați compresie zlib pentru payload
- Măsurați economia de bandă

### 5. Multiplexare Conexiuni

Implementați un protocol care:
- Multiplexează mai multe canale logice pe o conexiune TCP
- Oferă identificatori de canal în antet
- Permite prioritizare

---

## Resurse în Limba Română

### Cărți

**Rețele de Calculatoare**
- Diverse manuale universitare românești
- Verificați biblioteca ASE

### Online

**Wikipedia Română - Rețele de Calculatoare**
- https://ro.wikipedia.org/wiki/Rețea_de_calculatoare
- Concepte de bază în română

**Cursuri Online**
- Platforme precum Udemy, Coursera cu subtitrări

---

## Următorii Pași

După acest laborator, puteți explora:

1. **Nivelul Rețea** - Routing, IP, ICMP
2. **Nivelul Transport** - TCP în detaliu, congestion control
3. **Securitate** - TLS, criptare, autentificare
4. **Protocoale Moderne** - HTTP/2, QUIC, WebSocket
5. **Rețele Definite prin Software (SDN)**

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
