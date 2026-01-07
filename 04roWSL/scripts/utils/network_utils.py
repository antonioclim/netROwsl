#!/usr/bin/env python3
"""
Utilitare Rețea
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Oferă funcționalități pentru operațiuni de rețea.
"""

import socket
import struct
import binascii
from typing import Optional, Tuple

from .logger import configureaza_logger

logger = configureaza_logger("network_utils")


class UtilitareRetea:
    """Clasă cu utilitare pentru operațiuni de rețea."""
    
    @staticmethod
    def verifica_port_activ(port: int, host: str = "localhost", 
                           protocol: str = "tcp", timeout: float = 2.0) -> bool:
        """
        Verifică dacă un serviciu răspunde pe un port.
        
        Args:
            port: Portul de verificat
            host: Adresa gazdei
            protocol: "tcp" sau "udp"
            timeout: Timeout în secunde
        
        Returns:
            True dacă serviciul răspunde
        """
        try:
            if protocol == "tcp":
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(timeout)
                    rezultat = s.connect_ex((host, port))
                    return rezultat == 0
            else:  # UDP
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.settimeout(timeout)
                    s.sendto(b"test", (host, port))
                    return True
        except Exception:
            return False
    
    @staticmethod
    def gaseste_port_liber(port_start: int = 5000, port_sfarsit: int = 6000) -> Optional[int]:
        """
        Găsește un port TCP liber în intervalul specificat.
        
        Args:
            port_start: Începutul intervalului
            port_sfarsit: Sfârșitul intervalului
        
        Returns:
            Numărul portului liber sau None
        """
        for port in range(port_start, port_sfarsit):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    return port
            except OSError:
                continue
        return None
    
    @staticmethod
    def calculeaza_crc32(date: bytes) -> int:
        """
        Calculează CRC32 pentru un bloc de date.
        
        Args:
            date: Datele pentru care se calculează CRC
        
        Returns:
            Valoarea CRC32 ca întreg pozitiv pe 32 de biți
        """
        return binascii.crc32(date) & 0xFFFFFFFF
    
    @staticmethod
    def verifica_crc32(date: bytes, crc_asteptat: int) -> bool:
        """
        Verifică dacă CRC32 se potrivește.
        
        Args:
            date: Datele de verificat
            crc_asteptat: Valoarea CRC32 așteptată
        
        Returns:
            True dacă CRC se potrivește
        """
        crc_calculat = binascii.crc32(date) & 0xFFFFFFFF
        return crc_calculat == crc_asteptat
    
    @staticmethod
    def impacheteaza_mesaj_text(continut: str) -> bytes:
        """
        Împachetează un mesaj în formatul protocolului TEXT.
        
        Format: <LUNGIME> <CONȚINUT>
        
        Args:
            continut: Conținutul mesajului
        
        Returns:
            Mesajul împachetat ca bytes
        """
        continut_bytes = continut.encode('utf-8')
        lungime = len(continut_bytes)
        return f"{lungime} ".encode() + continut_bytes
    
    @staticmethod
    def despacheteaza_mesaj_text(date: bytes) -> Tuple[int, str]:
        """
        Despacheteează un mesaj din formatul protocolului TEXT.
        
        Args:
            date: Datele primite
        
        Returns:
            Tuple (lungime, conținut)
        """
        date_str = date.decode('utf-8')
        spatiu_idx = date_str.index(' ')
        lungime = int(date_str[:spatiu_idx])
        continut = date_str[spatiu_idx + 1:spatiu_idx + 1 + lungime]
        return lungime, continut
    
    @staticmethod
    def construieste_datagrama_senzor(
        sensor_id: int,
        temperatura: float,
        locatie: str,
        versiune: int = 1
    ) -> bytes:
        """
        Construiește o datagramă pentru protocolul Senzor UDP.
        
        Args:
            sensor_id: ID-ul senzorului (2 octeți)
            temperatura: Temperatura ca float
            locatie: Locația (max 10 caractere)
            versiune: Versiunea protocolului
        
        Returns:
            Datagrama de 23 de octeți
        """
        locatie_bytes = locatie.encode('utf-8')[:10].ljust(10, b'\x00')
        date_fara_crc = struct.pack('!BHf', versiune, sensor_id, temperatura) + locatie_bytes
        crc = binascii.crc32(date_fara_crc) & 0xFFFFFFFF
        rezervat = b'\x00\x00'
        datagrama = date_fara_crc + struct.pack('!I', crc) + rezervat
        return datagrama
    
    @staticmethod
    def obtine_ip_local() -> str:
        """
        Obține adresa IP locală a mașinii.
        
        Returns:
            Adresa IP ca string
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(('8.8.8.8', 80))
                return s.getsockname()[0]
        except Exception:
            return '127.0.0.1'


class TipuriMesajBinar:
    """Constante pentru tipurile de mesaje din protocolul BINAR."""
    PING = 0x01
    PONG = 0x02
    SET = 0x03
    GET = 0x04
    DELETE = 0x05
    RESPONSE = 0x06
    ERROR = 0xFF
    
    @classmethod
    def nume(cls, tip: int) -> str:
        """Returnează numele unui tip de mesaj."""
        nume_dict = {
            cls.PING: "PING",
            cls.PONG: "PONG",
            cls.SET: "SET",
            cls.GET: "GET",
            cls.DELETE: "DELETE",
            cls.RESPONSE: "RESPONSE",
            cls.ERROR: "ERROR"
        }
        return nume_dict.get(tip, f"NECUNOSCUT(0x{tip:02X})")
