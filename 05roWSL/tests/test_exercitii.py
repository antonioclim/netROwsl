#!/usr/bin/env python3
"""
Teste pentru Exercițiile de Laborator – Săptămâna 5
===================================================
Laborator Rețele de Calculatoare – ASE, Informatică Economică

Acest modul conține teste unitare pentru toate funcțiile
din modulele de exerciții.

Rulare:
    python3 -m pytest tests/test_exercitii.py -v
    python3 tests/test_exercitii.py
    python3 tests/test_exercitii.py --exercitiu 1
"""

import sys
import unittest
import ipaddress
from pathlib import Path

# Adaugă directorul rădăcină la PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Import funcții de testat
from src.utils.net_utils import (
    analizeaza_interfata_ipv4,
    imparte_flsm,
    aloca_vlsm,
    comprima_ipv6,
    expandeaza_ipv6,
    prefix_pentru_gazde,
    ip_la_binar,
    ip_la_binar_punctat,
    prefix_la_masca,
    masca_la_prefix,
    valideaza_cidr,
    valideaza_adresa_ipv4,
    valideaza_cidr_ipv4,
    este_in_retea,
    binar_la_ip,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Analiză IPv4
# ═══════════════════════════════════════════════════════════════════════════════

class TesteAnalizaIPv4(unittest.TestCase):
    """Teste pentru funcția analizeaza_interfata_ipv4."""
    
    def test_analiza_cidr_24(self):
        """Testează analiza unei rețele /24 standard."""
        info = analizeaza_interfata_ipv4("192.168.1.100/24")
        
        self.assertEqual(str(info.adresa), "192.168.1.100")
        self.assertEqual(str(info.retea.network_address), "192.168.1.0")
        self.assertEqual(str(info.masca), "255.255.255.0")
        self.assertEqual(str(info.broadcast), "192.168.1.255")
        self.assertEqual(info.total_adrese, 256)
        self.assertEqual(info.gazde_utilizabile, 254)
    
    def test_analiza_cidr_26(self):
        """Testează analiza unei rețele /26."""
        info = analizeaza_interfata_ipv4("192.168.10.14/26")
        
        self.assertEqual(str(info.retea.network_address), "192.168.10.0")
        self.assertEqual(str(info.broadcast), "192.168.10.63")
        self.assertEqual(info.total_adrese, 64)
        self.assertEqual(info.gazde_utilizabile, 62)
    
    def test_analiza_cidr_30(self):
        """Testează analiza unei rețele /30 (point-to-point)."""
        info = analizeaza_interfata_ipv4("10.0.0.1/30")
        
        self.assertEqual(info.total_adrese, 4)
        self.assertEqual(info.gazde_utilizabile, 2)
    
    def test_adresa_privata(self):
        """Testează detectarea adresei private."""
        info = analizeaza_interfata_ipv4("192.168.1.1/24")
        self.assertTrue(info.este_privata)
        self.assertEqual(info.tip_adresa, "privată")
    
    def test_adresa_loopback(self):
        """Testează detectarea adresei loopback."""
        info = analizeaza_interfata_ipv4("127.0.0.1/8")
        self.assertEqual(info.tip_adresa, "loopback")
    
    def test_prima_ultima_gazda(self):
        """Testează identificarea primei și ultimei gazde."""
        info = analizeaza_interfata_ipv4("10.0.0.0/24")
        
        self.assertEqual(str(info.prima_gazda), "10.0.0.1")
        self.assertEqual(str(info.ultima_gazda), "10.0.0.254")
    
    def test_cidr_invalid(self):
        """Testează respingerea CIDR-ului invalid."""
        with self.assertRaises(ValueError):
            analizeaza_interfata_ipv4("invalid")
        
        with self.assertRaises(ValueError):
            analizeaza_interfata_ipv4("192.168.1.1")  # fără prefix
        
        with self.assertRaises(ValueError):
            analizeaza_interfata_ipv4("192.168.1.1/33")  # prefix invalid


# ═══════════════════════════════════════════════════════════════════════════════
# Teste FLSM
# ═══════════════════════════════════════════════════════════════════════════════

class TesteFLSM(unittest.TestCase):
    """Teste pentru funcția imparte_flsm."""
    
    def test_flsm_4_subretele(self):
        """Testează împărțirea în 4 subrețele egale."""
        subretele = imparte_flsm("192.168.100.0/24", 4)
        
        self.assertEqual(len(subretele), 4)
        self.assertEqual(subretele[0].prefixlen, 26)
        
        # Verifică adresele de rețea
        self.assertEqual(str(subretele[0].network_address), "192.168.100.0")
        self.assertEqual(str(subretele[1].network_address), "192.168.100.64")
        self.assertEqual(str(subretele[2].network_address), "192.168.100.128")
        self.assertEqual(str(subretele[3].network_address), "192.168.100.192")
    
    def test_flsm_8_subretele(self):
        """Testează împărțirea în 8 subrețele."""
        subretele = imparte_flsm("10.0.0.0/24", 8)
        
        self.assertEqual(len(subretele), 8)
        self.assertEqual(subretele[0].prefixlen, 27)
    
    def test_flsm_2_subretele(self):
        """Testează împărțirea în 2 subrețele."""
        subretele = imparte_flsm("172.16.0.0/16", 2)
        
        self.assertEqual(len(subretele), 2)
        self.assertEqual(subretele[0].prefixlen, 17)
    
    def test_flsm_numar_invalid(self):
        """Testează respingerea numărului care nu e putere de 2."""
        with self.assertRaises(ValueError):
            imparte_flsm("192.168.0.0/24", 3)
        
        with self.assertRaises(ValueError):
            imparte_flsm("192.168.0.0/24", 5)
    
    def test_flsm_prea_multe_subretele(self):
        """Testează respingerea când sunt prea multe subrețele."""
        with self.assertRaises(ValueError):
            imparte_flsm("192.168.0.0/30", 16)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste VLSM
# ═══════════════════════════════════════════════════════════════════════════════

class TesteVLSM(unittest.TestCase):
    """Teste pentru funcția aloca_vlsm."""
    
    def test_vlsm_cerinte_simple(self):
        """Testează alocarea VLSM pentru cerințe simple."""
        alocari = aloca_vlsm("192.168.0.0/24", [60, 20, 10, 2])
        
        self.assertEqual(len(alocari), 4)
        
        # Verifică că fiecare alocare are suficiente gazde
        for alocare in alocari:
            gazde_disponibile = alocare['subretea'].num_addresses - 2
            self.assertGreaterEqual(gazde_disponibile, alocare['cerinta'])
    
    def test_vlsm_eficienta(self):
        """Testează eficiența alocării VLSM."""
        alocari = aloca_vlsm("10.0.0.0/24", [100, 50, 20, 10])
        
        # Verifică prefixurile optime
        prefixuri = [a['subretea'].prefixlen for a in alocari]
        
        # 100 gazde necesită /25 (126 disponibile)
        self.assertIn(25, prefixuri)
    
    def test_vlsm_spatiu_insuficient(self):
        """Testează detectarea spațiului insuficient."""
        with self.assertRaises(ValueError):
            aloca_vlsm("192.168.0.0/28", [50, 50])
    
    def test_vlsm_cerinte_identice(self):
        """Testează VLSM cu cerințe identice (similar cu FLSM)."""
        alocari = aloca_vlsm("192.168.0.0/24", [30, 30, 30, 30])
        
        self.assertEqual(len(alocari), 4)
        
        # Toate ar trebui să aibă același prefix
        prefixuri = [a['subretea'].prefixlen for a in alocari]
        self.assertEqual(len(set(prefixuri)), 1)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste IPv6
# ═══════════════════════════════════════════════════════════════════════════════

class TesteIPv6(unittest.TestCase):
    """Teste pentru funcțiile IPv6."""
    
    def test_comprimare_standard(self):
        """Testează comprimarea standard IPv6."""
        adresa = "2001:0db8:0000:0000:0000:0000:0000:0001"
        comprimata = comprima_ipv6(adresa)
        self.assertEqual(comprimata, "2001:db8::1")
    
    def test_expandare_standard(self):
        """Testează expandarea standard IPv6."""
        adresa = "2001:db8::1"
        expandata = expandeaza_ipv6(adresa)
        self.assertEqual(expandata, "2001:0db8:0000:0000:0000:0000:0000:0001")
    
    def test_comprimare_loopback(self):
        """Testează comprimarea adresei loopback."""
        adresa = "0000:0000:0000:0000:0000:0000:0000:0001"
        comprimata = comprima_ipv6(adresa)
        self.assertEqual(comprimata, "::1")
    
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
    
    def test_comprimare_link_local(self):
        """Testează comprimarea adresei link-local."""
        adresa = "fe80:0000:0000:0000:0000:0000:0000:0001"
        comprimata = comprima_ipv6(adresa)
        self.assertEqual(comprimata, "fe80::1")
    
    def test_ipv6_invalid(self):
        """Testează respingerea adresei IPv6 invalide."""
        with self.assertRaises(ValueError):
            comprima_ipv6("invalid")
        
        with self.assertRaises(ValueError):
            expandeaza_ipv6("not:an:ipv6")


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Prefix
# ═══════════════════════════════════════════════════════════════════════════════

class TestePrefix(unittest.TestCase):
    """Teste pentru calculul prefixului."""
    
    def test_prefix_pentru_100_gazde(self):
        """Testează prefixul pentru 100 de gazde."""
        prefix = prefix_pentru_gazde(100)
        self.assertEqual(prefix, 25)
    
    def test_prefix_pentru_2_gazde(self):
        """Testează prefixul pentru 2 gazde."""
        prefix = prefix_pentru_gazde(2)
        self.assertEqual(prefix, 30)
    
    def test_prefix_pentru_500_gazde(self):
        """Testează prefixul pentru 500 de gazde."""
        prefix = prefix_pentru_gazde(500)
        self.assertEqual(prefix, 23)
    
    def test_prefix_pentru_1_gazda(self):
        """Testează prefixul pentru 1 gazdă."""
        prefix = prefix_pentru_gazde(1)
        self.assertEqual(prefix, 30)
    
    def test_prefix_pentru_254_gazde(self):
        """Testează prefixul pentru exact 254 gazde."""
        prefix = prefix_pentru_gazde(254)
        self.assertEqual(prefix, 24)
    
    def test_prefix_pentru_0_gazde(self):
        """Testează prefixul pentru 0 gazde."""
        prefix = prefix_pentru_gazde(0)
        self.assertEqual(prefix, 30)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Conversii Binare
# ═══════════════════════════════════════════════════════════════════════════════

class TesteConversiiBinare(unittest.TestCase):
    """Teste pentru funcțiile de conversie binară."""
    
    def test_ip_la_binar(self):
        """Testează conversia IP la binar."""
        binar = ip_la_binar("192.168.1.1")
        self.assertEqual(len(binar), 32)
        self.assertEqual(binar, "11000000101010000000000100000001")
    
    def test_ip_la_binar_punctat(self):
        """Testează conversia IP la binar cu puncte."""
        binar = ip_la_binar_punctat("192.168.1.1")
        self.assertEqual(binar, "11000000.10101000.00000001.00000001")
    
    def test_binar_la_ip(self):
        """Testează conversia binar la IP."""
        ip = binar_la_ip("11000000101010000000000100000001")
        self.assertEqual(ip, "192.168.1.1")
    
    def test_binar_punctat_la_ip(self):
        """Testează conversia binar cu puncte la IP."""
        ip = binar_la_ip("11000000.10101000.00000001.00000001")
        self.assertEqual(ip, "192.168.1.1")
    
    def test_binar_conversie_reversibila(self):
        """Verifică că conversia e reversibilă."""
        original = "10.20.30.40"
        binar = ip_la_binar(original)
        inapoi = binar_la_ip(binar)
        self.assertEqual(original, inapoi)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Conversii Mască/Prefix
# ═══════════════════════════════════════════════════════════════════════════════

class TesteConversiiMascaPrefix(unittest.TestCase):
    """Teste pentru conversiile mască-prefix."""
    
    def test_prefix_la_masca_24(self):
        """Testează conversia prefix /24 la mască."""
        masca = prefix_la_masca(24)
        self.assertEqual(masca, "255.255.255.0")
    
    def test_prefix_la_masca_26(self):
        """Testează conversia prefix /26 la mască."""
        masca = prefix_la_masca(26)
        self.assertEqual(masca, "255.255.255.192")
    
    def test_prefix_la_masca_8(self):
        """Testează conversia prefix /8 la mască."""
        masca = prefix_la_masca(8)
        self.assertEqual(masca, "255.0.0.0")
    
    def test_masca_la_prefix_24(self):
        """Testează conversia mască la prefix /24."""
        prefix = masca_la_prefix("255.255.255.0")
        self.assertEqual(prefix, 24)
    
    def test_masca_la_prefix_26(self):
        """Testează conversia mască la prefix /26."""
        prefix = masca_la_prefix("255.255.255.192")
        self.assertEqual(prefix, 26)
    
    def test_masca_invalida_non_contigua(self):
        """Testează respingerea măștii cu biți non-contigui."""
        with self.assertRaises(ValueError):
            masca_la_prefix("255.255.0.255")
        
        with self.assertRaises(ValueError):
            masca_la_prefix("255.0.255.0")
    
    def test_conversie_reversibila(self):
        """Verifică că conversia e reversibilă."""
        for prefix in [8, 16, 20, 24, 26, 28, 30, 32]:
            masca = prefix_la_masca(prefix)
            inapoi = masca_la_prefix(masca)
            self.assertEqual(prefix, inapoi)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Validare
# ═══════════════════════════════════════════════════════════════════════════════

class TesteValidare(unittest.TestCase):
    """Teste pentru funcțiile de validare."""
    
    def test_valideaza_cidr_valid(self):
        """Testează validarea CIDR valid."""
        self.assertTrue(valideaza_cidr("192.168.1.0/24"))
        self.assertTrue(valideaza_cidr("10.0.0.0/8"))
    
    def test_valideaza_cidr_invalid(self):
        """Testează respingerea CIDR invalid."""
        self.assertFalse(valideaza_cidr("invalid"))
        self.assertFalse(valideaza_cidr("192.168.1.0/33"))
    
    def test_valideaza_adresa_ipv4_valida(self):
        """Testează validarea adresei IPv4 valide."""
        self.assertTrue(valideaza_adresa_ipv4("192.168.1.1"))
        self.assertTrue(valideaza_adresa_ipv4("10.0.0.1"))
    
    def test_valideaza_adresa_ipv4_invalida(self):
        """Testează respingerea adresei IPv4 invalide."""
        with self.assertRaises(ValueError):
            valideaza_adresa_ipv4("invalid")
        
        with self.assertRaises(ValueError):
            valideaza_adresa_ipv4("256.1.1.1")
    
    def test_valideaza_cidr_ipv4_valid(self):
        """Testează validarea CIDR IPv4 valid."""
        self.assertTrue(valideaza_cidr_ipv4("192.168.1.0/24"))
    
    def test_valideaza_cidr_ipv4_invalid(self):
        """Testează respingerea CIDR IPv4 invalid."""
        with self.assertRaises(ValueError):
            valideaza_cidr_ipv4("invalid/24")


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Edge Cases
# ═══════════════════════════════════════════════════════════════════════════════

class TesteEdgeCases(unittest.TestCase):
    """Teste pentru cazuri limită și input-uri invalide."""
    
    def test_cidr_prefix_32(self):
        """Testează /32 - o singură gazdă (host route)."""
        info = analizeaza_interfata_ipv4("10.0.0.1/32")
        self.assertEqual(info.gazde_utilizabile, 0)
        self.assertEqual(info.total_adrese, 1)
    
    def test_cidr_prefix_31(self):
        """Testează /31 - rețea point-to-point (RFC 3021)."""
        info = analizeaza_interfata_ipv4("10.0.0.0/31")
        self.assertEqual(info.total_adrese, 2)
    
    def test_cidr_prefix_0(self):
        """Testează /0 - întregul spațiu IPv4."""
        info = analizeaza_interfata_ipv4("0.0.0.0/0")
        self.assertEqual(info.total_adrese, 2**32)
    
    def test_este_in_retea(self):
        """Testează verificarea apartenenței la rețea."""
        self.assertTrue(este_in_retea("192.168.1.50", "192.168.1.0/24"))
        self.assertFalse(este_in_retea("192.168.2.1", "192.168.1.0/24"))
        self.assertTrue(este_in_retea("10.0.0.1", "10.0.0.0/8"))


# ═══════════════════════════════════════════════════════════════════════════════
# Funcție de rulare
# ═══════════════════════════════════════════════════════════════════════════════

def ruleaza_teste_exercitiu(numar_exercitiu: int = None):
    """
    Rulează testele pentru un anumit exercițiu sau toate.
    
    Args:
        numar_exercitiu: 1, 2 sau None pentru toate
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    if numar_exercitiu == 1:
        # Teste pentru Exercițiul 1: CIDR și FLSM
        suite.addTests(loader.loadTestsFromTestCase(TesteAnalizaIPv4))
        suite.addTests(loader.loadTestsFromTestCase(TesteFLSM))
        suite.addTests(loader.loadTestsFromTestCase(TesteConversiiBinare))
        suite.addTests(loader.loadTestsFromTestCase(TesteConversiiMascaPrefix))
    elif numar_exercitiu == 2:
        # Teste pentru Exercițiul 2: VLSM și IPv6
        suite.addTests(loader.loadTestsFromTestCase(TesteVLSM))
        suite.addTests(loader.loadTestsFromTestCase(TesteIPv6))
    else:
        # Toate testele
        suite.addTests(loader.loadTestsFromTestCase(TesteAnalizaIPv4))
        suite.addTests(loader.loadTestsFromTestCase(TesteFLSM))
        suite.addTests(loader.loadTestsFromTestCase(TesteVLSM))
        suite.addTests(loader.loadTestsFromTestCase(TesteIPv6))
        suite.addTests(loader.loadTestsFromTestCase(TestePrefix))
        suite.addTests(loader.loadTestsFromTestCase(TesteConversiiBinare))
        suite.addTests(loader.loadTestsFromTestCase(TesteConversiiMascaPrefix))
        suite.addTests(loader.loadTestsFromTestCase(TesteValidare))
        suite.addTests(loader.loadTestsFromTestCase(TesteEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    rezultat = runner.run(suite)
    
    return rezultat.wasSuccessful()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Rulează testele pentru exerciții")
    parser.add_argument(
        "--exercitiu", "-e",
        type=int,
        choices=[1, 2],
        help="Numărul exercițiului (1 sau 2). Fără argument: toate testele."
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("  Teste Exerciții Săptămâna 5 – Nivelul Rețea")
    print("=" * 70)
    print()
    
    succes = ruleaza_teste_exercitiu(args.exercitiu)
    
    print()
    print("=" * 70)
    if succes:
        print("  ✓ TOATE TESTELE AU TRECUT!")
    else:
        print("  ✗ UNELE TESTE AU EȘUAT")
    print("=" * 70)
    
    sys.exit(0 if succes else 1)
