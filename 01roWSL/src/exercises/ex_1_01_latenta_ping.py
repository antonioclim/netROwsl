#!/usr/bin/env python3
"""
Exercițiul 1.01: Măsurarea Latenței cu Ping
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest exercițiu demonstrează măsurarea latenței rețelei folosind ICMP Echo Request/Reply.
Veți învăța despre RTT (Round Trip Time) și variabilitatea latenței.

Concepte cheie:
- ICMP (Internet Control Message Protocol)
- RTT (Round Trip Time) - timpul dus-întors
- Latență și jitter (variația latenței)
- Pierdere de pachete

Rulare:
    python ex_1_01_latenta_ping.py
    python ex_1_01_latenta_ping.py --gazda 8.8.8.8 --numar 10
"""

from __future__ import annotations

import subprocess
import sys
import time
import argparse
import statistics
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RezultatPing:
    """Stochează rezultatul unui singur ping."""
    secventa: int
    rtt_ms: Optional[float]
    reusit: bool
    mesaj: str = ""


@dataclass
class StatisticiPing:
    """Statistici agregate pentru o sesiune de ping."""
    gazda: str
    total_trimise: int
    total_primite: int
    pierdere_procent: float
    rtt_min: Optional[float]
    rtt_medie: Optional[float]
    rtt_max: Optional[float]
    rtt_stddev: Optional[float]


def parseaza_linie_ping(linie: str, secventa: int) -> RezultatPing:
    """Parsează o linie de ieșire ping pentru a extrage RTT.
    
    Args:
        linie: Linia de ieșire de la comanda ping
        secventa: Numărul de secvență al pachetului
        
    Returns:
        Obiect RezultatPing cu datele extrase
    """
    if "time=" in linie:
        try:
            parti = linie.split("time=")
            rtt_str = parti[1].split()[0].replace("ms", "")
            rtt = float(rtt_str)
            return RezultatPing(
                secventa=secventa,
                rtt_ms=rtt,
                reusit=True,
                mesaj="Răspuns primit"
            )
        except (IndexError, ValueError):
            pass
    
    if "Destination Host Unreachable" in linie:
        return RezultatPing(
            secventa=secventa,
            rtt_ms=None,
            reusit=False,
            mesaj="Gazdă inaccesibilă"
        )
    
    if "Request timeout" in linie or "no answer" in linie:
        return RezultatPing(
            secventa=secventa,
            rtt_ms=None,
            reusit=False,
            mesaj="Timeout"
        )
    
    return RezultatPing(
        secventa=secventa,
        rtt_ms=None,
        reusit=False,
        mesaj="Răspuns necunoscut"
    )


def executa_ping(gazda: str, numar: int = 5, timeout: int = 5) -> List[RezultatPing]:
    """Execută ping către o gazdă și colectează rezultatele.
    
    Args:
        gazda: Adresa IP sau hostname-ul țintă
        numar: Numărul de pachete de trimis
        timeout: Timeout per pachet în secunde
        
    Returns:
        Lista de rezultate pentru fiecare pachet
    """
    rezultate = []
    
    print(f"\nSe trimite ping către {gazda}...")
    print("-" * 50)
    
    for i in range(numar):
        secventa = i + 1
        try:
            timp_start = time.time()
            proc = subprocess.run(
                ["ping", "-c", "1", "-W", str(timeout), gazda],
                capture_output=True,
                text=True,
                timeout=timeout + 2
            )
            timp_total = (time.time() - timp_start) * 1000
            
            if proc.returncode == 0:
                # Caută linia cu time=
                for linie in proc.stdout.split("\n"):
                    if "time=" in linie:
                        rez = parseaza_linie_ping(linie, secventa)
                        break
                else:
                    rez = RezultatPing(
                        secventa=secventa,
                        rtt_ms=timp_total,
                        reusit=True,
                        mesaj="Răspuns primit"
                    )
            else:
                rez = RezultatPing(
                    secventa=secventa,
                    rtt_ms=None,
                    reusit=False,
                    mesaj="Fără răspuns"
                )
                
        except subprocess.TimeoutExpired:
            rez = RezultatPing(
                secventa=secventa,
                rtt_ms=None,
                reusit=False,
                mesaj="Timeout expirat"
            )
        except Exception as e:
            rez = RezultatPing(
                secventa=secventa,
                rtt_ms=None,
                reusit=False,
                mesaj=str(e)
            )
        
        # Afișează rezultatul
        if rez.reusit and rez.rtt_ms:
            print(f"  Pachet {secventa:3d}: RTT = {rez.rtt_ms:7.2f} ms ✓")
        else:
            print(f"  Pachet {secventa:3d}: {rez.mesaj} ✗")
        
        rezultate.append(rez)
        
        # Pauză scurtă între pachete
        if i < numar - 1:
            time.sleep(0.2)
    
    return rezultate


def calculeaza_statistici(gazda: str, rezultate: List[RezultatPing]) -> StatisticiPing:
    """Calculează statistici din rezultatele ping.
    
    Args:
        gazda: Gazda testată
        rezultate: Lista de rezultate individuale
        
    Returns:
        Obiect StatisticiPing cu statisticile calculate
    """
    total = len(rezultate)
    primite = sum(1 for r in rezultate if r.reusit)
    pierdere = ((total - primite) / total) * 100 if total > 0 else 100.0
    
    # Extrage RTT-urile valide
    rtt_uri = [r.rtt_ms for r in rezultate if r.reusit and r.rtt_ms is not None]
    
    if rtt_uri:
        return StatisticiPing(
            gazda=gazda,
            total_trimise=total,
            total_primite=primite,
            pierdere_procent=pierdere,
            rtt_min=min(rtt_uri),
            rtt_medie=statistics.mean(rtt_uri),
            rtt_max=max(rtt_uri),
            rtt_stddev=statistics.stdev(rtt_uri) if len(rtt_uri) > 1 else 0.0
        )
    else:
        return StatisticiPing(
            gazda=gazda,
            total_trimise=total,
            total_primite=primite,
            pierdere_procent=pierdere,
            rtt_min=None,
            rtt_medie=None,
            rtt_max=None,
            rtt_stddev=None
        )


def afiseaza_statistici(stats: StatisticiPing) -> None:
    """Afișează statisticile într-un format citibil.
    
    Args:
        stats: Statisticile de afișat
    """
    print("\n" + "=" * 50)
    print(f"STATISTICI PING PENTRU {stats.gazda}")
    print("=" * 50)
    
    print(f"\nPachete:")
    print(f"  • Trimise:   {stats.total_trimise}")
    print(f"  • Primite:   {stats.total_primite}")
    print(f"  • Pierdere:  {stats.pierdere_procent:.1f}%")
    
    if stats.rtt_medie is not None:
        print(f"\nTimpi de răspuns (RTT):")
        print(f"  • Minim:     {stats.rtt_min:.2f} ms")
        print(f"  • Mediu:     {stats.rtt_medie:.2f} ms")
        print(f"  • Maxim:     {stats.rtt_max:.2f} ms")
        print(f"  • Deviație:  {stats.rtt_stddev:.2f} ms")
        
        # Interpretare
        print(f"\nInterpretare:")
        if stats.rtt_medie < 1:
            print("  → Latență excelentă (conexiune locală)")
        elif stats.rtt_medie < 20:
            print("  → Latență foarte bună (rețea locală)")
        elif stats.rtt_medie < 50:
            print("  → Latență bună (regional)")
        elif stats.rtt_medie < 100:
            print("  → Latență acceptabilă (continental)")
        else:
            print("  → Latență ridicată (intercontinental sau congestie)")
        
        if stats.rtt_stddev and stats.rtt_stddev > stats.rtt_medie * 0.2:
            print("  → Jitter ridicat (variabilitate în latență)")
    else:
        print("\n⚠ Nu s-au primit răspunsuri - nu se pot calcula statisticile RTT")
    
    if stats.pierdere_procent > 0:
        print(f"\n⚠ Pierdere de pachete detectată ({stats.pierdere_procent:.1f}%)")
        if stats.pierdere_procent > 5:
            print("  → Posibilă congestie sau probleme de rețea")
    
    print("=" * 50)


def main() -> int:
    """Funcția principală a programului."""
    parser = argparse.ArgumentParser(
        description="Măsurarea Latenței cu Ping",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python ex_1_01_latenta_ping.py                    # Ping localhost
  python ex_1_01_latenta_ping.py --gazda 8.8.8.8   # Ping Google DNS
  python ex_1_01_latenta_ping.py --numar 20        # 20 de pachete
        """
    )
    parser.add_argument(
        "--gazda", "-g",
        default="127.0.0.1",
        help="Adresa IP sau hostname de testat (implicit: 127.0.0.1)"
    )
    parser.add_argument(
        "--numar", "-n",
        type=int,
        default=5,
        help="Numărul de pachete de trimis (implicit: 5)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=5,
        help="Timeout per pachet în secunde (implicit: 5)"
    )
    args = parser.parse_args()

    print()
    print("╔" + "═" * 48 + "╗")
    print("║" + "  EXERCIȚIUL 1.01: MĂSURAREA LATENȚEI CU PING".center(48) + "║")
    print("║" + "  Curs REȚELE DE CALCULATOARE - ASE".center(48) + "║")
    print("╚" + "═" * 48 + "╝")

    try:
        # Execută ping
        rezultate = executa_ping(args.gazda, args.numar, args.timeout)
        
        # Calculează și afișează statistici
        stats = calculeaza_statistici(args.gazda, rezultate)
        afiseaza_statistici(stats)
        
        return 0 if stats.total_primite > 0 else 1

    except KeyboardInterrupt:
        print("\n\n⚠ Întrerupt de utilizator")
        return 130
    except Exception as e:
        print(f"\n✗ Eroare: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
