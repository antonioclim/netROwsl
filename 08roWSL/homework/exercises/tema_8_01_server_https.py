#!/usr/bin/env python3
"""
TEMA 1: Server HTTPS cu TLS
===========================
Disciplina: Rețele de Calculatoare, Săptămâna 8
Nivel: Avansat
Timp estimat: 90-120 minute
Punctaj: 100 puncte

OBIECTIVE DE ÎNVĂȚARE:
- Înțelegerea protocolului TLS și a certificatelor
- Implementarea unui server HTTPS securizat
- Gestionarea erorilor de conexiune TLS

CERINȚE:
1. Generați un certificat auto-semnat (20 puncte)
2. Implementați context SSL/TLS (30 puncte)
3. Rulați server dual-port HTTP + HTTPS (20 puncte)
4. Gestionați corect erorile (15 puncte)
5. Calitatea codului și documentație (15 puncte)

GENERARE CERTIFICAT:
    mkdir -p certs
    openssl req -x509 -newkey rsa:4096 \\
        -keyout certs/key.pem \\
        -out certs/cert.pem \\
        -days 365 -nodes \\
        -subj "/CN=localhost"

TESTARE:
    curl http://localhost:8080/
    curl -k https://localhost:8443/  # -k ignoră verificarea certificatului

© Revolvix & ASE-CSIE București
"""

import socket
import ssl
import threading
import mimetypes
from pathlib import Path
from typing import Tuple, Optional, Dict

# =============================================================================
# CONFIGURAȚIE
# =============================================================================

PORT_HTTP = 8080
PORT_HTTPS = 8443
GAZDA = "127.0.0.1"
DIMENSIUNE_BUFFER = 4096

# Căi fișiere
RADACINA_PROIECT = Path(__file__).parent.parent.parent
RADACINA_DOCUMENTE = RADACINA_PROIECT / "www"
FISIER_CERTIFICAT = RADACINA_PROIECT / "certs" / "cert.pem"
FISIER_CHEIE = RADACINA_PROIECT / "certs" / "key.pem"


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE (30 puncte)
# =============================================================================

def creeaza_context_ssl() -> Optional[ssl.SSLContext]:
    """
    Creează și configurează contextul SSL pentru server.
    
    Returns:
        Contextul SSL configurat sau None dacă certificatele nu există
    
    🔮 PREDICȚIE: Ce se întâmplă dacă încerci să încarci un certificat
       care nu corespunde cu cheia privată? Ce eroare aștepți?
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Creează un SSLContext pentru server TLS
       context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    2. Setează versiunea minimă TLS (securitate!)
       context.minimum_version = ssl.TLSVersion.TLSv1_2
       
       De ce TLS 1.2? Versiunile mai vechi (SSLv3, TLS 1.0, TLS 1.1) au 
       vulnerabilități cunoscute (POODLE, BEAST, etc.)
    
    3. Încarcă certificatul și cheia privată
       context.load_cert_chain(
           certfile=str(FISIER_CERTIFICAT),
           keyfile=str(FISIER_CHEIE)
       )
    
    4. Tratează FileNotFoundError (certificatele nu există)
       - Afișează instrucțiuni pentru generare
       - Returnează None
    
    5. Tratează ssl.SSLError (certificat/cheie invalide)
       - Loghează eroarea
       - Returnează None
    
    EXEMPLU RETURN:
        >>> ctx = creeaza_context_ssl()
        >>> ctx is not None  # dacă certificatele există
        True
        >>> ctx.minimum_version
        <TLSVersion.TLSv1_2: 771>
    
    GREȘELI COMUNE:
    ───────────────
    ✗ Folosirea PROTOCOL_TLS în loc de PROTOCOL_TLS_SERVER
    ✗ Uitarea să convertești Path la str pentru load_cert_chain
    ✗ Nesetarea versiunii minime (permite versiuni nesigure)
    """
    
    # TODO: Implementează crearea contextului SSL
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează creeaza_context_ssl()")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE (20 puncte parțial)
# =============================================================================

def gestioneaza_cerere(date_cerere: bytes) -> Tuple[int, Dict[str, str], bytes]:
    """
    Procesează cererea HTTP și returnează răspunsul.
    
    Args:
        date_cerere: Cererea HTTP brută în bytes
    
    Returns:
        Tuplu (cod_stare, antete, corp)
    
    🔮 PREDICȚIE: Ce cod de stare ar trebui să returneze serverul pentru:
       - GET /index.html (fișier există)
       - GET /inexistent.txt (fișier nu există)
       - GET /../../../etc/passwd (path traversal)
       - POST /index.html (metodă nepermisă)
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Decodifică cererea din bytes în string
       text_cerere = date_cerere.decode('utf-8', errors='replace')
    
    2. Extrage prima linie (request line)
       prima_linie = text_cerere.split('\\r\\n')[0]
       parti = prima_linie.split(' ')  # ['GET', '/path', 'HTTP/1.1']
    
    3. Validează cererea
       - Verifică că are cel puțin 2 părți
       - Verifică metoda (doar GET și HEAD permise)
    
    4. Previne path traversal (SECURITATE!)
       - Verifică dacă '..' apare în cale
       - Returnează 403 Forbidden dacă da
    
    5. Rezolvă calea fișierului
       - '/' → 'index.html'
       - Construiește calea completă
    
    6. Verifică existența și citește fișierul
       - 404 dacă nu există
       - 403 dacă e director
       - 200 + conținut dacă e fișier valid
    
    7. Determină Content-Type
       tip_mime, _ = mimetypes.guess_type(str(cale_fisier))
    
    GREȘELI COMUNE:
    ───────────────
    ✗ Uitarea să tratezi cazul când calea e doar '/'
    ✗ Verificarea path traversal după rezolvarea căii (prea târziu!)
    ✗ Citirea fișierului în mod text în loc de binar
    """
    
    # TODO: Implementează procesarea cererii
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează gestioneaza_cerere()")


# =============================================================================
# COD FURNIZAT - POȚI MODIFICA DACĂ DOREȘTI
# =============================================================================

def construieste_raspuns(cod_stare: int, antete: Dict[str, str], corp: bytes) -> bytes:
    """
    Construiește răspunsul HTTP complet.
    
    Cod furnizat - poți modifica dacă dorești să adaugi headers suplimentare.
    """
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
    """Gestionează conexiunea unui client. Cod furnizat."""
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


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE (10 puncte)
# =============================================================================

def porneste_server_http() -> None:
    """
    Pornește serverul HTTP pe PORT_HTTP.
    
    🔮 PREDICȚIE: De ce setăm SO_REUSEADDR pe socket? Ce se întâmplă
       dacă nu-l setăm și repornim serverul rapid?
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Creează socket TCP
       socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    2. Setează opțiunea SO_REUSEADDR (permite refolosirea portului)
       socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    3. Leagă socket-ul la adresă și port
       socket_server.bind((GAZDA, PORT_HTTP))
    
    4. Începe să asculte (queue de 100 conexiuni)
       socket_server.listen(100)
    
    5. Bucla principală: acceptă conexiuni
       while True:
           socket_client, adresa = socket_server.accept()
           fir = threading.Thread(target=gestioneaza_client, args=(...))
           fir.start()
    """
    
    # TODO: Implementează serverul HTTP
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează porneste_server_http()")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE (20 puncte)
# =============================================================================

def porneste_server_https(context: ssl.SSLContext) -> None:
    """
    Pornește serverul HTTPS pe PORT_HTTPS.
    
    Args:
        context: Contextul SSL configurat
    
    🔮 PREDICȚIE: Ce se întâmplă dacă un client încearcă să se conecteze
       cu HTTP simplu (nu HTTPS) la portul 8443? Ce eroare va apărea?
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Similar cu porneste_server_http() - creează și leagă socket-ul
    
    2. În bucla de accept, împachetează socket-ul cu TLS:
       try:
           socket_ssl = context.wrap_socket(
               socket_client,
               server_side=True  # IMPORTANT: suntem server, nu client!
           )
       except ssl.SSLError as e:
           print(f"Handshake eșuat: {e}")
           socket_client.close()
           continue
    
    3. Gestionează clientul cu socket_ssl (nu socket_client!)
    
    DIFERENȚA CHEIE:
    ────────────────
    HTTP:  accept() → gestionează direct
    HTTPS: accept() → wrap_socket() → gestionează socket-ul TLS
    
    GREȘELI COMUNE:
    ───────────────
    ✗ Uitarea server_side=True (wrap_socket presupune client implicit)
    ✗ Trimiterea socket-ului ne-împachetat la handler
    ✗ Neprinderea ssl.SSLError din wrap_socket
    """
    
    # TODO: Implementează serverul HTTPS
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează porneste_server_https()")


# =============================================================================
# FUNCȚIA PRINCIPALĂ - NU MODIFICA
# =============================================================================

def main():
    """Funcția principală."""
    print("=" * 60)
    print("Server HTTPS cu TLS - Tema 1")
    print("Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("=" * 60)
    print()
    
    (RADACINA_PROIECT / "certs").mkdir(exist_ok=True)
    
    context = creeaza_context_ssl()
    
    if context is None:
        print()
        print("[INFO] Serverul va rula doar în mod HTTP.")
        print("[INFO] Generează certificatul pentru a activa HTTPS.")
        print()
    
    print(f"Rădăcina documentelor: {RADACINA_DOCUMENTE}")
    print()
    print("Apăsați Ctrl+C pentru a opri serverul")
    print("-" * 60)
    
    try:
        fir_http = threading.Thread(target=porneste_server_http, daemon=True)
        fir_http.start()
        
        if context:
            fir_https = threading.Thread(
                target=porneste_server_https, 
                args=(context,),
                daemon=True
            )
            fir_https.start()
        
        while True:
            threading.Event().wait(1)
            
    except KeyboardInterrupt:
        print("\n[INFO] Oprire servere...")
        print("[INFO] Servere oprite")


if __name__ == "__main__":
    main()
