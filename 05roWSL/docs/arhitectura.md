# Arhitectura Codului – Săptămâna 5

> Documentație tehnică pentru structura și design-ul modulelor
> Laborator Rețele de Calculatoare – ASE, Informatică Economică

---

## Structura Modulelor

```
05roWSL/
│
├── src/                              # ═══ COD SURSĂ PRINCIPAL ═══
│   │
│   ├── utils/                        # Biblioteci reutilizabile
│   │   ├── __init__.py
│   │   ├── net_utils.py              # ⭐ Biblioteca principală de rețea
│   │   └── constante.py              # Constante globale
│   │
│   ├── exercises/                    # Exerciții interactive CLI
│   │   ├── ex_5_01_cidr_flsm.py      # Analiză CIDR + FLSM
│   │   ├── ex_5_02_vlsm_ipv6.py      # VLSM + operații IPv6
│   │   └── ex_5_03_generator_quiz.py # Quiz interactiv
│   │
│   └── apps/                         # Aplicații standalone
│       ├── calculator_subretea.py    # Calculator subrețea GUI/CLI
│       └── udp_echo.py               # Server/Client UDP Echo
│
├── scripts/                          # ═══ AUTOMATIZARE ═══
│   │
│   ├── utils/                        # Utilitare pentru scripturi
│   │   ├── __init__.py
│   │   ├── utilitare_docker.py       # Manager Docker Compose
│   │   ├── utilitare_retea.py        # Verificări rețea
│   │   └── logger.py                 # Configurare logging
│   │
│   ├── porneste_laborator.py         # Entry point principal
│   ├── opreste_laborator.py          # Cleanup resurse
│   └── ruleaza_demo.py               # Demonstrații
│
├── tests/                            # ═══ TESTE AUTOMATIZATE ═══
│   ├── test_exercitii.py             # Teste funcționale
│   ├── test_utilitare.py             # Teste module utils
│   └── test_smoke.py                 # Smoke tests rapide
│
├── docs/                             # ═══ DOCUMENTAȚIE ═══
│   ├── api_reference.md              # Referință API
│   ├── arhitectura.md                # Acest fișier
│   ├── depanare.md                   # Troubleshooting
│   ├── exemple_utilizare.md          # Scenarii complete
│   ├── exercitii_perechi.md          # Pair programming
│   ├── exercitii_trace.md            # Exerciții non-coding
│   ├── fisa_comenzi.md               # Cheatsheet comenzi
│   ├── peer_instruction.md           # MCQ pentru seminarii
│   └── rezumat_teorie.md             # Teorie condensată
│
├── homework/                         # ═══ TEME ═══
│   └── exercises/
│       ├── tema1_retea_corporativa.md
│       ├── tema2_migrare_ipv6.md
│       └── tema3_design_startup.md
│
├── docker/                           # ═══ CONTAINERE ═══
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── configs/
│
├── pcap/                             # ═══ CAPTURI REȚEA ═══
│   └── udp_echo_sample.pcap
│
├── setup/                            # ═══ CONFIGURARE ═══
│   ├── verifica_mediu.py
│   ├── instaleaza_cerinte.py
│   └── requirements.txt
│
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```

---

## Diagrama Dependențelor

```
                         ┌──────────────────────┐
                         │   CLI Applications   │
                         │  ┌────────────────┐  │
                         │  │ ex_5_01.py     │  │
                         │  │ ex_5_02.py     │  │
                         │  │ ex_5_03.py     │  │
                         │  └───────┬────────┘  │
                         └──────────┼──────────┘
                                    │ importă
                                    ▼
┌──────────────────────────────────────────────────────────────┐
│                       net_utils.py                            │
│                    (Biblioteca Centrală)                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │ Analiză IPv4    │  │  Subnetare      │  │    IPv6      │  │
│  │                 │  │                 │  │              │  │
│  │ • analizeaza_*  │  │ • imparte_flsm  │  │ • comprima_  │  │
│  │ • interval_*    │  │ • aloca_vlsm    │  │ • expandeaza_│  │
│  │ • ip_la_binar   │  │ • prefix_pentru │  │ • genereaza_ │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐                    │
│  │   Validare      │  │   Conversie     │                    │
│  │                 │  │                 │                    │
│  │ • valideaza_*   │  │ • prefix_la_*   │                    │
│  │                 │  │ • masca_la_*    │                    │
│  └─────────────────┘  └─────────────────┘                    │
└──────────────────────────────────────────────────────────────┘
                                    │ folosește
                                    ▼
                    ┌───────────────────────────┐
                    │   constante.py            │
                    │                           │
                    │ • BITI_IPV4 = 32          │
                    │ • BITI_IPV6 = 128         │
                    │ • PREFIX_MAX_IPV4 = 32    │
                    │ • ADRESE_REZERVATE = 2    │
                    └───────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │      ipaddress            │
                    │   (Python stdlib)         │
                    │                           │
                    │ • IPv4Address             │
                    │ • IPv4Network             │
                    │ • IPv6Address             │
                    │ • IPv6Network             │
                    └───────────────────────────┘
```

---

## Fluxul de Date

### Exercițiul 1: Analiză CIDR

```
┌───────────────┐     ┌──────────────────┐     ┌───────────────┐
│    INPUT      │     │    PROCESARE     │     │    OUTPUT     │
│               │     │                  │     │               │
│ CLI argument  │────▶│ valideaza_cidr() │────▶│  InfoRetea    │
│               │     │        │         │     │  dataclass    │
│ "192.168.10.  │     │        ▼         │     │               │
│  14/26"       │     │ analizeaza_      │     │ • retea       │
│               │     │ interfata_ipv4() │     │ • broadcast   │
└───────────────┘     │        │         │     │ • gazde       │
                      │        ▼         │     │ • interval    │
                      │ interval_gazde() │     │               │
                      └──────────────────┘     └───────┬───────┘
                                                       │
                                               ┌───────▼───────┐
                                               │   Formatare   │
                                               │               │
                                               │ • Text (CLI)  │
                                               │ • JSON        │
                                               │ • Tabel       │
                                               └───────────────┘
```

### Exercițiul 2: Alocare VLSM

```
┌───────────────┐     ┌──────────────────────────────────────┐
│    INPUT      │     │           ALGORITM VLSM              │
│               │     │                                      │
│ baza: str     │     │  1. sortează cerințe descrescător    │
│ cerinte: list │────▶│  2. pentru fiecare cerință:          │
│               │     │     a. calculează prefix_pentru_gazde│
│ "172.16.0.0/  │     │     b. găsește prima subrețea liberă │
│  16"          │     │     c. alocă și marchează            │
│ [500,120,60]  │     │  3. returnează lista de alocări      │
└───────────────┘     └──────────────────┬───────────────────┘
                                         │
                      ┌──────────────────▼───────────────────┐
                      │              OUTPUT                   │
                      │                                       │
                      │  List[dict] cu:                       │
                      │  • cerinta: int                       │
                      │  • subretea: IPv4Network              │
                      │  • gazde_disponibile: int             │
                      │  • eficienta: float                   │
                      └───────────────────────────────────────┘
```

---

## Convenții de Cod

### Naming

| Element | Convenție | Exemplu |
|---------|-----------|---------|
| Funcții (RO) | snake_case | `analizeaza_interfata_ipv4()` |
| Alias (EN) | snake_case | `analyze_ipv4_interface` |
| Clase | PascalCase | `InfoRetea`, `ManagerDocker` |
| Constante | SCREAMING_SNAKE | `BITI_IPV4`, `PREFIX_MAX_IPV4` |
| Fișiere | snake_case | `net_utils.py`, `ex_5_01_cidr_flsm.py` |
| Variabile | snake_case | `numar_gazde`, `prefix_nou` |

### Docstrings

Format standard pentru toate funcțiile publice:

```python
def functie_exemplu(parametru1: str, parametru2: int = 10) -> bool:
    """
    Descriere scurtă pe o singură linie.
    
    Descriere extinsă dacă e necesar, explicând contextul,
    algoritmul sau detalii importante de implementare.
    
    Args:
        parametru1: Ce reprezintă primul parametru
        parametru2: Ce reprezintă al doilea parametru (default: 10)
    
    Returns:
        Ce returnează funcția și în ce condiții
    
    Raises:
        ValueError: Când se aruncă această excepție
        TypeError: Altă excepție posibilă
    
    Example:
        >>> functie_exemplu("test", 5)
        True
        >>> functie_exemplu("invalid")
        False
    """
    ...
```

### Subgoal Labels

Secțiunile majore sunt marcate cu comentarii vizuale:

```python
# ═══════════════════════════════════════════════════════════════════════════════
# Funcții de Analiză IPv4
# ═══════════════════════════════════════════════════════════════════════════════

def analizeaza_interfata_ipv4(...):
    ...

# ═══════════════════════════════════════════════════════════════════════════════
# Funcții de Subnetare FLSM
# ═══════════════════════════════════════════════════════════════════════════════

def imparte_flsm(...):
    ...
```

### Type Hints

Toate funcțiile publice au type hints complete:

```python
from typing import List, Dict, Tuple, Optional, Union
from ipaddress import IPv4Address, IPv4Network, IPv6Network

def aloca_vlsm(
    baza: str, 
    cerinte: List[int]
) -> List[Dict[str, Union[int, IPv4Network, float]]]:
    ...
```

---

## Arhitectura Testelor

```
tests/
├── test_exercitii.py      # Teste funcționale pentru exerciții
│   ├── TesteAnalizaCIDR   # Teste analiză IPv4
│   ├── TesteFLSM          # Teste subnetare FLSM
│   ├── TesteVLSM          # Teste alocare VLSM
│   ├── TesteIPv6          # Teste operații IPv6
│   ├── TesteEdgeCases     # Cazuri limită
│   ├── TestePerformanta   # Volume mari
│   └── TesteIntegrare     # Workflow-uri complete
│
├── test_utilitare.py      # Teste module utilitare
│   ├── TesteLogger
│   ├── TesteDockerManager
│   └── TesteVerificariDocker
│
└── test_smoke.py          # Smoke tests rapide
    └── TestSmoke
        ├── test_import_net_utils
        ├── test_import_exercises
        └── test_docker_available
```

### Rulare Teste

```bash
# Toate testele
python -m pytest tests/ -v

# Doar un fișier
python -m pytest tests/test_exercitii.py -v

# Doar o clasă
python -m pytest tests/test_exercitii.py::TesteVLSM -v

# Doar un test
python -m pytest tests/test_exercitii.py::TesteVLSM::test_vlsm_cerinte_variate -v

# Cu coverage
python -m pytest tests/ --cov=src --cov-report=html
```

---

## Managementul Configurației

### Fișierul constante.py

Centralizează toate valorile magice:

```python
# IPv4
BITI_IPV4 = 32
BITI_OCTET = 8
PREFIX_MIN_IPV4 = 0
PREFIX_MAX_IPV4 = 32
ADRESE_REZERVATE_PER_RETEA = 2  # Rețea + Broadcast

# IPv6
BITI_IPV6 = 128
BITI_HEXTET = 16
PREFIX_MIN_IPV6 = 0
PREFIX_MAX_IPV6 = 128

# Timeout-uri
TIMEOUT_DOCKER_INFO = 10
TIMEOUT_DOCKER_COMPOSE = 60

# Laborator
LAB_NETWORK_NAME = "week5_labnet"
LAB_NETWORK_SUBNET = "10.5.0.0/24"
```

### Configurație Docker

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  python:
    container_name: week5_python
    networks:
      labnet:
        ipv4_address: 10.5.0.10
    cap_add:
      - NET_ADMIN
      - NET_RAW

networks:
  labnet:
    driver: bridge
    ipam:
      config:
        - subnet: 10.5.0.0/24
          gateway: 10.5.0.1
```

---

## Pattern-uri de Design

### 1. Factory pentru InfoRetea

```python
def analizeaza_interfata_ipv4(cidr: str) -> InfoRetea:
    """Factory care construiește obiectul InfoRetea complet."""
    valideaza_cidr_ipv4(cidr)
    
    interfata = ipaddress.ip_interface(cidr)
    retea = interfata.network
    
    return InfoRetea(
        adresa=interfata.ip,
        retea=retea,
        masca=retea.netmask,
        # ... restul câmpurilor
    )
```

### 2. Strategy pentru Output

```python
def formateaza_rezultat(info: InfoRetea, format: str) -> str:
    """Selectează strategia de formatare."""
    if format == "json":
        return _formateaza_json(info)
    elif format == "tabel":
        return _formateaza_tabel(info)
    else:
        return _formateaza_text(info)
```

### 3. Validare Defensivă

```python
def aloca_vlsm(baza: str, cerinte: List[int]) -> List[dict]:
    # Validare input
    valideaza_cidr_ipv4(baza)
    
    if not cerinte:
        raise ValueError("Lista de cerințe nu poate fi goală")
    
    if any(c < 0 for c in cerinte):
        raise ValueError("Cerințele nu pot fi negative")
    
    # Verificare spațiu suficient
    retea = ipaddress.ip_network(baza, strict=False)
    total_necesar = sum(2 ** (32 - prefix_pentru_gazde(c)) for c in cerinte)
    
    if total_necesar > retea.num_addresses:
        raise ValueError(f"Spațiu insuficient: {total_necesar} > {retea.num_addresses}")
    
    # Implementare algoritm
    ...
```

---

## Documente Înrudite

- [README Principal](../README.md) — Ghid de pornire rapidă
- [Referință API](api_reference.md) — Documentație funcții
- [Exemple Utilizare](exemple_utilizare.md) — Scenarii practice
- [CONTRIBUTING](../CONTRIBUTING.md) — Ghid contribuții

---

*Documentație arhitectură pentru Laborator Rețele de Calculatoare – ASE București*
