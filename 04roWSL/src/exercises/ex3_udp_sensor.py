#!/usr/bin/env python3
"""
Exercițiu 3: Client Senzor UDP
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Implementați un client care trimite date de senzor prin UDP.

ÎNAINTE DE A ÎNCEPE — Răspunde mental:
======================================
1. Ce tip de socket folosești pentru UDP? (SOCK_STREAM sau SOCK_DGRAM?)
2. Pentru UDP, folosești connect()+send() sau sendto()? De ce?
3. Datagrama senzorului are exact câți bytes? (hint: dimensiune fixă)
4. Dacă serverul nu primește datagrama, clientul știe? De ce da/nu?

Notează răspunsurile și verifică-le după ce termini exercițiul.

INSTRUCȚIUNI:
    1. Completați funcțiile marcate cu TODO
    2. Testați cu serverul din container: localhost:5402
    3. Observați că UDP nu garantează livrarea!

STRUCTURA DATAGRAMEI (23 bytes):
    | Offset | Lungime | Câmp        | Format         |
    |--------|---------|-------------|----------------|
    | 0      | 1       | Versiune    | uint8          |
    | 1-2    | 2       | ID Senzor   | uint16 BE      |
    | 3-6    | 4       | Temperatură | float BE       |
    | 7-16   | 10      | Locație     | ASCII + padding|
    | 17-20  | 4       | CRC32       | uint32 BE      |
    | 21-22  | 2       | Rezervat    | 2x null byte   |

    BE = Big-Endian (Network Byte Order)

PUNCTAJ: 10 puncte
"""

import socket
import struct
import binascii
import time
import random
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL
# Scop: Definește valorile fixe ale protocolului senzor
# Transferabil la: Orice protocol cu datagrame de dimensiune fixă
# ═══════════════════════════════════════════════════════════════════════════════

SENZOR_VERSIUNE = 1
SENZOR_DIMENSIUNE = 23
SENZOR_LUNGIME_LOCATIE = 10

SERVER_HOST = 'localhost'
SERVER_PORT = 5402


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_PROTOCOL
# Scop: Construcția datagramelor senzor
# Transferabil la: Orice protocol IoT cu mesaje de dimensiune fixă
# ═══════════════════════════════════════════════════════════════════════════════

def calculeaza_crc32(date: bytes) -> int:
    """
    Calculează CRC32 pentru date.
    
    Args:
        date: Datele pentru CRC
    
    Returns:
        CRC32 ca întreg pozitiv pe 32 de biți
    """
    return binascii.crc32(date) & 0xFFFFFFFF


def construieste_datagrama(sensor_id: int, temperatura: float, locatie: str) -> bytes:
    """
    Construiește o datagramă de senzor.
    
    PREDICȚIE:
    - Dacă locația are 3 caractere, cu ce umpli restul până la 10?
    - Ce se întâmplă dacă locația are mai mult de 10 caractere?
    - În ce ordine pui bytes-ii pentru float în rețea?
    
    Args:
        sensor_id: ID-ul senzorului (0-65535)
        temperatura: Temperatura măsurată
        locatie: Locația senzorului (max 10 caractere)
    
    Returns:
        Datagrama de 23 de bytes
    """
    # TODO: Implementați construcția datagramei
    # Pași:
    # 1. Pregătește locația (10 bytes, padding cu \x00):
    #    loc_bytes = locatie.encode('utf-8')[:10]
    #    loc_padded = loc_bytes + b'\x00' * (10 - len(loc_bytes))
    #
    # 2. Construiește partea fără CRC (17 bytes):
    #    parte_fara_crc = struct.pack('!BHf', SENZOR_VERSIUNE, sensor_id, temperatura) + loc_padded
    #
    # 3. Calculează CRC32 pentru partea de mai sus
    #
    # 4. Construiește datagrama completă (23 bytes):
    #    datagrama = parte_fara_crc + struct.pack('!I', crc) + b'\x00\x00'
    #
    # 5. Verifică lungimea: assert len(datagrama) == 23
    pass


def afiseaza_datagrama(datagrama: bytes):
    """
    Afișează conținutul unei datagrame în format uman.
    
    Args:
        datagrama: Datagrama de afișat
    """
    if len(datagrama) != SENZOR_DIMENSIUNE:
        print(f"Eroare: lungime invalidă ({len(datagrama)} != {SENZOR_DIMENSIUNE})")
        return
    
    versiune = datagrama[0]
    sensor_id = struct.unpack('!H', datagrama[1:3])[0]
    temperatura = struct.unpack('!f', datagrama[3:7])[0]
    locatie = datagrama[7:17].rstrip(b'\x00').decode('utf-8', errors='replace')
    crc = struct.unpack('!I', datagrama[17:21])[0]
    
    print(f"  Versiune:    {versiune}")
    print(f"  Sensor ID:   {sensor_id}")
    print(f"  Temperatură: {temperatura:.2f}°C")
    print(f"  Locație:     '{locatie}'")
    print(f"  CRC32:       0x{crc:08X}")
    print(f"  Hex complet: {datagrama.hex()}")


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_REȚEA
# Scop: Trimitere datagrame prin UDP
# Transferabil la: Orice comunicare UDP fire-and-forget
# ═══════════════════════════════════════════════════════════════════════════════

def trimite_datagrama(datagrama: bytes) -> bool:
    """
    Trimite o datagramă UDP la server.
    
    PREDICȚIE:
    - UDP necesită connect() înainte de trimitere?
    - Cum știi dacă serverul a primit datagrama?
    - Ce se întâmplă dacă serverul nu există?
    
    Args:
        datagrama: Datagrama de trimis
    
    Returns:
        True dacă trimiterea a reușit (nu garantează recepția!)
    """
    # TODO: Implementați trimiterea UDP
    # Pași:
    # 1. Creează socket UDP: socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. Trimite cu sendto(): sock.sendto(datagrama, (SERVER_HOST, SERVER_PORT))
    # 3. Închide socket-ul
    # 4. Returnează True (nu avem confirmare de la server!)
    pass


def simuleaza_senzor(sensor_id: int, locatie: str, 
                     temp_baza: float = 22.0, variatie: float = 2.0,
                     numar_citiri: int = 5, interval: float = 1.0):
    """
    Simulează un senzor care trimite citiri periodice.
    
    PREDICȚIE:
    - Dacă trimiți 5 datagrame, câte va primi serverul? (hint: UDP!)
    - Ce distribuție statistică e mai realistă pentru temperatură?
    
    Args:
        sensor_id: ID-ul senzorului
        locatie: Locația senzorului
        temp_baza: Temperatura medie
        variatie: Variația maximă (+/-)
        numar_citiri: Numărul de citiri de trimis
        interval: Timpul între citiri (secunde)
    """
    print(f"\nSimulare senzor #{sensor_id} la '{locatie}'")
    print(f"Temperatura bază: {temp_baza}°C ± {variatie}°C")
    print(f"Citiri: {numar_citiri}, interval: {interval}s")
    print("-" * 40)
    
    for i in range(numar_citiri):
        # Generează temperatură cu variație aleatorie
        temperatura = temp_baza + random.uniform(-variatie, variatie)
        
        # Construiește și trimite datagrama
        datagrama = construieste_datagrama(sensor_id, temperatura, locatie)
        
        if datagrama:
            print(f"\nCitirea {i+1}/{numar_citiri}:")
            afiseaza_datagrama(datagrama)
            
            succes = trimite_datagrama(datagrama)
            if succes:
                print("  Status: Trimis (fără confirmare)")
            else:
                print("  Status: EROARE la trimitere")
        
        # Așteaptă înainte de următoarea citire (exceptând ultima)
        if i < numar_citiri - 1:
            time.sleep(interval)


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRAM_PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Demonstrează utilizarea clientului senzor UDP."""
    print("=" * 60)
    print("Client Senzor UDP")
    print("=" * 60)
    
    # Test construcție datagramă
    print("\n1. Test construcție datagramă...")
    datagrama = construieste_datagrama(42, 23.5, "Lab1")
    if datagrama:
        if len(datagrama) == SENZOR_DIMENSIUNE:
            print(f"   ✓ Lungime corectă: {len(datagrama)} bytes")
            afiseaza_datagrama(datagrama)
        else:
            print(f"   ✗ Lungime greșită: {len(datagrama)} (așteptat {SENZOR_DIMENSIUNE})")
    else:
        print("   ✗ Datagrama nu a fost construită!")
        print("   Implementați construieste_datagrama() mai întâi.")
        return
    
    # Test trimitere singulară
    print("\n2. Test trimitere singulară...")
    succes = trimite_datagrama(datagrama)
    if succes:
        print("   ✓ Datagrama trimisă (verificați log-urile serverului)")
        print("   docker logs saptamana4-senzor --tail 10")
    else:
        print("   ✗ Eroare la trimitere!")
        print("   Implementați trimite_datagrama() mai întâi.")
        return
    
    # Simulare senzor
    print("\n3. Simulare senzor cu citiri multiple...")
    simuleaza_senzor(
        sensor_id=1,
        locatie="Laborator",
        temp_baza=22.0,
        variatie=1.5,
        numar_citiri=3,
        interval=0.5
    )
    
    print("\n" + "=" * 60)
    print("Test complet!")
    print("=" * 60)
    
    print("\nPentru a verifica recepția, rulați:")
    print("  docker logs saptamana4-senzor --tail 20")
    
    # Verificare răspunsuri predicție
    print("\n" + "-" * 60)
    print("VERIFICARE PREDICȚII:")
    print("-" * 60)
    print("1. UDP folosește SOCK_DGRAM (TCP ar fi SOCK_STREAM)")
    print("2. Pentru UDP folosești sendto() - nu necesită connect()")
    print("3. Datagrama senzorului are fix 23 bytes")
    print("4. UDP = fire-and-forget, clientul NU știe dacă serverul a primit")


if __name__ == "__main__":
    main()
