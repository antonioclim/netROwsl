#!/usr/bin/env python3
"""
Asistent pentru Captura de Trafic
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oferă funcții helper pentru capturarea și analiza traficului de rețea.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Adaugă rădăcina proiectului la calea Python

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("captura_trafic")

# Filtre Wireshark recomandate pentru fiecare protocol
FILTRE_RECOMANDATE = {
    "http": "http or tcp.port == 8000",
    "dns": "udp.port == 5353 or dns",
    "ssh": "tcp.port == 2222 or ssh",
    "ftp": "tcp.port == 2121 or ftp or tcp.portrange == 30000-30009",
    "tls": "tcp.port == 4443 or tls or ssl",
    "toate": "ip.addr == 172.20.0.0/24",
}



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_filtre():
    """Afișează filtrele Wireshark recomandate."""
    print()
    print("=" * 60)
    print("  FILTRE WIRESHARK RECOMANDATE")
    print("=" * 60)
    print()
    
    for protocol, filtru in FILTRE_RECOMANDATE.items():
        print(f"  {protocol.upper():10} → {filtru}")
    
    print()
    print("  Combinații utile:")
    print("  ─" * 25)
    print("  HTTP + DNS:  (http or dns) and ip.addr == 172.20.0.0/24")
    print("  Doar cereri: http.request or dns.flags.response == 0")
    print("  Erori HTTP:  http.response.code >= 400")
    print()


def genereaza_nume_fisier(protocol: str = "general") -> Path:
    """Generează un nume de fișier pentru captură."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_capturi = RADACINA_PROIECT / "pcap"
    dir_capturi.mkdir(parents=True, exist_ok=True)
    return dir_capturi / f"week10_{protocol}_{timestamp}.pcap"


def porneste_captura_tcpdump(
    interfata: str = "any",
    fisier: Path = None,
    filtru: str = None,
    numar_pachete: int = None
):
    """
    Pornește captura cu tcpdump în containerul debug.
    
    Args:
        interfata: Interfața de rețea
        fisier: Fișierul de ieșire
        filtru: Filtru BPF
        numar_pachete: Număr maxim de pachete
    """
    if fisier is None:
        fisier = genereaza_nume_fisier()
    
    comanda = [
        "docker", "exec", "-it", "week10_debug",
        "tcpdump", "-i", interfata, "-w", f"/tmp/{fisier.name}"
    ]
    
    if filtru:
        comanda.extend(["-f", filtru])
    
    if numar_pachete:
        comanda.extend(["-c", str(numar_pachete)])
    
    logger.info(f"Pornire captură pe {interfata}...")
    logger.info(f"Fișier ieșire: {fisier}")
    logger.info("Apăsați Ctrl+C pentru oprire")
    print()
    
    try:
        subprocess.run(comanda)
        
        # Copiază fișierul din container
        logger.info("Copiere fișier captură...")
        subprocess.run([
            "docker", "cp",
            f"week10_debug:/tmp/{fisier.name}",
            str(fisier)
        ])
        logger.info(f"Captură salvată: {fisier}")
        
    except KeyboardInterrupt:
        logger.info("\nCaptură oprită")
        # Încearcă să copieze ce s-a capturat
        subprocess.run([
            "docker", "cp",
            f"week10_debug:/tmp/{fisier.name}",
            str(fisier)
        ], capture_output=True)


def deschide_wireshark(fisier: Path = None):
    """Deschide Wireshark cu un fișier de captură."""
    cai_wireshark = [
        r"C:\Program Files\Wireshark\Wireshark.exe",
        r"C:\Program Files (x86)\Wireshark\Wireshark.exe",
        "wireshark",
    ]
    
    cale_wireshark = None
    for cale in cai_wireshark:
        try:
            subprocess.run(
                [cale, "--version"],
                capture_output=True,
                timeout=5
            )
            cale_wireshark = cale
            break
        except Exception:
            continue
    
    if not cale_wireshark:
        logger.error("Wireshark nu a fost găsit")
        logger.info("Instalați Wireshark de pe: https://www.wireshark.org/")
        return False
    
    comanda = [cale_wireshark]
    if fisier and fisier.exists():
        comanda.append(str(fisier))
    
    logger.info(f"Pornire Wireshark...")
    subprocess.Popen(comanda)
    return True


def listeaza_capturi():
    """Listează capturile existente."""
    dir_capturi = RADACINA_PROIECT / "pcap"
    
    print()
    print("=" * 60)
    print("  CAPTURI SALVATE")
    print("=" * 60)
    print()
    
    capturi = list(dir_capturi.glob("*.pcap"))
    
    if not capturi:
        print("  Nu există capturi salvate.")
        print(f"  Director: {dir_capturi}")
    else:
        for captura in sorted(capturi):
            dimensiune = captura.stat().st_size
            print(f"  {captura.name:40} ({dimensiune:,} bytes)")
    
    print()



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Asistent pentru Captura de Trafic - Laboratorul Săptămânii 10"
    )
    parser.add_argument(
        "--interfata", "-i",
        default="any",
        help="Interfața de rețea pentru captură (implicit: any)"
    )
    parser.add_argument(
        "--iesire", "-o",
        type=Path,
        help="Fișierul de ieșire pentru captură"
    )
    parser.add_argument(
        "--filtru", "-f",
        help="Filtru BPF pentru captură"
    )
    parser.add_argument(
        "--numar", "-n",
        type=int,
        help="Număr maxim de pachete de capturat"
    )
    parser.add_argument(
        "--filtre",
        action="store_true",
        help="Afișează filtrele Wireshark recomandate"
    )
    parser.add_argument(
        "--lista",
        action="store_true",
        help="Listează capturile existente"
    )
    parser.add_argument(
        "--wireshark",
        action="store_true",
        help="Deschide Wireshark"
    )
    parser.add_argument(
        "--deschide",
        type=Path,
        help="Deschide un fișier de captură specific în Wireshark"
    )
    args = parser.parse_args()

    try:
        if args.filtre:
            afiseaza_filtre()
            return 0
        
        if args.lista:
            listeaza_capturi()
            return 0
        
        if args.wireshark:
            deschide_wireshark()
            return 0
        
        if args.deschide:
            deschide_wireshark(args.deschide)
            return 0
        
        # Pornire captură
        porneste_captura_tcpdump(
            interfata=args.interfata,
            fisier=args.iesire,
            filtru=args.filtru,
            numar_pachete=args.numar
        )
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare: {e}")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
