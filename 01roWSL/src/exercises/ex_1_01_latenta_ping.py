#!/usr/bin/env python3
"""
Exercițiul 1.01: Măsurarea Latenței cu Ping
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest exercițiu demonstrează măsurarea latenței de rețea folosind ICMP Echo.

Concepte cheie:
- RTT (Round Trip Time) — timpul dus-întors al unui pachet
- Latență — întârzierea în comunicare
- Jitter — variația latenței în timp
- Pierdere pachete — când pachetele nu ajung la destinație

Nivel Bloom: APPLY, ANALYSE
Durată: 15 minute
"""

from __future__ import annotations

import subprocess
import sys
import re
from dataclasses import dataclass, field
from typing import List, Tuple
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS_SI_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("ex_latenta")


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PRAGURI
# ═══════════════════════════════════════════════════════════════════════════════

# Praguri de latență (ms) — bazate pe recomandări ITU-T G.114 pentru VoIP
LATENTA_EXCELENTA_MS: float = 1.0       # Loopback sau LAN direct
LATENTA_FOARTE_BUNA_MS: float = 20.0    # LAN sau conexiune locală
LATENTA_BUNA_MS: float = 100.0          # Conexiuni regionale
LATENTA_ACCEPTABILA_MS: float = 300.0   # Limita pentru VoIP interactiv

# Praguri de jitter (ms) — variația RTT
JITTER_EXCELENT_MS: float = 1.0         # Conexiune foarte stabilă
JITTER_ACCEPTABIL_MS: float = 10.0      # Acceptabil pentru majoritatea aplicațiilor
JITTER_PROBLEMATIC_MS: float = 30.0     # Probleme pentru VoIP/gaming

# Praguri de pierdere pachete (%)
PIERDERE_EXCELENTA: float = 0.0
PIERDERE_ACCEPTABILA: float = 5.0
PIERDERE_PROBLEMATICA: float = 10.0

# Limite pentru validare
MIN_PACHETE: int = 1
MAX_PACHETE: int = 100
DEFAULT_PACHETE: int = 4
DEFAULT_TIMEOUT_SEC: int = 5


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

# Culori ANSI pentru output
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
        rtt_mdev: Deviația standard RTT (ms) — măsoară jitter-ul
    """
    destinatie: str
    pachete_trimise: int = 0
    pachete_primite: int = 0
    rtt_values: List[float] = field(default_factory=list)
    rtt_min: float = 0.0
    rtt_avg: float = 0.0
    rtt_max: float = 0.0
    rtt_mdev: float = 0.0
    
    @property
    def pierdere_procent(self) -> float:
        """Calculează procentul de pachete pierdute."""
        if self.pachete_trimise == 0:
            return 0.0
        return ((self.pachete_trimise - self.pachete_primite) / self.pachete_trimise) * 100


# ═══════════════════════════════════════════════════════════════════════════════
# INTERPRETARE_REZULTATE
# ═══════════════════════════════════════════════════════════════════════════════

def interpreteaza_latenta(rtt_avg: float) -> Tuple[str, str]:
    """Interpretează valoarea RTT mediu.
    
    Args:
        rtt_avg: RTT mediu în milisecunde
        
    Returns:
        Tuple (cod_culoare, mesaj_explicativ)
    """
    if rtt_avg < LATENTA_EXCELENTA_MS:
        return (VERDE, f"excelentă (<{LATENTA_EXCELENTA_MS}ms) — probabil loopback sau LAN")
    elif rtt_avg < LATENTA_FOARTE_BUNA_MS:
        return (VERDE, f"foarte bună (<{LATENTA_FOARTE_BUNA_MS}ms) — conexiune locală rapidă")
    elif rtt_avg < LATENTA_BUNA_MS:
        return (GALBEN, f"bună (<{LATENTA_BUNA_MS}ms) — tipică pentru conexiuni regionale")
    else:
        return (ROSU, f"ridicată (>{LATENTA_BUNA_MS}ms) — conexiune la distanță sau congestie")


def interpreteaza_jitter(rtt_mdev: float) -> Tuple[str, str]:
    """Interpretează valoarea jitter-ului (deviația RTT).
    
    Args:
        rtt_mdev: Deviația standard RTT în milisecunde
        
    Returns:
        Tuple (cod_culoare, mesaj_explicativ)
    """
    if rtt_mdev < JITTER_EXCELENT_MS:
        return (VERDE, "excelent — conexiune foarte stabilă")
    elif rtt_mdev < JITTER_ACCEPTABIL_MS:
        return (GALBEN, "acceptabil — unele variații normale")
    else:
        return (ROSU, "ridicat — conexiune instabilă, probleme pentru VoIP/gaming")


def interpreteaza_pierdere(pierdere: float) -> Tuple[str, str]:
    """Interpretează procentul de pachete pierdute.
    
    Args:
        pierdere: Procentul de pierdere (0-100)
        
    Returns:
        Tuple (cod_culoare, mesaj_explicativ)
    """
    if pierdere == PIERDERE_EXCELENTA:
        return (VERDE, "Excelent!")
    elif pierdere < PIERDERE_ACCEPTABILA:
        return (GALBEN, "Acceptabil")
    else:
        return (ROSU, "Problemă de rețea!")


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTIE_PING
# ═══════════════════════════════════════════════════════════════════════════════

def executa_ping(
    destinatie: str,
    numar_pachete: int = DEFAULT_PACHETE,
    timeout: int = DEFAULT_TIMEOUT_SEC
) -> RezultatPing:
    """Execută ping și parsează rezultatele.
    
    Args:
        destinatie: Adresa IP sau hostname țintă
        numar_pachete: Câte pachete ICMP să trimită (1-100)
        timeout: Timeout per pachet în secunde
        
    Returns:
        RezultatPing cu datele colectate
        
    Raises:
        ValueError: Dacă numar_pachete nu e în intervalul valid
        
    Note:
        Funcția nu aruncă excepții pentru destinații inaccesibile;
        în schimb, returnează RezultatPing cu pachete_primite=0.
    """
    # Validare input
    if not MIN_PACHETE <= numar_pachete <= MAX_PACHETE:
        raise ValueError(
            f"numar_pachete trebuie să fie între {MIN_PACHETE} și {MAX_PACHETE}, "
            f"primit: {numar_pachete}"
        )
    
    rezultat = RezultatPing(destinatie=destinatie)
    
    try:
        # Rulează ping — formatul e standard Linux
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
    except FileNotFoundError:
        logger.error("Comanda 'ping' nu a fost găsită. Ești în container?")
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
    culoare_pierdere, mesaj_pierdere = interpreteaza_pierdere(pierdere)
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
        culoare_lat, mesaj_lat = interpreteaza_latenta(rezultat.rtt_avg)
        print(f"  • Latență {culoare_lat}{mesaj_lat}{RESET}")
        
        # Interpretare jitter
        culoare_jit, mesaj_jit = interpreteaza_jitter(rezultat.rtt_mdev)
        print(f"  • Jitter {culoare_jit}{mesaj_jit}{RESET}")
    
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
    """Funcția principală — rulează demonstrația de ping."""
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
    
    rezultate: List[RezultatPing] = []
    
    for ip, descriere in destinatii:
        print(f"{CYAN}Se testează: {descriere} ({ip})...{RESET}")
        rezultat = executa_ping(ip, numar_pachete=DEFAULT_PACHETE)
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
