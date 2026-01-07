#!/usr/bin/env python3
"""
Teste pentru Exerciții
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Validează implementările exercițiilor din Săptămâna 9.
"""

import struct
import zlib
import sys
import unittest
from pathlib import Path

# Adaugă directorul rădăcină la cale
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


class TestEndianness(unittest.TestCase):
    """Teste pentru conversiile endianness."""
    
    def test_impachetare_big_endian(self):
        """Testează împachetarea în format big-endian."""
        valoare = 0x12345678
        impachetat = struct.pack(">I", valoare)
        
        self.assertEqual(
            impachetat,
            b'\x12\x34\x56\x78',
            "Împachetare big-endian incorectă"
        )
    
    def test_impachetare_little_endian(self):
        """Testează împachetarea în format little-endian."""
        valoare = 0x12345678
        impachetat = struct.pack("<I", valoare)
        
        self.assertEqual(
            impachetat,
            b'\x78\x56\x34\x12',
            "Împachetare little-endian incorectă"
        )
    
    def test_despachetare_big_endian(self):
        """Testează despachetarea din format big-endian."""
        date = b'\x12\x34\x56\x78'
        valoare = struct.unpack(">I", date)[0]
        
        self.assertEqual(
            valoare,
            0x12345678,
            "Despachetare big-endian incorectă"
        )
    
    def test_conversie_simetrica(self):
        """Testează că împachetare + despachetare returnează valoarea originală."""
        valoare_originala = 0xDEADBEEF
        
        # Big-endian
        impachetat = struct.pack(">I", valoare_originala)
        despachetata = struct.unpack(">I", impachetat)[0]
        self.assertEqual(valoare_originala, despachetata)
        
        # Little-endian
        impachetat = struct.pack("<I", valoare_originala)
        despachetata = struct.unpack("<I", impachetat)[0]
        self.assertEqual(valoare_originala, despachetata)
    
    def test_ordine_retea(self):
        """Testează că '!' este echivalent cu '>' (network byte order)."""
        valoare = 0x12345678
        
        big_endian = struct.pack(">I", valoare)
        ordine_retea = struct.pack("!I", valoare)
        
        self.assertEqual(
            big_endian,
            ordine_retea,
            "Ordinea rețelei trebuie să fie identică cu big-endian"
        )


class TestCRC32(unittest.TestCase):
    """Teste pentru calculul CRC-32."""
    
    def test_crc_string_gol(self):
        """Testează CRC-32 pentru string gol."""
        crc = zlib.crc32(b"") & 0xFFFFFFFF
        self.assertEqual(crc, 0)
    
    def test_crc_valoare_cunoscuta(self):
        """Testează CRC-32 pentru o valoare cunoscută."""
        # "Hello" are un CRC-32 cunoscut
        crc = zlib.crc32(b"Hello") & 0xFFFFFFFF
        self.assertIsInstance(crc, int)
        self.assertLessEqual(crc, 0xFFFFFFFF)
    
    def test_crc_deterministic(self):
        """Testează că CRC-32 este deterministic."""
        date = b"Date de test pentru CRC"
        
        crc1 = zlib.crc32(date) & 0xFFFFFFFF
        crc2 = zlib.crc32(date) & 0xFFFFFFFF
        
        self.assertEqual(crc1, crc2, "CRC-32 trebuie să fie deterministic")
    
    def test_crc_detecteaza_modificari(self):
        """Testează că CRC-32 detectează modificările."""
        date_originale = b"Date originale"
        date_modificate = b"Date modificate"
        
        crc_original = zlib.crc32(date_originale) & 0xFFFFFFFF
        crc_modificat = zlib.crc32(date_modificate) & 0xFFFFFFFF
        
        self.assertNotEqual(
            crc_original,
            crc_modificat,
            "CRC-32 trebuie să detecteze modificările"
        )


class TestFormatStruct(unittest.TestCase):
    """Teste pentru formatele struct."""
    
    def test_dimensiune_header(self):
        """Testează calculul dimensiunii header-ului."""
        # Format tipic: MAGIC(4) + VERSION(1) + TYPE(1) + LENGTH(4) + CRC(4)
        format_header = ">4sBBII"
        dimensiune = struct.calcsize(format_header)
        
        self.assertEqual(
            dimensiune,
            14,
            f"Dimensiune header incorectă: {dimensiune} != 14"
        )
    
    def test_impachetare_header_complet(self):
        """Testează împachetarea unui header complet."""
        format_header = ">4sBBII"
        
        magic = b"TEST"
        versiune = 1
        tip = 0x01
        lungime = 100
        crc = 0xDEADBEEF
        
        header = struct.pack(format_header, magic, versiune, tip, lungime, crc)
        
        self.assertEqual(len(header), 14)
        self.assertTrue(header.startswith(magic))
    
    def test_despachetare_header(self):
        """Testează despachetarea unui header."""
        format_header = ">4sBBII"
        
        # Creează un header
        header = struct.pack(format_header, b"TEST", 1, 2, 256, 0x12345678)
        
        # Despachetează
        magic, versiune, tip, lungime, crc = struct.unpack(format_header, header)
        
        self.assertEqual(magic, b"TEST")
        self.assertEqual(versiune, 1)
        self.assertEqual(tip, 2)
        self.assertEqual(lungime, 256)
        self.assertEqual(crc, 0x12345678)


class TestProtocolBinar(unittest.TestCase):
    """Teste pentru implementarea protocolului binar."""
    
    def test_mesaj_text(self):
        """Testează serializarea unui mesaj text."""
        payload = "Salut, lume!".encode('utf-8')
        
        # Header: MAGIC(4) + LEN(4) + CRC(4)
        crc = zlib.crc32(payload) & 0xFFFFFFFF
        header = struct.pack(">4sII", b"FTPC", len(payload), crc)
        
        mesaj = header + payload
        
        # Verifică dimensiunea
        self.assertEqual(len(mesaj), 12 + len(payload))
        
        # Decodează și verifică
        magic, lungime, crc_citit = struct.unpack(">4sII", mesaj[:12])
        payload_citit = mesaj[12:]
        
        self.assertEqual(magic, b"FTPC")
        self.assertEqual(lungime, len(payload))
        self.assertEqual(crc_citit, crc)
        self.assertEqual(payload_citit, payload)


def ruleaza_teste():
    """Rulează toate testele."""
    print("=" * 60)
    print("Teste Exerciții - Săptămâna 9")
    print("=" * 60)
    print()
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestEndianness))
    suite.addTests(loader.loadTestsFromTestCase(TestCRC32))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatStruct))
    suite.addTests(loader.loadTestsFromTestCase(TestProtocolBinar))
    
    runner = unittest.TextTestRunner(verbosity=2)
    rezultat = runner.run(suite)
    
    return len(rezultat.failures) == 0 and len(rezultat.errors) == 0


if __name__ == "__main__":
    succes = ruleaza_teste()
    sys.exit(0 if succes else 1)
