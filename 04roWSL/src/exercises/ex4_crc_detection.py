#!/usr/bin/env python3
"""
Exercițiu 4: Detectare Erori cu CRC32
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Înțelegeți și implementați verificarea integrității datelor folosind CRC32.

CRC32 (Cyclic Redundancy Check):
    - Algoritm de detectare a erorilor bazat pe polinoame
    - Generează o valoare de 32 de biți (4 octeți)
    - Detectează 100% erorile de 1-2 biți și rafale ≤32 biți
    - Folosit în Ethernet, ZIP, PNG, etc.

INSTRUCȚIUNI:
    1. Completați funcțiile marcate cu TODO
    2. Testați detectarea diferitelor tipuri de erori
    3. Analizați rezultatele
"""

import binascii
import struct


def calculeaza_crc32(date: bytes) -> int:
    """
    Calculează CRC32 pentru un bloc de date.
    
    Args:
        date: Datele pentru care se calculează CRC
    
    Returns:
        Valoarea CRC32 ca întreg pozitiv pe 32 de biți
    
    Exemplu:
        calculeaza_crc32(b"123456789") -> 0xCBF43926
    """
    # TODO: Implementați calculul CRC32
    # Indiciu: Folosiți binascii.crc32() și mascați rezultatul cu 0xFFFFFFFF
    pass


def verifica_integritate(date: bytes, crc_original: int) -> bool:
    """
    Verifică dacă datele nu au fost modificate.
    
    Args:
        date: Datele de verificat
        crc_original: CRC-ul calculat înainte de transmisie
    
    Returns:
        True dacă datele sunt intacte
    """
    # TODO: Implementați verificarea
    pass


def simuleaza_eroare_bit(date: bytes, pozitie: int) -> bytes:
    """
    Simulează o eroare de un singur bit.
    
    Args:
        date: Datele originale
        pozitie: Poziția bitului de inversat (0 = primul bit)
    
    Returns:
        Datele cu bitul inversat
    """
    # TODO: Implementați simularea erorii
    # Indiciu:
    # 1. Convertiți la bytearray pentru modificare
    # 2. Calculați indexul octetului și bitul din octet
    # 3. Inversați bitul folosind XOR
    pass


def simuleaza_eroare_rafala(date: bytes, start: int, lungime: int) -> bytes:
    """
    Simulează o eroare de rafală (burst error).
    
    O eroare de rafală afectează biți consecutivi.
    
    Args:
        date: Datele originale
        start: Poziția primului bit afectat
        lungime: Numărul de biți afectați
    
    Returns:
        Datele cu eroarea de rafală
    """
    # TODO: Implementați simularea erorii de rafală
    pass


def analizeaza_detectare():
    """
    Analizează capacitatea CRC32 de a detecta diferite tipuri de erori.
    """
    print("=" * 60)
    print("Analiză Detectare Erori cu CRC32")
    print("=" * 60)
    
    # Date de test
    date_originale = b"Mesaj de test pentru analiza CRC32"
    crc_original = calculeaza_crc32(date_originale)
    
    print(f"\nDate originale: {date_originale}")
    print(f"CRC32 original: 0x{crc_original:08X}")
    
    # TODO: Completați analiza
    # 
    # 1. Test eroare bit singur
    # print("\n--- Test: Eroare Bit Singur ---")
    # for pozitie in [0, 7, 15, 100]:
    #     date_eronate = simuleaza_eroare_bit(date_originale, pozitie)
    #     crc_nou = calculeaza_crc32(date_eronate)
    #     detectat = crc_nou != crc_original
    #     print(f"Poziție {pozitie}: Detectat = {detectat}")
    #
    # 2. Test eroare rafală
    # print("\n--- Test: Eroare Rafală ---")
    # for lungime in [1, 8, 16, 32, 33]:
    #     date_eronate = simuleaza_eroare_rafala(date_originale, 0, lungime)
    #     crc_nou = calculeaza_crc32(date_eronate)
    #     detectat = crc_nou != crc_original
    #     print(f"Lungime {lungime}: Detectat = {detectat}")
    #
    # 3. Statistici pentru erori aleatorii
    # print("\n--- Test: Erori Aleatorii ---")
    # ...
    
    print("\nImplementați analiza conform instrucțiunilor!")


def construieste_mesaj_cu_crc(date: bytes) -> bytes:
    """
    Construiește un mesaj cu CRC32 atașat la final.
    
    Args:
        date: Datele mesajului
    
    Returns:
        Mesaj + CRC32 (4 octeți, big-endian)
    """
    # TODO: Implementați construcția mesajului
    # Indiciu: date + struct.pack('!I', crc)
    pass


def verifica_mesaj_cu_crc(mesaj: bytes) -> tuple:
    """
    Verifică un mesaj care conține CRC32 la final.
    
    Args:
        mesaj: Mesajul complet (date + CRC)
    
    Returns:
        Tuple (date, crc_valid)
    """
    # TODO: Implementați verificarea
    # Indiciu:
    # 1. Extrageți datele (tot minus ultimii 4 octeți)
    # 2. Extrageți CRC-ul (ultimii 4 octeți)
    # 3. Verificați dacă CRC-ul se potrivește
    pass


def main():
    """Funcție principală."""
    # Testare funcții de bază
    print("=" * 60)
    print("Exercițiu: Detectare Erori cu CRC32")
    print("=" * 60)
    
    # Test valoare cunoscută
    date_test = b"123456789"
    crc = calculeaza_crc32(date_test)
    print(f"\nTest valoare cunoscută:")
    print(f"  Date: {date_test}")
    print(f"  CRC32 calculat: 0x{crc:08X}")
    print(f"  CRC32 așteptat: 0xCBF43926")
    print(f"  Corect: {crc == 0xCBF43926}")
    
    # Rulare analiză
    analizeaza_detectare()


if __name__ == "__main__":
    main()
