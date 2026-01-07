#!/usr/bin/env python3
"""
Teste pentru Exercițiile de Laborator
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest script verifică implementările protocoalelor.
"""

import socket
import struct
import binascii
import sys
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului la path
RADACINA = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA))


def verifica_port(port: int, timeout: float = 2.0) -> bool:
    """Verifică dacă un port este activ."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex(('localhost', port)) == 0
    except:
        return False


def test_exercitiu_1():
    """Test: Protocol TEXT."""
    print("\n" + "=" * 50)
    print("EXERCIȚIU 1: Protocol TEXT")
    print("=" * 50)
    
    if not verifica_port(5400):
        print("❌ Serverul TEXT nu rulează pe port 5400")
        return False
    
    teste_reusit = 0
    teste_total = 4
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 5400))
        sock.settimeout(5)
        
        # Test PING
        print("\n1. Test PING...")
        sock.sendall(b'4 PING')
        raspuns = sock.recv(1024).decode()
        if 'PONG' in raspuns:
            print("   ✅ PING/PONG funcționează")
            teste_reusit += 1
        else:
            print(f"   ❌ Răspuns neașteptat: {raspuns}")
        
        # Test SET
        print("\n2. Test SET...")
        sock.sendall(b'15 SET test valoare')
        raspuns = sock.recv(1024).decode()
        if 'OK' in raspuns:
            print("   ✅ SET funcționează")
            teste_reusit += 1
        else:
            print(f"   ❌ Răspuns neașteptat: {raspuns}")
        
        # Test GET
        print("\n3. Test GET...")
        sock.sendall(b'8 GET test')
        raspuns = sock.recv(1024).decode()
        if 'valoare' in raspuns:
            print("   ✅ GET funcționează")
            teste_reusit += 1
        else:
            print(f"   ❌ Răspuns neașteptat: {raspuns}")
        
        # Test DEL
        print("\n4. Test DEL...")
        sock.sendall(b'8 DEL test')
        raspuns = sock.recv(1024).decode()
        if 'OK' in raspuns:
            print("   ✅ DEL funcționează")
            teste_reusit += 1
        else:
            print(f"   ❌ Răspuns neașteptat: {raspuns}")
        
        sock.close()
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        return False
    
    print(f"\nRezultat: {teste_reusit}/{teste_total} teste reușite")
    return teste_reusit == teste_total


def test_exercitiu_2():
    """Test: Protocol BINAR."""
    print("\n" + "=" * 50)
    print("EXERCIȚIU 2: Protocol BINAR")
    print("=" * 50)
    
    if not verifica_port(5401):
        print("❌ Serverul BINAR nu rulează pe port 5401")
        return False
    
    teste_reusit = 0
    teste_total = 2
    
    def construieste_mesaj(tip, payload, secventa):
        magic = b'NP'
        versiune = 1
        lungime = len(payload)
        antet = struct.pack('!2sBBHI', magic, versiune, tip, lungime, secventa)
        crc = binascii.crc32(antet + payload) & 0xFFFFFFFF
        return struct.pack('!2sBBHII', magic, versiune, tip, lungime, secventa, crc) + payload
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 5401))
        sock.settimeout(5)
        
        # Test PING
        print("\n1. Test PING binar...")
        mesaj = construieste_mesaj(0x01, b'', 1)
        sock.sendall(mesaj)
        raspuns = sock.recv(1024)
        
        if len(raspuns) >= 14:
            _, _, tip, _, _, _ = struct.unpack('!2sBBHII', raspuns[:14])
            if tip == 0x02:
                print("   ✅ PING/PONG binar funcționează")
                teste_reusit += 1
            else:
                print(f"   ❌ Tip răspuns neașteptat: 0x{tip:02X}")
        else:
            print("   ❌ Răspuns prea scurt")
        
        # Test CRC invalid
        print("\n2. Test detectare CRC invalid...")
        mesaj_corupt = bytearray(construieste_mesaj(0x01, b'', 2))
        mesaj_corupt[-1] ^= 0xFF  # Corupem CRC
        sock.sendall(bytes(mesaj_corupt))
        raspuns = sock.recv(1024)
        
        if len(raspuns) >= 14:
            _, _, tip, _, _, _ = struct.unpack('!2sBBHII', raspuns[:14])
            if tip == 0xFF:  # ERROR
                print("   ✅ Serverul detectează CRC invalid")
                teste_reusit += 1
            else:
                print(f"   ⚠️  Tip răspuns: 0x{tip:02X} (așteptat ERROR)")
        
        sock.close()
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        return False
    
    print(f"\nRezultat: {teste_reusit}/{teste_total} teste reușite")
    return teste_reusit == teste_total


def test_exercitiu_3():
    """Test: Protocol Senzor UDP."""
    print("\n" + "=" * 50)
    print("EXERCIȚIU 3: Protocol Senzor UDP")
    print("=" * 50)
    
    teste_reusit = 0
    teste_total = 2
    
    def construieste_datagrama(sensor_id, temp, locatie):
        versiune = 1
        locatie_bytes = locatie.encode()[:10].ljust(10, b'\x00')
        date = struct.pack('!BHf', versiune, sensor_id, temp) + locatie_bytes
        crc = binascii.crc32(date) & 0xFFFFFFFF
        return date + struct.pack('!I', crc) + b'\x00\x00'
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Test trimitere datagramă validă
        print("\n1. Test trimitere datagramă validă...")
        datagrama = construieste_datagrama(1, 23.5, "TestLab")
        
        if len(datagrama) == 23:
            sock.sendto(datagrama, ('localhost', 5402))
            print("   ✅ Datagramă de 23 octeți trimisă")
            teste_reusit += 1
        else:
            print(f"   ❌ Dimensiune greșită: {len(datagrama)}")
        
        # Test structură datagramă
        print("\n2. Verificare structură datagramă...")
        versiune = datagrama[0]
        sensor_id = struct.unpack('!H', datagrama[1:3])[0]
        temp = struct.unpack('!f', datagrama[3:7])[0]
        
        if versiune == 1 and sensor_id == 1 and abs(temp - 23.5) < 0.01:
            print("   ✅ Structura datagramei corectă")
            teste_reusit += 1
        else:
            print("   ❌ Structură invalidă")
        
        sock.close()
        
    except Exception as e:
        print(f"❌ Eroare: {e}")
        return False
    
    print(f"\nRezultat: {teste_reusit}/{teste_total} teste reușite")
    return teste_reusit == teste_total


def test_exercitiu_4():
    """Test: Detectare Erori CRC32."""
    print("\n" + "=" * 50)
    print("EXERCIȚIU 4: Detectare Erori CRC32")
    print("=" * 50)
    
    teste_reusit = 0
    teste_total = 3
    
    # Test 1: CRC consistent
    print("\n1. Test consistență CRC32...")
    date = b"Test detectare erori"
    crc1 = binascii.crc32(date) & 0xFFFFFFFF
    crc2 = binascii.crc32(date) & 0xFFFFFFFF
    
    if crc1 == crc2:
        print(f"   ✅ CRC consistent: 0x{crc1:08X}")
        teste_reusit += 1
    else:
        print("   ❌ CRC inconsistent")
    
    # Test 2: Detectare modificare
    print("\n2. Test detectare modificare bit...")
    date_originale = b"Date de test pentru CRC"
    crc_original = binascii.crc32(date_originale) & 0xFFFFFFFF
    
    date_modificate = bytearray(date_originale)
    date_modificate[5] ^= 0x01
    crc_modificat = binascii.crc32(bytes(date_modificate)) & 0xFFFFFFFF
    
    if crc_original != crc_modificat:
        print(f"   ✅ Modificare detectată")
        print(f"      Original:  0x{crc_original:08X}")
        print(f"      Modificat: 0x{crc_modificat:08X}")
        teste_reusit += 1
    else:
        print("   ❌ Modificare nedetectată")
    
    # Test 3: Valoare cunoscută
    print("\n3. Test valoare CRC cunoscută...")
    date_test = b"123456789"
    crc_calculat = binascii.crc32(date_test) & 0xFFFFFFFF
    crc_asteptat = 0xCBF43926  # Valoare standard
    
    if crc_calculat == crc_asteptat:
        print(f"   ✅ CRC corect: 0x{crc_calculat:08X}")
        teste_reusit += 1
    else:
        print(f"   ❌ CRC incorect: 0x{crc_calculat:08X} (așteptat 0x{crc_asteptat:08X})")
    
    print(f"\nRezultat: {teste_reusit}/{teste_total} teste reușite")
    return teste_reusit == teste_total


def main():
    parser = argparse.ArgumentParser(description="Teste Exerciții Laborator")
    parser.add_argument("--exercise", "-e", type=int, choices=[1, 2, 3, 4],
                        help="Numărul exercițiului de testat")
    parser.add_argument("--all", "-a", action="store_true",
                        help="Rulează toate testele")
    args = parser.parse_args()
    
    print("=" * 60)
    print("TESTE EXERCIȚII - LABORATOR SĂPTĂMÂNA 4")
    print("=" * 60)
    
    rezultate = {}
    
    if args.all or args.exercise == 1:
        rezultate[1] = test_exercitiu_1()
    
    if args.all or args.exercise == 2:
        rezultate[2] = test_exercitiu_2()
    
    if args.all or args.exercise == 3:
        rezultate[3] = test_exercitiu_3()
    
    if args.all or args.exercise == 4:
        rezultate[4] = test_exercitiu_4()
    
    if not rezultate:
        parser.print_help()
        return
    
    # Sumar
    print("\n" + "=" * 60)
    print("SUMAR REZULTATE")
    print("=" * 60)
    
    for ex, reusit in rezultate.items():
        status = "✅ REUȘIT" if reusit else "❌ EȘUAT"
        print(f"Exercițiul {ex}: {status}")
    
    total_reusit = sum(rezultate.values())
    total = len(rezultate)
    print(f"\nTotal: {total_reusit}/{total} exerciții completate")


if __name__ == "__main__":
    main()
