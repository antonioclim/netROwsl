#!/usr/bin/env python3
"""
Exercițiul 2: Client Protocol BINAR
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Obiectiv: Implementați un client pentru protocolul BINAR.

Structura antetului (14 octeți):
┌─────────┬──────────┬─────┬────────┬──────────┬───────┐
│ Magic   │ Versiune │ Tip │ Lungime│ Secvență │ CRC32 │
│ 2 octeți│ 1 octet  │1 oct│ 2 oct  │ 4 octeți │ 4 oct │
└─────────┴──────────┴─────┴────────┴──────────┴───────┘

Tipuri de mesaje:
- PING (0x01): Verificare conexiune
- PONG (0x02): Răspuns la PING
- SET (0x03): Setare valoare
- GET (0x04): Citire valoare
- DELETE (0x05): Ștergere cheie
- RESPONSE (0x06): Răspuns generic
- ERROR (0xFF): Eroare

Sarcini:
1. Completați funcția construieste_mesaj()
2. Completați funcția parseaza_raspuns()
3. Implementați funcția ping()
4. Implementați funcțiile get() și set()
"""

import socket
import struct
import binascii

# Constante protocol
HOST = 'localhost'
PORT = 5401
MAGIC = b'NP'
VERSIUNE = 1
DIMENSIUNE_ANTET = 14


class TipMesaj:
    """Tipuri de mesaje pentru protocolul BINAR."""
    PING = 0x01
    PONG = 0x02
    SET = 0x03
    GET = 0x04
    DELETE = 0x05
    RESPONSE = 0x06
    ERROR = 0xFF


def calculeaza_crc(date: bytes) -> int:
    """
    Calculează CRC32 pentru date.
    
    Args:
        date: Datele pentru care se calculează CRC
    
    Returns:
        Valoarea CRC32 (întreg pozitiv pe 32 de biți)
    """
    return binascii.crc32(date) & 0xFFFFFFFF


def construieste_mesaj(tip: int, payload: bytes, secventa: int) -> bytes:
    """
    Construiește un mesaj în format protocol BINAR.
    
    SARCINA 1: Completați această funcție
    
    Args:
        tip: Tipul mesajului (vezi clasa TipMesaj)
        payload: Conținutul mesajului (bytes)
        secventa: Numărul de secvență
    
    Returns:
        Mesajul complet ca bytes (antet + payload)
    
    Indicii:
    - Folosiți struct.pack() cu formatul '!2sBBHI' pentru antet fără CRC
    - Calculați CRC peste antet_partial + payload
    - Apoi construiți mesajul complet cu formatul '!2sBBHII'
    """
    # TODO: Implementați construirea mesajului
    # Pas 1: Creați antetul parțial (fără CRC)
    # Pas 2: Calculați CRC
    # Pas 3: Construiți mesajul complet
    
    pass  # Înlocuiți cu implementarea dvs.


def parseaza_raspuns(date: bytes) -> dict:
    """
    Parsează un răspuns în format protocol BINAR.
    
    SARCINA 2: Completați această funcție
    
    Args:
        date: Răspunsul primit de la server
    
    Returns:
        Dicționar cu câmpurile:
        {
            'magic': bytes,
            'versiune': int,
            'tip': int,
            'lungime': int,
            'secventa': int,
            'crc': int,
            'payload': bytes,
            'crc_valid': bool
        }
    
    Indicii:
    - Verificați că aveți cel puțin DIMENSIUNE_ANTET octeți
    - Folosiți struct.unpack() cu formatul '!2sBBHII'
    - Verificați CRC-ul primit
    """
    # TODO: Implementați parsarea răspunsului
    
    pass  # Înlocuiți cu implementarea dvs.


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
        self.socket.settimeout(10.0)
        self.socket.connect((self.host, self.port))
        print(f"Conectat la {self.host}:{self.port}")
    
    def deconecteaza(self):
        """Închide conexiunea."""
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Deconectat")
    
    def _urmatoarea_secventa(self) -> int:
        """Returnează următorul număr de secvență."""
        self.secventa += 1
        return self.secventa
    
    def _trimite_si_primeste(self, tip: int, payload: bytes = b'') -> dict:
        """
        Trimite un mesaj și primește răspunsul.
        
        Args:
            tip: Tipul mesajului
            payload: Conținutul (opțional)
        
        Returns:
            Răspunsul parsat
        """
        secventa = self._urmatoarea_secventa()
        mesaj = construieste_mesaj(tip, payload, secventa)
        
        if mesaj is None:
            raise NotImplementedError("Funcția construieste_mesaj() nu este implementată")
        
        self.socket.sendall(mesaj)
        raspuns = self.socket.recv(4096)
        
        rezultat = parseaza_raspuns(raspuns)
        if rezultat is None:
            raise NotImplementedError("Funcția parseaza_raspuns() nu este implementată")
        
        return rezultat
    
    def ping(self) -> bool:
        """
        Trimite un mesaj PING și verifică răspunsul PONG.
        
        SARCINA 3: Completați această funcție
        
        Returns:
            True dacă serverul răspunde cu PONG
        """
        # TODO: Implementați PING
        # Indiciu: Trimiteți un mesaj de tip TipMesaj.PING și verificați
        # dacă răspunsul are tipul TipMesaj.PONG
        
        pass  # Înlocuiți cu implementarea dvs.
    
    def seteaza(self, cheie: str, valoare: str) -> bool:
        """
        Setează o valoare pentru o cheie.
        
        SARCINA 4a: Completați această funcție
        
        Args:
            cheie: Numele cheii
            valoare: Valoarea de setat
        
        Returns:
            True dacă operațiunea a reușit
        
        Indicii:
        - Payload format: lungime_cheie (2 octeți) + cheie + valoare
        - Folosiți struct.pack('!H', len(cheie_bytes)) pentru lungime
        """
        # TODO: Implementați SET
        
        pass  # Înlocuiți cu implementarea dvs.
    
    def obtine(self, cheie: str) -> str:
        """
        Obține valoarea pentru o cheie.
        
        SARCINA 4b: Completați această funcție
        
        Args:
            cheie: Numele cheii
        
        Returns:
            Valoarea sau None dacă cheia nu există
        """
        # TODO: Implementați GET
        
        pass  # Înlocuiți cu implementarea dvs.


def main():
    """Funcția principală pentru testare."""
    print("=" * 50)
    print("Exercițiul 2: Client Protocol BINAR")
    print("=" * 50)
    
    client = ClientBinar()
    
    try:
        client.conecteaza()
        
        # Test PING
        print("\n1. Test PING...")
        rezultat = client.ping()
        if rezultat:
            print("   ✅ PING reușit!")
        elif rezultat is None:
            print("   ⚠️  Funcția ping() nu este implementată")
        else:
            print("   ❌ PING eșuat")
        
        # Test SET
        print("\n2. Test SET...")
        rezultat = client.seteaza("test_cheie", "test_valoare")
        if rezultat:
            print("   ✅ SET reușit!")
        elif rezultat is None:
            print("   ⚠️  Funcția seteaza() nu este implementată")
        else:
            print("   ❌ SET eșuat")
        
        # Test GET
        print("\n3. Test GET...")
        valoare = client.obtine("test_cheie")
        if valoare:
            print(f"   ✅ GET reușit: {valoare}")
        elif valoare is None:
            print("   ⚠️  Funcția obtine() nu este implementată sau cheia nu există")
        
    except NotImplementedError as e:
        print(f"\n⚠️  {e}")
        print("Completați funcțiile marcate cu TODO!")
    except ConnectionRefusedError:
        print(f"\n❌ Nu se poate conecta la {HOST}:{PORT}")
        print("Asigurați-vă că serverul BINAR rulează.")
    except Exception as e:
        print(f"\n❌ Eroare: {e}")
    finally:
        client.deconecteaza()


if __name__ == "__main__":
    main()
