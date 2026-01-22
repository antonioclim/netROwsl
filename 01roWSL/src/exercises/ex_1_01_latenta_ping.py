#!/usr/bin/env python3
"""
Exercițiul 1.01: Măsurarea Latenței cu Ping
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest exercițiu demonstrează măsurarea latenței de rețea folosind ICMP Echo.

Concepte cheie:
- RTT (Round Trip Time) - timpul dus-întors al unui pachet
- Latență - întârzierea în comunicare
- Jitter - variația latenței în timp
- Pierdere pachete - când pachetele nu ajung la destinație
"""

from __future__ import annotations

import subprocess
import sys
import re
import statistics
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS_SI_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("ex_latenta")

# Culori pentru output
VERDE = "\033[92m"
GALBEN = "\033[93m"
ROSU = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


# ═══════════════════════════════════════════════════════════════════════════════
# STRUCTURI_DATE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class RezultatPing:
    """Rezultatul unei sesiuni de ping.
    
    Attributes:
        destinatie: Adresa/hostname țintă
        pachete_trimise: Numărul de pachete ICMP trimise
        pachete_primite: Numărul de răspunsuri primite
        rtt_values: Lista timpilor RTT individuali (ms)
        rtt_min: RTT minim (ms)
        rtt_avg: RTT mediu (ms)
        rtt_max: RTT maxim (ms)
        rtt_mdev: Deviația standard RTT (ms) - măsoară jitter-ul
    """
    destinatie: str
    pachete_trimise: int = 0
    pachete_primite: int = 0
    rtt_values: List[float] = None
    rtt_min: float = 0.0
    rtt_avg: float = 0.0
    rtt_max: float = 0.0
    rtt_mdev: float = 0.0
    
    def __post_init__(self):
        if self.rtt_values is None:
            self.rtt_values = []
    
    @property
    def pierdere_procent(self) -> float:
        """Calculează procentul de pachete pierdute."""
        if self.pachete_trimise == 0:
            return 0.0
        return ((self.pachete_trimise - self.pachete_primite) / self.pachete_trimise) * 100


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTIE_PING
# ═══════════════════════════════════════════════════════════════════════════════

def executa_ping(destinatie: str, numar_pachete: int = 4, timeout: int = 5) -> RezultatPing:
    """Execută ping și parsează rezultatele.
    
    Args:
        destinatie: Adresa IP sau hostname țintă
        numar_pachete: Câte pachete ICMP să trimită
        timeout: Timeout per pachet în secunde
        
    Returns:
        RezultatPing cu datele colectate
    """
    rezultat = RezultatPing(destinatie=destinatie)
    
    try:
        # Rulează ping - formatul e standard Linux
        proces = subprocess.run(
            ["ping", "-c", str(numar_pachete), "-W", str(timeout), destinatie],
            capture_output=True,
            text=True,
            timeout=numar_pachete * timeout + 10
        )
        
        output = proces.stdout + proces.stderr
        
        # Parsează RTT-uri individuale din linii de genul:
        # 64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.034 ms
        pattern_rtt = r"time=(\d+\.?\d*)\s*ms"
        rezultat.rtt_values = [float(m) for m in re.findall(pattern_rtt, output)]
        
        # Parsează statisticile finale:
        # 4 packets transmitted, 4 received, 0% packet loss, time 3062ms
        pattern_stats = r"(\d+)\s+packets transmitted.*?(\d+)\s+received"
        match_stats = re.search(pattern_stats, output)
        if match_stats:
            rezultat.pachete_trimise = int(match_stats.group(1))
            rezultat.pachete_primite = int(match_stats.group(2))
        
        # Parsează RTT min/avg/max/mdev:
        # rtt min/avg/max/mdev = 0.034/0.038/0.041/0.003 ms
        pattern_rtt_stats = r"rtt min/avg/max/mdev\s*=\s*([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)"
        match_rtt = re.search(pattern_rtt_stats, output)
        if match_rtt:
            rezultat.rtt_min = float(match_rtt.group(1))
            rezultat.rtt_avg = float(match_rtt.group(2))
            rezultat.rtt_max = float(match_rtt.group(3))
            rezultat.rtt_mdev = float(match_rtt.group(4))
            
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout la ping către {destinatie}")
    except Exception as e:
        logger.error(f"Eroare la ping: {e}")
    
    return rezultat


# ═══════════════════════════════════════════════════════════════════════════════
# AFISARE_REZULTATE
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_statistici(rezultat: RezultatPing) -> None:
    """Afișează statisticile într-un format vizual.
    
    Interpretează automat rezultatele pentru a ajuta la înțelegere.
    """
    print()
    print(f"{BOLD}{'═' * 60}{RESET}")
    print(f"{BOLD}  REZULTATE PING: {rezultat.destinatie}{RESET}")
    print(f"{BOLD}{'═' * 60}{RESET}")
    print()
    
    # Statistici de bază
    print(f"  Pachete trimise:  {rezultat.pachete_trimise}")
    print(f"  Pachete primite:  {rezultat.pachete_primite}")
    
    # Colorare pierdere în funcție de severitate
    pierdere = rezultat.pierdere_procent
    if pierdere == 0:
        culoare_pierdere = VERDE
        mesaj_pierdere = "Excelent!"
    elif pierdere < 5:
        culoare_pierdere = GALBEN
        mesaj_pierdere = "Acceptabil"
    else:
        culoare_pierdere = ROSU
        mesaj_pierdere = "Problemă de rețea!"
    
    print(f"  Pierdere:         {culoare_pierdere}{pierdere:.1f}%{RESET} ({mesaj_pierdere})")
    print()
    
    # Statistici RTT
    if rezultat.rtt_values:
        print(f"  {CYAN}Statistici RTT (Round Trip Time):{RESET}")
        print(f"  ┌{'─' * 40}┐")
        print(f"  │  Minim:     {rezultat.rtt_min:>10.3f} ms          │")
        print(f"  │  Mediu:     {rezultat.rtt_avg:>10.3f} ms          │")
        print(f"  │  Maxim:     {rezultat.rtt_max:>10.3f} ms          │")
        print(f"  │  Deviație:  {rezultat.rtt_mdev:>10.3f} ms (jitter) │")
        print(f"  └{'─' * 40}┘")
        
        # Interpretare automată a rezultatelor
        print()
        print(f"  {BOLD}Interpretare:{RESET}")
        
        # Interpretare latență
        if rezultat.rtt_avg < 1:
            print(f"  • Latență {VERDE}excelentă{RESET} (<1ms) - probabil loopback sau LAN")
        elif rezultat.rtt_avg < 20:
            print(f"  • Latență {VERDE}foarte bună{RESET} (<20ms) - conexiune locală rapidă")
        elif rezultat.rtt_avg < 100:
            print(f"  • Latență {GALBEN}bună{RESET} (<100ms) - tipică pentru conexiuni regionale")
        else:
            print(f"  • Latență {ROSU}ridicată{RESET} (>100ms) - conexiune la distanță sau congestie")
        
        # Interpretare jitter
        if rezultat.rtt_mdev < 1:
            print(f"  • Jitter {VERDE}excelent{RESET} - conexiune foarte stabilă")
        elif rezultat.rtt_mdev < 10:
            print(f"  • Jitter {GALBEN}acceptabil{RESET} - unele variații normale")
        else:
            print(f"  • Jitter {ROSU}ridicat{RESET} - conexiune instabilă, probleme pentru VoIP/gaming")
    
    print()
    print(f"{'═' * 60}")
    print()


def afiseaza_comparatie(rezultate: List[RezultatPing]) -> None:
    """Afișează o comparație între mai multe destinații.
    
    Util pentru a compara latența către diferite ținte.
    """
    print()
    print(f"{BOLD}{'═' * 70}{RESET}")
    print(f"{BOLD}  COMPARAȚIE LATENȚĂ{RESET}")
    print(f"{BOLD}{'═' * 70}{RESET}")
    print()
    
    # Header tabel
    print(f"  {'Destinație':<20} {'RTT Mediu':>12} {'Pierdere':>10} {'Jitter':>10}")
    print(f"  {'-' * 20} {'-' * 12} {'-' * 10} {'-' * 10}")
    
    # Sortează după RTT mediu
    rezultate_sortate = sorted(rezultate, key=lambda r: r.rtt_avg if r.rtt_avg > 0 else 9999)
    
    for r in rezultate_sortate:
        if r.rtt_avg > 0:
            print(f"  {r.destinatie:<20} {r.rtt_avg:>10.2f}ms {r.pierdere_procent:>9.1f}% {r.rtt_mdev:>8.2f}ms")
        else:
            print(f"  {r.destinatie:<20} {'N/A':>12} {'N/A':>10} {'N/A':>10}")
    
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Funcția principală - rulează demonstrația de ping."""
    print()
    print(f"{BOLD}╔{'═' * 58}╗{RESET}")
    print(f"{BOLD}║  EXERCIȚIUL 1.01: MĂSURAREA LATENȚEI CU PING            ║{RESET}")
    print(f"{BOLD}╚{'═' * 58}╝{RESET}")
    print()
    
    # Lista de destinații de testat
    destinatii = [
        ("127.0.0.1", "Loopback (local)"),
        ("172.20.1.1", "Gateway Docker"),
    ]
    
    rezultate = []
    
    for ip, descriere in destinatii:
        print(f"{CYAN}Se testează: {descriere} ({ip})...{RESET}")
        rezultat = executa_ping(ip, numar_pachete=4)
        rezultate.append(rezultat)
        afiseaza_statistici(rezultat)
    
    # Comparație finală
    if len(rezultate) > 1:
        afiseaza_comparatie(rezultate)
    
    print(f"{VERDE}✓ Exercițiu completat!{RESET}")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
