# Ghid de Debugging Pas-cu-Pas

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest ghid te ajută să rezolvi problemele comune întâlnite în laboratorul de rețele.

---

## Flux de Diagnosticare

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROBLEMA APĂRUTĂ                             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  1. Docker rulează?  ──NO──► sudo service docker start        │
│     docker ps                                                 │
└───────────────────────────┬───────────────────────────────────┘
                           YES
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  2. Containerele Up?  ──NO──► docker compose up -d            │
│     docker ps | grep saptamana4                               │
└───────────────────────────┬───────────────────────────────────┘
                           YES
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  3. Port răspunde?  ──NO──► verifică firewall, port mapping   │
│     nc -zv localhost 5400                                     │
└───────────────────────────┬───────────────────────────────────┘
                           YES
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  4. Codul trimite corect?  ──NO──► verifică CRC, byte order   │
│     Wireshark, print debugging                                │
└───────────────────────────┬───────────────────────────────────┘
                           YES
                            │
                            ▼
                    [PROBLEMA REZOLVATĂ]
```

---

## Problema: Clientul nu se conectează

### Pas 1: Verifică dacă serverul rulează

```bash
docker ps | grep saptamana4
```

**Output așteptat:**
```
abc123   saptamana4-text    Up 2 minutes   0.0.0.0:5400->5400/tcp
def456   saptamana4-binar   Up 2 minutes   0.0.0.0:5401->5401/tcp
ghi789   saptamana4-senzor  Up 2 minutes   0.0.0.0:5402->5402/udp
```

**Dacă nu vezi containerele:**
```bash
cd /mnt/d/RETELE/SAPT4/04roWSL
docker compose -f docker/docker-compose.yml up -d
```

### Pas 2: Verifică portul

```bash
nc -zv localhost 5400
```

**Output așteptat:** `Connection to localhost 5400 port [tcp/*] succeeded!`

### Pas 3: Test minimal Python

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)

try:
    s.connect(('localhost', 5400))
    print("Conectat cu succes!")
    s.sendall(b'4 PING')
    raspuns = s.recv(100)
    print(f"Răspuns: {raspuns}")
except socket.timeout:
    print("EROARE: Timeout la conectare")
except ConnectionRefusedError:
    print("EROARE: Conexiune refuzată - serverul nu rulează")
finally:
    s.close()
```

---

## Problema: CRC invalid

### Diagramă: Flux Verificare CRC

```
┌─────────────────┐                      ┌─────────────────┐
│    EMIȚĂTOR     │                      │    RECEPTOR     │
└────────┬────────┘                      └────────┬────────┘
         │                                        │
    ┌────▼────┐                                   │
    │  Date   │                                   │
    │originale│                                   │
    └────┬────┘                                   │
         │                                        │
    ┌────▼────────┐                               │
    │ Calculează  │                               │
    │   CRC32     │                               │
    └────┬────────┘                               │
         │                                        │
    ┌────▼────────────────┐     TRANSMISIE   ┌───▼───────────────┐
    │ Date + CRC ─────────│─────────────────►│ Date + CRC primit │
    └─────────────────────┘                  └───┬───────────────┘
                                                 │
                                            ┌────▼────────┐
                                            │ Extrage     │
                                            │ CRC primit  │
                                            └────┬────────┘
                                                 │
                                            ┌────▼────────┐
                                            │ Recalculează│
                                            │ CRC32       │
                                            └────┬────────┘
                                                 │
                                            ┌────▼────────────┐
                                            │ CRC primit ==   │
                                            │ CRC calculat?   │
                                            └───┬─────────┬───┘
                                               YES        NO
                                                │          │
                                            ┌───▼───┐  ┌───▼───┐
                                            │ VALID │  │EROARE │
                                            └───────┘  └───────┘
```

### Pas 1: Verifică ordinea bytes (Network Byte Order)

```python
import struct

valoare = 0x12345678

# GREȘIT (ordinea sistemului):
pachet_gresit = struct.pack('I', valoare)
print(f"Greșit: {pachet_gresit.hex()}")  # 78563412

# CORECT (network order):
pachet_corect = struct.pack('!I', valoare)
print(f"Corect: {pachet_corect.hex()}")  # 12345678
```

**Regula de aur:** Folosește ÎNTOTDEAUNA `!` în format string pentru date de rețea.

### Pas 2: Verifică ce date include CRC

```
Antetul BINAR (14 bytes):
┌──────────────────────────────────────────────────────────────┐
│ [0:2]   Magic "NP"    │  INCLUS în CRC                       │
│ [2]     Versiune      │  INCLUS în CRC                       │
│ [3]     Tip           │  INCLUS în CRC                       │
│ [4:6]   Lungime       │  INCLUS în CRC                       │
│ [6:10]  Secvență      │  INCLUS în CRC                       │
├──────────────────────────────────────────────────────────────┤
│ [10:14] CRC32         │  NU se include! (ar fi recursiv)     │
└──────────────────────────────────────────────────────────────┘
│ [14:...]  Payload     │  INCLUS în CRC                       │
└──────────────────────────────────────────────────────────────┘

CRC = crc32(bytes[0:10] + payload)
```

### Pas 3: Debug cu afișare detaliată

```python
import struct
import binascii

def debug_crc(mesaj: bytes):
    """Analizează un mesaj BINAR și verifică CRC."""
    if len(mesaj) < 14:
        print(f"EROARE: Mesaj prea scurt ({len(mesaj)} bytes)")
        return
    
    magic = mesaj[0:2]
    versiune = mesaj[2]
    tip = mesaj[3]
    lungime = struct.unpack('!H', mesaj[4:6])[0]
    secventa = struct.unpack('!I', mesaj[6:10])[0]
    crc_primit = struct.unpack('!I', mesaj[10:14])[0]
    payload = mesaj[14:14+lungime]
    
    print(f"Magic:      {magic} ({'OK' if magic == b'NP' else 'INVALID'})")
    print(f"Versiune:   {versiune}")
    print(f"Tip:        0x{tip:02X}")
    print(f"Lungime:    {lungime}")
    print(f"Secvență:   {secventa}")
    print(f"CRC primit: 0x{crc_primit:08X}")
    
    # Recalculează CRC
    date_pentru_crc = mesaj[0:10] + payload
    crc_calculat = binascii.crc32(date_pentru_crc) & 0xFFFFFFFF
    print(f"CRC calculat: 0x{crc_calculat:08X}")
    
    if crc_primit == crc_calculat:
        print("✓ CRC VALID")
    else:
        print("✗ CRC INVALID!")
```

---

## Problema: UDP nu primește date

### Diagramă: Flux UDP (Fire-and-Forget)

```
┌─────────────┐                           ┌─────────────┐
│   SENZOR    │                           │   SERVER    │
│   (client)  │                           │  (receptor) │
└──────┬──────┘                           └──────┬──────┘
       │                                         │
       │ ────── Datagramă 23 bytes ──────────►   │
       │         (fără confirmare!)              │
       │                                         │
       │ ────── Datagramă 23 bytes ──────────►   │
       │                                         │
       │ ────── Datagramă 23 bytes ──────────►   │
       │                                         │
                                                 
Notă: UDP nu garantează:
- Livrarea (pachetul poate fi pierdut)
- Ordinea (pot ajunge în altă ordine)
- Unicitatea (pot fi duplicate)
```

### Pas 1: Verifică că serverul ascultă

```bash
sudo ss -ulnp | grep 5402
```

**Output așteptat:**
```
UNCONN  0  0  0.0.0.0:5402  0.0.0.0:*  users:(("python3",...))
```

### Pas 2: Verifică structura datagramei senzor

```
Datagrama Senzor (23 bytes):
┌─────────┬──────────┬─────────────┬──────────┬────────┬──────────┐
│Versiune │ ID Senzor│ Temperatură │  Locație │ CRC32  │ Rezervat │
│ 1 byte  │ 2 bytes  │  4 bytes    │ 10 bytes │4 bytes │ 2 bytes  │
│         │ (big-e)  │ (float b-e) │ (null-pd)│(big-e) │ (zeros)  │
└─────────┴──────────┴─────────────┴──────────┴────────┴──────────┘
  offset:     0          1-2           3-6        7-16     17-20    21-22

CRC = crc32(bytes[0:17])  # NU include CRC și rezervat
```

---

## Problema: Wireshark nu capturează pachete

### Diagrama: TCP 3-Way Handshake

```
┌────────┐                                  ┌────────┐
│ Client │                                  │ Server │
└───┬────┘                                  └───┬────┘
    │                                           │
    │ ────── SYN (seq=x) ───────────────────►   │
    │        Flags: [SYN]                       │
    │                                           │
    │ ◄───── SYN-ACK (seq=y, ack=x+1) ───────   │
    │        Flags: [SYN, ACK]                  │
    │                                           │
    │ ────── ACK (ack=y+1) ─────────────────►   │
    │        Flags: [ACK]                       │
    │                                           │
    │        [CONEXIUNE STABILITĂ]              │
    │                                           │
    │ ────── PSH, ACK (date) ──────────────►    │
    │        [Primul mesaj aplicație]           │
```

### Checklist Wireshark

1. **Interfața corectă?** Selectează "vEthernet (WSL)"
2. **Captura pornită?** Butonul albastru (aripioara de rechin)
3. **Filtrul corect?** `tcp.port == 5400` (dublu `==`)
4. **Generezi trafic ÎN TIMPUL capturii?** Nu înainte!

### Filtre Corecte vs Greșite

| Corect | Greșit |
|--------|--------|
| `tcp.port == 5400` | `tcp.port = 5400` |
| `udp.port == 5402` | `port == 5402` |
| `tcp contains "PING"` | `tcp contains 'PING'` |

---

## Problema: "Address already in use"

### Pas 1: Găsește procesul

```bash
sudo ss -tlnp | grep 5400
# Output: LISTEN  0  5  0.0.0.0:5400  *  users:(("python3",pid=12345))
```

### Pas 2: Oprește procesul

```bash
kill -9 12345  # sau
docker compose down
```

---

## Problema: Timeout la conectare

### Cauze și Soluții

| Cauză | Verificare | Soluție |
|-------|------------|---------|
| Server nu rulează | `docker ps` | `docker compose up -d` |
| Firewall blochează | `sudo ufw status` | `sudo ufw allow 5400/tcp` |
| Port greșit | docker-compose.yml | Corectează mapping |
| Adresă greșită | Cod client | Folosește `localhost` |

---

## Checklist General de Debugging

```
□ Docker rulează?              sudo service docker status
□ Containerele sunt Up?        docker ps
□ Porturile sunt mapate?       docker ps (coloana PORTS)
□ Porturile răspund?           nc -zv localhost 5400
□ Firewallul permite?          sudo ufw status
□ Log-uri container?           docker logs <container>
□ Wireshark vede trafic?       Captură fără filtru
□ Codul folosește '!'?         Verifică network byte order
□ CRC include datele corecte?  Vezi diagrama de mai sus
```

---

## Referințe

- [FAQ](faq.md) — Întrebări frecvente
- [Troubleshooting](troubleshooting.md) — Probleme specifice
- [Glossar](glossar.md) — Termeni tehnici

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
