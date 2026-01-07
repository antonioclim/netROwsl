#!/usr/bin/env python3
"""
Script de Captură a Traficului de Rețea
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Wrapper pentru tcpdump/tshark cu suport pentru filtre specifice laboratorului.
"""

import subprocess
import sys
import argparse
import signal
import time
from pathlib import Path
from datetime import datetime

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("captura_trafic")

# Filtre predefinite pentru protocoalele din laborator
FILTRE_PREDEFINITE = {
    "smtp": "port 1025",
    "jsonrpc": "port 6200",
    "xmlrpc": "port 6201",
    "grpc": "port 6251",
    "rpc-toate": "port 6200 or port 6201 or port 6251",
    "toate": "port 1025 or port 6200 or port 6201 or port 6251"
}


class CaptorTrafic:
    """Clasă pentru gestionarea capturilor de trafic."""
    
    def __init__(self, interfata: str = "any"):
        self.interfata = interfata
        self.proces = None
    
    def genereaza_filtru_bpf(self, porturi: list = None, protocol: str = None) -> str:
        """Generează un filtru BPF pentru captura de trafic."""
        if protocol and protocol in FILTRE_PREDEFINITE:
            return FILTRE_PREDEFINITE[protocol]
        
        if porturi:
            conditii = [f"port {p}" for p in porturi]
            return " or ".join(conditii)
        
        return FILTRE_PREDEFINITE["toate"]
    
    def porneste_captura(self, fisier_iesire: Path, filtru: str, durata: int = None):
        """Pornește captura de trafic."""
        
        # Verificăm dacă avem tcpdump sau tshark
        comanda = None
        
        # Încercăm tcpdump mai întâi
        rezultat = subprocess.run(
            ["which", "tcpdump"],
            capture_output=True
        )
        if rezultat.returncode == 0:
            comanda = [
                "tcpdump",
                "-i", self.interfata,
                "-w", str(fisier_iesire),
                filtru
            ]
            if durata:
                # tcpdump nu are durată directă, folosim timeout
                comanda = ["timeout", str(durata)] + comanda
        else:
            # Încercăm tshark
            rezultat = subprocess.run(
                ["which", "tshark"],
                capture_output=True
            )
            if rezultat.returncode == 0:
                comanda = [
                    "tshark",
                    "-i", self.interfata,
                    "-w", str(fisier_iesire),
                    "-f", filtru
                ]
                if durata:
                    comanda.extend(["-a", f"duration:{durata}"])
        
        if not comanda:
            logger.error("Nici tcpdump nici tshark nu sunt disponibile!")
            logger.info("Instalați cu: apt-get install tcpdump tshark")
            return False
        
        logger.info(f"Pornire captură: {' '.join(comanda)}")
        logger.info(f"Fișier ieșire: {fisier_iesire}")
        logger.info(f"Filtru: {filtru}")
        
        if durata:
            logger.info(f"Durată: {durata} secunde")
        else:
            logger.info("Apăsați Ctrl+C pentru a opri captura")
        
        try:
            self.proces = subprocess.Popen(
                comanda,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Așteptăm finalizarea sau întreruperea
            self.proces.wait()
            
            logger.info(f"✓ Captură salvată în: {fisier_iesire}")
            return True
            
        except KeyboardInterrupt:
            logger.info("\nCaptură oprită de utilizator")
            if self.proces:
                self.proces.terminate()
            return True
        except Exception as e:
            logger.error(f"Eroare la captură: {e}")
            return False
    
    def analizeaza_captura(self, fisier_captura: Path):
        """Analizează o captură existentă."""
        if not fisier_captura.exists():
            logger.error(f"Fișierul nu există: {fisier_captura}")
            return
        
        logger.info(f"Analiză captură: {fisier_captura}")
        logger.info("-" * 40)
        
        # Statistici cu tshark
        comenzi_analiza = [
            ("Rezumat pachete", ["tshark", "-r", str(fisier_captura), "-q", "-z", "io,stat,0"]),
            ("Ierarhie protocoale", ["tshark", "-r", str(fisier_captura), "-q", "-z", "io,phs"]),
            ("Conversații", ["tshark", "-r", str(fisier_captura), "-q", "-z", "conv,tcp"])
        ]
        
        for titlu, comanda in comenzi_analiza:
            print(f"\n{titlu}:")
            print("-" * 30)
            try:
                rezultat = subprocess.run(
                    comanda,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if rezultat.stdout:
                    print(rezultat.stdout)
            except Exception as e:
                print(f"  Eroare: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Captură trafic de rețea pentru Laboratorul Săptămânii 12"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Fișier de ieșire pentru captură"
    )
    parser.add_argument(
        "--durata", "-d",
        type=int,
        help="Durata capturii în secunde"
    )
    parser.add_argument(
        "--interfata", "-i",
        default="any",
        help="Interfața de rețea (implicit: any)"
    )
    parser.add_argument(
        "--filtru", "-f",
        help="Filtru BPF personalizat"
    )
    parser.add_argument(
        "--protocol", "-p",
        choices=list(FILTRE_PREDEFINITE.keys()),
        default="toate",
        help="Protocol predefinit pentru captură"
    )
    parser.add_argument(
        "--port",
        type=int,
        action="append",
        help="Port specific de capturat (poate fi repetat)"
    )
    parser.add_argument(
        "--analiza",
        type=Path,
        help="Analizează o captură existentă"
    )
    args = parser.parse_args()

    captor = CaptorTrafic(interfata=args.interfata)

    # Modul analiză
    if args.analiza:
        captor.analizeaza_captura(args.analiza)
        return 0

    # Generare nume fișier implicit
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = RADACINA_PROIECT / "pcap" / f"week12_{args.protocol}_{timestamp}.pcap"
    
    # Asigurare că directorul există
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Determinare filtru
    if args.filtru:
        filtru = args.filtru
    elif args.port:
        filtru = captor.genereaza_filtru_bpf(porturi=args.port)
    else:
        filtru = captor.genereaza_filtru_bpf(protocol=args.protocol)

    logger.info("=" * 60)
    logger.info("Captură Trafic - Laboratorul Săptămânii 12")
    logger.info("=" * 60)

    succes = captor.porneste_captura(
        fisier_iesire=args.output,
        filtru=filtru,
        durata=args.durata
    )

    return 0 if succes else 1


if __name__ == "__main__":
    sys.exit(main())
