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

import socket
import struct
import binascii
import logging
from datetime import datetime
from typing import Dict, List

# Configurare logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurație server
HOST = '0.0.0.0'
PORT = 5402
DIMENSIUNE_DATAGRAMA = 23


class RegistruSenzori:
    """Registru pentru urmărirea senzorilor și citirilor lor."""
    
    def __init__(self):
        self._citiri: Dict[int, List[dict]] = {}
        self._max_citiri = 100  # Per senzor
    
    def adauga_citire(self, sensor_id: int, temperatura: float, locatie: str):
        """Adaugă o citire de la un senzor."""
        if sensor_id not in self._citiri:
            self._citiri[sensor_id] = []
        
        citire = {
            'temperatura': temperatura,
            'locatie': locatie,
            'timestamp': datetime.now().isoformat()
        }
        
        self._citiri[sensor_id].append(citire)
        
        # Păstrează doar ultimele N citiri
        if len(self._citiri[sensor_id]) > self._max_citiri:
            self._citiri[sensor_id] = self._citiri[sensor_id][-self._max_citiri:]
    
    def obtine_citiri(self, sensor_id: int) -> List[dict]:
        """Obține citirile pentru un senzor."""
        return self._citiri.get(sensor_id, [])
    
    def obtine_ultima_citire(self, sensor_id: int) -> dict:
        """Obține ultima citire pentru un senzor."""
        citiri = self._citiri.get(sensor_id, [])
        return citiri[-1] if citiri else None
    
    def obtine_senzori_activi(self) -> List[int]:
        """Returnează lista de senzori activi."""
        return list(self._citiri.keys())
    
    def statistica(self) -> dict:
        """Returnează statistici despre senzori."""
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


def calculeaza_crc(date: bytes) -> int:
    """Calculează CRC32 pentru date."""
    return binascii.crc32(date) & 0xFFFFFFFF


def parseaza_datagrama(date: bytes) -> dict:
    """
    Parsează o datagramă de senzor.
    
    Returns:
        Dicționar cu datele senzorului
    
    Raises:
        ValueError: Dacă datagrama este invalidă
    """
    if len(date) != DIMENSIUNE_DATAGRAMA:
        raise ValueError(f"Dimensiune invalidă: {len(date)} (așteptat {DIMENSIUNE_DATAGRAMA})")
    
    # Despachetare
    versiune = date[0]
    sensor_id = struct.unpack('!H', date[1:3])[0]
    temperatura = struct.unpack('!f', date[3:7])[0]
    locatie = date[7:17].rstrip(b'\x00').decode('utf-8', errors='replace')
    crc_primit = struct.unpack('!I', date[17:21])[0]
    
    # Verificare CRC
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


def afiseaza_citire(citire: dict, adresa: tuple):
    """Afișează o citire de senzor."""
    stare_crc = "✓" if citire['crc_valid'] else "✗"
    
    logger.info(
        f"[{stare_crc}] Senzor #{citire['sensor_id']:04d} | "
        f"Temp: {citire['temperatura']:6.2f}°C | "
        f"Loc: {citire['locatie']:10s} | "
        f"De la: {adresa[0]}:{adresa[1]}"
    )


def porneste_server():
    """Pornește serverul UDP pentru senzori."""
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
                    logger.debug(f"Date: {date.hex()}")
                    
            except socket.timeout:
                continue
                
    except KeyboardInterrupt:
        print()
        logger.info("Oprire server...")
        
        # Afișează statistici
        stat = registru.statistica()
        logger.info(f"Statistici finale: {stat['numar_senzori']} senzori, {stat['total_citiri']} citiri totale")
        
    finally:
        server.close()


if __name__ == "__main__":
    porneste_server()
