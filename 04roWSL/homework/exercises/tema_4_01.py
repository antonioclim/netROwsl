#!/usr/bin/env python3
"""
Tema 4.01: Protocol TEXT Extins
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Extindeți clientul protocolului TEXT cu funcționalități suplimentare.

CERINȚE:
    1. Implementați comenzile suplimentare (EXPIRE, TTL, INCR, DECR)
    2. Adăugați logging pentru toate operațiunile
    3. Implementați reconectare automată
    4. Adăugați suport pentru comenzi din fișier batch

INSTRUCȚIUNI:
    - Completați funcțiile marcate cu TODO
    - Nu modificați semnăturile funcțiilor existente
    - Adăugați comentarii explicative pentru codul vostru
    - Testați implementarea cu serverul TEXT din laborator

PUNCTAJ: 25 puncte
"""

import socket
import logging
import time
from typing import Optional, List

# TODO: Configurați logging-ul
# Indiciu: Folosiți logging.basicConfig() cu format și nivel corespunzător
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClientTEXTExtins:
    """
    Client extins pentru protocolul TEXT.
    
    Această clasă extinde funcționalitatea clientului TEXT de bază
    cu comenzi suplimentare și caracteristici avansate.
    """
    
    def __init__(self, host: str = 'localhost', port: int = 5400):
        """
        Inițializează clientul.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
        """
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.conectat = False
        self.timeout = 10.0
        self.incercari_reconectare = 3
    
    def conecteaza(self) -> bool:
        """
        Stabilește conexiunea la server.
        
        Returns:
            True dacă conexiunea a reușit
        """
        # TODO: Implementați conectarea la server
        # Indiciu:
        # 1. Creați un socket TCP
        # 2. Setați timeout-ul
        # 3. Conectați-vă la (self.host, self.port)
        # 4. Logați succesul sau eșecul
        # 5. Actualizați self.conectat
        pass
    
    def deconecteaza(self):
        """Închide conexiunea."""
        # TODO: Implementați deconectarea
        # Indiciu: Închideți socket-ul și actualizați self.conectat
        pass
    
    def _reconecteaza(self) -> bool:
        """
        Încearcă reconectarea automată.
        
        Returns:
            True dacă reconectarea a reușit
        """
        # TODO: Implementați reconectarea automată
        # Indiciu:
        # 1. Încercați de self.incercari_reconectare ori
        # 2. Așteptați între încercări (ex: 1 secundă)
        # 3. Logați fiecare încercare
        pass
    
    def _formateaza_mesaj(self, continut: str) -> bytes:
        """
        Formatează un mesaj pentru trimitere.
        
        Args:
            continut: Conținutul mesajului
        
        Returns:
            Mesaj formatat ca bytes
        """
        # TODO: Implementați formatarea mesajului
        # Format: <LUNGIME> <CONȚINUT>
        pass
    
    def _parseaza_raspuns(self, date: bytes) -> str:
        """
        Parsează răspunsul serverului.
        
        Args:
            date: Răspunsul brut
        
        Returns:
            Conținutul răspunsului
        """
        # TODO: Implementați parsarea răspunsului
        pass
    
    def _trimite_comanda(self, comanda: str) -> Optional[str]:
        """
        Trimite o comandă și primește răspunsul.
        
        Încorporează reconectare automată în caz de eroare.
        
        Args:
            comanda: Comanda de trimis
        
        Returns:
            Răspunsul serverului sau None în caz de eroare
        """
        # TODO: Implementați trimiterea comenzii cu reconectare
        # Indiciu:
        # 1. Verificați conexiunea
        # 2. Formatați și trimiteți mesajul
        # 3. Așteptați și parsați răspunsul
        # 4. În caz de eroare, încercați reconectarea
        # 5. Logați operațiunea
        pass
    
    # =========================================================
    # Comenzi de bază
    # =========================================================
    
    def ping(self) -> bool:
        """Verifică conectivitatea cu serverul."""
        raspuns = self._trimite_comanda("PING")
        return raspuns == "PONG"
    
    def seteaza(self, cheie: str, valoare: str) -> bool:
        """Setează o valoare pentru o cheie."""
        raspuns = self._trimite_comanda(f"SET {cheie} {valoare}")
        return raspuns == "OK"
    
    def obtine(self, cheie: str) -> Optional[str]:
        """Obține valoarea unei chei."""
        raspuns = self._trimite_comanda(f"GET {cheie}")
        if raspuns and not raspuns.startswith("ERR"):
            return raspuns
        return None
    
    def sterge(self, cheie: str) -> bool:
        """Șterge o cheie."""
        raspuns = self._trimite_comanda(f"DEL {cheie}")
        return raspuns == "OK"
    
    # =========================================================
    # Comenzi extinse (DE IMPLEMENTAT)
    # =========================================================
    
    def expire(self, cheie: str, secunde: int) -> bool:
        """
        Setează un TTL (Time To Live) pentru o cheie.
        
        NOTĂ: Serverul actual nu suportă această comandă nativ.
        Implementați logica pe partea de client.
        
        Args:
            cheie: Cheia pentru care se setează TTL
            secunde: Durata în secunde până la expirare
        
        Returns:
            True dacă operațiunea a reușit
        """
        # TODO: Implementați EXPIRE
        # Indiciu: Puteți stoca timestamp-urile de expirare într-un dicționar local
        pass
    
    def ttl(self, cheie: str) -> int:
        """
        Returnează timpul rămas până la expirarea unei chei.
        
        Args:
            cheie: Cheia de verificat
        
        Returns:
            Secunde rămase, -1 dacă nu expiră, -2 dacă nu există
        """
        # TODO: Implementați TTL
        pass
    
    def incr(self, cheie: str) -> Optional[int]:
        """
        Incrementează valoarea unei chei numerice.
        
        Args:
            cheie: Cheia de incrementat
        
        Returns:
            Noua valoare sau None dacă eroare
        """
        # TODO: Implementați INCR
        # Indiciu:
        # 1. Obțineți valoarea curentă
        # 2. Convertiți la int și incrementați
        # 3. Salvați noua valoare
        pass
    
    def decr(self, cheie: str) -> Optional[int]:
        """
        Decrementează valoarea unei chei numerice.
        
        Args:
            cheie: Cheia de decrementat
        
        Returns:
            Noua valoare sau None dacă eroare
        """
        # TODO: Implementați DECR
        pass
    
    # =========================================================
    # Funcționalități suplimentare
    # =========================================================
    
    def executa_batch(self, cale_fisier: str) -> List[str]:
        """
        Execută comenzi dintr-un fișier batch.
        
        Formatul fișierului: o comandă pe linie
        Liniile goale și cele care încep cu # sunt ignorate.
        
        Args:
            cale_fisier: Calea către fișierul batch
        
        Returns:
            Lista răspunsurilor pentru fiecare comandă
        """
        # TODO: Implementați execuția batch
        # Indiciu:
        # 1. Citiți fișierul linie cu linie
        # 2. Ignorați comentariile și liniile goale
        # 3. Executați fiecare comandă
        # 4. Colectați și returnați răspunsurile
        pass


def test_client():
    """Funcție de test pentru client."""
    print("=" * 50)
    print("Test Client TEXT Extins")
    print("=" * 50)
    
    client = ClientTEXTExtins()
    
    # TODO: Adăugați teste pentru funcționalitățile implementate
    # Exemplu:
    # if client.conecteaza():
    #     print("✅ Conectat cu succes")
    #     
    #     if client.ping():
    #         print("✅ PING reușit")
    #     
    #     # Testați celelalte funcții...
    #     
    #     client.deconecteaza()
    
    print("\nImplementați testele pentru funcționalitățile voastre!")


if __name__ == "__main__":
    test_client()
