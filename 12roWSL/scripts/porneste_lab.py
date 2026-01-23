#!/usr/bin/env python3
"""
Script de Pornire a Laboratorului Săptămânii 12
===============================================
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI_SI_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import time
import argparse
import socket
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_SI_CONFIGURATIE
# ═══════════════════════════════════════════════════════════════════════════════
PORTAINER_PORT = 9000
SERVICII = {
    "smtp": {"port": 1025, "descriere": "Server SMTP"},
    "jsonrpc": {"port": 6200, "descriere": "Server JSON-RPC"},
    "xmlrpc": {"port": 6201, "descriere": "Server XML-RPC"},
    "grpc": {"port": 6251, "descriere": "Server gRPC"},
}

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICARE_DOCKER
# ═══════════════════════════════════════════════════════════════════════════════
def verifica_docker_disponibil() -> bool:
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=10)
        return result.returncode == 0
    except Exception:
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICARE_PORTURI_SERVICII
# ═══════════════════════════════════════════════════════════════════════════════
def verifica_port(port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex(('localhost', port)) == 0
    except Exception:
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# ASTEPTARE_SERVICII
# ═══════════════════════════════════════════════════════════════════════════════
def asteapta_servicii(timeout: int = 60) -> bool:
    logger.info("Se așteaptă pornirea serviciilor...")
    timp_start = time.time()
    porturi_asteptate = {1025, 6200, 6201, 6251}
    
    while time.time() - timp_start < timeout:
        porturi_active = {p for p in porturi_asteptate if verifica_port(p)}
        if porturi_active == porturi_asteptate:
            logger.info("✓ Toate serviciile sunt active!")
            return True
        time.sleep(2)
    return False

# ═══════════════════════════════════════════════════════════════════════════════
# AFISARE_STATUS
# ═══════════════════════════════════════════════════════════════════════════════
def afiseaza_status() -> None:
    print("\n" + "=" * 60)
    print("Starea Serviciilor Laboratorului Săptămânii 12")
    print("=" * 60)
    for nume, config in SERVICII.items():
        port = config["port"]
        activ = verifica_port(port)
        status = "✓ ACTIV" if activ else "✗ OPRIT"
        culoare = "\033[92m" if activ else "\033[91m"
        print(f"  {culoare}{status}\033[0m  {config['descriere']:20} (port {port})")
    print("=" * 60)

# ═══════════════════════════════════════════════════════════════════════════════
# PARSEAZA_ARGUMENTE
# ═══════════════════════════════════════════════════════════════════════════════
def parseaza_argumente() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pornire Laborator Săptămâna 12")
    parser.add_argument("--status", action="store_true", help="Afișează doar starea")
    parser.add_argument("--rebuild", action="store_true", help="Reconstruiește imaginile")
    return parser.parse_args()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ORCHESTRARE
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    args = parseaza_argumente()
    logger.info("Pornire Mediu de Laborator - Săptămâna 12")
    
    if not verifica_docker_disponibil():
        logger.error("Docker nu este disponibil!")
        return 1
    
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    if args.status:
        afiseaza_status()
        return 0
    
    try:
        if args.rebuild:
            docker.compune_build()
        docker.compune_up(detasat=True)
        
        if not asteapta_servicii(timeout=60):
            logger.error("Unele servicii nu au pornit corect.")
            return 1
        
        logger.info("✓ Mediul de laborator este pregătit!")
        logger.info("  SMTP: localhost:1025 | JSON-RPC: http://localhost:6200")
        logger.info("  XML-RPC: http://localhost:6201 | gRPC: localhost:6251")
        return 0
    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
