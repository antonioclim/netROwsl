#!/usr/bin/env python3
"""
Tema 2.02: Client UDP cu Retry Automat
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

CERINȚĂ:
Implementați un client UDP care gestionează pierderea pachetelor prin retry.

SPECIFICAȚII:
1. Dacă nu primește răspuns în 2 secunde, clientul retrimite cererea
2. Maximum 3 încercări înainte de a raporta eșec
3. Afișați statistici: încercări necesare, timp total
4. Implementați un mod de test care simulează pierdere de pachete

EXEMPLU OUTPUT:
    Trimitere: ping
      Încercarea 1... timeout
      Încercarea 2... succes!
    Răspuns: PONG (2 încercări, 2.15s total)
"""

import socket
import argparse
import sys
import time
import random
from dataclasses import dataclass
from typing import Optional, Tuple


# ============================================================================
# Configurație
# ============================================================================

HOST_IMPLICIT = "localhost"
PORT_IMPLICIT = 9091
TIMEOUT_IMPLICIT = 2.0
MAX_RETRY_IMPLICIT = 3


@dataclass
class StatisticiTrimitere:
    """Statisticile unei operațiuni de trimitere."""
    succes: bool
    răspuns: Optional[str]
    încercări: int
    timp_total: float
    
    def __str__(self) -> str:
        if self.succes:
            return (f"Răspuns: {self.răspuns} "
                    f"({self.încercări} încercare{'i' if self.încercări > 1 else ''}, "
                    f"{self.timp_total:.2f}s total)")
        else:
            return f"Eșuat după {self.încercări} încercări ({self.timp_total:.2f}s total)"


# ============================================================================
# TODO: Implementați clasa ClientUDPRetryer
# ============================================================================

class ClientUDPRetryer:
    """
    Client UDP cu mecanism de retry pentru gestionarea pierderii pachetelor.
    
    Atribute:
        host: Adresa serverului
        port: Portul serverului
        timeout: Timeout pentru fiecare încercare (secunde)
        max_retry: Numărul maxim de încercări
        verbose: Dacă să afișeze mesaje detaliate
    """
    
    def __init__(
        self,
        host: str = HOST_IMPLICIT,
        port: int = PORT_IMPLICIT,
        timeout: float = TIMEOUT_IMPLICIT,
        max_retry: int = MAX_RETRY_IMPLICIT,
        verbose: bool = True
    ):
        """
        Inițializează clientul UDP cu retry.
        
        Args:
            host: Adresa serverului
            port: Portul serverului
            timeout: Timeout per încercare în secunde
            max_retry: Număr maxim de încercări
            verbose: Afișare mesaje detaliate
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.max_retry = max_retry
        self.verbose = verbose
        self.adresă_server = (host, port)
        
        # Statistici cumulative
        self.total_trimise = 0
        self.total_reușite = 0
        self.total_eșuate = 0
        self.total_încercări = 0
    
    def _log(self, mesaj: str) -> None:
        """Afișează mesaj dacă modul verbose este activ."""
        if self.verbose:
            print(f"  {mesaj}")
    
    def trimite_cu_retry(self, mesaj: str) -> StatisticiTrimitere:
        """
        Trimite un mesaj cu retry automat la timeout.
        
        Args:
            mesaj: Mesajul de trimis serverului
            
        Returns:
            StatisticiTrimitere cu rezultatul operațiunii
            
        TODO: Implementați algoritmul de retry:
        1. Creați un socket UDP
        2. Pentru fiecare încercare (1 până la max_retry):
           a. Înregistrați timpul de start
           b. Trimiteți datagramă
           c. Încercați să primiți răspuns (cu timeout)
           d. Dacă succes, returnați rezultatul
           e. Dacă timeout, afișați mesaj și continuați
        3. Dacă toate încercările eșuează, returnați eșec
        4. Calculați timpul total și statisticile
        """
        if self.verbose:
            print(f"Trimitere: {mesaj}")
        
        timp_start_total = time.perf_counter()
        încercări = 0
        răspuns = None
        succes = False
        
        # TODO: Implementare buclă de retry
        # Creați socket-ul AICI, o singură dată
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(self.timeout)
                
                for încercare in range(1, self.max_retry + 1):
                    încercări = încercare
                    
                    # TODO: Implementați logica de trimitere și primire
                    # Hint: folosiți sock.sendto() și sock.recvfrom()
                    
                    try:
                        # TODO: Trimiteți mesajul
                        # sock.sendto(mesaj.encode('utf-8'), self.adresă_server)
                        
                        # TODO: Așteptați răspuns
                        # date, _ = sock.recvfrom(1024)
                        # răspuns = date.decode('utf-8')
                        
                        # TODO: Dacă ajungeți aici, a funcționat
                        # self._log(f"Încercarea {încercare}... succes!")
                        # succes = True
                        # break
                        
                        pass  # Înlocuiți cu implementarea
                        
                    except socket.timeout:
                        self._log(f"Încercarea {încercare}... timeout")
                        # Continuă cu următoarea încercare
                        continue
                    
        except Exception as e:
            self._log(f"Eroare: {e}")
        
        timp_total = time.perf_counter() - timp_start_total
        
        # Actualizare statistici globale
        self.total_trimise += 1
        self.total_încercări += încercări
        if succes:
            self.total_reușite += 1
        else:
            self.total_eșuate += 1
        
        return StatisticiTrimitere(
            succes=succes,
            răspuns=răspuns,
            încercări=încercări,
            timp_total=timp_total
        )
    
    def afișează_statistici(self) -> None:
        """Afișează statisticile cumulative."""
        print("\n" + "=" * 50)
        print("Statistici Client UDP cu Retry")
        print("=" * 50)
        print(f"  Total cereri:     {self.total_trimise}")
        print(f"  Reușite:          {self.total_reușite}")
        print(f"  Eșuate:           {self.total_eșuate}")
        print(f"  Total încercări:  {self.total_încercări}")
        if self.total_trimise > 0:
            rată_succes = (self.total_reușite / self.total_trimise) * 100
            medie_încercări = self.total_încercări / self.total_trimise
            print(f"  Rată succes:      {rată_succes:.1f}%")
            print(f"  Medie încercări:  {medie_încercări:.2f}")
        print("=" * 50)


class ClientUDPTestPierderi(ClientUDPRetryer):
    """
    Client UDP care simulează pierdere de pachete pentru testare.
    
    TODO: Extindeți ClientUDPRetryer pentru a:
    1. Simula pierdere de pachete cu o anumită probabilitate
    2. Permite testarea mecanismului de retry fără server real
    """
    
    def __init__(
        self,
        probabilitate_pierdere: float = 0.3,
        **kwargs
    ):
        """
        Inițializează clientul de test.
        
        Args:
            probabilitate_pierdere: Probabilitatea ca un pachet să fie "pierdut" (0.0-1.0)
            **kwargs: Argumente pentru clasa părinte
        """
        super().__init__(**kwargs)
        self.probabilitate_pierdere = probabilitate_pierdere
    
    def trimite_cu_retry(self, mesaj: str) -> StatisticiTrimitere:
        """
        Trimite cu simulare de pierdere.
        
        TODO: Implementare care:
        1. La fiecare încercare, decide aleatoriu dacă pachetul este "pierdut"
        2. Dacă pierdut, simulează timeout
        3. Dacă nu, simulează răspuns instant
        """
        if self.verbose:
            print(f"Trimitere (test, pierdere={self.probabilitate_pierdere:.0%}): {mesaj}")
        
        timp_start = time.perf_counter()
        încercări = 0
        succes = False
        răspuns = None
        
        # TODO: Implementați simularea
        # Hint: folosiți random.random() < self.probabilitate_pierdere
        
        for încercare in range(1, self.max_retry + 1):
            încercări = încercare
            
            # TODO: Simulați pierdere/succes
            pass
        
        timp_total = time.perf_counter() - timp_start
        
        self.total_trimise += 1
        self.total_încercări += încercări
        if succes:
            self.total_reușite += 1
        else:
            self.total_eșuate += 1
        
        return StatisticiTrimitere(
            succes=succes,
            răspuns=răspuns,
            încercări=încercări,
            timp_total=timp_total
        )


# ============================================================================
# Funcții de Test
# ============================================================================

def test_client_retryer() -> None:
    """Testează clientul cu retry folosind un server real."""
    print("=" * 60)
    print("Test Client UDP cu Retry")
    print("=" * 60)
    print("NOTĂ: Serverul UDP trebuie să ruleze pe localhost:9091")
    print()
    
    client = ClientUDPRetryer(verbose=True)
    
    comenzi = ["ping", "upper:test", "time", "help"]
    
    for comandă in comenzi:
        rezultat = client.trimite_cu_retry(comandă)
        print(f"  → {rezultat}")
        print()
    
    client.afișează_statistici()


def test_simulare_pierdere() -> None:
    """Testează simularea pierderii de pachete."""
    print("=" * 60)
    print("Test Simulare Pierdere Pachete")
    print("=" * 60)
    print()
    
    client = ClientUDPTestPierderi(probabilitate_pierdere=0.5, verbose=True)
    
    for i in range(5):
        print(f"\n--- Cererea {i + 1} ---")
        rezultat = client.trimite_cu_retry(f"test_{i}")
        print(f"  → {rezultat}")
    
    client.afișează_statistici()


# ============================================================================
# Punct de Intrare
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Client UDP cu Retry Automat",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  # Trimitere comandă
  python hw_2_02.py --command "ping"
  
  # Mod interactiv
  python hw_2_02.py --interactive
  
  # Test cu server real
  python hw_2_02.py --test
  
  # Simulare pierdere pachete
  python hw_2_02.py --simulate --loss 0.5
        """
    )
    parser.add_argument("--host", "-H", default=HOST_IMPLICIT, help="Adresa server")
    parser.add_argument("--port", "-p", type=int, default=PORT_IMPLICIT, help="Port server")
    parser.add_argument("--timeout", "-t", type=float, default=TIMEOUT_IMPLICIT, help="Timeout (sec)")
    parser.add_argument("--retry", "-r", type=int, default=MAX_RETRY_IMPLICIT, help="Max încercări")
    parser.add_argument("--command", "-c", help="Comandă de trimis")
    parser.add_argument("--interactive", "-i", action="store_true", help="Mod interactiv")
    parser.add_argument("--test", action="store_true", help="Rulează teste cu server real")
    parser.add_argument("--simulate", "-s", action="store_true", help="Simulare pierdere")
    parser.add_argument("--loss", "-l", type=float, default=0.3, help="Probabilitate pierdere (0-1)")
    
    args = parser.parse_args()
    
    if args.test:
        test_client_retryer()
        return 0
    
    if args.simulate:
        test_simulare_pierdere()
        return 0
    
    client = ClientUDPRetryer(
        host=args.host,
        port=args.port,
        timeout=args.timeout,
        max_retry=args.retry,
        verbose=True
    )
    
    if args.interactive:
        print(f"Client UDP cu Retry conectat la {args.host}:{args.port}")
        print("Introduceți comenzi (quit pentru ieșire)")
        print("-" * 40)
        
        try:
            while True:
                comandă = input("> ").strip()
                if comandă.lower() in ("quit", "exit"):
                    break
                if comandă:
                    rezultat = client.trimite_cu_retry(comandă)
                    print(f"  → {rezultat}")
        except (EOFError, KeyboardInterrupt):
            pass
        
        client.afișează_statistici()
        return 0
    
    if args.command:
        rezultat = client.trimite_cu_retry(args.command)
        print(rezultat)
        return 0 if rezultat.succes else 1
    
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
