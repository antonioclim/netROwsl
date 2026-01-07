#!/usr/bin/env python3
"""
Teste pentru Exercițiile Săptămânii 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Verifică corectitudinea implementărilor din exerciții.
"""

import sys
import unittest
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from src.utils.net_utils import (
    analizeaza_interfata_ipv4,
    imparte_flsm,
    aloca_vlsm,
    comprima_ipv6,
    expandeaza_ipv6,
    prefix_pentru_gazde,
    ip_la_binar,
)


class TesteAnalizaCIDR(unittest.TestCase):
    """Teste pentru analiza CIDR (Exercițiul 5.01)."""
    
    def test_analiza_192_168_10_14_26(self):
        """Testează analiza adresei 192.168.10.14/26."""
        info = analizeaza_interfata_ipv4("192.168.10.14/26")
        
        self.assertEqual(str(info.retea.network_address), "192.168.10.0")
        self.assertEqual(str(info.broadcast), "192.168.10.63")
        self.assertEqual(info.gazde_utilizabile, 62)
        self.assertEqual(str(info.prima_gazda), "192.168.10.1")
        self.assertEqual(str(info.ultima_gazda), "192.168.10.62")
        self.assertTrue(info.este_privata)
    
    def test_analiza_10_0_0_1_8(self):
        """Testează analiza adresei 10.0.0.1/8."""
        info = analizeaza_interfata_ipv4("10.0.0.1/8")
        
        self.assertEqual(str(info.retea.network_address), "10.0.0.0")
        self.assertEqual(str(info.broadcast), "10.255.255.255")
        self.assertEqual(info.gazde_utilizabile, 16777214)
        self.assertTrue(info.este_privata)
    
    def test_analiza_adresa_publica(self):
        """Testează analiza unei adrese publice."""
        info = analizeaza_interfata_ipv4("8.8.8.8/32")
        
        self.assertFalse(info.este_privata)
        self.assertEqual(info.gazde_utilizabile, 0)
    
    def test_conversie_binara(self):
        """Testează conversia IP la binar."""
        binar = ip_la_binar("192.168.1.1")
        self.assertEqual(len(binar), 32)
        self.assertEqual(binar, "11000000101010000000000100000001")


class TesteFLSM(unittest.TestCase):
    """Teste pentru subnetarea FLSM (Exercițiul 5.01)."""
    
    def test_flsm_4_subretele(self):
        """Testează împărțirea în 4 subrețele egale."""
        subretele = imparte_flsm("192.168.100.0/24", 4)
        
        self.assertEqual(len(subretele), 4)
        # Fiecare subrețea ar trebui să fie /26
        for subretea in subretele:
            self.assertEqual(subretea.prefixlen, 26)
            self.assertEqual(subretea.num_addresses - 2, 62)
    
    def test_flsm_8_subretele(self):
        """Testează împărțirea în 8 subrețele egale."""
        subretele = imparte_flsm("10.0.0.0/24", 8)
        
        self.assertEqual(len(subretele), 8)
        # Fiecare subrețea ar trebui să fie /27
        for subretea in subretele:
            self.assertEqual(subretea.prefixlen, 27)
            self.assertEqual(subretea.num_addresses - 2, 30)
    
    def test_flsm_adrese_consecutive(self):
        """Verifică că subrețelele sunt consecutive."""
        subretele = imparte_flsm("192.168.0.0/24", 4)
        
        self.assertEqual(str(subretele[0].network_address), "192.168.0.0")
        self.assertEqual(str(subretele[1].network_address), "192.168.0.64")
        self.assertEqual(str(subretele[2].network_address), "192.168.0.128")
        self.assertEqual(str(subretele[3].network_address), "192.168.0.192")


class TesteVLSM(unittest.TestCase):
    """Teste pentru alocarea VLSM (Exercițiul 5.02)."""
    
    def test_vlsm_cerinte_variate(self):
        """Testează alocarea VLSM pentru cerințe variate."""
        cerinte = [60, 20, 10, 2]
        alocari = aloca_vlsm("192.168.0.0/24", cerinte)
        
        self.assertEqual(len(alocari), 4)
        
        # Verifică că fiecare alocare satisface cerința
        for alocare in alocari:
            gazde_disponibile = alocare['subretea'].num_addresses - 2
            self.assertGreaterEqual(gazde_disponibile, alocare['cerinta'])
    
    def test_vlsm_sortare_descrescatoare(self):
        """Verifică că VLSM alocă întâi cerințele mari."""
        cerinte = [10, 50, 20, 100]
        alocari = aloca_vlsm("172.16.0.0/24", cerinte)
        
        # Prima alocare ar trebui să fie pentru 100 de gazde
        cerinte_alocate = [a['cerinta'] for a in alocari]
        self.assertEqual(cerinte_alocate[0], 100)
    
    def test_vlsm_eficienta(self):
        """Verifică că VLSM este mai eficient decât FLSM."""
        cerinte = [60, 20, 10, 2]
        
        # VLSM
        alocari_vlsm = aloca_vlsm("192.168.0.0/24", cerinte)
        total_vlsm = sum(a['subretea'].num_addresses - 2 for a in alocari_vlsm)
        
        # FLSM (trebuie să acomodeze cel mai mare)
        subretele_flsm = imparte_flsm("192.168.0.0/24", 4)
        total_flsm = sum(s.num_addresses - 2 for s in subretele_flsm)
        
        # VLSM ar trebui să fie mai eficient
        self.assertLessEqual(total_vlsm, total_flsm)


class TesteIPv6(unittest.TestCase):
    """Teste pentru operațiile IPv6 (Exercițiul 5.02)."""
    
    def test_comprimare_ipv6_zerouri_consecutive(self):
        """Testează comprimarea zerourilor consecutive."""
        adresa = "2001:0db8:0000:0000:0000:0000:0000:0001"
        comprimata = comprima_ipv6(adresa)
        self.assertEqual(comprimata, "2001:db8::1")
    
    def test_comprimare_ipv6_loopback(self):
        """Testează comprimarea adresei loopback."""
        adresa = "0000:0000:0000:0000:0000:0000:0000:0001"
        comprimata = comprima_ipv6(adresa)
        self.assertEqual(comprimata, "::1")
    
    def test_expandare_ipv6(self):
        """Testează expandarea unei adrese comprimate."""
        adresa = "2001:db8::1"
        expandata = expandeaza_ipv6(adresa)
        self.assertEqual(expandata, "2001:0db8:0000:0000:0000:0000:0000:0001")
    
    def test_expandare_loopback(self):
        """Testează expandarea adresei loopback."""
        expandata = expandeaza_ipv6("::1")
        self.assertEqual(expandata, "0000:0000:0000:0000:0000:0000:0000:0001")
    
    def test_comprimare_expandare_idempotenta(self):
        """Verifică că comprimare + expandare este idempotentă."""
        original = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        comprimata = comprima_ipv6(original)
        expandata = expandeaza_ipv6(comprimata)
        self.assertEqual(expandata, original)


class TestePrefix(unittest.TestCase):
    """Teste pentru calculul prefixului."""
    
    def test_prefix_pentru_100_gazde(self):
        """Testează prefixul pentru 100 de gazde."""
        prefix = prefix_pentru_gazde(100)
        self.assertEqual(prefix, 25)  # /25 = 126 gazde
    
    def test_prefix_pentru_2_gazde(self):
        """Testează prefixul pentru 2 gazde."""
        prefix = prefix_pentru_gazde(2)
        self.assertEqual(prefix, 30)  # /30 = 2 gazde
    
    def test_prefix_pentru_500_gazde(self):
        """Testează prefixul pentru 500 de gazde."""
        prefix = prefix_pentru_gazde(500)
        self.assertEqual(prefix, 23)  # /23 = 510 gazde


def ruleaza_teste_specifice(exercitiu: int = None):
    """Rulează teste pentru un exercițiu specific sau toate."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    if exercitiu == 1:
        suite.addTests(loader.loadTestsFromTestCase(TesteAnalizaCIDR))
        suite.addTests(loader.loadTestsFromTestCase(TesteFLSM))
    elif exercitiu == 2:
        suite.addTests(loader.loadTestsFromTestCase(TesteVLSM))
        suite.addTests(loader.loadTestsFromTestCase(TesteIPv6))
    elif exercitiu == 3:
        suite.addTests(loader.loadTestsFromTestCase(TestePrefix))
    else:
        # Toate testele
        suite.addTests(loader.loadTestsFromTestCase(TesteAnalizaCIDR))
        suite.addTests(loader.loadTestsFromTestCase(TesteFLSM))
        suite.addTests(loader.loadTestsFromTestCase(TesteVLSM))
        suite.addTests(loader.loadTestsFromTestCase(TesteIPv6))
        suite.addTests(loader.loadTestsFromTestCase(TestePrefix))
    
    runner = unittest.TextTestRunner(verbosity=2)
    rezultat = runner.run(suite)
    
    return len(rezultat.failures) == 0 and len(rezultat.errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description="Teste pentru exercițiile Săptămânii 5"
    )
    parser.add_argument(
        "--exercitiu", "-e",
        type=int,
        choices=[1, 2, 3, 4],
        help="Rulează teste doar pentru exercițiul specificat"
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("  Teste Exerciții Săptămâna 5")
    print("  Rețele de Calculatoare – ASE")
    print("=" * 60)
    print()
    
    if args.exercitiu:
        print(f"Rulare teste pentru Exercițiul {args.exercitiu}")
    else:
        print("Rulare toate testele")
    print()
    
    succes = ruleaza_teste_specifice(args.exercitiu)
    
    print()
    if succes:
        print("✓ Toate testele au trecut!")
    else:
        print("✗ Unele teste au eșuat.")
    
    return 0 if succes else 1


if __name__ == "__main__":
    sys.exit(main())
