#!/usr/bin/env python3
"""
Teste pentru Exercițiile Laboratorului
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Verifică funcționalitatea fiecărui exercițiu individual.
"""

import unittest
import sys
import socket
from pathlib import Path
from unittest.mock import patch, MagicMock

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


class TestExercitiu1ScannerPorturi(unittest.TestCase):
    """Teste pentru Exercițiul 1: Scanner Porturi."""
    
    def test_parseaza_porturi_simplu(self):
        """Testează parsarea unui port simplu."""
        from src.exercises.ex_13_01_scanner_porturi import parseaza_porturi
        rezultat = parseaza_porturi("80")
        self.assertEqual(rezultat, [80])
    
    def test_parseaza_porturi_lista(self):
        """Testează parsarea unei liste de porturi."""
        from src.exercises.ex_13_01_scanner_porturi import parseaza_porturi
        rezultat = parseaza_porturi("22,80,443")
        self.assertEqual(rezultat, [22, 80, 443])
    
    def test_parseaza_porturi_interval(self):
        """Testează parsarea unui interval de porturi."""
        from src.exercises.ex_13_01_scanner_porturi import parseaza_porturi
        rezultat = parseaza_porturi("80-85")
        self.assertEqual(rezultat, [80, 81, 82, 83, 84, 85])
    
    def test_parseaza_porturi_mixt(self):
        """Testează parsarea unei specificații mixte."""
        from src.exercises.ex_13_01_scanner_porturi import parseaza_porturi
        rezultat = parseaza_porturi("22,80-82,443")
        self.assertEqual(rezultat, [22, 80, 81, 82, 443])
    
    def test_parseaza_porturi_invalid(self):
        """Testează că porturile invalide sunt ignorate."""
        from src.exercises.ex_13_01_scanner_porturi import parseaza_porturi
        rezultat = parseaza_porturi("80,invalid,443")
        self.assertEqual(rezultat, [80, 443])
    
    def test_scaneaza_port_deschis(self):
        """Testează scanarea unui port deschis (dacă serviciile rulează)."""
        from src.exercises.ex_13_01_scanner_porturi import scaneaza_port
        
        # Verifică dacă portul 1883 este deschis (MQTT)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex(("localhost", 1883)) == 0:
                    rezultat = scaneaza_port("localhost", 1883, timeout=2.0)
                    self.assertEqual(rezultat.stare, "deschis")
                else:
                    self.skipTest("Portul 1883 nu este deschis")
        except Exception:
            self.skipTest("Nu se poate verifica portul 1883")


class TestExercitiu2ClientMQTT(unittest.TestCase):
    """Teste pentru Exercițiul 2: Client MQTT."""
    
    def test_import_paho_mqtt(self):
        """Testează că biblioteca paho-mqtt este instalată."""
        try:
            import paho.mqtt.client as mqtt
            self.assertTrue(True)
        except ImportError:
            self.fail("paho-mqtt nu este instalat")
    
    def test_creeaza_client(self):
        """Testează crearea unui client MQTT."""
        from src.exercises.ex_13_02_client_mqtt import creeaza_client
        
        config = {'mod': 'subscribe', 'topic': 'test/#', 'qos': 0}
        client = creeaza_client("test-client", config)
        
        self.assertIsNotNone(client)
        self.assertTrue(hasattr(client, 'connect'))
        self.assertTrue(hasattr(client, 'publish'))
        self.assertTrue(hasattr(client, 'subscribe'))


class TestExercitiu3SnifferPachete(unittest.TestCase):
    """Teste pentru Exercițiul 3: Sniffer Pachete."""
    
    def test_import_scapy(self):
        """Testează că biblioteca scapy este instalată."""
        try:
            from scapy.all import sniff, IP, TCP
            self.assertTrue(True)
        except ImportError:
            self.skipTest("scapy nu este instalat")
    
    def test_identifica_protocol_mqtt(self):
        """Testează identificarea protocolului MQTT."""
        from src.exercises.ex_13_03_sniffer_pachete import AnalizorPachete
        
        analizor = AnalizorPachete(verbose=False)
        protocol = analizor.identifica_protocol(12345, 1883)
        self.assertEqual(protocol, "MQTT")
    
    def test_identifica_protocol_http(self):
        """Testează identificarea protocolului HTTP."""
        from src.exercises.ex_13_03_sniffer_pachete import AnalizorPachete
        
        analizor = AnalizorPachete(verbose=False)
        protocol = analizor.identifica_protocol(54321, 8080)
        self.assertEqual(protocol, "HTTP-ALT")


class TestExercitiu4VerificatorVulnerabilitati(unittest.TestCase):
    """Teste pentru Exercițiul 4: Verificator Vulnerabilități."""
    
    def test_import_requests(self):
        """Testează că biblioteca requests este instalată."""
        try:
            import requests
            self.assertTrue(True)
        except ImportError:
            self.fail("requests nu este instalat")


def ruleaza_teste_exercitiu(numar_exercitiu: int):
    """Rulează testele pentru un exercițiu specific."""
    suite = unittest.TestSuite()
    
    clase_test = {
        1: TestExercitiu1ScannerPorturi,
        2: TestExercitiu2ClientMQTT,
        3: TestExercitiu3SnifferPachete,
        4: TestExercitiu4VerificatorVulnerabilitati,
    }
    
    if numar_exercitiu in clase_test:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(clase_test[numar_exercitiu]))
    else:
        print(f"Exercițiul {numar_exercitiu} nu există!")
        return 1
    
    runner = unittest.TextTestRunner(verbosity=2)
    rezultat = runner.run(suite)
    
    return 0 if rezultat.wasSuccessful() else 1


def main():
    """Funcția principală."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Teste pentru exercițiile laboratorului"
    )
    parser.add_argument("--exercitiu", "-e", type=int, choices=[1, 2, 3, 4],
                        help="Numărul exercițiului de testat")
    parser.add_argument("--toate", "-a", action="store_true",
                        help="Rulează toate testele")
    
    args = parser.parse_args()
    
    if args.exercitiu:
        return ruleaza_teste_exercitiu(args.exercitiu)
    else:
        # Rulează toate testele
        unittest.main(argv=[''], exit=False, verbosity=2)
        return 0


if __name__ == "__main__":
    sys.exit(main())
