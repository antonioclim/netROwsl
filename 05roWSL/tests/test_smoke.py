#!/usr/bin/env python3
"""
Test Smoke Rapid - Săptămâna 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Verificare rapidă a funcționalității de bază (< 60 secunde).
"""

import sys
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


def test_import_module():
    """Verifică importul modulelor principale."""
    print("  ○ Import module...", end=" ")
    try:
        from src.utils.net_utils import (
            analizeaza_interfata_ipv4,
            imparte_flsm,
            aloca_vlsm,
            comprima_ipv6,
            expandeaza_ipv6,
        )
        print("✓")
        return True
    except ImportError as e:
        print(f"✗ ({e})")
        return False


def test_analiza_cidr():
    """Verifică analiza CIDR de bază."""
    print("  ○ Analiză CIDR...", end=" ")
    try:
        from src.utils.net_utils import analizeaza_interfata_ipv4
        
        info = analizeaza_interfata_ipv4("192.168.1.100/24")
        
        assert str(info.retea.network_address) == "192.168.1.0"
        assert info.gazde_utilizabile == 254
        print("✓")
        return True
    except Exception as e:
        print(f"✗ ({e})")
        return False


def test_flsm():
    """Verifică subnetarea FLSM."""
    print("  ○ Subnetare FLSM...", end=" ")
    try:
        from src.utils.net_utils import imparte_flsm
        
        subretele = imparte_flsm("10.0.0.0/24", 4)
        
        assert len(subretele) == 4
        assert subretele[0].prefixlen == 26
        print("✓")
        return True
    except Exception as e:
        print(f"✗ ({e})")
        return False


def test_vlsm():
    """Verifică alocarea VLSM."""
    print("  ○ Alocare VLSM...", end=" ")
    try:
        from src.utils.net_utils import aloca_vlsm
        
        alocari = aloca_vlsm("192.168.0.0/24", [50, 20, 10])
        
        assert len(alocari) == 3
        for alocare in alocari:
            gazde = alocare['subretea'].num_addresses - 2
            assert gazde >= alocare['cerinta']
        print("✓")
        return True
    except Exception as e:
        print(f"✗ ({e})")
        return False


def test_ipv6():
    """Verifică operațiile IPv6."""
    print("  ○ Operații IPv6...", end=" ")
    try:
        from src.utils.net_utils import comprima_ipv6, expandeaza_ipv6
        
        original = "2001:0db8:0000:0000:0000:0000:0000:0001"
        comprimata = comprima_ipv6(original)
        expandata = expandeaza_ipv6(comprimata)
        
        assert comprimata == "2001:db8::1"
        assert expandata == original
        print("✓")
        return True
    except Exception as e:
        print(f"✗ ({e})")
        return False


def test_structura_fisiere():
    """Verifică structura fișierelor."""
    print("  ○ Structură fișiere...", end=" ")
    
    fisiere_necesare = [
        "src/exercises/ex_5_01_cidr_flsm.py",
        "src/exercises/ex_5_02_vlsm_ipv6.py",
        "src/utils/net_utils.py",
        "docker/docker-compose.yml",
        "README.md",
    ]
    
    lipseste = []
    for fisier in fisiere_necesare:
        if not (RADACINA_PROIECT / fisier).exists():
            lipseste.append(fisier)
    
    if lipseste:
        print(f"✗ (lipsesc: {', '.join(lipseste)})")
        return False
    
    print("✓")
    return True


def main():
    print()
    print("═" * 50)
    print("  Test Smoke Rapid - Săptămâna 5")
    print("═" * 50)
    print()
    
    teste = [
        test_structura_fisiere,
        test_import_module,
        test_analiza_cidr,
        test_flsm,
        test_vlsm,
        test_ipv6,
    ]
    
    rezultate = []
    for test in teste:
        rezultate.append(test())
    
    print()
    print("═" * 50)
    
    trecut = sum(rezultate)
    total = len(rezultate)
    
    if all(rezultate):
        print(f"  ✓ Toate testele au trecut ({trecut}/{total})")
        print("  Mediul de laborator este pregătit!")
        cod_iesire = 0
    else:
        print(f"  ✗ {total - trecut} teste au eșuat")
        print("  Verificați configurația mediului.")
        cod_iesire = 1
    
    print("═" * 50)
    print()
    
    return cod_iesire


if __name__ == "__main__":
    sys.exit(main())
