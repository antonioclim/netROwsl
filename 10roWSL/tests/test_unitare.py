#!/usr/bin/env python3
"""
Teste Unitare pentru Laborator
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Teste care rulează FĂRĂ a necesita Docker sau servicii active.
Verifică funcțiile helper și logica de bază.

Utilizare:
    python tests/test_unitare.py
    python -m pytest tests/test_unitare.py -v
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Adaugă rădăcina proiectului la calea Python
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


class TestConfiguratie(unittest.TestCase):
    """Teste pentru modulul de configurație."""
    
    def test_config_valori_implicite(self):
        """Verifică valorile implicite ale configurației."""
        from scripts.utils.config import config
        
        self.assertEqual(config.PORTAINER_PORT, 9000)
        self.assertEqual(config.SSH_PORT, 2222)
        self.assertEqual(config.FTP_PORT, 2121)
        self.assertEqual(config.WEB_PORT, 8000)
        self.assertEqual(config.DNS_PORT, 5353)
    
    def test_config_credentiale_implicite(self):
        """Verifică credențialele implicite."""
        from scripts.utils.config import config
        
        self.assertEqual(config.PORTAINER_USER, "stud")
        self.assertEqual(config.SSH_USER, "labuser")
        self.assertEqual(config.FTP_USER, "labftp")
    
    def test_config_url_portainer(self):
        """Verifică generarea URL-ului Portainer."""
        from scripts.utils.config import config
        
        url = config.portainer_url()
        self.assertEqual(url, "http://localhost:9000")
    
    def test_config_url_web(self):
        """Verifică generarea URL-ului web."""
        from scripts.utils.config import config
        
        url = config.web_url()
        self.assertEqual(url, "http://localhost:8000")
    
    def test_config_ftp_passive_range(self):
        """Verifică intervalul de porturi pasive FTP."""
        from scripts.utils.config import config
        
        passive_range = config.ftp_passive_range()
        self.assertEqual(passive_range, "30000-30009")
    
    def test_config_to_dict(self):
        """Verifică conversia configurației în dicționar."""
        from scripts.utils.config import config
        
        config_dict = config.to_dict()
        
        self.assertIn("portainer", config_dict)
        self.assertIn("ssh", config_dict)
        self.assertIn("ftp", config_dict)
        self.assertIn("services", config_dict)
        self.assertIn("network", config_dict)
    
    def test_config_retea(self):
        """Verifică configurația rețelei."""
        from scripts.utils.config import config
        
        self.assertEqual(config.LAB_SUBNET, "172.20.0.0/24")
        self.assertEqual(config.LAB_GATEWAY, "172.20.0.1")
        self.assertEqual(config.LAB_NETWORK_NAME, "week10_labnet")


class TestValidarePort(unittest.TestCase):
    """Teste pentru validarea porturilor."""
    
    def test_port_valid_minim(self):
        """Portul 1 este valid."""
        self.assertTrue(self._valideaza_port(1))
    
    def test_port_valid_maxim(self):
        """Portul 65535 este valid."""
        self.assertTrue(self._valideaza_port(65535))
    
    def test_port_valid_comun(self):
        """Porturile comune sunt valide."""
        porturi_comune = [22, 80, 443, 8000, 8080, 9000]
        for port in porturi_comune:
            self.assertTrue(self._valideaza_port(port), f"Portul {port} ar trebui să fie valid")
    
    def test_port_invalid_zero(self):
        """Portul 0 este invalid."""
        self.assertFalse(self._valideaza_port(0))
    
    def test_port_invalid_negativ(self):
        """Porturile negative sunt invalide."""
        self.assertFalse(self._valideaza_port(-1))
        self.assertFalse(self._valideaza_port(-100))
    
    def test_port_invalid_prea_mare(self):
        """Porturile > 65535 sunt invalide."""
        self.assertFalse(self._valideaza_port(65536))
        self.assertFalse(self._valideaza_port(100000))
    
    def test_port_invalid_string(self):
        """String-urile nu sunt porturi valide."""
        self.assertFalse(self._valideaza_port("abc"))
        self.assertFalse(self._valideaza_port("8080"))  # String, nu int
    
    def test_port_invalid_none(self):
        """None nu este port valid."""
        self.assertFalse(self._valideaza_port(None))
    
    @staticmethod
    def _valideaza_port(port) -> bool:
        """Helper pentru validarea porturilor."""
        try:
            port_int = int(port) if port is not None else 0
            return 1 <= port_int <= 65535
        except (ValueError, TypeError):
            return False


class TestValidareIP(unittest.TestCase):
    """Teste pentru validarea adreselor IP."""
    
    def test_ip_valid_localhost(self):
        """127.0.0.1 este valid."""
        self.assertTrue(self._valideaza_ip("127.0.0.1"))
    
    def test_ip_valid_retea_privata(self):
        """Adresele de rețea privată sunt valide."""
        ips_valide = [
            "192.168.1.1",
            "172.20.0.10",
            "10.0.0.1",
            "172.16.0.1"
        ]
        for ip in ips_valide:
            self.assertTrue(self._valideaza_ip(ip), f"IP-ul {ip} ar trebui să fie valid")
    
    def test_ip_valid_extreme(self):
        """Adrese IP la limite."""
        self.assertTrue(self._valideaza_ip("0.0.0.0"))
        self.assertTrue(self._valideaza_ip("255.255.255.255"))
    
    def test_ip_invalid_octet_prea_mare(self):
        """Octeți > 255 sunt invalizi."""
        self.assertFalse(self._valideaza_ip("256.1.1.1"))
        self.assertFalse(self._valideaza_ip("1.1.1.256"))
    
    def test_ip_invalid_format_gresit(self):
        """Formate greșite sunt invalide."""
        ips_invalide = [
            "1.2.3",           # Prea puține octeți
            "1.2.3.4.5",       # Prea mulți octeți
            "a.b.c.d",         # Nu sunt numere
            "192.168.1",       # Incomplet
            "",                # Gol
            "192.168.1.1/24",  # Cu mască (nu e IP simplu)
        ]
        for ip in ips_invalide:
            self.assertFalse(self._valideaza_ip(ip), f"IP-ul '{ip}' ar trebui să fie invalid")
    
    def test_ip_invalid_negativ(self):
        """Octeți negativi sunt invalizi."""
        self.assertFalse(self._valideaza_ip("-1.0.0.1"))
        self.assertFalse(self._valideaza_ip("192.168.-1.1"))
    
    @staticmethod
    def _valideaza_ip(ip: str) -> bool:
        """Helper pentru validarea adreselor IPv4."""
        if not ip or not isinstance(ip, str):
            return False
        
        parti = ip.split(".")
        if len(parti) != 4:
            return False
        
        try:
            for parte in parti:
                octet = int(parte)
                if octet < 0 or octet > 255:
                    return False
            return True
        except ValueError:
            return False


class TestParseazaSubnet(unittest.TestCase):
    """Teste pentru parsarea notației CIDR."""
    
    def test_subnet_valid_24(self):
        """Parsare subnet /24."""
        subnet, mask = self._parseaza_subnet("172.20.0.0/24")
        self.assertEqual(subnet, "172.20.0.0")
        self.assertEqual(mask, 24)
    
    def test_subnet_valid_16(self):
        """Parsare subnet /16."""
        subnet, mask = self._parseaza_subnet("192.168.0.0/16")
        self.assertEqual(subnet, "192.168.0.0")
        self.assertEqual(mask, 16)
    
    def test_subnet_valid_32(self):
        """Parsare subnet /32 (host unic)."""
        subnet, mask = self._parseaza_subnet("10.0.0.1/32")
        self.assertEqual(subnet, "10.0.0.1")
        self.assertEqual(mask, 32)
    
    def test_subnet_invalid_fara_masca(self):
        """Subnet fără mască ridică excepție."""
        with self.assertRaises(ValueError):
            self._parseaza_subnet("172.20.0.0")
    
    def test_subnet_invalid_masca_prea_mare(self):
        """Mască > 32 ridică excepție."""
        with self.assertRaises(ValueError):
            self._parseaza_subnet("172.20.0.0/33")
    
    @staticmethod
    def _parseaza_subnet(cidr: str) -> tuple:
        """Helper pentru parsarea notației CIDR."""
        if "/" not in cidr:
            raise ValueError(f"Notație CIDR invalidă: {cidr}")
        
        parti = cidr.split("/")
        if len(parti) != 2:
            raise ValueError(f"Notație CIDR invalidă: {cidr}")
        
        subnet = parti[0]
        try:
            mask = int(parti[1])
        except ValueError:
            raise ValueError(f"Mască invalidă: {parti[1]}")
        
        if mask < 0 or mask > 32:
            raise ValueError(f"Mască în afara intervalului [0, 32]: {mask}")
        
        return subnet, mask


class TestFormatareMesaje(unittest.TestCase):
    """Teste pentru formatarea mesajelor de log."""
    
    def test_format_eroare_docker(self):
        """Formatare mesaj eroare Docker."""
        mesaj = self._formateaza_eroare("docker", "Cannot connect to Docker daemon")
        self.assertIn("Docker", mesaj)
        self.assertIn("Cannot connect", mesaj)
    
    def test_format_eroare_retea(self):
        """Formatare mesaj eroare rețea."""
        mesaj = self._formateaza_eroare("network", "Connection refused", host="localhost", port=8000)
        self.assertIn("localhost", mesaj)
        self.assertIn("8000", mesaj)
    
    @staticmethod
    def _formateaza_eroare(tip: str, mesaj: str, **kwargs) -> str:
        """Helper pentru formatarea mesajelor de eroare."""
        parti = [f"[{tip.upper()}] {mesaj}"]
        for cheie, valoare in kwargs.items():
            parti.append(f"{cheie}={valoare}")
        return " | ".join(parti)


class TestContainerNaming(unittest.TestCase):
    """Teste pentru convenția de denumire a containerelor."""
    
    def test_nume_container_valid(self):
        """Verifică formatul numelui containerului."""
        nume = self._genereaza_nume_container("web", 10)
        self.assertEqual(nume, "week10_web")
    
    def test_nume_container_sapt_diferita(self):
        """Verifică numele pentru săptămâni diferite."""
        self.assertEqual(self._genereaza_nume_container("dns", 5), "week5_dns")
        self.assertEqual(self._genereaza_nume_container("ssh", 14), "week14_ssh")
    
    def test_nume_container_servicii_multiple(self):
        """Verifică numele pentru servicii diferite."""
        servicii = ["web", "dns", "ssh", "ftp", "debug"]
        for serviciu in servicii:
            nume = self._genereaza_nume_container(serviciu, 10)
            self.assertTrue(nume.startswith("week10_"))
            self.assertTrue(nume.endswith(serviciu))
    
    @staticmethod
    def _genereaza_nume_container(serviciu: str, saptamana: int) -> str:
        """Helper pentru generarea numelor de containere."""
        return f"week{saptamana}_{serviciu}"


class TestHTTPStatusCodes(unittest.TestCase):
    """Teste pentru interpretarea codurilor HTTP."""
    
    def test_succes_codes(self):
        """Codurile 2xx sunt de succes."""
        coduri_succes = [200, 201, 204]
        for cod in coduri_succes:
            self.assertTrue(self._este_succes(cod), f"Codul {cod} ar trebui să fie succes")
    
    def test_redirect_codes(self):
        """Codurile 3xx sunt de redirecționare."""
        coduri_redirect = [301, 302, 304]
        for cod in coduri_redirect:
            self.assertTrue(self._este_redirect(cod), f"Codul {cod} ar trebui să fie redirect")
    
    def test_client_error_codes(self):
        """Codurile 4xx sunt erori client."""
        coduri_eroare = [400, 401, 403, 404, 405]
        for cod in coduri_eroare:
            self.assertTrue(self._este_eroare_client(cod), f"Codul {cod} ar trebui să fie eroare client")
    
    def test_server_error_codes(self):
        """Codurile 5xx sunt erori server."""
        coduri_eroare = [500, 502, 503]
        for cod in coduri_eroare:
            self.assertTrue(self._este_eroare_server(cod), f"Codul {cod} ar trebui să fie eroare server")
    
    @staticmethod
    def _este_succes(cod: int) -> bool:
        return 200 <= cod < 300
    
    @staticmethod
    def _este_redirect(cod: int) -> bool:
        return 300 <= cod < 400
    
    @staticmethod
    def _este_eroare_client(cod: int) -> bool:
        return 400 <= cod < 500
    
    @staticmethod
    def _este_eroare_server(cod: int) -> bool:
        return 500 <= cod < 600


class TestDNSResponseCodes(unittest.TestCase):
    """Teste pentru interpretarea codurilor DNS."""
    
    def test_noerror(self):
        """NOERROR = 0."""
        self.assertEqual(self._cod_dns("NOERROR"), 0)
    
    def test_nxdomain(self):
        """NXDOMAIN = 3."""
        self.assertEqual(self._cod_dns("NXDOMAIN"), 3)
    
    def test_servfail(self):
        """SERVFAIL = 2."""
        self.assertEqual(self._cod_dns("SERVFAIL"), 2)
    
    def test_refused(self):
        """REFUSED = 5."""
        self.assertEqual(self._cod_dns("REFUSED"), 5)
    
    @staticmethod
    def _cod_dns(nume: str) -> int:
        """Returnează codul numeric DNS pentru un nume."""
        coduri = {
            "NOERROR": 0,
            "FORMERR": 1,
            "SERVFAIL": 2,
            "NXDOMAIN": 3,
            "NOTIMP": 4,
            "REFUSED": 5
        }
        return coduri.get(nume, -1)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  TESTE UNITARE - LABORATOR SĂPTĂMÂNA 10")
    print("  (Rulează fără Docker sau servicii active)")
    print("=" * 60)
    print()
    
    # Rulează testele cu verbosity
    unittest.main(verbosity=2)
