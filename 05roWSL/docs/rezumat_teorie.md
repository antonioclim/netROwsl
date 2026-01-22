# Rezumat Teoretic – Săptămâna 5

> Laborator Rețele de Calculatoare – ASE, Informatică Economică
> realizat de Revolvix

---

## Nivelul Rețea în Modelul OSI/TCP-IP

Nivelul Rețea (Network Layer, OSI Layer 3) rezolvă patru probleme:

1. **Adresarea logică** — Identificarea unică a dispozitivelor prin adrese IP
2. **Rutarea** — Determinarea căii optime pentru pachete între rețele
3. **Fragmentarea** — Împărțirea pachetelor mari pentru a se potrivi cu MTU-ul rețelei
4. **Încapsularea** — Adăugarea header-ului IP peste datele de la nivelul Transport

### Diferența față de Nivelul Legătură de Date

| Caracteristică | Nivelul Legătură (L2) | Nivelul Rețea (L3) |
|----------------|----------------------|-------------------|
| Adresare | MAC (fizică, 48 biți) | IP (logică, 32/128 biți) |
| Scop | Comunicare în aceeași rețea | Comunicare între rețele |
| Dispozitiv | Switch | Router |
| Protocol | Ethernet, Wi-Fi | IP, ICMP |

---

## Adresarea IPv4

### Structura Adresei

O adresă IPv4 are 32 de biți, reprezentați în notație zecimală cu punct:

```
   192    .   168    .    10    .    14
┌────────┬────────┬────────┬────────┐
│11000000│10101000│00001010│00001110│  = 32 biți
└────────┴────────┴────────┴────────┘
  Octet 1  Octet 2  Octet 3  Octet 4
```

### Clase de Adrese (Clasful Addressing)

| Clasă | Primul Octet | Mască Implicită | Nr. Rețele | Nr. Gazde/Rețea |
|-------|--------------|-----------------|------------|-----------------|
| A | 1-126 | /8 (255.0.0.0) | 126 | 16.777.214 |
| B | 128-191 | /16 (255.255.0.0) | 16.384 | 65.534 |
| C | 192-223 | /24 (255.255.255.0) | 2.097.152 | 254 |
| D | 224-239 | - | Multicast | - |
| E | 240-255 | - | Experimental | - |

**Notă:** Adresarea clasful este depășită. CIDR este standardul actual.

### Adrese Private (RFC 1918)

| Bloc | Interval | Utilizare Tipică |
|------|----------|------------------|
| 10.0.0.0/8 | 10.0.0.0 – 10.255.255.255 | Rețele enterprise mari |
| 172.16.0.0/12 | 172.16.0.0 – 172.31.255.255 | Rețele medii |
| 192.168.0.0/16 | 192.168.0.0 – 192.168.255.255 | Rețele casnice/mici |

### Adrese Speciale

| Adresă | Scop |
|--------|------|
| 0.0.0.0/8 | Rețeaua curentă (doar ca sursă) |
| 127.0.0.0/8 | Loopback (localhost) |
| 169.254.0.0/16 | Link-local (APIPA) |
| 224.0.0.0/4 | Multicast |
| 255.255.255.255 | Broadcast limitat |

---

## Notația CIDR

CIDR (Classless Inter-Domain Routing) permite prefixe de lungime arbitrară.

### Sintaxă

```
<adresă_IP>/<lungime_prefix>

Exemple:
  192.168.10.0/24    →  Mască: 255.255.255.0    →  256 adrese
  10.0.0.0/8         →  Mască: 255.0.0.0        →  16.777.216 adrese
  172.16.0.0/12      →  Mască: 255.240.0.0      →  1.048.576 adrese
```

### Conversia Prefix ↔ Mască

| Prefix | Mască Zecimală | Biți Rețea | Biți Gazdă | Total Adrese | Gazde Utilizabile |
|--------|----------------|------------|------------|--------------|-------------------|
| /8 | 255.0.0.0 | 8 | 24 | 16.777.216 | 16.777.214 |
| /16 | 255.255.0.0 | 16 | 16 | 65.536 | 65.534 |
| /24 | 255.255.255.0 | 24 | 8 | 256 | 254 |
| /25 | 255.255.255.128 | 25 | 7 | 128 | 126 |
| /26 | 255.255.255.192 | 26 | 6 | 64 | 62 |
| /27 | 255.255.255.224 | 27 | 5 | 32 | 30 |
| /28 | 255.255.255.240 | 28 | 4 | 16 | 14 |
| /29 | 255.255.255.248 | 29 | 3 | 8 | 6 |
| /30 | 255.255.255.252 | 30 | 2 | 4 | 2 |
| /31 | 255.255.255.254 | 31 | 1 | 2 | 2* |
| /32 | 255.255.255.255 | 32 | 0 | 1 | 0 |

*RFC 3021: /31 pentru legături point-to-point

### Formule de Calcul

```
Total Adrese = 2^(32 - prefix)
Gazde Utilizabile = 2^(32 - prefix) - 2

Exemplu pentru /26:
  Total = 2^(32-26) = 2^6 = 64
  Gazde = 64 - 2 = 62
```

---

## Componente Cheie ale unei Rețele

### 1. Adresa de Rețea

Prima adresă din bloc — identifică rețeaua. Se obține prin AND între IP și mască.

```
Exemplu: 192.168.10.14/26

IP:     11000000.10101000.00001010.00001110
Mască:  11111111.11111111.11111111.11000000
AND:    11000000.10101000.00001010.00000000  →  192.168.10.0
```

### 2. Adresa de Broadcast

Ultima adresă din bloc — trimite către toate gazdele din rețea.

```
Adresa de rețea:  192.168.10.0
Biți gazdă:       6 biți (toți pe 1)
Broadcast:        192.168.10.63  (00111111 = 63)
```

### 3. Intervalul de Gazde

Adresele utilizabile pentru dispozitive.

```
Rețea:       192.168.10.0    (rezervată)
Prima gazdă: 192.168.10.1
Ultima gazdă: 192.168.10.62
Broadcast:   192.168.10.63   (rezervată)
```

### 4. Masca Wildcard

Inversul măștii de rețea — folosită în ACL-uri și OSPF.

```
Mască:     255.255.255.192  →  11111111.11111111.11111111.11000000
Wildcard:  0.0.0.63         →  00000000.00000000.00000000.00111111
```

---

## ✓ Checkpoint: Verifică-ți Înțelegerea CIDR

Înainte de a continua, asigură-te că poți răspunde:

1. Care e formula pentru gazde utilizabile dintr-un prefix?
2. Cum calculezi adresa de broadcast pentru 10.20.30.40/27?
3. Ce prefix ai nevoie pentru 100 de gazde?

<details>
<summary>Verifică răspunsurile</summary>

1. `Gazde = 2^(32-prefix) - 2`
2. Rețea = 10.20.30.32, Broadcast = 10.20.30.63 (salt = 32)
3. Prefix /25 (126 gazde disponibile, /26 ar oferi doar 62)

</details>

---

## Subnetarea FLSM

FLSM (Fixed Length Subnet Mask) împarte o rețea în subrețele de dimensiuni egale.

### Algoritmul FLSM

1. Determină numărul de subrețele necesare (N)
2. Calculează biții de împrumut: `ceil(log2(N))`
3. Noul prefix = prefix_vechi + biți_împrumut
4. Aplică noul prefix pentru a genera subrețelele

### Exemplu: Împărțire 192.168.0.0/24 în 4 subrețele

```
Rețea originală: 192.168.0.0/24 (256 adrese)
Subrețele dorite: 4
Biți împrumut: log2(4) = 2
Prefix nou: 24 + 2 = /26

Rezultat:
┌────────────────────────────────────────────┐
│ Subrețea 1: 192.168.0.0/26                 │
│   Interval gazde: .1 - .62 (62 gazde)      │
│   Broadcast: 192.168.0.63                  │
├────────────────────────────────────────────┤
│ Subrețea 2: 192.168.0.64/26                │
│   Interval gazde: .65 - .126 (62 gazde)    │
│   Broadcast: 192.168.0.127                 │
├────────────────────────────────────────────┤
│ Subrețea 3: 192.168.0.128/26               │
│   Interval gazde: .129 - .190 (62 gazde)   │
│   Broadcast: 192.168.0.191                 │
├────────────────────────────────────────────┤
│ Subrețea 4: 192.168.0.192/26               │
│   Interval gazde: .193 - .254 (62 gazde)   │
│   Broadcast: 192.168.0.255                 │
└────────────────────────────────────────────┘
```

### Limitări FLSM

- Numărul de subrețele trebuie să fie putere de 2
- Risipă de adrese când cerințele diferă între departamente
- Nu se poate adapta la cerințe variabile

---

## Subnetarea VLSM

VLSM (Variable Length Subnet Mask) permite subrețele de dimensiuni diferite.

### Algoritmul VLSM

1. Sortează cerințele descrescător după numărul de gazde
2. Pentru fiecare cerință:
   a. Calculează prefixul minim necesar
   b. Alocă prima subrețea disponibilă cu acest prefix
   c. Marchează spațiul ca utilizat
3. Repetă până toate cerințele sunt satisfăcute

### Exemplu: VLSM pentru TechVision SRL

**Cerințe:** DEV (120), SALES (55), HR (25), IT (10), P2P (2)  
**Rețea de bază:** 172.20.0.0/22 (1022 gazde disponibile)

```
Pas 1: Sortare descrescătoare
  120, 55, 25, 10, 2

Pas 2: Alocare

DEV (120 gazde):
  Prefix necesar: /25 (126 gazde)
  Alocat: 172.20.0.0/25
  Interval: 172.20.0.1 - 172.20.0.126

SALES (55 gazde):
  Prefix necesar: /26 (62 gazde)
  Alocat: 172.20.0.128/26
  Interval: 172.20.0.129 - 172.20.0.190

HR (25 gazde):
  Prefix necesar: /27 (30 gazde)
  Alocat: 172.20.0.192/27
  Interval: 172.20.0.193 - 172.20.0.222

IT (10 gazde):
  Prefix necesar: /28 (14 gazde)
  Alocat: 172.20.0.224/28
  Interval: 172.20.0.225 - 172.20.0.238

P2P (2 gazde):
  Prefix necesar: /30 (2 gazde)
  Alocat: 172.20.0.240/30
  Interval: 172.20.0.241 - 172.20.0.242
```

### Comparație FLSM vs VLSM

| Aspect | FLSM | VLSM |
|--------|------|------|
| Complexitate | Simplă | Necesită planificare |
| Eficiență | Scăzută (risipă) | Ridicată |
| Flexibilitate | Limitată | Mare |
| Utilizare | Rețele mici, uniforme | Rețele enterprise |

---

## ✓ Checkpoint: Verifică-ți Înțelegerea VLSM

Înainte de a trece la IPv6, verifică:

1. De ce VLSM necesită sortare descrescătoare a cerințelor?
2. Dacă ai cerințele [30, 30, 30, 30], VLSM e mai eficient ca FLSM?
3. Ce se întâmplă dacă aloci o subrețea mică înainte de una mare?

<details>
<summary>Verifică răspunsurile</summary>

1. Subrețelele mari necesită aliniere la granițe specifice (multipli de dimensiunea blocului). Alocarea lor prima evită fragmentarea spațiului de adrese.
2. Nu — pentru cerințe identice, FLSM și VLSM produc același rezultat.
3. Poți "bloca" spațiu care ar fi necesar pentru subrețeaua mare, rezultând în fragmentare sau imposibilitatea alocării.

</details>

---

## Adresarea IPv6

### De ce IPv6?

IPv4 are ~4.3 miliarde de adrese. Toate au fost alocate din 2011, iar IANA a epuizat stocul central în 2019.

### Analogie: IPv4 vs IPv6

Gândește-te la adrese IP ca la coduri poștale:

- **IPv4** = cod poștal românesc (6 cifre): 010011
  - ~4.3 miliarde combinații (toate ocupate din 2019)
  - Trebuie să "împarți apartamentul" (NAT) ca să încapă toată lumea

- **IPv6** = cod poștal pentru întreaga galaxie (32 cifre hex)
  - 340 undecilioane de combinații (mai multe decât atomii de pe Pământ)
  - Fiecare dispozitiv primește adresă proprie, fără NAT

La fel cum România a trecut de la coduri poștale de 4 cifre la 6 cifre când au apărut mai multe adrese, Internetul trece de la IPv4 la IPv6.

### Structura Adresei IPv6

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
└──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘
   │        │        │        │
   │        │        │        └── Interface ID (64 biți)
   │        │        │
   │        │        └── Subnet ID
   │        │
   │        └── Site prefix
   │
   └── Global routing prefix

Total: 128 biți = 8 grupuri × 16 biți
```

### Reguli de Comprimare

1. **Zerourile din față** ale fiecărui grup pot fi omise
   ```
   2001:0db8:0000:0000 → 2001:db8:0:0
   ```

2. **Grupuri consecutive de zerouri** pot fi înlocuite cu `::`
   ```
   2001:db8:0:0:0:0:0:1 → 2001:db8::1
   ```

3. **Doar o singură** secvență `::` este permisă
   ```
   2001:0:0:1:0:0:0:1 → 2001:0:0:1::1 sau 2001::1:0:0:0:1
   NU: 2001::1::1 (ambiguu!)
   ```

### Tipuri de Adrese IPv6

| Tip | Prefix | Scop |
|-----|--------|------|
| Global Unicast | 2000::/3 | Adrese publice rutabile |
| Link-Local | fe80::/10 | Comunicare în aceeași rețea (auto-generate) |
| Unique Local | fc00::/7 | Echivalent adrese private IPv4 |
| Multicast | ff00::/8 | Grup de destinații |
| Loopback | ::1/128 | Echivalent 127.0.0.1 |
| Unspecified | ::/128 | Echivalent 0.0.0.0 |

### Autoconfigurare (SLAAC)

IPv6 permite autoconfigurarea fără server DHCP:

1. Generează adresă link-local din MAC (EUI-64)
2. Verifică unicitatea (DAD - Duplicate Address Detection)
3. Primește prefix de la router (RA - Router Advertisement)
4. Combină prefix + Interface ID pentru adresa globală

---

## Rețele Docker

### Analogie: Container Networking

Gândește-te la containere ca la apartamente într-un bloc:

- **Rețeaua Docker** = blocul de apartamente (cu o adresă de stradă)
- **Containerele** = apartamentele individuale (cu numere de apartament)
- **Port mapping** = cutia poștală de la intrare care redirecționează scrisorile

### Rețeaua week5_labnet

```yaml
networks:
  labnet:
    driver: bridge
    ipam:
      config:
        - subnet: 10.5.0.0/24
          gateway: 10.5.0.1
```

| Container | IP | Rol |
|-----------|-----|-----|
| week5_python | 10.5.0.10 | Mediu exerciții |
| week5_udp-server | 10.5.0.20 | Server Echo UDP |
| week5_udp-client | 10.5.0.30 | Client testare |

### Port Mapping

```yaml
ports:
  - "8080:80"    # host_port:container_port
```

Din Windows, accesezi `localhost:8080` → Docker redirecționează către `container:80`

---

## Formule Utile

### Calcul Rapid Prefix

| Gazde Necesare | Prefix Minim | Formula |
|----------------|--------------|---------|
| 2 | /30 | 32 - ceil(log2(2+2)) = 30 |
| 6 | /29 | 32 - ceil(log2(6+2)) = 29 |
| 14 | /28 | 32 - ceil(log2(14+2)) = 28 |
| 30 | /27 | 32 - ceil(log2(30+2)) = 27 |
| 62 | /26 | 32 - ceil(log2(62+2)) = 26 |
| 126 | /25 | 32 - ceil(log2(126+2)) = 25 |
| 254 | /24 | 32 - ceil(log2(254+2)) = 24 |

### Salt între Subrețele

```
Salt = 2^(32 - prefix) = Total adrese în subrețea

/24: salt = 256 (0, 256, 512, ...)
/25: salt = 128 (0, 128, 256, ...)
/26: salt = 64  (0, 64, 128, ...)
/27: salt = 32  (0, 32, 64, ...)
/28: salt = 16  (0, 16, 32, ...)
```

---

## Navigare Rapidă

| ← Anterior | Document | Următor → |
|------------|----------|-----------|
| [Glosar](GLOSSARY.md) | **Rezumat Teoretic** | [Fișa de Comenzi](fisa_comenzi.md) |

## Documente Înrudite

- [README Principal](../README.md) — Ghid de pornire rapidă
- [Fișa de Comenzi](fisa_comenzi.md) — Referință rapidă
- [Depanare](depanare.md) — Rezolvarea problemelor
- [Referință API](api_reference.md) — Documentație funcții
- [Exemple](exemple_utilizare.md) — Scenarii complete

---

*Material didactic pentru Laborator Rețele de Calculatoare – ASE București*
