# Sumar Teoretic: Săptămâna 9

> Nivelul Sesiune (L5) și Nivelul Prezentare (L6)
> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Introducere

Săptămâna 9 explorează nivelurile intermediare ale modelului OSI care fac
legătura între nivelul transport fiabil (L4) și protocoalele specifice
aplicațiilor (L7). Aceste niveluri gestionează **managementul dialogului**
(sesiune) și **reprezentarea datelor** (prezentare).

---

## Nivelul Sesiune (L5)

### Scop

Nivelul Sesiune gestionează **dialogul logic** între aplicații, oferind:

- **Stabilirea sesiunii**: Inițierea comunicării cu autentificare
- **Sincronizare**: Puncte de control pentru reluare după erori
- **Control dialog**: Gestionarea alternării în comunicarea half-duplex
- **Terminare**: Închidere grațioasă cu păstrarea stării

### Distincție Importantă: Conexiune vs Sesiune

| Aspect           | Conexiune TCP (L4)       | Sesiune (L5)              |
|------------------|--------------------------|---------------------------|
| Puncte finale    | IP:port ↔ IP:port        | Utilizator ↔ Serviciu     |
| Stare            | Numere de secvență       | Autentificare, context    |
| Persistență      | Durata de viață socket   | Poate persista între reconectări |
| Tratare erori    | Retransmisie             | Punct de control/reluare  |

### Exemple din Lumea Reală

- **Sesiuni HTTP**: Cookie-urile mențin starea utilizatorului între multiple conexiuni TCP
- **Sesiuni FTP**: Autentificarea persistă în timp ce conexiunile de date se deschid/închid
- **Conexiuni baze de date**: Starea tranzacției menținută între interogări

---

## Nivelul Prezentare (L6)

### Scop

Nivelul Prezentare gestionează transformările **sintaxei datelor**:

- **Serializare**: Convertirea structurilor de date în secvențe de octeți
- **Codificare**: Conversii între seturi de caractere (ASCII, UTF-8, etc.)
- **Compresie**: Reducerea dimensiunii datelor pentru transmisie
- **Criptare**: Protejarea confidențialității datelor

### Endianness (Ordinea Octeților)

Numerele multi-octet pot fi stocate în două moduri:

```
Valoare: 0x12345678

Big-Endian (Ordinea Rețelei):
┌────┬────┬────┬────┐
│ 12 │ 34 │ 56 │ 78 │  ← Octetul cel mai semnificativ PRIMUL
└────┴────┴────┴────┘

Little-Endian (Intel/AMD):
┌────┬────┬────┬────┐
│ 78 │ 56 │ 34 │ 12 │  ← Octetul cel mai puțin semnificativ PRIMUL
└────┴────┴────┴────┘
```

**Regula de Aur**: Protocoalele de rețea folosesc **big-endian** (network byte order).

### Caractere Format Python `struct`

| Caracter | Semnificație             | Dimensiune |
|----------|--------------------------|------------|
| `>`      | Big-endian (rețea)       | -          |
| `<`      | Little-endian            | -          |
| `!`      | Ordine rețea (= `>`)     | -          |
| `B`      | Octet fără semn          | 1 octet    |
| `H`      | Short fără semn          | 2 octeți   |
| `I`      | Int fără semn            | 4 octeți   |
| `s`      | Șir (bytes)              | n octeți   |

### Exemplu: Header Protocol

```python
import struct
import zlib

# Definește formatul header: magic(4), lungime(4), crc(4), flags(4)
FORMAT_HEADER = ">4sIII"

def impacheteaza_mesaj(payload: bytes) -> bytes:
    magic = b"FTPC"
    lungime = len(payload)
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    flags = 0
    
    header = struct.pack(FORMAT_HEADER, magic, lungime, crc, flags)
    return header + payload
```

---

## Analiza Protocolului FTP

### Arhitectură

FTP folosește **două conexiuni separate**:

1. **Conexiunea de Control** (port 21): Comenzi text, gestiunea sesiunii
2. **Conexiunea de Date** (port 20 sau dinamic): Transferuri de fișiere

```
┌─────────────┐                    ┌─────────────┐
│   Client    │──── Control ───────│   Server    │
│             │     (port 21)      │             │
│             │                    │             │
│             │──── Date ──────────│             │
│             │  (port 20/dinamic) │             │
└─────────────┘                    └─────────────┘
```

### Ciclul de Viață al Sesiunii

```
1. Conectare TCP (SYN/SYN-ACK/ACK)
2. Server: "220 Bine ați venit"
3. Client: "USER alice"
4. Server: "331 Parola necesară"
5. Client: "PASS secret"
6. Server: "230 Autentificat"      ← Sesiune stabilită
7. Client: "PWD" / "LIST" / "RETR" / etc.
8. Client: "QUIT"
9. Server: "221 La revedere"       ← Sesiune închisă
```

### Moduri de Transfer

| Mod    | Comandă   | Utilizare                   |
|--------|-----------|------------------------------|
| ASCII  | `TYPE A`  | Fișiere text (conversie sfârșit de linie) |
| Binar  | `TYPE I`  | Executabile, imagini, arhive |

### Mod Activ vs Pasiv

| Mod     | Inițiator        | Prietenos cu firewall |
|---------|------------------|----------------------|
| Activ   | Server → Client:20 | ✗ |
| Pasiv   | Client → Server:dinamic | ✓ |

---

## Aplicații Practice

### Lista de Verificare pentru Design Protocol Binar

1. **Octeți magic**: Identifică protocolul, ajută la resincronizare
2. **Câmp versiune**: Permite evoluția protocolului
3. **Câmp lungime**: Permite delimitarea mesajelor
4. **Sumă de control**: Verifică integritatea (CRC-32, MD5, SHA-256)
5. **Flags**: Caracteristici opționale (compresie, criptare)

### Formate de Serializare Comune

| Format           | Tip    | Caz de utilizare              |
|------------------|--------|-------------------------------|
| JSON             | Text   | API-uri web, lizibil de om    |
| Protocol Buffers | Binar  | Performanță înaltă, tipizat   |
| MessagePack      | Binar  | Alternativă compactă la JSON  |
| CBOR             | Binar  | IoT, dispozitive constrânse   |

---

## Concluzii Cheie

1. **Sesiune ≠ Conexiune**: Sesiunile adaugă stare la nivel de aplicație
2. **Folosiți întotdeauna ordinea rețelei** pentru portabilitate
3. **Delimitarea este esențială**: TCP nu păstrează limitele mesajelor
4. **Sumele de control detectează erori**: Includeți-le în fiecare protocol
5. **FTP separă responsabilitățile**: Control și date pe canale diferite

---

## Lectură Suplimentară

- RFC 959: File Transfer Protocol (FTP)
- RFC 4217: Securing FTP with TLS
- Stevens, W.R. *TCP/IP Illustrated, Volume 1*
- Kurose, J. & Ross, K. *Computer Networking: A Top-Down Approach*

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
