#!/usr/bin/env python3
"""
Tema 4.01: Client Complet Protocol BINAR
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Implementați un client complet pentru protocolul BINAR care să poată
    interacționa cu un key-value store distribuit.

CERINȚE:
    1. Conectare și deconectare de la server
    2. Implementare operații: PING, SET, GET, DELETE
    3. Gestionare corectă a numărului de secvență
    4. Tratare erori și timeout-uri

INSTRUCȚIUNI:
    - Completați funcțiile marcate cu TODO
    - Respectați specificația protocolului din docs/theory_summary.md
    - Testați cu serverul din container: localhost:5401

PUNCTAJ: 50 puncte
"""

import socket
import struct
import binascii
import logging
from typing import Optional, Tuple, Any
from dataclasses import dataclass
from enum import IntEnum

# Configurare logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL
# Scop: Definește valorile fixe ale protocolului BINAR
# Transferabil la: Orice implementare de protocol cu antet fix
# ═══════════════════════════════════════════════════════════════════════════════

BINAR_MAGIC = b'NP'
BINAR_VERSIUNE = 1
BINAR_DIMENSIUNE_ANTET = 14
TIMEOUT_IMPLICIT = 5.0  # secunde


class TipMesaj(IntEnum):
    """Tipurile de mesaje suportate de protocolul BINAR."""
    PING = 0x01
    PONG = 0x02
    SET = 0x03
    GET = 0x04
    DELETE = 0x05
    RESPONSE = 0x06
    ERROR = 0xFF


# ═══════════════════════════════════════════════════════════════════════════════
# STRUCTURI_DATE
# Scop: Definește tipurile de date pentru mesaje și răspunsuri
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class RaspunsServer:
    """Răspunsul parsat de la server."""
    tip: TipMesaj
    secventa: int
    payload: bytes
    crc_valid: bool
    
    @property
    def succes(self) -> bool:
        """Returnează True dacă răspunsul indică succes."""
        return self.tip != TipMesaj.ERROR and self.crc_valid
    
    @property
    def valoare(self) -> Optional[str]:
        """Returnează payload-ul decodat ca string, sau None dacă e eroare."""
        if self.tip == TipMesaj.ERROR:
            return None
        try:
            return self.payload.decode('utf-8')
        except UnicodeDecodeError:
            return None


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE_CRC
# Scop: Calcul și verificare CRC32
# ═══════════════════════════════════════════════════════════════════════════════

def calculeaza_crc32(date: bytes) -> int:
    """
    Calculează CRC32 pentru un șir de bytes.
    
    Args:
        date: Datele pentru care se calculează CRC
        
    Returns:
        Valoarea CRC32 ca întreg pozitiv pe 32 biți
    """
    return binascii.crc32(date) & 0xFFFFFFFF


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_BINAR
# Scop: Implementează clientul pentru protocolul BINAR
# ═══════════════════════════════════════════════════════════════════════════════

class ClientBinar:
    """
    Client pentru protocolul BINAR.
    
    Exemplu utilizare:
        client = ClientBinar('localhost', 5401)
        if client.conecteaza():
            raspuns = client.ping()
            print(f"Server activ: {raspuns.succes}")
            client.deconecteaza()
    """
    
    def __init__(self, host: str, port: int, timeout: float = TIMEOUT_IMPLICIT):
        """
        Inițializează clientul.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
            timeout: Timeout pentru operații socket (secunde)
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
        self.secventa = 0
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GESTIONARE_SECVENTA
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _urmatoarea_secventa(self) -> int:
        """
        Returnează următorul număr de secvență.
        
        Secvența crește cu 1 la fiecare mesaj trimis și
        se resetează la 0 după 0xFFFFFFFF.
        
        ---
        PREDICȚIE înainte de implementare:
        1. Ce valoare maximă poate avea secvența? (hint: 4 bytes unsigned)
        2. Ce operator folosești pentru wrap-around? (hint: modulo sau AND)
        3. De ce e important să incrementezi ÎNAINTE de returnare?
        ---
        """
        # TODO: Implementați incrementarea secvenței
        # Indiciu: self.secventa trebuie să rămână în range 0 - 0xFFFFFFFF
        # Soluție posibilă: self.secventa = (self.secventa + 1) & 0xFFFFFFFF
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CONECTARE_DECONECTARE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def conecteaza(self) -> bool:
        """
        Stabilește conexiunea cu serverul.
        
        ---
        PREDICȚIE înainte de implementare:
        1. Ce excepție ridică connect() dacă serverul nu există?
        2. Cât e timeout-ul implicit al unui socket nou creat?
        3. Ce returnează connect() la succes? (hint: nimic!)
        ---
        
        Returns:
            True dacă conexiunea a reușit, False altfel
        """
        # TODO: Implementați conectarea la server
        # Indiciu:
        # 1. Creați un socket TCP (AF_INET, SOCK_STREAM)
        # 2. Setați timeout-ul cu settimeout()
        # 3. Conectați-vă la (self.host, self.port)
        # 4. Gestionați excepțiile: socket.timeout, ConnectionRefusedError, OSError
        pass
    
    def deconecteaza(self) -> None:
        """
        Închide conexiunea cu serverul.
        
        ---
        PREDICȚIE:
        1. Ce se întâmplă dacă apelezi close() pe un socket deja închis?
        2. Socket-ul mai poate fi reutilizat după close()?
        ---
        """
        # TODO: Implementați deconectarea
        # Indiciu: Verificați că socket-ul există înainte de close()
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CONSTRUIRE_MESAJE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _construieste_mesaj(self, tip: TipMesaj, payload: bytes = b'') -> bytes:
        """
        Construiește un mesaj BINAR complet.
        
        ---
        PREDICȚIE:
        1. Câți bytes va avea mesajul final pentru un PING (payload gol)?
        2. Care e ordinea bytes-ilor pentru câmpurile numerice?
        3. CRC se calculează peste ce date exact?
        ---
        
        Structura mesajului (14 bytes antet + payload):
        - Magic: 2 bytes ('NP')
        - Versiune: 1 byte
        - Tip: 1 byte
        - Lungime payload: 2 bytes (big-endian)
        - Secvență: 4 bytes (big-endian)
        - CRC32: 4 bytes (big-endian)
        - Payload: variabil
        
        Args:
            tip: Tipul mesajului
            payload: Datele utile (poate fi gol)
        
        Returns:
            Mesajul complet ca bytes
        """
        # TODO: Implementați construcția mesajului
        # Indiciu:
        # 1. Calculați lungimea payload-ului
        # 2. Construiți antetul parțial (fără CRC) cu struct.pack('!2sBBHI', ...)
        # 3. Calculați CRC32 peste antet_partial + payload
        # 4. Construiți mesajul final cu CRC inclus
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PARSARE_RASPUNSURI
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _parseaza_raspuns(self, date: bytes) -> Optional[RaspunsServer]:
        """
        Parsează răspunsul primit de la server.
        
        ---
        PREDICȚIE:
        1. Ce se întâmplă dacă primești mai puțin de 14 bytes?
        2. Cum verifici că CRC-ul primit e corect?
        3. Payload-ul unde începe în buffer?
        ---
        
        Args:
            date: Buffer-ul de date primit
        
        Returns:
            RaspunsServer parsat sau None dacă datele sunt invalide
        """
        # TODO: Implementați parsarea răspunsului
        # Indiciu:
        # 1. Verificați că avem minim 14 bytes
        # 2. Extrageți câmpurile cu struct.unpack('!2sBBHII', date[:14])
        # 3. Verificați magic-ul
        # 4. Extrageți payload-ul
        # 5. Verificați CRC-ul
        # 6. Returnați un RaspunsServer
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COMUNICARE_RETEA
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _trimite_si_primeste(self, tip: TipMesaj, payload: bytes = b'') -> Optional[RaspunsServer]:
        """
        Trimite un mesaj și așteaptă răspunsul.
        
        Args:
            tip: Tipul mesajului de trimis
            payload: Payload-ul mesajului
        
        Returns:
            Răspunsul parsat sau None dacă a eșuat
        """
        if self.socket is None:
            logger.error("Nu sunteți conectat la server")
            return None
        
        # TODO: Implementați trimiterea și recepția
        # Indiciu:
        # 1. Construiți mesajul cu _construieste_mesaj
        # 2. Trimiteți cu sendall()
        # 3. Primiți răspunsul cu recv()
        # 4. Parsați răspunsul cu _parseaza_raspuns
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAȚII_PROTOCOL
    # Scop: Implementează operațiile de nivel înalt ale protocolului
    # ═══════════════════════════════════════════════════════════════════════════
    
    def ping(self) -> Optional[RaspunsServer]:
        """
        Trimite un mesaj PING pentru a verifica conexiunea.
        
        Returns:
            Răspunsul PONG sau None dacă a eșuat
        """
        logger.info("Trimit PING...")
        return self._trimite_si_primeste(TipMesaj.PING)
    
    def set(self, cheie: str, valoare: str) -> Optional[RaspunsServer]:
        """
        Setează o valoare în key-value store.
        
        ---
        PREDICȚIE:
        1. Cum separi cheia de valoare în payload?
        2. Ce răspuns aștepți de la server la SET reușit?
        ---
        
        Args:
            cheie: Cheia de setat
            valoare: Valoarea de asociat
        
        Returns:
            Răspunsul serverului
        """
        # TODO: Implementați operația SET
        # Indiciu: Payload format din: lungime_cheie (2 bytes) + cheie + valoare
        # lung_cheie = len(cheie.encode('utf-8'))
        # payload = struct.pack('!H', lung_cheie) + cheie.encode() + valoare.encode()
        pass
    
    def get(self, cheie: str) -> Optional[RaspunsServer]:
        """
        Citește o valoare din key-value store.
        
        Args:
            cheie: Cheia de citit
        
        Returns:
            Răspunsul cu valoarea sau eroare
        """
        # TODO: Implementați operația GET
        # Indiciu: Payload-ul conține doar cheia
        pass
    
    def delete(self, cheie: str) -> Optional[RaspunsServer]:
        """
        Șterge o cheie din key-value store.
        
        Args:
            cheie: Cheia de șters
        
        Returns:
            Răspunsul serverului
        """
        # TODO: Implementați operația DELETE
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRAȚIE
# ═══════════════════════════════════════════════════════════════════════════════

def demonstratie():
    """Demonstrează utilizarea clientului BINAR."""
    print("=" * 60)
    print("Demonstrație Client Protocol BINAR")
    print("=" * 60)
    
    # Creați clientul
    client = ClientBinar('localhost', 5401)
    
    # Conectare
    print("\n1. Conectare la server...")
    if not client.conecteaza():
        print("   EROARE: Nu s-a putut conecta!")
        print("   Verificați că laboratorul e pornit: python3 scripts/start_lab.py")
        return
    print("   Conectat cu succes!")
    
    # Test PING
    print("\n2. Test PING...")
    raspuns = client.ping()
    if raspuns and raspuns.succes:
        print(f"   PONG primit! (secvență: {raspuns.secventa})")
    else:
        print("   EROARE la PING!")
    
    # Test SET
    print("\n3. Test SET...")
    raspuns = client.set("nume", "Student ASE")
    if raspuns and raspuns.succes:
        print("   SET reușit!")
    else:
        print("   EROARE la SET!")
    
    # Test GET
    print("\n4. Test GET...")
    raspuns = client.get("nume")
    if raspuns and raspuns.succes:
        print(f"   Valoare: {raspuns.valoare}")
    else:
        print("   EROARE la GET!")
    
    # Test DELETE
    print("\n5. Test DELETE...")
    raspuns = client.delete("nume")
    if raspuns and raspuns.succes:
        print("   DELETE reușit!")
    else:
        print("   EROARE la DELETE!")
    
    # Verificare ștergere
    print("\n6. Verificare ștergere (GET pe cheie ștearsă)...")
    raspuns = client.get("nume")
    if raspuns and raspuns.tip == TipMesaj.ERROR:
        print("   Corect: cheia nu mai există!")
    else:
        print("   AVERTISMENT: cheia încă există?!")
    
    # Deconectare
    print("\n7. Deconectare...")
    client.deconecteaza()
    print("   Deconectat!")
    
    print("\n" + "=" * 60)
    print("Demonstrație completă!")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-EVALUARE (completează înainte de predare)
# ═══════════════════════════════════════════════════════════════════════════════
# □ Codul rulează fără erori de sintaxă
# □ Toate funcțiile marcate cu TODO sunt implementate
# □ Am testat cu serverul din container (localhost:5401)
# □ PING funcționează și primesc PONG
# □ SET funcționează (verific cu GET)
# □ GET returnează valoarea corectă
# □ DELETE funcționează (GET după DELETE returnează eroare)
# □ CRC-ul se calculează corect (verificat în Wireshark)
# □ Am înțeles de ce folosim '!' în struct.pack (network byte order)
# □ Am înțeles diferența dintre antet și payload
# □ Secvența se incrementează corect la fiecare mesaj
# ═══════════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    demonstratie()
