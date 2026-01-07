#!/usr/bin/env python3
"""
Tema 9.02: Mașină de Stări pentru Sesiuni
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Implementați o mașină de stări finite (FSM) pentru gestionarea sesiunilor
de tip FTP.

Punctaj: 100 puncte
Dificultate: Medie-Avansată
"""

from enum import Enum, auto
from typing import List, Optional
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════
# ENUMERĂRI - NU MODIFICAȚI
# ═══════════════════════════════════════════════════════════════════════════

class StareSesiune(Enum):
    """Stările posibile ale unei sesiuni FTP."""
    DECONECTAT = auto()
    CONECTAT = auto()
    AUTENTIFICARE = auto()
    AUTENTIFICAT = auto()
    TRANSFER = auto()
    EROARE = auto()


class Eveniment(Enum):
    """Evenimentele care pot declanșa tranziții."""
    CONECTARE = auto()          # Client se conectează
    USER = auto()               # Comandă USER primită
    PASS_CORECT = auto()        # Parolă corectă
    PASS_GRESIT = auto()        # Parolă greșită
    RETR = auto()               # Comandă RETR (descărcare)
    STOR = auto()               # Comandă STOR (încărcare)
    TRANSFER_COMPLET = auto()   # Transfer finalizat
    TRANSFER_EROARE = auto()    # Eroare în timpul transferului
    QUIT = auto()               # Comandă QUIT
    TIMEOUT = auto()            # Timeout sesiune
    RESET = auto()              # Reset din stare de eroare


# ═══════════════════════════════════════════════════════════════════════════
# CLASĂ DE IMPLEMENTAT
# ═══════════════════════════════════════════════════════════════════════════

class MasinaStariSesiune:
    """
    Mașină de stări pentru gestionarea sesiunilor de tip FTP.
    
    Această clasă implementează un automat finit determinist (DFA) care
    modelează ciclul de viață al unei sesiuni FTP.
    
    Diagrama de tranziții:
    
    ```
    DECONECTAT ──conectare──▶ CONECTAT ──user──▶ AUTENTIFICARE
         ▲                                           │
         │                              pass_corect──┼──pass_gresit
         │                                   │       │       │
         │                                   ▼       │       ▼
         │                            AUTENTIFICAT   │    EROARE
         │                                │    ▲     │       │
         │                         retr/stor   │     │       │
         │                                │    │     │    reset
         │                                ▼    │     │       │
         │                            TRANSFER─┘     │       │
         │                                           │       │
         └────────────quit/timeout───────────────────┴───────┘
    ```
    
    Atribute:
        _stare: Starea curentă
        _istoric: Lista stărilor anterioare cu timestamp
        _utilizator: Numele utilizatorului (după USER)
    """
    
    def __init__(self):
        """
        Inițializează mașina de stări.
        
        Starea inițială: DECONECTAT
        """
        # TODO: Implementați inițializarea
        #
        # Inițializați:
        # - _stare cu DECONECTAT
        # - _istoric ca listă goală
        # - _utilizator ca None
        
        raise NotImplementedError("Implementați __init__()")
    
    def stare_curenta(self) -> StareSesiune:
        """
        Returnează starea curentă a sesiunii.
        
        Returnează:
            StareSesiune: Starea curentă
        """
        # TODO: Implementați această metodă
        raise NotImplementedError("Implementați stare_curenta()")
    
    def tranzitie(self, eveniment: Eveniment) -> bool:
        """
        Încearcă să execute o tranziție bazată pe eveniment.
        
        Argumente:
            eveniment: Evenimentul care declanșează tranziția
        
        Returnează:
            bool: True dacă tranziția a avut loc, False dacă era invalidă
        
        Efect secundar:
            - Actualizează starea curentă
            - Adaugă la istoric (stare, timestamp)
        
        Exemple:
            >>> fsm = MasinaStariSesiune()
            >>> fsm.tranzitie(Eveniment.CONECTARE)
            True
            >>> fsm.stare_curenta() == StareSesiune.CONECTAT
            True
            >>> fsm.tranzitie(Eveniment.RETR)  # Invalid din CONECTAT
            False
        """
        # TODO: Implementați această metodă
        #
        # Pași:
        # 1. Definiți tabelul de tranziții valide:
        #    tranzitii = {
        #        (StareSesiune.DECONECTAT, Eveniment.CONECTARE): StareSesiune.CONECTAT,
        #        (StareSesiune.CONECTAT, Eveniment.USER): StareSesiune.AUTENTIFICARE,
        #        ... etc
        #    }
        # 2. Verificați dacă (stare_curenta, eveniment) există în tabel
        # 3. Dacă da:
        #    - Salvați starea veche în istoric
        #    - Actualizați _stare
        #    - Returnați True
        # 4. Dacă nu, returnați False
        #
        # Notă: QUIT și TIMEOUT trebuie să funcționeze din orice stare
        
        raise NotImplementedError("Implementați tranzitie()")
    
    def istoric(self) -> List[tuple]:
        """
        Returnează istoricul tranzițiilor.
        
        Returnează:
            list: Lista de tuple (stare, timestamp)
        
        Exemplu:
            >>> fsm = MasinaStariSesiune()
            >>> fsm.tranzitie(Eveniment.CONECTARE)
            >>> fsm.tranzitie(Eveniment.USER)
            >>> len(fsm.istoric()) >= 2
            True
        """
        # TODO: Implementați această metodă
        raise NotImplementedError("Implementați istoric()")
    
    def este_autentificat(self) -> bool:
        """
        Verifică dacă sesiunea este autentificată.
        
        Returnează:
            bool: True dacă starea este AUTENTIFICAT sau TRANSFER
        """
        # TODO: Implementați această metodă
        raise NotImplementedError("Implementați este_autentificat()")
    
    def este_activa(self) -> bool:
        """
        Verifică dacă sesiunea este activă (nu e DECONECTAT sau EROARE).
        
        Returnează:
            bool: True dacă sesiunea e activă
        """
        # TODO: Implementați această metodă
        raise NotImplementedError("Implementați este_activa()")
    
    def seteaza_utilizator(self, utilizator: str) -> None:
        """
        Setează numele utilizatorului.
        
        Argumente:
            utilizator: Numele utilizatorului
        """
        # TODO: Implementați această metodă
        raise NotImplementedError("Implementați seteaza_utilizator()")
    
    def obtine_utilizator(self) -> Optional[str]:
        """
        Returnează numele utilizatorului curent.
        
        Returnează:
            str sau None: Numele utilizatorului sau None dacă nu e setat
        """
        # TODO: Implementați această metodă
        raise NotImplementedError("Implementați obtine_utilizator()")
    
    def reseteaza(self) -> None:
        """
        Resetează mașina de stări la starea inițială.
        
        Efect:
            - Stare → DECONECTAT
            - Istoric → se păstrează (adaugă tranziția)
            - Utilizator → None
        """
        # TODO: Implementați această metodă
        raise NotImplementedError("Implementați reseteaza()")


# ═══════════════════════════════════════════════════════════════════════════
# FUNCȚII HELPER (OPȚIONALE)
# ═══════════════════════════════════════════════════════════════════════════

def simuleaza_sesiune_ftp() -> MasinaStariSesiune:
    """
    Simulează o sesiune FTP completă.
    
    Returnează:
        MasinaStariSesiune: Mașina de stări după simulare
    """
    fsm = MasinaStariSesiune()
    
    # Secvența tipică FTP
    fsm.tranzitie(Eveniment.CONECTARE)
    fsm.seteaza_utilizator("test")
    fsm.tranzitie(Eveniment.USER)
    fsm.tranzitie(Eveniment.PASS_CORECT)
    fsm.tranzitie(Eveniment.RETR)
    fsm.tranzitie(Eveniment.TRANSFER_COMPLET)
    fsm.tranzitie(Eveniment.QUIT)
    
    return fsm


# ═══════════════════════════════════════════════════════════════════════════
# TESTE LOCALE
# ═══════════════════════════════════════════════════════════════════════════

def test_masina_stari():
    """Rulează teste de bază pentru verificare."""
    print("=" * 50)
    print("Teste Mașină de Stări Sesiuni")
    print("=" * 50)
    print()
    
    teste_trecute = 0
    teste_total = 0
    
    # Test 1: Stare inițială
    teste_total += 1
    try:
        fsm = MasinaStariSesiune()
        assert fsm.stare_curenta() == StareSesiune.DECONECTAT
        print("  ✓ Test stare inițială: TRECUT")
        teste_trecute += 1
    except NotImplementedError:
        print("  ⚠ Test stare inițială: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test stare inițială: EȘUAT - {e}")
    
    # Test 2: Tranziție validă
    teste_total += 1
    try:
        fsm = MasinaStariSesiune()
        rezultat = fsm.tranzitie(Eveniment.CONECTARE)
        
        assert rezultat == True, "Tranziția ar fi trebuit să reușească"
        assert fsm.stare_curenta() == StareSesiune.CONECTAT
        
        print("  ✓ Test tranziție validă: TRECUT")
        teste_trecute += 1
    except NotImplementedError:
        print("  ⚠ Test tranziție validă: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test tranziție validă: EȘUAT - {e}")
    
    # Test 3: Tranziție invalidă
    teste_total += 1
    try:
        fsm = MasinaStariSesiune()
        # RETR din DECONECTAT nu e valid
        rezultat = fsm.tranzitie(Eveniment.RETR)
        
        assert rezultat == False, "Tranziția ar fi trebuit să eșueze"
        assert fsm.stare_curenta() == StareSesiune.DECONECTAT
        
        print("  ✓ Test tranziție invalidă: TRECUT")
        teste_trecute += 1
    except NotImplementedError:
        print("  ⚠ Test tranziție invalidă: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test tranziție invalidă: EȘUAT - {e}")
    
    # Test 4: Flux complet autentificare
    teste_total += 1
    try:
        fsm = MasinaStariSesiune()
        fsm.tranzitie(Eveniment.CONECTARE)
        fsm.tranzitie(Eveniment.USER)
        fsm.tranzitie(Eveniment.PASS_CORECT)
        
        assert fsm.este_autentificat() == True
        assert fsm.stare_curenta() == StareSesiune.AUTENTIFICAT
        
        print("  ✓ Test flux autentificare: TRECUT")
        teste_trecute += 1
    except NotImplementedError:
        print("  ⚠ Test flux autentificare: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test flux autentificare: EȘUAT - {e}")
    
    # Test 5: Eroare la parolă greșită
    teste_total += 1
    try:
        fsm = MasinaStariSesiune()
        fsm.tranzitie(Eveniment.CONECTARE)
        fsm.tranzitie(Eveniment.USER)
        fsm.tranzitie(Eveniment.PASS_GRESIT)
        
        assert fsm.stare_curenta() == StareSesiune.EROARE
        assert fsm.este_autentificat() == False
        
        print("  ✓ Test parolă greșită: TRECUT")
        teste_trecute += 1
    except NotImplementedError:
        print("  ⚠ Test parolă greșită: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test parolă greșită: EȘUAT - {e}")
    
    # Test 6: Istoric
    teste_total += 1
    try:
        fsm = MasinaStariSesiune()
        fsm.tranzitie(Eveniment.CONECTARE)
        fsm.tranzitie(Eveniment.USER)
        
        istoric = fsm.istoric()
        assert len(istoric) >= 2, "Istoricul ar trebui să aibă cel puțin 2 intrări"
        
        print("  ✓ Test istoric: TRECUT")
        teste_trecute += 1
    except NotImplementedError:
        print("  ⚠ Test istoric: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test istoric: EȘUAT - {e}")
    
    # Test 7: QUIT din orice stare
    teste_total += 1
    try:
        fsm = MasinaStariSesiune()
        fsm.tranzitie(Eveniment.CONECTARE)
        fsm.tranzitie(Eveniment.USER)
        fsm.tranzitie(Eveniment.PASS_CORECT)
        
        # QUIT trebuie să funcționeze din AUTENTIFICAT
        rezultat = fsm.tranzitie(Eveniment.QUIT)
        
        assert rezultat == True
        assert fsm.stare_curenta() == StareSesiune.DECONECTAT
        
        print("  ✓ Test QUIT: TRECUT")
        teste_trecute += 1
    except NotImplementedError:
        print("  ⚠ Test QUIT: NEIMPLEMENTAT")
    except Exception as e:
        print(f"  ✗ Test QUIT: EȘUAT - {e}")
    
    # Sumar
    print()
    print("=" * 50)
    print(f"Rezultate: {teste_trecute}/{teste_total} teste trecute")
    print("=" * 50)
    
    return teste_trecute == teste_total


if __name__ == "__main__":
    test_masina_stari()
