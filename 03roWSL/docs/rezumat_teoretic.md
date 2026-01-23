# Rezumat Teoretic - Săptămâna 3

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Cuprins

1. [Moduri de Comunicare](#moduri-de-comunicare)
2. [Analogii pentru Înțelegere](#analogii-pentru-înțelegere)
3. [Transmisia Broadcast](#transmisia-broadcast)
4. [Comunicarea Multicast](#comunicarea-multicast)
5. [Tunelarea TCP](#tunelarea-tcp)
6. [Opțiuni Socket Relevante](#opțiuni-socket-relevante)
7. [Protocolul IGMP](#protocolul-igmp)
8. [Diagrame de Referință](#diagrame-de-referință)

---

## Moduri de Comunicare

Comunicarea în rețele de calculatoare se poate clasifica în trei moduri fundamentale bazate pe relația dintre emițător și receptor(i):

### Comparație Vizuală

```
UNICAST (1:1)              BROADCAST (1:ALL)          MULTICAST (1:MANY)
┌───┐                      ┌───┐                      ┌───┐
│ S │──────►┌───┐          │ S │──┬──►┌───┐          │ S │──┬──►┌───┐ ✓ membru
└───┘       │ R │          └───┘  │   │R1 │          └───┘  │   │R1 │
            └───┘                 │   └───┘                 │   └───┘
                                  ├──►┌───┐                 └──►┌───┐ ✓ membru
                                  │   │R2 │                     │R2 │
                                  │   └───┘                     └───┘
                                  └──►┌───┐                     ┌───┐ ✗ nu e membru
                                      │R3 │                     │R3 │
                                      └───┘                     └───┘
                            Toți primesc              Doar membrii primesc
```

### Unicast (Unul-la-Unul)

Comunicarea punct-la-punct între un singur emițător și un singur receptor. Aceasta este forma cea mai comună de comunicare în Internet, folosită de protocoale precum HTTP, SSH și majoritatea aplicațiilor client-server.

Caracteristici: eficient pentru comunicare individualizată, scalabilitate limitată pentru distribuția conținutului către mulți receptori, fiecare destinatar necesită o copie separată a datelor.

### Broadcast (Unul-la-Toți)

Un emițător transmite către toate dispozitivele dintr-un segment de rețea, indiferent dacă acestea doresc sau nu să primească datele.

Caracteristici: simplu de implementat, nu necesită cunoașterea prealabilă a receptorilor, limitat la rețeaua locală (nu traversează routere), poate genera trafic inutil dacă majoritatea dispozitivelor nu sunt interesate.

### Multicast (Unul-la-Mulți)

Un emițător transmite către un grup selectat de receptori care s-au înscris pentru a primi datele.

Caracteristici: eficient pentru distribuție unul-la-mulți, scalabil (emițătorul trimite o singură copie), poate traversa routere (cu configurare corespunzătoare), receptorii se înscriu/dezabonează dinamic.

---

## Analogii pentru Înțelegere

Înainte de a studia detaliile tehnice, gândește-te la aceste comparații din viața reală:

| Concept | Analogie | Explicație |
|---------|----------|------------|
| **Unicast** | Apel telefonic | Vorbești cu o singură persoană, linie dedicată |
| **Broadcast** | Anunț pe megafon în piață | Toți aud, indiferent dacă vor sau nu |
| **Multicast** | Grup de WhatsApp | Doar membrii grupului primesc mesajele |
| **IGMP Join** | Abonare la newsletter | Te înscrii activ pentru a primi |
| **IGMP Leave** | Dezabonare | Anunți că nu mai vrei să primești |
| **TTL** | Bilet de metrou valabil N stații | La fiecare router, "o stație" se consumă |
| **SO_BROADCAST** | Permis de megafon | Fără el, sistemul refuză să "strige" |
| **Port UDP** | Cutia poștală a apartamentului | Adresa IP e clădirea, portul e apartamentul |
| **Tunel TCP** | Poștaș care redirecționează | Primește scrisori și le trimite mai departe |

Revino la aceste analogii când întâmpini dificultăți cu conceptele tehnice.

---

## Transmisia Broadcast

### Adrese de Broadcast

Există două tipuri de adrese broadcast în IPv4:

**Broadcast Limitat (255.255.255.255)**
- Nu traversează niciodată routerele
- Folosit când expeditorul nu cunoaște configurația rețelei locale
- Procesat de stratul de legătură de date prin adresa MAC ff:ff:ff:ff:ff:ff

**Broadcast Direcționat**
- Format: adresa de rețea cu toți biții de host setați la 1
- Exemplu: 192.168.1.255 pentru rețeaua 192.168.1.0/24
- Poate traversa routere (dacă sunt configurate să le permită)

### Implementare în Python

```python
import socket

# Creează socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# OBLIGATORIU: Activează opțiunea SO_BROADCAST
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Transmite la adresa de broadcast
sock.sendto(b"Mesaj broadcast", ('255.255.255.255', 5007))
```

### Receptor Broadcast

```python
import socket

# Creează socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# IMPORTANT: Bind la 0.0.0.0, NU la IP specific!
sock.bind(('0.0.0.0', 5007))

# Primește mesaje
data, addr = sock.recvfrom(1024)
```

⚠️ **Atenție:** Dacă faci bind la IP-ul specific al mașinii (ex: 192.168.1.5), NU vei primi mesajele broadcast!

### Când să Folosești Broadcast

✓ Descoperirea serviciilor în rețeaua locală (ex: DHCP)  
✓ Anunțuri către toate dispozitivele  
✓ Protocoale de sincronizare simplă  

✗ Nu pentru comunicare regulată cu destinatari cunoscuți  
✗ Nu pentru date sensibile (toată lumea le poate vedea)  
✗ Nu când scalabilitatea este importantă  

---

## Comunicarea Multicast

### Adrese Multicast

Multicast-ul folosește intervalul de adrese 224.0.0.0 - 239.255.255.255:

| Interval | Scop |
|----------|------|
| 224.0.0.0 - 224.0.0.255 | Local Network Control (TTL=1) |
| 224.0.1.0 - 224.0.1.255 | Internetwork Control |
| 224.0.2.0 - 224.255.255.255 | AD-HOC Block I |
| 232.0.0.0 - 232.255.255.255 | Source-Specific Multicast |
| 233.0.0.0 - 233.255.255.255 | GLOP Block |
| 239.0.0.0 - 239.255.255.255 | Administratively Scoped |

**Pentru teste și aplicații locale, folosește intervalul 239.x.x.x**

### Adresa MAC Multicast

Adresele IP multicast se mapează la adrese MAC speciale:
- Prefixul MAC: 01:00:5E
- Ultimii 23 de biți: ultimii 23 de biți ai adresei IP multicast
- Exemplu: 239.0.0.1 → 01:00:5E:00:00:01

### Implementare în Python - Receptor

```python
import socket
import struct

# Creează socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind la toate interfețele (portabil!)
sock.bind(('', 5008))

# Construiește cererea de membership
mreq = struct.pack(
    '4s4s',
    socket.inet_aton('239.0.0.1'),    # Adresa grup
    socket.inet_aton('0.0.0.0')        # Interfața (toate)
)

# Înscrie în grup - trimite IGMP Membership Report
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Primește mesaje
data, addr = sock.recvfrom(1024)
```

### Implementare în Python - Emițător

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Setează TTL (1 = doar rețea locală)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

# Trimite la grupul multicast
sock.sendto(b"Mesaj multicast", ('239.0.0.1', 5008))
```

### TTL (Time To Live) pentru Multicast

TTL-ul controlează propagarea pachetelor multicast:

| TTL | Scop | Descriere |
|-----|------|-----------|
| 0 | Doar localhost | Pachetul nu părăsește mașina |
| 1 | Doar rețeaua locală | Nu traversează routere |
| 32 | Organizație | Traversează routere locale |
| 64 | Regiune | Traversează routere regionale |
| 128 | Continent | Propagare continentală |
| 255 | Nelimitat | Propagare globală (teoretic) |

---

## Tunelarea TCP

### Concept

Tunelarea TCP implică acceptarea conexiunilor pe un port și redirecționarea transparentă a traficului către o altă destinație. Aceasta este fundamentală pentru proxy-uri, load balancere, bastion hosts, VPN-uri, și port forwarding (SSH tunneling, NAT traversal).

### Arhitectura unui Tunel

```
┌────────┐          ┌────────┐          ┌────────┐
│ Client │ ←──────→ │ Tunel  │ ←──────→ │ Server │
│        │  Conn 1  │        │  Conn 2  │        │
└────────┘          └────────┘          └────────┘

Conn 1: Client se conectează la tunel
Conn 2: Tunelul se conectează la server
Datele sunt relayate bidirecțional între cele două conexiuni
```

**Important:** Serverul vede IP-ul tunelului ca sursă, NU IP-ul clientului original.

### Implementare Simplificată

```python
import threading

def relay_date(sursa, destinatie, nume):
    """Relay date între două socket-uri."""
    try:
        while True:
            date = sursa.recv(4096)
            if not date:
                break
            destinatie.sendall(date)
    except Exception as e:
        pass
    finally:
        sursa.close()
        destinatie.close()

# Pentru relay bidirecțional, folosește două thread-uri:
t1 = threading.Thread(target=relay_date, args=(client, server, "C→S"))
t2 = threading.Thread(target=relay_date, args=(server, client, "S→C"))
t1.start()
t2.start()
```

### Considerații de Implementare

1. **Bidirecționalitate**: Datele circulă în ambele direcții simultan
2. **Gestionarea Deconectărilor**: Când o parte închide conexiunea, trebuie închisă și cealaltă
3. **Buffering**: Gestionarea diferențelor de viteză între conexiuni
4. **Concurență**: Un thread per direcție sau I/O asincron (select/poll/asyncio)
5. **Timeout-uri**: Pentru conexiuni blocate sau abandonate

---

## Opțiuni Socket Relevante

### Opțiuni de Nivel Socket (SOL_SOCKET)

| Opțiune | Scop |
|---------|------|
| SO_BROADCAST | Permite transmisia broadcast |
| SO_REUSEADDR | Permite rebindarea rapidă a portului |
| SO_KEEPALIVE | Detectează conexiuni moarte |
| SO_RCVBUF | Dimensiunea buffer-ului de recepție |
| SO_SNDBUF | Dimensiunea buffer-ului de transmisie |

### Opțiuni IP (IPPROTO_IP)

| Opțiune | Scop |
|---------|------|
| IP_ADD_MEMBERSHIP | Înscrie socket-ul într-un grup multicast |
| IP_DROP_MEMBERSHIP | Părăsește un grup multicast |
| IP_MULTICAST_TTL | Setează TTL pentru multicast |
| IP_MULTICAST_LOOP | Controlează primirea propriilor mesaje |
| IP_MULTICAST_IF | Specifică interfața pentru multicast |

### Opțiuni TCP (IPPROTO_TCP)

| Opțiune | Scop |
|---------|------|
| TCP_NODELAY | Dezactivează algoritmul Nagle |
| TCP_KEEPIDLE | Timp până la primul keepalive |
| TCP_KEEPINTVL | Interval între keepalive |
| TCP_KEEPCNT | Număr de keepalive înainte de timeout |

---

## Protocolul IGMP

### Prezentare Generală

Internet Group Management Protocol (IGMP) gestionează apartenența la grupuri multicast pe segmentul local. Stațiile folosesc IGMP pentru a anunța routerul despre interesul lor pentru anumite grupuri multicast.

### Versiuni IGMP

| Versiune | RFC | Caracteristici |
|----------|-----|----------------|
| IGMPv1 | RFC 1112 | Raportare de bază |
| IGMPv2 | RFC 2236 | Mesaje Leave Group |
| IGMPv3 | RFC 3376 | Source-Specific Multicast |

### Tipuri de Mesaje (IGMPv2)

1. **Membership Query (0x11)**: Router-ul întreabă ce grupuri sunt active
2. **Membership Report (0x16)**: Stația anunță apartenența la grup
3. **Leave Group (0x17)**: Stația anunță părăsirea grupului

### Flux de Operații IGMP

```
┌─────────┐                    ┌─────────┐
│  Host   │  IGMP Join (0x16)  │ Router  │
│         │ ─────────────────► │         │
│         │                    │         │
│         │  IGMP Query (0x11) │         │
│         │ ◄───────────────── │ (~60s)  │
│         │                    │         │
│         │  IGMP Report       │         │
│         │ ─────────────────► │         │
│         │                    │         │
│         │  IGMP Leave (0x17) │         │
│         │ ─────────────────► │         │
└─────────┘                    └─────────┘
```

### Verificare IGMP pe Linux

```bash
# Verifică grupurile la care este înscris sistemul
cat /proc/net/igmp

# Sau folosind ip
ip maddr show

# În containere Docker
docker exec container_name cat /proc/net/igmp
```

---

## Diagrame de Referință

### Flux TTL la Traversarea Routerelor

```
┌─────────┐    TTL=3    ┌─────────┐    TTL=2    ┌─────────┐    TTL=1    ┌─────────┐
│ Sender  │ ──────────► │Router 1 │ ──────────► │Router 2 │ ──────────► │Receiver │
│         │             │  -1     │             │  -1     │             │ PRIMIT! │
└─────────┘             └─────────┘             └─────────┘             └─────────┘

                        Dacă TTL devine 0 înainte de destinație:
┌─────────┐    TTL=1    ┌─────────┐    TTL=0    
│ Sender  │ ──────────► │Router 1 │ ──────────► ❌ DROPPED (Time Exceeded)
│         │             │  -1     │             
└─────────┘             └─────────┘             

ANALOGIE: TTL este ca un bilet de metrou valabil pentru N stații.
          La fiecare router traversat, se "perforează" o stație.
          Când nu mai ai stații, ești dat jos din tren.
```

### Structura Header IGMP

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Type (8)     | Max Resp (8)  |        Checksum (16)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Group Address (32)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Type:
  0x11 = Membership Query
  0x16 = Membership Report (v2)
  0x17 = Leave Group
```

### Maparea IP Multicast → MAC

```
IP Multicast:  239.  0.  0.  1
               ─────────────────
               1110 1111.0000 0000.0000 0000.0000 0001
                        └──────────────────────────┘
                              Ultimii 23 biți
                                    │
                                    ▼
MAC Multicast: 01:00:5E:  00:  00:  01
               ───────── ─────────────
               Prefix    Ultimii 23 biți din IP
               fix
```

---

## Referințe

### RFC-uri Esențiale

- **RFC 919**: Broadcasting Internet Datagrams
- **RFC 922**: Broadcasting Internet Datagrams in the Presence of Subnets
- **RFC 1112**: Host Extensions for IP Multicasting
- **RFC 2236**: Internet Group Management Protocol, Version 2
- **RFC 3376**: Internet Group Management Protocol, Version 3
- **RFC 5771**: IANA Guidelines for IPv4 Multicast Address Assignments

### Bibliografie

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson. Cap. 4.4.
- Stevens, W. R., Fenner, B., & Rudoff, A. (2004). *UNIX Network Programming, Vol. 1* (ed. 3). Addison-Wesley. Cap. 21.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress. Cap. 3.

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
