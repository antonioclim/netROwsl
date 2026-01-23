#!/usr/bin/env python3
"""
Exemplu 2: Diferența dintre bytes și str
========================================
Demonstrează conversia între text și date binare în Python.

Curs: Rețele de Calculatoare - ASE București, CSIE
Autor: ing. dr. Antonio Clim
Versiune: 2.1 — cu subgoal labels și comentarii extinse

💡 ANALOGIE: Bytes și Strings ca Scrisori și Telegrame
------------------------------------------------------
- String = scrisoare în română pe care o citești direct
- Bytes = telegramă codificată în Morse — trebuie decodată ca să o înțelegi
- encode() = a traduce scrisoarea în Morse pentru transmisie
- decode() = a traduce Morse-ul înapoi în text lizibil

Rețeaua "vorbește" doar în Morse (bytes). Calculatorul tău "gândește" în text (strings).

Obiective de învățare:
- Înțelegerea diferenței fundamentale între str și bytes
- Gestionarea erorilor de encoding pentru caractere speciale
- Pattern-uri pentru lucrul cu fișiere binare
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import logging
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURARE_LOGGING
# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: Logging-ul e preferat față de print() pentru debugging în producție
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRATIE_CONVERSIE_BAZA
# ═══════════════════════════════════════════════════════════════════════════════
def demonstreaza_conversie() -> None:
    """Demonstrează conversia fundamentală între str și bytes.
    
    Parcurge exemplele de bază ale conversiei, incluzând:
    - Diferența vizuală între str și bytes
    - Folosirea encode() și decode()
    - Bytes literals pentru protocoale de rețea
    - Reprezentarea hexadecimală a adreselor IP
    
    Returns:
        None. Afișează output la consolă.
        
    Example:
        >>> demonstreaza_conversie()
        String: Salut, Rețele!
        Tip: <class 'str'>
        ...
    """
    print("=" * 60)
    print("DEMONSTRAȚIE: bytes vs str în Python")
    print("=" * 60)
    
    # ─────────────────────────────────────────────────────────────────
    # PARTEA_1_STRINGURI
    # ─────────────────────────────────────────────────────────────────
    print("\n📝 PARTEA 1: String-uri (str)")
    print("-" * 40)
    
    # NOTE: String-urile sunt pentru text pe care oamenii îl citesc
    text: str = "Salut, Rețele!"
    print(f"String: {text}")
    print(f"Tip: {type(text)}")
    print(f"Lungime în caractere: {len(text)}")
    
    # ─────────────────────────────────────────────────────────────────
    # PARTEA_2_CONVERSIE_LA_BYTES
    # ─────────────────────────────────────────────────────────────────
    print("\n📦 PARTEA 2: Conversie str → bytes (encode)")
    print("-" * 40)
    
    # NOTE: encode() transformă textul în bytes pentru transmisie pe rețea
    octeti: bytes = text.encode('utf-8')
    print(f"Bytes: {octeti}")
    print(f"Tip: {type(octeti)}")
    print(f"Lungime în bytes: {len(octeti)}")
    # HACK: Caracterele românești (ț, ș) ocupă 2 bytes în UTF-8!
    print(f"  → Observă: 14 caractere = 16 bytes (ț și e ocupă 2 bytes fiecare)")
    
    # ─────────────────────────────────────────────────────────────────
    # PARTEA_3_CONVERSIE_INAPOI
    # ─────────────────────────────────────────────────────────────────
    print("\n🔄 PARTEA 3: Conversie bytes → str (decode)")
    print("-" * 40)
    
    # NOTE: decode() transformă bytes înapoi în text citibil
    text_decodat: str = octeti.decode('utf-8')
    print(f"Decodat: {text_decodat}")
    print(f"Original == Decodat: {text == text_decodat}")
    
    # ─────────────────────────────────────────────────────────────────
    # PARTEA_4_BYTES_LITERALS
    # ─────────────────────────────────────────────────────────────────
    print("\n🌐 PARTEA 4: Bytes literals pentru protocoale")
    print("-" * 40)
    
    # NOTE: Prefixul b"..." creează direct bytes, nu string
    # Folosit pentru protocoale de rețea unde structura e fixă
    http_request: bytes = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
    print(f"HTTP Request (bytes):")
    print(f"  {http_request}")
    print(f"  Lungime: {len(http_request)} bytes")
    
    # ─────────────────────────────────────────────────────────────────
    # PARTEA_5_REPREZENTARE_HEX
    # ─────────────────────────────────────────────────────────────────
    print("\n🔢 PARTEA 5: Reprezentare hexadecimală")
    print("-" * 40)
    
    # NOTE: Adresele IP sunt numere pe 4 bytes
    # 192.168.1.1 = 0xC0.0xA8.0x01.0x01
    ip_bytes: bytes = b'\xC0\xA8\x01\x01'
    print(f"IP 192.168.1.1 ca bytes: {ip_bytes}")
    print(f"Hex: {ip_bytes.hex()}")
    print(f"  → C0 = 192, A8 = 168, 01 = 1, 01 = 1")
    
    # Conversie înapoi la string IP
    octeti_ip: list[int] = list(ip_bytes)
    ip_str: str = '.'.join(str(b) for b in octeti_ip)
    print(f"Reconstruit: {ip_str}")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRATIE_ERORI_ENCODING
# ═══════════════════════════════════════════════════════════════════════════════
def demonstreaza_erori_encoding() -> None:
    """Demonstrează erorile comune de encoding și cum să le gestionezi.
    
    Arată ce se întâmplă când:
    - Încerci să encodezi caractere românești în ASCII
    - Primești bytes invalide pentru UTF-8
    - Diferite strategii de gestionare a erorilor
    
    Returns:
        None. Afișează output la consolă.
        
    Example:
        >>> demonstreaza_erori_encoding()
        ⚠️  Eroare la encoding ASCII: ...
    """
    print("\n" + "=" * 60)
    print("DEMONSTRAȚIE: Gestionarea erorilor de encoding")
    print("=" * 60)
    
    # ─────────────────────────────────────────────────────────────────
    # EROARE_1_ASCII_ROMANE
    # ─────────────────────────────────────────────────────────────────
    print("\n❌ EROARE 1: Encoding ASCII pentru text românesc")
    print("-" * 40)
    
    text_romanesc: str = "Ștefan și Îțî"
    
    try:
        # WARNING: ASCII nu suportă caractere românești!
        octeti_ascii: bytes = text_romanesc.encode('ascii')
        print(f"Rezultat: {octeti_ascii}")  # Nu se va executa
    except UnicodeEncodeError as e:
        logger.warning(f"Encoding ASCII eșuat: {e}")
        print(f"⚠️  Eroare: {e}")
        print("  → ASCII nu suportă caractere românești (Ș, ț, Î, etc.)")
        print("  → SOLUȚIE: Folosește UTF-8 în loc de ASCII")
    
    # NOTE: UTF-8 e standardul modern și suportă toate caracterele
    print("\n✅ SOLUȚIE: UTF-8")
    octeti_utf8: bytes = text_romanesc.encode('utf-8')
    print(f"UTF-8: {octeti_utf8}")
    print(f"Decodat corect: {octeti_utf8.decode('utf-8')}")
    
    # ─────────────────────────────────────────────────────────────────
    # EROARE_2_BYTES_INVALIDE
    # ─────────────────────────────────────────────────────────────────
    print("\n❌ EROARE 2: Decoding bytes invalide")
    print("-" * 40)
    
    # NOTE: Acești bytes nu sunt UTF-8 valid (secvențe incomplete)
    bytes_invalide: bytes = b'\x80\x81\x82'
    
    try:
        text_invalid: str = bytes_invalide.decode('utf-8')
        print(f"Rezultat: {text_invalid}")  # Nu se va executa
    except UnicodeDecodeError as e:
        logger.warning(f"Decoding UTF-8 eșuat: {e}")
        print(f"⚠️  Eroare: {e}")
        print("  → Acești bytes nu reprezintă caractere UTF-8 valide")
    
    # ─────────────────────────────────────────────────────────────────
    # STRATEGII_GESTIONARE_ERORI
    # ─────────────────────────────────────────────────────────────────
    print("\n🛠️  STRATEGII de gestionare erori")
    print("-" * 40)
    
    bytes_mixte: bytes = b'Hello \x80\x81 World'
    
    # HACK: errors='ignore' pierde informație, dar nu dă eroare
    result_ignore: str = bytes_mixte.decode('utf-8', errors='ignore')
    print(f"errors='ignore':  '{result_ignore}'")
    
    # NOTE: errors='replace' e cea mai sigură pentru debugging
    result_replace: str = bytes_mixte.decode('utf-8', errors='replace')
    print(f"errors='replace': '{result_replace}'")
    
    # Strategia 3: backslashreplace — afișează codul escape
    result_backslash: str = bytes_mixte.decode('utf-8', errors='backslashreplace')
    print(f"errors='backslashreplace': '{result_backslash}'")
    
    print("\n💡 RECOMANDARE: Folosește errors='replace' pentru debugging")


# ═══════════════════════════════════════════════════════════════════════════════
# EXEMPLU_FISIER_BINAR
# ═══════════════════════════════════════════════════════════════════════════════
def exemplu_fisier_binar() -> None:
    """Demonstrează citirea/scrierea binară cu context managers.
    
    Arată cum să lucrezi cu fișiere binare pentru:
    - Salvarea datelor de rețea (ex: capturi de pachete)
    - Citirea fișierelor binare existente
    - Diferența între modurile 'w'/'r' și 'wb'/'rb'
    
    Returns:
        None. Creează și șterge un fișier temporar.
        
    Example:
        >>> exemplu_fisier_binar()
        Scris 4 bytes în fișier
        Citit: 45000028
    """
    import os
    import tempfile
    
    print("\n" + "=" * 60)
    print("DEMONSTRAȚIE: Fișiere binare cu context managers")
    print("=" * 60)
    
    # NOTE: Simulăm un header IP parțial
    date_test: bytes = b'\x45\x00\x00\x28'  # IPv4, IHL=5, length=40
    
    # HACK: Folosim un fișier temporar pentru a nu polua sistemul
    temp_path: str = os.path.join(tempfile.gettempdir(), 'test_packet.bin')
    
    try:
        # ─────────────────────────────────────────────────────────────
        # SCRIERE_BINARA
        # ─────────────────────────────────────────────────────────────
        print(f"\n📝 Scriere în {temp_path}")
        
        # NOTE: 'wb' = write binary — crucial pentru date de rețea
        with open(temp_path, 'wb') as f:
            bytes_scrisi: int = f.write(date_test)
            print(f"  Scris {bytes_scrisi} bytes")
        # Fișierul se închide automat la ieșirea din 'with'
        
        # ─────────────────────────────────────────────────────────────
        # CITIRE_BINARA
        # ─────────────────────────────────────────────────────────────
        print(f"\n📖 Citire din {temp_path}")
        
        # NOTE: 'rb' = read binary
        with open(temp_path, 'rb') as f:
            citit: bytes = f.read()
            print(f"  Citit: {citit}")
            print(f"  Hex: {citit.hex()}")
            print(f"  Lungime: {len(citit)} bytes")
        
        # ─────────────────────────────────────────────────────────────
        # INTERPRETARE_HEADER
        # ─────────────────────────────────────────────────────────────
        print(f"\n🔍 Interpretare:")
        # NOTE: Primul byte conține versiunea (high nibble) și IHL (low nibble)
        print(f"  Versiune IP: {citit[0] >> 4}")
        print(f"  Header length: {(citit[0] & 0x0F) * 4} bytes")
        
    except IOError as e:
        logger.error(f"Eroare I/O: {e}")
        print(f"❌ Eroare la operația cu fișierul: {e}")
        
    finally:
        # NOTE: Cleanup — ștergem fișierul temporar
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"\n🧹 Cleanup: fișier temporar șters")


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_INTERACTIV
# ═══════════════════════════════════════════════════════════════════════════════
def quiz_bytes_vs_str() -> None:
    """Quiz interactiv pentru verificarea înțelegerii.
    
    Testează cunoștințele despre bytes vs str cu întrebări practice.
    
    Returns:
        None. Afișează quiz-ul interactiv.
    """
    print("\n" + "=" * 60)
    print("🗳️  QUIZ: Bytes vs Strings")
    print("=" * 60)
    
    print("""
🔮 PREDICȚIE: Ce se întâmplă când rulezi acest cod?

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8080))
    s.send("Hello")  # ← Ce se întâmplă aici?

Opțiuni:
  A) Mesajul "Hello" este trimis cu succes
  B) TypeError: a bytes-like object is required, not 'str'
  C) Mesajul este trimis dar corupt
  D) Socket-ul se blochează în așteptare

Răspuns corect: B

Explicație:
  Socket-urile Python 3 acceptă DOAR bytes, nu strings.
  Codul corect: s.send(b"Hello") sau s.send("Hello".encode())
  
  De ce A e greșit: Python 3 a separat strict bytes de str
  De ce C e greșit: Nu se trimite nimic, dă eroare înainte
  De ce D e greșit: Eroarea apare imediat, nu e blocaj
""")


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_HELPER_UTILE
# ═══════════════════════════════════════════════════════════════════════════════
def ensure_bytes(data) -> bytes:
    """Convertește input-ul în bytes, indiferent de tip.
    
    Args:
        data: str, bytes, sau orice obiect cu __str__
        
    Returns:
        bytes: Reprezentarea bytes a input-ului
        
    Example:
        >>> ensure_bytes("Hello")
        b'Hello'
        >>> ensure_bytes(b"Hello")
        b'Hello'
    """
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode('utf-8')
    return str(data).encode('utf-8')


def ensure_str(data) -> str:
    """Convertește input-ul în str, indiferent de tip.
    
    Args:
        data: bytes, str, sau orice obiect
        
    Returns:
        str: Reprezentarea string a input-ului
        
    Example:
        >>> ensure_str(b"Hello")
        'Hello'
        >>> ensure_str("Hello")
        'Hello'
    """
    if isinstance(data, str):
        return data
    if isinstance(data, bytes):
        return data.decode('utf-8', errors='replace')
    return str(data)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        demonstreaza_conversie()
        demonstreaza_erori_encoding()
        exemplu_fisier_binar()
        quiz_bytes_vs_str()
        
        print("\n" + "=" * 60)
        print("✅ Toate demonstrațiile completate cu succes!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n👋 Întrerupt de utilizator")
    except Exception as e:
        logger.exception(f"Eroare neașteptată: {e}")
        print(f"\n❌ Eroare neașteptată: {e}")
