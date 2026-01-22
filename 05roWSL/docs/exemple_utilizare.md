# Exemple de Utilizare – Săptămâna 5

> Scenarii complete pentru utilizarea scripturilor
> Laborator Rețele de Calculatoare – ASE, Informatică Economică

---

## Scenariu 1: Analiza Rețelei Corporative

### Context

Ai primit sarcina să analizezi rețeaua `172.16.0.0/16` a companiei pentru a înțelege capacitatea și structura ei.

### Pas 1: Analiză Generală

```bash
cd /mnt/d/RETELE/SAPT5/05roWSL

python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 172.16.0.0/16
```

**Output:**
```
═══════════════════════════════════════════════════
  Analiză IPv4 CIDR
═══════════════════════════════════════════════════

  Adresa de rețea:        172.16.0.0/16
  Mască de rețea:         255.255.0.0
  Adresa broadcast:       172.16.255.255

  Total adrese:           65536
  Gazde utilizabile:      65534
  Prima gazdă:            172.16.0.1
  Ultima gazdă:           172.16.255.254

  Adresă privată:         Da (RFC 1918)
```

### Pas 2: Analiză Detaliată

```bash
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 172.16.0.0/16 --detaliat
```

Adaugă reprezentarea binară și masca wildcard.

### Pas 3: Export JSON pentru Raport

```bash
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 172.16.0.0/16 --json \
    > raport_retea.json
```

---

## Scenariu 2: Planificare Subrețele cu FLSM

### Context

Trebuie să împarți rețeaua `192.168.0.0/24` în 4 departamente egale.

### Pas 1: Generare Subrețele

```bash
python3 src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.0.0/24 4
```

**Output:**
```
═══════════════════════════════════════════════════
  Subnetare FLSM
═══════════════════════════════════════════════════

  Rețea de bază:          192.168.0.0/24
  Subrețele generate:     4
  Prefix nou:             /26

┌────┬──────────────────────┬─────────────────┬──────────┐
│ #  │ Subrețea             │ Interval Gazde  │ Broadcast│
├────┼──────────────────────┼─────────────────┼──────────┤
│ 1  │ 192.168.0.0/26       │ .1 - .62        │ .63      │
│ 2  │ 192.168.0.64/26      │ .65 - .126      │ .127     │
│ 3  │ 192.168.0.128/26     │ .129 - .190     │ .191     │
│ 4  │ 192.168.0.192/26     │ .193 - .254     │ .255     │
└────┴──────────────────────┴─────────────────┴──────────┘

  Gazde per subrețea:     62
```

### Pas 2: Verificare pentru 8 Subrețele

```bash
python3 src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.0.0/24 8
```

---

## Scenariu 3: Alocare VLSM pentru Departamente

### Context

**TechVision SRL** are următoarele departamente cu cerințe diferite:

| Departament | Gazde Necesare |
|-------------|----------------|
| Development | 120 |
| Sales | 55 |
| Finance | 30 |
| HR | 25 |
| IT | 15 |
| Management | 8 |
| Link Router 1 | 2 |
| Link Router 2 | 2 |

Rețea de bază: `172.20.0.0/22` (1022 gazde)

### Pas 1: Verificare Spațiu Disponibil

```bash
python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 172.20.0.0/22
```

Verifică că ai suficiente gazde: 1022 > 120+55+30+25+15+8+2+2 = 257 ✓

### Pas 2: Alocare VLSM

```bash
python3 src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.20.0.0/22 \
    --cerinte 120,55,30,25,15,8,2,2
```

**Output:**
```
═══════════════════════════════════════════════════
  Alocare VLSM
═══════════════════════════════════════════════════

  Rețea de bază:          172.20.0.0/22 (1022 gazde)

┌──────────┬────────┬────────────────────┬───────────┬───────────┐
│ Cerință  │ Prefix │ Subrețea           │ Disponibil│ Eficiență │
├──────────┼────────┼────────────────────┼───────────┼───────────┤
│ 120      │ /25    │ 172.20.0.0/25      │ 126       │ 95%       │
│ 55       │ /26    │ 172.20.0.128/26    │ 62        │ 89%       │
│ 30       │ /27    │ 172.20.0.192/27    │ 30        │ 100%      │
│ 25       │ /27    │ 172.20.0.224/27    │ 30        │ 83%       │
│ 15       │ /28    │ 172.20.1.0/28      │ 14        │ 107%*     │
│ 8        │ /28    │ 172.20.1.16/28     │ 14        │ 57%       │
│ 2        │ /30    │ 172.20.1.32/30     │ 2         │ 100%      │
│ 2        │ /30    │ 172.20.1.36/30     │ 2         │ 100%      │
└──────────┴────────┴────────────────────┴───────────┴───────────┘

  Total cerut:            257 gazde
  Total alocat:           280 gazde
  Eficiență globală:      92%
  Spațiu rămas:           742 gazde
```

### Pas 3: Export pentru Documentație

```bash
python3 src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.20.0.0/22 \
    --cerinte 120,55,30,25,15,8,2,2 --json > techvision_vlsm.json
```

---

## Scenariu 4: Migrare la IPv6

### Context

Compania primește prefixul IPv6 `2001:db8:cafe::/48` de la ISP.

### Pas 1: Generare Subrețele pentru Departamente

```bash
python3 src/exercises/ex_5_02_vlsm_ipv6.py subretele-ipv6 \
    "2001:db8:cafe::/48" --numar 6
```

**Output:**
```
═══════════════════════════════════════════════════
  Subrețele IPv6
═══════════════════════════════════════════════════

  Prefix de bază:         2001:db8:cafe::/48
  Subrețele generate:     6 (prefix /64)

┌────┬────────────────────────────┬─────────────────────────┐
│ #  │ Subrețea                   │ Prima Adresă Utilizabilă│
├────┼────────────────────────────┼─────────────────────────┤
│ 1  │ 2001:db8:cafe::/64         │ 2001:db8:cafe::1        │
│ 2  │ 2001:db8:cafe:1::/64       │ 2001:db8:cafe:1::1      │
│ 3  │ 2001:db8:cafe:2::/64       │ 2001:db8:cafe:2::1      │
│ 4  │ 2001:db8:cafe:3::/64       │ 2001:db8:cafe:3::1      │
│ 5  │ 2001:db8:cafe:4::/64       │ 2001:db8:cafe:4::1      │
│ 6  │ 2001:db8:cafe:5::/64       │ 2001:db8:cafe:5::1      │
└────┴────────────────────────────┴─────────────────────────┘
```

### Pas 2: Verificare Adrese

```bash
# Comprimare
python3 src/exercises/ex_5_02_vlsm_ipv6.py ipv6-comprimare \
    "2001:0db8:cafe:0001:0000:0000:0000:0001"
# Output: 2001:db8:cafe:1::1

# Expandare
python3 src/exercises/ex_5_02_vlsm_ipv6.py ipv6-expandare \
    "2001:db8:cafe:1::1"
# Output: 2001:0db8:cafe:0001:0000:0000:0000:0001
```

---

## Scenariu 5: Auto-Testare cu Quiz

### Quiz Rapid (5 întrebări, nivel ușor)

```bash
python3 src/exercises/ex_5_03_generator_quiz.py --intrebari 5 --dificultate usor
```

### Quiz Standard (10 întrebări, nivel mediu)

```bash
python3 src/exercises/ex_5_03_generator_quiz.py
```

### Quiz Pregătire Examen (20 întrebări, nivel greu)

```bash
python3 src/exercises/ex_5_03_generator_quiz.py --intrebari 20 --dificultate greu
```

---

## Scenariu 6: Utilizare Programatică

### Script Python Custom

```python
#!/usr/bin/env python3
"""Exemplu de utilizare programatică a bibliotecii net_utils."""

import sys
from pathlib import Path

# Adaugă rădăcina proiectului în path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.net_utils import (
    analizeaza_interfata_ipv4,
    aloca_vlsm,
    comprima_ipv6,
    prefix_pentru_gazde,
)


def exemplu_analiza():
    """Analizează o rețea și afișează informații."""
    info = analizeaza_interfata_ipv4("192.168.1.100/24")
    
    print(f"Rețea: {info.retea}")
    print(f"Broadcast: {info.broadcast}")
    print(f"Gazde disponibile: {info.gazde_utilizabile}")
    print(f"Este privată: {info.este_privata}")


def exemplu_vlsm():
    """Planifică subrețele pentru departamente."""
    departamente = {
        "Development": 50,
        "QA": 20,
        "Production": 100,
        "Management": 10,
    }
    
    cerinte = list(departamente.values())
    alocari = aloca_vlsm("10.0.0.0/24", cerinte)
    
    print("\nPlan VLSM:")
    for alocare, (dept, _) in zip(alocari, departamente.items()):
        print(f"  {dept:15} → {alocare['subretea']} "
              f"({alocare['gazde_disponibile']} gazde)")


def exemplu_prefix():
    """Calculează prefixul necesar pentru diferite cerințe."""
    cerinte = [10, 50, 100, 200, 500]
    
    print("\nPrefix necesar:")
    for c in cerinte:
        p = prefix_pentru_gazde(c)
        disponibil = 2 ** (32 - p) - 2
        print(f"  {c:4} gazde → /{p} ({disponibil} disponibile)")


def exemplu_ipv6():
    """Procesează adrese IPv6."""
    adrese = [
        "2001:0db8:0000:0000:0000:0000:0000:0001",
        "fe80:0000:0000:0000:0000:0000:0000:0001",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    ]
    
    print("\nComprimare IPv6:")
    for adresa in adrese:
        comprimata = comprima_ipv6(adresa)
        print(f"  {adresa}")
        print(f"  → {comprimata}\n")


if __name__ == "__main__":
    exemplu_analiza()
    exemplu_vlsm()
    exemplu_prefix()
    exemplu_ipv6()
```

Salvează ca `exemplu_custom.py` și rulează:

```bash
python3 exemplu_custom.py
```

---

## Scenariu 7: Integrare cu Docker

### Verificare Rețea Docker

```bash
# Inspectează rețeaua laboratorului
docker network inspect week5_labnet | python3 -m json.tool

# Extrage doar IP-urile containerelor
docker network inspect week5_labnet --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}'
```

### Test Conectivitate

```bash
# Ping între containere
docker exec week5_python ping -c 3 10.5.0.20

# Verifică rutele
docker exec week5_python ip route
```

---

## Scenariu 8: Captură și Analiză Trafic

### Pas 1: Pornește Wireshark

Deschide Wireshark și selectează interfața `vEthernet (WSL)`.

### Pas 2: Generează Trafic

```bash
# Terminal 1: Pornește serverul UDP
docker exec -it week5_udp-server python3 /app/udp_server.py

# Terminal 2: Trimite mesaje
docker exec week5_python echo "Test mesaj" | nc -u 10.5.0.20 9999
```

### Pas 3: Oprește Captura

În Wireshark, oprește captura și aplică filtrul:
```
udp.port == 9999
```

### Pas 4: Salvează

Salvează captura în `pcap/udp_demo.pcap`.

---

## Documente Înrudite

- [README Principal](../README.md) — Ghid de pornire
- [Referință API](api_reference.md) — Documentație funcții
- [Fișa de Comenzi](fisa_comenzi.md) — Referință rapidă
- [Depanare](depanare.md) — Rezolvarea problemelor

---

*Exemple de utilizare pentru Laborator Rețele de Calculatoare – ASE București*
