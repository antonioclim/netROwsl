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

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# Scop: Importă modulele necesare pentru networking și procesare binară
# Transferabil la: Orice server TCP cu protocol binar
# ═══════════════════════════════════════════════════════════════════════════════

import socket
import struct
import threading
import binascii
import logging
from typing import Dict, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURARE_LOGGING
# Scop: Setează formatarea și nivelul de logging
# Transferabil la: Orice aplicație Python cu necesități de logging
# ═══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL
# Scop: Definește valorile fixe ale protocolului
# Transferabil la: Orice implementare de protocol cu antet fix
# ═══════════════════════════════════════════════════════════════════════════════

HOST: str = '0.0.0.0'
PORT: int = 5401
DIMENSIUNE_ANTET: int = 14
MAGIC: bytes = b'NP'
VERSIUNE: int = 1


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINIRE_TIPURI_MESAJE
# Scop: Enumerează tipurile de mesaje suportate
# Transferabil la: Orice protocol cu mai multe tipuri de mesaje
# ═══════════════════════════════════════════════════════════════════════════════

class TipMesaj:
    """Tipurile de mesaje suportate de protocolul BINAR."""
    PING: int = 0x01
    PONG: int = 0x02
    SET: int = 0x03
    GET: int = 0x04
    DELETE: int = 0x05
    RESPONSE: int = 0x06
    ERROR: int = 0xFF


# ═══════════════════════════════════════════════════════════════════════════════
# STOCARE_DATE
# Scop: Implementează un magazin thread-safe pentru perechi cheie-valoare
# Transferabil la: Orice sistem care necesită stocare partajată între threads
# ═══════════════════════════════════════════════════════════════════════════════

class MagazinCheieValoare:
    """Magazin thread-safe pentru perechi cheie-valoare."""
    
    def __init__(self) -> None:
        self._date: Dict[bytes, bytes] = {}
        self._lock = threading.Lock()
    
    def seteaza(self, cheie: bytes, valoare: bytes) -> bool:
        """Setează o valoare pentru o cheie."""
        with self._lock:
            self._date[cheie] = valoare
            return True
    
    def obtine(self, cheie: bytes) -> Optional[bytes]:
        """Obține valoarea pentru o cheie."""
        with self._lock:
            return self._date.get(cheie)
    
    def sterge(self, cheie: bytes) -> bool:
        """Șterge o cheie și returnează True dacă exista."""
        with self._lock:
            if cheie in self._date:
                del self._date[cheie]
                return True
            return False


# Instanță globală
magazin = MagazinCheieValoare()


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_CRC
# Scop: Calculul și verificarea CRC32
# Transferabil la: Orice protocol care necesită verificare integritate
# ═══════════════════════════════════════════════════════════════════════════════

def calculeaza_crc(date: bytes) -> int:
    """
    Calculează CRC32 pentru date.
    
    Args:
        date: Bytes pentru care se calculează CRC
        
    Returns:
        Valoarea CRC32 ca întreg pozitiv pe 32 biți
    """
    return binascii.crc32(date) & 0xFFFFFFFF


def verifica_crc(antet: bytes, payload: bytes, crc_primit: int) -> bool:
    """
    Verifică CRC-ul mesajului.
    
    Args:
        antet: Antetul complet (14 bytes)
        payload: Payload-ul mesajului
        crc_primit: CRC-ul primit în mesaj
        
    Returns:
        True dacă CRC-ul este valid
    """
    antet_fara_crc = antet[:10]  # Fără ultimii 4 octeți (CRC)
    crc_calculat = calculeaza_crc(antet_fara_crc + payload)
    return crc_calculat == crc_primit


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTRUIRE_MESAJE
# Scop: Împachetarea mesajelor în format binar
# Transferabil la: Orice protocol cu structură de antet fixă
# ═══════════════════════════════════════════════════════════════════════════════

def construieste_mesaj(tip: int, payload: bytes, secventa: int) -> bytes:
    """
    Construiește un mesaj binar complet.
    
    Args:
        tip: Tipul mesajului (TipMesaj.*)
        payload: Datele utile ale mesajului
        secventa: Numărul de secvență
        
    Returns:
        Mesaj complet: antet (14 bytes) + payload
    """
    lungime = len(payload)
    
    # Antet fără CRC (10 bytes)
    antet_partial = struct.pack('!2sBBHI',
        MAGIC, VERSIUNE, tip, lungime, secventa
    )
    
    # Calculează CRC peste antet_partial + payload
    crc = calculeaza_crc(antet_partial + payload)
    
    # Mesaj complet cu CRC
    mesaj = struct.pack('!2sBBHII',
        MAGIC, VERSIUNE, tip, lungime, secventa, crc
    ) + payload
    
    return mesaj


# ═══════════════════════════════════════════════════════════════════════════════
# PARSARE_PROTOCOL
# Scop: Extragerea și validarea câmpurilor din mesaje primite
# Transferabil la: Orice parser de protocol binar
# ═══════════════════════════════════════════════════════════════════════════════

def parseaza_antet(date: bytes) -> Tuple[int, int, int, int, int]:
    """
    Parsează antetul unui mesaj.
    
    Args:
        date: Buffer-ul de date (minim 14 bytes)
    
    Returns:
        Tuple (versiune, tip, lungime, secventa, crc)
    
    Raises:
        ValueError: Dacă antetul este invalid (prea scurt sau magic greșit)
    """
    if len(date) < DIMENSIUNE_ANTET:
        raise ValueError(f"Antet prea scurt: {len(date)} < {DIMENSIUNE_ANTET}")
    
    magic, versiune, tip, lungime, secventa, crc = struct.unpack(
        '!2sBBHII', date[:DIMENSIUNE_ANTET]
    )
    
    if magic != MAGIC:
        raise ValueError(f"Magic invalid: {magic}")
    
    return versiune, tip, lungime, secventa, crc


# ═══════════════════════════════════════════════════════════════════════════════
# PROCESARE_COMENZI
# Scop: Implementează logica de business pentru fiecare tip de comandă
# Transferabil la: Orice server cu comenzi multiple
# ═══════════════════════════════════════════════════════════════════════════════

def proceseaza_mesaj(tip: int, payload: bytes, secventa: int) -> bytes:
    """
    Procesează un mesaj și returnează răspunsul.
    
    Args:
        tip: Tipul mesajului primit
        payload: Payload-ul mesajului
        secventa: Numărul de secvență (se păstrează în răspuns)
        
    Returns:
        Răspunsul serializat ca bytes
    """
    if tip == TipMesaj.PING:
        return construieste_mesaj(TipMesaj.PONG, b'', secventa)
    
    elif tip == TipMesaj.SET:
        # Payload: lungime_cheie (2 bytes) + cheie + valoare
        if len(payload) < 2:
            return construieste_mesaj(TipMesaj.ERROR, b'payload invalid', secventa)
        
        lung_cheie = struct.unpack('!H', payload[:2])[0]
        if len(payload) < 2 + lung_cheie:
            return construieste_mesaj(TipMesaj.ERROR, b'cheie incompleta', secventa)
        
        cheie = payload[2:2 + lung_cheie]
        valoare = payload[2 + lung_cheie:]
        
        magazin.seteaza(cheie, valoare)
        logger.debug(f"SET {cheie!r} = {valoare!r}")
        return construieste_mesaj(TipMesaj.RESPONSE, b'OK', secventa)
    
    elif tip == TipMesaj.GET:
        cheie = payload
        valoare = magazin.obtine(cheie)
        
        if valoare is None:
            return construieste_mesaj(TipMesaj.ERROR, b'cheie inexistenta', secventa)
        
        logger.debug(f"GET {cheie!r} -> {valoare!r}")
        return construieste_mesaj(TipMesaj.RESPONSE, valoare, secventa)
    
    elif tip == TipMesaj.DELETE:
        cheie = payload
        
        if magazin.sterge(cheie):
            logger.debug(f"DELETE {cheie!r}")
            return construieste_mesaj(TipMesaj.RESPONSE, b'OK', secventa)
        else:
            return construieste_mesaj(TipMesaj.ERROR, b'cheie inexistenta', secventa)
    
    else:
        logger.warning(f"Tip necunoscut: 0x{tip:02X}")
        return construieste_mesaj(TipMesaj.ERROR, b'tip necunoscut', secventa)


# ═══════════════════════════════════════════════════════════════════════════════
# GESTIONARE_CLIENT
# Scop: Gestionează ciclul de viață al unei conexiuni client
# Transferabil la: Orice server TCP concurent
# ═══════════════════════════════════════════════════════════════════════════════

def gestioneaza_client(socket_client: socket.socket, adresa: Tuple[str, int]) -> None:
    """
    Gestionează o conexiune client.
    
    Rulează într-un thread separat. Primește mesaje, le procesează
    și trimite răspunsuri până când clientul se deconectează.
    
    Args:
        socket_client: Socket-ul conectat la client
        adresa: Tuple (IP, port) al clientului
    """
    logger.info(f"Conexiune nouă de la {adresa[0]}:{adresa[1]}")
    buffer = b''
    
    try:
        while True:
            date = socket_client.recv(4096)
            if not date:
                logger.info(f"Client deconectat: {adresa[0]}:{adresa[1]}")
                break
            
            buffer += date
            
            # Procesare mesaje complete din buffer
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
                
                logger.debug(f"Mesaj: tip=0x{tip:02X}, seq={secventa}, len={lungime}")
                
                # Procesează și răspunde
                raspuns = proceseaza_mesaj(tip, payload, secventa)
                socket_client.sendall(raspuns)
                
    except ConnectionResetError:
        logger.warning(f"Conexiune resetată: {adresa}")
    except Exception as e:
        logger.error(f"Eroare cu clientul {adresa}: {e}")
    finally:
        socket_client.close()


# ═══════════════════════════════════════════════════════════════════════════════
# PORNIRE_SERVER
# Scop: Inițializează și pornește serverul TCP
# Transferabil la: Orice server TCP multi-threaded
# ═══════════════════════════════════════════════════════════════════════════════

def porneste_server() -> None:
    """
    Pornește serverul BINAR.
    
    Ascultă pe HOST:PORT și creează un thread nou pentru fiecare
    conexiune client. Rulează până la Ctrl+C.
    """
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
                args=(socket_client, adresa),
                daemon=True
            )
            thread.start()
            
    except KeyboardInterrupt:
        logger.info("Oprire server...")
    finally:
        server.close()
        logger.info("Server oprit.")


# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    porneste_server()
