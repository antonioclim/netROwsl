#!/usr/bin/env python3
"""
Teste Unitare pentru Protocoale
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Suite de teste pentru verificarea implementărilor protocoalelor.
"""

import unittest
import struct
import binascii
import sys
from pathlib import Path

# Adaugă rădăcina proiectului la path
RADACINA = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA))

from src.utils.protocol_utils import (
    calculeaza_crc32,
    verifica_crc32,
    impacheteaza_text,
    despacheteaza_text,
    impacheteaza_binar,
    despacheteaza_binar,
    impacheteaza_senzor,
    despacheteaza_senzor,
    TipMesajBinar
)


class TesteCRC32(unittest.TestCase):
    """Teste pentru funcțiile CRC32."""
    
    def test_crc32_valoare_cunoscuta(self):
        """Verifică CRC32 pentru valoarea standard de test."""
        date = b"123456789"
        crc = calculeaza_crc32(date)
        self.assertEqual(crc, 0xCBF43926)
    
    def test_crc32_string_gol(self):
        """Verifică CRC32 pentru string gol."""
        crc = calculeaza_crc32(b"")
        self.assertEqual(crc, 0x00000000)
    
    def test_crc32_consistenta(self):
        """Verifică că CRC32 este consistent pentru aceleași date."""
        date = b"Date de test pentru consistenta"
        crc1 = calculeaza_crc32(date)
        crc2 = calculeaza_crc32(date)
        self.assertEqual(crc1, crc2)
    
    def test_crc32_detecteaza_modificare(self):
        """Verifică că CRC32 detectează modificări."""
        date_originale = b"Date originale"
        date_modificate = b"Date modificate"
        
        crc1 = calculeaza_crc32(date_originale)
        crc2 = calculeaza_crc32(date_modificate)
        
        self.assertNotEqual(crc1, crc2)
    
    def test_verifica_crc32_corect(self):
        """Verifică funcția de verificare cu CRC corect."""
        date = b"Test verificare"
        crc = calculeaza_crc32(date)
        self.assertTrue(verifica_crc32(date, crc))
    
    def test_verifica_crc32_incorect(self):
        """Verifică funcția de verificare cu CRC incorect."""
        date = b"Test verificare"
        crc_gresit = 0x12345678
        self.assertFalse(verifica_crc32(date, crc_gresit))


class TesteProtocolTEXT(unittest.TestCase):
    """Teste pentru protocolul TEXT."""
    
    def test_impachetare_simpla(self):
        """Verifică împachetarea unui mesaj simplu."""
        mesaj = impacheteaza_text("PING")
        self.assertEqual(mesaj, b"4 PING")
    
    def test_impachetare_cu_spatii(self):
        """Verifică împachetarea unui mesaj cu spații."""
        mesaj = impacheteaza_text("SET cheie valoare")
        self.assertEqual(mesaj, b"17 SET cheie valoare")
    
    def test_despachetare_simpla(self):
        """Verifică despachetarea unui mesaj simplu."""
        lungime, continut, rest = despacheteaza_text(b"4 PING")
        self.assertEqual(lungime, 4)
        self.assertEqual(continut, "PING")
        self.assertEqual(rest, b"")
    
    def test_despachetare_cu_rest(self):
        """Verifică despachetarea când există date suplimentare."""
        lungime, continut, rest = despacheteaza_text(b"4 PINGextra")
        self.assertEqual(lungime, 4)
        self.assertEqual(continut, "PING")
        self.assertEqual(rest, b"extra")
    
    def test_despachetare_incompleta(self):
        """Verifică comportamentul pentru date incomplete."""
        lungime, continut, rest = despacheteaza_text(b"10 scurt")
        self.assertIsNone(lungime)
        self.assertIsNone(continut)
    
    def test_ciclu_complet(self):
        """Verifică împachetare și despachetare."""
        mesaj_original = "SET cheie valoare_test"
        impachetat = impacheteaza_text(mesaj_original)
        lungime, continut, rest = despacheteaza_text(impachetat)
        self.assertEqual(continut, mesaj_original)


class TesteProtocolBINAR(unittest.TestCase):
    """Teste pentru protocolul BINAR."""
    
    def test_impachetare_ping(self):
        """Verifică împachetarea unui mesaj PING."""
        mesaj = impacheteaza_binar(TipMesajBinar.PING, b"", 1)
        self.assertEqual(len(mesaj), 14)  # Doar antet
        self.assertTrue(mesaj.startswith(b"NP"))
    
    def test_impachetare_cu_payload(self):
        """Verifică împachetarea unui mesaj cu payload."""
        payload = b"test payload"
        mesaj = impacheteaza_binar(TipMesajBinar.SET, payload, 1)
        self.assertEqual(len(mesaj), 14 + len(payload))
    
    def test_despachetare_ping(self):
        """Verifică despachetarea unui mesaj PING."""
        mesaj = impacheteaza_binar(TipMesajBinar.PING, b"", 42)
        rezultat = despacheteaza_binar(mesaj)
        
        self.assertIsNotNone(rezultat)
        self.assertEqual(rezultat['tip'], TipMesajBinar.PING)
        self.assertEqual(rezultat['secventa'], 42)
        self.assertTrue(rezultat['crc_valid'])
    
    def test_despachetare_cu_payload(self):
        """Verifică despachetarea unui mesaj cu payload."""
        payload = b"date test"
        mesaj = impacheteaza_binar(TipMesajBinar.RESPONSE, payload, 100)
        rezultat = despacheteaza_binar(mesaj)
        
        self.assertEqual(rezultat['payload'], payload)
        self.assertTrue(rezultat['crc_valid'])
    
    def test_detectare_crc_invalid(self):
        """Verifică detectarea CRC invalid."""
        mesaj = bytearray(impacheteaza_binar(TipMesajBinar.PING, b"", 1))
        mesaj[-1] ^= 0xFF  # Corupem ultimul byte
        
        rezultat = despacheteaza_binar(bytes(mesaj))
        self.assertFalse(rezultat['crc_valid'])
    
    def test_magic_invalid(self):
        """Verifică respingerea mesajelor cu magic invalid."""
        mesaj = b"XX" + b"\x00" * 12
        rezultat = despacheteaza_binar(mesaj)
        self.assertIsNone(rezultat)
    
    def test_nume_tipuri_mesaje(self):
        """Verifică denumirile tipurilor de mesaje."""
        self.assertEqual(TipMesajBinar.nume(0x01), "PING")
        self.assertEqual(TipMesajBinar.nume(0x02), "PONG")
        self.assertEqual(TipMesajBinar.nume(0xFF), "ERROR")
        self.assertIn("NECUNOSCUT", TipMesajBinar.nume(0x99))


class TesteProtocolSenzorUDP(unittest.TestCase):
    """Teste pentru protocolul Senzor UDP."""
    
    def test_dimensiune_datagrama(self):
        """Verifică că datagrama are exact 23 de octeți."""
        datagrama = impacheteaza_senzor(1, 25.5, "Lab1")
        self.assertEqual(len(datagrama), 23)
    
    def test_impachetare_despachetare(self):
        """Verifică ciclul complet de împachetare/despachetare."""
        sensor_id = 42
        temperatura = 23.75
        locatie = "Sala101"
        
        datagrama = impacheteaza_senzor(sensor_id, temperatura, locatie)
        rezultat = despacheteaza_senzor(datagrama)
        
        self.assertIsNotNone(rezultat)
        self.assertEqual(rezultat['sensor_id'], sensor_id)
        self.assertAlmostEqual(rezultat['temperatura'], temperatura, places=2)
        self.assertEqual(rezultat['locatie'], locatie)
        self.assertTrue(rezultat['crc_valid'])
    
    def test_locatie_trunchiata(self):
        """Verifică că locația lungă este trunchiată la 10 caractere."""
        locatie_lunga = "LocatieFoarteLunga"
        datagrama = impacheteaza_senzor(1, 20.0, locatie_lunga)
        rezultat = despacheteaza_senzor(datagrama)
        
        self.assertEqual(len(rezultat['locatie']), 10)
        self.assertEqual(rezultat['locatie'], "LocatiFoar")
    
    def test_temperatura_negativa(self):
        """Verifică că temperaturile negative sunt gestionate corect."""
        temperatura = -15.5
        datagrama = impacheteaza_senzor(1, temperatura, "Congelator")
        rezultat = despacheteaza_senzor(datagrama)
        
        self.assertAlmostEqual(rezultat['temperatura'], temperatura, places=2)
    
    def test_crc_invalid(self):
        """Verifică detectarea CRC invalid în datagramă."""
        datagrama = bytearray(impacheteaza_senzor(1, 25.0, "Test"))
        datagrama[18] ^= 0xFF  # Corupem CRC
        
        rezultat = despacheteaza_senzor(bytes(datagrama))
        self.assertFalse(rezultat['crc_valid'])
    
    def test_dimensiune_invalida(self):
        """Verifică respingerea datagramelor cu dimensiune invalidă."""
        rezultat = despacheteaza_senzor(b"prea scurt")
        self.assertIsNone(rezultat)


class TesteIntegrare(unittest.TestCase):
    """Teste de integrare pentru protocoale."""
    
    def test_secvente_multiple_binar(self):
        """Verifică gestionarea secvențelor multiple în protocolul BINAR."""
        mesaje = []
        for i in range(10):
            mesaj = impacheteaza_binar(TipMesajBinar.PING, b"", i)
            mesaje.append(mesaj)
        
        for i, mesaj in enumerate(mesaje):
            rezultat = despacheteaza_binar(mesaj)
            self.assertEqual(rezultat['secventa'], i)
    
    def test_payloaduri_diverse(self):
        """Verifică diverse dimensiuni de payload."""
        dimensiuni = [0, 1, 10, 100, 1000]
        
        for dim in dimensiuni:
            payload = b"X" * dim
            mesaj = impacheteaza_binar(TipMesajBinar.SET, payload, 1)
            rezultat = despacheteaza_binar(mesaj)
            
            self.assertEqual(len(rezultat['payload']), dim)
            self.assertTrue(rezultat['crc_valid'])


if __name__ == "__main__":
    # Rulează testele cu output detaliat
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adaugă toate testele
    suite.addTests(loader.loadTestsFromTestCase(TesteCRC32))
    suite.addTests(loader.loadTestsFromTestCase(TesteProtocolTEXT))
    suite.addTests(loader.loadTestsFromTestCase(TesteProtocolBINAR))
    suite.addTests(loader.loadTestsFromTestCase(TesteProtocolSenzorUDP))
    suite.addTests(loader.loadTestsFromTestCase(TesteIntegrare))
    
    # Rulează cu verbozitate
    runner = unittest.TextTestRunner(verbosity=2)
    rezultat = runner.run(suite)
    
    # Returnează cod de ieșire
    sys.exit(0 if rezultat.wasSuccessful() else 1)
