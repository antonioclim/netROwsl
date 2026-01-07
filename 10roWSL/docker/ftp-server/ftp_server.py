#!/usr/bin/env python3
"""
Server FTP pentru Laborator
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Server FTP simplu folosind pyftpdlib.
Credențiale: labftp / labftp
Porturi pasive: 30000-30009
"""

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Configurație
PORT_FTP = 2121
GAZDA = "0.0.0.0"
DIRECTOR_RADACINA = "/home/labftp"
UTILIZATOR = "labftp"
PAROLA = "labftp"
PORTURI_PASIVE = (30000, 30009)


class HandlerPersonalizat(FTPHandler):
    """Handler FTP cu logging personalizat."""
    
    def on_connect(self):
        print(f"[CONECTARE] {self.remote_ip}:{self.remote_port}")
    
    def on_disconnect(self):
        print(f"[DECONECTARE] {self.remote_ip}")
    
    def on_login(self, username):
        print(f"[AUTENTIFICARE] {username} de la {self.remote_ip}")
    
    def on_logout(self, username):
        print(f"[DELOGARE] {username}")
    
    def on_file_sent(self, file):
        print(f"[DESCĂRCARE] {file}")
    
    def on_file_received(self, file):
        print(f"[ÎNCĂRCARE] {file}")


def main():
    """Funcția principală - pornește serverul FTP."""
    print("=" * 50)
    print("  Server FTP - Laborator Săptămâna 10")
    print("=" * 50)
    print()
    
    # Configurează autorizarea
    autorizator = DummyAuthorizer()
    autorizator.add_user(
        UTILIZATOR,
        PAROLA,
        DIRECTOR_RADACINA,
        perm="elradfmwMT"  # Permisiuni complete
    )
    
    # Permite și acces anonim (doar citire)
    autorizator.add_anonymous(DIRECTOR_RADACINA, perm="elr")
    
    # Configurează handler-ul
    handler = HandlerPersonalizat
    handler.authorizer = autorizator
    handler.passive_ports = range(*PORTURI_PASIVE)
    
    # Banner personalizat
    handler.banner = "Bine ați venit pe serverul FTP de laborator! (by Revolvix)"
    
    # Creează și pornește serverul
    server = FTPServer((GAZDA, PORT_FTP), handler)
    
    # Limite de conexiuni
    server.max_cons = 50
    server.max_cons_per_ip = 5
    
    print(f"  Ascultare pe {GAZDA}:{PORT_FTP}")
    print(f"  Director rădăcină: {DIRECTOR_RADACINA}")
    print(f"  Utilizator: {UTILIZATOR}")
    print(f"  Porturi pasive: {PORTURI_PASIVE[0]}-{PORTURI_PASIVE[1]}")
    print()
    print("  Așteptare conexiuni...")
    print("-" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer oprit.")
        server.close_all()


if __name__ == "__main__":
    main()
