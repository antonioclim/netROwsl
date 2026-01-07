#!/usr/bin/env python3
"""
Client/Server UDP Echo
======================
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Demonstrează comunicarea UDP de bază între client și server.

Utilizare Server:
    python udp_echo.py server --port 9999

Utilizare Client:
    python udp_echo.py client --gazda 10.5.0.20 --port 9999 --mesaj "Test"
"""

import argparse
import socket
import sys
from typing import Optional


# Coduri culori ANSI
class Culori:
    CYAN = '\033[96m'
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    SFARSIT = '\033[0m'


def coloreaza(text: str, culoare: str) -> str:
    """Aplică culoare dacă stdout este un terminal."""
    if sys.stdout.isatty():
        return f"{culoare}{text}{Culori.SFARSIT}"
    return text


def ruleaza_server(port: int, adresa: str = "0.0.0.0"):
    """
    Pornește un server UDP echo.
    
    Args:
        port: Portul pe care să asculte
        adresa: Adresa la care să se lege (implicit: toate interfețele)
    """
    print(coloreaza("═" * 50, Culori.CYAN))
    print(coloreaza("  Server UDP Echo", Culori.CYAN))
    print(coloreaza("═" * 50, Culori.CYAN))
    print()
    
    try:
        # Crează socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Leagă la adresa și port
        sock.bind((adresa, port))
        
        print(f"  Ascult pe {adresa}:{port}")
        print(f"  Apăsați Ctrl+C pentru a opri serverul.")
        print()
        print(coloreaza("─" * 50, Culori.CYAN))
        
        while True:
            # Primește date
            data, addr = sock.recvfrom(4096)
            mesaj = data.decode('utf-8', errors='replace')
            
            print(f"  [{addr[0]}:{addr[1]}] Primit: {mesaj}")
            
            # Trimite înapoi (echo)
            sock.sendto(data, addr)
            print(f"  [{addr[0]}:{addr[1]}] Trimis: {mesaj}")
            
    except KeyboardInterrupt:
        print("\n")
        print(coloreaza("  Server oprit.", Culori.GALBEN))
    except socket.error as e:
        print(coloreaza(f"  Eroare socket: {e}", Culori.ROSU))
        return 1
    finally:
        sock.close()
    
    return 0


def ruleaza_client(
    gazda: str,
    port: int,
    mesaj: str,
    timeout: float = 5.0
) -> Optional[str]:
    """
    Trimite un mesaj UDP și așteaptă răspunsul.
    
    Args:
        gazda: Adresa serverului
        port: Portul serverului
        mesaj: Mesajul de trimis
        timeout: Timeout în secunde
    
    Returns:
        Răspunsul primit sau None dacă a expirat timeout-ul
    """
    print(coloreaza("═" * 50, Culori.CYAN))
    print(coloreaza("  Client UDP Echo", Culori.CYAN))
    print(coloreaza("═" * 50, Culori.CYAN))
    print()
    
    try:
        # Crează socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        
        print(f"  Destinație: {gazda}:{port}")
        print(f"  Mesaj: {mesaj}")
        print()
        
        # Trimite mesajul
        sock.sendto(mesaj.encode('utf-8'), (gazda, port))
        print(coloreaza("  ✓ Mesaj trimis", Culori.VERDE))
        
        # Așteaptă răspunsul
        data, addr = sock.recvfrom(4096)
        raspuns = data.decode('utf-8', errors='replace')
        
        print(coloreaza(f"  ✓ Răspuns primit: {raspuns}", Culori.VERDE))
        print()
        
        return raspuns
        
    except socket.timeout:
        print(coloreaza("  ✗ Timeout - serverul nu a răspuns", Culori.ROSU))
        return None
    except socket.error as e:
        print(coloreaza(f"  ✗ Eroare socket: {e}", Culori.ROSU))
        return None
    finally:
        sock.close()


def ruleaza_client_interactiv(gazda: str, port: int):
    """
    Rulează clientul în mod interactiv.
    
    Args:
        gazda: Adresa serverului
        port: Portul serverului
    """
    print(coloreaza("═" * 50, Culori.CYAN))
    print(coloreaza("  Client UDP Interactiv", Culori.CYAN))
    print(coloreaza("═" * 50, Culori.CYAN))
    print()
    print(f"  Server: {gazda}:{port}")
    print(f"  Tastați mesajul și apăsați Enter pentru a trimite.")
    print(f"  Tastați 'iesire' sau Ctrl+C pentru a ieși.")
    print()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5.0)
        
        while True:
            try:
                mesaj = input(coloreaza("  > ", Culori.GALBEN))
            except EOFError:
                break
            
            if mesaj.lower() in ('iesire', 'exit', 'quit'):
                break
            
            if not mesaj:
                continue
            
            try:
                sock.sendto(mesaj.encode('utf-8'), (gazda, port))
                data, addr = sock.recvfrom(4096)
                raspuns = data.decode('utf-8', errors='replace')
                print(coloreaza(f"  < {raspuns}", Culori.VERDE))
            except socket.timeout:
                print(coloreaza("  ! Timeout", Culori.ROSU))
            except socket.error as e:
                print(coloreaza(f"  ! Eroare: {e}", Culori.ROSU))
        
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        print("\n  La revedere!")


def main():
    parser = argparse.ArgumentParser(
        description="Client/Server UDP Echo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  %(prog)s server --port 9999              Pornește serverul pe portul 9999
  %(prog)s client -g 10.5.0.20 -p 9999 -m "Test"  Trimite un mesaj
  %(prog)s client -g 10.5.0.20 -p 9999 --interactiv  Mod interactiv
"""
    )
    
    subparsers = parser.add_subparsers(dest="mod", required=True)
    
    # Subcomanda server
    p_server = subparsers.add_parser("server", help="Pornește serverul UDP echo")
    p_server.add_argument(
        "--port", "-p",
        type=int,
        default=9999,
        help="Portul de ascultare (implicit: 9999)"
    )
    p_server.add_argument(
        "--adresa", "-a",
        default="0.0.0.0",
        help="Adresa de legare (implicit: 0.0.0.0)"
    )
    
    # Subcomanda client
    p_client = subparsers.add_parser("client", help="Rulează clientul UDP")
    p_client.add_argument(
        "--gazda", "-g",
        required=True,
        help="Adresa serverului"
    )
    p_client.add_argument(
        "--port", "-p",
        type=int,
        default=9999,
        help="Portul serverului (implicit: 9999)"
    )
    p_client.add_argument(
        "--mesaj", "-m",
        help="Mesajul de trimis (omiteți pentru mod interactiv)"
    )
    p_client.add_argument(
        "--interactiv", "-i",
        action="store_true",
        help="Mod interactiv"
    )
    p_client.add_argument(
        "--timeout", "-t",
        type=float,
        default=5.0,
        help="Timeout în secunde (implicit: 5.0)"
    )
    
    args = parser.parse_args()
    
    if args.mod == "server":
        return ruleaza_server(args.port, args.adresa)
    elif args.mod == "client":
        if args.interactiv or not args.mesaj:
            ruleaza_client_interactiv(args.gazda, args.port)
            return 0
        else:
            raspuns = ruleaza_client(args.gazda, args.port, args.mesaj, args.timeout)
            return 0 if raspuns else 1


if __name__ == "__main__":
    sys.exit(main())
