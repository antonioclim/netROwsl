#!/usr/bin/env python3
"""
Exercițiul 11.01: Server Backend HTTP
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Un server HTTP simplu care poate fi folosit ca backend pentru echilibrul de sarcină.
Fiecare instanță are un ID unic pentru a putea fi identificată în răspunsuri.

Utilizare:
    python ex_11_01_backend.py --id 1 --port 8081
    python ex_11_01_backend.py --id 2 --port 8082
    python ex_11_01_backend.py --id 3 --port 8083
"""

import argparse
import socket
import threading
import time
from datetime import datetime
import platform


# Contor global pentru cereri (thread-safe)
contor_cereri = 0
lock_contor = threading.Lock()


def incrementeaza_contor() -> int:
    """Incrementează contorul de cereri și returnează noua valoare."""
    global contor_cereri
    with lock_contor:
        contor_cereri += 1
        return contor_cereri


def genereaza_raspuns(id_backend: int, intarziere: float = 0) -> bytes:
    """
    Generează răspunsul HTTP pentru backend.
    
    Args:
        id_backend: Identificatorul acestui backend
        intarziere: Întârziere opțională în secunde
    
    Returns:
        Răspunsul HTTP complet ca bytes
    """
    if intarziere > 0:
        time.sleep(intarziere)
    
    numar_cerere = incrementeaza_contor()
    timestamp = datetime.now().isoformat(timespec='seconds')
    hostname = platform.node()
    
    # Corpul răspunsului
    body = f"Backend {id_backend} | Gazdă: {hostname} | Timp: {timestamp} | Cerere #{numar_cerere}\n"
    
    # Construiește răspunsul HTTP
    headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/plain; charset=utf-8",
        f"Content-Length: {len(body.encode())}",
        f"X-Backend-ID: {id_backend}",
        f"X-Served-By: backend-{id_backend}",
        "Connection: close",
        "",
        ""
    ]
    
    raspuns = "\r\n".join(headers) + body
    return raspuns.encode()


def gestioneaza_client(sock_client: socket.socket, adresa: tuple, id_backend: int, 
                       intarziere: float, verbose: bool):
    """
    Gestionează o conexiune de la un client.
    
    Args:
        sock_client: Socket-ul clientului
        adresa: Adresa clientului (ip, port)
        id_backend: ID-ul acestui backend
        intarziere: Întârziere de procesare
        verbose: Afișează mesaje detaliate
    """
    try:
        # Primește cererea (nu o procesăm, doar așteptăm)
        sock_client.settimeout(5.0)
        cerere = sock_client.recv(4096)
        
        if not cerere:
            return
        
        # Extrage prima linie a cererii pentru logging
        prima_linie = cerere.decode('utf-8', errors='ignore').split('\r\n')[0]
        
        if verbose:
            print(f"[Backend {id_backend}] {adresa[0]}:{adresa[1]} - {prima_linie}")
        
        # Trimite răspunsul
        raspuns = genereaza_raspuns(id_backend, intarziere)
        sock_client.sendall(raspuns)
        
    except socket.timeout:
        if verbose:
            print(f"[Backend {id_backend}] Timeout pentru {adresa[0]}:{adresa[1]}")
    except Exception as e:
        if verbose:
            print(f"[Backend {id_backend}] Eroare: {e}")
    finally:
        sock_client.close()


def ruleaza_server(id_backend: int, port: int, intarziere: float, verbose: bool):
    """
    Rulează serverul backend.
    
    Args:
        id_backend: Identificatorul unic al acestui backend
        port: Portul pe care să asculte
        intarziere: Întârziere de procesare în secunde
        verbose: Afișează mesaje detaliate
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind(('0.0.0.0', port))
        server.listen(128)
        
        print(f"[Backend {id_backend}] Ascultă pe 0.0.0.0:{port}")
        if intarziere > 0:
            print(f"[Backend {id_backend}] Întârziere configurată: {intarziere}s")
        print(f"[Backend {id_backend}] Apăsați Ctrl+C pentru oprire")
        print()
        
        while True:
            sock_client, adresa = server.accept()
            
            # Gestionează clientul într-un thread separat
            thread = threading.Thread(
                target=gestioneaza_client,
                args=(sock_client, adresa, id_backend, intarziere, verbose)
            )
            thread.daemon = True
            thread.start()
            
    except KeyboardInterrupt:
        print(f"\n[Backend {id_backend}] Oprire...")
    finally:
        server.close()


def main():
    parser = argparse.ArgumentParser(
        description="Server Backend HTTP pentru exercițiile de echilibrare a sarcinii",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python ex_11_01_backend.py --id 1 --port 8081
  python ex_11_01_backend.py --id 2 --port 8082 --delay 0.5
  python ex_11_01_backend.py --id 3 --port 8083 -v
        """
    )
    
    parser.add_argument(
        '--id',
        type=int,
        default=1,
        help='Identificatorul unic al backend-ului (implicit: 1)'
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=8081,
        help='Portul pe care să asculte (implicit: 8081)'
    )
    parser.add_argument(
        '--delay', '--intarziere', '-d',
        type=float,
        default=0.0,
        help='Întârziere de procesare în secunde (implicit: 0)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Afișează mesaje detaliate pentru fiecare cerere'
    )
    
    args = parser.parse_args()
    
    ruleaza_server(args.id, args.port, args.delay, args.verbose)


if __name__ == '__main__':
    main()
