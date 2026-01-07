#!/usr/bin/env python3
"""
Test rapid
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Verificare rapidă de funcționalitate pentru mediul de laborator Săptămâna 6.
Ar trebui să se finalizeze în sub 60 de secunde.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent


def verifica_importuri_python() -> tuple[bool, str]:
    """Verifică dacă modulele Python necesare pot fi importate."""
    necesare = ["socket", "argparse", "subprocess", "pathlib"]
    
    for modul in necesare:
        try:
            __import__(modul)
        except ImportError:
            return False, f"Eșec la importul {modul}"
    
    return True, "Toate modulele necesare sunt disponibile"


def verifica_fisiere_sursa() -> tuple[bool, str]:
    """Verifică dacă fișierele sursă există."""
    fisiere_necesare = [
        "src/exercises/topo_nat.py",
        "src/exercises/topo_sdn.py",
        "src/apps/tcp_echo.py",
        "src/apps/udp_echo.py",
        "src/apps/nat_observer.py",
    ]
    
    lipsa = []
    for cale_rel in fisiere_necesare:
        cale_completa = RADACINA_PROIECT / cale_rel
        if not cale_completa.exists():
            lipsa.append(cale_rel)
    
    if lipsa:
        return False, f"Fișiere lipsă: {', '.join(lipsa)}"
    return True, "Toate fișierele sursă sunt prezente"


def verifica_docker() -> tuple[bool, str]:
    """Verifică disponibilitatea Docker."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if rezultat.returncode == 0:
            return True, "Docker rulează"
        return False, "Docker nu răspunde"
    except FileNotFoundError:
        return False, "Docker nu este instalat"
    except subprocess.TimeoutExpired:
        return False, "Verificarea Docker a expirat"


def verifica_instrumente_retea() -> tuple[bool, str]:
    """Verifică disponibilitatea instrumentelor de rețea."""
    instrumente = {
        "ping": False,
        "ip": False,
    }
    
    for instrument in instrumente:
        try:
            rezultat = subprocess.run(
                ["which", instrument],
                capture_output=True,
                timeout=5
            )
            instrumente[instrument] = rezultat.returncode == 0
        except Exception:
            pass
    
    disponibile = [t for t, ok in instrumente.items() if ok]
    lipsa = [t for t, ok in instrumente.items() if not ok]
    
    if lipsa:
        return False, f"Lipsă: {', '.join(lipsa)}; Disponibile: {', '.join(disponibile)}"
    return True, "Toate instrumentele de rețea sunt disponibile"


def verifica_sintaxa() -> tuple[bool, str]:
    """Verifică sintaxa fișierelor Python."""
    fisiere_python = list((RADACINA_PROIECT / "src").rglob("*.py"))
    fisiere_python += list((RADACINA_PROIECT / "scripts").rglob("*.py"))
    
    erori = []
    for fisier_py in fisiere_python:
        try:
            with open(fisier_py, "r") as f:
                compile(f.read(), fisier_py, "exec")
        except SyntaxError as e:
            erori.append(f"{fisier_py.name}: {e.msg}")
    
    if erori:
        return False, f"Erori de sintaxă: {'; '.join(erori[:3])}"
    return True, f"Toate cele {len(fisiere_python)} fișiere Python au sintaxă validă"


def main() -> int:
    """Rulează testele rapide."""
    print()
    print("=" * 60)
    print("Test rapid Săptămâna 6")
    print("Disciplina REȚELE DE CALCULATOARE - ASE | de Revolvix")
    print("=" * 60)
    print()
    
    timp_start = time.time()
    
    teste = [
        ("Importuri Python", verifica_importuri_python),
        ("Fișiere sursă", verifica_fisiere_sursa),
        ("Docker", verifica_docker),
        ("Instrumente rețea", verifica_instrumente_retea),
        ("Sintaxă Python", verifica_sintaxa),
    ]
    
    rezultate = []
    
    for nume, functie_test in teste:
        try:
            trecut, mesaj = functie_test()
            rezultate.append((nume, trecut, mesaj))
        except Exception as e:
            rezultate.append((nume, False, str(e)))
    
    # Afișează rezultatele
    for nume, trecut, mesaj in rezultate:
        stare = "OK" if trecut else "EȘUAT"
        print(f"  [{stare}] {nume}: {mesaj}")
    
    timp_scurs = time.time() - timp_start
    
    # Sumar
    print()
    print("-" * 60)
    numar_trecute = sum(1 for _, p, _ in rezultate if p)
    numar_total = len(rezultate)
    print(f"Rezultate: {numar_trecute}/{numar_total} trecute în {timp_scurs:.2f}s")
    
    if numar_trecute == numar_total:
        print("✓ Toate testele rapide au trecut!")
        return 0
    else:
        print("✗ Unele teste au eșuat")
        return 1


if __name__ == "__main__":
    sys.exit(main())
