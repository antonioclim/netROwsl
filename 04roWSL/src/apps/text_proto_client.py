#!/usr/bin/env python3
"""
Client Protocol TEXT
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Client interactiv pentru protocolul TEXT.
Format mesaj: <LUNGIME> <CONȚINUT>
Port implicit: 5400
"""

import socket
import sys

# Configurație
HOST = 'localhost'
PORT = 5400
TIMEOUT = 10.0


def formateaza_mesaj(continut: str) -> bytes:
    """Formatează un mesaj în format protocol TEXT."""
    lungime = len(continut)
    return f"{lungime} {continut}".encode('utf-8')


def parseaza_raspuns(date: bytes) -> str:
    """Parsează un răspuns din format protocol TEXT."""
    text = date.decode('utf-8')
    spatiu_idx = text.find(' ')
    if spatiu_idx == -1:
        return text
    lungime = int(text[:spatiu_idx])
    return text[spatiu_idx + 1:spatiu_idx + 1 + lungime]


def trimite_comanda(sock: socket.socket, comanda: str) -> str:
    """Trimite o comandă și primește răspunsul."""
    mesaj = formateaza_mesaj(comanda)
    sock.sendall(mesaj)
    
    raspuns = sock.recv(4096)
    return parseaza_raspuns(raspuns)


def mod_interactiv():
    """Rulează clientul în mod interactiv."""
    print("=" * 50)
    print("Client Protocol TEXT")
    print("=" * 50)
    print(f"Conectare la {HOST}:{PORT}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((HOST, PORT))
        print("Conectat cu succes!")
        print()
        print("Comenzi disponibile:")
        print("  PING              - Test conectivitate")
        print("  SET <cheie> <val> - Setare valoare")
        print("  GET <cheie>       - Citire valoare")
        print("  DEL <cheie>       - Ștergere cheie")
        print("  COUNT             - Numărare chei")
        print("  KEYS              - Listare chei")
        print("  QUIT              - Ieșire")
        print()
        
        while True:
            try:
                comanda = input(">>> ").strip()
                if not comanda:
                    continue
                
                raspuns = trimite_comanda(sock, comanda)
                print(f"<<< {raspuns}")
                
                if comanda.upper() == "QUIT":
                    break
                    
            except EOFError:
                print("\nÎnchidere...")
                trimite_comanda(sock, "QUIT")
                break
                
    except ConnectionRefusedError:
        print(f"Eroare: Nu se poate conecta la {HOST}:{PORT}")
        print("Asigurați-vă că serverul rulează.")
        sys.exit(1)
    except socket.timeout:
        print("Eroare: Timeout la conexiune")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nÎntrerupt de utilizator")
    finally:
        sock.close()


def mod_non_interactiv(comenzi: list):
    """Execută o listă de comenzi."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((HOST, PORT))
        
        for comanda in comenzi:
            raspuns = trimite_comanda(sock, comanda)
            print(f"{comanda} -> {raspuns}")
            
            if comanda.upper() == "QUIT":
                break
                
    except Exception as e:
        print(f"Eroare: {e}")
        sys.exit(1)
    finally:
        sock.close()


def main():
    """Funcția principală."""
    if len(sys.argv) > 1:
        # Mod non-interactiv cu comenzi din linia de comandă
        comenzi = sys.argv[1:]
        mod_non_interactiv(comenzi)
    else:
        # Mod interactiv
        mod_interactiv()


if __name__ == "__main__":
    main()
