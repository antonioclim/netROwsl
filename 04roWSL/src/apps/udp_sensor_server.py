#!/usr/bin/env python3
"""
Server Senzor UDP
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Server UDP pentru recepția datelor de la senzori IoT.
Fiecare datagramă are fix 23 de octeți.
Port implicit: 5402

Structura datagramei:
- Versiune: 1 octet
- ID Senzor: 2 octeți (big-endian)
- Temperatură: 4 octeți (float, big-endian)
- Locație: 10 octeți (string, padding cu null)
- CRC32: 4 octeți (big-endian)
- Rezervat: 2 octeți
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# Scop: Importă modulele necesare pentru networking UDP și procesare binară
# Transferabil la: Orice server UDP cu protocol binar
# ═══════════════════════════════════════════════════════════════════════════════

import socket
import struct
import binascii
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional

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
# Scop: Definește valorile fixe ale protocolului senzor
# Transferabil la: Orice implementare de protocol cu datagrame de dimensiune fixă
# ═══════════════════════════════════════════════════════════════════════════════

HOST: str = '0.0.0.0'
PORT: int = 5402
DIMENSIUNE_DATAGRAMA: int = 23
VERSIUNE_SUPORTATA: int = 1


# ═══════════════════════════════════════════════════════════════════════════════
# STOCARE_DATE
# Scop: Implementează un registru pentru urmărirea citirilor de la senzori
# Transferabil la: Orice sistem IoT cu agregare date multi-senzor
# ═══════════════════════════════════════════════════════════════════════════════

class RegistruSenzori:
    """Registru pentru urmărirea senzorilor și citirilor lor."""
    
    def __init__(self, max_citiri_per_senzor: int = 100) -> None:
        """
        Inițializează registrul.
        
        Args:
            max_citiri_per_senzor: Numărul maxim de citiri păstrate per senzor
        """
        self._citiri: Dict[int, List[dict]] = {}
        self._max_citiri = max_citiri_per_senzor
    
    def adauga_citire(self, sensor_id: int, temperatura: float, locatie: str) -> None:
        """
        Adaugă o citire de la un senzor.
        
        Args:
            sensor_id: ID-ul senzorului
            temperatura: Valoarea temperaturii
            locatie: Locația senzorului
        """
        if sensor_id not in self._citiri:
            self._citiri[sensor_id] = []
        
        citire = {
            'temperatura': temperatura,
            'locatie': locatie,
            'timestamp': datetime.now().isoformat()
        }
        
        self._citiri[sensor_id].append(citire)
        
        # Păstrează doar ultimele N citiri (FIFO)
        if len(self._citiri[sensor_id]) > self._max_citiri:
            self._citiri[sensor_id] = self._citiri[sensor_id][-self._max_citiri:]
    
    def obtine_citiri(self, sensor_id: int) -> List[dict]:
        """Obține toate citirile pentru un senzor."""
        return self._citiri.get(sensor_id, [])
    
    def obtine_ultima_citire(self, sensor_id: int) -> Optional[dict]:
        """Obține ultima citire pentru un senzor."""
        citiri = self._citiri.get(sensor_id, [])
        return citiri[-1] if citiri else None
    
    def obtine_senzori_activi(self) -> List[int]:
        """Returnează lista de ID-uri ale senzorilor activi."""
        return list(self._citiri.keys())
    
    def statistica(self) -> dict:
        """
        Returnează statistici despre senzori.
        
        Returns:
            Dicționar cu: numar_senzori, total_citiri, senzori (per-senzor counts)
        """
        total_citiri = sum(len(c) for c in self._citiri.values())
        return {
            'numar_senzori': len(self._citiri),
            'total_citiri': total_citiri,
            'senzori': {
                sid: len(citiri) 
                for sid, citiri in self._citiri.items()
            }
        }


# Instanță globală
registru = RegistruSenzori()


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


# ═══════════════════════════════════════════════════════════════════════════════
# PARSARE_PROTOCOL
# Scop: Extragerea și validarea câmpurilor din datagrame
# Transferabil la: Orice parser de protocol binar cu dimensiune fixă
# ═══════════════════════════════════════════════════════════════════════════════

def parseaza_datagrama(date: bytes) -> dict:
    """
    Parsează o datagramă de senzor.
    
    Structura (23 octeți):
    - [0]: Versiune (1 byte)
    - [1-2]: Sensor ID (2 bytes, big-endian)
    - [3-6]: Temperatură (4 bytes, float big-endian)
    - [7-16]: Locație (10 bytes, null-padded)
    - [17-20]: CRC32 (4 bytes, big-endian)
    - [21-22]: Rezervat (2 bytes)
    
    Args:
        date: Datagrama brută de 23 bytes
    
    Returns:
        Dicționar cu câmpurile parsate și crc_valid
    
    Raises:
        ValueError: Dacă datagrama are dimensiune greșită
    """
    if len(date) != DIMENSIUNE_DATAGRAMA:
        raise ValueError(f"Dimensiune invalidă: {len(date)} (așteptat {DIMENSIUNE_DATAGRAMA})")
    
    # Despachetare câmpuri
    versiune = date[0]
    sensor_id = struct.unpack('!H', date[1:3])[0]
    temperatura = struct.unpack('!f', date[3:7])[0]
    locatie = date[7:17].rstrip(b'\x00').decode('utf-8', errors='replace')
    crc_primit = struct.unpack('!I', date[17:21])[0]
    
    # Verificare CRC (calculat peste primii 17 bytes)
    crc_calculat = calculeaza_crc(date[:17])
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
# AFISARE_DATE
# Scop: Formatează și afișează citirile de la senzori
# Transferabil la: Orice sistem de monitorizare cu output formatat
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_citire(citire: dict, adresa: Tuple[str, int]) -> None:
    """
    Afișează o citire de senzor în format formatat.
    
    Args:
        citire: Dicționarul cu datele parsate
        adresa: Tuple (IP, port) de la care a venit datagrama
    """
    stare_crc = "OK" if citire['crc_valid'] else "ERR"
    
    logger.info(
        f"[{stare_crc:3s}] Senzor #{citire['sensor_id']:04d} | "
        f"Temp: {citire['temperatura']:6.2f}C | "
        f"Loc: {citire['locatie']:10s} | "
        f"De la: {adresa[0]}:{adresa[1]}"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PORNIRE_SERVER
# Scop: Inițializează și pornește serverul UDP
# Transferabil la: Orice server UDP datagram-based
# ═══════════════════════════════════════════════════════════════════════════════

def porneste_server() -> None:
    """
    Pornește serverul UDP pentru senzori.
    
    Ascultă pe HOST:PORT și procesează datagrame de 23 bytes.
    Rulează până la Ctrl+C, apoi afișează statistici finale.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        logger.info(f"Server Senzor UDP pornit pe {HOST}:{PORT}")
        logger.info(f"Aștept datagrame de {DIMENSIUNE_DATAGRAMA} octeți...")
        logger.info("(Ctrl+C pentru oprire)")
        print()
        
        while True:
            try:
                date, adresa = server.recvfrom(1024)
                
                try:
                    citire = parseaza_datagrama(date)
                    afiseaza_citire(citire, adresa)
                    
                    if citire['crc_valid']:
                        registru.adauga_citire(
                            citire['sensor_id'],
                            citire['temperatura'],
                            citire['locatie']
                        )
                    else:
                        logger.warning(f"CRC invalid de la senzor #{citire['sensor_id']}")
                        
                except ValueError as e:
                    logger.warning(f"Datagramă invalidă de la {adresa}: {e}")
                    logger.debug(f"Date hex: {date.hex()}")
                    
            except socket.timeout:
                continue
                
    except KeyboardInterrupt:
        print()
        logger.info("Oprire server...")
        
        # Afișează statistici finale
        stat = registru.statistica()
        logger.info(f"Statistici finale: {stat['numar_senzori']} senzori, "
                   f"{stat['total_citiri']} citiri totale")
        
    finally:
        server.close()
        logger.info("Server oprit.")


# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    porneste_server()
