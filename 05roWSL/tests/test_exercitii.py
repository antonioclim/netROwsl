#!/usr/bin/env python3
"""
Teste pentru Exercițiile Săptămânii 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Verifică corectitudinea implementărilor din exerciții.
Include teste pentru edge cases, performanță și integrare.
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
    prefix_la_masca,
    masca_la_prefix,
    valideaza_adresa_ipv4,
    valideaza_cidr_ipv4,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Analiză CIDR
# ═══════════════════════════════════════════════════════════════════════════════

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
    
    def test_conversie_binara_cu_puncte(self):
        """Testează conversia IP la binar cu separatori."""
        binar = ip_la_binar("192.168.1.1", cu_puncte=True)
        self.assertEqual(binar, "11000000.10101000.00000001.00000001")
    
    def test_prefix_la_masca(self):
        """Testează conversia prefix la mască."""
        self.assertEqual(str(prefix_la_masca(24)), "255.255.255.0")
        self.assertEqual(str(prefix_la_masca(26)), "255.255.255.192")
        self.assertEqual(str(prefix_la_masca(8)), "255.0.0.0")
        self.assertEqual(str(prefix_la_masca(0)), "0.0.0.0")
        self.assertEqual(str(prefix_la_masca(32)), "255.255.255.255")
    
    def test_masca_la_prefix(self):
        """Testează conversia mască la prefix."""
        self.assertEqual(masca_la_prefix("255.255.255.0"), 24)
        self.assertEqual(masca_la_prefix("255.255.255.192"), 26)
        self.assertEqual(masca_la_prefix("255.0.0.0"), 8)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste FLSM
# ═══════════════════════════════════════════════════════════════════════════════

class TesteFLSM(unittest.TestCase):
    """Teste pentru subnetarea FLSM (Exercițiul 5.01)."""
    
    def test_flsm_4_subretele(self):
        """Testează împărțirea în 4 subrețele egale."""
        subretele = imparte_flsm("192.168.100.0/24", 4)
        
        self.assertEqual(len(subretele), 4)
        for subretea in subretele:
            self.assertEqual(subretea.prefixlen, 26)
            self.assertEqual(subretea.num_addresses - 2, 62)
    
    def test_flsm_8_subretele(self):
        """Testează împărțirea în 8 subrețele egale."""
        subretele = imparte_flsm("10.0.0.0/24", 8)
        
        self.assertEqual(len(subretele), 8)
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
    
    def test_flsm_2_subretele(self):
        """Testează împărțirea în 2 subrețele."""
        subretele = imparte_flsm("172.16.0.0/16", 2)
        
        self.assertEqual(len(subretele), 2)
        self.assertEqual(subretele[0].prefixlen, 17)
        self.assertEqual(str(subretele[0].network_address), "172.16.0.0")
        self.assertEqual(str(subretele[1].network_address), "172.16.128.0")


# ═══════════════════════════════════════════════════════════════════════════════
# Teste VLSM
# ═══════════════════════════════════════════════════════════════════════════════

class TesteVLSM(unittest.TestCase):
    """Teste pentru alocarea VLSM (Exercițiul 5.02)."""
    
    def test_vlsm_cerinte_variate(self):
        """Testează alocarea VLSM pentru cerințe variate."""
        cerinte = [60, 20, 10, 2]
        alocari = aloca_vlsm("192.168.0.0/24", cerinte)
        
        self.assertEqual(len(alocari), 4)
        
        for alocare in alocari:
            gazde_disponibile = alocare['subretea'].num_addresses - 2
            self.assertGreaterEqual(gazde_disponibile, alocare['cerinta'])
    
    def test_vlsm_sortare_descrescatoare(self):
        """Verifică că VLSM alocă întâi cerințele mari."""
        cerinte = [10, 50, 20, 100]
        alocari = aloca_vlsm("172.16.0.0/24", cerinte)
        
        cerinte_alocate = [a['cerinta'] for a in alocari]
        self.assertEqual(cerinte_alocate[0], 100)
    
    def test_vlsm_eficienta(self):
        """Verifică că VLSM este mai eficient decât FLSM."""
        cerinte = [60, 20, 10, 2]
        
        alocari_vlsm = aloca_vlsm("192.168.0.0/24", cerinte)
        total_vlsm = sum(a['subretea'].num_addresses - 2 for a in alocari_vlsm)
        
        subretele_flsm = imparte_flsm("192.168.0.0/24", 4)
        total_flsm = sum(s.num_addresses - 2 for s in subretele_flsm)
        
        self.assertLessEqual(total_vlsm, total_flsm)
    
    def test_vlsm_cerinte_egale(self):
        """Testează VLSM cu cerințe egale (ar trebui să fie ca FLSM)."""
        cerinte = [30, 30, 30, 30]
        alocari = aloca_vlsm("192.168.0.0/24", cerinte)
        
        prefixe = [a['subretea'].prefixlen for a in alocari]
        self.assertTrue(all(p == prefixe[0] for p in prefixe))


# ═══════════════════════════════════════════════════════════════════════════════
# Teste IPv6
# ═══════════════════════════════════════════════════════════════════════════════

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
    
    def test_comprimare_link_local(self):
        """Testează comprimarea adresei link-local."""
        adresa = "fe80:0000:0000:0000:0000:0000:0000:0001"
        comprimata = comprima_ipv6(adresa)
        self.assertEqual(comprimata, "fe80::1")


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
        # RFC 3021: /31 pentru point-to-point, ambele adrese utilizabile
    
    def test_cidr_prefix_30(self):
        """Testează /30 - cea mai mică rețea standard."""
        info = analizeaza_interfata_ipv4("192.168.1.0/30")
        self.assertEqual(info.gazde_utilizabile, 2)
        self.assertEqual(str(info.prima_gazda), "192.168.1.1")
        self.assertEqual(str(info.ultima_gazda), "192.168.1.2")
    
    def test_cidr_prefix_0(self):
        """Testează /0 - întregul spațiu IPv4."""
        info = analizeaza_interfata_ipv4("0.0.0.0/0")
        self.assertEqual(info.total_adrese, 2**32)
    
    def test_flsm_prefix_prea_mare(self):
        """Testează FLSM când rezultatul ar depăși /32."""
        with self.assertRaises(ValueError):
            imparte_flsm("192.168.0.0/30", 8)
    
    def test_flsm_numar_non_putere_2(self):
        """Testează FLSM cu număr care nu e putere de 2."""
        with self.assertRaises(ValueError):
            imparte_flsm("192.168.0.0/24", 5)
    
    def test_vlsm_spatiu_insuficient(self):
        """Testează VLSM când cerințele depășesc spațiul."""
        with self.assertRaises(ValueError):
            aloca_vlsm("192.168.0.0/28", [10, 10, 10])
    
    def test_vlsm_cerinta_zero(self):
        """Testează VLSM cu cerință de 0 gazde."""
        alocari = aloca_vlsm("10.0.0.0/24", [0, 10])
        self.assertEqual(len(alocari), 2)
    
    def test_validare_ip_invalid_octet(self):
        """Testează validarea cu octet invalid."""
        with self.assertRaises(ValueError):
            valideaza_adresa_ipv4("256.1.1.1")
    
    def test_validare_ip_format_invalid(self):
        """Testează validarea cu format invalid."""
        with self.assertRaises(ValueError):
            valideaza_adresa_ipv4("192.168.1")
    
    def test_validare_cidr_prefix_invalid(self):
        """Testează validarea CIDR cu prefix invalid."""
        with self.assertRaises(ValueError):
            valideaza_cidr_ipv4("192.168.1.0/33")
    
    def test_ipv6_dublu_colon_invalid(self):
        """Testează IPv6 cu :: dublu (invalid)."""
        with self.assertRaises(ValueError):
            expandeaza_ipv6("2001::db8::1")


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Performanță
# ═══════════════════════════════════════════════════════════════════════════════

class TestePerformanta(unittest.TestCase):
    """Teste pentru performanță și volume mari."""
    
    def test_vlsm_multe_cerinte(self):
        """Testează VLSM cu multe cerințe."""
        cerinte = [2] * 100
        alocari = aloca_vlsm("10.0.0.0/16", cerinte)
        self.assertEqual(len(alocari), 100)
    
    def test_flsm_multe_subretele(self):
        """Testează FLSM cu multe subrețele."""
        subretele = imparte_flsm("10.0.0.0/8", 256)
        self.assertEqual(len(subretele), 256)
        self.assertEqual(subretele[0].prefixlen, 16)
    
    def test_analiza_multipla(self):
        """Testează analiza multiplă rapidă."""
        adrese = [
            f"192.168.{i}.{j}/24"
            for i in range(10)
            for j in range(10)
        ]
        
        for adresa in adrese:
            info = analizeaza_interfata_ipv4(adresa)
            self.assertIsNotNone(info)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Integrare
# ═══════════════════════════════════════════════════════════════════════════════

class TesteIntegrare(unittest.TestCase):
    """Teste de integrare pentru workflow-uri complete."""
    
    def test_workflow_tema1_techvision(self):
        """Simulează workflow-ul Temei 1 - TechVision SRL."""
        cerinte = [120, 55, 30, 25, 15, 8, 2, 2]
        baza = "172.20.0.0/22"
        
        alocari = aloca_vlsm(baza, cerinte)
        
        for alocare in alocari:
            disponibil = alocare['subretea'].num_addresses - 2
            self.assertGreaterEqual(disponibil, alocare['cerinta'])
        
        import ipaddress
        retea_baza = ipaddress.ip_network(baza)
        for alocare in alocari:
            self.assertTrue(
                alocare['subretea'].subnet_of(retea_baza),
                f"{alocare['subretea']} nu e în {retea_baza}"
            )
    
    def test_workflow_ipv6_migrare(self):
        """Simulează workflow-ul de migrare IPv6."""
        adrese_test = [
            "2001:0db8:cafe:0010:0000:0000:0000:0001",
            "fe80:0000:0000:0000:0000:0000:0000:0001",
        ]
        
        for adresa in adrese_test:
            comprimata = comprima_ipv6(adresa)
            expandata = expandeaza_ipv6(comprimata)
            self.assertEqual(expandata, adresa)
    
    def test_workflow_flsm_vs_vlsm(self):
        """Compară FLSM și VLSM pentru același scenariu."""
        baza = "192.168.0.0/24"
        cerinte = [50, 20, 10, 5]
        
        subretele_flsm = imparte_flsm(baza, 4)
        alocari_vlsm = aloca_vlsm(baza, cerinte)
        
        total_flsm = sum(s.num_addresses for s in subretele_flsm)
        total_vlsm = sum(a['subretea'].num_addresses for a in alocari_vlsm)
        
        self.assertLessEqual(total_vlsm, total_flsm)


# ═══════════════════════════════════════════════════════════════════════════════
# Runner
# ═══════════════════════════════════════════════════════════════════════════════

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
    elif exercitiu == 4:
        suite.addTests(loader.loadTestsFromTestCase(TesteEdgeCases))
        suite.addTests(loader.loadTestsFromTestCase(TestePerformanta))
        suite.addTests(loader.loadTestsFromTestCase(TesteIntegrare))
    else:
        suite.addTests(loader.loadTestsFromTestCase(TesteAnalizaCIDR))
        suite.addTests(loader.loadTestsFromTestCase(TesteFLSM))
        suite.addTests(loader.loadTestsFromTestCase(TesteVLSM))
        suite.addTests(loader.loadTestsFromTestCase(TesteIPv6))
        suite.addTests(loader.loadTestsFromTestCase(TestePrefix))
        suite.addTests(loader.loadTestsFromTestCase(TesteEdgeCases))
        suite.addTests(loader.loadTestsFromTestCase(TestePerformanta))
        suite.addTests(loader.loadTestsFromTestCase(TesteIntegrare))
    
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
        help="Rulează teste doar pentru exercițiul specificat (4 = edge cases)"
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
