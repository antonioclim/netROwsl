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

NIVEL: Intermediar (Bloom: APPLY)
TIMP ESTIMAT: 45-60 minute
"""

from __future__ import annotations

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
HOST: str = "0.0.0.0"
PORT: int = 9090
MAX_ÎNCERCĂRI: int = 3


# ============================================================================
# TODO: Implementați funcționalitatea de autentificare
# ============================================================================

class SesiuneClient:
    """
    Gestionează starea unei sesiuni client.
    
    Această clasă păstrează informații despre starea autentificării
    unui client conectat, inclusiv numărul de încercări eșuate.
    
    Attributes:
        autentificat: True dacă clientul s-a autentificat cu succes
        utilizator: Numele utilizatorului autentificat (None dacă neautentificat)
        încercări_eșuate: Numărul de încercări de autentificare eșuate
    
    TODO: Completați această clasă pentru a:
    1. Urmări dacă clientul este autentificat
    2. Număra încercările de autentificare eșuate
    3. Stoca numele utilizatorului autentificat
    """
    
    def __init__(self) -> None:
        """Inițializează o nouă sesiune cu stare neautentificată."""
        self.autentificat: bool = False
        self.utilizator: Optional[str] = None
        self.încercări_eșuate: int = 0
    
    def încearcă_autentificare(self, utilizator: str, parolă: str) -> Tuple[bool, str]:
        """
        Încearcă să autentifice utilizatorul cu credențialele furnizate.
        
        Verifică perechea utilizator/parolă contra dicționarului UTILIZATORI_VALIZI.
        La succes, actualizează starea sesiunii. La eșec, incrementează contorul
        de încercări eșuate.
        
        Args:
            utilizator: Numele de utilizator furnizat de client
            parolă: Parola furnizată de client
            
        Returns:
            Tuple cu două elemente:
            - bool: True dacă autentificarea a reușit, False altfel
            - str: Mesaj descriptiv pentru client
            
        Example:
            >>> sesiune = SesiuneClient()
            >>> succes, mesaj = sesiune.încearcă_autentificare("admin", "admin123")
            >>> succes
            True
            >>> sesiune.autentificat
            True
            
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
        
        Un client care a depășit MAX_ÎNCERCĂRI încercări eșuate nu mai
        poate continua și conexiunea ar trebui închisă.
        
        Returns:
            True dacă clientul mai are încercări disponibile sau este
            deja autentificat, False dacă a epuizat încercările.
            
        Note:
            Un client autentificat poate întotdeauna continua.
        """
        # TODO: Implementare
        pass


def procesează_mesaj(mesaj: str, sesiune: SesiuneClient) -> Tuple[str, bool]:
    """
    Procesează un mesaj ținând cont de starea autentificării clientului.
    
    Această funcție implementează logica de procesare a comenzilor,
    diferențiind între clienții autentificați și cei neautentificați.
    
    Args:
        mesaj: Mesajul primit de la client (poate conține whitespace)
        sesiune: Obiectul SesiuneClient care păstrează starea conexiunii
        
    Returns:
        Tuple cu două elemente:
        - str: Răspunsul de trimis clientului (include \\n la final)
        - bool: True pentru a continua conexiunea, False pentru a o închide
        
    Comenzi suportate:
        - LOGIN:utilizator:parolă - Autentificare
        - upper:text - Convertește text la majuscule (necesită autentificare)
        - lower:text - Convertește text la minuscule (necesită autentificare)
        - exit/quit - Închide conexiunea
        
    TODO: Implementați logica de procesare:
    1. Dacă mesajul începe cu "LOGIN:", extrageți și verificați credențialele
    2. Dacă clientul NU este autentificat și comanda NU este LOGIN,
       returnați eroare și solicitați autentificare
    3. Dacă clientul ESTE autentificat, procesați comanda normal
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
    if mesaj.lower().startswith("upper:"):
        text = mesaj[6:]
        return f"OK: {text.upper()}\n", True
    
    if mesaj.lower().startswith("lower:"):
        text = mesaj[6:]
        return f"OK: {text.lower()}\n", True
    
    return f"EROARE: Comandă necunoscută '{mesaj}'\n", True


def gestionează_client(socket_client: socket.socket, adresă: Tuple[str, int]) -> None:
    """
    Gestionează comunicarea cu un client conectat.
    
    Această funcție rulează într-un thread separat pentru fiecare client
    și gestionează întregul ciclu de viață al conexiunii: salut, autentificare,
    procesare comenzi și închidere.
    
    Args:
        socket_client: Socket-ul TCP conectat la client
        adresă: Tuple (ip, port) reprezentând adresa clientului
        
    Note:
        - Socket-ul este închis automat la ieșirea din funcție
        - Excepțiile sunt prinse și loggate, nu propagate
        - Thread-ul este daemon, deci nu blochează oprirea serverului
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
            
            # Verificare dacă clientul a depășit numărul de încercări
            if not sesiune.poate_continua():
                socket_client.sendall(
                    "EROARE: Prea multe încercări. Conexiune închisă.\n".encode('utf-8')
                )
                break
                
    except ConnectionResetError:
        print(f"Conexiune resetată de client: {adresă[0]}:{adresă[1]}")
    except Exception as e:
        print(f"Eroare cu clientul {adresă[0]}:{adresă[1]}: {e}")
    finally:
        socket_client.close()
        print(f"Conexiune închisă: {adresă[0]}:{adresă[1]}")


def pornește_server(host: str, port: int) -> None:
    """
    Pornește serverul TCP cu suport pentru autentificare.
    
    Serverul acceptă conexiuni pe adresa și portul specificate,
    creând un thread separat pentru fiecare client conectat.
    Rulează până când primește Ctrl+C (KeyboardInterrupt).
    
    Args:
        host: Adresa IP pe care să asculte.
            - "0.0.0.0" pentru toate interfețele (accesibil din rețea)
            - "127.0.0.1" doar pentru conexiuni locale
        port: Portul TCP pe care să asculte (1-65535)
        
    Note:
        - Utilizatorii valizi sunt definiți în constanta UTILIZATORI_VALIZI
        - Fiecare client are maxim MAX_ÎNCERCĂRI pentru autentificare
        - Thread-urile client sunt daemon (se opresc automat cu serverul)
        - SO_REUSEADDR este setat pentru a permite restart rapid
        
    Raises:
        OSError: Dacă portul este deja în uz sau adresa invalidă
        
    Example:
        >>> pornește_server("0.0.0.0", 9090)  # Accesibil din rețea
        >>> pornește_server("127.0.0.1", 8080)  # Doar local
    """
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
                    args=(socket_client, adresă),
                    daemon=True
                )
                thread.start()
        except KeyboardInterrupt:
            print("\nServer oprit.")


# ============================================================================
# Punct de Intrare
# ============================================================================

def main() -> int:
    """
    Punct de intrare pentru rularea serverului din linia de comandă.
    
    Returns:
        Cod de ieșire (0 pentru succes)
    """
    parser = argparse.ArgumentParser(
        description="Server TCP cu Autentificare - Tema 2.01",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python hw_2_01.py                    # Pornește pe portul implicit (9090)
  python hw_2_01.py --port 8080        # Pornește pe portul 8080

Testare cu netcat:
  nc localhost 9090
        """
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=PORT,
        help=f"Portul pe care să asculte serverul (implicit: {PORT})"
    )
    args = parser.parse_args()
    
    pornește_server(HOST, args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
