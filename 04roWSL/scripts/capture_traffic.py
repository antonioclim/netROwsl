#!/usr/bin/env python3
"""
Asistent Capturare Trafic
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest script ajută la capturarea traficului de rețea pentru analiză.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# Adaugă rădăcina proiectului la path

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("capture")



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def gaseste_instrument_captura() -> tuple[str, str]:
    """Găsește instrumentul de capturare disponibil."""
    instrumente = [
        ("tcpdump", "tcpdump"),
        ("tshark", "tshark"),
        ("dumpcap", "dumpcap")
    ]
    
    for nume, comanda in instrumente:
        if shutil.which(comanda):
            return nume, comanda
    
    return None, None


def listeaza_interfete():
    """Listează interfețele de rețea disponibile."""
    nume, comanda = gaseste_instrument_captura()
    
    if not comanda:
        logger.error("Niciun instrument de capturare găsit (tcpdump, tshark, dumpcap)")
        logger.info("Instalați Wireshark sau tcpdump pentru capturare pachete")
        return
    
    logger.info("Interfețe de rețea disponibile:")
    
    try:
        if nume == "tcpdump":
            rezultat = subprocess.run(
                ["tcpdump", "-D"],
                capture_output=True,
                timeout=5
            )
        elif nume in ["tshark", "dumpcap"]:
            rezultat = subprocess.run(
                [comanda, "-D"],
                capture_output=True,
                timeout=5
            )
        
        if rezultat.returncode == 0:
            print(rezultat.stdout.decode())
        else:
            logger.error(f"Eroare: {rezultat.stderr.decode()}")
            
    except subprocess.TimeoutExpired:
        logger.error("Timeout la listarea interfețelor")
    except PermissionError:
        logger.error("Permisiuni insuficiente. Încercați cu sudo/administrator.")
    except Exception as e:
        logger.error(f"Eroare: {e}")


def porneste_captura(interfata: str, output: str, port: int = None, 
                     durata: int = None, numar_pachete: int = None):
    """Pornește capturarea traficului."""
    nume, comanda = gaseste_instrument_captura()
    
    if not comanda:
        logger.error("Niciun instrument de capturare găsit")
        logger.info("Pe Windows: Instalați Wireshark")
        logger.info("Pe Linux/WSL: sudo apt install tcpdump")
        return False
    
    # Construiește comanda
    if nume == "tcpdump":
        cmd = ["tcpdump", "-i", interfata, "-w", output]
        if port:
            cmd.extend(["port", str(port)])
        if numar_pachete:
            cmd.extend(["-c", str(numar_pachete)])
    elif nume in ["tshark", "dumpcap"]:
        cmd = [comanda, "-i", interfata, "-w", output]
        if port:
            cmd.extend(["-f", f"port {port}"])
        if durata:
            cmd.extend(["-a", f"duration:{durata}"])
        if numar_pachete:
            cmd.extend(["-c", str(numar_pachete)])
    
    logger.info(f"Pornire capturare cu {nume}...")
    logger.info(f"  Interfață: {interfata}")
    logger.info(f"  Fișier: {output}")
    if port:
        logger.info(f"  Port: {port}")
    if durata:
        logger.info(f"  Durată: {durata} secunde")
    if numar_pachete:
        logger.info(f"  Număr pachete: {numar_pachete}")
    
    logger.info("\nCapturare în curs... Apăsați Ctrl+C pentru oprire.\n")
    
    try:
        if durata and nume == "tcpdump":
            # tcpdump nu are opțiune nativă de durată
            subprocess.run(cmd, timeout=durata)
        else:
            subprocess.run(cmd)
        
        logger.info(f"\n✓ Capturare salvată: {output}")
        return True
        
    except subprocess.TimeoutExpired:
        logger.info(f"\n✓ Capturare oprită după {durata} secunde")
        logger.info(f"  Fișier salvat: {output}")
        return True
    except KeyboardInterrupt:
        logger.info("\n✓ Capturare oprită de utilizator")
        logger.info(f"  Fișier salvat: {output}")
        return True
    except PermissionError:
        logger.error("\nEroare: Permisiuni insuficiente pentru capturare.")
        logger.info("Pe Linux/WSL: rulați cu sudo")
        logger.info("Pe Windows: rulați ca Administrator")
        return False
    except Exception as e:
        logger.error(f"\nEroare la capturare: {e}")
        return False


def genereaza_nume_fisier(prefix: str = "captura") -> str:
    """Generează un nume de fișier cu timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.pcap"



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Asistent Capturare Trafic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python scripts/capture_traffic.py --list              # Listează interfețele
  python scripts/capture_traffic.py -i eth0            # Capturează pe eth0
  python scripts/capture_traffic.py -i any --port 5400  # Filtrează port 5400
  python scripts/capture_traffic.py -i any --duration 60  # Capturează 60s
  python scripts/capture_traffic.py -i any -o captura.pcap  # Specifică fișierul

Porturi laborator:
  5400 - Protocol TEXT (TCP)
  5401 - Protocol BINAR (TCP)
  5402 - Senzor UDP
        """
    )
    parser.add_argument("--list", "-l", action="store_true",
                        help="Listează interfețele de rețea disponibile")
    parser.add_argument("--interface", "-i", default="any",
                        help="Interfața de rețea (implicit: any)")
    parser.add_argument("--output", "-o",
                        help="Fișierul de ieșire (implicit: captura_<timestamp>.pcap)")
    parser.add_argument("--port", "-p", type=int,
                        help="Filtrează după port")
    parser.add_argument("--duration", "-d", type=int,
                        help="Durată capturare în secunde")
    parser.add_argument("--count", "-c", type=int,
                        help="Număr pachete de capturat")
    
    args = parser.parse_args()
    
    if args.list:
        listeaza_interfete()
        return 0
    
    # Determină fișierul de ieșire
    if args.output:
        fisier_output = args.output
    else:
        dir_pcap = RADACINA_PROIECT / "pcap"
        dir_pcap.mkdir(exist_ok=True)
        fisier_output = str(dir_pcap / genereaza_nume_fisier())
    
    # Asigură-te că fișierul are extensia .pcap
    if not fisier_output.endswith(".pcap"):
        fisier_output += ".pcap"
    
    logger.info("=" * 60)
    logger.info("ASISTENT CAPTURARE TRAFIC")
    logger.info("Laborator Săptămâna 4 - Rețele de Calculatoare")
    logger.info("=" * 60)
    
    succes = porneste_captura(
        interfata=args.interface,
        output=fisier_output,
        port=args.port,
        durata=args.duration,
        numar_pachete=args.count
    )
    
    if succes:
        logger.info("\nPentru analiză, deschideți fișierul în Wireshark:")
        logger.info(f"  wireshark {fisier_output}")
        logger.info("\nSau folosiți tshark pentru analiză în linia de comandă:")
        logger.info(f"  tshark -r {fisier_output}")
    
    return 0 if succes else 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
