#!/usr/bin/env python3
"""
Exercițiul 3: Client Senzor UDP
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Obiectiv: Implementați un client UDP pentru trimiterea datelor de la senzori.

Structura datagramei (23 octeți):
┌──────────┬─────────┬─────────────┬─────────┬───────┬──────────┐
│ Versiune │ ID Senz │ Temperatură │ Locație │ CRC32 │ Rezervat │
│ 1 octet  │ 2 oct   │ 4 oct (flt) │ 10 oct  │ 4 oct │ 2 oct    │
└──────────┴─────────┴─────────────┴─────────┴───────┴──────────┘

Caracteristici:
- Dimensiune fixă: 23 octeți
- Verificare integritate: CRC32
- Transport: UDP (fără conexiune)

Sarcini:
1. Completați funcția construieste_datagrama()
2. Completați funcția verifica_datagrama()
3. Implementați funcția trimite_citire()
4. Implementați simularea mai multor senzori
"""

import socket
import struct
import binascii
import time
import random

# Constante
HOST = 'localhost'
PORT = 5402
VERSIUNE = 1
DIMENSIUNE_DATAGRAMA = 23


def calculeaza_crc(date: bytes) -> int:
    """
    Calculează CRC32 pentru date.
    
    Args:
        date: Datele pentru care se calculează CRC
    
    Returns:
        Valoarea CRC32 (întreg pozitiv pe 32 de biți)
    """
    return binascii.crc32(date) & 0xFFFFFFFF


def construieste_datagrama(sensor_id: int, temperatura: float, locatie: str) -> bytes:
    """
    Construiește o datagramă de senzor de 23 de octeți.
    
    SARCINA 1: Completați această funcție
    
    Args:
        sensor_id: ID-ul senzorului (0-65535)
        temperatura: Valoarea temperaturii (float)
        locatie: Numele locației (max 10 caractere)
    
    Returns:
        Datagramă de exact 23 de octeți
    
    Structura:
    - Octet 0: Versiune (1)
    - Octeți 1-2: ID Senzor (big-endian, unsigned short)
    - Octeți 3-6: Temperatură (big-endian, float)
    - Octeți 7-16: Locație (10 caractere, padding cu null)
    - Octeți 17-20: CRC32 (peste octeții 0-16)
    - Octeți 21-22: Rezervat (zerouri)
    
    Indicii:
    - Folosiți struct.pack('!BHf', versiune, sensor_id, temperatura)
    - Locația trebuie să aibă exact 10 octeți (padding cu b'\\x00')
    - CRC se calculează peste primii 17 octeți (fără CRC și rezervat)
    """
    # TODO: Implementați construirea datagramei
    
    # Pas 1: Pregătiți locația (10 octeți)
    # locatie_bytes = ...
    
    # Pas 2: Construiți partea fără CRC (17 octeți)
    # date_fara_crc = struct.pack('!BHf', ...) + locatie_bytes
    
    # Pas 3: Calculați CRC
    # crc = calculeaza_crc(date_fara_crc)
    
    # Pas 4: Asamblați datagrama completă
    # datagrama = date_fara_crc + struct.pack('!I', crc) + b'\\x00\\x00'
    
    pass  # Înlocuiți cu implementarea dvs.


def verifica_datagrama(date: bytes) -> dict:
    """
    Verifică și parsează o datagramă de senzor.
    
    SARCINA 2: Completați această funcție
    
    Args:
        date: Datagrama primită (ar trebui să aibă 23 de octeți)
    
    Returns:
        Dicționar cu:
        {
            'valid': bool,           # True dacă dimensiunea e corectă
            'versiune': int,
            'sensor_id': int,
            'temperatura': float,
            'locatie': str,
            'crc': int,
            'crc_valid': bool        # True dacă CRC se potrivește
        }
        sau None dacă datagrama e invalidă
    
    Indicii:
    - Verificați mai întâi dimensiunea (trebuie să fie exact 23)
    - Folosiți struct.unpack() pentru a extrage câmpurile
    - Recalculați CRC și comparați cu cel primit
    """
    # TODO: Implementați verificarea datagramei
    
    pass  # Înlocuiți cu implementarea dvs.


def trimite_citire(sensor_id: int, temperatura: float, locatie: str,
                   host: str = HOST, port: int = PORT) -> bool:
    """
    Trimite o citire de senzor prin UDP.
    
    SARCINA 3: Completați această funcție
    
    Args:
        sensor_id: ID-ul senzorului
        temperatura: Valoarea temperaturii
        locatie: Locația senzorului
        host: Adresa serverului
        port: Portul serverului
    
    Returns:
        True dacă trimiterea a reușit
    
    Indicii:
    - Creați un socket UDP: socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    - Folosiți sock.sendto(datagrama, (host, port))
    - UDP nu garantează livrarea, deci nu așteptăm răspuns
    """
    # TODO: Implementați trimiterea citirii
    
    pass  # Înlocuiți cu implementarea dvs.


def simuleaza_senzori(numar_senzori: int, numar_citiri: int, interval: float = 1.0):
    """
    Simulează mai mulți senzori care trimit citiri.
    
    SARCINA 4: Completați această funcție
    
    Args:
        numar_senzori: Câți senzori să simuleze
        numar_citiri: Câte citiri per senzor
        interval: Pauza între citiri (secunde)
    
    Indicii:
    - Creați o listă de locații (ex: "Lab1", "Lab2", "Hol", etc.)
    - Pentru fiecare citire:
      - Alegeți un senzor aleatoriu
      - Generați o temperatură realistă (ex: 18-28°C cu variație mică)
      - Trimiteți citirea
    - Afișați progresul
    """
    # TODO: Implementați simularea
    
    # Locații posibile
    locatii = ["Lab1", "Lab2", "Hol", "Birou", "Sala", "Depozit"]
    
    print(f"Simulare {numar_senzori} senzori, {numar_citiri} citiri fiecare")
    print("-" * 50)
    
    # TODO: Implementați logica de simulare
    
    pass  # Înlocuiți cu implementarea dvs.


def main():
    """Funcția principală pentru testare."""
    print("=" * 50)
    print("Exercițiul 3: Client Senzor UDP")
    print("=" * 50)
    
    # Test 1: Construire datagramă
    print("\n1. Test construire datagramă...")
    datagrama = construieste_datagrama(1, 23.5, "TestLab")
    
    if datagrama is None:
        print("   ⚠️  Funcția construieste_datagrama() nu este implementată")
    elif len(datagrama) != DIMENSIUNE_DATAGRAMA:
        print(f"   ❌ Dimensiune greșită: {len(datagrama)} (așteptat {DIMENSIUNE_DATAGRAMA})")
    else:
        print(f"   ✅ Datagramă construită: {len(datagrama)} octeți")
        print(f"   Hex: {datagrama.hex()}")
    
    # Test 2: Verificare datagramă
    print("\n2. Test verificare datagramă...")
    if datagrama:
        rezultat = verifica_datagrama(datagrama)
        
        if rezultat is None:
            print("   ⚠️  Funcția verifica_datagrama() nu este implementată")
        else:
            print(f"   Versiune: {rezultat.get('versiune')}")
            print(f"   Senzor ID: {rezultat.get('sensor_id')}")
            print(f"   Temperatură: {rezultat.get('temperatura')}°C")
            print(f"   Locație: {rezultat.get('locatie')}")
            print(f"   CRC Valid: {'✅' if rezultat.get('crc_valid') else '❌'}")
    
    # Test 3: Trimitere citire
    print("\n3. Test trimitere citire...")
    succes = trimite_citire(1, 25.0, "Lab1")
    
    if succes is None:
        print("   ⚠️  Funcția trimite_citire() nu este implementată")
    elif succes:
        print("   ✅ Citire trimisă cu succes!")
        print(f"   (Verificați serverul pe {HOST}:{PORT})")
    else:
        print("   ❌ Trimitere eșuată")
    
    # Test 4: Simulare (doar dacă celelalte funcții sunt implementate)
    print("\n4. Test simulare...")
    if datagrama and succes:
        print("   Pornire simulare cu 3 senzori, 5 citiri...")
        simuleaza_senzori(3, 5, interval=0.5)
    else:
        print("   ⚠️  Completați mai întâi funcțiile anterioare")


if __name__ == "__main__":
    main()
