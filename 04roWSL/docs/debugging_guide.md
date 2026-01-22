# Ghid de Debugging Pas-cu-Pas

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest ghid te ajută să rezolvi problemele comune întâlnite în laboratorul de rețele.

---

## Problema: Clientul nu se conectează

### Pas 1: Verifică dacă serverul rulează

```bash
docker ps | grep saptamana4
```

**Output așteptat:**
```
abc123def456   saptamana4-text    "/usr/bin/python3 ..."   Up 2 minutes   0.0.0.0:5400->5400/tcp
def456abc123   saptamana4-binar   "/usr/bin/python3 ..."   Up 2 minutes   0.0.0.0:5401->5401/tcp
ghi789jkl012   saptamana4-senzor  "/usr/bin/python3 ..."   Up 2 minutes   0.0.0.0:5402->5402/udp
```

**Dacă nu vezi containerele:**
```bash
cd /mnt/d/RETELE/SAPT4/04roWSL
docker compose -f docker/docker-compose.yml up -d
```

**Dacă containerele sunt "Exited":**
```bash
# Vezi de ce a ieșit
docker logs saptamana4-text

# Repornește
docker restart saptamana4-text
```

### Pas 2: Verifică portul

```bash
# Verifică că portul ascultă
nc -zv localhost 5400
```

**Output așteptat:**
```
Connection to localhost 5400 port [tcp/*] succeeded!
```

**Dacă eșuează:**
```bash
# Verifică ce proces folosește portul
sudo ss -tlnp | grep 5400

# Sau pe Windows (PowerShell ca Administrator)
netstat -ano | findstr 5400
```

### Pas 3: Test minimal Python

```python
import socket

# Test de conectare minimal
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
except Exception as e:
    print(f"EROARE: {e}")
finally:
    s.close()
```

### Pas 4: Verifică firewallul (dacă pașii anteriori au eșuat)

```bash
# În WSL Ubuntu
sudo ufw status
# Dacă e activ, adaugă excepție:
sudo ufw allow 5400/tcp
sudo ufw allow 5401/tcp
sudo ufw allow 5402/udp
```

---

## Problema: CRC invalid

### Pas 1: Verifică ordinea bytes (Network Byte Order)

```python
import struct

valoare = 0x12345678

# GREȘIT - ordinea sistemului (little-endian pe x86):
pachet_gresit = struct.pack('I', valoare)
print(f"Greșit: {pachet_gresit.hex()}")  # 78563412

# CORECT - network byte order (big-endian):
pachet_corect = struct.pack('!I', valoare)
print(f"Corect: {pachet_corect.hex()}")  # 12345678
```

**Regula de aur:** Folosește ÎNTOTDEAUNA `!` în format string pentru date de rețea:
- `'!H'` pentru 2 bytes (unsigned short)
- `'!I'` pentru 4 bytes (unsigned int)
- `'!f'` pentru float

### Pas 2: Verifică ce date include CRC

```python
import struct
import binascii

# Antetul BINAR are 14 bytes:
# [0:2]   Magic "NP"
# [2]     Versiune
# [3]     Tip
# [4:6]   Lungime
# [6:10]  Secvență  
# [10:14] CRC32  <-- ACEST câmp NU se include în calcul!

# CRC se calculează peste:
# - Antet FĂRĂ câmpul CRC (primii 10 bytes)
# - PLUS payload-ul complet

antet_partial = struct.pack('!2sBBHI',
    b'NP',      # Magic
    1,          # Versiune
    0x01,       # Tip (PING)
    0,          # Lungime payload
    1           # Secvență
)  # = 10 bytes

payload = b''  # PING nu are payload

# Calculează CRC peste antet_partial + payload
crc = binascii.crc32(antet_partial + payload) & 0xFFFFFFFF
print(f"CRC calculat: 0x{crc:08X}")

# Mesaj complet
mesaj = antet_partial + struct.pack('!I', crc) + payload
print(f"Mesaj complet ({len(mesaj)} bytes): {mesaj.hex()}")
```

### Pas 3: Debug cu afișare detaliată

```python
def debug_crc(mesaj: bytes):
    """Analizează un mesaj BINAR și verifică CRC."""
    if len(mesaj) < 14:
        print(f"EROARE: Mesaj prea scurt ({len(mesaj)} bytes, minim 14)")
        return
    
    # Extrage componentele
    magic = mesaj[0:2]
    versiune = mesaj[2]
    tip = mesaj[3]
    lungime = struct.unpack('!H', mesaj[4:6])[0]
    secventa = struct.unpack('!I', mesaj[6:10])[0]
    crc_primit = struct.unpack('!I', mesaj[10:14])[0]
    payload = mesaj[14:14+lungime]
    
    print(f"Magic:     {magic} ({'OK' if magic == b'NP' else 'INVALID'})")
    print(f"Versiune:  {versiune}")
    print(f"Tip:       0x{tip:02X}")
    print(f"Lungime:   {lungime}")
    print(f"Secvență:  {secventa}")
    print(f"CRC primit: 0x{crc_primit:08X}")
    print(f"Payload:   {payload.hex() if payload else '(gol)'}")
    
    # Recalculează CRC
    date_pentru_crc = mesaj[0:10] + payload
    crc_calculat = binascii.crc32(date_pentru_crc) & 0xFFFFFFFF
    print(f"CRC calculat: 0x{crc_calculat:08X}")
    
    if crc_primit == crc_calculat:
        print("✓ CRC VALID")
    else:
        print("✗ CRC INVALID!")
        print(f"  Date pentru CRC: {date_pentru_crc.hex()}")
```

---

## Problema: UDP nu primește date

### Pas 1: Verifică că serverul ascultă

```bash
# Verifică portul UDP
sudo ss -ulnp | grep 5402
```

**Output așteptat:**
```
UNCONN  0  0  0.0.0.0:5402  0.0.0.0:*  users:(("python3",pid=12345,fd=3))
```

### Pas 2: Test cu netcat

```bash
# Trimite date de test
echo -n "test" | nc -u localhost 5402

# Verifică log-urile serverului
docker logs saptamana4-senzor --tail 20
```

### Pas 3: Verifică structura datagramei

```python
import struct
import binascii

def construieste_datagrama_corecta(sensor_id: int, temp: float, loc: str) -> bytes:
    """Construiește o datagramă validă de 23 bytes."""
    
    # Pregătește locația (exact 10 bytes, padding cu \x00)
    loc_bytes = loc.encode('utf-8')[:10]
    loc_padded = loc_bytes + b'\x00' * (10 - len(loc_bytes))
    
    # Partea fără CRC (17 bytes)
    parte_fara_crc = struct.pack('!BHf',
        1,              # Versiune (1 byte)
        sensor_id,      # ID senzor (2 bytes, big-endian)
        temp            # Temperatură (4 bytes, float big-endian)
    ) + loc_padded      # Locație (10 bytes)
    
    # Calculează CRC
    crc = binascii.crc32(parte_fara_crc) & 0xFFFFFFFF
    
    # Datagrama completă (23 bytes)
    datagrama = parte_fara_crc + struct.pack('!I', crc) + b'\x00\x00'
    
    assert len(datagrama) == 23, f"Lungime greșită: {len(datagrama)}"
    return datagrama

# Test
dg = construieste_datagrama_corecta(42, 23.5, "Lab1")
print(f"Datagrama ({len(dg)} bytes): {dg.hex()}")
```

---

## Problema: Wireshark nu capturează pachete

### Pas 1: Verifică interfața

Interfețe disponibile pentru trafic WSL:

| Interfață | Când folosești |
|-----------|----------------|
| vEthernet (WSL) | Cel mai frecvent |
| Loopback Adapter | Doar pentru 127.0.0.1 |

### Pas 2: Verifică filtrul

Filtre care funcționează:
```
tcp.port == 5400
udp.port == 5402
tcp.port == 5400 or tcp.port == 5401
```

Filtre **GREȘITE** (erori comune):
```
tcp.port = 5400      # Greșit: un singur =
port == 5400         # Greșit: lipsește tcp/udp
tcp.port==5400       # Poate funcționa, dar e mai bine cu spații
```

### Pas 3: Generează trafic în timpul capturii

1. Pornește captura în Wireshark ÎNTÂI
2. Apoi rulează clientul
3. Oprește captura DUPĂ

### Pas 4: Verifică că vezi CEVA

Șterge filtrul temporar și verifică:
- Vezi pachete de orice fel?
- Dacă nu, interfața e greșită
- Dacă da, filtrul e prea restrictiv

---

## Problema: "Address already in use"

### Pas 1: Găsește procesul care ocupă portul

```bash
# Linux/WSL
sudo ss -tlnp | grep 5400
# sau
sudo lsof -i :5400

# Windows PowerShell (Administrator)
netstat -ano | findstr 5400
```

### Pas 2: Oprește procesul

```bash
# Linux - oprește după PID
kill -9 <PID>

# Sau oprește containerele
docker compose -f docker/docker-compose.yml down
```

### Pas 3: Așteaptă eliberarea portului

Uneori portul rămâne în starea TIME_WAIT:
```bash
# Verifică starea
ss -tan | grep 5400

# Așteaptă ~30 secunde sau forțează în cod:
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

---

## Problema: Timeout la conectare

### Cauze posibile

1. **Serverul nu rulează** - verifică cu `docker ps`
2. **Firewall blochează** - verifică cu `ufw status`
3. **Port greșit** - verifică în docker-compose.yml
4. **Adresă greșită** - folosește `localhost`, nu `127.0.0.1` în WSL

### Mărește timeout-ul pentru debugging

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(30)  # 30 secunde în loc de default

try:
    sock.connect(('localhost', 5400))
except socket.timeout:
    print("Timeout după 30 secunde - serverul nu răspunde")
```

---

## Checklist General de Debugging

Când ceva nu funcționează:

```
□ Docker rulează?              sudo service docker status
□ Containerele sunt Up?        docker ps
□ Porturile sunt mapate?       docker ps (coloana PORTS)
□ Porturile răspund?           nc -zv localhost 5400
□ Firewallul permite?          sudo ufw status
□ Log-uri container?           docker logs <container>
□ Wireshark vede trafic?       Captură fără filtru
□ Codul folosește '!' în struct? Verifică network byte order
□ CRC include datele corecte?  Verifică ce bytes intră în calcul
```

---

## Referințe

- [README principal](../README.md)
- [Troubleshooting detaliat](troubleshooting.md)
- [FAQ](faq.md)

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
