#!/usr/bin/env python3
"""
Runner pentru Doctest-uri – Săptămâna 5
=======================================
Laborator Rețele de Calculatoare – ASE, Informatică Economică

Acest script rulează toate doctest-urile din modulele de utilitate.

Rulare:
    python3 tests/test_doctest.py
    python3 tests/test_doctest.py -v  # verbose
"""

import sys
import doctest
from pathlib import Path

# Adaugă directorul rădăcină la PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))


def ruleaza_doctests(verbose: bool = False) -> bool:
    """
    Rulează toate doctest-urile din modulele de utilitate.
    
    Args:
        verbose: Dacă True, afișează detalii pentru fiecare test
    
    Returns:
        True dacă toate testele au trecut
    """
    from src.utils import net_utils
    
    print("=" * 60)
    print("  Doctest Runner – Săptămâna 5")
    print("=" * 60)
    print()
    
    total_testate = 0
    total_esuate = 0
    
    # Testează net_utils
    print("Testing: src/utils/net_utils.py")
    print("-" * 40)
    
    rezultate = doctest.testmod(
        net_utils,
        verbose=verbose,
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    )
    
    total_testate += rezultate.attempted
    total_esuate += rezultate.failed
    
    if rezultate.failed == 0:
        print(f"  ✓ {rezultate.attempted} doctest-uri au trecut")
    else:
        print(f"  ✗ {rezultate.failed}/{rezultate.attempted} au eșuat")
    
    print()
    print("=" * 60)
    print("  SUMAR")
    print("=" * 60)
    print(f"  Total testate:  {total_testate}")
    print(f"  Total eșuate:   {total_esuate}")
    print()
    
    if total_esuate == 0:
        print("  ✓ TOATE DOCTEST-URILE AU TRECUT!")
        return True
    else:
        print(f"  ✗ {total_esuate} DOCTEST-URI AU EȘUAT")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Rulează doctest-urile")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Afișează detalii pentru fiecare test"
    )
    
    args = parser.parse_args()
    
    succes = ruleaza_doctests(verbose=args.verbose)
    sys.exit(0 if succes else 1)
