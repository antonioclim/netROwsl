#!/usr/bin/env python3
"""
Teste Unitare pentru Utilitarele de Protocol

Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Rulare:
    python -m pytest tests/test_protocol_utils.py -v
    
Sau direct:
    python tests/test_protocol_utils.py
"""

import sys
from pathlib import Path

# Adaugă directorul părinte la path pentru import
sys.path.insert(0, str(Path(__file__).parent.parent))

import struct
import binascii
from typing import Optional

# Încearcă să importe pytest, altfel folosește unittest
try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False
    import unittest


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE PROTOCOL (duplicat din protocol_utils pentru teste independente)
# ═══════════════════════════════════════════════════════════════════════════════

BINAR_MAGIC = b'NP'
BINAR_VERSIUNE = 1
BINAR_DIMENSIUNE_ANTET = 14

# Tipuri mesaje BINAR
class TipMesajBinar:
    PING = 0x01
    PONG = 0x02
    SET = 0x03
    GET = 0x04
    DELETE = 0x05
    RESPONSE = 0x06
    ERROR = 0xFF


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII HELPER (implementare de referință pentru teste)
# ═══════════════════════════════════════════════════════════════════════════════

def calculeaza_crc32(date: bytes) -> int:
    """Calculează CRC32 pentru date."""
    return binascii.crc32(date) & 0xFFFFFFFF


def impacheteaza_binar(tip: int, payload: bytes, secventa: int, 
                       versiune: int = BINAR_VERSIUNE) -> bytes:
    """Construiește un mesaj BINAR complet."""
    lungime = len(payload)
    
    # Antet parțial (fără CRC)
    antet_partial = struct.pack('!2sBBHI',
        BINAR_MAGIC,
        versiune,
        tip,
        lungime,
        secventa
    )
    
    # Calculează CRC peste antet + payload
    crc = calculeaza_crc32(antet_partial + payload)
    
    # Mesaj complet
    mesaj = struct.pack('!2sBBHII',
        BINAR_MAGIC,
        versiune,
        tip,
        lungime,
        secventa,
        crc
    ) + payload
    
    return mesaj


def despacheteaza_binar(date: bytes) -> Optional[dict]:
    """Parsează un mesaj BINAR și verifică CRC."""
    if len(date) < BINAR_DIMENSIUNE_ANTET:
        return None
    
    # Extrage antetul
    magic, versiune, tip, lungime, secventa, crc_primit = struct.unpack(
        '!2sBBHII', date[:BINAR_DIMENSIUNE_ANTET]
    )
    
    # Verifică magic
    if magic != BINAR_MAGIC:
        return None
    
    # Extrage payload
    payload = date[BINAR_DIMENSIUNE_ANTET:BINAR_DIMENSIUNE_ANTET + lungime]
    
    # Verifică CRC
    antet_fara_crc = date[:10]
    crc_calculat = calculeaza_crc32(antet_fara_crc + payload)
    crc_valid = (crc_primit == crc_calculat)
    
    return {
        'versiune': versiune,
        'tip': tip,
        'lungime': lungime,
        'secventa': secventa,
        'crc': crc_primit,
        'crc_valid': crc_valid,
        'payload': payload
    }


def impacheteaza_senzor(sensor_id: int, temperatura: float, locatie: str,
                        versiune: int = 1) -> bytes:
    """Construiește o datagramă de senzor (23 bytes)."""
    # Pregătește locația (10 bytes, padding cu null)
    loc_bytes = locatie.encode('utf-8')[:10]
    loc_padded = loc_bytes + b'\x00' * (10 - len(loc_bytes))
    
    # Partea fără CRC
    parte_fara_crc = struct.pack('!BHf',
        versiune,
        sensor_id,
        temperatura
    ) + loc_padded
    
    # CRC
    crc = calculeaza_crc32(parte_fara_crc)
    
    # Datagrama completă
    datagrama = parte_fara_crc + struct.pack('!I', crc) + b'\x00\x00'
    
    return datagrama


def despacheteaza_senzor(date: bytes) -> Optional[dict]:
    """Parsează o datagramă de senzor."""
    if len(date) != 23:
        return None
    
    versiune, sensor_id, temperatura = struct.unpack('!BHf', date[:7])
    locatie_raw = date[7:17]
    crc_primit = struct.unpack('!I', date[17:21])[0]
    
    # Extrage locația (elimină padding null)
    locatie = locatie_raw.rstrip(b'\x00').decode('utf-8', errors='replace')
    
    # Verifică CRC
    crc_calculat = calculeaza_crc32(date[:17])
    crc_valid = (crc_primit == crc_calculat)
    
    return {
        'versiune': versiune,
        'sensor_id': sensor_id,
        'temperatura': temperatura,
        'locatie': locatie,
        'crc': crc_primit,
        'crc_valid': crc_valid
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE CRC32
# ═══════════════════════════════════════════════════════════════════════════════

class TestCRC32:
    """Teste pentru calculul CRC32."""
    
    def test_valoare_cunoscuta(self):
        """CRC32 pentru '123456789' trebuie să fie 0xCBF43926."""
        rezultat = calculeaza_crc32(b"123456789")
        assert rezultat == 0xCBF43926, f"Așteptat 0xCBF43926, primit 0x{rezultat:08X}"
    
    def test_date_goale(self):
        """CRC32 pentru date goale trebuie să fie 0."""
        rezultat = calculeaza_crc32(b"")
        assert rezultat == 0, f"Așteptat 0, primit 0x{rezultat:08X}"
    
    def test_determinism(self):
        """Același input produce același CRC."""
        date = b"test data pentru CRC"
        crc1 = calculeaza_crc32(date)
        crc2 = calculeaza_crc32(date)
        assert crc1 == crc2, "CRC nu este determinist"
    
    def test_sensibilitate_la_modificari(self):
        """Modificarea unui bit schimbă CRC-ul."""
        date1 = b"test"
        date2 = b"Test"  # Diferă doar primul caracter
        crc1 = calculeaza_crc32(date1)
        crc2 = calculeaza_crc32(date2)
        assert crc1 != crc2, "CRC identic pentru date diferite"
    
    def test_range_32bit(self):
        """CRC-ul e întotdeauna pe 32 de biți."""
        for i in range(100):
            date = bytes([i] * 100)
            crc = calculeaza_crc32(date)
            assert 0 <= crc <= 0xFFFFFFFF, f"CRC în afara range-ului: 0x{crc:X}"


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE PROTOCOL BINAR
# ═══════════════════════════════════════════════════════════════════════════════

class TestProtocolBinar:
    """Teste pentru protocolul BINAR."""
    
    def test_impachetare_ping(self):
        """Mesajul PING are 14 bytes (antet) + 0 bytes (payload)."""
        mesaj = impacheteaza_binar(TipMesajBinar.PING, b'', 1)
        assert len(mesaj) == 14, f"Lungime greșită: {len(mesaj)}"
    
    def test_magic_corect(self):
        """Primii 2 bytes sunt 'NP'."""
        mesaj = impacheteaza_binar(TipMesajBinar.PING, b'', 1)
        assert mesaj[:2] == b'NP', f"Magic greșit: {mesaj[:2]}"
    
    def test_roundtrip_ping(self):
        """Impachetare → despachetare recuperează datele originale (PING)."""
        mesaj = impacheteaza_binar(TipMesajBinar.PING, b'', 42)
        rezultat = despacheteaza_binar(mesaj)
        
        assert rezultat is not None, "Parsarea a eșuat"
        assert rezultat['tip'] == TipMesajBinar.PING
        assert rezultat['secventa'] == 42
        assert rezultat['payload'] == b''
        assert rezultat['crc_valid'] is True
    
    def test_roundtrip_cu_payload(self):
        """Impachetare → despachetare cu payload."""
        payload_original = b"date de test pentru protocol"
        mesaj = impacheteaza_binar(TipMesajBinar.SET, payload_original, 123)
        rezultat = despacheteaza_binar(mesaj)
        
        assert rezultat is not None
        assert rezultat['tip'] == TipMesajBinar.SET
        assert rezultat['secventa'] == 123
        assert rezultat['payload'] == payload_original
        assert rezultat['crc_valid'] is True
    
    def test_crc_invalid_detectat(self):
        """Modificarea unui byte invalidează CRC-ul."""
        mesaj = bytearray(impacheteaza_binar(TipMesajBinar.PING, b'', 1))
        mesaj[5] ^= 0xFF  # Modifică un byte
        rezultat = despacheteaza_binar(bytes(mesaj))
        
        assert rezultat is not None  # Parsarea încă funcționează
        assert rezultat['crc_valid'] is False  # Dar CRC e invalid
    
    def test_magic_invalid(self):
        """Magic invalid returnează None."""
        mesaj = bytearray(impacheteaza_binar(TipMesajBinar.PING, b'', 1))
        mesaj[0] = ord('X')  # Schimbă magic
        rezultat = despacheteaza_binar(bytes(mesaj))
        
        assert rezultat is None, "Ar fi trebuit să returneze None pentru magic invalid"
    
    def test_date_prea_scurte(self):
        """Date mai scurte de 14 bytes returnează None."""
        rezultat = despacheteaza_binar(b'NP123456789')  # 11 bytes
        assert rezultat is None
    
    def test_network_byte_order(self):
        """Verifică că se folosește network byte order (big-endian)."""
        mesaj = impacheteaza_binar(TipMesajBinar.PING, b'', 0x12345678)
        
        # Secvența e la offset 6-9
        secventa_bytes = mesaj[6:10]
        
        # În big-endian, 0x12345678 e [0x12, 0x34, 0x56, 0x78]
        assert secventa_bytes == b'\x12\x34\x56\x78', \
            f"Ordinea bytes greșită: {secventa_bytes.hex()}"
    
    def test_toate_tipurile(self):
        """Toate tipurile de mesaje funcționează."""
        tipuri = [
            TipMesajBinar.PING,
            TipMesajBinar.PONG,
            TipMesajBinar.SET,
            TipMesajBinar.GET,
            TipMesajBinar.DELETE,
            TipMesajBinar.RESPONSE,
            TipMesajBinar.ERROR
        ]
        
        for tip in tipuri:
            mesaj = impacheteaza_binar(tip, b'test', 1)
            rezultat = despacheteaza_binar(mesaj)
            assert rezultat is not None
            assert rezultat['tip'] == tip
            assert rezultat['crc_valid'] is True


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE PROTOCOL SENZOR
# ═══════════════════════════════════════════════════════════════════════════════

class TestProtocolSenzor:
    """Teste pentru protocolul senzor UDP."""
    
    def test_dimensiune_datagrama(self):
        """Datagrama trebuie să aibă exact 23 bytes."""
        datagrama = impacheteaza_senzor(1, 23.5, "Lab1")
        assert len(datagrama) == 23, f"Lungime greșită: {len(datagrama)}"
    
    def test_roundtrip(self):
        """Impachetare → despachetare recuperează datele."""
        datagrama = impacheteaza_senzor(42, 25.5, "Sala101")
        rezultat = despacheteaza_senzor(datagrama)
        
        assert rezultat is not None
        assert rezultat['sensor_id'] == 42
        assert abs(rezultat['temperatura'] - 25.5) < 0.01  # Float comparison
        assert rezultat['locatie'] == "Sala101"
        assert rezultat['crc_valid'] is True
    
    def test_locatie_padding(self):
        """Locația scurtă e padded cu null bytes."""
        datagrama = impacheteaza_senzor(1, 20.0, "A")
        
        # Locația e la offset 7-16 (10 bytes)
        locatie_raw = datagrama[7:17]
        assert locatie_raw == b'A' + b'\x00' * 9
    
    def test_locatie_truncata(self):
        """Locația prea lungă e truncată la 10 bytes."""
        datagrama = impacheteaza_senzor(1, 20.0, "NumeFoarteLungCareTrebuieTruncat")
        rezultat = despacheteaza_senzor(datagrama)
        
        assert rezultat is not None
        assert len(rezultat['locatie']) <= 10
    
    def test_temperatura_negativa(self):
        """Temperaturile negative funcționează."""
        datagrama = impacheteaza_senzor(1, -15.5, "Frigider")
        rezultat = despacheteaza_senzor(datagrama)
        
        assert rezultat is not None
        assert abs(rezultat['temperatura'] - (-15.5)) < 0.01
    
    def test_crc_invalid_detectat(self):
        """Modificarea datelor invalidează CRC-ul."""
        datagrama = bytearray(impacheteaza_senzor(1, 20.0, "Test"))
        datagrama[5] ^= 0xFF  # Modifică un byte
        rezultat = despacheteaza_senzor(bytes(datagrama))
        
        assert rezultat is not None
        assert rezultat['crc_valid'] is False
    
    def test_range_sensor_id(self):
        """sensor_id funcționează în range 0-65535."""
        for sensor_id in [0, 1, 255, 256, 65535]:
            datagrama = impacheteaza_senzor(sensor_id, 20.0, "Test")
            rezultat = despacheteaza_senzor(datagrama)
            assert rezultat['sensor_id'] == sensor_id


# ═══════════════════════════════════════════════════════════════════════════════
# RULARE TESTE
# ═══════════════════════════════════════════════════════════════════════════════

def run_tests_simple():
    """Rulează testele fără pytest."""
    print("=" * 70)
    print("Teste Unitare Protocol Utils")
    print("=" * 70)
    print()
    
    test_classes = [TestCRC32, TestProtocolBinar, TestProtocolSenzor]
    total = 0
    passed = 0
    failed = 0
    
    for cls in test_classes:
        print(f"\n{cls.__name__}:")
        print("-" * 40)
        
        instance = cls()
        for name in dir(instance):
            if name.startswith('test_'):
                total += 1
                try:
                    getattr(instance, name)()
                    print(f"  ✓ {name}")
                    passed += 1
                except AssertionError as e:
                    print(f"  ✗ {name}: {e}")
                    failed += 1
                except Exception as e:
                    print(f"  ✗ {name}: Excepție - {e}")
                    failed += 1
    
    print()
    print("=" * 70)
    print(f"Rezultat: {passed}/{total} teste trecute")
    if failed > 0:
        print(f"         {failed} teste eșuate")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    if HAS_PYTEST:
        # Rulează cu pytest dacă e disponibil
        sys.exit(pytest.main([__file__, "-v"]))
    else:
        # Rulează simplu fără pytest
        success = run_tests_simple()
        sys.exit(0 if success else 1)
