#!/usr/bin/env python3
"""
Client Protocol BINAR
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Client pentru protocolul BINAR cu antet fix și verificare CRC32.
Port implicit: 5401
"""

import socket
import struct
import binascii
import sys

# Configurație
HOST = 'localhost'
PORT = 5401
TIMEOUT = 10.0
DIMENSIUNE_ANTET = 14
MAGIC = b'NP'
VERSIUNE = 1


class TipMesaj:
    """Constante pentru tipurile de mesaje."""
    PING = 0x01
    PONG = 0x02
    SET = 0x03
    GET = 0x04
    DELETE = 0x05
    RESPONSE = 0x06
    ERROR = 0xFF
    
    @classmethod
    def nume(cls, tip: int) -> str:
        nume_dict = {
            cls.PING: "PING",
            cls.PONG: "PONG",
            cls.SET: "SET",
            cls.GET: "GET",
            cls.DELETE: "DELETE",
            cls.RESPONSE: "RESPONSE",
            cls.ERROR: "ERROR"
        }
        return nume_dict.get(tip, f"NECUNOSCUT({tip:02X})")


def calculeaza_crc(date: bytes) -> int:
    """Calculează CRC32 pentru date."""
    return binascii.crc32(date) & 0xFFFFFFFF


def construieste_mesaj(tip: int, payload: bytes, secventa: int) -> bytes:
    """Construiește un mesaj binar complet."""
    lungime = len(payload)
    
    antet_partial = struct.pack('!2sBBHI',
        MAGIC, VERSIUNE, tip, lungime, secventa
    )
    
    crc = calculeaza_crc(antet_partial + payload)
    
    mesaj = struct.pack('!2sBBHII',
        MAGIC, VERSIUNE, tip, lungime, secventa, crc
    ) + payload
    
    return mesaj


def parseaza_raspuns(date: bytes) -> dict:
    """Parsează un răspuns binar."""
    if len(date) < DIMENSIUNE_ANTET:
        raise ValueError(f"Răspuns prea scurt: {len(date)}")
    
    magic, versiune, tip, lungime, secventa, crc = struct.unpack(
        '!2sBBHII', date[:DIMENSIUNE_ANTET]
    )
    
    payload = date[DIMENSIUNE_ANTET:DIMENSIUNE_ANTET + lungime]
    
    return {
        'magic': magic,
        'versiune': versiune,
        'tip': tip,
        'lungime': lungime,
        'secventa': secventa,
        'crc': crc,
        'payload': payload
    }


class ClientBinar:
    """Client pentru protocolul BINAR."""
    
    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port
        self.socket = None
        self.secventa = 0
    
    def conecteaza(self):
        """Stabilește conexiunea la server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(TIMEOUT)
        self.socket.connect((self.host, self.port))
    
    def deconecteaza(self):
        """Închide conexiunea."""
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def _urmatoarea_secventa(self) -> int:
        """Returnează următorul număr de secvență."""
        self.secventa += 1
        return self.secventa
    
    def _trimite_si_primeste(self, tip: int, payload: bytes = b'') -> dict:
        """Trimite un mesaj și primește răspunsul."""
        secventa = self._urmatoarea_secventa()
        mesaj = construieste_mesaj(tip, payload, secventa)
        
        self.socket.sendall(mesaj)
        raspuns = self.socket.recv(4096)
        
        return parseaza_raspuns(raspuns)
    
    def ping(self) -> bool:
        """Trimite PING și verifică PONG."""
        raspuns = self._trimite_si_primeste(TipMesaj.PING)
        return raspuns['tip'] == TipMesaj.PONG
    
    def seteaza(self, cheie: str, valoare: str) -> bool:
        """Setează o valoare."""
        cheie_bytes = cheie.encode('utf-8')
        valoare_bytes = valoare.encode('utf-8')
        
        # Payload: lungime_cheie (2) + cheie + valoare
        payload = struct.pack('!H', len(cheie_bytes)) + cheie_bytes + valoare_bytes
        
        raspuns = self._trimite_si_primeste(TipMesaj.SET, payload)
        return raspuns['tip'] == TipMesaj.RESPONSE
    
    def obtine(self, cheie: str) -> str:
        """Obține o valoare."""
        cheie_bytes = cheie.encode('utf-8')
        raspuns = self._trimite_si_primeste(TipMesaj.GET, cheie_bytes)
        
        if raspuns['tip'] == TipMesaj.ERROR:
            return None
        
        return raspuns['payload'].decode('utf-8')
    
    def sterge(self, cheie: str) -> bool:
        """Șterge o cheie."""
        cheie_bytes = cheie.encode('utf-8')
        raspuns = self._trimite_si_primeste(TipMesaj.DELETE, cheie_bytes)
        return raspuns['tip'] == TipMesaj.RESPONSE


def demonstratie():
    """Demonstrație a clientului binar."""
    print("=" * 50)
    print("Demonstrație Client Protocol BINAR")
    print("=" * 50)
    
    client = ClientBinar()
    
    try:
        print(f"\nConectare la {HOST}:{PORT}...")
        client.conecteaza()
        print("Conectat!")
        
        # Test PING
        print("\n1. Test PING/PONG:")
        if client.ping():
            print("   ✓ Server răspunde la PING")
        else:
            print("   ✗ PING eșuat")
        
        # Test SET
        print("\n2. Test SET:")
        if client.seteaza("cheie_test", "valoare_test"):
            print("   ✓ SET reușit")
        else:
            print("   ✗ SET eșuat")
        
        # Test GET
        print("\n3. Test GET:")
        valoare = client.obtine("cheie_test")
        if valoare:
            print(f"   ✓ GET: cheie_test = {valoare}")
        else:
            print("   ✗ GET eșuat")
        
        # Test DELETE
        print("\n4. Test DELETE:")
        if client.sterge("cheie_test"):
            print("   ✓ DELETE reușit")
        else:
            print("   ✗ DELETE eșuat")
        
        # Verificare ștergere
        print("\n5. Verificare ștergere:")
        valoare = client.obtine("cheie_test")
        if valoare is None:
            print("   ✓ Cheie ștearsă corect")
        else:
            print("   ✗ Cheie încă există")
        
    except ConnectionRefusedError:
        print(f"\nEroare: Nu se poate conecta la {HOST}:{PORT}")
        print("Asigurați-vă că serverul BINAR rulează.")
        sys.exit(1)
    except Exception as e:
        print(f"\nEroare: {e}")
        sys.exit(1)
    finally:
        client.deconecteaza()
        print("\nDeconectat.")


if __name__ == "__main__":
    demonstratie()
