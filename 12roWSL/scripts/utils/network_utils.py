#!/usr/bin/env python3
"""
Utilitare de Rețea
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Clase helper pentru testarea protocoalelor SMTP și RPC.
"""

import socket
import json
import time
from typing import Any, Dict, List, Optional
from xmlrpc.client import ServerProxy

from .logger import configureaza_logger

logger = configureaza_logger("network_utils")


class TesterSMTP:
    """Clasă pentru testarea dialogurilor SMTP."""
    
    def __init__(self, host: str = "localhost", port: int = 1025, timeout: float = 10.0):
        """
        Inițializează testerul SMTP.
        
        Args:
            host: Adresa serverului SMTP
            port: Portul serverului
            timeout: Timeout pentru operații
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
    
    def conecteaza(self) -> str:
        """
        Stabilește conexiunea cu serverul SMTP.
        
        Returns:
            Banner-ul de salut al serverului
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.socket.connect((self.host, self.port))
        
        # Primire banner inițial
        raspuns = self._primeste_raspuns()
        logger.debug(f"Banner SMTP: {raspuns}")
        return raspuns
    
    def _primeste_raspuns(self) -> str:
        """Primește răspunsul de la server."""
        date = b""
        while True:
            parte = self.socket.recv(1024)
            date += parte
            if b"\r\n" in date or len(parte) < 1024:
                break
        return date.decode("utf-8").strip()
    
    def trimite_comanda(self, comanda: str) -> str:
        """
        Trimite o comandă SMTP și primește răspunsul.
        
        Args:
            comanda: Comanda SMTP de trimis
        
        Returns:
            Răspunsul serverului
        """
        logger.debug(f"Trimitere: {comanda}")
        self.socket.send(f"{comanda}\r\n".encode("utf-8"))
        raspuns = self._primeste_raspuns()
        logger.debug(f"Răspuns: {raspuns}")
        return raspuns
    
    def trimite_date(self, date: str) -> str:
        """
        Trimite date (conținutul mesajului).
        
        Args:
            date: Datele de trimis (terminat cu \\r\\n.\\r\\n)
        
        Returns:
            Răspunsul serverului
        """
        # Asigurare terminare corectă
        if not date.endswith("\r\n.\r\n"):
            if date.endswith("\n.\n"):
                date = date.replace("\n.\n", "\r\n.\r\n")
            elif date.endswith("."):
                date = date + "\r\n"
            else:
                date = date + "\r\n.\r\n"
        
        logger.debug(f"Trimitere date: {len(date)} bytes")
        self.socket.send(date.encode("utf-8"))
        raspuns = self._primeste_raspuns()
        logger.debug(f"Răspuns: {raspuns}")
        return raspuns
    
    def deconecteaza(self):
        """Închide conexiunea."""
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
            self.socket = None


class TesterJSONRPC:
    """Clasă pentru testarea apelurilor JSON-RPC 2.0."""
    
    def __init__(self, host: str = "localhost", port: int = 6200, timeout: float = 10.0):
        """
        Inițializează testerul JSON-RPC.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
            timeout: Timeout pentru cereri
        """
        self.url = f"http://{host}:{port}"
        self.timeout = timeout
        self._id_cerere = 0
    
    def _urmatorul_id(self) -> int:
        """Generează următorul ID de cerere."""
        self._id_cerere += 1
        return self._id_cerere
    
    def apeleaza(self, metoda: str, parametri: Any = None) -> Any:
        """
        Efectuează un apel JSON-RPC.
        
        Args:
            metoda: Numele metodei
            parametri: Parametrii apelului (list sau dict)
        
        Returns:
            Rezultatul apelului
        
        Raises:
            Exception: Dacă apelul returnează o eroare
        """
        import urllib.request
        
        cerere = {
            "jsonrpc": "2.0",
            "method": metoda,
            "id": self._urmatorul_id()
        }
        
        if parametri is not None:
            cerere["params"] = parametri
        
        date = json.dumps(cerere).encode("utf-8")
        
        req = urllib.request.Request(
            self.url,
            data=date,
            headers={"Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as raspuns:
                rezultat = json.loads(raspuns.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            rezultat = json.loads(e.read().decode("utf-8"))
        
        if "error" in rezultat:
            eroare = rezultat["error"]
            raise Exception(f"Eroare JSON-RPC {eroare.get('code')}: {eroare.get('message')}")
        
        return rezultat.get("result")
    
    def apel_lot(self, cereri: List[Dict]) -> List[Any]:
        """
        Efectuează un apel în lot (batch).
        
        Args:
            cereri: Lista de cereri (fiecare cu 'method' și opțional 'params')
        
        Returns:
            Lista de rezultate
        """
        import urllib.request
        
        cereri_complete = []
        for c in cereri:
            cerere = {
                "jsonrpc": "2.0",
                "method": c["method"],
                "id": self._urmatorul_id()
            }
            if "params" in c:
                cerere["params"] = c["params"]
            cereri_complete.append(cerere)
        
        date = json.dumps(cereri_complete).encode("utf-8")
        
        req = urllib.request.Request(
            self.url,
            data=date,
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=self.timeout) as raspuns:
            rezultate = json.loads(raspuns.read().decode("utf-8"))
        
        return [r.get("result") if "result" in r else r.get("error") for r in rezultate]


class TesterXMLRPC:
    """Clasă pentru testarea apelurilor XML-RPC."""
    
    def __init__(self, host: str = "localhost", port: int = 6201):
        """
        Inițializează testerul XML-RPC.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
        """
        self.url = f"http://{host}:{port}"
        self._proxy = None
    
    @property
    def proxy(self) -> ServerProxy:
        """Returnează proxy-ul XML-RPC (creat la cerere)."""
        if self._proxy is None:
            self._proxy = ServerProxy(self.url, allow_none=True)
        return self._proxy


def verifica_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Verifică dacă un port este accesibil.
    
    Args:
        host: Adresa de verificat
        port: Portul de verificat
        timeout: Timeout în secunde
    
    Returns:
        True dacă portul răspunde
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            rezultat = s.connect_ex((host, port))
            return rezultat == 0
    except Exception:
        return False


def asteapta_port(host: str, port: int, timeout: float = 30.0, interval: float = 1.0) -> bool:
    """
    Așteaptă ca un port să devină disponibil.
    
    Args:
        host: Adresa de verificat
        port: Portul de verificat
        timeout: Timeout total în secunde
        interval: Interval între verificări
    
    Returns:
        True dacă portul a devenit disponibil
    """
    timp_start = time.time()
    
    while time.time() - timp_start < timeout:
        if verifica_port(host, port, timeout=2.0):
            return True
        time.sleep(interval)
    
    return False
