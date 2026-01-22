# Rezumat Teoretic: Nivelul Fizic și Nivelul Legătură de Date

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

## Cuprins
1. [Nivelul Fizic](#nivelul-fizic)
2. [Nivelul Legătură de Date](#nivelul-legătură-de-date)
3. [Tehnici de Încadrare](#tehnici-de-încadrare)
4. [Detectarea Erorilor](#detectarea-erorilor)
5. [Protocoale de Laborator](#protocoale-de-laborator)
6. [Analogii pentru Înțelegere](#analogii-pentru-înțelegere)

---

## Nivelul Fizic

### Definiție

Nivelul Fizic (Physical Layer) este primul nivel din modelul OSI, care transmite biții bruti prin mediul fizic de comunicare.

---
**PREDICȚIE:** Înainte de a continua:
1. Ce crezi că se întâmplă cu un semnal electric când parcurge un cablu de 100m?
2. De ce crezi că fibra optică poate transmite pe distanțe mai mari decât cablul de cupru?
---

### Funcții Principale

Nivelul fizic îndeplinește patru funcții: transmisia biților (convertește datele în semnale electrice sau optice), sincronizarea între emițător și receptor pentru coordonarea timing-ului, specificarea caracteristicilor fizice ale mediului (conectori, tensiuni, frecvențe) și definirea topologiei rețelei.

### Tipuri de Medii de Transmisie

**Medii Ghidate (Cu Fir)**

Cablul coaxial era utilizat în rețelele mai vechi și oferă rezistență bună la interferențe. Cablul torsadat (UTP/STP) este cel mai comun în rețelele LAN moderne datorită costului redus și instalării ușoare. Fibra optică permite viteze foarte mari și imunitate la interferențe electromagnetice, fiind preferată pentru distanțe lungi.

**Medii Neghidate (Fără Fir)**

Undele radio sunt folosite pentru WiFi și Bluetooth. Microundele servesc pentru legături punct-la-punct pe distanțe mari. Infraroșul este limitat la comunicații pe distanțe scurte, cum ar fi telecomenzile.

### Codificări de Linie

NRZ (Non-Return to Zero) este cea mai simplă codificare dar are probleme de sincronizare la secvențe lungi de biți identici. Manchester rezolvă problema sincronizării prin tranziție la mijlocul fiecărui bit. 4B/5B adaugă redundanță pentru a evita secvențele problematice.

---

## Nivelul Legătură de Date

### Definiție

Nivelul Legătură de Date (Data Link Layer) este al doilea nivel din modelul OSI, care transferă date fiabil între noduri adiacente.

### Sub-niveluri (IEEE 802)

**LLC (Logical Link Control)** se ocupă de controlul fluxului, multiplexarea protocoalelor și secvențierea cadrelor.

**MAC (Media Access Control)** gestionează adresarea fizică (adrese MAC), controlul accesului la mediu și detectarea coliziunilor.

### Funcții Principale

**Încadrarea (Framing)** grupează biții în unități logice numite cadre (frames).

**Adresarea Fizică** identifică unic dispozitivele prin adrese MAC de 48 biți.

**Controlul Accesului la Mediu** coordonează accesul când mai multe dispozitive partajează mediul — CSMA/CD pentru Ethernet cu fir, CSMA/CA pentru rețele wireless.

**Detectarea și Corectarea Erorilor** identifică și opțional corectează erorile de transmisie.

**Controlul Fluxului** previne supraîncărcarea receptorului.

---

## Tehnici de Încadrare

---
**PREDICȚIE:** Înainte de a citi despre încadrare:
1. Cum ar ști receptorul unde se termină un mesaj și unde începe următorul?
2. Ce probleme pot apărea dacă datele conțin aceleași caractere ca delimitatorii?
---

### Numărare Caractere (Prefix de Lungime)

Primul câmp al cadrului specifică numărul de caractere/octeți. Această metodă este simplă de implementat și eficientă (overhead minim), dar o eroare în câmpul de lungime poate pierde sincronizarea, iar recuperarea devine dificilă.

Exemplu (Protocolul TEXT):
```
"13 SET cheie val"
 ↑
 Lungime = 13 caractere ("SET cheie val")
```

### Delimitatori (Caractere de Bornare)

Caractere speciale marchează începutul și sfârșitul cadrului. Oferă rezistență mai bună la erori și sincronizare ușoară, dar necesită escaping pentru date care conțin delimitatorul.

Exemplu:
```
FLAG | DATE | FLAG
0x7E | ...  | 0x7E
```

### Inserare de Biți (Bit Stuffing)

Inserarea automată de biți previne confuzia cu delimitatorii. În HDLC, după 5 biți consecutivi de 1 se inserează un 0.

### Câmpuri de Dimensiune Fixă

Toate cadrele au exact aceeași dimensiune. Parsarea devine foarte simplă și metoda e bună pentru aplicații real-time, dar risipește spațiu pentru mesaje scurte și necesită fragmentare pentru date mari.

Exemplu (Protocol Senzor UDP): fiecare datagramă are exact 23 de octeți.

---

## Detectarea Erorilor

---
**PREDICȚIE:** Înainte de a studia CRC:
1. De ce CRC32 nu este potrivit pentru securitate, deși detectează erori foarte bine?
2. Care e diferența dintre detectare și corectare de erori?
3. Ce tip de erori crezi că sunt mai frecvente: biți singulari sau rafale?
---

### Tipuri de Erori

Erorile de bit singur afectează doar un bit. Erorile de rafală (burst) afectează o secvență de biți consecutivi. Erorile aleatorii afectează biți în poziții nepredictibile.

### Tehnici de Detectare

**Paritate** — Adaugă un bit care face numărul total de 1-uri par sau impar. Detectează doar erori de un singur bit.

Exemplu paritate pară:
```
Date: 1010001 → Adaugă 1 → 10100011 (număr par de 1)
```

**Checksum (Sumă de Control)** — Suma tuturor octeților din date. Folosit în IP, TCP, UDP. Simplu și rapid, dar nu detectează reordonarea.

**CRC (Cyclic Redundancy Check)** — Tratează datele ca un polinom și calculează restul împărțirii la un polinom generator.

CRC32 folosește polinomul 0x04C11DB7 și produce o verificare de 32 de biți. Detectează 100% din erorile de 1 bit, 100% din erorile de 2 biți, 100% din erorile de rafală până la 32 de biți și 99.99999995% din erorile aleatorii.

Calcul CRC32 în Python:
```python
import binascii

date = b"Mesaj de test"
crc = binascii.crc32(date) & 0xFFFFFFFF
print(f"CRC32: 0x{crc:08X}")
```

**Hash-uri Criptografice** (MD5, SHA-1, SHA-256) oferă verificare integritate cu rezistență la manipulare intenționată. CRC NU este potrivit pentru securitate!

---

## Protocoale de Laborator

### Protocol TEXT (TCP:5400)

Protocol simplu, lizibil de către om.

Format Mesaj:
```
<LUNGIME> <COMANDĂ> [<ARGUMENTE>]
```

Comenzi:

| Comandă | Format | Descriere |
|---------|--------|-----------|
| PING | `4 PING` | Test conectivitate |
| SET | `<L> SET <cheie> <valoare>` | Setare valoare |
| GET | `<L> GET <cheie>` | Citire valoare |
| DEL | `<L> DEL <cheie>` | Ștergere cheie |
| COUNT | `5 COUNT` | Numărare chei |
| KEYS | `4 KEYS` | Listare chei |
| QUIT | `4 QUIT` | Închidere conexiune |

### Protocol BINAR (TCP:5401)

Protocol eficient cu antet fix.

Structura Antetului (14 octeți):
```
┌─────────┬──────────┬─────┬────────┬──────────┬───────┐
│ Magic   │ Versiune │ Tip │ Lungime│ Secvență │ CRC32 │
│ 2 octeți│ 1 octet  │1 oct│ 2 oct  │ 4 octeți │ 4 oct │
└─────────┴──────────┴─────┴────────┴──────────┴───────┘
```

Tipuri de Mesaje:

| Cod | Nume | Descriere |
|-----|------|-----------|
| 0x01 | PING | Verificare conexiune |
| 0x02 | PONG | Răspuns PING |
| 0x03 | SET | Setare valoare |
| 0x04 | GET | Citire valoare |
| 0x05 | DELETE | Ștergere cheie |
| 0x06 | RESPONSE | Răspuns generic |
| 0xFF | ERROR | Eroare |

### Protocol Senzor UDP (UDP:5402)

Protocol pentru dispozitive IoT cu datagrame fixe.

Structura Datagramei (23 octeți):
```
┌──────────┬─────────┬─────────────┬─────────┬───────┬──────────┐
│ Versiune │ ID Senz │ Temperatură │ Locație │ CRC32 │ Rezervat │
│ 1 octet  │ 2 oct   │ 4 oct (flt) │ 10 oct  │ 4 oct │ 2 oct    │
└──────────┴─────────┴─────────────┴─────────┴───────┴──────────┘
```

---

## Comparație TCP vs UDP

| Caracteristică | TCP | UDP |
|----------------|-----|-----|
| Orientat conexiune | Da | Nu |
| Fiabilitate | Garantată | Negarantată |
| Ordonare | Garantată | Negarantată |
| Control flux | Da | Nu |
| Overhead | Mai mare | Mai mic |
| Utilizare | Web, email, fișiere | Streaming, jocuri, DNS |

---

## Analogii pentru Înțelegere

### CRC32 — Cifra de Control

**CONCRET:** Gândește-te la codul numeric personal (CNP) sau la IBAN. Ultima cifră e calculată din celelalte. Dacă greșești o cifră când copiezi, sistemul detectează eroarea. Nu poți "ghici" un cod valid fără să calculezi. DAR: cineva care știe algoritmul poate genera coduri false — de aceea CRC nu oferă securitate!

CRC32 funcționează identic, dar pentru date binare.

**PICTORIAL:**
```
Date originale:    [D][A][T][E][ ][ ][ ]
                         ↓ algoritm CRC32
Checksum:          [C][R][C][!]

Transmis:          [D][A][T][E][ ][ ][ ][C][R][C][!]
                   └─────────────────┘ └─────────┘
                         date           verificare
                         
La recepție:
1. Extrage CRC primit
2. Recalculează CRC din date
3. Compară → egal = OK, diferit = EROARE
```

**ABSTRACT:**
```python
crc = binascii.crc32(date) & 0xFFFFFFFF
```

---

### Antet Protocol BINAR — Plicul Poștal

**CONCRET:** Un plic de scrisoare conține adresa destinatarului (cine primește), adresa expeditorului (cine trimite), timbrul (dovadă că e valid) și înăuntru scrisoarea propriu-zisă.

Antetul binar e "plicul" pentru datele tale.

**PICTORIAL:**
```
┌──────────────────────────────────────────────────────┐
│ PLIC (Antet - 14 octeți)                             │
│ ┌──────┬──────┬─────┬────────┬────────┬───────────┐ │
│ │Timbru│Vers. │ Tip │Lungime │Nr.ord. │Semnătură  │ │
│ │ "NP" │  1   │0x01 │   0    │   1    │ CRC32     │ │
│ │ 2B   │ 1B   │ 1B  │  2B    │  4B    │   4B      │ │
│ └──────┴──────┴─────┴────────┴────────┴───────────┘ │
├──────────────────────────────────────────────────────┤
│ SCRISOARE (Payload - lungime variabilă)              │
│ [conținutul efectiv al mesajului]                    │
└──────────────────────────────────────────────────────┘
```

**ABSTRACT:**
```python
antet = struct.pack('!2sBBHII', b'NP', 1, tip, lungime, seq, crc)
mesaj = antet + payload
```

---

### TCP vs UDP — Telefon vs SMS

**CONCRET:**

| TCP = Apel telefonic | UDP = SMS |
|---------------------|-----------|
| Suni, aștepți să răspundă | Trimiți direct |
| "Alo?" - "Da?" (handshake) | Fără confirmare |
| Vorbești alternativ | Fire-and-forget |
| Știi când s-a încheiat | Nu știi dacă a ajuns |
| Dacă nu auzi, ceri repetare | Dacă se pierde, ghinion |
| Conexiune stabilită | Fără conexiune |

**PICTORIAL - Handshake TCP:**
```
┌────────┐                          ┌────────┐
│ Client │                          │ Server │
└───┬────┘                          └───┬────┘
    │                                   │
    │ ─────── SYN (seq=x) ──────────>   │
    │                                   │
    │ <─── SYN-ACK (seq=y, ack=x+1) ──  │
    │                                   │
    │ ─────── ACK (ack=y+1) ─────────>  │
    │                                   │
    │         [Conexiune stabilită]     │
```

---

### Port Mapping — Apartamente în Bloc

**CONCRET:**
- Blocul = calculatorul (adresa IP)
- Scara = interfața de rețea
- Apartamentul = aplicația (portul)
- Adresa completă: Bloc 5, Ap. 23 = 192.168.1.5:8080

Docker port mapping `-p 8080:80` înseamnă: "Cine bate la ușa blocului cerând ap. 8080, trimite-l la ap. 80 din interiorul containerului"

```
                  Exterior              Interior Container
                  (host)                
Vizitator → [Bloc:Ap.8080] ──mapping──→ [Container:Ap.80] → Nginx
```

---

## Referințe

1. Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach*. Pearson.
2. Tanenbaum, A. & Wetherall, D. (2011). *Computer Networks*. Pearson.
3. RFC 793 - Transmission Control Protocol
4. RFC 768 - User Datagram Protocol
5. IEEE 802.3 - Ethernet Standard

Pentru mai multe resurse, vezi [Lectură Suplimentară](further_reading.md).
Pentru comenzi practice, vezi [Fișa de Comenzi](commands_cheatsheet.md).

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
