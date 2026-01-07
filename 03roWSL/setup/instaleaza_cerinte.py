#!/usr/bin/env python3
"""
Asistent de Instalare Cerințe Preliminare
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Ghidează utilizatorul prin procesul de instalare a componentelor necesare.

Utilizare:
    python setup/instaleaza_cerinte.py
"""

import subprocess
import sys
import shutil
import webbrowser
from pathlib import Path


class AsistentInstalare:
    """Asistent interactiv pentru instalarea cerințelor."""
    
    def __init__(self):
        self.componente_instalate = []
        self.componente_necesare = []
    
    def afiseaza_antet(self) -> None:
        """Afișează antetul asistentului."""
        print("=" * 60)
        print("Asistent de Instalare - Laboratorul Săptămânii 3")
        print("Rețele de Calculatoare - ASE, Informatică Economică")
        print("=" * 60)
        print()
        print("Acest asistent vă va ghida prin instalarea componentelor necesare.")
        print()
    
    def verifica_comanda(self, cmd: str) -> bool:
        """Verifică dacă o comandă este disponibilă."""
        return shutil.which(cmd) is not None
    
    def cere_confirmare(self, mesaj: str) -> bool:
        """Cere confirmarea utilizatorului."""
        while True:
            raspuns = input(f"{mesaj} [d/n]: ").strip().lower()
            if raspuns in ['d', 'da', 'y', 'yes']:
                return True
            elif raspuns in ['n', 'nu', 'no']:
                return False
            print("Vă rugăm răspundeți cu 'd' pentru da sau 'n' pentru nu.")
    
    def deschide_url(self, url: str) -> None:
        """Deschide un URL în browser-ul implicit."""
        try:
            webbrowser.open(url)
            print(f"  → S-a deschis: {url}")
        except Exception as e:
            print(f"  → Deschideți manual: {url}")
    
    def instaleaza_docker(self) -> bool:
        """Ghidează instalarea Docker Desktop."""
        print("\n" + "-" * 40)
        print("DOCKER DESKTOP")
        print("-" * 40)
        
        if self.verifica_comanda("docker"):
            print("✓ Docker este deja instalat.")
            return True
        
        print("Docker Desktop este necesar pentru rularea containerelor de laborator.")
        print()
        print("Pași de instalare:")
        print("1. Descărcați Docker Desktop de la docker.com")
        print("2. Rulați instalatorul și urmați instrucțiunile")
        print("3. Activați integrarea WSL2 în setări")
        print("4. Reporniți computerul dacă este necesar")
        print()
        
        if self.cere_confirmare("Doriți să deschid pagina de descărcare Docker?"):
            self.deschide_url("https://www.docker.com/products/docker-desktop/")
        
        input("\nApăsați Enter după ce ați instalat Docker Desktop...")
        
        if self.verifica_comanda("docker"):
            print("✓ Docker instalat cu succes!")
            self.componente_instalate.append("Docker")
            return True
        else:
            print("✗ Docker nu a fost detectat. Încercați din nou mai târziu.")
            self.componente_necesare.append("Docker")
            return False
    
    def instaleaza_wsl2(self) -> bool:
        """Ghidează activarea WSL2."""
        print("\n" + "-" * 40)
        print("WSL2 (Windows Subsystem for Linux)")
        print("-" * 40)
        
        try:
            rezultat = subprocess.run(["wsl", "--status"], capture_output=True, timeout=10)
            output = rezultat.stdout.decode() + rezultat.stderr.decode()
            if "WSL 2" in output or "Default Version: 2" in output:
                print("✓ WSL2 este deja activat.")
                return True
        except Exception:
            pass
        
        print("WSL2 este necesar pentru backend-ul Docker.")
        print()
        print("Pentru activare, rulați în PowerShell ca Administrator:")
        print()
        print("  wsl --install")
        print()
        print("Apoi reporniți computerul.")
        print()
        
        if self.cere_confirmare("Doriți să deschid documentația Microsoft pentru WSL2?"):
            self.deschide_url("https://docs.microsoft.com/en-us/windows/wsl/install")
        
        return False
    
    def instaleaza_wireshark(self) -> bool:
        """Ghidează instalarea Wireshark."""
        print("\n" + "-" * 40)
        print("WIRESHARK")
        print("-" * 40)
        
        cale_wireshark = Path(r"C:\Program Files\Wireshark\Wireshark.exe")
        if cale_wireshark.exists() or self.verifica_comanda("wireshark"):
            print("✓ Wireshark este deja instalat.")
            return True
        
        print("Wireshark este necesar pentru analiza pachetelor de rețea.")
        print()
        print("Pași de instalare:")
        print("1. Descărcați Wireshark de la wireshark.org")
        print("2. Rulați instalatorul")
        print("3. Includeți Npcap în instalare (necesar pentru captură)")
        print()
        
        if self.cere_confirmare("Doriți să deschid pagina de descărcare Wireshark?"):
            self.deschide_url("https://www.wireshark.org/download.html")
        
        input("\nApăsați Enter după ce ați instalat Wireshark...")
        
        if cale_wireshark.exists():
            print("✓ Wireshark instalat cu succes!")
            self.componente_instalate.append("Wireshark")
            return True
        else:
            print("  Wireshark nu a fost detectat în locația standard.")
            self.componente_necesare.append("Wireshark")
            return False
    
    def instaleaza_pachete_python(self) -> bool:
        """Instalează pachetele Python necesare."""
        print("\n" + "-" * 40)
        print("PACHETE PYTHON")
        print("-" * 40)
        
        pachete = ["pyyaml", "requests"]
        pachete_lipsa = []
        
        for pachet in pachete:
            try:
                nume_import = "yaml" if pachet == "pyyaml" else pachet
                __import__(nume_import)
                print(f"  ✓ {pachet} - instalat")
            except ImportError:
                print(f"  ✗ {pachet} - lipsă")
                pachete_lipsa.append(pachet)
        
        if not pachete_lipsa:
            print("\n✓ Toate pachetele Python sunt instalate.")
            return True
        
        print(f"\nLipsesc: {', '.join(pachete_lipsa)}")
        
        if self.cere_confirmare("Doriți să instalez pachetele lipsă automat?"):
            for pachet in pachete_lipsa:
                print(f"\nInstalez {pachet}...")
                try:
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", pachet],
                        check=True
                    )
                    print(f"  ✓ {pachet} instalat cu succes")
                    self.componente_instalate.append(f"Python: {pachet}")
                except subprocess.CalledProcessError:
                    print(f"  ✗ Eroare la instalarea {pachet}")
                    self.componente_necesare.append(f"Python: {pachet}")
        
        return len(pachete_lipsa) == 0
    
    def afiseaza_sumar(self) -> None:
        """Afișează sumarul instalării."""
        print("\n" + "=" * 60)
        print("SUMAR INSTALARE")
        print("=" * 60)
        
        if self.componente_instalate:
            print("\n✓ Componente instalate în această sesiune:")
            for comp in self.componente_instalate:
                print(f"  - {comp}")
        
        if self.componente_necesare:
            print("\n✗ Componente care necesită atenție:")
            for comp in self.componente_necesare:
                print(f"  - {comp}")
            print("\nVă rugăm să instalați componentele lipsă și să rulați din nou verificarea.")
        else:
            print("\n✓ Toate componentele sunt instalate!")
            print("  Rulați: python setup/verifica_mediu.py")
            print("  pentru a confirma că totul este pregătit.")
    
    def ruleaza(self) -> int:
        """Rulează asistentul de instalare."""
        self.afiseaza_antet()
        
        self.instaleaza_wsl2()
        self.instaleaza_docker()
        self.instaleaza_wireshark()
        self.instaleaza_pachete_python()
        
        self.afiseaza_sumar()
        
        return 0 if not self.componente_necesare else 1


def main():
    """Punctul principal de intrare."""
    asistent = AsistentInstalare()
    return asistent.ruleaza()


if __name__ == "__main__":
    sys.exit(main())
