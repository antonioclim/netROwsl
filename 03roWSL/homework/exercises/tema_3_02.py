#!/usr/bin/env python3
"""
Tema 3.2: Aplicație Chat Multicast
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Autor: [Numele Complet]
Grupă: [Grupa]
Data: [Data]

Implementați o aplicație de chat bazată pe multicast care permite
comunicarea între mai mulți utilizatori în rețeaua locală.

Utilizare:
    python tema_3_02.py --username Alice
    python tema_3_02.py --username Bob --grup 239.0.0.10 --port 5010
"""

import socket
import struct
import sys
import json
import threading
import argparse
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAȚIE
# ═══════════════════════════════════════════════════════════════════════════

GRUP_MULTICAST = '239.0.0.10'
PORT_MULTICAST = 5010
DIMENSIUNE_BUFFER = 4096


# ═══════════════════════════════════════════════════════════════════════════
# PROTOCOL MESAJE
# ═══════════════════════════════════════════════════════════════════════════

class TipMesaj(Enum):
    """Tipurile de mesaje suportate de protocol."""
    JOIN = "JOIN"
    MESSAGE = "MESSAGE"
    LEAVE = "LEAVE"


@dataclass
class MesajChat:
    """Structura unui mesaj de chat."""
    
    tip: str
    utilizator: str
    text: str = ""
    timestamp: str = ""
    
    def __post_init__(self):
        """Setează timestamp-ul dacă nu este furnizat."""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_json(self) -> str:
        """
        Serializează mesajul în format JSON.
        
        TODO: Implementați această metodă
        
        Returns:
            String JSON reprezentând mesajul
        """
        # TODO: Returnați reprezentarea JSON a mesajului
        # Hint: json.dumps(asdict(self))
        pass
        return "{}"
    
    @classmethod
    def from_json(cls, date_json: str) -> Optional['MesajChat']:
        """
        Deserializează un mesaj din format JSON.
        
        TODO: Implementați această metodă
        
        Args:
            date_json: String JSON
            
        Returns:
            Instanță MesajChat sau None dacă parsing-ul eșuează
        """
        # TODO: Parsați JSON-ul și creați instanța
        # Hint: data = json.loads(date_json)
        #       return cls(**data)
        pass
        return None
    
    @classmethod
    def creaza_join(cls, utilizator: str) -> 'MesajChat':
        """Creează un mesaj de intrare în chat."""
        return cls(tip=TipMesaj.JOIN.value, utilizator=utilizator)
    
    @classmethod
    def creaza_mesaj(cls, utilizator: str, text: str) -> 'MesajChat':
        """Creează un mesaj normal de chat."""
        return cls(tip=TipMesaj.MESSAGE.value, utilizator=utilizator, text=text)
    
    @classmethod
    def creaza_leave(cls, utilizator: str) -> 'MesajChat':
        """Creează un mesaj de părăsire."""
        return cls(tip=TipMesaj.LEAVE.value, utilizator=utilizator)


# ═══════════════════════════════════════════════════════════════════════════
# APLICAȚIE CHAT MULTICAST
# ═══════════════════════════════════════════════════════════════════════════

class ChatMulticast:
    """Aplicație de chat bazată pe multicast UDP."""
    
    def __init__(
        self,
        username: str,
        grup: str = GRUP_MULTICAST,
        port: int = PORT_MULTICAST
    ):
        """
        Inițializează aplicația de chat.
        
        Args:
            username: Numele utilizatorului
            grup: Adresa grupului multicast
            port: Portul pentru comunicare
        """
        self.username = username
        self.grup = grup
        self.port = port
        self.activ = False
        
        # Socket-uri
        self.sock_trimitere: Optional[socket.socket] = None
        self.sock_receptie: Optional[socket.socket] = None
    
    def _configureaza_socket_trimitere(self) -> None:
        """
        Configurează socket-ul pentru trimitere multicast.
        
        TODO: Implementați această metodă
        """
        self.sock_trimitere = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # TODO: Setați TTL pentru multicast
        # Hint: sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        pass
    
    def _configureaza_socket_receptie(self) -> None:
        """
        Configurează socket-ul pentru recepție multicast.
        
        TODO: Implementați această metodă
        """
        self.sock_receptie = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # TODO: Setați SO_REUSEADDR
        pass
        
        # TODO: Legați socket-ul la port
        # Hint: sock.bind(('', self.port))
        pass
        
        # TODO: Alăturați-vă grupului multicast
        # Hint: mreq = struct.pack('4s4s', ...)
        #       sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        pass
    
    def _trimite_mesaj(self, mesaj: MesajChat) -> None:
        """
        Trimite un mesaj către grupul multicast.
        
        TODO: Implementați această metodă
        
        Args:
            mesaj: Mesajul de trimis
        """
        # TODO: Serializați și trimiteți mesajul
        # Hint: date = mesaj.to_json().encode('utf-8')
        #       self.sock_trimitere.sendto(date, (self.grup, self.port))
        pass
    
    def _formateaza_afisare(self, mesaj: MesajChat) -> str:
        """
        Formatează un mesaj pentru afișare.
        
        TODO: Implementați această metodă
        
        Args:
            mesaj: Mesajul de formatat
            
        Returns:
            String formatat pentru afișare în consolă
        """
        # TODO: Formatați mesajul în funcție de tip
        # JOIN: "[10:30:05] >>> Alice a intrat în chat"
        # MESSAGE: "[10:30:10] Alice: Salut tuturor!"
        # LEAVE: "[10:30:15] <<< Alice a părăsit chat-ul"
        pass
        return ""
    
    def _bucla_receptie(self) -> None:
        """
        Bucla de recepție a mesajelor (rulează într-un thread separat).
        
        TODO: Implementați această metodă
        """
        while self.activ:
            try:
                # TODO: Setați timeout pentru a permite oprirea
                self.sock_receptie.settimeout(1.0)
                
                # TODO: Primiți date
                # date, adresa = self.sock_receptie.recvfrom(DIMENSIUNE_BUFFER)
                pass
                
                # TODO: Deserializați mesajul
                # mesaj = MesajChat.from_json(date.decode('utf-8'))
                pass
                
                # TODO: Ignorați propriile mesaje
                # if mesaj and mesaj.utilizator != self.username:
                pass
                
                # TODO: Afișați mesajul formatat
                pass
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.activ:
                    print(f"Eroare recepție: {e}")
    
    def _bucla_input(self) -> None:
        """
        Bucla principală pentru input utilizator.
        
        TODO: Implementați această metodă
        """
        print("\nScrieți mesajul și apăsați Enter. '/quit' pentru a ieși.\n")
        
        while self.activ:
            try:
                # TODO: Citiți input de la utilizator
                # text = input()
                pass
                
                # TODO: Verificați comanda de ieșire
                # if text.lower() == '/quit':
                pass
                
                # TODO: Creați și trimiteți mesajul
                # if text.strip():
                #     mesaj = MesajChat.creaza_mesaj(self.username, text)
                #     self._trimite_mesaj(mesaj)
                pass
                
            except EOFError:
                break
            except Exception as e:
                print(f"Eroare: {e}")
    
    def _anunta_intrare(self) -> None:
        """Trimite mesaj de intrare în chat."""
        mesaj = MesajChat.creaza_join(self.username)
        self._trimite_mesaj(mesaj)
    
    def _anunta_plecare(self) -> None:
        """Trimite mesaj de părăsire."""
        mesaj = MesajChat.creaza_leave(self.username)
        self._trimite_mesaj(mesaj)
    
    def porneste(self) -> None:
        """
        Pornește aplicația de chat.
        
        TODO: Completați implementarea
        """
        print("=" * 50)
        print("CHAT MULTICAST")
        print("=" * 50)
        print(f"Utilizator: {self.username}")
        print(f"Grup: {self.grup}:{self.port}")
        print("-" * 50)
        
        # Configurare socket-uri
        self._configureaza_socket_trimitere()
        self._configureaza_socket_receptie()
        
        self.activ = True
        
        # TODO: Anunțați intrarea în chat
        self._anunta_intrare()
        
        # TODO: Porniți thread-ul de recepție
        # thread_receptie = threading.Thread(target=self._bucla_receptie, daemon=True)
        # thread_receptie.start()
        pass
        
        try:
            # Bucla principală de input
            self._bucla_input()
        finally:
            self.opreste()
    
    def opreste(self) -> None:
        """Oprește aplicația de chat."""
        if self.activ:
            self.activ = False
            
            # Anunță plecarea
            self._anunta_plecare()
            
            # Închide socket-urile
            if self.sock_trimitere:
                self.sock_trimitere.close()
            if self.sock_receptie:
                self.sock_receptie.close()
            
            print("\n" + "-" * 50)
            print("Chat închis.")


# ═══════════════════════════════════════════════════════════════════════════
# PUNCT DE INTRARE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description='Aplicație Chat Multicast'
    )
    parser.add_argument(
        '--username', '-u',
        type=str,
        required=True,
        help='Numele de utilizator'
    )
    parser.add_argument(
        '--grup', '-g',
        type=str,
        default=GRUP_MULTICAST,
        help=f'Adresa grupului multicast (implicit: {GRUP_MULTICAST})'
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=PORT_MULTICAST,
        help=f'Portul (implicit: {PORT_MULTICAST})'
    )
    args = parser.parse_args()
    
    chat = ChatMulticast(
        username=args.username,
        grup=args.grup,
        port=args.port
    )
    chat.porneste()


if __name__ == '__main__':
    main()
