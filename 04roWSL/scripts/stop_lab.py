#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 4
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest script oprește toate containerele și procesele laboratorului.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!
"""

import subprocess
import sys
import time
import argparse
import signal
import socket
import os
from pathlib import Path

# Adaugă rădăcina proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("stop_lab")

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"

# Containere care NU trebuie oprite (rulează global)
CONTAINERE_EXCLUSE = ["portainer"]


def verifica_portainer_status() -> bool:
    """Verifică dacă Portainer rulează pe portul 9000."""
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0 and "Up" in rezultat.stdout:
            return True
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', PORTAINER_PORT))
            sock.close()
            return result == 0
        except Exception:
            return False
            
    except Exception:
        return False


def este_container_exclus(nume_container: str) -> bool:
    """Verifică dacă un container este în lista de excluderi."""
    return any(exclus in nume_container.lower() for exclus in CONTAINERE_EXCLUSE)


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
    """Oprește containerele Docker (exclusiv Portainer)."""
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    try:
        # Obține lista containerelor saptamana4 (exclude portainer)
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=saptamana4", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        
        containere = [
            c.strip() for c in rezultat.stdout.strip().split("\n") 
            if c.strip() and not este_container_exclus(c.strip())
        ]
        
        if not containere:
            logger.info("  Nu există containere de laborator active.")
            return True
        
        logger.info(f"  Se opresc {len(containere)} containere de laborator...")
        logger.info("  (Portainer va rămâne activ)")
        
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
    """Verifică dacă toate serviciile de laborator sunt oprite."""
    porturi = [5400, 5401, 5402]  # Fără 9000 (Portainer)
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
  python3 scripts/stop_lab.py            # Oprire grațioasă
  python3 scripts/stop_lab.py --force    # Oprire forțată
  python3 scripts/stop_lab.py --timeout 30  # Oprire cu timeout personalizat

NOTĂ: Portainer NU este oprit - rulează global pe portul 9000.
        """
    )
    parser.add_argument("--force", "-f", action="store_true",
                        help="Oprire forțată (kill în loc de stop)")
    parser.add_argument("--timeout", "-t", type=int, default=10,
                        help="Timeout pentru oprire grațioasă (implicit: 10s)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Afișează informații detaliate")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Oprire Mediu Laborator Săptămâna 4")
    logger.info("(Portainer rămâne activ pe portul 9000)")
    logger.info("=" * 60)
    
    # Oprește procesele native
    logger.info("\nOprire procese native...")
    procese_oprite = opreste_procese_native()
    if procese_oprite > 0:
        logger.info(f"  {procese_oprite} procese native oprite")
    else:
        logger.info("  Niciun proces nativ activ")
    
    # Oprește containerele Docker (fără Portainer)
    logger.info("\nOprire containere Docker...")
    opreste_containere_docker(args.force, args.timeout)
    
    # Așteaptă puțin pentru oprire completă
    time.sleep(2)
    
    # Verificare
    logger.info("\nVerificare stare finală...")
    if verifica_servicii_oprite():
        logger.info("  ✓ Toate serviciile de laborator sunt oprite")
    else:
        logger.warning("  ⚠ Unele servicii încă rulează")
        logger.info("    Încercați: python3 scripts/stop_lab.py --force")
    
    # Verifică și afișează status Portainer
    if verifica_portainer_status():
        logger.info(f"  ✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
    else:
        logger.warning(f"  ⚠ Portainer nu rulează")
    
    # Verificare containere Docker
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=saptamana4", "-q"],
            capture_output=True,
            timeout=5
        )
        if rezultat.stdout.strip():
            logger.warning("  ⚠ Unele containere Docker încă rulează")
            logger.info("    Rulați: docker ps pentru detalii")
        else:
            logger.info("  ✓ Niciun container Docker saptamana4 activ")
    except Exception:
        pass
    
    logger.info("\n" + "=" * 60)
    logger.info("Oprire completă!")
    logger.info("")
    logger.info("Pentru a relua laboratorul:")
    logger.info("  python3 scripts/start_lab.py")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
