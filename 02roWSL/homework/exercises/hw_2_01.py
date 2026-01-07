#!/usr/bin/env python3
"""
Tema 2.01: Server TCP cu Autentificare
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

CERINȚĂ:
Extindeți serverul TCP pentru a implementa autentificare simplă.

SPECIFICAȚII:
1. La conectare, serverul cere autentificare
2. Format comandă: LOGIN:utilizator:parolă
3. Utilizatori valizi: admin:admin123, student:parola
4. După autentificare, comenzile normale funcționează
5. Fără autentificare, doar LOGIN este acceptată
6. După 3 încercări eșuate, conexiunea se închide

EXEMPLU INTERACȚIUNE:
    Client: upper:test
    Server: EROARE: Trebuie să vă autentificați. Folosiți LOGIN:user:pass
    
    Client: LOGIN:admin:admin123
    Server: OK: Autentificare reușită. Bine ați venit, admin!
    
    Client: upper:test
    Server: OK: TEST
"""

import socket
import threading
import argparse
import sys
from typing import Tuple, Optional, Dict


# ============================================================================
# Configurație
# ============================================================================

# Utilizatori valizi (în producție, aceștia ar fi într-o bază de date)
UTILIZATORI_VALIZI: Dict[str, str] = {
    "admin": "admin123",
    "student": "parola",
}

# Configurație server
HOST = "0.0.0.0"
PORT = 9090
MAX_ÎNCERCĂRI = 3


# ============================================================================
# TODO: Implementați funcționalitatea de autentificare
# ============================================================================

class SesiuneClient:
    """
    Gestionează starea unei sesiuni client.
    
    TODO: Completați această clasă pentru a:
    1. Urmări dacă clientul este autentificat
    2. Număra încercările de autentificare eșuate
    3. Stoca numele utilizatorului autentificat
    """
    
    def __init__(self):
        # TODO: Inițializați variabilele de stare
        self.autentificat: bool = False
        self.utilizator: Optional[str] = None
        self.încercări_eșuate: int = 0
    
    def încearcă_autentificare(self, utilizator: str, parolă: str) -> Tuple[bool, str]:
        """
        Încearcă să autentifice utilizatorul.
        
        Args:
            utilizator: Numele de utilizator
            parolă: Parola
            
        Returns:
            Tuple (succes, mesaj)
            
        TODO: Implementați logica de autentificare:
        1. Verificați credențialele în UTILIZATORI_VALIZI
        2. Actualizați self.autentificat și self.utilizator la succes
        3. Incrementați self.încercări_eșuate la eșec
        4. Returnați mesajul corespunzător
        """
        # TODO: Implementare
        pass
    
    def poate_continua(self) -> bool:
        """
        Verifică dacă clientul mai poate încerca autentificarea.
        
        Returns:
            True dacă mai are încercări disponibile
        """
        # TODO: Implementare
        pass


def procesează_mesaj(mesaj: str, sesiune: SesiuneClient) -> Tuple[str, bool]:
    """
    Procesează un mesaj ținând cont de starea autentificării.
    
    Args:
        mesaj: Mesajul primit de la client
        sesiune: Sesiunea curentă a clientului
        
    Returns:
        Tuple (răspuns, continuă_conexiune)
        
    TODO: Implementați logica de procesare:
    1. Dacă mesajul începe cu "LOGIN:", extrageți și verificați credențialele
    2. Dacă clientul NU este autentificat și comanda NU este LOGIN,
       returnați eroare și solicitați autentificare
    3. Dacă clientul ESTE autentificat, procesați comanda normal
       (upper, lower, exit, etc.)
    """
    mesaj = mesaj.strip()
    
    # Verificare comandă de ieșire
    if mesaj.lower() in ("exit", "quit"):
        return "La revedere!\n", False
    
    # TODO: Verificare și procesare LOGIN
    if mesaj.upper().startswith("LOGIN:"):
        # TODO: Extrageți utilizator și parolă din mesaj
        # Format: LOGIN:utilizator:parolă
        # Apelați sesiune.încearcă_autentificare()
        pass
    
    # TODO: Verificare dacă clientul este autentificat
    if not sesiune.autentificat:
        # TODO: Returnați mesaj de eroare
        pass
    
    # Comenzi normale (doar pentru utilizatori autentificați)
    # TODO: Procesați comenzile normale (upper, lower, etc.)
    if mesaj.lower().startswith("upper:"):
        text = mesaj[6:]
        return f"OK: {text.upper()}\n", True
    
    if mesaj.lower().startswith("lower:"):
        text = mesaj[6:]
        return f"OK: {text.lower()}\n", True
    
    return f"EROARE: Comandă necunoscută '{mesaj}'\n", True


def gestionează_client(socket_client: socket.socket, adresă: Tuple[str, int]) -> None:
    """
    Gestionează comunicarea cu un client.
    
    Args:
        socket_client: Socket-ul clientului
        adresă: Adresa clientului (ip, port)
    """
    print(f"Client conectat: {adresă[0]}:{adresă[1]}")
    
    # Creare sesiune pentru acest client
    sesiune = SesiuneClient()
    
    try:
        # Trimitere mesaj de bun venit
        bun_venit = "Bine ați venit! Vă rugăm să vă autentificați cu LOGIN:utilizator:parolă\n"
        socket_client.sendall(bun_venit.encode('utf-8'))
        
        while True:
            date = socket_client.recv(1024)
            
            if not date:
                print(f"Client deconectat: {adresă[0]}:{adresă[1]}")
                break
            
            mesaj = date.decode('utf-8')
            print(f"De la {adresă[0]}:{adresă[1]}: {mesaj.strip()}")
            
            răspuns, continuă = procesează_mesaj(mesaj, sesiune)
            socket_client.sendall(răspuns.encode('utf-8'))
            
            if not continuă:
                break
            
            # TODO: Verificați dacă clientul a depășit numărul de încercări
            if not sesiune.poate_continua():
                socket_client.sendall("EROARE: Prea multe încercări. Conexiune închisă.\n".encode('utf-8'))
                break
                
    except Exception as e:
        print(f"Eroare: {e}")
    finally:
        socket_client.close()
        print(f"Conexiune închisă: {adresă[0]}:{adresă[1]}")


def pornește_server(host: str, port: int) -> None:
    """Pornește serverul TCP cu autentificare."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        
        print("=" * 60)
        print(f"Server TCP cu Autentificare pornit pe {host}:{port}")
        print("Utilizatori valizi: admin, student")
        print("Apăsați Ctrl+C pentru oprire")
        print("=" * 60)
        
        try:
            while True:
                socket_client, adresă = server.accept()
                thread = threading.Thread(
                    target=gestionează_client,
                    args=(socket_client, adresă)
                )
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nServer oprit.")


# ============================================================================
# Punct de Intrare
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(description="Server TCP cu Autentificare")
    parser.add_argument("--port", "-p", type=int, default=PORT, help="Port")
    args = parser.parse_args()
    
    pornește_server(HOST, args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
