#!/usr/bin/env python3
"""
Utilitare Protocol
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Funcții utilitare pentru lucrul cu protocoalele de laborator.
"""

import struct
import binascii
from typing import Tuple, Optional


def calculeaza_crc32(date: bytes) -> int:
    """
    Calculează CRC32 pentru un bloc de date.
    
    Args:
        date: Datele pentru care se calculează CRC
    
    Returns:
        Valoarea CRC32 ca întreg pozitiv pe 32 de biți
    """
    return binascii.crc32(date) & 0xFFFFFFFF


def verifica_crc32(date: bytes, crc_asteptat: int) -> bool:
    """
    Verifică dacă CRC32 se potrivește.
    
    Args:
        date: Datele de verificat
        crc_asteptat: Valoarea CRC32 așteptată
    
    Returns:
        True dacă CRC se potrivește
    """
    return calculeaza_crc32(date) == crc_asteptat


def formateaza_hex(date: bytes, separator: str = ' ') -> str:
    """
    Formatează date binare ca string hexazecimal.
    
    Args:
        date: Datele de formatat
        separator: Separator între octeți
    
    Returns:
        String formatat
    """
    return separator.join(f'{b:02X}' for b in date)


def parseaza_hex(text: str) -> bytes:
    """
    Parsează un string hexazecimal în bytes.
    
    Args:
        text: String hexazecimal (cu sau fără separatori)
    
    Returns:
        Bytes
    """
    # Elimină spații și caractere comune
    text = text.replace(' ', '').replace(':', '').replace('-', '')
    return bytes.fromhex(text)


# ============================================================
# Utilitare Protocol TEXT
# ============================================================

def impacheteaza_text(continut: str) -> bytes:
    """
    Împachetează conținut în format protocol TEXT.
    
    Format: <LUNGIME> <CONȚINUT>
    
    Args:
        continut: Conținutul mesajului
    
    Returns:
        Mesaj formatat ca bytes
    """
    continut_bytes = continut.encode('utf-8')
    lungime = len(continut_bytes)
    return f"{lungime} ".encode('utf-8') + continut_bytes


def despacheteaza_text(date: bytes) -> Tuple[Optional[int], Optional[str], bytes]:
    """
    Despacheteează un mesaj din format protocol TEXT.
    
    Args:
        date: Datele primite
    
    Returns:
        Tuple (lungime, continut, rest) sau (None, None, date) dacă incomplet
    """
    try:
        text = date.decode('utf-8')
        spatiu_idx = text.find(' ')
        
        if spatiu_idx == -1:
            return None, None, date
        
        lungime = int(text[:spatiu_idx])
        start = spatiu_idx + 1
        
        if len(text) < start + lungime:
            return None, None, date
        
        continut = text[start:start + lungime]
        rest = text[start + lungime:].encode('utf-8')
        
        return lungime, continut, rest
        
    except (ValueError, UnicodeDecodeError):
        return None, None, date


# ============================================================
# Utilitare Protocol BINAR
# ============================================================

BINAR_MAGIC = b'NP'
BINAR_VERSIUNE = 1
BINAR_DIMENSIUNE_ANTET = 14


class TipMesajBinar:
    """Constante pentru tipurile de mesaje din protocolul BINAR."""
    PING = 0x01
    PONG = 0x02
    SET = 0x03
    GET = 0x04
    DELETE = 0x05
    RESPONSE = 0x06
    ERROR = 0xFF
    
    _nume = {
        0x01: "PING",
        0x02: "PONG",
        0x03: "SET",
        0x04: "GET",
        0x05: "DELETE",
        0x06: "RESPONSE",
        0xFF: "ERROR"
    }
    
    @classmethod
    def nume(cls, tip: int) -> str:
        """Returnează numele tipului de mesaj."""
        return cls._nume.get(tip, f"NECUNOSCUT(0x{tip:02X})")


def impacheteaza_binar(tip: int, payload: bytes, secventa: int, 
                       versiune: int = BINAR_VERSIUNE) -> bytes:
    """
    Împachetează un mesaj în format protocol BINAR.
    
    Args:
        tip: Tipul mesajului
        payload: Conținutul mesajului
        secventa: Numărul de secvență
        versiune: Versiunea protocolului
    
    Returns:
        Mesaj binar complet
    """
    lungime = len(payload)
    
    # Antet fără CRC
    antet_partial = struct.pack('!2sBBHI',
        BINAR_MAGIC, versiune, tip, lungime, secventa
    )
    
    # Calculează CRC
    crc = calculeaza_crc32(antet_partial + payload)
    
    # Mesaj complet
    return struct.pack('!2sBBHII',
        BINAR_MAGIC, versiune, tip, lungime, secventa, crc
    ) + payload


def despacheteaza_binar(date: bytes) -> Optional[dict]:
    """
    Despacheteează un mesaj din format protocol BINAR.
    
    Args:
        date: Datele primite (minim 14 octeți)
    
    Returns:
        Dicționar cu câmpurile sau None dacă invalid
    """
    if len(date) < BINAR_DIMENSIUNE_ANTET:
        return None
    
    magic, versiune, tip, lungime, secventa, crc = struct.unpack(
        '!2sBBHII', date[:BINAR_DIMENSIUNE_ANTET]
    )
    
    if magic != BINAR_MAGIC:
        return None
    
    if len(date) < BINAR_DIMENSIUNE_ANTET + lungime:
        return None
    
    payload = date[BINAR_DIMENSIUNE_ANTET:BINAR_DIMENSIUNE_ANTET + lungime]
    
    # Verifică CRC
    antet_fara_crc = date[:10]
    crc_calculat = calculeaza_crc32(antet_fara_crc + payload)
    
    return {
        'magic': magic,
        'versiune': versiune,
        'tip': tip,
        'lungime': lungime,
        'secventa': secventa,
        'crc': crc,
        'crc_valid': crc == crc_calculat,
        'payload': payload
    }


# ============================================================
# Utilitare Protocol Senzor UDP
# ============================================================

UDP_DIMENSIUNE_DATAGRAMA = 23


def impacheteaza_senzor(sensor_id: int, temperatura: float, locatie: str,
                        versiune: int = 1) -> bytes:
    """
    Împachetează date de senzor în datagramă UDP.
    
    Args:
        sensor_id: ID-ul senzorului
        temperatura: Valoarea temperaturii
        locatie: Locația senzorului (max 10 caractere)
        versiune: Versiunea protocolului
    
    Returns:
        Datagramă de 23 de octeți
    """
    locatie_bytes = locatie.encode('utf-8')[:10].ljust(10, b'\x00')
    date_fara_crc = struct.pack('!BHf', versiune, sensor_id, temperatura) + locatie_bytes
    crc = calculeaza_crc32(date_fara_crc)
    rezervat = b'\x00\x00'
    
    return date_fara_crc + struct.pack('!I', crc) + rezervat


def despacheteaza_senzor(date: bytes) -> Optional[dict]:
    """
    Despacheteează o datagramă de senzor UDP.
    
    Args:
        date: Datagrama de 23 de octeți
    
    Returns:
        Dicționar cu datele sau None dacă invalid
    """
    if len(date) != UDP_DIMENSIUNE_DATAGRAMA:
        return None
    
    versiune = date[0]
    sensor_id = struct.unpack('!H', date[1:3])[0]
    temperatura = struct.unpack('!f', date[3:7])[0]
    locatie = date[7:17].rstrip(b'\x00').decode('utf-8', errors='replace')
    crc = struct.unpack('!I', date[17:21])[0]
    
    crc_calculat = calculeaza_crc32(date[:17])
    
    return {
        'versiune': versiune,
        'sensor_id': sensor_id,
        'temperatura': temperatura,
        'locatie': locatie,
        'crc': crc,
        'crc_valid': crc == crc_calculat
    }
