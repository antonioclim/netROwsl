#!/usr/bin/env python3
"""
================================================================================
Teste Unitare - Laborator Săptămâna 13
================================================================================
IoT și Securitate în Rețelele de Calculatoare

Aceste teste verifică funcționalitatea corectă a modulelor din exerciții.
Rulare: python3 -m pytest tests/test_unitare.py -v
Sau:    python3 tests/test_unitare.py

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
================================================================================
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from dataclasses import asdict

# Adaugă rădăcina proiectului în PATH
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


# ==============================================================================
# TESTE PENTRU EX_13_01: SCANNER PORTURI
# ==============================================================================

class TestParseazaPorturi(unittest.TestCase):
    """Teste pentru funcția parseaza_porturi din scanner."""
    
    @classmethod
    def setUpClass(cls):
        """Importă modulul o singură dată."""
        from src.exercises.ex_13_01_scanner_porturi import parseaza_porturi
        cls.parseaza_porturi = staticmethod(parseaza_porturi)
    
    def test_port_singur(self):
        """Verifică parsarea unui singur port."""
        rezultat = self.parseaza_porturi("80")
        self.assertEqual(rezultat, [80])
    
    def test_porturi_multiple_virgula(self):
        """Verifică parsarea porturilor separate prin virgulă."""
        rezultat = self.parseaza_porturi("22,80,443")
        self.assertEqual(rezultat, [22, 80, 443])
    
    def test_interval_porturi(self):
        """Verifică parsarea unui interval de porturi."""
        rezultat = self.parseaza_porturi("80-83")
        self.assertEqual(rezultat, [80, 81, 82, 83])
    
    def test_combinatie_porturi_si_intervale(self):
        """Verifică parsarea combinată."""
        rezultat = self.parseaza_porturi("22,80-82,443")
        self.assertEqual(rezultat, [22, 80, 81, 82, 443])
    
    def test_porturi_duplicate_eliminate(self):
        """Verifică eliminarea duplicatelor."""
        rezultat = self.parseaza_porturi("80,80,80")
        self.assertEqual(rezultat, [80])
    
    def test_port_zero_ignorat(self):
        """Verifică că portul 0 este ignorat."""
        rezultat = self.parseaza_porturi("0,80")
        self.assertEqual(rezultat, [80])
    
    def test_port_peste_65535_ignorat(self):
        """Verifică că porturile > 65535 sunt ignorate."""
        rezultat = self.parseaza_porturi("80,70000")
        self.assertEqual(rezultat, [80])
    
    def test_sir_gol(self):
        """Verifică comportamentul cu șir gol."""
        rezultat = self.parseaza_porturi("")
        self.assertEqual(rezultat, [])
    
    def test_spatii_tolerate(self):
        """Verifică că spațiile sunt tolerate."""
        rezultat = self.parseaza_porturi("22, 80, 443")
        self.assertEqual(rezultat, [22, 80, 443])
    
    def test_rezultat_sortat(self):
        """Verifică că rezultatul este sortat."""
        rezultat = self.parseaza_porturi("443,22,80")
        self.assertEqual(rezultat, [22, 80, 443])


class TestParseazaTinte(unittest.TestCase):
    """Teste pentru funcția parseaza_tinte din scanner."""
    
    @classmethod
    def setUpClass(cls):
        """Importă modulul o singură dată."""
        from src.exercises.ex_13_01_scanner_porturi import parseaza_tinte
        cls.parseaza_tinte = staticmethod(parseaza_tinte)
    
    def test_ip_singur(self):
        """Verifică parsarea unui singur IP."""
        rezultat = self.parseaza_tinte("192.168.1.1")
        self.assertEqual(rezultat, ["192.168.1.1"])
    
    def test_hostname(self):
        """Verifică parsarea unui hostname."""
        rezultat = self.parseaza_tinte("localhost")
        self.assertEqual(rezultat, ["localhost"])
    
    def test_interval_ip(self):
        """Verifică parsarea unui interval de IP-uri."""
        rezultat = self.parseaza_tinte("192.168.1.1-3")
        self.assertEqual(rezultat, ["192.168.1.1", "192.168.1.2", "192.168.1.3"])
    
    def test_cidr_mic(self):
        """Verifică parsarea unei rețele CIDR mici."""
        rezultat = self.parseaza_tinte("192.168.1.0/30")
        # /30 = 4 adrese, 2 hosts (fără network și broadcast)
        self.assertEqual(len(rezultat), 2)
        self.assertIn("192.168.1.1", rezultat)
        self.assertIn("192.168.1.2", rezultat)


class TestRezultatPort(unittest.TestCase):
    """Teste pentru dataclass RezultatPort."""
    
    @classmethod
    def setUpClass(cls):
        """Importă modulul o singură dată."""
        from src.exercises.ex_13_01_scanner_porturi import RezultatPort
        cls.RezultatPort = RezultatPort
    
    def test_creare_rezultat_minim(self):
        """Verifică crearea cu câmpuri obligatorii."""
        rez = self.RezultatPort(port=80, stare="deschis", serviciu="HTTP")
        self.assertEqual(rez.port, 80)
        self.assertEqual(rez.stare, "deschis")
        self.assertEqual(rez.serviciu, "HTTP")
        self.assertIsNone(rez.banner)
        self.assertIsNone(rez.timp_raspuns_ms)
    
    def test_creare_rezultat_complet(self):
        """Verifică crearea cu toate câmpurile."""
        rez = self.RezultatPort(
            port=80,
            stare="deschis",
            serviciu="HTTP",
            banner="nginx/1.18.0",
            timp_raspuns_ms=5.23
        )
        self.assertEqual(rez.banner, "nginx/1.18.0")
        self.assertEqual(rez.timp_raspuns_ms, 5.23)
    
    def test_conversie_dict(self):
        """Verifică conversia în dicționar."""
        rez = self.RezultatPort(port=80, stare="deschis", serviciu="HTTP")
        d = asdict(rez)
        self.assertIsInstance(d, dict)
        self.assertEqual(d["port"], 80)


# ==============================================================================
# TESTE PENTRU EX_13_02: CLIENT MQTT
# ==============================================================================

class TestCallbackuriMQTT(unittest.TestCase):
    """Teste pentru callback-urile MQTT."""
    
    @classmethod
    def setUpClass(cls):
        """Importă modulul o singură dată."""
        from src.exercises.ex_13_02_client_mqtt import la_conectare, la_mesaj
        cls.la_conectare = staticmethod(la_conectare)
        cls.la_mesaj = staticmethod(la_mesaj)
    
    def test_la_conectare_succes(self):
        """Verifică callback la conectare reușită."""
        mock_client = MagicMock()
        mock_client.subscribe = MagicMock()
        
        userdata = {'mod': 'subscribe', 'topic': 'test/#', 'qos': 0}
        
        # rc=0 înseamnă succes
        with patch('builtins.print'):
            self.la_conectare(mock_client, userdata, {}, 0)
        
        # Verifică că s-a apelat subscribe
        mock_client.subscribe.assert_called_once_with('test/#', 0)
    
    def test_la_conectare_eroare(self):
        """Verifică callback la eroare de conectare."""
        mock_client = MagicMock()
        
        # rc=4 înseamnă credențiale invalide
        with patch('builtins.print') as mock_print:
            self.la_conectare(mock_client, None, {}, 4)
        
        # Verifică că NU s-a apelat subscribe
        mock_client.subscribe.assert_not_called()


# ==============================================================================
# TESTE PENTRU EX_13_04: VERIFICATOR VULNERABILITĂȚI
# ==============================================================================

class TestVulnerabilitate(unittest.TestCase):
    """Teste pentru dataclass Vulnerabilitate."""
    
    @classmethod
    def setUpClass(cls):
        """Importă modulul o singură dată."""
        from src.exercises.ex_13_04_verificator_vulnerabilitati import Vulnerabilitate
        cls.Vulnerabilitate = Vulnerabilitate
    
    def test_creare_vulnerabilitate(self):
        """Verifică crearea unei vulnerabilități."""
        vuln = self.Vulnerabilitate(
            serviciu="FTP",
            port=21,
            severitate="CRITIC",
            titlu="Backdoor detectat",
            descriere="Portul 6200 răspunde la conexiuni"
        )
        self.assertEqual(vuln.serviciu, "FTP")
        self.assertEqual(vuln.severitate, "CRITIC")
        self.assertIsNone(vuln.cve)
    
    def test_creare_cu_cve(self):
        """Verifică crearea cu CVE."""
        vuln = self.Vulnerabilitate(
            serviciu="FTP",
            port=21,
            severitate="CRITIC",
            titlu="vsftpd backdoor",
            descriere="Vulnerabilitate cunoscută",
            cve="CVE-2011-2523",
            remediere="Actualizează la versiunea curentă"
        )
        self.assertEqual(vuln.cve, "CVE-2011-2523")
        self.assertEqual(vuln.remediere, "Actualizează la versiunea curentă")


class TestSeveritate(unittest.TestCase):
    """Teste pentru constantele de severitate."""
    
    def test_severitati_definite(self):
        """Verifică că toate severitățile sunt definite."""
        from src.exercises.ex_13_04_verificator_vulnerabilitati import Severitate
        
        self.assertEqual(Severitate.CRITIC, "CRITIC")
        self.assertEqual(Severitate.RIDICAT, "RIDICAT")
        self.assertEqual(Severitate.MEDIU, "MEDIU")
        self.assertEqual(Severitate.SCAZUT, "SCĂZUT")
        self.assertEqual(Severitate.INFO, "INFO")


# ==============================================================================
# TESTE UTILITARE
# ==============================================================================

class TestUtilitareRetea(unittest.TestCase):
    """Teste pentru utilitarele de rețea."""
    
    def test_import_utilitare(self):
        """Verifică că modulul se importă corect."""
        try:
            from scripts.utils import utilitare_retea
            self.assertTrue(hasattr(utilitare_retea, 'verifica_port'))
        except ImportError:
            self.skipTest("Modulul utilitare_retea nu este disponibil")


class TestUtilitareDocker(unittest.TestCase):
    """Teste pentru utilitarele Docker."""
    
    def test_import_utilitare(self):
        """Verifică că modulul se importă corect."""
        try:
            from scripts.utils import utilitare_docker
            self.assertTrue(hasattr(utilitare_docker, 'ManagerDocker'))
        except ImportError:
            self.skipTest("Modulul utilitare_docker nu este disponibil")


# ==============================================================================
# TESTE DE STRUCTURĂ
# ==============================================================================

class TestStructuraProiect(unittest.TestCase):
    """Verifică structura corectă a proiectului."""
    
    def test_fisiere_exercitii_exista(self):
        """Verifică că toate fișierele de exerciții există."""
        exercitii = [
            "src/exercises/ex_13_01_scanner_porturi.py",
            "src/exercises/ex_13_02_client_mqtt.py",
            "src/exercises/ex_13_03_sniffer_pachete.py",
            "src/exercises/ex_13_04_verificator_vulnerabilitati.py",
        ]
        
        for ex in exercitii:
            cale = RADACINA_PROIECT / ex
            self.assertTrue(cale.exists(), f"Fișierul {ex} nu există")
    
    def test_docker_compose_exista(self):
        """Verifică că docker-compose.yml există."""
        cale = RADACINA_PROIECT / "docker" / "docker-compose.yml"
        self.assertTrue(cale.exists())
    
    def test_readme_exista(self):
        """Verifică că README.md există."""
        cale = RADACINA_PROIECT / "README.md"
        self.assertTrue(cale.exists())
    
    def test_documentatie_exista(self):
        """Verifică că documentația există."""
        docs = [
            "docs/sumar_teorie.md",
            "docs/depanare.md",
            "docs/cheatsheet_comenzi.md",
        ]
        
        for doc in docs:
            cale = RADACINA_PROIECT / doc
            self.assertTrue(cale.exists(), f"Documentul {doc} nu există")


# ==============================================================================
# TESTE DE INTEGRARE (necesită Docker)
# ==============================================================================

class TestIntegrareDocker(unittest.TestCase):
    """Teste de integrare care necesită Docker."""
    
    @classmethod
    def setUpClass(cls):
        """Verifică dacă Docker este disponibil."""
        import subprocess
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=5
            )
            cls.docker_disponibil = (result.returncode == 0)
        except Exception:
            cls.docker_disponibil = False
    
    def test_docker_disponibil(self):
        """Verifică dacă Docker este disponibil (informativ)."""
        if not self.docker_disponibil:
            self.skipTest("Docker nu este disponibil - testele de integrare sunt sărite")
        self.assertTrue(self.docker_disponibil)


# ==============================================================================
# RUNNER
# ==============================================================================

if __name__ == "__main__":
    # Configurare pentru output mai detaliat
    unittest.main(verbosity=2, buffer=True)
