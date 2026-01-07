#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 4
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest script oprește toate containerele și procesele laboratorului.
"""

import subprocess
import sys
import time
import argparse
import signal
import os
from pathlib import Path

# Adaugă rădăcina proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("stop_lab")


def opreste_procese_native():
    """Oprește procesele Python native (serverele protocol)."""
    procese_oprite = 0
    
    # Caută și oprește procesele server
    scripturi_server = [
        "text_proto_server.py",
        "binary_proto_server.py",
        "udp_sensor_server.py"
    ]
    
    try:
        # Pe Windows/WSL
        if sys.platform == "win32":
            for script in scripturi_server:
                subprocess.run(
                    ["taskkill", "/F", "/IM", "python.exe", "/FI", f"WINDOWTITLE eq *{script}*"],
                    capture_output=True
                )
        else:
            # Pe Linux/Unix
            rezultat = subprocess.run(
                ["pgrep", "-f", "proto_server"],
                capture_output=True
            )
            if rezultat.returncode == 0:
                pids = rezultat.stdout.decode().strip().split('\n')
                for pid in pids:
                    if pid:
                        try:
                            os.kill(int(pid), signal.SIGTERM)
                            procese_oprite += 1
                            logger.info(f"  Proces oprit: PID {pid}")
                        except ProcessLookupError:
                            pass
                        except Exception as e:
                            logger.warning(f"  Nu s-a putut opri PID {pid}: {e}")
    except Exception as e:
        logger.debug(f"Eroare la oprirea proceselor native: {e}")
    
    return procese_oprite


def opreste_containere_docker(force: bool = False, timeout: int = 10):
    """Oprește containerele Docker."""
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    try:
        if force:
            logger.info("Oprire forțată a containerelor...")
            subprocess.run(
                ["docker", "compose", "-f", str(RADACINA_PROIECT / "docker" / "docker-compose.yml"),
                 "kill"],
                capture_output=True,
                timeout=30
            )
        else:
            logger.info(f"Oprire grațioasă a containerelor (timeout: {timeout}s)...")
            docker.compose_down(volumes=False)
        
        return True
    except Exception as e:
        logger.error(f"Eroare la oprirea containerelor: {e}")
        return False


def verifica_servicii_oprite() -> bool:
    """Verifică dacă toate serviciile sunt oprite."""
    import socket
    
    porturi = [5400, 5401, 5402, 9443]
    toate_oprite = True
    
    for port in porturi:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                rezultat = s.connect_ex(('localhost', port))
                if rezultat == 0:
                    toate_oprite = False
                    logger.warning(f"  Portul {port} încă activ")
        except Exception:
            pass
    
    return toate_oprite


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprire Laborator Săptămâna 4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python scripts/stop_lab.py            # Oprire grațioasă
  python scripts/stop_lab.py --force    # Oprire forțată
  python scripts/stop_lab.py --timeout 30  # Oprire cu timeout personalizat
        """
    )
    parser.add_argument("--force", "-f", action="store_true",
                        help="Oprire forțată (kill în loc de stop)")
    parser.add_argument("--timeout", "-t", type=int, default=10,
                        help="Timeout pentru oprire grațioasă (implicit: 10s)")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Oprire Mediu Laborator Săptămâna 4")
    logger.info("=" * 60)
    
    # Oprește procesele native
    logger.info("\nOprire procese native...")
    procese_oprite = opreste_procese_native()
    if procese_oprite > 0:
        logger.info(f"  {procese_oprite} procese native oprite")
    else:
        logger.info("  Niciun proces nativ activ")
    
    # Oprește containerele Docker
    logger.info("\nOprire containere Docker...")
    opreste_containere_docker(args.force, args.timeout)
    
    # Așteaptă puțin pentru oprire completă
    time.sleep(2)
    
    # Verificare
    logger.info("\nVerificare stare finală...")
    if verifica_servicii_oprite():
        logger.info("  ✓ Toate serviciile sunt oprite")
    else:
        logger.warning("  ⚠ Unele servicii încă rulează")
        logger.info("    Încercați: python scripts/stop_lab.py --force")
    
    # Verificare containere Docker
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=week4", "-q"],
            capture_output=True,
            timeout=5
        )
        if rezultat.stdout.strip():
            logger.warning("  ⚠ Unele containere Docker încă rulează")
            logger.info("    Rulați: docker ps pentru detalii")
        else:
            logger.info("  ✓ Niciun container Docker week4 activ")
    except Exception:
        pass
    
    logger.info("\n" + "=" * 60)
    logger.info("Oprire completă!")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
