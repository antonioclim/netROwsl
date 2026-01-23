#!/usr/bin/env python3
"""
FTP Demo Server - Server FTP folosind pyftpdlib

Acest modul oferă un server FTP complet pentru comparație cu implementarea
pseudo-FTP din exercițiul 9.02. Folosește biblioteca pyftpdlib care
implementează protocolul FTP standard conform RFC 959.

Funcționalități:
    - Autentificare utilizatori
    - Mod activ și pasiv
    - Operații complete de fișiere (list, get, put, delete)
    - Configurare porturi passive

Utilizare:
    python3 ftp_demo_server.py --host 127.0.0.1 --port 2121 --root ./server-files

Cerințe:
    pip install pyftpdlib --break-system-packages

Credențiale implicite:
    Utilizator: test
    Parolă: 12345

Comparație cu pseudo-FTP:
    Acest server implementează protocolul FTP complet (RFC 959).
    Pseudo-FTP din ex_9_02 este o versiune simplificată pentru
    scopuri didactice, cu header binar personalizat.
"""

import argparse
import sys
from pathlib import Path

try:
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer
except ImportError:
    print("Error: pyftpdlib is not installed.")
    print("Install with: pip install pyftpdlib --break-system-packages")
    sys.exit(1)


def main() -> None:
    """
    Funcția principală a serverului FTP.
    
    Configurează autorizarea, handler-ul și pornește serverul.
    Serverul rulează până la întrerupere (Ctrl+C).
    """
    parser = argparse.ArgumentParser(description="FTP Demo Server")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address")
    parser.add_argument("--port", type=int, default=2121, help="Port (default: 2121)")
    parser.add_argument("--root", default="./server-files", help="Root directory")
    parser.add_argument("--user", default="test", help="Username")
    parser.add_argument("--password", default="12345", help="Password")
    parser.add_argument("--passive-ports", default="60000-60100", 
                        help="Passive port range")
    
    args = parser.parse_args()
    
    # Ensure root directory exists
    root_path = Path(args.root).resolve()
    root_path.mkdir(parents=True, exist_ok=True)
    
    # Configure authorisation
    authorizer = DummyAuthorizer()
    
    # Add user with all permissions
    # Permissions: e=cwd, l=list, r=retr, a=appe, d=delete, f=rename, m=mkdir, w=stor
    authorizer.add_user(args.user, args.password, str(root_path), perm="elradfmw")
    
    # Configure handler
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "Pseudo-FTP Demo Server (pyftpdlib)"
    
    # Configure passive ports
    start_port, end_port = map(int, args.passive_ports.split("-"))
    handler.passive_ports = range(start_port, end_port + 1)
    
    # Create and start server
    address = (args.host, args.port)
    server = FTPServer(address, handler)
    
    # Server configuration
    server.max_cons = 256
    server.max_cons_per_ip = 5
    
    print(f"[FTP SERVER] Started on {args.host}:{args.port}")
    print(f"[FTP SERVER] Root: {root_path}")
    print(f"[FTP SERVER] User: {args.user}")
    print(f"[FTP SERVER] Passive ports: {args.passive_ports}")
    print("[FTP SERVER] Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[FTP SERVER] Stopping...")
        server.close_all()


if __name__ == "__main__":
    main()
