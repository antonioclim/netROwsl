#!/usr/bin/env python3
"""
Server Protocol TEXT
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Server pentru protocolul TEXT care folosește mesaje lizibile cu prefix de lungime.
Format mesaj: <LUNGIME> <CONȚINUT>
Port implicit: 5400
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# Scop: Importă modulele necesare pentru networking și concurență
# Transferabil la: Orice server TCP multi-threaded
# ═══════════════════════════════════════════════════════════════════════════════

import socket
import threading
import logging
from typing import Dict, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURARE_LOGGING
# Scop: Setează formatarea și nivelul de logging
# Transferabil la: Orice aplicație Python cu necesități de logging
# ═══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL
# Scop: Definește valorile fixe ale protocolului
# Transferabil la: Orice server TCP cu configurare centralizată
# ═══════════════════════════════════════════════════════════════════════════════

HOST: str = '0.0.0.0'
PORT: int = 5400
DIMENSIUNE_BUFFER: int = 4096


# ═══════════════════════════════════════════════════════════════════════════════
# STOCARE_DATE
# Scop: Implementează un magazin thread-safe pentru perechi cheie-valoare
# Transferabil la: Orice sistem care necesită stocare partajată între threads
# ═══════════════════════════════════════════════════════════════════════════════

class MagazinCheieValoare:
    """Magazin thread-safe pentru perechi cheie-valoare."""
    
    def __init__(self) -> None:
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
        """Șterge o cheie și returnează True dacă exista."""
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


# ═══════════════════════════════════════════════════════════════════════════════
# FORMATARE_MESAJE
# Scop: Serializare răspunsuri în format protocol TEXT
# Transferabil la: Orice protocol text-based cu length prefix
# ═══════════════════════════════════════════════════════════════════════════════

def formateaza_raspuns(continut: str) -> bytes:
    """
    Formatează un răspuns în format protocol TEXT.
    
    Args:
        continut: Textul răspunsului
        
    Returns:
        Răspunsul formatat ca bytes: "<lungime> <continut>"
    """
    lungime = len(continut)
    return f"{lungime} {continut}".encode('utf-8')


# ═══════════════════════════════════════════════════════════════════════════════
# PROCESARE_COMENZI
# Scop: Implementează logica de business pentru fiecare comandă
# Transferabil la: Orice server cu comenzi multiple
# ═══════════════════════════════════════════════════════════════════════════════

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
    
    Args:
        comanda: Comanda primită de la client
        
    Returns:
        Răspunsul pentru client
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
        logger.debug(f"SET {cheie} = {valoare}")
        return "OK"
    
    elif cmd == "GET":
        if len(parti) < 2:
            return "ERR GET necesita cheie"
        cheie = parti[1]
        valoare = magazin.obtine(cheie)
        if valoare is None:
            return "ERR cheie inexistenta"
        logger.debug(f"GET {cheie} -> {valoare}")
        return valoare
    
    elif cmd == "DEL":
        if len(parti) < 2:
            return "ERR DEL necesita cheie"
        cheie = parti[1]
        if magazin.sterge(cheie):
            logger.debug(f"DEL {cheie}")
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
        logger.warning(f"Comandă necunoscută: {cmd}")
        return f"ERR comanda necunoscuta: {cmd}"


# ═══════════════════════════════════════════════════════════════════════════════
# PARSARE_PROTOCOL
# Scop: Extragerea mesajelor complete din buffer
# Transferabil la: Orice parser de protocol cu length prefix
# ═══════════════════════════════════════════════════════════════════════════════

def parseaza_mesaj(date: bytes) -> Tuple[Optional[int], Optional[str], bytes]:
    """
    Parsează un mesaj în format protocol TEXT.
    
    Args:
        date: Buffer-ul de date primite
    
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


# ═══════════════════════════════════════════════════════════════════════════════
# GESTIONARE_CLIENT
# Scop: Gestionează ciclul de viață al unei conexiuni client
# Transferabil la: Orice server TCP concurent
# ═══════════════════════════════════════════════════════════════════════════════

def gestioneaza_client(socket_client: socket.socket, adresa: Tuple[str, int]) -> None:
    """
    Gestionează o conexiune client.
    
    Rulează într-un thread separat. Primește mesaje, le procesează
    și trimite răspunsuri până când clientul se deconectează sau 
    trimite QUIT.
    
    Args:
        socket_client: Socket-ul conectat la client
        adresa: Tuple (IP, port) al clientului
    """
    logger.info(f"Conexiune nouă de la {adresa[0]}:{adresa[1]}")
    buffer = b''
    
    try:
        while True:
            # Primire date
            date = socket_client.recv(DIMENSIUNE_BUFFER)
            if not date:
                logger.info(f"Client deconectat: {adresa[0]}:{adresa[1]}")
                break
            
            buffer += date
            
            # Procesare mesaje complete din buffer
            while buffer:
                lungime, continut, rest = parseaza_mesaj(buffer)
                
                if lungime is None:
                    break  # Mesaj incomplet, așteaptă mai multe date
                
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


# ═══════════════════════════════════════════════════════════════════════════════
# PORNIRE_SERVER
# Scop: Inițializează și pornește serverul TCP
# Transferabil la: Orice server TCP multi-threaded
# ═══════════════════════════════════════════════════════════════════════════════

def porneste_server() -> None:
    """
    Pornește serverul TEXT.
    
    Ascultă pe HOST:PORT și creează un thread nou pentru fiecare
    conexiune client. Rulează până la Ctrl+C.
    """
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
                args=(socket_client, adresa),
                daemon=True
            )
            thread.start()
            
    except KeyboardInterrupt:
        logger.info("Oprire server...")
    finally:
        server.close()
        logger.info("Server oprit.")


# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    porneste_server()
