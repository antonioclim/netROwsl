# Referință API – Modulul net_utils

> Documentație completă pentru funcțiile de rețea din Săptămâna 5
> Laborator Rețele de Calculatoare – ASE, Informatică Economică

---

## Importuri

```python
from src.utils.net_utils import (
    # Analiză IPv4
    analizeaza_interfata_ipv4,
    interval_gazde_ipv4,
    ip_la_binar,
    prefix_la_masca,
    masca_la_prefix,
    
    # Subnetare
    imparte_flsm,
    aloca_vlsm,
    prefix_pentru_gazde,
    
    # IPv6
    comprima_ipv6,
    expandeaza_ipv6,
    genereaza_subretele_ipv6,
    
    # Validare
    valideaza_adresa_ipv4,
    valideaza_cidr_ipv4,
)

from src.utils.constante import (
    BITI_IPV4,
    BITI_IPV6,
    PREFIX_MAX_IPV4,
    ADRESE_REZERVATE_PER_RETEA,
)
```

---

## Structuri de Date

### InfoRetea (dataclass)

Obiect returnat de `analizeaza_interfata_ipv4()`.

```python
@dataclass
class InfoRetea:
    adresa: IPv4Address          # Adresa IP originală
    retea: IPv4Network           # Rețeaua CIDR
    masca: IPv4Address           # Masca de rețea
    wildcard: IPv4Address        # Masca wildcard (inversă)
    broadcast: IPv4Address       # Adresa de broadcast
    total_adrese: int            # Numărul total de adrese
    gazde_utilizabile: int       # Gazde disponibile pentru dispozitive
    prima_gazda: IPv4Address     # Prima adresă utilizabilă (sau None)
    ultima_gazda: IPv4Address    # Ultima adresă utilizabilă (sau None)
    este_privata: bool           # True dacă e adresă RFC 1918
    tip_adresa: str              # "privată", "publică", "loopback", etc.
```

**Exemplu utilizare:**
```python
info = analizeaza_interfata_ipv4("192.168.10.14/26")

print(f"Rețea: {info.retea}")              # 192.168.10.0/26
print(f"Broadcast: {info.broadcast}")       # 192.168.10.63
print(f"Gazde: {info.gazde_utilizabile}")   # 62
print(f"Interval: {info.prima_gazda} - {info.ultima_gazda}")
# Interval: 192.168.10.1 - 192.168.10.62
```

---

## Funcții de Analiză IPv4

### analizeaza_interfata_ipv4

```python
def analizeaza_interfata_ipv4(cidr: str) -> InfoRetea
```

Analizează o adresă IPv4 cu prefix CIDR și returnează toate proprietățile rețelei.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `cidr` | str | Adresă în format CIDR (ex: "192.168.10.14/26") |

**Returnează:** `InfoRetea` — obiect cu toate proprietățile rețelei

**Excepții:**
- `ValueError` — format CIDR invalid sau prefix în afara intervalului [0, 32]

**Exemplu:**
```python
>>> info = analizeaza_interfata_ipv4("10.0.0.1/8")
>>> print(info.total_adrese)
16777216
>>> print(info.este_privata)
True
>>> print(info.tip_adresa)
"privată"
```

---

### interval_gazde_ipv4

```python
def interval_gazde_ipv4(retea: IPv4Network) -> Tuple[IPv4Address, IPv4Address, int]
```

Returnează intervalul de gazde utilizabile pentru o rețea.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `retea` | IPv4Network | Obiect rețea din ipaddress |

**Returnează:** Tuple cu (prima_gazda, ultima_gazda, numar_gazde)

**Exemplu:**
```python
>>> import ipaddress
>>> retea = ipaddress.ip_network("192.168.1.0/24")
>>> prima, ultima, numar = interval_gazde_ipv4(retea)
>>> print(f"{prima} - {ultima} ({numar} gazde)")
192.168.1.1 - 192.168.1.254 (254 gazde)
```

---

### ip_la_binar

```python
def ip_la_binar(ip: str, cu_puncte: bool = False) -> str
```

Convertește o adresă IPv4 la reprezentarea binară.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `ip` | str | Adresă IPv4 în format zecimal cu punct |
| `cu_puncte` | bool | Dacă True, separă octeții cu punct (default: False) |

**Returnează:** String cu reprezentarea binară (32 caractere sau 35 cu puncte)

**Exemplu:**
```python
>>> ip_la_binar("192.168.1.1")
"11000000101010000000000100000001"

>>> ip_la_binar("192.168.1.1", cu_puncte=True)
"11000000.10101000.00000001.00000001"
```

---

### prefix_la_masca

```python
def prefix_la_masca(prefix: int) -> IPv4Address
```

Convertește un prefix CIDR la mască de rețea.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `prefix` | int | Lungimea prefixului (0-32) |

**Returnează:** IPv4Address reprezentând masca

**Excepții:**
- `ValueError` — prefix în afara intervalului [0, 32]

**Exemplu:**
```python
>>> prefix_la_masca(24)
IPv4Address('255.255.255.0')

>>> prefix_la_masca(26)
IPv4Address('255.255.255.192')
```

---

### masca_la_prefix

```python
def masca_la_prefix(masca: str) -> int
```

Convertește o mască de rețea la prefix CIDR.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `masca` | str | Mască în format zecimal cu punct |

**Returnează:** int — lungimea prefixului

**Excepții:**
- `ValueError` — mască invalidă (nu e continuă)

**Exemplu:**
```python
>>> masca_la_prefix("255.255.255.0")
24

>>> masca_la_prefix("255.255.255.192")
26
```

---

## Funcții de Subnetare

### imparte_flsm

```python
def imparte_flsm(baza: str, numar_subretele: int) -> List[IPv4Network]
```

Împarte o rețea în subrețele egale folosind FLSM.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `baza` | str | Rețea de bază în format CIDR |
| `numar_subretele` | int | Număr de subrețele (trebuie putere de 2) |

**Returnează:** Listă de IPv4Network reprezentând subrețelele

**Excepții:**
- `ValueError` — număr nu e putere de 2 sau prefixul rezultat > 32

**Exemplu:**
```python
>>> subretele = imparte_flsm("192.168.100.0/24", 4)
>>> for s in subretele:
...     print(f"{s} ({s.num_addresses - 2} gazde)")
192.168.100.0/26 (62 gazde)
192.168.100.64/26 (62 gazde)
192.168.100.128/26 (62 gazde)
192.168.100.192/26 (62 gazde)
```

---

### aloca_vlsm

```python
def aloca_vlsm(baza: str, cerinte: List[int]) -> List[dict]
```

Alocă subrețele folosind VLSM pentru cerințele date.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `baza` | str | Rețea de bază în format CIDR |
| `cerinte` | List[int] | Listă cu numărul de gazde necesare per subrețea |

**Returnează:** Listă de dicționare cu structura:
```python
{
    'cerinta': int,           # Cerința originală
    'subretea': IPv4Network,  # Subrețeaua alocată
    'gazde_disponibile': int, # Gazde utilizabile
    'eficienta': float        # cerinta / gazde_disponibile
}
```

**Excepții:**
- `ValueError` — spațiu insuficient pentru toate cerințele

**Exemplu:**
```python
>>> alocari = aloca_vlsm("192.168.0.0/24", [60, 20, 10, 2])
>>> for a in alocari:
...     print(f"{a['cerinta']:3d} gazde → {a['subretea']} "
...           f"(eficiență: {a['eficienta']:.0%})")
 60 gazde → 192.168.0.0/26 (eficiență: 97%)
 20 gazde → 192.168.0.64/27 (eficiență: 67%)
 10 gazde → 192.168.0.96/28 (eficiență: 71%)
  2 gazde → 192.168.0.112/30 (eficiență: 100%)
```

---

### prefix_pentru_gazde

```python
def prefix_pentru_gazde(numar_gazde: int) -> int
```

Calculează prefixul minim necesar pentru un număr de gazde.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `numar_gazde` | int | Numărul de gazde necesare |

**Returnează:** int — prefixul CIDR minim

**Exemplu:**
```python
>>> prefix_pentru_gazde(100)
25  # /25 oferă 126 gazde

>>> prefix_pentru_gazde(2)
30  # /30 oferă exact 2 gazde

>>> prefix_pentru_gazde(500)
23  # /23 oferă 510 gazde
```

---

## Funcții IPv6

### comprima_ipv6

```python
def comprima_ipv6(adresa: str) -> str
```

Comprimă o adresă IPv6 la forma canonică scurtă.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `adresa` | str | Adresă IPv6 în orice format valid |

**Returnează:** String cu adresa comprimată

**Excepții:**
- `ValueError` — adresă IPv6 invalidă

**Exemplu:**
```python
>>> comprima_ipv6("2001:0db8:0000:0000:0000:0000:0000:0001")
"2001:db8::1"

>>> comprima_ipv6("0000:0000:0000:0000:0000:0000:0000:0001")
"::1"

>>> comprima_ipv6("fe80:0000:0000:0000:0000:0000:0000:0001")
"fe80::1"
```

---

### expandeaza_ipv6

```python
def expandeaza_ipv6(adresa: str) -> str
```

Expandează o adresă IPv6 la forma completă cu toate zerourile.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `adresa` | str | Adresă IPv6 în orice format valid |

**Returnează:** String cu adresa completă (39 caractere)

**Excepții:**
- `ValueError` — adresă IPv6 invalidă sau două secvențe `::`

**Exemplu:**
```python
>>> expandeaza_ipv6("2001:db8::1")
"2001:0db8:0000:0000:0000:0000:0000:0001"

>>> expandeaza_ipv6("::1")
"0000:0000:0000:0000:0000:0000:0000:0001"
```

---

### genereaza_subretele_ipv6

```python
def genereaza_subretele_ipv6(prefix: str, numar: int) -> List[IPv6Network]
```

Generează subrețele IPv6 dintr-un prefix dat.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `prefix` | str | Prefix IPv6 în format CIDR |
| `numar` | int | Numărul de subrețele de generat |

**Returnează:** Listă de IPv6Network

**Exemplu:**
```python
>>> subretele = genereaza_subretele_ipv6("2001:db8:cafe::/48", 6)
>>> for s in subretele:
...     print(s)
2001:db8:cafe::/64
2001:db8:cafe:1::/64
2001:db8:cafe:2::/64
2001:db8:cafe:3::/64
2001:db8:cafe:4::/64
2001:db8:cafe:5::/64
```

---

## Funcții de Validare

### valideaza_adresa_ipv4

```python
def valideaza_adresa_ipv4(ip: str) -> bool
```

Validează formatul unei adrese IPv4.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `ip` | str | Șirul de validat |

**Returnează:** True dacă formatul este valid

**Excepții:**
- `ValueError` — cu mesaj descriptiv dacă invalid

**Exemplu:**
```python
>>> valideaza_adresa_ipv4("192.168.1.1")
True

>>> valideaza_adresa_ipv4("256.1.1.1")
ValueError: Octetul 1 (256) depășește intervalul valid [0-255]
```

---

### valideaza_cidr_ipv4

```python
def valideaza_cidr_ipv4(cidr: str) -> bool
```

Validează formatul notației CIDR IPv4.

**Parametri:**
| Parametru | Tip | Descriere |
|-----------|-----|-----------|
| `cidr` | str | Șirul de validat (ex: "192.168.1.0/24") |

**Returnează:** True dacă formatul este valid

**Excepții:**
- `ValueError` — cu mesaj descriptiv dacă invalid

**Exemplu:**
```python
>>> valideaza_cidr_ipv4("192.168.1.0/24")
True

>>> valideaza_cidr_ipv4("192.168.1.0/33")
ValueError: Prefixul 33 depășește intervalul valid [0-32]
```

---

## Alias-uri pentru Compatibilitate

Toate funcțiile au alias-uri în limba engleză pentru compatibilitate:

| Funcție Română | Alias Engleză |
|----------------|---------------|
| `analizeaza_interfata_ipv4` | `analyze_ipv4_interface` |
| `interval_gazde_ipv4` | `ipv4_host_range` |
| `ip_la_binar` | `ip_to_binary` |
| `prefix_la_masca` | `prefix_to_mask` |
| `masca_la_prefix` | `mask_to_prefix` |
| `imparte_flsm` | `flsm_split` |
| `aloca_vlsm` | `vlsm_allocate` |
| `prefix_pentru_gazde` | `prefix_for_hosts` |
| `comprima_ipv6` | `compress_ipv6` |
| `expandeaza_ipv6` | `expand_ipv6` |

---

## Documente Înrudite

- [README Principal](../README.md) — Ghid de pornire rapidă
- [Arhitectura Cod](arhitectura.md) — Structura modulelor
- [Exemple Utilizare](exemple_utilizare.md) — Scenarii complete
- [Rezumat Teoretic](rezumat_teorie.md) — Concepte de bază

---

*Documentație API pentru Laborator Rețele de Calculatoare – ASE București*
