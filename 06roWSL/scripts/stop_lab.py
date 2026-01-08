#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 6
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script oprește grațios toate containerele Docker păstrând datele.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import socket
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("stop_lab")

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


def main() -> int:
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description="Oprește mediul de laborator Săptămâna 6"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Timeout în secunde pentru oprire grațioasă (implicit: 30)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Forțează oprirea imediată a containerelor"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișare detaliată"
    )
    args = parser.parse_args()
    
    if args.verbose:
        from scripts.utils.logger import set_verbose
        set_verbose(logger, True)
    
    director_docker = RADACINA_PROIECT / "docker"
    
    try:
        docker = DockerManager(director_docker)
    except FileNotFoundError as e:
        logger.error(f"Configurația Docker nu a fost găsită: {e}")
        return 1
    
    logger.info("=" * 60)
    logger.info("Oprirea mediului de laborator Săptămâna 6")
    logger.info("(Portainer rămâne activ pe portul 9000)")
    logger.info("=" * 60)
    
    try:
        # Afișează starea curentă
        logger.info("Servicii care rulează în prezent:")
        stare = docker.compose_ps()
        for nume, info in stare.items():
            starea_serv = info.get("State", "necunoscută")
            # Nu afișa Portainer în lista de servicii de laborator
            if "portainer" not in nume.lower():
                logger.info(f"  {nume}: {starea_serv}")
        
        if not stare:
            logger.info("  Niciun serviciu de laborator nu rulează")
            return 0
        
        # Oprește serviciile
        logger.info("")
        logger.info("Se opresc containerele de laborator...")
        logger.info("(Portainer va rămâne activ)")
        
        if args.force:
            logger.info("Oprire forțată a tuturor containerelor...")
        else:
            logger.info(f"Oprire grațioasă a containerelor (timeout: {args.timeout}s)...")
        
        # docker compose stop păstrează volumele
        fisier_compose = director_docker / "docker-compose.yml"
        
        cmd = ["docker", "compose", "-f", str(fisier_compose), "stop"]
        if args.timeout:
            cmd.extend(["-t", str(args.timeout)])
        
        rezultat = subprocess.run(cmd, cwd=director_docker)
        
        if rezultat.returncode == 0:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ Toate serviciile de laborator au fost oprite cu succes")
            logger.info("")
            
            # Verifică și afișează status Portainer
            if verifica_portainer_status():
                logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
            else:
                logger.warning(f"⚠ Portainer nu rulează pe {PORTAINER_URL}")
            
            logger.info("")
            logger.info("Datele din volume au fost păstrate.")
            logger.info("Pentru a elimina complet containerele: python3 scripts/cleanup.py")
            logger.info("Pentru a reporni: python3 scripts/start_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Eșec la oprirea unor servicii")
            return 1
    
    except KeyboardInterrupt:
        print("\nOprire întreruptă")
        return 130
    except Exception as e:
        logger.error(f"Eșec la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
