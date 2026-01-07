#!/usr/bin/env python3
"""
Tema 1.1: Raport de Configurare a Rețelei
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script colectează informații despre configurația de rețea
și generează un șablon pentru raportul de analiză.
"""

from __future__ import annotations

import subprocess
import sys
import socket
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional


def ruleaza_comanda(comanda: str) -> str:
    """Rulează o comandă și returnează rezultatul.
    
    Args:
        comanda: Comanda de executat
        
    Returns:
        Rezultatul comenzii sau mesaj de eroare
    """
    try:
        rezultat = subprocess.run(
            comanda,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return rezultat.stdout.strip() if rezultat.returncode == 0 else f"Eroare: {rezultat.stderr}"
    except subprocess.TimeoutExpired:
        return "Eroare: Timeout expirat"
    except Exception as e:
        return f"Eroare: {e}"


def obtine_interfete() -> str:
    """Obține lista interfețelor de rețea."""
    return ruleaza_comanda("ip -br addr show")


def obtine_interfete_detaliat() -> str:
    """Obține informații detaliate despre interfețe."""
    return ruleaza_comanda("ip addr show")


def obtine_tabela_rutare() -> str:
    """Obține tabela de rutare."""
    return ruleaza_comanda("ip route show")


def obtine_conexiuni_active() -> str:
    """Obține conexiunile active."""
    return ruleaza_comanda("ss -tunap")


def obtine_dns() -> str:
    """Obține configurația DNS."""
    try:
        with open("/etc/resolv.conf", "r") as f:
            return f.read().strip()
    except Exception as e:
        return f"Nu s-a putut citi: {e}"


def obtine_hostname() -> str:
    """Obține informații despre hostname."""
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except Exception:
        ip = "N/A"
    return f"Hostname: {hostname}\nIP local: {ip}"


def genereaza_raport(cale_iesire: Path) -> None:
    """Generează raportul în format Markdown.
    
    Args:
        cale_iesire: Calea fișierului de ieșire
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    continut = f"""# Raport de Configurare a Rețelei

> Generat: {timestamp}
> Curs REȚELE DE CALCULATOARE - ASE, Informatică

---

## 1. Informații Generale

```
{obtine_hostname()}
```

---

## 2. Interfețe de Rețea

### 2.1 Rezumat Interfețe

```
{obtine_interfete()}
```

### 2.2 Detalii Complete

```
{obtine_interfete_detaliat()}
```

### TODO: Analiza Interfețelor

Răspundeți la următoarele întrebări:

1. **Câte interfețe de rețea aveți active?**
   
   [Răspunsul dvs. aici]

2. **Care este adresa IP a interfeței principale?**
   
   [Răspunsul dvs. aici]

3. **Ce tip de adrese aveți? (IPv4, IPv6, ambele)**
   
   [Răspunsul dvs. aici]

4. **Care este adresa MAC a interfeței principale?**
   
   [Răspunsul dvs. aici]

---

## 3. Tabela de Rutare

```
{obtine_tabela_rutare()}
```

### TODO: Analiza Rutelor

1. **Care este gateway-ul implicit (default)?**
   
   [Răspunsul dvs. aici]

2. **Pe ce interfață este configurat gateway-ul implicit?**
   
   [Răspunsul dvs. aici]

3. **Explicați ce înseamnă fiecare linie din tabela de rutare:**
   
   [Explicația dvs. aici]

---

## 4. Conexiuni Active

```
{obtine_conexiuni_active()}
```

### TODO: Analiza Conexiunilor

1. **Câte socket-uri sunt în starea LISTEN?**
   
   [Răspunsul dvs. aici]

2. **Ce servicii ascultă pe porturile de sub 1024?**
   
   [Răspunsul dvs. aici]

3. **Există conexiuni ESTABLISHED? Către ce adrese?**
   
   [Răspunsul dvs. aici]

---

## 5. Configurația DNS

```
{obtine_dns()}
```

### TODO: Analiza DNS

1. **Ce servere DNS sunt configurate?**
   
   [Răspunsul dvs. aici]

2. **Sunt acestea servere publice sau private?**
   
   [Răspunsul dvs. aici]

---

## 6. Observații Interesante

### TODO: Completați această secțiune

Descrieți cel puțin 3 observații interesante despre configurația voastră de rețea:

1. [Observația 1]

2. [Observația 2]

3. [Observația 3]

---

## 7. Concluzii

### TODO: Scrieți concluziile

Rezumați în 3-5 propoziții ce ați învățat din analiza configurației de rețea:

[Concluziile dvs. aici]

---

*Raport generat cu tema_1_01_raport_retea.py*
*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
"""

    with open(cale_iesire, "w", encoding="utf-8") as f:
        f.write(continut)
    
    print(f"✓ Raport generat: {cale_iesire}")
    print()
    print("Pași următori:")
    print("1. Deschideți fișierul într-un editor de text")
    print("2. Completați secțiunile marcate cu TODO")
    print("3. Salvați și predați raportul")


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Generează raport de configurare a rețelei",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python tema_1_01_raport_retea.py
  python tema_1_01_raport_retea.py --output raportul_meu.md
        """
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("raport_retea.md"),
        help="Calea fișierului de ieșire (implicit: raport_retea.md)"
    )
    args = parser.parse_args()

    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  TEMA 1.1: RAPORT CONFIGURARE REȚEA".center(58) + "║")
    print("║" + "  Curs REȚELE DE CALCULATOARE - ASE, Informatică".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    try:
        genereaza_raport(args.output)
        return 0
    except Exception as e:
        print(f"Eroare: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
