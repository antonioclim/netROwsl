#!/usr/bin/env python3
"""
Client Senzor UDP
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Client pentru trimiterea datelor de senzor prin UDP.
Port implicit: 5402
"""

import socket
import struct
import binascii
import argparse
import time
import random
import sys

# Configurație
HOST = 'localhost'
PORT = 5402
DIMENSIUNE_DATAGRAMA = 23
VERSIUNE = 1


def calculeaza_crc(date: bytes) -> int:
    """Calculează CRC32 pentru date."""
    return binascii.crc32(date) & 0xFFFFFFFF


def construieste_datagrama(sensor_id: int, temperatura: float, locatie: str) -> bytes:
    """
    Construiește o datagramă de senzor de 23 de octeți.
    
    Structura:
    - Versiune: 1 octet
    - ID Senzor: 2 octeți
    - Temperatură: 4 octeți (float)
    - Locație: 10 octeți
    - CRC32: 4 octeți
    - Rezervat: 2 octeți
    """
    # Pregătește locația (10 octeți, padding cu null)
    locatie_bytes = locatie.encode('utf-8')[:10].ljust(10, b'\x00')
    
    # Construiește datele fără CRC
    date_fara_crc = struct.pack('!BHf', VERSIUNE, sensor_id, temperatura) + locatie_bytes
    
    # Calculează CRC
    crc = calculeaza_crc(date_fara_crc)
    
    # Adaugă CRC și bytes rezervați
    rezervat = b'\x00\x00'
    datagrama = date_fara_crc + struct.pack('!I', crc) + rezervat
    
    assert len(datagrama) == DIMENSIUNE_DATAGRAMA, f"Dimensiune greșită: {len(datagrama)}"
    
    return datagrama


def trimite_citire(sensor_id: int, temperatura: float, locatie: str, 
                   host: str = HOST, port: int = PORT):
    """Trimite o citire de senzor."""
    datagrama = construieste_datagrama(sensor_id, temperatura, locatie)
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(datagrama, (host, port))
    
    return True


def simulare_senzor(sensor_id: int, locatie: str, temp_baza: float = 22.0,
                    interval: float = 1.0, numar_citiri: int = 10):
    """Simulează un senzor care trimite citiri periodice."""
    print(f"Simulare senzor #{sensor_id} în '{locatie}'")
    print(f"Temperatură bază: {temp_baza}°C, Interval: {interval}s")
    print(f"Se vor trimite {numar_citiri} citiri...")
    print()
    
    for i in range(numar_citiri):
        # Variație aleatorie a temperaturii
        variatie = random.uniform(-1.5, 1.5)
        temperatura = temp_baza + variatie
        
        try:
            trimite_citire(sensor_id, temperatura, locatie)
            print(f"  [{i+1}/{numar_citiri}] Trimis: {temperatura:.2f}°C")
        except Exception as e:
            print(f"  [{i+1}/{numar_citiri}] Eroare: {e}")
        
        if i < numar_citiri - 1:
            time.sleep(interval)
    
    print("\nSimulare completă!")


def mod_interactiv():
    """Mod interactiv pentru trimiterea citirilor."""
    print("=" * 50)
    print("Client Senzor UDP - Mod Interactiv")
    print("=" * 50)
    print()
    print("Comenzi:")
    print("  send <id> <temp> <locatie>  - Trimite o citire")
    print("  sim <id> <locatie> [n]      - Simulare (n citiri)")
    print("  quit                        - Ieșire")
    print()
    
    while True:
        try:
            linie = input(">>> ").strip()
            if not linie:
                continue
            
            parti = linie.split()
            cmd = parti[0].lower()
            
            if cmd == "quit" or cmd == "exit":
                break
            
            elif cmd == "send":
                if len(parti) < 4:
                    print("Utilizare: send <id> <temp> <locatie>")
                    continue
                
                sensor_id = int(parti[1])
                temperatura = float(parti[2])
                locatie = ' '.join(parti[3:])
                
                trimite_citire(sensor_id, temperatura, locatie)
                print(f"Trimis: Senzor #{sensor_id}, {temperatura}°C, '{locatie}'")
            
            elif cmd == "sim":
                if len(parti) < 3:
                    print("Utilizare: sim <id> <locatie> [numar_citiri]")
                    continue
                
                sensor_id = int(parti[1])
                locatie = parti[2]
                numar = int(parti[3]) if len(parti) > 3 else 5
                
                simulare_senzor(sensor_id, locatie, numar_citiri=numar)
            
            else:
                print(f"Comandă necunoscută: {cmd}")
                
        except ValueError as e:
            print(f"Eroare de format: {e}")
        except KeyboardInterrupt:
            print("\nÎntrerupt")
            break
        except EOFError:
            break


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Client Senzor UDP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python udp_sensor_client.py --sensor-id 1 --temp 23.5 --location "Lab1"
  python udp_sensor_client.py --simulate --sensor-id 1 --location "Lab1" --count 10
  python udp_sensor_client.py --interactive
        """
    )
    parser.add_argument("--host", default=HOST, help=f"Adresa serverului (implicit: {HOST})")
    parser.add_argument("--port", type=int, default=PORT, help=f"Portul serverului (implicit: {PORT})")
    parser.add_argument("--sensor-id", type=int, help="ID-ul senzorului")
    parser.add_argument("--temp", type=float, help="Temperatura de trimis")
    parser.add_argument("--location", help="Locația senzorului")
    parser.add_argument("--simulate", action="store_true", help="Rulează simulare")
    parser.add_argument("--count", type=int, default=10, help="Număr citiri în simulare")
    parser.add_argument("--interval", type=float, default=1.0, help="Interval între citiri (secunde)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Mod interactiv")
    
    args = parser.parse_args()
    
    if args.interactive:
        mod_interactiv()
    elif args.simulate:
        if not args.sensor_id or not args.location:
            print("Eroare: --sensor-id și --location sunt necesare pentru simulare")
            sys.exit(1)
        simulare_senzor(
            args.sensor_id, 
            args.location,
            interval=args.interval,
            numar_citiri=args.count
        )
    elif args.sensor_id and args.temp and args.location:
        trimite_citire(args.sensor_id, args.temp, args.location, args.host, args.port)
        print(f"Citire trimisă: Senzor #{args.sensor_id}, {args.temp}°C, '{args.location}'")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
