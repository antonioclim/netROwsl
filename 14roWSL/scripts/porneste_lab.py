#!/usr/bin/env python3
"""
Lansator Laborator Săptămâna 14
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent

# Coduri de culoare pentru terminal
class Culori:
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    FINAL = '\033[0m'

def afiseaza_info(mesaj: str) -> None:
    print(f"{Culori.CYAN}[INFO]{Culori.FINAL} {mesaj}")

def afiseaza_succes(mesaj: str) -> None:
    print(f"{Culori.VERDE}[OK]{Culori.FINAL} {mesaj}")

def afiseaza_eroare(mesaj: str) -> None:
    print(f"{Culori.ROSU}[EROARE]{Culori.FINAL} {mesaj}")

def afiseaza_avertisment(mesaj: str) -> None:
    print(f"{Culori.GALBEN}[ATENȚIE]{Culori.FINAL} {mesaj}")

# Configurare servicii
SERVICII = {
    "app1": {"container": "week14_app1", "port": 8001, "timp_pornire": 5},
    "app2": {"container": "week14_app2", "port": 8002, "timp_pornire": 5},
    "lb": {"container": "week14_lb", "port": 8080, "timp_pornire": 10},
    "echo": {"container": "week14_echo", "port": 9000, "timp_pornire": 3},
    "client": {"container": "week14_client", "port": None, "timp_pornire": 2}
}

def verifica_docker_pornit() -> bool:
    """Verifică dacă daemon-ul Docker rulează."""
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=10)
        return result.returncode == 0
    except Exception:
        return False

def construieste_imagini(fara_cache: bool = False) -> bool:
    """Construiește imaginile Docker."""
    afiseaza_info("Se construiesc imaginile Docker...")
    
    cmd = ["docker", "compose", "-f", "docker/docker-compose.yml", "build"]
    if fara_cache:
        cmd.append("--no-cache")
    
    try:
        result = subprocess.run(cmd, cwd=str(RADACINA_PROIECT), timeout=300)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        afiseaza_eroare("Construirea imaginilor a expirat")
        return False
    except Exception as e:
        afiseaza_eroare(f"Eroare la construire: {e}")
        return False

def porneste_containere() -> bool:
    """Pornește containerele cu docker compose."""
    afiseaza_info("Se pornesc containerele...")
    
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", "docker/docker-compose.yml", "up", "-d"],
            cwd=str(RADACINA_PROIECT),
            timeout=120
        )
        return result.returncode == 0
    except Exception as e:
        afiseaza_eroare(f"Eroare la pornirea containerelor: {e}")
        return False

def asteapta_verificari_sanatate(timeout: int = 60) -> bool:
    """Așteaptă ca toate serviciile să devină sănătoase."""
    afiseaza_info("Se așteaptă inițializarea serviciilor...")
    
    timp_inceput = time.time()
    
    while time.time() - timp_inceput < timeout:
        toate_sanatoase = True
        
        for nume, config in SERVICII.items():
            try:
                result = subprocess.run(
                    ["docker", "inspect", "--format", "{{.State.Health.Status}}", config["container"]],
                    capture_output=True, text=True, timeout=5
                )
                
                stare = result.stdout.strip()
                if stare not in ["healthy", ""]:
                    if stare == "starting":
                        toate_sanatoase = False
                elif result.returncode != 0:
                    result2 = subprocess.run(
                        ["docker", "inspect", "--format", "{{.State.Running}}", config["container"]],
                        capture_output=True, text=True, timeout=5
                    )
                    if result2.stdout.strip() != "true":
                        toate_sanatoase = False
            except Exception:
                toate_sanatoase = False
        
        if toate_sanatoase:
            return True
        time.sleep(2)
    
    return False

def afiseaza_stare() -> None:
    """Afișează starea curentă a containerelor."""
    print(f"\n{Culori.BOLD}Starea Containerelor:{Culori.FINAL}")
    print("-" * 50)
    
    for nume, config in SERVICII.items():
        try:
            result = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Status}} {{.State.Health.Status}}", config["container"]],
                capture_output=True, text=True, timeout=5
            )
            
            parti = result.stdout.strip().split()
            stare_rulare = parti[0] if parti else "necunoscut"
            stare_sanatate = parti[1] if len(parti) > 1 else "n/a"
            
            if stare_rulare == "running" and stare_sanatate in ["healthy", "n/a", ""]:
                culoare, simbol = Culori.VERDE, "✓"
            else:
                culoare, simbol = Culori.ROSU, "✗"
            
            port_info = f":{config['port']}" if config['port'] else ""
            print(f"  {culoare}{simbol}{Culori.FINAL} {nume}{port_info} - {stare_rulare} ({stare_sanatate})")
        except Exception as e:
            print(f"  {Culori.ROSU}✗{Culori.FINAL} {nume} - eroare: {e}")

def afiseaza_puncte_acces() -> None:
    """Afișează punctele de acces pentru servicii."""
    print(f"\n{Culori.BOLD}Puncte de Acces:{Culori.FINAL}")
    print("-" * 50)
    print(f"  Load Balancer:    {Culori.CYAN}http://localhost:8080{Culori.FINAL}")
    print(f"  Backend App 1:    {Culori.CYAN}http://localhost:8001{Culori.FINAL}")
    print(f"  Backend App 2:    {Culori.CYAN}http://localhost:8002{Culori.FINAL}")
    print(f"  Server Echo TCP:  {Culori.CYAN}tcp://localhost:9000{Culori.FINAL}")
    print(f"  Portainer:        {Culori.CYAN}https://localhost:9443{Culori.FINAL}")

def main() -> int:
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description="Pornire Laborator Săptămâna 14",
        epilog="Laborator Rețele de Calculatoare - ASE | by Revolvix"
    )
    
    parser.add_argument("--status", "-s", action="store_true", help="Verifică doar starea")
    parser.add_argument("--rebuild", "-r", action="store_true", help="Reconstruiește imaginile")
    parser.add_argument("--attach", "-a", action="store_true", help="Atașează la log-uri")
    
    args = parser.parse_args()
    
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Pornire Mediu Laborator Săptămâna 14{Culori.FINAL}")
    print(f"{Culori.CYAN}Laborator Rețele de Calculatoare - ASE, Informatică Economică{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    
    if args.status:
        afiseaza_stare()
        afiseaza_puncte_acces()
        return 0
    
    afiseaza_info("Se verifică starea Docker...")
    if not verifica_docker_pornit():
        afiseaza_eroare("Daemon-ul Docker nu rulează")
        afiseaza_info("Porniți Docker Desktop și încercați din nou")
        return 1
    afiseaza_succes("Daemon-ul Docker rulează")
    
    if args.rebuild:
        if not construieste_imagini(fara_cache=True):
            afiseaza_eroare("Construirea imaginilor a eșuat")
            return 1
        afiseaza_succes("Imaginile au fost construite")
    
    if not porneste_containere():
        afiseaza_eroare("Pornirea containerelor a eșuat")
        return 1
    afiseaza_succes("Containerele au fost pornite")
    
    if not asteapta_verificari_sanatate():
        afiseaza_avertisment("Unele servicii ar putea să nu fie încă pregătite")
    
    afiseaza_stare()
    afiseaza_puncte_acces()
    
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.VERDE}Mediul de laborator este pregătit!{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    
    if args.attach:
        afiseaza_info("Atașare la log-uri (Ctrl+C pentru oprire)...")
        try:
            subprocess.run(["docker", "compose", "-f", "docker/docker-compose.yml", "logs", "-f"],
                          cwd=str(RADACINA_PROIECT))
        except KeyboardInterrupt:
            print("\nDeconectat de la log-uri")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
