#!/usr/bin/env python3
"""
Server Protocol BINAR
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Server pentru protocolul BINAR cu antet fix de 14 octeți și verificare CRC32.
Port implicit: 5401

Structura antetului:
- Magic: 2 octeți ('NP')
- Versiune: 1 octet
- Tip: 1 octet
- Lungime: 2 octeți (big-endian)
- Secvență: 4 octeți (big-endian)
- CRC32: 4 octeți (big-endian)
"""

import socket
import struct
import threading
import binascii
import logging
from typing import Dict, Optional, Tuple

# Configurare logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurație server
HOST = '0.0.0.0'
PORT = 5401
DIMENSIUNE_ANTET = 14
MAGIC = b'NP'
VERSIUNE = 1

# Tipuri de mesaje
class TipMesaj:
    PING = 0x01
    PONG = 0x02
    SET = 0x03
    GET = 0x04
    DELETE = 0x05
    RESPONSE = 0x06
    ERROR = 0xFF


class MagazinCheieValoare:
    """Magazin thread-safe pentru perechi cheie-valoare."""
    
    def __init__(self):
        self._date: Dict[bytes, bytes] = {}
        self._lock = threading.Lock()
    
    def seteaza(self, cheie: bytes, valoare: bytes) -> bool:
        with self._lock:
            self._date[cheie] = valoare
            return True
    
    def obtine(self, cheie: bytes) -> Optional[bytes]:
        with self._lock:
            return self._date.get(cheie)
    
    def sterge(self, cheie: bytes) -> bool:
        with self._lock:
            if cheie in self._date:
                del self._date[cheie]
                return True
            return False


# Instanță globală
magazin = MagazinCheieValoare()


def calculeaza_crc(date: bytes) -> int:
    """Calculează CRC32 pentru date."""
    return binascii.crc32(date) & 0xFFFFFFFF


def construieste_mesaj(tip: int, payload: bytes, secventa: int) -> bytes:
    """Construiește un mesaj binar complet."""
    lungime = len(payload)
    
    # Antet fără CRC
    antet_partial = struct.pack('!2sBBHI',
        MAGIC, VERSIUNE, tip, lungime, secventa
    )
    
    # Calculează CRC
    crc = calculeaza_crc(antet_partial + payload)
    
    # Mesaj complet
    mesaj = struct.pack('!2sBBHII',
        MAGIC, VERSIUNE, tip, lungime, secventa, crc
    ) + payload
    
    return mesaj


def parseaza_antet(date: bytes) -> Tuple[int, int, int, int, int]:
    """
    Parsează antetul unui mesaj.
    
    Returns:
        (versiune, tip, lungime, secventa, crc)
    
    Raises:
        ValueError: Dacă antetul este invalid
    """
    if len(date) < DIMENSIUNE_ANTET:
        raise ValueError(f"Antet prea scurt: {len(date)} < {DIMENSIUNE_ANTET}")
    
    magic, versiune, tip, lungime, secventa, crc = struct.unpack(
        '!2sBBHII', date[:DIMENSIUNE_ANTET]
    )
    
    if magic != MAGIC:
        raise ValueError(f"Magic invalid: {magic}")
    
    return versiune, tip, lungime, secventa, crc


def verifica_crc(antet: bytes, payload: bytes, crc_primit: int) -> bool:
    """Verifică CRC-ul mesajului."""
    antet_fara_crc = antet[:10]  # Fără ultimii 4 octeți (CRC)
    crc_calculat = calculeaza_crc(antet_fara_crc + payload)
    return crc_calculat == crc_primit


def proceseaza_mesaj(tip: int, payload: bytes, secventa: int) -> bytes:
    """Procesează un mesaj și returnează răspunsul."""
    
    if tip == TipMesaj.PING:
        return construieste_mesaj(TipMesaj.PONG, b'', secventa)
    
    elif tip == TipMesaj.SET:
        # Payload: lungime_cheie (2) + cheie + valoare
        if len(payload) < 2:
            return construieste_mesaj(TipMesaj.ERROR, b'payload invalid', secventa)
        
        lung_cheie = struct.unpack('!H', payload[:2])[0]
        if len(payload) < 2 + lung_cheie:
            return construieste_mesaj(TipMesaj.ERROR, b'cheie incompleta', secventa)
        
        cheie = payload[2:2 + lung_cheie]
        valoare = payload[2 + lung_cheie:]
        
        magazin.seteaza(cheie, valoare)
        return construieste_mesaj(TipMesaj.RESPONSE, b'OK', secventa)
    
    elif tip == TipMesaj.GET:
        cheie = payload
        valoare = magazin.obtine(cheie)
        
        if valoare is None:
            return construieste_mesaj(TipMesaj.ERROR, b'cheie inexistenta', secventa)
        
        return construieste_mesaj(TipMesaj.RESPONSE, valoare, secventa)
    
    elif tip == TipMesaj.DELETE:
        cheie = payload
        
        if magazin.sterge(cheie):
            return construieste_mesaj(TipMesaj.RESPONSE, b'OK', secventa)
        else:
            return construieste_mesaj(TipMesaj.ERROR, b'cheie inexistenta', secventa)
    
    else:
        return construieste_mesaj(TipMesaj.ERROR, b'tip necunoscut', secventa)


def gestioneaza_client(socket_client: socket.socket, adresa: tuple):
    """Gestionează o conexiune client."""
    logger.info(f"Conexiune nouă de la {adresa}")
    buffer = b''
    
    try:
        while True:
            date = socket_client.recv(4096)
            if not date:
                logger.info(f"Client deconectat: {adresa}")
                break
            
            buffer += date
            
            # Procesare mesaje complete
            while len(buffer) >= DIMENSIUNE_ANTET:
                try:
                    versiune, tip, lungime, secventa, crc = parseaza_antet(buffer)
                except ValueError as e:
                    logger.warning(f"Antet invalid de la {adresa}: {e}")
                    buffer = buffer[1:]  # Încearcă să resincronizeze
                    continue
                
                # Verifică dacă avem tot mesajul
                dim_totala = DIMENSIUNE_ANTET + lungime
                if len(buffer) < dim_totala:
                    break  # Așteaptă mai multe date
                
                # Extrage mesajul complet
                antet = buffer[:DIMENSIUNE_ANTET]
                payload = buffer[DIMENSIUNE_ANTET:dim_totala]
                buffer = buffer[dim_totala:]
                
                # Verifică CRC
                if not verifica_crc(antet, payload, crc):
                    logger.warning(f"CRC invalid de la {adresa}")
                    raspuns = construieste_mesaj(TipMesaj.ERROR, b'CRC invalid', secventa)
                    socket_client.sendall(raspuns)
                    continue
                
                logger.debug(f"Mesaj de la {adresa}: tip={tip:02X}, seq={secventa}")
                
                # Procesează și răspunde
                raspuns = proceseaza_mesaj(tip, payload, secventa)
                socket_client.sendall(raspuns)
                
    except ConnectionResetError:
        logger.warning(f"Conexiune resetată: {adresa}")
    except Exception as e:
        logger.error(f"Eroare cu clientul {adresa}: {e}")
    finally:
        socket_client.close()


def porneste_server():
    """Pornește serverul BINAR."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        logger.info(f"Server BINAR pornit pe {HOST}:{PORT}")
        logger.info("Aștept conexiuni... (Ctrl+C pentru oprire)")
        
        while True:
            socket_client, adresa = server.accept()
            thread = threading.Thread(
                target=gestioneaza_client,
                args=(socket_client, adresa)
            )
            thread.daemon = True
            thread.start()
            
    except KeyboardInterrupt:
        logger.info("\nOprire server...")
    finally:
        server.close()


if __name__ == "__main__":
    porneste_server()
