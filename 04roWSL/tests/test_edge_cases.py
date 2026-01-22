#!/usr/bin/env python3
"""
Teste Edge Cases pentru Protocoale
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Teste pentru cazuri limită și situații neobișnuite.
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
    impacheteaza_binar,
    despacheteaza_binar,
    impacheteaza_senzor,
    despacheteaza_senzor,
    TipMesajBinar,
    BINAR_MAX_PAYLOAD,
    BINAR_MAX_SECVENTA,
    SENZOR_DIMENSIUNE,
)


class TestePayloadExtrem(unittest.TestCase):
    """Teste pentru payload-uri de dimensiuni extreme."""
    
    def test_payload_gol(self):
        """Verifică comportamentul cu payload gol."""
        msg = impacheteaza_binar(TipMesajBinar.PING, b'', 1)
        rezultat = despacheteaza_binar(msg)
        
        self.assertIsNotNone(rezultat)
        self.assertTrue(rezultat.crc_valid)
        self.assertEqual(rezultat.lungime, 0)
        self.assertEqual(rezultat.payload, b'')
    
    def test_payload_un_byte(self):
        """Verifică comportamentul cu payload de 1 byte."""
        msg = impacheteaza_binar(TipMesajBinar.RESPONSE, b'X', 1)
        rezultat = despacheteaza_binar(msg)
        
        self.assertIsNotNone(rezultat)
        self.assertTrue(rezultat.crc_valid)
        self.assertEqual(rezultat.payload, b'X')
    
    def test_payload_mare(self):
        """Verifică comportamentul cu payload mare (1000 bytes)."""
        payload = b'X' * 1000
        msg = impacheteaza_binar(TipMesajBinar.SET, payload, 1)
        rezultat = despacheteaza_binar(msg)
        
        self.assertIsNotNone(rezultat)
        self.assertTrue(rezultat.crc_valid)
        self.assertEqual(len(rezultat.payload), 1000)
    
    def test_payload_maxim(self):
        """Verifică comportamentul cu payload de 65535 bytes (maxim)."""
        payload = b'Y' * BINAR_MAX_PAYLOAD
        msg = impacheteaza_binar(TipMesajBinar.SET, payload, 1)
        rezultat = despacheteaza_binar(msg)
        
        self.assertIsNotNone(rezultat)
        self.assertTrue(rezultat.crc_valid)
        self.assertEqual(len(rezultat.payload), BINAR_MAX_PAYLOAD)
    
    def test_payload_peste_maxim(self):
        """Verifică că payload peste maxim ridică excepție."""
        payload = b'Z' * (BINAR_MAX_PAYLOAD + 1)
        
        with self.assertRaises(ValueError):
            impacheteaza_binar(TipMesajBinar.SET, payload, 1)


class TesteSecventaExtrem(unittest.TestCase):
    """Teste pentru valori extreme ale secvenței."""
    
    def test_secventa_zero(self):
        """Verifică comportamentul cu secvență 0."""
        msg = impacheteaza_binar(TipMesajBinar.PING, b'', 0)
        rezultat = despacheteaza_binar(msg)
        
        self.assertIsNotNone(rezultat)
        self.assertEqual(rezultat.secventa, 0)
    
    def test_secventa_maxima(self):
        """Verifică comportamentul cu secvență maximă (0xFFFFFFFF)."""
        msg = impacheteaza_binar(TipMesajBinar.PING, b'', BINAR_MAX_SECVENTA)
        rezultat = despacheteaza_binar(msg)
        
        self.assertIsNotNone(rezultat)
        self.assertEqual(rezultat.secventa, BINAR_MAX_SECVENTA)
    
    def test_secventa_peste_maxim(self):
        """Verifică că secvență peste maxim ridică excepție."""
        with self.assertRaises(ValueError):
            impacheteaza_binar(TipMesajBinar.PING, b'', BINAR_MAX_SECVENTA + 1)
    
    def test_secventa_negativa(self):
        """Verifică că secvență negativă ridică excepție."""
        with self.assertRaises(ValueError):
            impacheteaza_binar(TipMesajBinar.PING, b'', -1)


class TesteCRCIntegritate(unittest.TestCase):
    """Teste pentru verificarea integrității CRC."""
    
    def test_crc_detecteaza_bit_flip_antet(self):
        """Verifică că CRC detectează modificarea unui bit în antet."""
        msg = impacheteaza_binar(TipMesajBinar.PING, b'', 1)
        msg_corupt = bytearray(msg)
        msg_corupt[5] ^= 0x01  # Flip un bit în antet
        
        rezultat = despacheteaza_binar(bytes(msg_corupt))
        
        # Poate să returneze None (magic invalid) sau crc_valid=False
        if rezultat is not None:
            self.assertFalse(rezultat.crc_valid)
    
    def test_crc_detecteaza_bit_flip_payload(self):
        """Verifică că CRC detectează modificarea unui bit în payload."""
        msg = impacheteaza_binar(TipMesajBinar.RESPONSE, b'Hello', 1)
        msg_corupt = bytearray(msg)
        msg_corupt[14] ^= 0x01  # Flip un bit în payload
        
        rezultat = despacheteaza_binar(bytes(msg_corupt))
        
        self.assertIsNotNone(rezultat)
        self.assertFalse(rezultat.crc_valid)
    
    def test_crc_detecteaza_swap_bytes(self):
        """Verifică că CRC detectează schimbarea a doi bytes."""
        msg = impacheteaza_binar(TipMesajBinar.RESPONSE, b'ABCDEF', 1)
        msg_corupt = bytearray(msg)
        # Swap doi bytes în payload
        msg_corupt[14], msg_corupt[15] = msg_corupt[15], msg_corupt[14]
        
        rezultat = despacheteaza_binar(bytes(msg_corupt))
        
        self.assertIsNotNone(rezultat)
        self.assertFalse(rezultat.crc_valid)
    
    def test_crc_valoare_standard(self):
        """Verifică CRC32 cu valoarea standard de test."""
        # Valoarea CRC32 pentru "123456789" trebuie să fie 0xCBF43926
        crc = calculeaza_crc32(b"123456789")
        self.assertEqual(crc, 0xCBF43926)


class TesteSenzorEdgeCases(unittest.TestCase):
    """Teste pentru cazuri limită ale protocolului senzor."""
    
    def test_locatie_goala(self):
        """Verifică comportamentul cu locație goală."""
        dg = impacheteaza_senzor(1, 25.0, "")
        rez = despacheteaza_senzor(dg)
        
        self.assertIsNotNone(rez)
        self.assertTrue(rez.crc_valid)
        self.assertEqual(rez.locatie, "")
    
    def test_locatie_exact_10_caractere(self):
        """Verifică comportamentul cu locație de exact 10 caractere."""
        dg = impacheteaza_senzor(1, 25.0, "1234567890")
        rez = despacheteaza_senzor(dg)
        
        self.assertIsNotNone(rez)
        self.assertTrue(rez.crc_valid)
        self.assertEqual(rez.locatie, "1234567890")
    
    def test_locatie_peste_10_caractere(self):
        """Verifică că locația se trunchiază la 10 caractere."""
        dg = impacheteaza_senzor(1, 25.0, "12345678901234567890")
        rez = despacheteaza_senzor(dg)
        
        self.assertIsNotNone(rez)
        self.assertTrue(rez.crc_valid)
        # Locația trebuie să fie trunchiată la 10 caractere
        self.assertEqual(len(rez.locatie), 10)
    
    def test_locatie_unicode(self):
        """Verifică comportamentul cu caractere Unicode în locație."""
        # "București" are 9 caractere dar 10 bytes în UTF-8 (ș = 2 bytes)
        dg = impacheteaza_senzor(1, 25.0, "București")
        rez = despacheteaza_senzor(dg)
        
        self.assertIsNotNone(rez)
        self.assertTrue(rez.crc_valid)
        # Locația trebuie să se încadreze în 10 bytes UTF-8
    
    def test_temperatura_negativa(self):
        """Verifică comportamentul cu temperatură negativă."""
        dg = impacheteaza_senzor(1, -40.0, "Congelator")
        rez = despacheteaza_senzor(dg)
        
        self.assertIsNotNone(rez)
        self.assertTrue(rez.crc_valid)
        self.assertAlmostEqual(rez.temperatura, -40.0, places=2)
    
    def test_temperatura_foarte_mare(self):
        """Verifică comportamentul cu temperatură foarte mare."""
        dg = impacheteaza_senzor(1, 1000.0, "Cuptor")
        rez = despacheteaza_senzor(dg)
        
        self.assertIsNotNone(rez)
        self.assertTrue(rez.crc_valid)
        self.assertAlmostEqual(rez.temperatura, 1000.0, places=1)
    
    def test_sensor_id_maxim(self):
        """Verifică comportamentul cu sensor_id maxim (65535)."""
        dg = impacheteaza_senzor(65535, 25.0, "Test")
        rez = despacheteaza_senzor(dg)
        
        self.assertIsNotNone(rez)
        self.assertTrue(rez.crc_valid)
        self.assertEqual(rez.sensor_id, 65535)
    
    def test_sensor_id_zero(self):
        """Verifică comportamentul cu sensor_id 0."""
        dg = impacheteaza_senzor(0, 25.0, "Test")
        rez = despacheteaza_senzor(dg)
        
        self.assertIsNotNone(rez)
        self.assertTrue(rez.crc_valid)
        self.assertEqual(rez.sensor_id, 0)
    
    def test_dimensiune_datagrama(self):
        """Verifică că datagrama are exact 23 bytes."""
        dg = impacheteaza_senzor(1, 25.0, "Test")
        self.assertEqual(len(dg), SENZOR_DIMENSIUNE)


class TesteMesajeInvalide(unittest.TestCase):
    """Teste pentru mesaje invalide sau malformate."""
    
    def test_mesaj_prea_scurt(self):
        """Verifică comportamentul cu mesaj prea scurt."""
        rezultat = despacheteaza_binar(b'NP123456789')  # 11 bytes < 14
        self.assertIsNone(rezultat)
    
    def test_mesaj_magic_invalid(self):
        """Verifică comportamentul cu magic invalid."""
        # Construiește un mesaj cu magic greșit
        mesaj = b'XX' + b'\x01' + b'\x01' + b'\x00\x00' + b'\x00\x00\x00\x01' + b'\x00\x00\x00\x00'
        rezultat = despacheteaza_binar(mesaj)
        self.assertIsNone(rezultat)
    
    def test_datagrama_senzor_prea_scurta(self):
        """Verifică comportamentul cu datagramă senzor prea scurtă."""
        rezultat = despacheteaza_senzor(b'1234567890123456789012')  # 22 bytes < 23
        self.assertIsNone(rezultat)
    
    def test_datagrama_senzor_prea_lunga(self):
        """Verifică comportamentul cu datagramă senzor prea lungă."""
        rezultat = despacheteaza_senzor(b'123456789012345678901234')  # 24 bytes > 23
        self.assertIsNone(rezultat)


class TesteConsistenta(unittest.TestCase):
    """Teste pentru consistența operațiilor pack/unpack."""
    
    def test_round_trip_binar(self):
        """Verifică că pack + unpack returnează datele originale."""
        for tip in [TipMesajBinar.PING, TipMesajBinar.SET, TipMesajBinar.ERROR]:
            for payload in [b'', b'test', b'a' * 100]:
                for seq in [0, 1, 12345, BINAR_MAX_SECVENTA]:
                    with self.subTest(tip=tip, payload_len=len(payload), seq=seq):
                        msg = impacheteaza_binar(tip, payload, seq)
                        rez = despacheteaza_binar(msg)
                        
                        self.assertIsNotNone(rez)
                        self.assertTrue(rez.crc_valid)
                        self.assertEqual(rez.tip, tip)
                        self.assertEqual(rez.payload, payload)
                        self.assertEqual(rez.secventa, seq)
    
    def test_round_trip_senzor(self):
        """Verifică că pack + unpack returnează datele originale pentru senzor."""
        test_cases = [
            (1, 25.0, "Lab1"),
            (100, -10.5, "Frigider"),
            (65535, 100.0, "1234567890"),
            (0, 0.0, ""),
        ]
        
        for sensor_id, temp, loc in test_cases:
            with self.subTest(sensor_id=sensor_id, temp=temp, loc=loc):
                dg = impacheteaza_senzor(sensor_id, temp, loc)
                rez = despacheteaza_senzor(dg)
                
                self.assertIsNotNone(rez)
                self.assertTrue(rez.crc_valid)
                self.assertEqual(rez.sensor_id, sensor_id)
                self.assertAlmostEqual(rez.temperatura, temp, places=2)
                # Locația poate fi trunchiată
                self.assertEqual(rez.locatie, loc[:10])


if __name__ == "__main__":
    unittest.main(verbosity=2)
