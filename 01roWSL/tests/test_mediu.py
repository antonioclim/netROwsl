#!/usr/bin/env python3
"""
Teste de Validare a Mediului
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verifică dacă mediul de laborator este configurat corect.
"""

from __future__ import annotations

import subprocess
import sys
import socket
from pathlib import Path
from typing import Callable, List, Tuple

# Adaugă directorul rădăcină la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


class RulatoareTeste:
    """Clasă pentru rularea și raportarea testelor."""
    
    def __init__(self) -> None:
        self.rezultate: List[Tuple[str, bool, str]] = []
    
    def test(self, nume: str, conditie: bool, detalii: str = "") -> None:
        """Înregistrează rezultatul unui test.
        
        Args:
            nume: Numele testului
            conditie: True dacă testul a trecut
            detalii: Detalii suplimentare
        """
        self.rezultate.append((nume, conditie, detalii))
        
        simbol = "✓" if conditie else "✗"
        culoare = "\033[92m" if conditie else "\033[91m"
        reset = "\033[0m"
        
        print(f"  {culoare}{simbol}{reset} {nume}")
        if detalii and not conditie:
            print(f"      {detalii}")
    
    def sumar(self) -> int:
        """Afișează sumarul și returnează codul de ieșire."""
        total = len(self.rezultate)
        trecute = sum(1 for _, ok, _ in self.rezultate if ok)
        esuate = total - trecute
        
        print()
        print("=" * 60)
        print(f"REZULTATE: {trecute}/{total} teste trecute")
        
        if esuate == 0:
            print("\033[92m✓ Toate testele au trecut!\033[0m")
            return 0
        else:
            print(f"\033[91m✗ {esuate} teste eșuate\033[0m")
            return 1


def verifica_versiune_python() -> Tuple[bool, str]:
    """Verifică versiunea Python."""
    versiune = sys.version_info
    ok = versiune >= (3, 11)
    detalii = f"Python {versiune.major}.{versiune.minor}.{versiune.micro}"
    return ok, detalii


def verifica_pachet(nume: str) -> Tuple[bool, str]:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume)
        return True, f"{nume} instalat"
    except ImportError:
        return False, f"{nume} lipsește - pip install {nume}"


def verifica_docker_instalat() -> Tuple[bool, str]:
    """Verifică dacă Docker este instalat."""
    try:
        rezultat = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0:
            return True, rezultat.stdout.strip()
        return False, "Docker nu este instalat"
    except Exception as e:
        return False, str(e)


def verifica_docker_ruleaza() -> Tuple[bool, str]:
    """Verifică dacă Docker daemon-ul rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if rezultat.returncode == 0:
            return True, "Docker daemon activ"
        return False, "Docker daemon nu rulează"
    except Exception as e:
        return False, str(e)


def verifica_structura_proiect() -> Tuple[bool, str]:
    """Verifică structura directoarelor proiectului."""
    directoare_necesare = [
        "docker",
        "scripts",
        "src/exercises",
        "tests",
        "docs",
        "homework",
        "pcap",
        "artifacts",
    ]
    
    lipsa = []
    for d in directoare_necesare:
        if not (RADACINA_PROIECT / d).exists():
            lipsa.append(d)
    
    if lipsa:
        return False, f"Directoare lipsă: {', '.join(lipsa)}"
    return True, "Structură completă"


def verifica_fisier_compose() -> Tuple[bool, str]:
    """Verifică existența și validitatea docker-compose.yml."""
    cale = RADACINA_PROIECT / "docker" / "docker-compose.yml"
    
    if not cale.exists():
        return False, "Fișier docker-compose.yml lipsește"
    
    try:
        import yaml
        with open(cale, "r") as f:
            config = yaml.safe_load(f)
        
        if "services" in config:
            return True, f"Valid cu {len(config['services'])} servicii"
        return False, "Secțiune 'services' lipsește"
    except Exception as e:
        return False, f"Eroare parsare YAML: {e}"


def verifica_conectivitate_loopback() -> Tuple[bool, str]:
    """Verifică conectivitatea loopback."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.bind(("127.0.0.1", 0))
            return True, "Loopback funcțional"
    except Exception as e:
        return False, str(e)


def main() -> int:
    """Funcția principală."""
    print()
    print("=" * 60)
    print("  TESTE DE VALIDARE A MEDIULUI - SĂPTĂMÂNA 1")
    print("  Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)
    print()

    t = RulatoareTeste()

    # Teste Python
    print("MEDIU PYTHON:")
    ok, detalii = verifica_versiune_python()
    t.test("Versiune Python >= 3.11", ok, detalii)
    
    for pachet in ["docker", "requests", "yaml"]:
        ok, detalii = verifica_pachet(pachet)
        t.test(f"Pachet {pachet}", ok, detalii)
    
    # Teste Docker
    print("\nMEDIU DOCKER:")
    ok, detalii = verifica_docker_instalat()
    t.test("Docker instalat", ok, detalii)
    
    ok, detalii = verifica_docker_ruleaza()
    t.test("Docker daemon activ", ok, detalii)
    
    # Teste structură proiect
    print("\nSTRUCTURĂ PROIECT:")
    ok, detalii = verifica_structura_proiect()
    t.test("Directoare necesare", ok, detalii)
    
    ok, detalii = verifica_fisier_compose()
    t.test("Docker Compose valid", ok, detalii)
    
    # Teste conectivitate
    print("\nCONECTIVITATE:")
    ok, detalii = verifica_conectivitate_loopback()
    t.test("Loopback", ok, detalii)

    return t.sumar()


if __name__ == "__main__":
    sys.exit(main())
