#!/usr/bin/env python3
"""
Script Instalare Cerințe Preliminare
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Ghidează utilizatorul prin instalarea componentelor necesare.
"""

import subprocess
import sys
import webbrowser
from pathlib import Path


def afiseaza_titlu(titlu: str) -> None:
    """Afișează un titlu formatat."""
    print()
    print("=" * 50)
    print(titlu.center(50))
    print("=" * 50)
    print()


def intreaba_utilizator(mesaj: str, implicit: bool = True) -> bool:
    """
    Pune o întrebare da/nu utilizatorului.
    
    Argumente:
        mesaj: Întrebarea de afișat
        implicit: Răspunsul implicit
        
    Returnează:
        True pentru da, False pentru nu
    """
    sufix = " [D/n]: " if implicit else " [d/N]: "
    raspuns = input(mesaj + sufix).strip().lower()
    
    if not raspuns:
        return implicit
    
    return raspuns in ['d', 'da', 'y', 'yes']


def deschide_url(url: str, descriere: str) -> None:
    """
    Deschide un URL în browser.
    
    Argumente:
        url: Adresa URL
        descriere: Descrierea resursei
    """
    print(f"\n  Se deschide {descriere}...")
    print(f"  URL: {url}")
    webbrowser.open(url)
    input("  Apăsați Enter după ce ați terminat descărcarea...")


def verifica_instalare(comanda: str) -> bool:
    """Verifică dacă o comandă este disponibilă."""
    import shutil
    return shutil.which(comanda) is not None


def instaleaza_pachete_python() -> bool:
    """Instalează pachetele Python necesare."""
    print("\n  Se instalează pachetele Python...")
    
    fisier_cerinte = Path(__file__).parent / "requirements.txt"
    
    if not fisier_cerinte.exists():
        print("  Fișierul requirements.txt nu a fost găsit.")
        return False
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(fisier_cerinte)],
            check=True
        )
        print("  ✓ Pachetele au fost instalate cu succes!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Eroare la instalare: {e}")
        return False


def main():
    """Funcția principală."""
    afiseaza_titlu("Instalare Cerințe Preliminare")
    
    print("Acest script vă va ghida prin instalarea componentelor")
    print("necesare pentru laboratorul Săptămânii 9.")
    print()
    print("Componente necesare:")
    print("  1. Docker Desktop")
    print("  2. WSL2 (Windows Subsystem for Linux)")
    print("  3. Wireshark")
    print("  4. Python 3.8+ cu pachete necesare")
    print()
    
    if not intreaba_utilizator("Doriți să continuați?"):
        print("\nInstalare anulată.")
        return 0

    # 1. Docker Desktop
    afiseaza_titlu("1. Docker Desktop")
    
    if verifica_instalare("docker"):
        print("  ✓ Docker este deja instalat!")
    else:
        print("  Docker Desktop nu a fost detectat.")
        if intreaba_utilizator("Doriți să deschideți pagina de descărcare?"):
            deschide_url(
                "https://www.docker.com/products/docker-desktop",
                "Docker Desktop"
            )

    # 2. WSL2
    afiseaza_titlu("2. WSL2")
    
    print("  Pentru a activa WSL2, rulați în PowerShell (ca Administrator):")
    print()
    print("    wsl --install")
    print()
    print("  Apoi reporniți calculatorul.")
    print()
    
    if intreaba_utilizator("Doriți să vedeți documentația Microsoft?", implicit=False):
        deschide_url(
            "https://docs.microsoft.com/en-us/windows/wsl/install",
            "Documentația WSL2"
        )

    # 3. Wireshark
    afiseaza_titlu("3. Wireshark")
    
    wireshark_gasit = (
        Path(r"C:\Program Files\Wireshark\Wireshark.exe").exists() or
        verifica_instalare("wireshark")
    )
    
    if wireshark_gasit:
        print("  ✓ Wireshark este deja instalat!")
    else:
        print("  Wireshark nu a fost detectat.")
        if intreaba_utilizator("Doriți să deschideți pagina de descărcare?"):
            deschide_url(
                "https://www.wireshark.org/download.html",
                "Wireshark"
            )

    # 4. Pachete Python
    afiseaza_titlu("4. Pachete Python")
    
    print(f"  Versiune Python: {sys.version}")
    print()
    
    if intreaba_utilizator("Doriți să instalați pachetele Python necesare?"):
        instaleaza_pachete_python()

    # Sumar final
    afiseaza_titlu("Instalare Finalizată")
    
    print("Pași următori:")
    print()
    print("  1. Asigurați-vă că Docker Desktop rulează")
    print("  2. Verificați mediul:")
    print("       python setup/verifica_mediu.py")
    print()
    print("  3. Porniți laboratorul:")
    print("       python scripts/porneste_lab.py")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
