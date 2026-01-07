#!/usr/bin/env python3
"""
Teste de verificare exerciții
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Teste pentru a verifica că exercițiile de laborator au fost completate corect.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


def test_exercitiul_1() -> bool:
    """
    Testează Exercițiul 1: Configurare NAT/PAT.
    
    Verifică:
    - Topologia NAT poate porni
    - Regula MASQUERADE este configurată
    - Hosturile private pot ajunge la hostul public
    """
    print("Testare Exercițiul 1: Configurare NAT/PAT")
    print("-" * 50)
    
    fisier_topo = RADACINA_PROIECT / "src" / "exercises" / "topo_nat.py"
    
    if not fisier_topo.exists():
        print("  [EȘUAT] Fișierul de topologie nu a fost găsit")
        return False
    
    try:
        rezultat = subprocess.run(
            ["sudo", "python3", str(fisier_topo), "--test"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = rezultat.stdout + rezultat.stderr
        
        # Verifică output-urile așteptate
        verificari = [
            ("Topologia NAT a pornit", "topology" in output.lower() or "nat" in output.lower()),
            ("MASQUERADE prezent", "MASQUERADE" in output or "masquerade" in output.lower()),
            ("Testele au trecut", "PASS" in output or "trecut" in output.lower() or "OK" in output),
        ]
        
        toate_trecute = True
        for nume, trecut in verificari:
            stare = "OK" if trecut else "EȘUAT"
            print(f"  [{stare}] {nume}")
            if not trecut:
                toate_trecute = False
        
        if rezultat.returncode != 0 and toate_trecute:
            print(f"  [AVERT] Cod de ieșire {rezultat.returncode} dar testele au trecut")
        
        return toate_trecute
        
    except subprocess.TimeoutExpired:
        print("  [EȘUAT] Testul a expirat")
        return False
    except FileNotFoundError:
        print("  [EȘUAT] sudo/python3 nu este disponibil")
        return False
    except Exception as e:
        print(f"  [EȘUAT] Eroare: {e}")
        return False


def test_exercitiul_2() -> bool:
    """
    Testează Exercițiul 2: Topologie SDN și Observare Fluxuri.
    
    Verifică:
    - Topologia SDN poate porni
    - Regulile de flux sunt instalate
    - Traficul permis reușește
    - Traficul blocat eșuează
    """
    print("Testare Exercițiul 2: Topologie SDN și Observare Fluxuri")
    print("-" * 50)
    
    fisier_topo = RADACINA_PROIECT / "src" / "exercises" / "topo_sdn.py"
    
    if not fisier_topo.exists():
        print("  [EȘUAT] Fișierul de topologie nu a fost găsit")
        return False
    
    try:
        rezultat = subprocess.run(
            ["sudo", "python3", str(fisier_topo), "--test", "--install-flows"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = rezultat.stdout + rezultat.stderr
        
        # Verifică output-urile așteptate
        verificari = [
            ("Topologia SDN a pornit", "sdn" in output.lower() or "topology" in output.lower()),
            ("Conectivitate h1 ↔ h2 (PERMITE)", "PERMIT" in output or "PERMITE" in output or "0% packet loss" in output),
            ("h1 → h3 blocat (BLOCHEAZĂ)", "DROP" in output or "BLOCHEAZĂ" in output or "100% packet loss" in output),
            ("Tabel fluxuri prezent", "flow" in output.lower() or "flux" in output.lower() or "dump-flows" in output.lower()),
        ]
        
        toate_trecute = True
        for nume, trecut in verificari:
            stare = "OK" if trecut else "EȘUAT"
            print(f"  [{stare}] {nume}")
            if not trecut:
                toate_trecute = False
        
        return toate_trecute
        
    except subprocess.TimeoutExpired:
        print("  [EȘUAT] Testul a expirat")
        return False
    except FileNotFoundError:
        print("  [EȘUAT] sudo/python3 nu este disponibil")
        return False
    except Exception as e:
        print(f"  [EȘUAT] Eroare: {e}")
        return False


def test_exercitiul_3() -> bool:
    """
    Testează Exercițiul 3: Modificare Politici SDN.
    
    Acesta este un exercițiu manual, deci doar verificăm cerințele preliminare.
    """
    print("Testare Exercițiul 3: Modificare Politici SDN (cerințe preliminare)")
    print("-" * 50)
    
    # Verifică dacă ovs-ofctl este disponibil
    try:
        rezultat = subprocess.run(
            ["which", "ovs-ofctl"],
            capture_output=True,
            timeout=5
        )
        ovs_disponibil = rezultat.returncode == 0
    except Exception:
        ovs_disponibil = False
    
    print(f"  [{'OK' if ovs_disponibil else 'EȘUAT'}] ovs-ofctl disponibil")
    
    # Verifică fișierul de topologie
    fisier_topo = RADACINA_PROIECT / "src" / "exercises" / "topo_sdn.py"
    print(f"  [{'OK' if fisier_topo.exists() else 'EȘUAT'}] Fișierul de topologie SDN este prezent")
    
    # Verifică aplicațiile
    tcp_echo = RADACINA_PROIECT / "src" / "apps" / "tcp_echo.py"
    udp_echo = RADACINA_PROIECT / "src" / "apps" / "udp_echo.py"
    print(f"  [{'OK' if tcp_echo.exists() else 'EȘUAT'}] Aplicația echo TCP este prezentă")
    print(f"  [{'OK' if udp_echo.exists() else 'EȘUAT'}] Aplicația echo UDP este prezentă")
    
    print()
    print("  Notă: Exercițiul 3 necesită interacțiune manuală.")
    print("  Rulează: python scripts/run_demo.py --demo sdn")
    
    return ovs_disponibil and fisier_topo.exists()


def main() -> int:
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description="Verifică exercițiile de laborator Săptămâna 6"
    )
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=[1, 2, 3],
        help="Exercițiul specific de testat (1, 2 sau 3)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Rulează toate testele"
    )
    args = parser.parse_args()
    
    print()
    print("=" * 60)
    print("Verificare exerciții Săptămâna 6")
    print("Disciplina REȚELE DE CALCULATOARE - ASE | de Revolvix")
    print("=" * 60)
    print()
    
    teste = {
        1: test_exercitiul_1,
        2: test_exercitiul_2,
        3: test_exercitiul_3,
    }
    
    rezultate = {}
    
    if args.exercise:
        # Rulează testul specific
        functie_test = teste.get(args.exercise)
        if functie_test:
            rezultate[args.exercise] = functie_test()
    elif args.all:
        # Rulează toate testele
        for num, functie_test in teste.items():
            print()
            rezultate[num] = functie_test()
    else:
        print("Utilizare:")
        print("  python tests/test_exercises.py --exercise 1")
        print("  python tests/test_exercises.py --all")
        return 0
    
    # Sumar
    print()
    print("=" * 60)
    print("Sumar:")
    
    toate_trecute = True
    for num, trecut in rezultate.items():
        stare = "OK" if trecut else "EȘUAT"
        print(f"  Exercițiul {num}: [{stare}]")
        if not trecut:
            toate_trecute = False
    
    print("=" * 60)
    
    return 0 if toate_trecute else 1


if __name__ == "__main__":
    sys.exit(main())
