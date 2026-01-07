#!/usr/bin/env python3
"""
Tema 1: Server HTTPS cu TLS
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Implementați un server care suportă atât HTTP cât și HTTPS.

Cerințe:
    1. Generați un certificat auto-semnat
    2. Implementați context SSL/TLS
    3. Rulați server dual-port (HTTP și HTTPS)
    4. Gestionați erorile de conexiune

Generare certificat:
    openssl req -x509 -newkey rsa:4096 \\
        -keyout certs/key.pem \\
        -out certs/cert.pem \\
        -days 365 -nodes \\
        -subj "/CN=localhost"

Utilizare:
    python tema_8_01_server_https.py

Testare:
    curl http://localhost:8080/
    curl -k https://localhost:8443/
"""

import socket
import ssl
import threading
import mimetypes
from pathlib import Path
from typing import Tuple, Optional

# Configurație
PORT_HTTP = 8080
PORT_HTTPS = 8443
GAZDA = "127.0.0.1"
DIMENSIUNE_BUFFER = 4096

# Căi fișiere
RADACINA_PROIECT = Path(__file__).parent.parent.parent
RADACINA_DOCUMENTE = RADACINA_PROIECT / "www"
FISIER_CERTIFICAT = RADACINA_PROIECT / "certs" / "cert.pem"
FISIER_CHEIE = RADACINA_PROIECT / "certs" / "key.pem"


def creeaza_context_ssl() -> Optional[ssl.SSLContext]:
    """
    TODO: Creează și configurează contextul SSL.
    
    Returns:
        Contextul SSL configurat sau None dacă nu se poate crea
    
    Indicii:
    - Folosiți ssl.SSLContext cu ssl.PROTOCOL_TLS_SERVER
    - Setați versiunea minimă la TLS 1.2
    - Încărcați certificatul și cheia
    - Gestionați FileNotFoundError dacă certificatele nu există
    """
    # CODUL DUMNEAVOASTRĂ AICI
    try:
        # Creează context pentru server TLS
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        
        # Setează versiunea minimă
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        
        # Încarcă certificatul și cheia
        context.load_cert_chain(
            certfile=str(FISIER_CERTIFICAT),
            keyfile=str(FISIER_CHEIE)
        )
        
        return context
        
    except FileNotFoundError:
        print("[EROARE] Fișierele de certificat nu au fost găsite!")
        print(f"         Așteptate: {FISIER_CERTIFICAT}")
        print(f"                    {FISIER_CHEIE}")
        print()
        print("Generați certificatul cu comanda:")
        print("  mkdir -p certs")
        print("  openssl req -x509 -newkey rsa:4096 \\")
        print("    -keyout certs/key.pem \\")
        print("    -out certs/cert.pem \\")
        print("    -days 365 -nodes \\")
        print('    -subj "/CN=localhost"')
        return None
    except ssl.SSLError as e:
        print(f"[EROARE] Eroare SSL: {e}")
        return None


def gestioneaza_cerere(date_cerere: bytes) -> Tuple[int, dict, bytes]:
    """
    TODO: Procesează cererea HTTP și returnează răspunsul.
    
    Args:
        date_cerere: Cererea HTTP brută
    
    Returns:
        Tuplu (cod_stare, antete, corp)
    
    Indicii:
    - Parsați linia de cerere pentru a extrage calea
    - Verificați dacă fișierul există
    - Returnați codul de stare și conținutul corespunzător
    """
    # CODUL DUMNEAVOASTRĂ AICI
    try:
        # Decodifică cererea
        text_cerere = date_cerere.decode('utf-8', errors='replace')
        prima_linie = text_cerere.split('\r\n')[0]
        parti = prima_linie.split(' ')
        
        if len(parti) < 2:
            return 400, {}, b"Cerere invalida"
        
        metoda = parti[0]
        cale = parti[1]
        
        if metoda not in ["GET", "HEAD"]:
            return 405, {"Allow": "GET, HEAD"}, b"Metoda nepermisa"
        
        # Rezolvă calea fișierului
        cale_relativa = cale.lstrip('/')
        if not cale_relativa:
            cale_relativa = "index.html"
        
        # Previne traversarea directoarelor
        if '..' in cale_relativa:
            return 403, {}, b"Interzis"
        
        cale_fisier = RADACINA_DOCUMENTE / cale_relativa
        
        if not cale_fisier.exists():
            return 404, {}, b"Nu a fost gasit"
        
        if not cale_fisier.is_file():
            return 403, {}, b"Interzis"
        
        # Citește fișierul
        continut = cale_fisier.read_bytes()
        tip_mime, _ = mimetypes.guess_type(str(cale_fisier))
        if tip_mime is None:
            tip_mime = "application/octet-stream"
        
        antete = {
            "Content-Type": tip_mime,
            "Content-Length": str(len(continut))
        }
        
        if metoda == "HEAD":
            return 200, antete, b""
        
        return 200, antete, continut
        
    except Exception as e:
        return 500, {}, f"Eroare server: {e}".encode()


def construieste_raspuns(cod_stare: int, antete: dict, corp: bytes) -> bytes:
    """Construiește răspunsul HTTP."""
    motive = {
        200: "OK",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error"
    }
    
    motiv = motive.get(cod_stare, "Unknown")
    linie_stare = f"HTTP/1.1 {cod_stare} {motiv}\r\n"
    
    antete["Server"] = "ServerHTTPS-Tema/1.0"
    antete["Connection"] = "close"
    
    linii_antete = ""
    for nume, valoare in antete.items():
        linii_antete += f"{nume}: {valoare}\r\n"
    
    return linie_stare.encode() + linii_antete.encode() + b"\r\n" + corp


def gestioneaza_client(socket_client: socket.socket, adresa: tuple, protocol: str):
    """Gestionează conexiunea unui client."""
    try:
        date_cerere = socket_client.recv(DIMENSIUNE_BUFFER)
        
        if not date_cerere:
            return
        
        cod_stare, antete, corp = gestioneaza_cerere(date_cerere)
        raspuns = construieste_raspuns(cod_stare, antete, corp)
        
        socket_client.sendall(raspuns)
        
        print(f"[{protocol}] {adresa[0]}:{adresa[1]} - {cod_stare}")
        
    except ssl.SSLError as e:
        print(f"[EROARE SSL] {adresa[0]}:{adresa[1]} - {e}")
    except Exception as e:
        print(f"[EROARE] {adresa[0]}:{adresa[1]} - {e}")
    finally:
        socket_client.close()


def porneste_server_http() -> None:
    """
    TODO: Pornește serverul HTTP pe PORT_HTTP.
    
    Indicii:
    - Creați un socket TCP
    - Legați la (GAZDA, PORT_HTTP)
    - Acceptați conexiuni într-o buclă
    - Gestionați fiecare client într-un fir separat
    """
    # CODUL DUMNEAVOASTRĂ AICI
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    socket_server.bind((GAZDA, PORT_HTTP))
    socket_server.listen(100)
    
    print(f"[HTTP] Server pornit pe http://{GAZDA}:{PORT_HTTP}/")
    
    while True:
        try:
            socket_client, adresa = socket_server.accept()
            fir = threading.Thread(
                target=gestioneaza_client,
                args=(socket_client, adresa, "HTTP")
            )
            fir.start()
        except Exception as e:
            print(f"[EROARE HTTP] {e}")


def porneste_server_https(context: ssl.SSLContext) -> None:
    """
    TODO: Pornește serverul HTTPS pe PORT_HTTPS.
    
    Args:
        context: Contextul SSL configurat
    
    Indicii:
    - Similar cu serverul HTTP
    - Folosiți context.wrap_socket() pentru a împacheta socket-ul
    - Setați server_side=True
    """
    # CODUL DUMNEAVOASTRĂ AICI
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    socket_server.bind((GAZDA, PORT_HTTPS))
    socket_server.listen(100)
    
    print(f"[HTTPS] Server pornit pe https://{GAZDA}:{PORT_HTTPS}/")
    
    while True:
        try:
            socket_client, adresa = socket_server.accept()
            
            # Împachetează socket-ul cu TLS
            try:
                socket_ssl = context.wrap_socket(
                    socket_client,
                    server_side=True
                )
                
                fir = threading.Thread(
                    target=gestioneaza_client,
                    args=(socket_ssl, adresa, "HTTPS")
                )
                fir.start()
                
            except ssl.SSLError as e:
                print(f"[EROARE SSL] Handshake eșuat: {e}")
                socket_client.close()
                
        except Exception as e:
            print(f"[EROARE HTTPS] {e}")


def main():
    """Funcția principală."""
    print("=" * 60)
    print("Server HTTPS cu TLS - Tema 1")
    print("Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("=" * 60)
    print()
    
    # Creează directorul pentru certificate dacă nu există
    (RADACINA_PROIECT / "certs").mkdir(exist_ok=True)
    
    # Creează contextul SSL
    context = creeaza_context_ssl()
    
    if context is None:
        print()
        print("[INFO] Serverul va rula doar în mod HTTP.")
        print()
    
    print(f"Rădăcina documentelor: {RADACINA_DOCUMENTE}")
    print()
    print("Apăsați Ctrl+C pentru a opri serverul")
    print("-" * 60)
    
    try:
        # Pornește serverul HTTP într-un fir separat
        fir_http = threading.Thread(target=porneste_server_http, daemon=True)
        fir_http.start()
        
        # Pornește serverul HTTPS dacă avem context valid
        if context:
            fir_https = threading.Thread(
                target=porneste_server_https, 
                args=(context,),
                daemon=True
            )
            fir_https.start()
        
        # Menține programul activ
        while True:
            threading.Event().wait(1)
            
    except KeyboardInterrupt:
        print("\n[INFO] Oprire servere...")
        print("[INFO] Servere oprite")


if __name__ == "__main__":
    main()
