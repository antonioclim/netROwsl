# Rezumat Teoretic – Săptămâna 5: Nivelul Rețea

> Laborator Rețele de Calculatoare – ASE, Informatică Economică
> realizat de Revolvix

## 1. Nivelul Rețea în Modelul OSI/TCP-IP

### 1.1 Funcții Principale

Nivelul Rețea (Layer 3) oferă următoarele servicii esențiale:

- **Adresare logică**: Atribuirea de identificatori unici (adrese IP) dispozitivelor, independent de adresarea fizică (MAC)
- **Rutare**: Determinarea căii optime pentru pachete între rețele diferite
- **Fragmentare și reasamblare**: Divizarea pachetelor pentru a respecta MTU-ul fiecărei rețele
- **Încapsulare**: Adăugarea antetului IP la datele primite de la nivelurile superioare

### 1.2 Relația cu Alte Niveluri

```
┌─────────────────────────────────────────┐
│  Nivelul Transport (TCP/UDP)            │
│  - Segmentare, control flux             │
├─────────────────────────────────────────┤
│  Nivelul Rețea (IP)          ← AICI     │
│  - Adresare logică, rutare              │
├─────────────────────────────────────────┤
│  Nivelul Legătură de Date (Ethernet)    │
│  - Adresare fizică (MAC), cadre         │
└─────────────────────────────────────────┘
```

## 2. Adresarea IPv4

### 2.1 Structura Adresei IPv4

Adresele IPv4 constau din **32 de biți** (4 octeți), reprezentați în **notație zecimală cu punct**:

```
192.168.1.100
│   │   │  │
│   │   │  └── Octetul 4: 100 = 01100100
│   │   └───── Octetul 3:   1 = 00000001
│   └──────── Octetul 2: 168 = 10101000
└─────────── Octetul 1: 192 = 11000000

Reprezentare binară completă:
11000000.10101000.00000001.01100100
```

### 2.2 Clase de Adrese (Istoric)

| Clasă | Primul octet | Prefix implicit | Număr rețele | Gazde/rețea |
|-------|-------------|-----------------|--------------|-------------|
| A     | 1-126       | /8              | 126          | ~16 milioane |
| B     | 128-191     | /16             | 16.384       | 65.534      |
| C     | 192-223     | /24             | ~2 milioane  | 254         |
| D     | 224-239     | N/A             | Multicast    | N/A         |
| E     | 240-255     | N/A             | Experimental | N/A         |

### 2.3 Adrese Private (RFC 1918)

| Bloc          | Clasă | Număr adrese |
|---------------|-------|--------------|
| 10.0.0.0/8    | A     | 16.777.216   |
| 172.16.0.0/12 | B     | 1.048.576    |
| 192.168.0.0/16| C     | 65.536       |

## 3. CIDR (Classless Inter-Domain Routing)

### 3.1 Notația CIDR

CIDR elimină restricțiile claselor tradiționale, permițând prefixe de lungime arbitrară:

```
192.168.10.0/26
             │
             └── Numărul de biți pentru porțiunea de rețea (26 din 32)
```

### 3.2 Calculul Componentelor CIDR

Pentru `192.168.10.14/26`:

| Componentă | Valoare | Calcul |
|------------|---------|--------|
| Biți rețea | 26 | Din prefix |
| Biți gazdă | 6 | 32 - 26 = 6 |
| Total adrese | 64 | 2^6 = 64 |
| Gazde utilizabile | 62 | 2^6 - 2 = 62 |
| Mască de rețea | 255.255.255.192 | 26 biți de 1 |
| Adresa de rețea | 192.168.10.0 | Toți biții gazdă = 0 |
| Adresa broadcast | 192.168.10.63 | Toți biții gazdă = 1 |

### 3.3 Mască Wildcard

Masca wildcard este complementul măștii de rețea:

```
Mască de rețea:  255.255.255.192 = 11111111.11111111.11111111.11000000
Mască wildcard:  0.0.0.63        = 00000000.00000000.00000000.00111111
```

## 4. Tehnici de Subnetare

### 4.1 FLSM (Fixed-Length Subnet Mask)

FLSM împarte o rețea în subrețele de **dimensiuni egale**:

**Exemplu**: Împărțirea 192.168.0.0/24 în 4 subrețele

```
Rețea originală: /24 (256 adrese)
Biți împrumutați: 2 (pentru 4 subrețele: 2² = 4)
Prefix nou: /26 (64 adrese per subrețea)

Subrețea 1: 192.168.0.0/26   (192.168.0.1 - 192.168.0.62)
Subrețea 2: 192.168.0.64/26  (192.168.0.65 - 192.168.0.126)
Subrețea 3: 192.168.0.128/26 (192.168.0.129 - 192.168.0.190)
Subrețea 4: 192.168.0.192/26 (192.168.0.193 - 192.168.0.254)
```

**Avantaje FLSM:**
- Simplu de implementat și administrat
- Sumarizare ușoară a rutelor
- Predictibilitate în alocarea adreselor

**Dezavantaje FLSM:**
- Risipă de adrese când cerințele diferă
- Inflexibil pentru rețele eterogene

### 4.2 VLSM (Variable-Length Subnet Mask)

VLSM permite subrețele de **dimensiuni diferite**, optimizând utilizarea spațiului de adrese:

**Algoritm VLSM:**
1. Sortează cerințele descrescător
2. Pentru fiecare cerință, aloca blocul minim necesar
3. Asigură alinierea la granițe de bloc (puteri de 2)

**Exemplu**: Cerințe de 60, 20, 10, 2 gazde din 192.168.0.0/24

```
Cerință 60 gazde → /26 (62 gazde) → 192.168.0.0/26
Cerință 20 gazde → /27 (30 gazde) → 192.168.0.64/27
Cerință 10 gazde → /28 (14 gazde) → 192.168.0.96/28
Cerință 2 gazde  → /30 (2 gazde)  → 192.168.0.112/30
```

### 4.3 Comparație FLSM vs VLSM

| Aspect | FLSM | VLSM |
|--------|------|------|
| Complexitate | Scăzută | Medie |
| Eficiență | Scăzută | Ridicată |
| Administrare | Simplă | Necesită planificare |
| Sumarizare | Ușoară | Mai dificilă |
| Scalabilitate | Limitată | Bună |

## 5. Adresarea IPv6

### 5.1 Motivația pentru IPv6

- Epuizarea adreselor IPv4 (4.3 miliarde)
- Necesitatea unui spațiu de adrese mult mai mare
- Îmbunătățiri în securitate, mobilitate și QoS

### 5.2 Structura Adresei IPv6

Adresele IPv6 constau din **128 de biți**, reprezentați în **notație hexazecimală**:

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
│    │    │    │    │    │    │    │
└────┴────┴────┴────┴────┴────┴────┴── 8 grupuri de 16 biți (hextete)
```

### 5.3 Reguli de Comprimare IPv6

**Regulă 1**: Zerourile de început din fiecare grup pot fi omise
```
2001:0db8:0000:0000 → 2001:db8:0:0
```

**Regulă 2**: Un singur grup consecutiv de zerouri poate fi înlocuit cu ::
```
2001:db8:0:0:0:0:0:1 → 2001:db8::1
```

**Important**: `::` poate apărea o singură dată în adresă!

### 5.4 Tipuri de Adrese IPv6

| Tip | Prefix | Descriere |
|-----|--------|-----------|
| Global Unicast | 2000::/3 | Adrese publice, rutabile pe Internet |
| Link-Local | fe80::/10 | Comunicare locală pe segment |
| Unique Local | fc00::/7 | Echivalent adreselor private IPv4 |
| Multicast | ff00::/8 | Comunicare one-to-many |
| Loopback | ::1 | Echivalent 127.0.0.1 |

### 5.5 Subnetarea IPv6

Structura tipică a unei adrese IPv6 globale:

```
2001:0db8:abcd:0001:1234:5678:90ab:cdef
├────────────────┼────┼─────────────────┤
│     48 biți    │16bi│    64 biți      │
│   Global ID    │Sub │  Interface ID   │
│  (de la ISP)   │net │ (SLAAC/manual)  │
```

- ISP-ul alocă un prefix /48
- Organizația creează subrețele /64
- Fiecare subrețea /64 are 2^64 adrese (suficient pentru orice scenariu)

## 6. Formule Esențiale

### Calcule CIDR

```
Număr total adrese = 2^(32-prefix)
Gazde utilizabile = 2^(32-prefix) - 2
Biți pentru N subrețele = ⌈log₂(N)⌉
Prefix pentru H gazde = 32 - ⌈log₂(H+2)⌉
```

### Tabel Prefixe Comune

| Prefix | Mască | Adrese | Gazde |
|--------|-------|--------|-------|
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 14 |
| /29 | 255.255.255.248 | 8 | 6 |
| /30 | 255.255.255.252 | 4 | 2 |

## 7. Referințe

1. RFC 791 - Internet Protocol (IPv4)
2. RFC 8200 - Internet Protocol, Version 6 (IPv6)
3. RFC 4632 - Classless Inter-domain Routing (CIDR)
4. RFC 1918 - Address Allocation for Private Internets
5. Kurose & Ross - Computer Networking: A Top-Down Approach

---

*Material didactic pentru Laborator Rețele de Calculatoare – ASE Bucuresti*
