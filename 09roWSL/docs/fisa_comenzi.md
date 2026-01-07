# Fișă de Comenzi: Săptămâna 9

> Referință Rapidă pentru Laborator
> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

---

## Comenzi Docker

### Gestionare Containere

```bash
# Pornește toate serviciile
docker compose up -d

# Oprește toate serviciile
docker compose down

# Vizualizează containerele active
docker ps

# Vizualizează toate containerele
docker ps -a

# Urmărește log-urile
docker logs -f s9_ftp-server

# Intrare în container
docker exec -it s9_ftp-server /bin/bash

# Repornește un serviciu
docker compose restart ftp-server
```

### Curățare

```bash
# Oprește și șterge containerele
docker compose down

# Oprește, șterge containerele și volumele
docker compose down -v

# Curăță resursele neutilizate
docker system prune -f

# Curăță totul (atenție!)
docker system prune -a --volumes
```

---

## Comenzi FTP

### Comenzi de Bază

| Comandă | Descriere | Exemplu |
|---------|-----------|---------|
| `USER`  | Specifică utilizatorul | `USER test` |
| `PASS`  | Trimite parola | `PASS 12345` |
| `PWD`   | Afișează directorul curent | `PWD` |
| `CWD`   | Schimbă directorul | `CWD /uploads` |
| `LIST`  | Listează conținutul | `LIST` |
| `RETR`  | Descarcă fișier | `RETR fisier.txt` |
| `STOR`  | Încarcă fișier | `STOR fisier.txt` |
| `DELE`  | Șterge fișier | `DELE fisier.txt` |
| `MKD`   | Creează director | `MKD nou_dir` |
| `QUIT`  | Închide sesiunea | `QUIT` |

### Moduri Transfer

| Comandă | Descriere |
|---------|-----------|
| `PASV`  | Activează mod pasiv |
| `PORT`  | Specifică port pentru mod activ |
| `TYPE A`| Mod ASCII (text) |
| `TYPE I`| Mod binar (imagine) |

### Coduri Răspuns FTP

| Cod | Semnificație |
|-----|--------------|
| 220 | Serviciu pregătit |
| 230 | Autentificare reușită |
| 331 | Utilizator OK, parola necesară |
| 530 | Autentificare eșuată |
| 150 | Se deschide conexiunea de date |
| 226 | Transfer complet |
| 550 | Fișier indisponibil |

---

## Python struct

### Specificatori de Ordine

| Caracter | Ordine Octeți | Utilizare |
|----------|---------------|-----------|
| `>`      | Big-endian    | Protocoale rețea |
| `<`      | Little-endian | Intel/AMD local |
| `!`      | Network       | Echivalent cu `>` |
| `=`      | Native        | Sistemul curent |

### Caractere Format

| Caracter | Tip C | Dimensiune | Exemplu Python |
|----------|-------|------------|----------------|
| `B`      | unsigned char | 1 | `struct.pack(">B", 255)` |
| `H`      | unsigned short | 2 | `struct.pack(">H", 65535)` |
| `I`      | unsigned int | 4 | `struct.pack(">I", 0xDEADBEEF)` |
| `Q`      | unsigned long long | 8 | `struct.pack(">Q", 2**64-1)` |
| `s`      | char[] | n | `struct.pack("4s", b"TEST")` |
| `f`      | float | 4 | `struct.pack(">f", 3.14)` |
| `d`      | double | 8 | `struct.pack(">d", 3.14159)` |

### Exemple

```python
import struct

# Împachetare
date = struct.pack(">I", 0x12345678)
# Rezultat: b'\x12\x34\x56\x78'

# Despachetare
valoare = struct.unpack(">I", date)[0]
# Rezultat: 305419896 (0x12345678)

# Header complex
header = struct.pack(">4sHHI", b"FTPC", 1, 0, 1024)
```

---

## CRC-32

### Utilizare de Bază

```python
import zlib

# Calculează CRC-32
date = b"Date de verificat"
crc = zlib.crc32(date) & 0xFFFFFFFF

# Verificare
crc_verificare = zlib.crc32(date) & 0xFFFFFFFF
if crc == crc_verificare:
    print("Integritate OK")
```

### În Protocol

```python
def creeaza_mesaj(payload: bytes) -> bytes:
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    header = struct.pack(">4sII", b"FTPC", len(payload), crc)
    return header + payload

def verifica_mesaj(mesaj: bytes) -> bool:
    magic, lungime, crc = struct.unpack(">4sII", mesaj[:12])
    payload = mesaj[12:]
    return crc == (zlib.crc32(payload) & 0xFFFFFFFF)
```

---

## Filtre Wireshark

### FTP

```
# Tot traficul FTP
ftp

# Doar comenzile FTP
ftp.request

# Doar răspunsurile FTP
ftp.response

# Comandă specifică
ftp.request.command == "USER"

# Cod răspuns specific
ftp.response.code == 230

# Trafic de date FTP
ftp-data

# Pe port specific
tcp.port == 2121
```

### TCP General

```
# Trafic pe port
tcp.port == 21

# Interval de porturi
tcp.port >= 60000 and tcp.port <= 60010

# Adresă IP specifică
ip.addr == 172.29.9.2

# Doar pachetele cu date
tcp.len > 0

# Flags TCP
tcp.flags.syn == 1
tcp.flags.fin == 1
```

---

## Scripturi Laborator

### Pornire/Oprire

```bash
# Pornește laboratorul
python scripts/porneste_lab.py

# Verifică starea
python scripts/porneste_lab.py --status

# Oprește laboratorul
python scripts/opreste_lab.py

# Curățare completă
python scripts/curata.py --complet
```

### Demonstrații

```bash
# Lista demonstrațiilor
python scripts/ruleaza_demo.py --lista

# Rulează demo specific
python scripts/ruleaza_demo.py --demo endianness
python scripts/ruleaza_demo.py --demo ftp_sesiune
python scripts/ruleaza_demo.py --demo protocol_binar

# Toate demonstrațiile
python scripts/ruleaza_demo.py --toate
```

### Teste

```bash
# Test rapid (< 60 secunde)
python tests/test_rapid.py

# Teste mediu
python tests/test_mediu.py

# Teste exerciții
python tests/test_exercitii.py
```

---

## Rețea Docker - Săptămâna 9

| Resursă | Valoare |
|---------|---------|
| Rețea | week9_ftp_network |
| Subnet | 172.29.9.0/24 |
| Gateway | 172.29.9.1 |
| Server FTP | s9_ftp-server |
| Client 1 | s9_client1 |
| Client 2 | s9_client2 |

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
