#!/usr/bin/env python3
"""
Server Protocol TEXT
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Server pentru protocolul TEXT care folosește mesaje lizibile cu prefix de lungime.
Format mesaj: <LUNGIME> <CONȚINUT>
Port implicit: 5400
"""

import socket
import threading
import logging
from typing import Dict, Optional

# Configurare logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configurație server
HOST = '0.0.0.0'
PORT = 5400
DIMENSIUNE_BUFFER = 4096


class MagazinCheieValoare:
    """Magazin thread-safe pentru perechi cheie-valoare."""
    
    def __init__(self):
        self._date: Dict[str, str] = {}
        self._lock = threading.Lock()
    
    def seteaza(self, cheie: str, valoare: str) -> bool:
        """Setează o valoare pentru o cheie."""
        with self._lock:
            self._date[cheie] = valoare
            return True
    
    def obtine(self, cheie: str) -> Optional[str]:
        """Obține valoarea pentru o cheie."""
        with self._lock:
            return self._date.get(cheie)
    
    def sterge(self, cheie: str) -> bool:
        """Șterge o cheie."""
        with self._lock:
            if cheie in self._date:
                del self._date[cheie]
                return True
            return False
    
    def numar(self) -> int:
        """Returnează numărul de chei."""
        with self._lock:
            return len(self._date)
    
    def chei(self) -> list:
        """Returnează lista de chei."""
        with self._lock:
            return list(self._date.keys())


# Instanță globală a magazinului
magazin = MagazinCheieValoare()


def formateaza_raspuns(continut: str) -> bytes:
    """Formatează un răspuns în format protocol TEXT."""
    lungime = len(continut)
    return f"{lungime} {continut}".encode('utf-8')


def proceseaza_comanda(comanda: str) -> str:
    """
    Procesează o comandă și returnează răspunsul.
    
    Comenzi suportate:
    - PING: Returnează PONG
    - SET <cheie> <valoare>: Setează o valoare
    - GET <cheie>: Obține o valoare
    - DEL <cheie>: Șterge o cheie
    - COUNT: Returnează numărul de chei
    - KEYS: Returnează lista de chei
    - QUIT: Închide conexiunea
    """
    parti = comanda.strip().split(' ', 2)
    
    if not parti:
        return "ERR comanda goala"
    
    cmd = parti[0].upper()
    
    if cmd == "PING":
        return "PONG"
    
    elif cmd == "SET":
        if len(parti) < 3:
            return "ERR SET necesita cheie si valoare"
        cheie = parti[1]
        valoare = parti[2]
        magazin.seteaza(cheie, valoare)
        return "OK"
    
    elif cmd == "GET":
        if len(parti) < 2:
            return "ERR GET necesita cheie"
        cheie = parti[1]
        valoare = magazin.obtine(cheie)
        if valoare is None:
            return "ERR cheie inexistenta"
        return valoare
    
    elif cmd == "DEL":
        if len(parti) < 2:
            return "ERR DEL necesita cheie"
        cheie = parti[1]
        if magazin.sterge(cheie):
            return "OK"
        return "ERR cheie inexistenta"
    
    elif cmd == "COUNT":
        return str(magazin.numar())
    
    elif cmd == "KEYS":
        chei = magazin.chei()
        if not chei:
            return ""
        return " ".join(chei)
    
    elif cmd == "QUIT":
        return "BYE"
    
    else:
        return f"ERR comanda necunoscuta: {cmd}"


def parseaza_mesaj(date: bytes) -> tuple:
    """
    Parsează un mesaj în format protocol TEXT.
    
    Returns:
        Tuple (lungime, continut, rest) sau (None, None, date) dacă incomplet
    """
    try:
        text = date.decode('utf-8')
        spatiu_idx = text.find(' ')
        if spatiu_idx == -1:
            return None, None, date
        
        lungime = int(text[:spatiu_idx])
        start_continut = spatiu_idx + 1
        
        if len(text) < start_continut + lungime:
            return None, None, date
        
        continut = text[start_continut:start_continut + lungime]
        rest = text[start_continut + lungime:].encode('utf-8')
        
        return lungime, continut, rest
        
    except (ValueError, UnicodeDecodeError):
        return None, None, date


def gestioneaza_client(socket_client: socket.socket, adresa: tuple):
    """Gestionează o conexiune client."""
    logger.info(f"Conexiune nouă de la {adresa}")
    buffer = b''
    
    try:
        while True:
            # Primire date
            date = socket_client.recv(DIMENSIUNE_BUFFER)
            if not date:
                logger.info(f"Client deconectat: {adresa}")
                break
            
            buffer += date
            
            # Procesare mesaje complete
            while buffer:
                lungime, continut, rest = parseaza_mesaj(buffer)
                
                if lungime is None:
                    break  # Mesaj incomplet
                
                buffer = rest
                
                logger.debug(f"Primit de la {adresa}: {continut}")
                
                # Procesare comandă
                raspuns = proceseaza_comanda(continut)
                
                # Verifică QUIT
                if raspuns == "BYE":
                    socket_client.sendall(formateaza_raspuns(raspuns))
                    logger.info(f"Client a trimis QUIT: {adresa}")
                    return
                
                # Trimitere răspuns
                raspuns_bytes = formateaza_raspuns(raspuns)
                socket_client.sendall(raspuns_bytes)
                logger.debug(f"Trimis către {adresa}: {raspuns}")
                
    except ConnectionResetError:
        logger.warning(f"Conexiune resetată: {adresa}")
    except Exception as e:
        logger.error(f"Eroare cu clientul {adresa}: {e}")
    finally:
        socket_client.close()


def porneste_server():
    """Pornește serverul TEXT."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        logger.info(f"Server TEXT pornit pe {HOST}:{PORT}")
        logger.info("Aștept conexiuni... (Ctrl+C pentru oprire)")
        
        while True:
            socket_client, adresa = server.accept()
            thread = threading.Thread(
                target=gestioneaza_client,
                args=(socket_client, adresa)
            )
            thread.daemon = True
            thread.start()
            
    except KeyboardInterrupt:
        logger.info("\nOprire server...")
    finally:
        server.close()


if __name__ == "__main__":
    porneste_server()
