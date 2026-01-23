#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 2
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.

NOTĂ: Portainer rulează global pe portul 9000 și NU este gestionat de acest script.
Accesați Portainer la: http://localhost:9000 (credențiale: stud / studstudstud)
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import time
import argparse
import socket
from pathlib import Path
from typing import Dict, Any

# Adăugare rădăcină proiect la cale

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RĂDĂCINĂ_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RĂDĂCINĂ_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configurează_logger

logger = configurează_logger("start_lab")

# Definire servicii și configurația lor
# NOTĂ: Portainer NU este inclus - rulează global pe portul 9000
SERVICII: Dict[str, Dict[str, Any]] = {
    "week2_lab": {
        "container": "week2_lab",
        "port_tcp": 9090,
        "port_udp": 9091,
        "verificare_stare": None,
        "timp_pornire": 5,
        "descriere": "Container principal (servere TCP/UDP)"
    }
}

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def verifică_docker_activ() -> bool:
    """Verifică dacă Docker este activ și funcțional."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def pornește_docker_service() -> bool:
    """Încearcă să pornească serviciul Docker în WSL."""
    logger.info("Se încearcă pornirea serviciului Docker...")
    try:
        rezultat = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if rezultat.returncode == 0:
            time.sleep(2)
            return verifică_docker_activ()
        else:
            logger.error(f"Eroare la pornirea Docker: {rezultat.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("Timeout la pornirea serviciului Docker")
        return False
    except Exception as e:
        logger.error(f"Eroare neașteptată: {e}")
        return False


def verifică_portainer_status() -> bool:
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


def afișează_avertisment_portainer() -> None:
    """Afișează avertisment dacă Portainer nu rulează."""
    logger.warning("")
    logger.warning("=" * 60)
    logger.warning("⚠️  AVERTISMENT: Portainer nu rulează!")
    logger.warning("")
    logger.warning("Portainer este instrumentul vizual pentru gestionarea Docker.")
    logger.warning("Pentru a-l porni, executați în terminal:")
    logger.warning("")
    logger.warning("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
    logger.warning("    -v /var/run/docker.sock:/var/run/docker.sock \\")
    logger.warning("    -v portainer_data:/data portainer/portainer-ce:latest")
    logger.warning("")
    logger.warning(f"După pornire, accesați: {PORTAINER_URL}")
    logger.warning(f"Credențiale: {PORTAINER_USER} / {PORTAINER_PASS}")
    logger.warning("=" * 60)
    logger.warning("")


def afișează_stare(manager: ManagerDocker) -> None:
    """Afișează starea curentă a serviciilor."""
    logger.info("=" * 60)
    logger.info("Starea Serviciilor")
    logger.info("=" * 60)
    
    for nume, config in SERVICII.items():
        container = config["container"]
        rulează = manager.container_rulează(container)
        stare = "🟢 Activ" if rulează else "🔴 Oprit"
        logger.info(f"  {nume}: {stare}")
        
        if rulează and "port_tcp" in config:
            logger.info(f"      Port TCP: {config['port_tcp']}")
        if rulează and "port_udp" in config:
            logger.info(f"      Port UDP: {config['port_udp']}")
    
    # Afișează și starea Portainer
    if verifică_portainer_status():
        logger.info(f"  portainer: 🟢 Activ (global)")
        logger.info(f"      Port: {PORTAINER_PORT}")
    else:
        logger.info(f"  portainer: 🔴 Oprit (global)")


def verifică_servicii(manager: ManagerDocker) -> bool:
    """
    Verifică dacă toate serviciile sunt funcționale.
    
    Returns:
        True dacă toate serviciile sunt sănătoase
    """
    toate_sănătoase = True
    
    for nume, config in SERVICII.items():
        container = config["container"]
        
        if not manager.container_rulează(container):
            logger.error(f"  ✗ {nume}: Containerul nu rulează")
            toate_sănătoase = False
            continue
        
        # Verificare port TCP
        if "port_tcp" in config:
            port = config["port_tcp"]
            if manager.verifică_port("localhost", port):
                logger.info(f"  ✓ {nume}: Port TCP {port} accesibil")
            else:
                logger.warning(f"  ⚠ {nume}: Port TCP {port} nu răspunde încă")
        
        # Verificare port UDP (mai greu de testat)
        if "port_udp" in config:
            logger.info(f"  ℹ {nume}: Port UDP {config['port_udp']} configurat")
    
    return toate_sănătoase



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Pornire Laborator Săptămâna 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  python3 start_lab.py              # Pornire normală
  python3 start_lab.py --status     # Verificare stare
  python3 start_lab.py --rebuild    # Reconstruire imagini

NOTĂ: Portainer rulează global pe portul 9000 și nu este gestionat de acest script.
      Accesați: http://localhost:9000 (stud / studstudstud)
        """
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Doar verifică starea (nu pornește nimic)"
    )
    parser.add_argument(
        "--rebuild", "-r",
        action="store_true",
        help="Forțează reconstruirea imaginilor Docker"
    )
    parser.add_argument(
        "--detach", "-d",
        action="store_true",
        default=True,
        help="Rulează în fundal (implicit: da)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișează informații detaliate"
    )
    
    args = parser.parse_args()

    # Verifică și pornește Docker dacă nu rulează
    if not verifică_docker_activ():
        logger.warning("Docker nu este activ. Se încearcă pornirea automată...")
        if not pornește_docker_service():
            logger.error("")
            logger.error("Nu s-a putut porni Docker!")
            logger.error("Încercați manual: sudo service docker start")
            logger.error("(Parolă: stud)")
            return 1
        logger.info("✓ Docker a fost pornit cu succes!")

    # Inițializare manager Docker
    cale_docker = RĂDĂCINĂ_PROIECT / "docker"
    manager = ManagerDocker(cale_docker)

    # Verifică status Portainer (doar avertisment, nu oprește execuția)
    if not verifică_portainer_status():
        afișează_avertisment_portainer()

    # Doar afișare stare
    if args.status:
        afișează_stare(manager)
        return 0

    # Pornire laborator
    logger.info("=" * 60)
    logger.info("Pornire Mediu de Laborator - Săptămâna 2")
    logger.info("Rețele de Calculatoare - ASE, Informatică Economică")
    logger.info("=" * 60)

    try:
        # Construire imagini dacă este necesar
        if args.rebuild:
            logger.info("Reconstruire imagini Docker...")
            manager.compose_build()
        
        # Pornire containere (fără Portainer - rulează global)
        logger.info("Pornire containere...")
        manager.compose_up(detach=args.detach)

        # Așteptare inițializare servicii
        logger.info("Așteptare inițializare servicii...")
        timp_maxim = max(s.get("timp_pornire", 5) for s in SERVICII.values())
        
        for i in range(timp_maxim):
            time.sleep(1)
            sys.stdout.write(f"\r  Progres: {i + 1}/{timp_maxim} secunde...")
            sys.stdout.flush()
        print()

        # Verificare servicii
        logger.info("Verificare servicii...")
        toate_funcționale = verifică_servicii(manager)

        if toate_funcționale:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            
            # Afișează status Portainer
            if verifică_portainer_status():
                logger.info(f"  • Portainer:  {PORTAINER_URL}")
            else:
                logger.warning(f"  • Portainer:  NU RULEAZĂ (vezi instrucțiuni mai sus)")
            
            logger.info(f"  • Server TCP: localhost:9090")
            logger.info(f"  • Server UDP: localhost:9091")
            logger.info("")
            logger.info("Pentru a porni un server TCP:")
            logger.info("  docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server")
            logger.info("")
            logger.info("Pentru a porni un server UDP:")
            logger.info("  docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py server")
            logger.info("")
            logger.info("Pentru a opri laboratorul:")
            logger.info("  python3 scripts/stop_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.warning("Unele servicii nu au pornit complet.")
            logger.info("Încercați să așteptați câteva secunde și rulați:")
            logger.info("  python3 scripts/start_lab.py --status")
            return 1

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
