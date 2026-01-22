#!/usr/bin/env python3
"""
Utilitare pentru Protocoalele de Laborator
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest modul conține funcții utilitare pentru:
- Calculul și verificarea CRC32
- Împachetarea și despachetarea mesajelor BINAR
- Împachetarea și despachetarea datagramelor senzor

Utilizare:
    from src.utils.protocol_utils import (
        calculeaza_crc32,
        impacheteaza_binar,
        despacheteaza_binar,
        TipMesajBinar
    )
"""

import struct
import binascii
from typing import Optional, Dict, Any, Union
from enum import IntEnum
from dataclasses import dataclass


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL_BINAR
# Scop: Definește valorile fixe ale protocolului BINAR
# ═══════════════════════════════════════════════════════════════════════════════

BINAR_MAGIC: bytes = b'NP'
BINAR_VERSIUNE: int = 1
BINAR_DIMENSIUNE_ANTET: int = 14
BINAR_OFFSET_CRC: int = 10
BINAR_MAX_PAYLOAD: int = 65535  # uint16 max
BINAR_MAX_SECVENTA: int = 0xFFFFFFFF  # uint32 max


class TipMesajBinar(IntEnum):
    """Tipurile de mesaje suportate de protocolul BINAR."""
    PING = 0x01
    PONG = 0x02
    SET = 0x03
    GET = 0x04
    DELETE = 0x05
    RESPONSE = 0x06
    ERROR = 0xFF


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL_SENZOR
# Scop: Definește valorile fixe ale protocolului senzor UDP
# ═══════════════════════════════════════════════════════════════════════════════

SENZOR_VERSIUNE: int = 1
SENZOR_DIMENSIUNE: int = 23
SENZOR_LUNGIME_LOCATIE: int = 10
SENZOR_MAX_ID: int = 65535  # uint16 max


# ═══════════════════════════════════════════════════════════════════════════════
# STRUCTURI_DATE
# Scop: Definește tipurile de date pentru rezultatele parsării
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class RezultatBinar:
    """Rezultatul parsării unui mesaj BINAR."""
    versiune: int
    tip: TipMesajBinar
    lungime: int
    secventa: int
    crc: int
    crc_valid: bool
    payload: bytes


@dataclass
class RezultatSenzor:
    """Rezultatul parsării unei datagrame senzor."""
    versiune: int
    sensor_id: int
    temperatura: float
    locatie: str
    crc: int
    crc_valid: bool


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_CRC
# Scop: Calculul și verificarea CRC32
# Transferabil la: Orice protocol care necesită verificare integritate
# ═══════════════════════════════════════════════════════════════════════════════

def calculeaza_crc32(date: bytes) -> int:
    """
    Calculează CRC32 pentru un șir de bytes.
    
    Folosește algoritmul CRC32 standard (ISO 3309, ITU-T V.42).
    Rezultatul e mascat la 32 de biți pentru a asigura valoare pozitivă.
    
    Args:
        date: Datele pentru care se calculează CRC-ul
    
    Returns:
        Valoarea CRC32 ca întreg pozitiv pe 32 de biți (0 - 0xFFFFFFFF)
    
    Raises:
        TypeError: Dacă date nu este de tip bytes
    
    Example:
        >>> calculeaza_crc32(b"123456789")
        0xCBF43926
    """
    if not isinstance(date, (bytes, bytearray)):
        raise TypeError(f"Așteptat bytes, primit {type(date).__name__}")
    
    return binascii.crc32(date) & 0xFFFFFFFF


def verifica_crc32_standard() -> bool:
    """
    Verifică implementarea CRC32 cu valoarea standard de test.
    
    Valoarea CRC32 pentru "123456789" trebuie să fie 0xCBF43926.
    
    Returns:
        True dacă implementarea e corectă, False altfel
    """
    return calculeaza_crc32(b"123456789") == 0xCBF43926


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_PROTOCOL_BINAR
# Scop: Împachetare și despachetare mesaje BINAR
# Transferabil la: Orice protocol cu antet binar de dimensiune fixă
# ═══════════════════════════════════════════════════════════════════════════════

def impacheteaza_binar(
    tip: Union[int, TipMesajBinar],
    payload: bytes,
    secventa: int,
    versiune: int = BINAR_VERSIUNE
) -> bytes:
    """
    Construiește un mesaj BINAR complet.
    
    Creează antetul de 14 octeți, calculează CRC32 și atașează payload-ul.
    
    Structura antetului:
        - Magic "NP": 2 bytes
        - Versiune: 1 byte
        - Tip: 1 byte
        - Lungime payload: 2 bytes (big-endian)
        - Secvență: 4 bytes (big-endian)
        - CRC32: 4 bytes (big-endian)
    
    CRC32 se calculează peste: antet fără CRC (10 bytes) + payload
    
    Args:
        tip: Tipul mesajului (0x01-0xFF sau TipMesajBinar)
        payload: Datele utile ale mesajului
        secventa: Numărul de secvență pentru tracking
        versiune: Versiunea protocolului (implicit 1)
    
    Returns:
        Mesaj complet: antet (14 bytes) + payload
    
    Raises:
        ValueError: Dacă parametrii sunt în afara range-ului valid
        TypeError: Dacă payload nu este bytes
    
    Example:
        >>> msg = impacheteaza_binar(TipMesajBinar.PING, b'', 1)
        >>> len(msg)
        14
    """
    # Validare tip
    tip_val = int(tip)
    if not 0x00 <= tip_val <= 0xFF:
        raise ValueError(f"Tip invalid: {tip_val}. Trebuie să fie 0x00-0xFF.")
    
    # Validare payload
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError(f"Payload: așteptat bytes, primit {type(payload).__name__}")
    
    if len(payload) > BINAR_MAX_PAYLOAD:
        raise ValueError(f"Payload prea mare: {len(payload)}. Max {BINAR_MAX_PAYLOAD} bytes.")
    
    # Validare secvență
    if not 0 <= secventa <= BINAR_MAX_SECVENTA:
        raise ValueError(f"Secvență invalidă: {secventa}. Range: 0 - {BINAR_MAX_SECVENTA}.")
    
    # Validare versiune
    if not 0 <= versiune <= 255:
        raise ValueError(f"Versiune invalidă: {versiune}. Range: 0-255.")
    
    lungime = len(payload)
    
    # Antet parțial (fără CRC) - 10 bytes
    antet_partial = struct.pack('!2sBBHI',
        BINAR_MAGIC,
        versiune,
        tip_val,
        lungime,
        secventa
    )
    
    # Calculează CRC peste antet_partial + payload
    crc = calculeaza_crc32(antet_partial + payload)
    
    # Mesaj complet cu CRC
    mesaj = struct.pack('!2sBBHII',
        BINAR_MAGIC,
        versiune,
        tip_val,
        lungime,
        secventa,
        crc
    ) + payload
    
    return mesaj


def despacheteaza_binar(date: bytes) -> Optional[RezultatBinar]:
    """
    Parsează un mesaj BINAR și verifică CRC-ul.
    
    Args:
        date: Buffer-ul de date primit (minim 14 bytes)
    
    Returns:
        RezultatBinar cu câmpurile parsate sau None dacă datele sunt invalide
    
    Example:
        >>> msg = impacheteaza_binar(TipMesajBinar.PING, b'', 1)
        >>> rezultat = despacheteaza_binar(msg)
        >>> rezultat.crc_valid
        True
    """
    # Verifică lungimea minimă
    if len(date) < BINAR_DIMENSIUNE_ANTET:
        return None
    
    # Despachetează antetul
    try:
        magic, versiune, tip, lungime, secventa, crc_primit = struct.unpack(
            '!2sBBHII', date[:BINAR_DIMENSIUNE_ANTET]
        )
    except struct.error:
        return None
    
    # Verifică magic
    if magic != BINAR_MAGIC:
        return None
    
    # Extrage payload
    payload = date[BINAR_DIMENSIUNE_ANTET:BINAR_DIMENSIUNE_ANTET + lungime]
    
    # Verifică CRC
    antet_fara_crc = date[:BINAR_OFFSET_CRC]
    crc_calculat = calculeaza_crc32(antet_fara_crc + payload)
    crc_valid = (crc_primit == crc_calculat)
    
    # Convertește tip la enum dacă e posibil
    try:
        tip_enum = TipMesajBinar(tip)
    except ValueError:
        tip_enum = TipMesajBinar.ERROR  # Tip necunoscut
    
    return RezultatBinar(
        versiune=versiune,
        tip=tip_enum,
        lungime=lungime,
        secventa=secventa,
        crc=crc_primit,
        crc_valid=crc_valid,
        payload=payload
    )


def despacheteaza_binar_dict(date: bytes) -> Optional[Dict[str, Any]]:
    """
    Parsează un mesaj BINAR și returnează un dicționar.
    
    Versiune alternativă care returnează dict în loc de dataclass.
    
    Args:
        date: Buffer-ul de date primit
    
    Returns:
        Dicționar cu câmpurile sau None dacă invalid
    """
    rezultat = despacheteaza_binar(date)
    if rezultat is None:
        return None
    
    return {
        'versiune': rezultat.versiune,
        'tip': rezultat.tip,
        'lungime': rezultat.lungime,
        'secventa': rezultat.secventa,
        'crc': rezultat.crc,
        'crc_valid': rezultat.crc_valid,
        'payload': rezultat.payload
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_PROTOCOL_SENZOR
# Scop: Împachetare și despachetare datagrame senzor UDP
# Transferabil la: Orice protocol IoT cu mesaje de dimensiune fixă
# ═══════════════════════════════════════════════════════════════════════════════

def impacheteaza_senzor(
    sensor_id: int,
    temperatura: float,
    locatie: str,
    versiune: int = SENZOR_VERSIUNE
) -> bytes:
    """
    Construiește o datagramă de senzor (23 bytes).
    
    Structura:
        - Versiune: 1 byte
        - ID Senzor: 2 bytes (big-endian)
        - Temperatură: 4 bytes (float, big-endian)
        - Locație: 10 bytes (ASCII, padding cu null)
        - CRC32: 4 bytes (big-endian)
        - Rezervat: 2 bytes (null)
    
    Args:
        sensor_id: ID-ul senzorului (0-65535)
        temperatura: Valoarea temperaturii
        locatie: Locația senzorului (max 10 caractere)
        versiune: Versiunea protocolului (implicit 1)
    
    Returns:
        Datagramă de exact 23 bytes
    
    Raises:
        ValueError: Dacă parametrii sunt invalizi
    """
    # Validare sensor_id
    if not 0 <= sensor_id <= SENZOR_MAX_ID:
        raise ValueError(f"sensor_id invalid: {sensor_id}. Range: 0-{SENZOR_MAX_ID}.")
    
    # Validare versiune
    if not 0 <= versiune <= 255:
        raise ValueError(f"versiune invalidă: {versiune}. Range: 0-255.")
    
    # Pregătește locația (10 bytes, padding cu null)
    loc_bytes = locatie.encode('utf-8')[:SENZOR_LUNGIME_LOCATIE]
    loc_padded = loc_bytes + b'\x00' * (SENZOR_LUNGIME_LOCATIE - len(loc_bytes))
    
    # Partea fără CRC (17 bytes)
    parte_fara_crc = struct.pack('!BHf',
        versiune,
        sensor_id,
        temperatura
    ) + loc_padded
    
    # Calculează CRC
    crc = calculeaza_crc32(parte_fara_crc)
    
    # Datagrama completă (23 bytes)
    datagrama = parte_fara_crc + struct.pack('!I', crc) + b'\x00\x00'
    
    assert len(datagrama) == SENZOR_DIMENSIUNE, \
        f"Lungime greșită: {len(datagrama)} != {SENZOR_DIMENSIUNE}"
    
    return datagrama


def despacheteaza_senzor(date: bytes) -> Optional[RezultatSenzor]:
    """
    Parsează o datagramă de senzor și verifică CRC-ul.
    
    Args:
        date: Datagrama brută (exact 23 bytes)
    
    Returns:
        RezultatSenzor cu câmpurile parsate sau None dacă invalid
    """
    # Verifică lungimea exactă
    if len(date) != SENZOR_DIMENSIUNE:
        return None
    
    # Despachetează câmpurile
    try:
        versiune, sensor_id, temperatura = struct.unpack('!BHf', date[:7])
    except struct.error:
        return None
    
    # Extrage locația (elimină padding null)
    locatie_raw = date[7:17]
    locatie = locatie_raw.rstrip(b'\x00').decode('utf-8', errors='replace')
    
    # Extrage CRC
    crc_primit = struct.unpack('!I', date[17:21])[0]
    
    # Verifică CRC (peste primii 17 bytes)
    crc_calculat = calculeaza_crc32(date[:17])
    crc_valid = (crc_primit == crc_calculat)
    
    return RezultatSenzor(
        versiune=versiune,
        sensor_id=sensor_id,
        temperatura=temperatura,
        locatie=locatie,
        crc=crc_primit,
        crc_valid=crc_valid
    )


def despacheteaza_senzor_dict(date: bytes) -> Optional[Dict[str, Any]]:
    """
    Parsează o datagramă de senzor și returnează un dicționar.
    
    Args:
        date: Datagrama brută
    
    Returns:
        Dicționar cu câmpurile sau None dacă invalid
    """
    rezultat = despacheteaza_senzor(date)
    if rezultat is None:
        return None
    
    return {
        'versiune': rezultat.versiune,
        'sensor_id': rezultat.sensor_id,
        'temperatura': rezultat.temperatura,
        'locatie': rezultat.locatie,
        'crc': rezultat.crc,
        'crc_valid': rezultat.crc_valid
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_TEXT_PROTOCOL
# Scop: Formatare și parsare mesaje protocol TEXT
# ═══════════════════════════════════════════════════════════════════════════════

def formateaza_text(comanda: str) -> str:
    """
    Formatează o comandă pentru protocolul TEXT.
    
    Args:
        comanda: Comanda de formatat (ex: "PING", "SET cheie valoare")
    
    Returns:
        Mesajul formatat cu prefix de lungime
    
    Example:
        >>> formateaza_text("PING")
        '4 PING'
    """
    return f"{len(comanda)} {comanda}"


def parseaza_text(raspuns: str) -> tuple[Optional[int], Optional[str]]:
    """
    Parsează un răspuns de la protocolul TEXT.
    
    Args:
        raspuns: Răspunsul brut (format: "<lungime> <continut>")
    
    Returns:
        Tuple (lungime, continut) sau (None, None) dacă invalid
    """
    parts = raspuns.strip().split(' ', 1)
    if len(parts) < 2:
        return (None, None)
    
    try:
        lungime = int(parts[0])
        continut = parts[1]
        return (lungime, continut)
    except ValueError:
        return (None, None)


# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Test protocol_utils.py")
    print("=" * 50)
    
    # Test CRC32
    print("\n1. Test CRC32...")
    if verifica_crc32_standard():
        print("   ✓ CRC32 corect")
    else:
        print("   ✗ CRC32 INCORECT!")
    
    # Test BINAR
    print("\n2. Test protocol BINAR...")
    msg = impacheteaza_binar(TipMesajBinar.PING, b'', 1)
    rezultat = despacheteaza_binar(msg)
    if rezultat and rezultat.crc_valid:
        print(f"   ✓ PING: {len(msg)} bytes, CRC valid")
    else:
        print("   ✗ EROARE BINAR!")
    
    # Test SENZOR
    print("\n3. Test protocol SENZOR...")
    dg = impacheteaza_senzor(42, 23.5, "Lab1")
    rez = despacheteaza_senzor(dg)
    if rez and rez.crc_valid:
        print(f"   ✓ Senzor: {len(dg)} bytes, temp={rez.temperatura}°C, CRC valid")
    else:
        print("   ✗ EROARE SENZOR!")
    
    # Test TEXT
    print("\n4. Test protocol TEXT...")
    msg_text = formateaza_text("PING")
    if msg_text == "4 PING":
        print(f"   ✓ TEXT: '{msg_text}'")
    else:
        print(f"   ✗ TEXT INCORECT: '{msg_text}'")
    
    print("\n" + "=" * 50)
    print("Teste complete!")
