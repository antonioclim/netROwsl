#!/usr/bin/env python3
"""
Tema 11.02: Resolver DNS cu Cache
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Acest fișier conține scheletul pentru tema 2.
Implementați funcțiile marcate cu TODO.

Punctaj:
- Server DNS UDP: 30 puncte
- Implementare cache: 30 puncte
- Rezoluție upstream: 25 puncte
- Statistici și management: 15 puncte
"""

import argparse
import signal
import socket
import struct
import threading
import time
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# Constante DNS conform RFC 1035
TIPURI_INREGISTRARI = {
    'A': 1,
    'NS': 2,
    'CNAME': 5,
    'MX': 15,
    'TXT': 16,
    'AAAA': 28,
}

TIPURI_INVERSE = {v: k for k, v in TIPURI_INREGISTRARI.items()}

# Clase DNS
CLASA_IN = 1  # Internet

# Coduri răspuns
RCODE_OK = 0
RCODE_FORMAT_ERROR = 1
RCODE_SERVER_FAILURE = 2
RCODE_NAME_ERROR = 3


@dataclass
class AntetDNS:
    """Reprezintă antetul unui mesaj DNS."""
    id: int
    qr: int = 0  # 0=interogare, 1=răspuns
    opcode: int = 0
    aa: int = 0  # Authoritative Answer
    tc: int = 0  # Truncation
    rd: int = 1  # Recursion Desired
    ra: int = 0  # Recursion Available
    rcode: int = 0
    qdcount: int = 1
    ancount: int = 0
    nscount: int = 0
    arcount: int = 0


@dataclass
class IntrebareDNS:
    """Reprezintă o întrebare DNS."""
    nume: str
    tip: int
    clasa: int = CLASA_IN


@dataclass
class IntrareCache:
    """Reprezintă o intrare în cache."""
    nume: str
    tip: int
    raspuns: bytes  # Răspunsul complet
    ttl: int
    expira_la: float
    
    @property
    def expirata(self) -> bool:
        return time.time() >= self.expira_la


class CacheDNS:
    """
    Cache pentru răspunsuri DNS.
    
    TODO: Implementați operațiunile de cache.
    """
    
    def __init__(self, ttl_maxim: int = 3600):
        """
        Inițializează cache-ul.
        
        Args:
            ttl_maxim: TTL maxim în secunde (limitează TTL-urile prea mari)
        """
        self.ttl_maxim = ttl_maxim
        self._cache: dict[str, IntrareCache] = {}
        self._lock = threading.Lock()
        
        # Statistici
        self.total_interogari = 0
        self.cache_hits = 0
        self.cache_misses = 0
    
    def _genereaza_cheie(self, nume: str, tip: int) -> str:
        """Generează cheia pentru cache."""
        return f"{nume.lower()}:{tip}"
    
    def obtine(self, nume: str, tip: int) -> Optional[bytes]:
        """
        Obține un răspuns din cache.
        
        Args:
            nume: Numele de domeniu
            tip: Tipul înregistrării
        
        Returns:
            Răspunsul DNS sau None dacă nu există/a expirat
        """
        # TODO: Implementați obținerea din cache
        # Sfat: Verificați dacă intrarea există și nu a expirat
        # Sfat: Actualizați statisticile (hits/misses)
        # Sfat: Ștergeți intrările expirate
        pass
    
    def stocheaza(self, nume: str, tip: int, raspuns: bytes, ttl: int):
        """
        Stochează un răspuns în cache.
        
        Args:
            nume: Numele de domeniu
            tip: Tipul înregistrării
            raspuns: Răspunsul DNS complet
            ttl: Time-to-live în secunde
        """
        # TODO: Implementați stocarea în cache
        # Sfat: Limitați TTL-ul la self.ttl_maxim
        # Sfat: Calculați timpul de expirare
        pass
    
    def goleste(self):
        """Golește tot cache-ul."""
        # TODO: Implementați golirea cache-ului
        pass
    
    def obtine_statistici(self) -> dict:
        """Returnează statisticile cache-ului."""
        with self._lock:
            total = self.cache_hits + self.cache_misses
            rata_hit = (self.cache_hits / total * 100) if total > 0 else 0
            
            return {
                "total_interogari": self.total_interogari,
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "rata_hit_procent": rata_hit,
                "intrari_cache": len(self._cache)
            }
    
    def curata_expirate(self):
        """Elimină intrările expirate din cache."""
        # TODO: Implementați curățarea intrărilor expirate
        pass


class ResolverDNS:
    """
    Resolver DNS cu cache.
    
    TODO: Implementați logica de rezoluție.
    """
    
    def __init__(
        self,
        adresa_ascultare: tuple[str, int] = ("0.0.0.0", 5353),
        server_upstream: tuple[str, int] = ("8.8.8.8", 53),
        ttl_maxim: int = 3600
    ):
        """
        Inițializează resolver-ul.
        
        Args:
            adresa_ascultare: (host, port) pentru serverul local
            server_upstream: (host, port) pentru resolver-ul upstream
            ttl_maxim: TTL maxim pentru cache
        """
        self.adresa_ascultare = adresa_ascultare
        self.server_upstream = server_upstream
        self.cache = CacheDNS(ttl_maxim)
        
        self._socket: Optional[socket.socket] = None
        self._opreste = threading.Event()
    
    def porneste(self):
        """Pornește serverul DNS."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(self.adresa_ascultare)
        self._socket.settimeout(1.0)  # Pentru verificare periodică oprire
        
        print(f"[DNS Resolver] Ascultă pe {self.adresa_ascultare[0]}:{self.adresa_ascultare[1]}")
        print(f"[DNS Resolver] Upstream: {self.server_upstream[0]}:{self.server_upstream[1]}")
        print(f"[DNS Resolver] Cache activat (TTL max: {self.cache.ttl_maxim}s)")
        print()
        
        while not self._opreste.is_set():
            try:
                date, adresa_client = self._socket.recvfrom(512)
                
                # Procesează interogarea într-un thread separat
                thread = threading.Thread(
                    target=self._gestioneaza_interogare,
                    args=(date, adresa_client)
                )
                thread.daemon = True
                thread.start()
                
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[Eroare] {e}")
        
        self._socket.close()
    
    def opreste(self):
        """Oprește serverul DNS."""
        self._opreste.set()
    
    def _gestioneaza_interogare(self, date: bytes, adresa_client: tuple):
        """
        Gestionează o interogare DNS.
        
        Args:
            date: Pachetul DNS primit
            adresa_client: Adresa clientului (ip, port)
        """
        try:
            # Parsează antetul și întrebarea
            antet = self._parseaza_antet(date)
            intrebare = self._parseaza_intrebare(date, 12)
            
            if intrebare is None:
                return
            
            tip_str = TIPURI_INVERSE.get(intrebare.tip, str(intrebare.tip))
            print(f"[Query] {intrebare.nume} {tip_str} din {adresa_client[0]}")
            
            # Verifică cache-ul
            raspuns_cache = self.cache.obtine(intrebare.nume, intrebare.tip)
            
            if raspuns_cache:
                print(f"[Cache HIT] {intrebare.nume} {tip_str}")
                # TODO: Actualizați ID-ul în răspunsul din cache
                raspuns = self._actualizeaza_id(raspuns_cache, antet.id)
                self._socket.sendto(raspuns, adresa_client)
            else:
                print(f"[Cache MISS] Interogare upstream...")
                raspuns = self._interogheaza_upstream(date)
                
                if raspuns:
                    # Extrage TTL și stochează în cache
                    ttl = self._extrage_ttl(raspuns)
                    if ttl > 0:
                        self.cache.stocheaza(intrebare.nume, intrebare.tip, raspuns, ttl)
                        print(f"[Cache] Stocat {intrebare.nume} {tip_str} (TTL: {ttl}s)")
                    
                    self._socket.sendto(raspuns, adresa_client)
                else:
                    # Trimite răspuns de eroare
                    raspuns_eroare = self._construieste_raspuns_eroare(date, RCODE_SERVER_FAILURE)
                    self._socket.sendto(raspuns_eroare, adresa_client)
            
        except Exception as e:
            print(f"[Eroare procesare] {e}")
    
    def _parseaza_antet(self, date: bytes) -> AntetDNS:
        """Parsează antetul DNS."""
        valori = struct.unpack('>HHHHHH', date[:12])
        id_val, flags, qdcount, ancount, nscount, arcount = valori
        
        return AntetDNS(
            id=id_val,
            qr=(flags >> 15) & 1,
            opcode=(flags >> 11) & 0xF,
            aa=(flags >> 10) & 1,
            tc=(flags >> 9) & 1,
            rd=(flags >> 8) & 1,
            ra=(flags >> 7) & 1,
            rcode=flags & 0xF,
            qdcount=qdcount,
            ancount=ancount,
            nscount=nscount,
            arcount=arcount
        )
    
    def _parseaza_intrebare(self, date: bytes, offset: int) -> Optional[IntrebareDNS]:
        """Parsează secțiunea de întrebare."""
        try:
            nume, offset = self._decodeaza_nume(date, offset)
            tip, clasa = struct.unpack('>HH', date[offset:offset+4])
            
            return IntrebareDNS(nume=nume, tip=tip, clasa=clasa)
        except Exception:
            return None
    
    def _decodeaza_nume(self, date: bytes, offset: int) -> tuple[str, int]:
        """Decodează un nume de domeniu."""
        etichete = []
        
        while True:
            lungime = date[offset]
            
            # Pointer de compresie
            if (lungime & 0xC0) == 0xC0:
                pointer = ((lungime & 0x3F) << 8) | date[offset + 1]
                nume_referit, _ = self._decodeaza_nume(date, pointer)
                etichete.append(nume_referit)
                return '.'.join(etichete), offset + 2
            
            if lungime == 0:
                return '.'.join(etichete), offset + 1
            
            offset += 1
            etichete.append(date[offset:offset + lungime].decode())
            offset += lungime
    
    def _interogheaza_upstream(self, interogare: bytes) -> Optional[bytes]:
        """
        Trimite interogarea către serverul upstream.
        
        Args:
            interogare: Pachetul DNS original
        
        Returns:
            Răspunsul de la upstream sau None
        """
        # TODO: Implementați interogarea upstream
        # Sfat: Creați un socket UDP
        # Sfat: Trimiteți interogarea la self.server_upstream
        # Sfat: Așteptați răspunsul (timeout 5s)
        # Sfat: Returnați răspunsul sau None la eroare
        pass
    
    def _extrage_ttl(self, raspuns: bytes) -> int:
        """
        Extrage TTL-ul din primul răspuns.
        
        Args:
            raspuns: Pachetul de răspuns DNS
        
        Returns:
            TTL în secunde sau 0 dacă nu poate fi extras
        """
        # TODO: Implementați extragerea TTL-ului
        # Sfat: Parsați antetul pentru a găsi ancount
        # Sfat: Săriți peste întrebări
        # Sfat: TTL-ul este la offset fix în secțiunea de răspuns
        return 300  # Valoare implicită
    
    def _actualizeaza_id(self, raspuns: bytes, id_nou: int) -> bytes:
        """Actualizează ID-ul într-un răspuns din cache."""
        # Primii 2 octeți sunt ID-ul
        return struct.pack('>H', id_nou) + raspuns[2:]
    
    def _construieste_raspuns_eroare(self, interogare: bytes, rcode: int) -> bytes:
        """Construiește un răspuns de eroare."""
        # Copiază interogarea și modifică flags
        id_original = struct.unpack('>H', interogare[:2])[0]
        
        # Flags: QR=1, RCODE=rcode
        flags = 0x8000 | rcode
        
        antet = struct.pack(
            '>HHHHHH',
            id_original,
            flags,
            1,  # QDCOUNT
            0,  # ANCOUNT
            0,  # NSCOUNT
            0   # ARCOUNT
        )
        
        # Păstrăm întrebarea originală
        return antet + interogare[12:]


def handler_sigterm(signum, frame):
    """Handler pentru SIGTERM."""
    print("\n[DNS Resolver] Oprire...")
    raise SystemExit(0)


def handler_sigusr1(resolver: ResolverDNS):
    """Handler pentru SIGUSR1 (golește cache-ul)."""
    def _handler(signum, frame):
        print("[DNS Resolver] Golire cache...")
        resolver.cache.goleste()
        print("[DNS Resolver] Cache golit!")
    return _handler


def main():
    parser = argparse.ArgumentParser(
        description="Resolver DNS cu cache",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python hw_11_02.py --listen 0.0.0.0:5353 --upstream 8.8.8.8
  python hw_11_02.py --stats
  
Testare:
  dig @localhost -p 5353 google.com A
        """
    )
    
    parser.add_argument(
        '--listen', '--ascultare', '-l',
        default='0.0.0.0:5353',
        help='Adresa de ascultare (implicit: 0.0.0.0:5353)'
    )
    parser.add_argument(
        '--upstream', '-u',
        default='8.8.8.8:53',
        help='Server DNS upstream (implicit: 8.8.8.8:53)'
    )
    parser.add_argument(
        '--max-ttl',
        type=int,
        default=3600,
        help='TTL maxim în secunde (implicit: 3600)'
    )
    parser.add_argument(
        '--stats', '--statistici',
        action='store_true',
        help='Afișează statisticile și iese'
    )
    
    args = parser.parse_args()
    
    # Parsează adresele
    listen_parts = args.listen.split(':')
    listen_addr = (listen_parts[0], int(listen_parts[1]))
    
    upstream_parts = args.upstream.split(':')
    upstream_addr = (upstream_parts[0], int(upstream_parts[1]) if len(upstream_parts) > 1 else 53)
    
    # Creează resolver-ul
    resolver = ResolverDNS(
        adresa_ascultare=listen_addr,
        server_upstream=upstream_addr,
        ttl_maxim=args.max_ttl
    )
    
    # Configurează semnalele
    signal.signal(signal.SIGTERM, handler_sigterm)
    signal.signal(signal.SIGINT, handler_sigterm)
    
    # Pe Linux, configurează SIGUSR1 pentru golirea cache-ului
    try:
        signal.signal(signal.SIGUSR1, handler_sigusr1(resolver))
    except (ValueError, AttributeError):
        pass  # SIGUSR1 nu e disponibil pe Windows
    
    try:
        resolver.porneste()
    except SystemExit:
        pass
    finally:
        # Afișează statisticile la ieșire
        stats = resolver.cache.obtine_statistici()
        print()
        print("[Stats]", end=" ")
        print(f"Total: {stats['total_interogari']} |", end=" ")
        print(f"Hits: {stats['cache_hits']} ({stats['rata_hit_procent']:.1f}%) |", end=" ")
        print(f"Miss: {stats['cache_misses']}")


if __name__ == '__main__':
    main()
