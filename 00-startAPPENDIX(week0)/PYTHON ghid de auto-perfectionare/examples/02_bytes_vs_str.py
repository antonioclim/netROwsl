#!/usr/bin/env python3
"""
Exemplu 2: Diferența dintre bytes și str
========================================
Demonstrează conversia între text și date binare în Python.

Curs: Rețele de Calculatoare - ASE București, CSIE
Autor: ing. dr. Antonio Clim

💡 ANALOGIE: Bytes și Strings ca Scrisori și Telegrame
------------------------------------------------------
- String = scrisoare în română pe care o citești direct
- Bytes = telegramă codificată în Morse — trebuie decodată ca să o înțelegi
- encode() = a traduce scrisoarea în Morse pentru transmisie
- decode() = a traduce Morse-ul înapoi în text lizibil

Rețeaua "vorbește" doar în Morse (bytes). Calculatorul tău "gândește" în text (strings).

Obiective de învățare:
- Înțelegerea diferenței fundamentale între str și bytes
- Folosirea corectă a encode() și decode()
- Gestionarea erorilor de encoding pentru caractere speciale
"""
import logging
from typing import Optional

# Configurare logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


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
    
    # ─────────────────────────────────────────────────────────────
    # PARTEA 1: String-uri (text pentru oameni)
    # ─────────────────────────────────────────────────────────────
    print("\n📝 PARTEA 1: String-uri (str)")
    print("-" * 40)
    
    text: str = "Salut, Rețele!"
    print(f"String: {text}")
    print(f"Tip: {type(text)}")
    print(f"Lungime în caractere: {len(text)}")
    
    # ─────────────────────────────────────────────────────────────
    # PARTEA 2: Conversie la bytes (pentru trimitere pe rețea)
    # ─────────────────────────────────────────────────────────────
    print("\n📦 PARTEA 2: Conversie str → bytes (encode)")
    print("-" * 40)
    
    octeti: bytes = text.encode('utf-8')
    print(f"Bytes: {octeti}")
    print(f"Tip: {type(octeti)}")
    print(f"Lungime în bytes: {len(octeti)}")
    print(f"  → Observă: 14 caractere = 16 bytes (ț și ț au 2 bytes fiecare)")
    
    # ─────────────────────────────────────────────────────────────
    # PARTEA 3: Conversie înapoi la string (decode)
    # ─────────────────────────────────────────────────────────────
    print("\n🔄 PARTEA 3: Conversie bytes → str (decode)")
    print("-" * 40)
    
    text_decodat: str = octeti.decode('utf-8')
    print(f"Decodat: {text_decodat}")
    print(f"Original == Decodat: {text == text_decodat}")
    
    # ─────────────────────────────────────────────────────────────
    # PARTEA 4: Bytes literal (folosit des în networking)
    # ─────────────────────────────────────────────────────────────
    print("\n🌐 PARTEA 4: Bytes literals pentru protocoale")
    print("-" * 40)
    
    http_request: bytes = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
    print(f"HTTP Request (bytes):")
    print(f"  {http_request}")
    print(f"  Lungime: {len(http_request)} bytes")
    
    # ─────────────────────────────────────────────────────────────
    # PARTEA 5: Reprezentarea hexadecimală (adrese IP)
    # ─────────────────────────────────────────────────────────────
    print("\n🔢 PARTEA 5: Reprezentare hexadecimală")
    print("-" * 40)
    
    # 192.168.1.1 în format binar
    ip_bytes: bytes = b'\xC0\xA8\x01\x01'
    print(f"IP 192.168.1.1 ca bytes: {ip_bytes}")
    print(f"Hex: {ip_bytes.hex()}")
    print(f"  → C0 = 192, A8 = 168, 01 = 1, 01 = 1")
    
    # Conversie înapoi
    octeti_ip: list[int] = list(ip_bytes)
    ip_str: str = '.'.join(str(b) for b in octeti_ip)
    print(f"Reconstruit: {ip_str}")


def demonstreaza_erori_encoding() -> None:
    """Demonstrează erorile comune de encoding și cum să le gestionezi.
    
    Arată ce se întâmplă când:
    - Încerci să encodezi caractere românești în ASCII
    - Primești bytes invalide pentru UTF-8
    - Folosești strategii diferite de gestionare a erorilor
    
    Returns:
        None. Afișează output la consolă.
        
    Example:
        >>> demonstreaza_erori_encoding()
        ⚠️  Eroare la encoding ASCII: ...
    """
    print("\n" + "=" * 60)
    print("DEMONSTRAȚIE: Gestionarea erorilor de encoding")
    print("=" * 60)
    
    # ─────────────────────────────────────────────────────────────
    # EROARE 1: Caractere românești în ASCII
    # ─────────────────────────────────────────────────────────────
    print("\n❌ EROARE 1: Encoding ASCII pentru text românesc")
    print("-" * 40)
    
    text_romanesc: str = "Ștefan și Îțî"
    
    try:
        octeti_ascii: bytes = text_romanesc.encode('ascii')
        print(f"Rezultat: {octeti_ascii}")  # Nu se va executa
    except UnicodeEncodeError as e:
        logger.warning(f"Encoding ASCII eșuat: {e}")
        print(f"⚠️  Eroare: {e}")
        print("  → ASCII nu suportă caractere românești (Ș, ț, Î, etc.)")
        print("  → SOLUȚIE: Folosește UTF-8 în loc de ASCII")
    
    # Soluția corectă
    print("\n✅ SOLUȚIE: UTF-8")
    octeti_utf8: bytes = text_romanesc.encode('utf-8')
    print(f"UTF-8: {octeti_utf8}")
    print(f"Decodat corect: {octeti_utf8.decode('utf-8')}")
    
    # ─────────────────────────────────────────────────────────────
    # EROARE 2: Bytes invalide pentru UTF-8
    # ─────────────────────────────────────────────────────────────
    print("\n❌ EROARE 2: Decoding bytes invalide")
    print("-" * 40)
    
    # Bytes care nu sunt UTF-8 valid
    bytes_invalide: bytes = b'\x80\x81\x82'
    
    try:
        text_invalid: str = bytes_invalide.decode('utf-8')
        print(f"Rezultat: {text_invalid}")  # Nu se va executa
    except UnicodeDecodeError as e:
        logger.warning(f"Decoding UTF-8 eșuat: {e}")
        print(f"⚠️  Eroare: {e}")
        print("  → Acești bytes nu reprezintă caractere UTF-8 valide")
    
    # ─────────────────────────────────────────────────────────────
    # STRATEGII DE GESTIONARE A ERORILOR
    # ─────────────────────────────────────────────────────────────
    print("\n🛠️  STRATEGII de gestionare erori")
    print("-" * 40)
    
    bytes_mixte: bytes = b'Hello \x80\x81 World'
    
    # Strategia 1: ignore - omite caracterele invalide
    result_ignore: str = bytes_mixte.decode('utf-8', errors='ignore')
    print(f"errors='ignore':  '{result_ignore}'")
    
    # Strategia 2: replace - înlocuiește cu �
    result_replace: str = bytes_mixte.decode('utf-8', errors='replace')
    print(f"errors='replace': '{result_replace}'")
    
    # Strategia 3: backslashreplace - afișează codul escape
    result_backslash: str = bytes_mixte.decode('utf-8', errors='backslashreplace')
    print(f"errors='backslashreplace': '{result_backslash}'")
    
    print("\n💡 RECOMANDARE: Folosește errors='replace' pentru debugging")


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
    
    # Date de test: un header IP parțial
    date_test: bytes = b'\x45\x00\x00\x28'  # IPv4, IHL=5, length=40
    
    # Folosim un fișier temporar pentru siguranță
    temp_path: str = os.path.join(tempfile.gettempdir(), 'test_packet.bin')
    
    try:
        # ─────────────────────────────────────────────────────────
        # Scriere binară cu context manager
        # ─────────────────────────────────────────────────────────
        print(f"\n📝 Scriere în {temp_path}")
        
        with open(temp_path, 'wb') as f:
            bytes_scrisi: int = f.write(date_test)
            print(f"  Scris {bytes_scrisi} bytes")
        # Fișierul se închide automat la ieșirea din 'with'
        
        # ─────────────────────────────────────────────────────────
        # Citire binară cu context manager
        # ─────────────────────────────────────────────────────────
        print(f"\n📖 Citire din {temp_path}")
        
        with open(temp_path, 'rb') as f:
            citit: bytes = f.read()
            print(f"  Citit: {citit}")
            print(f"  Hex: {citit.hex()}")
            print(f"  Lungime: {len(citit)} bytes")
        
        # Interpretare header
        print(f"\n🔍 Interpretare:")
        print(f"  Versiune IP: {citit[0] >> 4}")
        print(f"  Header length: {(citit[0] & 0x0F) * 4} bytes")
        
    except IOError as e:
        logger.error(f"Eroare I/O: {e}")
        print(f"❌ Eroare la operația cu fișierul: {e}")
        
    finally:
        # Cleanup: ștergem fișierul temporar
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"\n🧹 Cleanup: fișier temporar șters")


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
  Codul corect: s.send("Hello".encode()) sau s.send(b"Hello")
  
  De ce A e greșit: Python 3 a separat strict bytes de str
  De ce C e greșit: Nu se trimite nimic, dă eroare înainte
  De ce D e greșit: Eroarea apare imediat, nu e blocaj
""")


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
