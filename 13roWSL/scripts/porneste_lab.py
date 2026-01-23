#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 13
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

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

# Adaugă rădăcina proiectului în PATH

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.utilitare_retea import verifica_port

logger = configureaza_logger("porneste_lab")

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"

# Definirea serviciilor laboratorului (FĂRĂ Portainer - rulează global)
SERVICII = {
    "mosquitto": {
        "container": "week13_mosquitto",
        "porturi": [1883, 8883],
        "descriere": "Broker MQTT (text clar + TLS)",
        "timp_pornire": 3
    },
    "dvwa": {
        "container": "week13_dvwa",
        "porturi": [8080],
        "descriere": "Aplicație Web Vulnerabilă",
        "timp_pornire": 5
    },
    "vsftpd": {
        "container": "week13_vsftpd",
        "porturi": [2121, 6200],
        "descriere": "Server FTP (cu simulare backdoor)",
        "timp_pornire": 2
    }
}



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def verifica_docker_disponibil() -> bool:
    """Verifică dacă Docker este disponibil și rulează."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def porneste_docker_service() -> bool:
    """Încearcă să pornească serviciul Docker în WSL."""
    logger.info("Se încearcă pornirea serviciului Docker...")
    try:
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            time.sleep(2)
            return verifica_docker_disponibil()
        else:
            logger.error(f"Eroare la pornirea Docker: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("Timeout la pornirea serviciului Docker")
        return False
    except Exception as e:
        logger.error(f"Eroare neașteptată: {e}")
        return False


def verifica_portainer_status() -> bool:
    """Verifică dacă Portainer rulează pe portul 9000."""
    try:
        # Verifică prin docker ps
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and "Up" in result.stdout:
            return True
        
        # Verifică prin socket
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


def afiseaza_avertisment_portainer():
    """Afișează avertisment dacă Portainer nu rulează."""
    print()
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
    print()


def verifica_cerinte_preliminare():
    """Verifică dacă fișierul .env și certificatele există."""
    fisier_env = RADACINA_PROIECT / ".env"
    director_certs = RADACINA_PROIECT / "docker" / "configs" / "certs"
    ca_crt = director_certs / "ca.crt"
    
    if not fisier_env.exists():
        logger.warning("Fișierul .env nu există. Se creează cu valori implicite...")
        # Rulează scriptul de configurare
        subprocess.run([
            sys.executable,
            str(RADACINA_PROIECT / "setup" / "configureaza_docker.py")
        ], cwd=str(RADACINA_PROIECT))
    
    if not ca_crt.exists():
        logger.warning("Certificatele TLS nu există. Se generează...")
        subprocess.run([
            sys.executable,
            str(RADACINA_PROIECT / "setup" / "configureaza_docker.py"),
            "--regen-certs"
        ], cwd=str(RADACINA_PROIECT))


def afiseaza_status(docker: ManagerDocker):
    """Afișează starea curentă a serviciilor."""
    print("\n" + "=" * 60)
    print("STATUS SERVICII LABORATOR - SĂPTĂMÂNA 13")
    print("=" * 60)
    
    containere = docker.listeaza_containere()
    
    for nume, info in SERVICII.items():
        container_gasit = False
        stare = "OPRIT"
        
        for container in containere:
            if info["container"] in container.get("Names", ""):
                container_gasit = True
                stare_container = container.get("State", "unknown")
                stare = "ACTIV" if stare_container == "running" else stare_container.upper()
                break
        
        porturi_str = ", ".join(str(p) for p in info["porturi"])
        simbol = "✓" if stare == "ACTIV" else "✗"
        culoare = "\033[92m" if stare == "ACTIV" else "\033[91m"
        reset = "\033[0m"
        print(f"  {culoare}[{simbol}]{reset} {nume:12} | Porturi: {porturi_str:12} | Stare: {stare}")
        print(f"      {info['descriere']}")
    
    # Afișează status Portainer
    print()
    print("Servicii Globale:")
    print("-" * 60)
    if verifica_portainer_status():
        print(f"  \033[92m[✓]\033[0m Portainer (Management)     | Port: {PORTAINER_PORT} | Stare: ACTIV")
    else:
        print(f"  \033[91m[✗]\033[0m Portainer (Management)     | Port: {PORTAINER_PORT} | Stare: OPRIT")
    
    print("=" * 60)


def verifica_servicii_active():
    """Verifică dacă toate serviciile sunt accesibile."""
    toate_ok = True
    
    logger.info("Verificare conectivitate servicii...")
    
    for nume, info in SERVICII.items():
        for port in info["porturi"]:
            if verifica_port("localhost", port):
                logger.info(f"  [OK] {nume} pe portul {port}")
            else:
                logger.error(f"  [EROARE] {nume} pe portul {port} - nu răspunde")
                toate_ok = False
    
    return toate_ok



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Pornire Laborator Săptămâna 13 - IoT și Securitate"
    )
    parser.add_argument("--status", action="store_true",
                        help="Afișează doar starea serviciilor")
    parser.add_argument("--rebuild", action="store_true",
                        help="Reconstruiește imaginile Docker")
    parser.add_argument("--logs", action="store_true",
                        help="Afișează log-urile după pornire")
    args = parser.parse_args()

    print("=" * 60)
    print("PORNIRE LABORATOR SĂPTĂMÂNA 13")
    print("IoT și Securitate în Rețelele de Calculatoare")
    print("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()

    # Verifică Docker
    logger.info("Verificare disponibilitate Docker...")
    if not verifica_docker_disponibil():
        logger.warning("Docker nu este disponibil. Se încearcă pornirea automată...")
        if not porneste_docker_service():
            logger.error("Nu s-a putut porni Docker!")
            logger.error("Încercați manual: sudo service docker start")
            logger.error("(Parolă: stud)")
            return 1
        logger.info("Docker a fost pornit cu succes!")
    else:
        logger.info("Daemon-ul Docker rulează")

    # Verifică status Portainer (doar avertisment)
    if not verifica_portainer_status():
        afiseaza_avertisment_portainer()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    if args.status:
        afiseaza_status(docker)
        return 0
    
    # Verifică cerințele preliminare
    verifica_cerinte_preliminare()
    
    try:
        # Construiește imaginile dacă este necesar
        if args.rebuild:
            logger.info("Se reconstruiesc imaginile Docker...")
            docker.compose_build()
        
        # Pornește containerele
        logger.info("Se pornesc containerele Docker...")
        docker.compose_up(detach=True)
        
        # Așteaptă inițializarea serviciilor
        logger.info("Se așteaptă inițializarea serviciilor...")
        time.sleep(10)
        
        # Verifică serviciile
        toate_active = verifica_servicii_active()
        
        if toate_active:
            print("\n" + "=" * 60)
            print("✓ MEDIUL DE LABORATOR ESTE PREGĂTIT!")
            print("=" * 60)
            print("\nPuncte de acces:")
            
            # Status Portainer
            if verifica_portainer_status():
                print(f"  • Portainer (Management): {PORTAINER_URL} ✓")
            else:
                print(f"  • Portainer (Management): {PORTAINER_URL} (INACTIV)")
            
            print("  • MQTT (text clar):  localhost:1883")
            print("  • MQTT (TLS):        localhost:8883")
            print("  • DVWA (HTTP):       http://localhost:8080")
            print("  • FTP:               localhost:2121")
            print("  • Backdoor simulat:  localhost:6200")
            print("\nComenzi rapide:")
            print("  python3 src/exercises/ex_13_01_scanner_porturi.py --help")
            print("  python3 src/exercises/ex_13_02_client_mqtt.py --help")
            print("  python3 scripts/ruleaza_demo.py --demo 1")
            print("\nPentru oprire: python3 scripts/opreste_lab.py")
            print("=" * 60)
            
            if args.logs:
                logger.info("\nLog-uri containere:")
                docker.afiseaza_loguri(linii=20)
            
            return 0
        else:
            logger.error("Unele servicii nu au pornit corect.")
            logger.error("Verificați log-urile: docker compose logs")
            return 1
    
    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la pornirea laboratorului: {e}")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
