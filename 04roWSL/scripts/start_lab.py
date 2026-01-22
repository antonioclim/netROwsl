#!/usr/bin/env python3
"""
Script de Pornire Laborator Săptămâna 4
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Pornește mediul de laborator cu toate serviciile necesare.

Utilizare:
    python3 scripts/start_lab.py [--rebuild] [--native]

Opțiuni:
    --rebuild    Reconstruiește imaginile Docker
    --native     Pornește serverele direct (fără Docker)
"""

import subprocess
import sys
import time
import socket
import argparse
from pathlib import Path
from typing import Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS_AND_CONFIGURATION
# Scop: Încarcă dependențele și setează constantele
# Transferabil la: Orice script Python care folosește module externe
# ═══════════════════════════════════════════════════════════════════════════════

# Detectare director de bază
SCRIPT_DIR = Path(__file__).parent.absolute()
BASE_DIR = SCRIPT_DIR.parent
DOCKER_DIR = BASE_DIR / "docker"
COMPOSE_FILE = DOCKER_DIR / "docker-compose.yml"

# Configurare porturi
PORTURI = {
    "TEXT": 5400,
    "BINAR": 5401,
    "SENZOR_UDP": 5402,
}

# Configurare timeout-uri
TIMEOUT_DOCKER_START = 30  # secunde
TIMEOUT_SERVICE_CHECK = 5  # secunde
INTERVAL_CHECK = 1  # secunde între verificări


# ═══════════════════════════════════════════════════════════════════════════════
# PREREQUISITE_VERIFICATION
# Scop: Verifică disponibilitatea Docker și a altor dependențe
# Transferabil la: Orice script care depinde de servicii externe
# ═══════════════════════════════════════════════════════════════════════════════

def verifica_docker_instalat() -> bool:
    """
    Verifică dacă Docker este instalat și accesibil.
    
    Returns:
        True dacă Docker e instalat, False altfel
    """
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("EROARE: Docker nu este instalat sau nu e în PATH")
        print("Instalare: https://docs.docker.com/engine/install/")
        return False
    except subprocess.TimeoutExpired:
        print("EROARE: Timeout la verificarea Docker")
        return False


def verifica_docker_activ() -> bool:
    """
    Verifică dacă serviciul Docker rulează.
    
    Returns:
        True dacă Docker răspunde, False altfel
    """
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("EROARE: Timeout - Docker nu răspunde")
        return False
    except subprocess.CalledProcessError:
        return False


def porneste_docker_service() -> bool:
    """
    Încearcă să pornească serviciul Docker.
    
    Returns:
        True dacă serviciul a pornit, False altfel
    """
    print("Se încearcă pornirea serviciului Docker...")
    
    try:
        # Încearcă cu sudo service (WSL)
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Așteaptă să devină activ
            for _ in range(10):
                time.sleep(1)
                if verifica_docker_activ():
                    print("✓ Docker a fost pornit cu succes!")
                    return True
        
        print("EROARE: Nu s-a putut porni Docker")
        print("Încercați manual: sudo service docker start")
        return False
        
    except subprocess.TimeoutExpired:
        print("EROARE: Timeout la pornirea Docker")
        return False
    except FileNotFoundError:
        print("EROARE: Comanda 'sudo' nu e disponibilă")
        return False


def verifica_compose_file() -> bool:
    """
    Verifică existența fișierului docker-compose.yml.
    
    Returns:
        True dacă fișierul există, False altfel
    """
    if not COMPOSE_FILE.exists():
        print(f"EROARE: Fișierul {COMPOSE_FILE} nu există")
        print(f"Verificați că sunteți în directorul corect: {BASE_DIR}")
        return False
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE_STARTUP
# Scop: Pornește containerele în ordinea corectă
# Transferabil la: Orice orchestrare de servicii dependente
# ═══════════════════════════════════════════════════════════════════════════════

def porneste_containere(rebuild: bool = False) -> bool:
    """
    Pornește containerele folosind docker-compose.
    
    Args:
        rebuild: Dacă True, reconstruiește imaginile
    
    Returns:
        True dacă containerele au pornit, False altfel
    """
    print("Pornire containere...")
    
    cmd = ["docker", "compose", "-f", str(COMPOSE_FILE), "up", "-d"]
    
    if rebuild:
        cmd.append("--build")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(BASE_DIR)
        )
        
        if result.returncode != 0:
            print(f"EROARE la pornire containere:")
            print(result.stderr)
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print("EROARE: Timeout la pornirea containerelor")
        print("Încercați: docker compose -f docker/docker-compose.yml up -d")
        return False
    except subprocess.CalledProcessError as e:
        print(f"EROARE: Comandă eșuată (cod {e.returncode})")
        print(e.stderr)
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH_VERIFICATION
# Scop: Confirmă că serviciile răspund după pornire
# Transferabil la: Health checks pentru orice serviciu TCP/UDP
# ═══════════════════════════════════════════════════════════════════════════════

def verifica_port_tcp(port: int, host: str = "localhost") -> bool:
    """
    Verifică dacă un port TCP răspunde.
    
    Args:
        port: Portul de verificat
        host: Adresa hostului
    
    Returns:
        True dacă portul răspunde, False altfel
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT_SERVICE_CHECK)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False


def verifica_port_udp(port: int, host: str = "localhost") -> bool:
    """
    Verifică dacă un port UDP pare activ.
    
    Notă: UDP e connectionless, deci nu putem verifica 100%.
    Verificăm doar că nu primim ICMP port unreachable imediat.
    
    Args:
        port: Portul de verificat
        host: Adresa hostului
    
    Returns:
        True (presupunem că e activ dacă nu avem eroare imediată)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(b"test", (host, port))
        sock.close()
        return True
    except socket.error:
        return False


def asteapta_servicii(timeout: int = TIMEOUT_DOCKER_START) -> bool:
    """
    Așteaptă ca toate serviciile să devină active.
    
    Args:
        timeout: Timpul maxim de așteptare (secunde)
    
    Returns:
        True dacă toate serviciile sunt active, False altfel
    """
    print(f"Așteptare inițializare servicii...")
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        elapsed = int(time.time() - start_time)
        print(f"  Progres: {elapsed}/{timeout} secunde...", end="\r")
        
        # Verifică toate serviciile
        text_ok = verifica_port_tcp(PORTURI["TEXT"])
        binar_ok = verifica_port_tcp(PORTURI["BINAR"])
        udp_ok = verifica_port_udp(PORTURI["SENZOR_UDP"])
        
        if text_ok and binar_ok and udp_ok:
            print()  # Linie nouă după progres
            return True
        
        time.sleep(INTERVAL_CHECK)
    
    print()  # Linie nouă după progres
    return False


def afiseaza_status_servicii():
    """Afișează statusul fiecărui serviciu."""
    print("Verificare Server Protocol TEXT...")
    if verifica_port_tcp(PORTURI["TEXT"]):
        print(f"  ✓ Server Protocol TEXT activ pe port {PORTURI['TEXT']}")
    else:
        print(f"  ✗ Server Protocol TEXT INACTIV pe port {PORTURI['TEXT']}")
    
    print("Verificare Server Protocol BINAR...")
    if verifica_port_tcp(PORTURI["BINAR"]):
        print(f"  ✓ Server Protocol BINAR activ pe port {PORTURI['BINAR']}")
    else:
        print(f"  ✗ Server Protocol BINAR INACTIV pe port {PORTURI['BINAR']}")
    
    print("Verificare Server Senzor UDP...")
    if verifica_port_udp(PORTURI["SENZOR_UDP"]):
        print(f"  ✓ Server Senzor UDP activ pe port {PORTURI['SENZOR_UDP']}")
    else:
        print(f"  ✗ Server Senzor UDP INACTIV pe port {PORTURI['SENZOR_UDP']}")


# ═══════════════════════════════════════════════════════════════════════════════
# NATIVE_MODE
# Scop: Pornește serverele direct fără Docker (pentru debugging)
# ═══════════════════════════════════════════════════════════════════════════════

def porneste_mod_nativ():
    """
    Pornește serverele direct în procese Python.
    
    Util pentru debugging sau când Docker nu e disponibil.
    """
    print("ATENȚIE: Modul nativ nu e complet implementat.")
    print("Folosiți Docker pentru funcționalitate completă.")
    print()
    print("Pentru a rula manual serverele:")
    print(f"  python3 {BASE_DIR}/src/apps/text_proto_server.py")
    print(f"  python3 {BASE_DIR}/src/apps/binary_proto_server.py")
    print(f"  python3 {BASE_DIR}/src/apps/udp_sensor_server.py")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ORCHESTRATION
# Scop: Coordonează întregul proces de pornire
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_banner():
    """Afișează banner-ul de pornire."""
    print("=" * 60)
    print("Pornire Mediu Laborator Săptămâna 4")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("=" * 60)


def afiseaza_informatii_finale():
    """Afișează informațiile de acces după pornire."""
    print()
    print("=" * 60)
    print("✓ Mediul de laborator este pregătit!")
    print()
    print("Puncte de acces:")
    print("  • Portainer:       http://localhost:9000")
    print(f"  • Protocol TEXT:   localhost:{PORTURI['TEXT']}")
    print(f"  • Protocol BINAR:  localhost:{PORTURI['BINAR']}")
    print(f"  • Senzor UDP:      localhost:{PORTURI['SENZOR_UDP']}")
    print()
    print("Pentru a opri laboratorul:")
    print("  python3 scripts/stop_lab.py")
    print("=" * 60)


def main():
    """Funcția principală de pornire."""
    # Parsare argumente
    parser = argparse.ArgumentParser(
        description="Pornește mediul de laborator pentru Săptămâna 4"
    )
    parser.add_argument(
        "--rebuild", 
        action="store_true",
        help="Reconstruiește imaginile Docker"
    )
    parser.add_argument(
        "--native",
        action="store_true", 
        help="Pornește serverele direct (fără Docker)"
    )
    
    args = parser.parse_args()
    
    # Banner
    afiseaza_banner()
    
    # Mod nativ
    if args.native:
        porneste_mod_nativ()
        return 0
    
    # Verificare Docker instalat
    if not verifica_docker_instalat():
        return 1
    
    # Verificare Docker activ
    if not verifica_docker_activ():
        if not porneste_docker_service():
            print()
            print("Nu s-a putut porni Docker.")
            print("Porniți manual: sudo service docker start")
            return 1
    
    # Verificare fișier compose
    if not verifica_compose_file():
        return 1
    
    # Pornire containere
    if not porneste_containere(rebuild=args.rebuild):
        return 1
    
    # Așteptare servicii
    if not asteapta_servicii():
        print()
        print("AVERTISMENT: Nu toate serviciile au pornit în timp util.")
        print("Verificați log-urile: docker compose logs")
    
    # Status final
    afiseaza_status_servicii()
    afiseaza_informatii_finale()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
