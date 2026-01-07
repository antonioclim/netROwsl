#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 13
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în PATH
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.utilitare_retea import verifica_port

logger = configureaza_logger("porneste_lab")

# Definirea serviciilor laboratorului
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
    print("STATUS SERVICII LABORATOR")
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
        print(f"  [{simbol}] {nume:12} | Porturi: {porturi_str:12} | Stare: {stare}")
        print(f"      {info['descriere']}")
    
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
    
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    if args.status:
        afiseaza_status(docker)
        return 0
    
    print("=" * 60)
    print("PORNIRE LABORATOR SĂPTĂMÂNA 13")
    print("IoT și Securitate în Rețelele de Calculatoare")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)
    print()
    
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
        time.sleep(8)
        
        # Verifică serviciile
        toate_active = verifica_servicii_active()
        
        if toate_active:
            print("\n" + "=" * 60)
            print("✓ MEDIUL DE LABORATOR ESTE PREGĂTIT!")
            print("=" * 60)
            print("\nPuncte de acces:")
            print("  • MQTT (text clar):  localhost:1883")
            print("  • MQTT (TLS):        localhost:8883")
            print("  • DVWA (HTTP):       http://localhost:8080")
            print("  • FTP:               localhost:2121")
            print("  • Backdoor simulat:  localhost:6200")
            print("\nComenzi rapide:")
            print("  python src/exercises/ex_13_01_scanner_porturi.py --help")
            print("  python src/exercises/ex_13_02_client_mqtt.py --help")
            print("  python scripts/ruleaza_demo.py --demo 1")
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


if __name__ == "__main__":
    sys.exit(main())
