#!/usr/bin/env python3
"""
Script de Verificare Calitate – Săptămâna 5
===========================================
Laborator Rețele de Calculatoare – ASE, Informatică Economică

Verifică automat:
- AI Fingerprints (cuvinte-semnal tipice AI)
- Structura fișierelor obligatorii
- Doctest-uri
- Teste unitare

Rulare:
    python3 scripts/verifica_calitate.py
    python3 scripts/verifica_calitate.py --verbose
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Directorul rădăcină al proiectului
ROOT_DIR = Path(__file__).resolve().parent.parent

# Cuvinte-semnal AI de căutat
AI_FINGERPRINTS = [
    "în această secțiune",
    "vom explora",
    "cauze comune",
    "în practică vei",
    "hai să",
    "vom învăța",
    "vom discuta",
    "este important de menționat",
    "merită menționat că",
    "în concluzie",
    "pe scurt",
    "în esență",
]

# Fișiere obligatorii
FISIERE_OBLIGATORII = [
    "README.md",
    "docs/GLOSSARY.md",
    "docs/rezumat_teorie.md",
    "docs/fisa_comenzi.md",
    "docs/depanare.md",
    "docs/peer_instruction.md",
    "docs/exercitii_perechi.md",
    "docs/exercitii_trace.md",
    "src/utils/net_utils.py",
    "src/exercises/ex_5_01_cidr_flsm.py",
    "src/exercises/ex_5_02_vlsm_ipv6.py",
    "tests/test_exercitii.py",
    "tests/test_doctest.py",
    "docker/docker-compose.yml",
]


def print_header(titlu: str):
    """Afișează un header formatat."""
    print()
    print("═" * 60)
    print(f"  {titlu}")
    print("═" * 60)


def print_result(test_name: str, passed: bool, details: str = ""):
    """Afișează rezultatul unui test."""
    status = "✓" if passed else "✗"
    color_start = "\033[92m" if passed else "\033[91m"
    color_end = "\033[0m"
    
    result_text = f"{color_start}{status}{color_end} {test_name}"
    if details:
        result_text += f" - {details}"
    print(result_text)


def verifica_ai_fingerprints(verbose: bool = False) -> Tuple[bool, List[str]]:
    """
    Verifică dacă există cuvinte-semnal AI în documentație.
    
    Returns:
        (passed, list_of_findings)
    """
    findings = []
    
    # Directoare de scanat
    dirs_to_scan = [
        ROOT_DIR / "docs",
        ROOT_DIR / "README.md",
    ]
    
    for path in dirs_to_scan:
        if path.is_file():
            files = [path]
        elif path.is_dir():
            files = list(path.glob("**/*.md"))
        else:
            continue
        
        for file_path in files:
            try:
                content = file_path.read_text(encoding='utf-8').lower()
                for pattern in AI_FINGERPRINTS:
                    if pattern.lower() in content:
                        rel_path = file_path.relative_to(ROOT_DIR)
                        findings.append(f"{rel_path}: '{pattern}'")
            except Exception as e:
                if verbose:
                    print(f"  Eroare la citirea {file_path}: {e}")
    
    return len(findings) == 0, findings


def verifica_structura(verbose: bool = False) -> Tuple[bool, List[str]]:
    """
    Verifică existența fișierelor obligatorii.
    
    Returns:
        (passed, list_of_missing)
    """
    missing = []
    
    for fisier in FISIERE_OBLIGATORII:
        path = ROOT_DIR / fisier
        if not path.exists():
            missing.append(fisier)
    
    return len(missing) == 0, missing


def verifica_doctest(verbose: bool = False) -> Tuple[bool, str]:
    """
    Rulează doctest-urile și returnează rezultatul.
    
    Returns:
        (passed, output)
    """
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT_DIR / "tests" / "test_doctest.py")],
            capture_output=True,
            text=True,
            cwd=str(ROOT_DIR),
            timeout=60
        )
        
        passed = result.returncode == 0
        output = result.stdout if passed else result.stderr
        
        return passed, output.strip()
    except subprocess.TimeoutExpired:
        return False, "Timeout la rularea doctest-urilor"
    except Exception as e:
        return False, f"Eroare: {e}"


def verifica_teste(verbose: bool = False) -> Tuple[bool, str]:
    """
    Rulează testele unitare și returnează rezultatul.
    
    Returns:
        (passed, output)
    """
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT_DIR / "tests" / "test_exercitii.py")],
            capture_output=True,
            text=True,
            cwd=str(ROOT_DIR),
            timeout=120
        )
        
        passed = result.returncode == 0
        
        # Extrage ultima linie cu rezultatul
        lines = result.stdout.strip().split('\n')
        summary = lines[-1] if lines else "No output"
        
        return passed, summary
    except subprocess.TimeoutExpired:
        return False, "Timeout la rularea testelor"
    except Exception as e:
        return False, f"Eroare: {e}"


def main():
    """Funcția principală de verificare."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Verifică calitatea materialelor Săptămâna 5"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Afișează detalii suplimentare"
    )
    
    args = parser.parse_args()
    verbose = args.verbose
    
    print_header("Verificare Calitate Materiale Săptămâna 5")
    
    results = {}
    
    # 1. Verifică AI Fingerprints
    print("\n[1/4] Verificare AI Fingerprints...")
    passed, findings = verifica_ai_fingerprints(verbose)
    results['AI Fingerprints'] = passed
    
    if passed:
        print_result("AI Fingerprints", True, "CURAT")
    else:
        print_result("AI Fingerprints", False, f"{len(findings)} găsite")
        if verbose:
            for finding in findings:
                print(f"      - {finding}")
    
    # 2. Verifică structura
    print("\n[2/4] Verificare structură fișiere...")
    passed, missing = verifica_structura(verbose)
    results['Structură'] = passed
    
    if passed:
        print_result("Structură", True, "COMPLETĂ")
    else:
        print_result("Structură", False, f"{len(missing)} lipsă")
        if verbose:
            for m in missing:
                print(f"      - {m}")
    
    # 3. Verifică doctest-uri
    print("\n[3/4] Verificare doctest-uri...")
    passed, output = verifica_doctest(verbose)
    results['Doctest'] = passed
    
    if passed:
        print_result("Doctest", True, "PASSED")
    else:
        print_result("Doctest", False, "FAILED")
        if verbose:
            print(f"      {output}")
    
    # 4. Verifică teste unitare
    print("\n[4/4] Verificare teste unitare...")
    passed, output = verifica_teste(verbose)
    results['Teste'] = passed
    
    if passed:
        print_result("Teste", True, "PASSED")
    else:
        print_result("Teste", False, "FAILED")
        if verbose:
            print(f"      {output}")
    
    # Sumar
    print_header("SUMAR")
    
    all_passed = True
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name:20} {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("  " + "=" * 40)
        print("  ✓ TOATE VERIFICĂRILE AU TRECUT!")
        print("  " + "=" * 40)
    else:
        print("  " + "=" * 40)
        print("  ✗ UNELE VERIFICĂRI AU EȘUAT")
        print("  " + "=" * 40)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
