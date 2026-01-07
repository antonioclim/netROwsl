#!/usr/bin/env python3
"""
Tema 4.02: Simulator Rețea Senzori
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Creați un simulator complet pentru o rețea de senzori IoT.

CERINȚE:
    1. Generator de senzori virtuali cu citiri realiste
    2. Analiză statistică a datelor primite
    3. (Bonus) Vizualizare grafică

INSTRUCȚIUNI:
    - Completați funcțiile marcate cu TODO
    - Senzorul trimite datagrame UDP de 23 de octeți
    - Folosiți protocolul Senzor definit în laborator

PUNCTAJ: 30 puncte (+ 10 puncte bonus pentru vizualizare)
"""

import socket
import struct
import binascii
import random
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import statistics

# =========================================================
# Structuri de date
# =========================================================

@dataclass
class ConfiguratieSenzor:
    """Configurația unui senzor virtual."""
    sensor_id: int
    locatie: str
    temperatura_baza: float
    variatie: float = 2.0  # ±°C
    interval: float = 1.0  # secunde între citiri


@dataclass 
class CitireSenzor:
    """O citire individuală de la un senzor."""
    sensor_id: int
    temperatura: float
    locatie: str
    timestamp: datetime
    crc_valid: bool = True


@dataclass
class StatisticiSenzor:
    """Statistici agregate pentru un senzor."""
    sensor_id: int
    numar_citiri: int = 0
    temperatura_medie: float = 0.0
    temperatura_min: float = float('inf')
    temperatura_max: float = float('-inf')
    deviatie_standard: float = 0.0
    citiri_invalide: int = 0


# =========================================================
# Generator de senzori
# =========================================================

class GeneratorSenzori:
    """
    Generator de senzori virtuali.
    
    Creează și gestionează o rețea de senzori simulați
    care trimit citiri periodice prin UDP.
    """
    
    def __init__(self, host: str = 'localhost', port: int = 5402):
        """
        Inițializează generatorul.
        
        Args:
            host: Adresa serverului UDP
            port: Portul serverului
        """
        self.host = host
        self.port = port
        self.senzori: Dict[int, ConfiguratieSenzor] = {}
        self.activ = False
        self.thread_uri: List[threading.Thread] = []
    
    def adauga_senzor(self, config: ConfiguratieSenzor):
        """
        Adaugă un senzor la rețea.
        
        Args:
            config: Configurația senzorului
        """
        # TODO: Implementați adăugarea senzorului
        # Indiciu: Stocați configurația în self.senzori
        pass
    
    def _construieste_datagrama(self, sensor_id: int, temperatura: float, 
                                 locatie: str) -> bytes:
        """
        Construiește o datagramă de senzor.
        
        Structura (23 octeți):
        - Versiune: 1 octet
        - ID Senzor: 2 octeți (big-endian)
        - Temperatură: 4 octeți (float, big-endian)
        - Locație: 10 octeți (padding cu null)
        - CRC32: 4 octeți (big-endian)
        - Rezervat: 2 octeți
        
        Args:
            sensor_id: ID-ul senzorului
            temperatura: Valoarea temperaturii
            locatie: Locația senzorului
        
        Returns:
            Datagramă de 23 de octeți
        """
        # TODO: Implementați construcția datagramei
        # Indiciu:
        # 1. Pregătiți locația (10 octeți, padding cu \x00)
        # 2. Împachetați versiunea, ID, temperatura, locația
        # 3. Calculați CRC32 pentru datele de până acum
        # 4. Adăugați CRC și bytes rezervați
        pass
    
    def _genereaza_temperatura(self, config: ConfiguratieSenzor) -> float:
        """
        Generează o temperatură realistă pentru un senzor.
        
        Args:
            config: Configurația senzorului
        
        Returns:
            Temperatura generată
        """
        # TODO: Implementați generarea temperaturii
        # Indiciu: 
        # - Folosiți temperatura_baza + variație aleatorie
        # - random.gauss() pentru distribuție normală
        # - Adăugați variație în funcție de "ora zilei" (opțional)
        pass
    
    def _ciclu_senzor(self, config: ConfiguratieSenzor):
        """
        Ciclu de execuție pentru un senzor individual.
        
        Args:
            config: Configurația senzorului
        """
        # TODO: Implementați ciclul de execuție
        # Indiciu:
        # 1. Creați un socket UDP
        # 2. Cât timp self.activ:
        #    - Generați temperatura
        #    - Construiți datagrama
        #    - Trimiteți prin UDP
        #    - Așteptați config.interval secunde
        pass
    
    def porneste(self):
        """Pornește toți senzorii."""
        # TODO: Implementați pornirea senzorilor
        # Indiciu: Creați un thread pentru fiecare senzor
        pass
    
    def opreste(self):
        """Oprește toți senzorii."""
        # TODO: Implementați oprirea senzorilor
        pass


# =========================================================
# Analizor de date
# =========================================================

class AnalizorDateSenzori:
    """
    Analizor pentru datele primite de la senzori.
    
    Colectează citiri și calculează statistici.
    """
    
    def __init__(self):
        """Inițializează analizorul."""
        self.citiri: Dict[int, List[CitireSenzor]] = {}
        self.statistici: Dict[int, StatisticiSenzor] = {}
    
    def _parseaza_datagrama(self, date: bytes) -> Optional[CitireSenzor]:
        """
        Parsează o datagramă de senzor.
        
        Args:
            date: Datagrama brută
        
        Returns:
            CitireSenzor sau None dacă invalid
        """
        # TODO: Implementați parsarea datagramei
        # Indiciu: Inversul funcției _construieste_datagrama
        pass
    
    def adauga_citire(self, citire: CitireSenzor):
        """
        Adaugă o citire la colecție.
        
        Args:
            citire: Citirea de adăugat
        """
        # TODO: Implementați adăugarea citirii
        pass
    
    def calculeaza_statistici(self, sensor_id: int) -> StatisticiSenzor:
        """
        Calculează statistici pentru un senzor.
        
        Args:
            sensor_id: ID-ul senzorului
        
        Returns:
            Statistici calculate
        """
        # TODO: Implementați calculul statisticilor
        # Indiciu: Folosiți modulul statistics pentru mean, stdev, etc.
        pass
    
    def detecteaza_anomalii(self, sensor_id: int, 
                            prag_deviatie: float = 2.0) -> List[CitireSenzor]:
        """
        Detectează citiri anormale (outliers).
        
        O citire este anormală dacă deviază cu mai mult de
        prag_deviatie * deviatie_standard de la medie.
        
        Args:
            sensor_id: ID-ul senzorului
            prag_deviatie: Pragul în deviații standard
        
        Returns:
            Lista citirilor anormale
        """
        # TODO: Implementați detectarea anomaliilor
        pass
    
    def genereaza_raport(self) -> str:
        """
        Generează un raport text cu toate statisticile.
        
        Returns:
            Raportul formatat
        """
        # TODO: Implementați generarea raportului
        # Indiciu: Formatați frumos statisticile pentru fiecare senzor
        pass


# =========================================================
# Receptor UDP (pentru testare)
# =========================================================

class ReceptorUDP:
    """Receptor UDP pentru colectarea datelor de la senzori."""
    
    def __init__(self, port: int = 5402, analizor: Optional[AnalizorDateSenzori] = None):
        """
        Inițializează receptorul.
        
        Args:
            port: Portul pe care ascultă
            analizor: Analizor pentru procesarea datelor
        """
        self.port = port
        self.analizor = analizor or AnalizorDateSenzori()
        self.activ = False
        self.socket: Optional[socket.socket] = None
    
    def porneste(self, durata: Optional[float] = None):
        """
        Pornește recepția.
        
        Args:
            durata: Durata în secunde (None = infinit)
        """
        # TODO: Implementați recepția UDP
        # Indiciu:
        # 1. Creați socket UDP și legați-l de port
        # 2. Primiți datagrame în buclă
        # 3. Parsați și adăugați la analizor
        pass
    
    def opreste(self):
        """Oprește recepția."""
        self.activ = False


# =========================================================
# Vizualizare (BONUS)
# =========================================================

def vizualizeaza_temperaturi(analizor: AnalizorDateSenzori):
    """
    Vizualizează temperaturile în timp.
    
    BONUS: Implementați această funcție pentru 10 puncte extra.
    
    Sugestii:
    - Folosiți matplotlib pentru grafice
    - Afișați un grafic liniar pentru fiecare senzor
    - Marcați anomaliile cu culoare diferită
    
    Args:
        analizor: Analizorul cu datele colectate
    """
    # TODO (BONUS): Implementați vizualizarea
    # Indiciu:
    # try:
    #     import matplotlib.pyplot as plt
    # except ImportError:
    #     print("matplotlib nu este instalat")
    #     return
    pass


# =========================================================
# Funcție principală de test
# =========================================================

def demonstratie():
    """Demonstrație a sistemului de senzori."""
    print("=" * 60)
    print("Demonstrație Simulator Rețea Senzori")
    print("=" * 60)
    
    # TODO: Completați demonstrația
    # Exemplu:
    # 
    # # Creați configurații pentru senzori
    # senzori = [
    #     ConfiguratieSenzor(1, "Lab1", 22.0),
    #     ConfiguratieSenzor(2, "Lab2", 24.0),
    #     ConfiguratieSenzor(3, "Hol", 20.0),
    # ]
    # 
    # # Creați generatorul și adăugați senzorii
    # generator = GeneratorSenzori()
    # for s in senzori:
    #     generator.adauga_senzor(s)
    # 
    # # Creați analizorul și receptorul
    # analizor = AnalizorDateSenzori()
    # receptor = ReceptorUDP(analizor=analizor)
    # 
    # # Porniți generatorul într-un thread
    # generator.porneste()
    # 
    # # Colectați date pentru 10 secunde
    # receptor.porneste(durata=10)
    # 
    # # Opriți generatorul
    # generator.opreste()
    # 
    # # Afișați raportul
    # print(analizor.genereaza_raport())
    # 
    # # (Bonus) Vizualizați
    # vizualizeaza_temperaturi(analizor)
    
    print("\nImplementați demonstrația conform instrucțiunilor!")


if __name__ == "__main__":
    demonstratie()
