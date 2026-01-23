#!/usr/bin/env python3
"""
EXERCIȚIUL 1: Server HTTP de Bază
=================================
Disciplina: Rețele de Calculatoare, Săptămâna 8
Nivel: Intermediar
Timp estimat: 30-45 minute

OBIECTIVE DE ÎNVĂȚARE:
- Înțelegerea formatului cerere/răspuns HTTP
- Implementarea parsării cererilor HTTP
- Servirea fișierelor statice cu securitate

INSTRUCȚIUNI:
1. Completați funcțiile marcate cu TODO
2. Rulați testele: python3 -m pytest tests/test_ex01.py -v
3. Testați manual: python3 ex_8_01_server_http.py --port 8888

EVALUARE:
- Parsare corectă cerere: 30%
- Servire fișiere: 30%
- Securitate (path traversal): 20%
- Metoda HEAD: 20%

© Revolvix & ASE-CSIE București
"""

import socket
import os
import sys
import argparse
from pathlib import Path
from typing import Tuple, Dict, Optional

# =============================================================================
# CONSTANTE
# =============================================================================

CRLF = "\r\n"
DOUBLE_CRLF = "\r\n\r\n"

HTTP_STATUS = {
    200: "OK",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}

MIME_TYPES = {
    ".html": "text/html",
    ".htm": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json",
    ".txt": "text/plain",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".ico": "image/x-icon",
}

DEFAULT_TYPE = "application/octet-stream"


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE
# =============================================================================

def parse_request(raw_request: bytes) -> Tuple[str, str, str, Dict[str, str]]:
    """
    Parsează o cerere HTTP și extrage componentele.
    
    Args:
        raw_request: Bytes primiți de la client
    
    Returns:
        Tuple cu: (metodă, cale, versiune, dicționar_headers)
        
    Exemple:
        >>> data = b'GET /index.html HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n'
        >>> metoda, cale, versiune, headers = parse_request(data)
        >>> metoda
        'GET'
        >>> cale
        '/index.html'
        >>> headers['host']
        'localhost'
    
    🔮 PREDICȚIE: Ce ar trebui să returneze funcția pentru cererea:
       b'GET / HTTP/1.1\\r\\nHost: test\\r\\n\\r\\n'
       Notează predicția ta înainte de a implementa!
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Decodifică raw_request din bytes în string (encoding='utf-8')
       Hint: raw_request.decode('utf-8')
    
    2. Separă pe linii folosind CRLF (\\r\\n)
       Hint: text.split(CRLF)
    
    3. Prima linie conține: METODĂ CALE VERSIUNE
       Hint: prima_linie.split(' ') → ['GET', '/index.html', 'HTTP/1.1']
    
    4. Restul liniilor sunt headers în format "Cheie: Valoare"
       Hint: linie.split(': ', 1) pentru a separa cheie de valoare
    
    5. Normalizează cheile headers la lowercase pentru comparații ușoare
       Hint: cheie.lower()
    
    CAZURI SPECIALE DE TRATAT:
    ──────────────────────────
    - Cerere goală sau invalidă → returnează valori implicite sau aruncă excepție
    - Linie de cerere cu mai puțin de 3 părți → eroare
    - Headers fără ':' → ignoră-le
    
    GREȘELI COMUNE:
    ───────────────
    ✗ Folosirea split('\\n') în loc de split('\\r\\n')
    ✗ Uitarea să decodifici bytes în string
    ✗ Nepunerea cheilor la lowercase
    """
    
    # TODO: Implementează parsarea cererii HTTP
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează parse_request()")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE
# =============================================================================

def is_safe_path(requested_path: str, docroot: str) -> bool:
    """
    Verifică dacă calea cerută este sigură (nu permite directory traversal).
    
    Args:
        requested_path: Calea cerută de client (ex: "/images/../../../etc/passwd")
        docroot: Directorul rădăcină pentru fișiere statice
    
    Returns:
        True dacă calea este sigură, False altfel
    
    Exemple:
        >>> is_safe_path("/index.html", "/var/www")
        True
        >>> is_safe_path("/../etc/passwd", "/var/www")
        False
        >>> is_safe_path("/images/logo.png", "/var/www")
        True
        >>> is_safe_path("/images/../../../etc/passwd", "/var/www")
        False
    
    🔮 PREDICȚIE: Pentru calea "/a/b/../../c.txt" cu docroot="/var/www",
       este sigură? Ce cale reală reprezintă? Notează înainte de implementare!
    
    ⚠️ ATENȚIE SECURITATE:
    ──────────────────────
    Aceasta este o funcție CRITICĂ pentru securitate!
    Atacatorii vor încerca:
    - /../../../etc/passwd
    - /..\\..\\..\\windows\\system32\\config\\sam
    - /%2e%2e%2f (URL-encoded ..)
    - /images/../../../etc/shadow
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Normalizează requested_path (elimină .. și .)
       Hint: os.path.normpath(requested_path)
    
    2. Construiește calea completă: docroot + requested_path
       Hint: os.path.join(docroot, requested_path.lstrip('/'))
    
    3. Obține calea absolută pentru ambele
       Hint: os.path.abspath()
    
    4. Verifică că calea completă începe cu docroot
       Hint: cale_completa.startswith(docroot_absolut)
    
    GREȘELI COMUNE:
    ───────────────
    ✗ Compararea string-urilor fără normalizare
    ✗ Uitarea să normalizezi și docroot-ul
    ✗ Nefolosirea abspath() (căi relative pot păcăli verificarea)
    """
    
    # TODO: Implementează verificarea securității căii
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează is_safe_path()")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE
# =============================================================================

def serve_file(path: str, docroot: str) -> Tuple[int, Dict[str, str], bytes]:
    """
    Servește un fișier static de pe disc.
    
    Args:
        path: Calea cerută (ex: "/index.html")
        docroot: Directorul rădăcină
    
    Returns:
        Tuple cu: (cod_status, dicționar_headers, corp_bytes)
    
    Exemple:
        >>> status, headers, body = serve_file("/index.html", "./www")
        >>> status
        200
        >>> headers['content-type']
        'text/html'
        >>> len(body) > 0
        True
    
    🔮 PREDICȚIE: Ce cod de status și headers aștepți pentru:
       - serve_file("/hello.txt", "./www") dacă fișierul există?
       - serve_file("/inexistent.txt", "./www")?
       - serve_file("/../etc/passwd", "./www")?
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Normalizează calea: "/" → "/index.html"
       if path == "/":
           path = "/index.html"
    
    2. Verifică securitatea cu is_safe_path()
       Dacă nesigură → returnează (403, {}, b"Forbidden")
    
    3. Construiește calea completă către fișier
       cale_fisier = os.path.join(docroot, path.lstrip('/'))
    
    4. Verifică dacă fișierul există
       Dacă nu există → returnează (404, {}, b"Not Found")
    
    5. Determină Content-Type din extensie
       extensie = os.path.splitext(path)[1].lower()
       content_type = MIME_TYPES.get(extensie, DEFAULT_TYPE)
    
    6. Citește conținutul fișierului în mod binar ('rb')
       with open(cale_fisier, 'rb') as f:
           continut = f.read()
    
    7. Construiește headers-ele răspunsului
       headers = {
           "Content-Type": content_type,
           "Content-Length": str(len(continut))
       }
    
    8. Returnează (200, headers, continut)
    
    GREȘELI COMUNE:
    ───────────────
    ✗ Citirea fișierului în mod text ('r') în loc de binar ('rb')
    ✗ Nesetarea Content-Length
    ✗ Returnarea stringului în loc de bytes pentru body
    """
    
    # TODO: Implementează servirea fișierului
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează serve_file()")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE
# =============================================================================

def build_response(status_code: int, headers: Dict[str, str], body: bytes) -> bytes:
    """
    Construiește un răspuns HTTP complet.
    
    Args:
        status_code: Codul de status HTTP (200, 404, etc.)
        headers: Dicționar cu headers
        body: Conținutul răspunsului în bytes
    
    Returns:
        Răspunsul HTTP complet ca bytes
    
    Exemple:
        >>> resp = build_response(200, {"Content-Type": "text/plain"}, b"Hello")
        >>> resp.startswith(b"HTTP/1.1 200 OK")
        True
        >>> b"Content-Type: text/plain" in resp
        True
        >>> resp.endswith(b"Hello")
        True
    
    FORMAT RĂSPUNS HTTP:
    ────────────────────
        HTTP/1.1 {status_code} {status_text}\\r\\n
        Header1: Value1\\r\\n
        Header2: Value2\\r\\n
        \\r\\n
        {body}
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Construiește linia de status: "HTTP/1.1 {code} {text}\\r\\n"
       status_text = HTTP_STATUS.get(status_code, "Unknown")
       status_line = f"HTTP/1.1 {status_code} {status_text}{CRLF}"
    
    2. Construiește liniile de headers: "{Key}: {Value}\\r\\n"
       header_lines = ""
       for key, value in headers.items():
           header_lines += f"{key}: {value}{CRLF}"
    
    3. Adaugă linia goală de separare: "\\r\\n"
       header_lines += CRLF
    
    4. Convertește header-ele în bytes și concatenează cu body
       return status_line.encode() + header_lines.encode() + body
    
    🔮 PREDICȚIE: Pentru build_response(404, {}, b"Not Found"),
       câți bytes va avea răspunsul final? Calculează înainte de a testa!
    """
    
    # TODO: Implementează construirea răspunsului HTTP
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează build_response()")


# =============================================================================
# TODO: IMPLEMENTEAZĂ ACEASTĂ FUNCȚIE
# =============================================================================

def handle_request(raw_request: bytes, docroot: str) -> bytes:
    """
    Procesează o cerere HTTP completă și returnează răspunsul.
    
    Args:
        raw_request: Cererea HTTP în bytes
        docroot: Directorul rădăcină pentru fișiere
    
    Returns:
        Răspunsul HTTP complet în bytes
    
    METODE SUPORTATE:
    ─────────────────
    - GET: returnează fișierul complet (headers + body)
    - HEAD: returnează doar headers (fără body)
    - Altele: returnează 405 Method Not Allowed
    
    🔮 PREDICȚIE: Ce diferență va fi între răspunsurile pentru:
       - GET /hello.txt HTTP/1.1
       - HEAD /hello.txt HTTP/1.1
       (Hint: unul are body, celălalt nu)
    
    PAȘI DE IMPLEMENTARE:
    ─────────────────────
    1. Parsează cererea cu parse_request()
       try:
           metoda, cale, versiune, headers = parse_request(raw_request)
       except Exception:
           return build_response(400, {}, b"Bad Request")
    
    2. Verifică metoda (GET sau HEAD)
       if metoda not in ["GET", "HEAD"]:
           return build_response(405, {"Allow": "GET, HEAD"}, b"Method Not Allowed")
    
    3. Servește fișierul cu serve_file()
       status, resp_headers, body = serve_file(cale, docroot)
    
    4. Pentru HEAD, setează body la b"" (dar păstrează headers!)
       if metoda == "HEAD":
           body = b""
    
    5. Construiește și returnează răspunsul
       return build_response(status, resp_headers, body)
    """
    
    # TODO: Implementează handler-ul complet
    # Scrie codul tău aici...
    
    raise NotImplementedError("TODO: Implementează handle_request()")


# =============================================================================
# COD FURNIZAT - NU MODIFICA
# =============================================================================

def run_server(host: str, port: int, docroot: str):
    """
    Pornește serverul HTTP.
    Cod furnizat - nu necesită modificări.
    """
    docroot = os.path.abspath(docroot)
    
    if not os.path.isdir(docroot):
        print(f"[EROARE] Directorul docroot nu există: {docroot}")
        sys.exit(1)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[INFO] Server pornit pe http://{host}:{port}/")
        print(f"[INFO] Document root: {docroot}")
        print("[INFO] Apasă Ctrl+C pentru oprire")
        
        while True:
            client_socket, client_addr = server_socket.accept()
            print(f"[CONN] Conexiune de la {client_addr[0]}:{client_addr[1]}")
            
            try:
                raw_request = client_socket.recv(4096)
                if raw_request:
                    response = handle_request(raw_request, docroot)
                    client_socket.sendall(response)
            except Exception as e:
                print(f"[EROARE] {e}")
                error_response = build_response(
                    500, 
                    {"Content-Type": "text/plain"}, 
                    b"Internal Server Error"
                )
                client_socket.sendall(error_response)
            finally:
                client_socket.close()
                
    except KeyboardInterrupt:
        print("\n[INFO] Server oprit de utilizator")
    finally:
        server_socket.close()


def main():
    parser = argparse.ArgumentParser(description="Server HTTP simplu")
    parser.add_argument("--host", default="0.0.0.0", help="Adresa de bind")
    parser.add_argument("--port", type=int, default=8888, help="Portul de ascultare")
    parser.add_argument("--docroot", default="www", help="Directorul cu fișiere statice")
    
    args = parser.parse_args()
    run_server(args.host, args.port, args.docroot)


if __name__ == "__main__":
    main()
