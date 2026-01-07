# Rezumat Teoretic - Săptămâna 3

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Cuprins

1. [Paradigme de Comunicare](#paradigme-de-comunicare)
2. [Transmisia Broadcast](#transmisia-broadcast)
3. [Comunicarea Multicast](#comunicarea-multicast)
4. [Tunelarea TCP](#tunelarea-tcp)
5. [Opțiuni Socket Relevante](#opțiuni-socket-relevante)
6. [Protocolul IGMP](#protocolul-igmp)

---

## Paradigme de Comunicare

Comunicarea în rețele de calculatoare se poate clasifica în trei paradigme fundamentale bazate pe relația dintre emițător și receptor(i):

### Unicast (Unul-la-Unul)
Comunicarea punct-la-punct între un singur emițător și un singur receptor. Aceasta este forma cea mai comună de comunicare în Internet, folosită de protocoale precum HTTP, SSH și majoritatea aplicațiilor client-server.

**Caracteristici:**
- Eficient pentru comunicare individualizată
- Scalabilitate limitată pentru distribuția conținutului către mulți receptori
- Fiecare destinatar necesită o copie separată a datelor

### Broadcast (Unul-la-Toți)
Un emițător transmite către toate dispozitivele dintr-un segment de rețea, indiferent dacă acestea doresc sau nu să primească datele.

**Caracteristici:**
- Simplu de implementat
- Nu necesită cunoașterea prealabilă a receptorilor
- Limitat la rețeaua locală (nu traversează routere)
- Poate genera trafic inutil dacă majoritatea dispozitivelor nu sunt interesate

### Multicast (Unul-la-Mulți)
Un emițător transmite către un grup selectat de receptori care s-au înscris pentru a primi datele.

**Caracteristici:**
- Eficient pentru distribuție unul-la-mulți
- Scalabil - emițătorul trimite o singură copie
- Poate traversa routere (cu configurare corespunzătoare)
- Receptorii se înscriu/dezabonează dinamic

---

## Transmisia Broadcast

### Adrese de Broadcast

Există două tipuri de adrese broadcast în IPv4:

**Broadcast Limitat (255.255.255.255)**
- Nu traversează niciodată routerele
- Utilizat când expeditorul nu cunoaște configurația rețelei locale
- Procesează de stratul de legătură de date prin adresa MAC ff:ff:ff:ff:ff:ff

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

**Pentru teste și aplicații locale, folosiți intervalul 239.x.x.x**

### Adresa MAC Multicast

Adresele IP multicast se mapează la adrese MAC speciale:
- Prefixul MAC: 01:00:5E
- Ultimii 23 de biți: ultimii 23 de biți ai adresei IP multicast
- Exemplu: 239.0.0.1 → 01:00:5E:00:00:01

### Implementare în Python

```python
import socket
import struct

# Creează socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 5008))

# Construiește cererea de membership
mreq = struct.pack(
    '4s4s',
    socket.inet_aton('239.0.0.1'),    # Adresa grup
    socket.inet_aton('0.0.0.0')        # Interfața (toate)
)

# Înscrie în grup - trimite IGMP Membership Report
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
```

### TTL (Time To Live) pentru Multicast

TTL-ul controlează propagarea pachetelor multicast:

| TTL | Scop |
|-----|------|
| 0 | Doar localhost |
| 1 | Doar rețeaua locală |
| 32 | Organizație |
| 64 | Regiune |
| 128 | Continent |
| 255 | Nelimitat |

---

## Tunelarea TCP

### Concept

Tunelarea TCP implică acceptarea conexiunilor pe un port și redirecționarea transparentă a traficului către o altă destinație. Aceasta este fundamentală pentru:

- **Proxy-uri**: Intermediari pentru acces la Internet
- **Load Balancere**: Distribuția sarcinii între servere
- **Bastion Hosts**: Puncte de acces securizate
- **VPN-uri**: Rețele private virtuale
- **Port Forwarding**: SSH tunneling, NAT traversal

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

### Implementare Simplificată

```python
def relay_date(sursa, destinatie):
    """Relay date între două socket-uri."""
    while True:
        date = sursa.recv(4096)
        if not date:
            break
        destinatie.sendall(date)

# Pentru relay bidirecțional, folosiți două thread-uri:
# Thread 1: relay_date(client, server)
# Thread 2: relay_date(server, client)
```

### Considerații de Implementare

1. **Bidirecționalitate**: Datele circulă în ambele direcții
2. **Gestionarea Deconectărilor**: Când o parte închide conexiunea
3. **Buffering**: Gestionarea diferențelor de viteză
4. **Concurență**: Un thread per direcție sau I/O asincron
5. **Timeout-uri**: Pentru conexiuni blocate

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

### Flux de Operații

```
Înscriere în grup:
Stație → Router: IGMP Membership Report

Verificare periodică:
Router → Rețea: IGMP Membership Query (la fiecare ~60s)
Stații → Router: IGMP Membership Report (pentru grupurile active)

Părăsire grup:
Stație → Router: IGMP Leave Group
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
