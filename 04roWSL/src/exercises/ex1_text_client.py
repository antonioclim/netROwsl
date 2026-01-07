#!/usr/bin/env python3
"""
Exercițiu 1: Client Protocol TEXT
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Implementați un client pentru protocolul TEXT.

PROTOCOLUL TEXT:
    - Transport: TCP, port 5400
    - Format mesaj: <LUNGIME> <CONȚINUT>
    - Exemple:
        - "4 PING" -> răspuns: "4 PONG"
        - "15 SET cheie valoare" -> răspuns: "2 OK"
        - "8 GET cheie" -> răspuns: "<L> <valoare>"

INSTRUCȚIUNI:
    1. Completați funcțiile marcate cu TODO
    2. Testați cu serverul TEXT din laborator
    3. Capturați traficul cu Wireshark pentru analiză
"""

import socket

# Configurație
HOST = 'localhost'
PORT = 5400


def formateaza_mesaj(continut: str) -> bytes:
    """
    Formatează un mesaj conform protocolului TEXT.
    
    Args:
        continut: Conținutul mesajului (ex: "PING", "SET cheie val")
    
    Returns:
        Mesajul formatat ca bytes
    
    Exemplu:
        formateaza_mesaj("PING") -> b"4 PING"
    """
    # TODO: Implementați formatarea mesajului
    # Indiciu: lungimea conținutului + spațiu + conținutul
    pass


def parseaza_raspuns(date: bytes) -> str:
    """
    Parsează un răspuns de la server.
    
    Args:
        date: Răspunsul brut de la server
    
    Returns:
        Conținutul răspunsului (fără prefixul de lungime)
    
    Exemplu:
        parseaza_raspuns(b"4 PONG") -> "PONG"
    """
    # TODO: Implementați parsarea răspunsului
    # Indiciu: găsiți primul spațiu, extrageți lungimea și conținutul
    pass


def trimite_comanda(sock: socket.socket, comanda: str) -> str:
    """
    Trimite o comandă și primește răspunsul.
    
    Args:
        sock: Socket-ul conectat
        comanda: Comanda de trimis
    
    Returns:
        Răspunsul serverului
    """
    # TODO: Implementați trimiterea și recepția
    # Pași:
    # 1. Formatați mesajul
    # 2. Trimiteți prin sock.sendall()
    # 3. Primiți răspunsul cu sock.recv()
    # 4. Parsați și returnați răspunsul
    pass


def main():
    """Funcția principală - demonstrație client."""
    print("=" * 50)
    print("Client Protocol TEXT")
    print("=" * 50)
    
    # TODO: Implementați clientul
    # Pași sugerați:
    # 1. Creați socket TCP
    # 2. Conectați-vă la server
    # 3. Trimiteți PING și verificați PONG
    # 4. Testați SET, GET, DEL
    # 5. Închideți conexiunea
    
    print("\nImplementați clientul conform instrucțiunilor!")


if __name__ == "__main__":
    main()
