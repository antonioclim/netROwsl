# Exerciții de Trace și Analiză – Săptămâna 5

> Exerciții non-coding pentru înțelegerea algoritmilor
> Laborator Rețele de Calculatoare – ASE, Informatică Economică

---

## Scopul Exercițiilor Trace

Aceste exerciții te ajută să înțelegi algoritmii **fără a scrie cod**:
- Urmărești pașii manual pe hârtie
- Verifici înțelegerea prin predicții
- Compari rezultatul cu scriptul doar la final

**Recomandare:** Completează pe hârtie ÎNAINTE de a rula verificarea.

---

## Exercițiul T1: Trace Algoritm VLSM

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 20 min | ★★★☆☆ | APPLY | Formula prefix, sortare |

### Input

- **Rețea de bază:** `10.0.0.0/24`
- **Cerințe:** 50, 25, 10, 2 gazde

### Instrucțiuni

Urmărește manual algoritmul VLSM. NU rula scriptul încă.

### Pasul 1: Sortare

Sortează cerințele descrescător:

```
Cerințe originale: 50, 25, 10, 2
Cerințe sortate:   ____, ____, ____, ____
```

### Pasul 2: Calcul Prefixe

Pentru fiecare cerință, calculează prefixul necesar.

Formula: `prefix = 32 - ceil(log2(gazde + 2))`

| Cerință | gazde + 2 | log2 | ceil | 32 - ceil | Prefix |
|---------|-----------|------|------|-----------|--------|
| 50 | 52 | 5.7 | 6 | 26 | /26 |
| 25 | | | | | |
| 10 | | | | | |
| 2 | | | | | |

### Pasul 3: Alocare Secvențială

Alocă subrețelele în ordine, începând de la adresa de bază.

| # | Cerință | Prefix | Adresa de început | Adresa de sfârșit | Broadcast |
|---|---------|--------|-------------------|-------------------|-----------|
| 1 | 50 | /26 | 10.0.0.0 | 10.0.0.62 | 10.0.0.63 |
| 2 | 25 | | | | |
| 3 | 10 | | | | |
| 4 | 2 | | | | |

**Hint:** Următoarea subrețea începe imediat după broadcast-ul precedentei.

### Pasul 4: Verificare

Rulează scriptul și compară cu calculele tale:

```bash
python3 src/exercises/ex_5_02_vlsm_ipv6.py vlsm 10.0.0.0/24 --cerinte 50,25,10,2
```

### Soluție Completă

<details>
<summary>Click pentru soluție</summary>

**Sortare:** 50, 25, 10, 2 (deja sortate)

**Prefixe:**
| Cerință | Prefix |
|---------|--------|
| 50 | /26 (62 gazde) |
| 25 | /27 (30 gazde) |
| 10 | /28 (14 gazde) |
| 2 | /30 (2 gazde) |

**Alocare:**
| # | Cerință | Subrețea | Interval Gazde |
|---|---------|----------|----------------|
| 1 | 50 | 10.0.0.0/26 | .1 - .62 |
| 2 | 25 | 10.0.0.64/27 | .65 - .94 |
| 3 | 10 | 10.0.0.96/28 | .97 - .110 |
| 4 | 2 | 10.0.0.112/30 | .113 - .114 |

</details>

---

## Exercițiul T2: Trace Operație AND pentru Adresa de Rețea

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 15 min | ★★☆☆☆ | APPLY | Conversie binară |

### Input

Interfață configurată: `172.16.147.89/21`

### Instrucțiuni

Calculează manual adresa de rețea folosind operația AND.

### Pasul 1: Conversie la Binar

Convertește IP-ul și masca la binar:

```
172 = ________
 16 = ________
147 = ________
 89 = ________

Mască /21 = 11111111.11111111.11111___._________
```

### Pasul 2: Operația AND

```
IP:    ________.________.________.________
Mască: 11111111.11111111.11111000.00000000
AND:   ________.________.________.________
```

### Pasul 3: Conversie la Zecimal

```
Adresa de rețea: ___.___.___.___
```

### Pasul 4: Calcul Broadcast

```
Broadcast = Adresa de rețea + (2^(32-21) - 1)
          = ___.___.___.___
```

### Verificare

```bash
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 172.16.147.89/21
```

### Soluție

<details>
<summary>Click pentru soluție</summary>

**Binar:**
```
172 = 10101100
 16 = 00010000
147 = 10010011
 89 = 01011001

IP:    10101100.00010000.10010011.01011001
Mască: 11111111.11111111.11111000.00000000
AND:   10101100.00010000.10010000.00000000
```

**Adresa de rețea:** 172.16.144.0  
**Broadcast:** 172.16.151.255 (144 + 2047 = ...151.255)  
**Gazde:** 2046

</details>

---

## Exercițiul T3: Trace FLSM

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 10 min | ★★☆☆☆ | APPLY | log2, puteri ale lui 2 |

### Input

- **Rețea:** `192.168.100.0/24`
- **Subrețele necesare:** 8

### Instrucțiuni

### Pasul 1: Calcul Biți Împrumutați

```
Număr subrețele: 8
Biți necesari: log2(8) = ____
Prefix nou: 24 + ____ = ____
```

### Pasul 2: Calcul Salt

```
Salt = 2^(32 - prefix_nou) = 2^____ = ____
```

### Pasul 3: Listare Subrețele

| # | Adresa de Rețea | Broadcast | Prima Gazdă | Ultima Gazdă |
|---|-----------------|-----------|-------------|--------------|
| 1 | 192.168.100.0 | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |

### Verificare

```bash
python3 src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.100.0/24 8
```

<details>
<summary>Click pentru soluție</summary>

**Calcule:**
- Biți împrumutați: log2(8) = 3
- Prefix nou: 24 + 3 = /27
- Salt: 2^(32-27) = 2^5 = 32

**Subrețele:**
| # | Adresa | Broadcast | Prima | Ultima |
|---|--------|-----------|-------|--------|
| 1 | .0 | .31 | .1 | .30 |
| 2 | .32 | .63 | .33 | .62 |
| 3 | .64 | .95 | .65 | .94 |
| 4 | .96 | .127 | .97 | .126 |
| 5 | .128 | .159 | .129 | .158 |
| 6 | .160 | .191 | .161 | .190 |
| 7 | .192 | .223 | .193 | .222 |
| 8 | .224 | .255 | .225 | .254 |

</details>

---

## Exercițiul T4: Analiză Captură Wireshark

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 15 min | ★★★☆☆ | ANALYZE | Wireshark instalat |

### Pregătire

Dacă nu ai o captură, generează una:

```bash
# În terminalul WSL
cd /mnt/d/RETELE/SAPT5/05roWSL

# Pornește containerele
python3 scripts/porneste_laborator.py

# Generează trafic (într-un terminal)
docker exec week5_python ping -c 5 10.5.0.20
```

În Wireshark, capturează pe `vEthernet (WSL)` în timpul ping-ului.

### Analiză Pachet ICMP

Pentru primul pachet ICMP Echo Request, completează:

| Câmp | Valoare |
|------|---------|
| IP Sursă | |
| IP Destinație | |
| TTL | |
| Protocol (număr) | |
| Lungime totală IP header | |
| Lungime payload ICMP | |
| Checksum valid? | Da / Nu |

### Întrebări

1. **Ce se întâmplă cu TTL-ul la fiecare hop?**

2. **De ce pachetul ICMP Reply are adresele inversate?**

3. **Care e diferența între Echo Request și Echo Reply în câmpul Type?**

<details>
<summary>Click pentru răspunsuri</summary>

1. TTL-ul scade cu 1 la fiecare router traversat
2. Destinatarul devine sursa răspunsului (și invers)
3. Echo Request = Type 8, Echo Reply = Type 0

</details>

---

## Exercițiul T5: Trace Comprimare IPv6

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 10 min | ★★☆☆☆ | APPLY | Reguli comprimare IPv6 |

### Input

Adresa: `2001:0db8:0000:0000:0000:0000:0000:0001`

### Instrucțiuni

Aplică regulile de comprimare pas cu pas:

### Pasul 1: Elimină Zerourile din Față

```
Original: 2001:0db8:0000:0000:0000:0000:0000:0001
Pas 1:    ____:____:____:____:____:____:____:____
```

### Pasul 2: Identifică Cel Mai Lung Șir de Zerouri

```
Grupuri zero consecutive: de la poziția ___ la poziția ___
Lungime: ___ grupuri
```

### Pasul 3: Înlocuiește cu ::

```
Rezultat final: ________________
```

### Verificare

```bash
python3 src/exercises/ex_5_02_vlsm_ipv6.py ipv6-comprimare \
    "2001:0db8:0000:0000:0000:0000:0000:0001"
```

### Exercițiu Invers

Expandează `fe80::1` la forma completă:

```
fe80::1 = ____:____:____:____:____:____:____:____
```

<details>
<summary>Click pentru soluție</summary>

**Comprimare:**
- Pas 1: 2001:db8:0:0:0:0:0:1
- Pas 2: Grupuri 3-7 sunt zero (5 grupuri consecutive)
- Pas 3: 2001:db8::1

**Expandare fe80::1:**
- fe80:0000:0000:0000:0000:0000:0000:0001

</details>

---

## Exercițiul T6: Diagrama de Adresare

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 20 min | ★★★★☆ | CREATE | VLSM, diagrame rețea |

### Scenariu

Desenează schema de adresare pentru rețeaua următoare:

```
         ┌─────────────┐
         │   Router    │
         │  10.0.0.1   │
         └──────┬──────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───┴───┐   ┌───┴───┐   ┌───┴───┐
│ VLAN10│   │ VLAN20│   │ VLAN30│
│  ???  │   │  ???  │   │  ???  │
│50 host│   │25 host│   │10 host│
└───────┘   └───────┘   └───────┘
```

Rețea de bază: `10.0.0.0/24`

### Cerințe

1. Folosește VLSM pentru eficiență
2. Completează adresele de rețea pentru fiecare VLAN
3. Specifică gateway-ul pentru fiecare VLAN

### Soluție Ta

| VLAN | Gazde | Subrețea | Gateway |
|------|-------|----------|---------|
| 10 | 50 | | |
| 20 | 25 | | |
| 30 | 10 | | |

<details>
<summary>Click pentru soluție</summary>

| VLAN | Gazde | Subrețea | Gateway |
|------|-------|----------|---------|
| 10 | 50 | 10.0.0.0/26 | 10.0.0.1 |
| 20 | 25 | 10.0.0.64/27 | 10.0.0.65 |
| 30 | 10 | 10.0.0.96/28 | 10.0.0.97 |

</details>

---

## ✓ Auto-Evaluare

După completarea exercițiilor, verifică:

| Exercițiu | Completat | Verificat cu Script | Înțeles |
|-----------|-----------|---------------------|---------|
| T1: VLSM | ☐ | ☐ | ☐ |
| T2: AND | ☐ | ☐ | ☐ |
| T3: FLSM | ☐ | ☐ | ☐ |
| T4: Wireshark | ☐ | - | ☐ |
| T5: IPv6 | ☐ | ☐ | ☐ |
| T6: Diagramă | ☐ | ☐ | ☐ |

### Checkpoint Final

Dacă ai completat toate exercițiile, ar trebui să poți:
- Calcula manual prefixul pentru orice număr de gazde
- Aplica operația AND pentru a găsi adresa de rețea
- Comprima și expanda adrese IPv6
- Analiza pachete în Wireshark

---

## Navigare Rapidă

| ← Anterior | Document | Următor → |
|------------|----------|-----------|
| [Exerciții Perechi](exercitii_perechi.md) | **Exerciții Trace** | [Exemple Utilizare](exemple_utilizare.md) |

## Documente Înrudite

- [Rezumat Teoretic](rezumat_teorie.md) — Concepte și formule
- [Peer Instruction](peer_instruction.md) — Întrebări MCQ
- [Exerciții Perechi](exercitii_perechi.md) — Pair programming
- [Fișa de Comenzi](fisa_comenzi.md) — Referință rapidă

---

*Material Trace pentru Laborator Rețele de Calculatoare – ASE București*
