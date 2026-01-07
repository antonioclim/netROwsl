# Rezumat Teoretic: Nivelul Fizic și Nivelul Legătură de Date

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

## Cuprins
1. [Nivelul Fizic](#nivelul-fizic)
2. [Nivelul Legătură de Date](#nivelul-legătură-de-date)
3. [Tehnici de Încadrare](#tehnici-de-încadrare)
4. [Detectarea Erorilor](#detectarea-erorilor)
5. [Protocoale de Laborator](#protocoale-de-laborator)

---

## Nivelul Fizic

### Definiție
Nivelul Fizic (Physical Layer) este primul nivel din modelul OSI, responsabil pentru transmisia biților bruti prin mediul fizic de comunicare.

### Funcții Principale
- **Transmisia biților**: Convertirea fluxului de biți în semnale fizice
- **Sincronizarea**: Coordonarea timpilor de transmisie și recepție
- **Specificații fizice**: Definirea conectorilor, cablurilor, tensiunilor
- **Topologia rețelei**: Definirea configurației fizice a rețelei

### Tipuri de Medii de Transmisie

#### Medii Ghidate (Cu Fir)
- **Cablu coaxial**: Utilizat în rețele mai vechi, rezistent la interferențe
- **Cablu torsadat (UTP/STP)**: Cel mai comun în rețele LAN moderne
- **Fibră optică**: Viteze mari, imunitate la interferențe electromagnetice

#### Medii Neghidate (Fără Fir)
- **Unde radio**: WiFi, Bluetooth
- **Microunde**: Legături punct-la-punct
- **Infraroșu**: Comunicații pe distanțe scurte

### Codificări de Linie
- **NRZ (Non-Return to Zero)**: Cel mai simplu, probleme de sincronizare
- **Manchester**: Tranziție la mijlocul fiecărui bit, auto-sincronizare
- **4B/5B**: Codificare cu redundanță pentru evitarea secvențelor lungi de 0

---

## Nivelul Legătură de Date

### Definiție
Nivelul Legătură de Date (Data Link Layer) este al doilea nivel din modelul OSI, responsabil pentru transferul fiabil de date între noduri adiacente.

### Sub-niveluri (IEEE 802)

#### LLC (Logical Link Control)
- Controlul fluxului
- Multiplexarea protocoalelor
- Secvențierea cadrelor

#### MAC (Media Access Control)
- Adresarea fizică (adrese MAC)
- Controlul accesului la mediu
- Detectarea coliziunilor

### Funcții Principale

#### 1. Încadrarea (Framing)
Gruparea biților în unități logice numite cadre (frames).

#### 2. Adresarea Fizică
Identificarea unică a dispozitivelor prin adrese MAC (48 biți).

#### 3. Controlul Accesului la Mediu
Coordonarea accesului când mai multe dispozitive partajează mediul:
- **CSMA/CD**: Pentru Ethernet cu fir
- **CSMA/CA**: Pentru rețele wireless

#### 4. Detectarea și Corectarea Erorilor
Identificarea și opțional corectarea erorilor de transmisie.

#### 5. Controlul Fluxului
Prevenirea supraîncărcării receptorului.

---

## Tehnici de Încadrare

### 1. Numărare Caractere (Prefix de Lungime)
Primul câmp al cadrului specifică numărul de caractere/octeți.

**Avantaje:**
- Simplu de implementat
- Eficient (overhead minim)

**Dezavantaje:**
- O eroare în câmpul de lungime pierde sincronizarea
- Recuperarea dificilă după erori

**Exemplu (Protocolul TEXT):**
```
"13 SET cheie val"
 ↑
 Lungime = 13 caractere ("SET cheie val")
```

### 2. Delimitatori (Caractere de Bornare)
Caractere speciale marchează începutul și sfârșitul cadrului.

**Avantaje:**
- Rezistență mai bună la erori
- Sincronizare ușoară

**Dezavantaje:**
- Necesită escaping pentru date care conțin delimitatorul
- Overhead suplimentar

**Exemplu:**
```
FLAG | DATE | FLAG
0x7E | ...  | 0x7E
```

### 3. Inserare de Biți (Bit Stuffing)
Inserarea automată de biți pentru a preveni confuzia cu delimitatorii.

**Regulă (HDLC):** După 5 biți consecutivi de 1, se inserează un 0.

### 4. Câmpuri de Dimensiune Fixă
Toate cadrele au exact aceeași dimensiune.

**Avantaje:**
- Parsare foarte simplă
- Bun pentru aplicații real-time

**Dezavantaje:**
- Risipă pentru mesaje scurte
- Necesită fragmentare pentru date mari

**Exemplu (Protocol Senzor UDP):**
```
Fiecare datagramă = 23 octeți exact
```

---

## Detectarea Erorilor

### Tipuri de Erori
- **Eroare de bit singur**: Un singur bit este inversat
- **Eroare de rafală (burst)**: Secvență de biți consecutivi afectați
- **Eroare aleatoare**: Biți afectați în poziții aleatorii

### Tehnici de Detectare

#### 1. Paritate
Adăugarea unui bit care face numărul total de 1-uri par sau impar.

**Paritate Pară:**
```
Date: 1010001 → Adaugă 1 → 10100011 (număr par de 1)
```

**Limitări:**
- Detectează doar erori de un singur bit
- Nu detectează erori de 2 biți

#### 2. Checksum (Sumă de Control)
Suma tuturor octeților din date.

**Utilizare:** IP, TCP, UDP

**Avantaje:** Simplu, rapid

**Dezavantaje:** Nu detectează reordonarea

#### 3. CRC (Cyclic Redundancy Check)
Tratarea datelor ca un polinom și împărțirea la un polinom generator.

**CRC32:**
- Polinom: 0x04C11DB7
- Lungime verificare: 32 biți
- Detectează:
  - 100% erori de 1 bit
  - 100% erori de 2 biți
  - 100% erori de rafală ≤ 32 biți
  - 99.99999995% erori aleatorii

**Calcul CRC32 în Python:**
```python
import binascii

date = b"Mesaj de test"
crc = binascii.crc32(date) & 0xFFFFFFFF
print(f"CRC32: 0x{crc:08X}")
```

#### 4. Hash-uri Criptografice
MD5, SHA-1, SHA-256 - pentru verificare integritate cu rezistență la manipulare intenționată.

**Notă:** CRC NU este potrivit pentru securitate!

---

## Protocoale de Laborator

### Protocol TEXT (TCP:5400)
Protocol simplu, lizibil de către om.

**Format Mesaj:**
```
<LUNGIME> <COMANDĂ> [<ARGUMENTE>]
```

**Comenzi:**
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

**Structura Antetului (14 octeți):**
```
┌─────────┬──────────┬─────┬────────┬──────────┬───────┐
│ Magic   │ Versiune │ Tip │ Lungime│ Secvență │ CRC32 │
│ 2 octeți│ 1 octet  │1 oct│ 2 oct  │ 4 octeți │ 4 oct │
└─────────┴──────────┴─────┴────────┴──────────┴───────┘
```

**Tipuri de Mesaje:**
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

**Structura Datagramei (23 octeți):**
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

## Referințe

1. Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach*. Pearson.
2. Tanenbaum, A. & Wetherall, D. (2011). *Computer Networks*. Pearson.
3. RFC 793 - Transmission Control Protocol
4. RFC 768 - User Datagram Protocol
5. IEEE 802.3 - Ethernet Standard

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
