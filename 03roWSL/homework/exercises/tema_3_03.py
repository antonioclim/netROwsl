#!/usr/bin/env python3
"""
Tema 3.3: Tunel TCP cu Logging și Metrici
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Autor: [Numele Complet]
Grupă: [Grupa]
Data: [Data]

Îmbunătățiți tunelul TCP cu sistem de logging, metrici de performanță
și gestionare avansată a conexiunilor.

Utilizare:
    python tema_3_03.py --port-ascultare 9090 --host-tinta localhost --port-tinta 8080
    python tema_3_03.py -l 9090 -H localhost -P 8080 --max-conexiuni 10 --log-file tunel.log
"""

import socket
import sys
import threading
import argparse
import logging
import signal
import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAȚIE
# ═══════════════════════════════════════════════════════════════════════════

PORT_ASCULTARE = 9090
HOST_TINTA = 'localhost'
PORT_TINTA = 8080
MAX_CONEXIUNI = 100
TIMEOUT_INACTIV = 300  # secunde
DIMENSIUNE_BUFFER = 4096


# ═══════════════════════════════════════════════════════════════════════════
# STRUCTURI DE DATE
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class StatisticiConexiune:
    """Statistici pentru o conexiune individuală."""
    
    id_conexiune: int
    timp_start: float = field(default_factory=time.time)
    bytes_client_server: int = 0
    bytes_server_client: int = 0
    ultima_activitate: float = field(default_factory=time.time)
    
    def calculeaza_durata(self) -> float:
        """
        Calculează durata conexiunii.
        
        TODO: Implementați această metodă
        
        Returns:
            Durata în secunde
        """
        # Hint: return time.time() - self.timp_start
        pass
        return 0.0
    
    def calculeaza_throughput(self) -> float:
        """
        Calculează throughput-ul mediu.
        
        TODO: Implementați această metodă
        
        Returns:
            Bytes pe secundă (ambele direcții)
        """
        # TODO: Calculați throughput-ul
        pass
        return 0.0
    
    def este_inactiva(self, timeout: float) -> bool:
        """
        Verifică dacă conexiunea este inactivă.
        
        TODO: Implementați această metodă
        
        Args:
            timeout: Timeout de inactivitate în secunde
            
        Returns:
            True dacă conexiunea este inactivă
        """
        # Hint: return (time.time() - self.ultima_activitate) > timeout
        pass
        return False
    
    def formateaza_log(self) -> str:
        """Formatează statisticile pentru logging."""
        return (
            f"Conexiune #{self.id_conexiune}: "
            f"Durata={self.calculeaza_durata():.2f}s, "
            f"C→S={self.bytes_client_server}B, "
            f"S→C={self.bytes_server_client}B, "
            f"Throughput={self.calculeaza_throughput():.2f}B/s"
        )


@dataclass
class StatisticiTunel:
    """Statistici globale pentru tunel."""
    
    timp_start: float = field(default_factory=time.time)
    total_conexiuni: int = 0
    conexiuni_active: int = 0
    max_conexiuni_simultane: int = 0
    total_bytes_transferati: int = 0
    conexiuni: Dict[int, StatisticiConexiune] = field(default_factory=dict)
    lock: threading.Lock = field(default_factory=threading.Lock)
    
    def inregistreaza_conexiune_noua(self, id_conexiune: int) -> StatisticiConexiune:
        """
        Înregistrează o nouă conexiune.
        
        TODO: Implementați această metodă
        
        Args:
            id_conexiune: ID-ul conexiunii
            
        Returns:
            Instanță StatisticiConexiune pentru conexiunea nouă
        """
        # TODO: Creați statistici pentru conexiune
        # TODO: Actualizați contoarele
        # TODO: Actualizați max_conexiuni_simultane dacă e cazul
        pass
        return StatisticiConexiune(id_conexiune=id_conexiune)
    
    def inregistreaza_conexiune_inchisa(self, id_conexiune: int) -> None:
        """
        Înregistrează închiderea unei conexiuni.
        
        TODO: Implementați această metodă
        
        Args:
            id_conexiune: ID-ul conexiunii închise
        """
        # TODO: Decrementați conexiuni_active
        # TODO: Actualizați total_bytes_transferati
        pass
    
    def calculeaza_uptime(self) -> float:
        """Calculează uptime-ul tunelului."""
        return time.time() - self.timp_start
    
    def formateaza_sumar(self) -> str:
        """
        Formatează sumarul statisticilor.
        
        TODO: Implementați această metodă
        
        Returns:
            String formatat cu statisticile
        """
        # TODO: Construiți sumarul statisticilor
        pass
        return "TODO: Implementați sumarul"


# ═══════════════════════════════════════════════════════════════════════════
# LOGGER TUNEL
# ═══════════════════════════════════════════════════════════════════════════

class LoggerTunel:
    """Sistem de logging pentru tunel."""
    
    def __init__(self, fisier_log: Optional[str] = None, nivel_debug: bool = False):
        """
        Inițializează sistemul de logging.
        
        Args:
            fisier_log: Calea fișierului de log (opțional)
            nivel_debug: True pentru logging la nivel DEBUG
        """
        self.logger = logging.getLogger('TunelTCP')
        self.logger.setLevel(logging.DEBUG if nivel_debug else logging.INFO)
        
        # Format
        format_log = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler consolă
        handler_consola = logging.StreamHandler()
        handler_consola.setFormatter(format_log)
        self.logger.addHandler(handler_consola)
        
        # Handler fișier (dacă este specificat)
        if fisier_log:
            handler_fisier = logging.FileHandler(fisier_log, encoding='utf-8')
            handler_fisier.setFormatter(format_log)
            self.logger.addHandler(handler_fisier)
    
    def log_conexiune(self, id_conexiune: int, mesaj: str, nivel: str = 'INFO') -> None:
        """
        Loghează un mesaj cu context de conexiune.
        
        Args:
            id_conexiune: ID-ul conexiunii
            mesaj: Mesajul de logat
            nivel: Nivelul de logging
        """
        mesaj_complet = f"[Conn-{id_conexiune:04d}] {mesaj}"
        
        if nivel == 'DEBUG':
            self.logger.debug(mesaj_complet)
        elif nivel == 'WARNING':
            self.logger.warning(mesaj_complet)
        elif nivel == 'ERROR':
            self.logger.error(mesaj_complet)
        else:
            self.logger.info(mesaj_complet)


# ═══════════════════════════════════════════════════════════════════════════
# TUNEL TCP CU METRICI
# ═══════════════════════════════════════════════════════════════════════════

class TunelTCPCuMetrici:
    """Tunel TCP îmbunătățit cu logging și metrici."""
    
    def __init__(
        self,
        port_ascultare: int,
        host_tinta: str,
        port_tinta: int,
        max_conexiuni: int = MAX_CONEXIUNI,
        timeout: int = TIMEOUT_INACTIV,
        logger: Optional[LoggerTunel] = None
    ):
        """
        Inițializează tunelul.
        
        Args:
            port_ascultare: Portul pe care tunelul ascultă
            host_tinta: Adresa serverului țintă
            port_tinta: Portul serverului țintă
            max_conexiuni: Numărul maxim de conexiuni simultane
            timeout: Timeout pentru conexiuni inactive
            logger: Instanță LoggerTunel
        """
        self.port_ascultare = port_ascultare
        self.host_tinta = host_tinta
        self.port_tinta = port_tinta
        self.max_conexiuni = max_conexiuni
        self.timeout = timeout
        self.logger = logger or LoggerTunel()
        
        self.socket_server: Optional[socket.socket] = None
        self.activ = False
        self.contor_conexiuni = 0
        self.lock = threading.Lock()
        
        self.statistici = StatisticiTunel()
        
        # Handler pentru semnale
        signal.signal(signal.SIGINT, self._handler_oprire)
        # SIGUSR1 pentru afișare status (doar pe Unix)
        try:
            signal.signal(signal.SIGUSR1, self._handler_status)
        except AttributeError:
            pass  # Windows nu are SIGUSR1
    
    def _handler_oprire(self, sig, frame) -> None:
        """Handler pentru oprire (Ctrl+C)."""
        self.logger.logger.info("Oprire inițiată...")
        self.activ = False
    
    def _handler_status(self, sig, frame) -> None:
        """Handler pentru afișare status (SIGUSR1)."""
        print("\n" + self.statistici.formateaza_sumar() + "\n")
    
    def _genereaza_id_conexiune(self) -> int:
        """Generează un ID unic pentru conexiune."""
        with self.lock:
            self.contor_conexiuni += 1
            return self.contor_conexiuni
    
    def _verifica_limita_conexiuni(self) -> bool:
        """
        Verifică dacă limita de conexiuni a fost atinsă.
        
        TODO: Implementați această metodă
        
        Returns:
            True dacă se pot accepta conexiuni noi
        """
        # TODO: Verificați dacă conexiuni_active < max_conexiuni
        pass
        return True
    
    def _relay_bidirecțional(
        self,
        sursa: socket.socket,
        destinatie: socket.socket,
        directie: str,
        id_conexiune: int,
        stats: StatisticiConexiune
    ) -> None:
        """
        Relayează date între două socket-uri.
        
        TODO: Implementați această metodă
        
        Args:
            sursa: Socket-ul de citire
            destinatie: Socket-ul de scriere
            directie: Descriere pentru logging
            id_conexiune: ID-ul conexiunii
            stats: Statisticile conexiunii
        """
        try:
            while self.activ:
                # TODO: Primiți date de la sursă
                # date = sursa.recv(DIMENSIUNE_BUFFER)
                pass
                
                # TODO: Verificați dacă conexiunea s-a închis
                # if not date:
                #     break
                pass
                
                # TODO: Trimiteți date către destinație
                # destinatie.sendall(date)
                pass
                
                # TODO: Actualizați statisticile
                # if directie == "client→server":
                #     stats.bytes_client_server += len(date)
                # else:
                #     stats.bytes_server_client += len(date)
                # stats.ultima_activitate = time.time()
                pass
                
                # TODO: Logați transferul (opțional, la nivel DEBUG)
                pass
                
        except Exception as e:
            self.logger.log_conexiune(id_conexiune, f"{directie}: {e}", 'ERROR')
        finally:
            try:
                sursa.shutdown(socket.SHUT_RD)
            except Exception:
                pass
            try:
                destinatie.shutdown(socket.SHUT_WR)
            except Exception:
                pass
    
    def _gestioneaza_conexiune(
        self,
        socket_client: socket.socket,
        adresa_client: tuple,
        id_conexiune: int
    ) -> None:
        """
        Gestionează o conexiune client.
        
        TODO: Completați implementarea
        
        Args:
            socket_client: Socket-ul conexiunii client
            adresa_client: Adresa clientului
            id_conexiune: ID-ul conexiunii
        """
        ip_client, port_client = adresa_client
        self.logger.log_conexiune(
            id_conexiune,
            f"Nouă conexiune de la {ip_client}:{port_client}"
        )
        
        # Înregistrează statistici
        stats = self.statistici.inregistreaza_conexiune_noua(id_conexiune)
        
        socket_server = None
        
        try:
            # TODO: Conectați-vă la serverul țintă
            # socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # socket_server.settimeout(10)
            # socket_server.connect((self.host_tinta, self.port_tinta))
            # socket_server.settimeout(self.timeout)
            pass
            
            self.logger.log_conexiune(
                id_conexiune,
                f"Conectat la {self.host_tinta}:{self.port_tinta}"
            )
            
            # TODO: Porniți thread-uri pentru relay bidirecțional
            # thread1 = threading.Thread(target=self._relay_bidirecțional, ...)
            # thread2 = threading.Thread(target=self._relay_bidirecțional, ...)
            pass
            
            # TODO: Așteptați terminarea thread-urilor
            pass
            
        except ConnectionRefusedError:
            self.logger.log_conexiune(
                id_conexiune,
                f"Conexiune refuzată de {self.host_tinta}:{self.port_tinta}",
                'ERROR'
            )
        except socket.timeout:
            self.logger.log_conexiune(id_conexiune, "Timeout", 'WARNING')
        except Exception as e:
            self.logger.log_conexiune(id_conexiune, f"Eroare: {e}", 'ERROR')
        finally:
            # Curățare
            try:
                socket_client.close()
            except Exception:
                pass
            if socket_server:
                try:
                    socket_server.close()
                except Exception:
                    pass
            
            # Înregistrează închiderea
            self.statistici.inregistreaza_conexiune_inchisa(id_conexiune)
            self.logger.log_conexiune(id_conexiune, stats.formateaza_log())
    
    def porneste(self) -> None:
        """Pornește tunelul TCP."""
        print("=" * 60)
        print("TUNEL TCP CU LOGGING ȘI METRICI")
        print("=" * 60)
        print(f"Ascultare pe: 0.0.0.0:{self.port_ascultare}")
        print(f"Redirecționare către: {self.host_tinta}:{self.port_tinta}")
        print(f"Max conexiuni: {self.max_conexiuni}")
        print(f"Timeout inactivitate: {self.timeout}s")
        print("Apăsați Ctrl+C pentru oprire")
        print("-" * 60)
        
        # Creează socket-ul de ascultare
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind(('0.0.0.0', self.port_ascultare))
        self.socket_server.listen(5)
        
        self.activ = True
        self.logger.logger.info("Tunel pornit")
        
        try:
            while self.activ:
                try:
                    self.socket_server.settimeout(1.0)
                    socket_client, adresa_client = self.socket_server.accept()
                    
                    # Verifică limita de conexiuni
                    if not self._verifica_limita_conexiuni():
                        self.logger.logger.warning("Limita de conexiuni atinsă")
                        socket_client.close()
                        continue
                    
                    id_conexiune = self._genereaza_id_conexiune()
                    
                    # Gestionează în thread separat
                    thread = threading.Thread(
                        target=self._gestioneaza_conexiune,
                        args=(socket_client, adresa_client, id_conexiune),
                        daemon=True
                    )
                    thread.start()
                    
                except socket.timeout:
                    continue
                    
        except Exception as e:
            self.logger.logger.error(f"Eroare fatală: {e}")
        finally:
            self.opreste()
    
    def opreste(self) -> None:
        """Oprește tunelul."""
        self.activ = False
        
        if self.socket_server:
            try:
                self.socket_server.close()
            except Exception:
                pass
        
        # Afișează statisticile finale
        print("\n" + "=" * 60)
        print("STATISTICI FINALE")
        print("=" * 60)
        print(self.statistici.formateaza_sumar())
        self.logger.logger.info("Tunel oprit")


# ═══════════════════════════════════════════════════════════════════════════
# PUNCT DE INTRARE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description='Tunel TCP cu Logging și Metrici'
    )
    parser.add_argument(
        '--port-ascultare', '-l',
        type=int,
        default=PORT_ASCULTARE,
        help=f'Portul de ascultare (implicit: {PORT_ASCULTARE})'
    )
    parser.add_argument(
        '--host-tinta', '-H',
        type=str,
        default=HOST_TINTA,
        help=f'Host-ul țintă (implicit: {HOST_TINTA})'
    )
    parser.add_argument(
        '--port-tinta', '-P',
        type=int,
        default=PORT_TINTA,
        help=f'Portul țintă (implicit: {PORT_TINTA})'
    )
    parser.add_argument(
        '--max-conexiuni', '-m',
        type=int,
        default=MAX_CONEXIUNI,
        help=f'Numărul maxim de conexiuni simultane (implicit: {MAX_CONEXIUNI})'
    )
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=TIMEOUT_INACTIV,
        help=f'Timeout inactivitate în secunde (implicit: {TIMEOUT_INACTIV})'
    )
    parser.add_argument(
        '--log-file', '-f',
        type=str,
        default=None,
        help='Fișier pentru log-uri (opțional)'
    )
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Activează logging la nivel DEBUG'
    )
    args = parser.parse_args()
    
    logger = LoggerTunel(
        fisier_log=args.log_file,
        nivel_debug=args.debug
    )
    
    tunel = TunelTCPCuMetrici(
        port_ascultare=args.port_ascultare,
        host_tinta=args.host_tinta,
        port_tinta=args.port_tinta,
        max_conexiuni=args.max_conexiuni,
        timeout=args.timeout,
        logger=logger
    )
    tunel.porneste()


if __name__ == '__main__':
    main()
