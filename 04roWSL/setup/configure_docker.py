#!/usr/bin/env python3
"""
Asistent Configurare Docker
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Verifică și ajută la configurarea Docker Desktop pentru laborator.
"""

import subprocess
import sys
import json
from pathlib import Path


def print_antet(titlu: str):
    """Afișează un antet formatat."""
    print("\n" + "=" * 60)
    print(f"  {titlu}")
    print("=" * 60)


def print_ok(mesaj: str):
    """Afișează un mesaj de succes."""
    print(f"  [\033[92mOK\033[0m] {mesaj}")


def print_eroare(mesaj: str):
    """Afișează un mesaj de eroare."""
    print(f"  [\033[91mEROARE\033[0m] {mesaj}")


def print_atentie(mesaj: str):
    """Afișează un avertisment."""
    print(f"  [\033[93mATENȚIE\033[0m] {mesaj}")


def print_info(mesaj: str):
    """Afișează un mesaj informativ."""
    print(f"  ℹ️  {mesaj}")


def verifica_docker_instalat() -> bool:
    """Verifică dacă Docker este instalat."""
    try:
        rezultat = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=5
        )
        if rezultat.returncode == 0:
            versiune = rezultat.stdout.decode().strip()
            print_ok(f"Docker instalat: {versiune}")
            return True
        return False
    except Exception:
        print_eroare("Docker nu este instalat sau nu este în PATH")
        return False


def verifica_docker_activ() -> bool:
    """Verifică dacă daemon-ul Docker rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if rezultat.returncode == 0:
            print_ok("Daemon-ul Docker rulează")
            return True
        else:
            print_eroare("Daemon-ul Docker nu rulează")
            print_info("Porniți Docker Desktop din meniul Start")
            return False
    except Exception as e:
        print_eroare(f"Nu se poate contacta daemon-ul Docker: {e}")
        return False


def verifica_backend_wsl2() -> bool:
    """Verifică dacă Docker folosește backend-ul WSL2."""
    try:
        rezultat = subprocess.run(
            ["docker", "info", "--format", "{{.OSType}}"],
            capture_output=True,
            timeout=10
        )
        tip_os = rezultat.stdout.decode().strip()
        
        if tip_os == "linux":
            # Verifică dacă e WSL2
            rezultat_info = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10
            )
            info = rezultat_info.stdout.decode()
            
            if "WSL" in info or "wsl" in info.lower():
                print_ok("Backend WSL2 detectat")
                return True
            else:
                print_ok("Backend Linux detectat (probabil WSL2)")
                return True
        else:
            print_atentie(f"Tip OS detectat: {tip_os}")
            return True
    except Exception as e:
        print_atentie(f"Nu se poate verifica backend-ul: {e}")
        return True


def verifica_resurse() -> dict:
    """Verifică resursele alocate Docker."""
    resurse = {
        "memorie_gb": 0,
        "cpus": 0
    }
    
    try:
        rezultat = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            timeout=10
        )
        
        if rezultat.returncode == 0:
            info = json.loads(rezultat.stdout.decode())
            
            # Memorie
            if "MemTotal" in info:
                memorie_bytes = info["MemTotal"]
                memorie_gb = memorie_bytes / (1024 ** 3)
                resurse["memorie_gb"] = memorie_gb
                
                if memorie_gb >= 4:
                    print_ok(f"Memorie disponibilă: {memorie_gb:.1f} GB")
                else:
                    print_atentie(f"Memorie disponibilă: {memorie_gb:.1f} GB (recomandat: 4+ GB)")
            
            # CPUs
            if "NCPU" in info:
                cpus = info["NCPU"]
                resurse["cpus"] = cpus
                
                if cpus >= 2:
                    print_ok(f"CPUs disponibile: {cpus}")
                else:
                    print_atentie(f"CPUs disponibile: {cpus} (recomandat: 2+)")
                    
    except Exception as e:
        print_atentie(f"Nu se pot verifica resursele: {e}")
    
    return resurse


def verifica_retea_docker() -> bool:
    """Verifică dacă rețeaua Docker poate fi creată."""
    try:
        # Încearcă să creeze o rețea de test
        rezultat = subprocess.run(
            ["docker", "network", "create", "--driver", "bridge", "test_week4_net"],
            capture_output=True,
            timeout=10
        )
        
        if rezultat.returncode == 0:
            # Șterge rețeaua de test
            subprocess.run(
                ["docker", "network", "rm", "test_week4_net"],
                capture_output=True,
                timeout=5
            )
            print_ok("Creare rețea Docker funcționează")
            return True
        else:
            eroare = rezultat.stderr.decode()
            if "already exists" in eroare:
                # Rețeaua există deja, șterge-o
                subprocess.run(
                    ["docker", "network", "rm", "test_week4_net"],
                    capture_output=True,
                    timeout=5
                )
                print_ok("Creare rețea Docker funcționează")
                return True
            print_eroare(f"Nu se poate crea rețea Docker: {eroare}")
            return False
    except Exception as e:
        print_eroare(f"Eroare la testarea rețelei: {e}")
        return False


def verifica_docker_compose() -> bool:
    """Verifică dacă Docker Compose este disponibil."""
    try:
        rezultat = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=5
        )
        
        if rezultat.returncode == 0:
            versiune = rezultat.stdout.decode().strip()
            print_ok(f"Docker Compose: {versiune}")
            return True
        else:
            print_eroare("Docker Compose nu este disponibil")
            return False
    except Exception as e:
        print_eroare(f"Eroare la verificarea Docker Compose: {e}")
        return False


def afiseaza_setari_recomandate():
    """Afișează setările recomandate pentru Docker Desktop."""
    print_antet("SETĂRI RECOMANDATE")
    
    print("\n  \033[1mDocker Desktop → Settings:\033[0m")
    print()
    print("  📌 General:")
    print("     ✓ Start Docker Desktop when you log in")
    print("     ✓ Use the WSL 2 based engine")
    print()
    print("  📌 Resources → WSL Integration:")
    print("     ✓ Enable integration with my default WSL distro")
    print("     ✓ Enable integration with additional distros (Ubuntu)")
    print()
    print("  📌 Resources → Advanced (dacă disponibil):")
    print("     • CPUs: 2 sau mai multe")
    print("     • Memory: 4 GB sau mai mult")
    print("     • Disk image size: 60 GB sau mai mult")
    print()
    print("  📌 Docker Engine:")
    print("     Configurație JSON implicită este suficientă pentru laborator")


def verifica_fisier_compose():
    """Verifică dacă fișierul docker-compose.yml există."""
    radacina = Path(__file__).parent.parent
    cale_compose = radacina / "docker" / "docker-compose.yml"
    
    if cale_compose.exists():
        print_ok(f"Fișier docker-compose.yml găsit")
        
        # Verifică sintaxa YAML
        try:
            import yaml
            with open(cale_compose, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print_ok("Sintaxa YAML validă")
            return True
        except ImportError:
            print_info("Modulul yaml nu este instalat, nu se poate valida sintaxa")
            return True
        except Exception as e:
            print_eroare(f"Eroare sintaxă YAML: {e}")
            return False
    else:
        print_eroare(f"Fișierul docker-compose.yml nu a fost găsit la {cale_compose}")
        return False


def main():
    """Funcția principală."""
    print("\n" + "=" * 60)
    print("  ASISTENT CONFIGURARE DOCKER")
    print("  Laborator Săptămâna 4 - Rețele de Calculatoare")
    print("  ASE București - Informatică Economică")
    print("=" * 60)
    
    toate_ok = True
    
    # Verificări
    print_antet("VERIFICĂRI DOCKER")
    
    if not verifica_docker_instalat():
        toate_ok = False
        print_info("Instalați Docker Desktop de pe https://docker.com")
        return 1
    
    if not verifica_docker_activ():
        toate_ok = False
        print_info("Porniți Docker Desktop și așteptați inițializarea")
        return 1
    
    verifica_backend_wsl2()
    verifica_resurse()
    
    if not verifica_docker_compose():
        toate_ok = False
    
    if not verifica_retea_docker():
        toate_ok = False
    
    # Verificare fișier compose
    print_antet("VERIFICARE FIȘIERE PROIECT")
    if not verifica_fisier_compose():
        toate_ok = False
    
    # Setări recomandate
    afiseaza_setari_recomandate()
    
    # Sumar
    print_antet("REZULTAT")
    if toate_ok:
        print("\n  \033[92m✓ Docker este configurat corect pentru laborator!\033[0m")
        print("\n  Puteți porni laboratorul cu:")
        print("    python scripts/start_lab.py")
    else:
        print("\n  \033[91m✗ Unele verificări au eșuat.\033[0m")
        print("  Verificați erorile de mai sus și încercați din nou.")
    
    return 0 if toate_ok else 1


if __name__ == "__main__":
    sys.exit(main())
