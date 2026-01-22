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
    - Consultați docs/theory_summary.md pentru structura datagramei

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

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL
# Scop: Definește valorile fixe ale protocolului senzor
# Transferabil la: Orice implementare de protocol cu datagrame de dimensiune fixă
# ═══════════════════════════════════════════════════════════════════════════════

SENZOR_VERSIUNE = 1
SENZOR_DIMENSIUNE_DATAGRAMA = 23
SENZOR_PORT_IMPLICIT = 5402


# ═══════════════════════════════════════════════════════════════════════════════
# STRUCTURI_DATE
# Scop: Definește tipurile de date pentru configurare și citiri
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ConfiguratieSenzor:
    """Configurația unui senzor virtual."""
    sensor_id: int
    locatie: str
    temperatura_baza: float
    variatie: float = 2.0  # ±°C variație maximă
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


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATOR_SENZORI
# Scop: Simulează o rețea de senzori care trimit date periodic
# Transferabil la: Orice simulator de dispozitive IoT
# ═══════════════════════════════════════════════════════════════════════════════

class GeneratorSenzori:
    """
    Generator de senzori virtuali.
    
    Creează și gestionează o rețea de senzori simulați
    care trimit citiri periodice prin UDP.
    
    Exemplu:
        generator = GeneratorSenzori()
        generator.adauga_senzor(ConfiguratieSenzor(1, "Lab1", 22.0))
        generator.porneste()
        time.sleep(10)
        generator.opreste()
    """
    
    def __init__(self, host: str = 'localhost', port: int = SENZOR_PORT_IMPLICIT):
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
        
        PREDICȚIE:
        - Ce se întâmplă dacă adaugi un senzor cu ID duplicat?
        - Poți adăuga senzori după ce rețeaua a pornit?
        
        Args:
            config: Configurația senzorului
        """
        # TODO: Implementați adăugarea senzorului
        # Indiciu: Stocați configurația în self.senzori folosind sensor_id ca cheie
        pass
    
    def _construieste_datagrama(self, sensor_id: int, temperatura: float, 
                                 locatie: str) -> bytes:
        """
        Construiește o datagramă de senzor.
        
        PREDICȚIE:
        - Care e ordinea octeților pentru float în rețea? (little/big-endian?)
        - Dacă locația are 5 caractere, cu ce umpli restul până la 10?
        - CRC se calculează ÎNAINTE sau DUPĂ adăugarea câmpurilor rezervate?
        
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
        #    loc_bytes = locatie.encode('utf-8')[:10]
        #    loc_padded = loc_bytes + b'\x00' * (10 - len(loc_bytes))
        # 2. Împachetați versiunea, ID, temperatura, locația cu struct.pack('!BHf', ...)
        # 3. Calculați CRC32 pentru datele de până acum (17 bytes)
        # 4. Adăugați CRC și bytes rezervați (2 x \x00)
        pass
    
    def _genereaza_temperatura(self, config: ConfiguratieSenzor) -> float:
        """
        Generează o temperatură realistă pentru un senzor.
        
        PREDICȚIE:
        - Ce distribuție statistică e mai realistă: uniformă sau normală?
        - Cum simulezi variația pe parcursul zilei?
        
        Args:
            config: Configurația senzorului
        
        Returns:
            Temperatura generată
        """
        # TODO: Implementați generarea temperaturii
        # Indiciu: 
        # - Folosiți temperatura_baza + variație aleatorie
        # - random.gauss(0, config.variatie/3) pentru distribuție normală
        # - Opțional: adăugați variație în funcție de ora zilei
        pass
    
    def _ciclu_senzor(self, config: ConfiguratieSenzor):
        """
        Ciclu de execuție pentru un senzor individual.
        
        Rulează într-un thread separat și trimite date periodic.
        
        Args:
            config: Configurația senzorului
        """
        # TODO: Implementați ciclul de execuție
        # Indiciu:
        # 1. Creați un socket UDP (socket.SOCK_DGRAM)
        # 2. Cât timp self.activ:
        #    - Generați temperatura cu _genereaza_temperatura
        #    - Construiți datagrama cu _construieste_datagrama
        #    - Trimiteți prin UDP cu sendto()
        #    - Așteptați config.interval secunde cu time.sleep()
        # 3. Închideți socket-ul la final
        pass
    
    def porneste(self):
        """
        Pornește toți senzorii.
        
        PREDICȚIE:
        - Ce se întâmplă dacă apelezi porneste() de două ori?
        - Thread-urile sunt daemon sau nu? De ce contează?
        """
        # TODO: Implementați pornirea senzorilor
        # Indiciu: 
        # 1. Setați self.activ = True
        # 2. Pentru fiecare senzor din self.senzori:
        #    - Creați un thread cu target=self._ciclu_senzor și args=(config,)
        #    - Setați daemon=True pentru oprire automată
        #    - Porniți thread-ul și adăugați-l la self.thread_uri
        pass
    
    def opreste(self):
        """Oprește toți senzorii."""
        # TODO: Implementați oprirea senzorilor
        # Indiciu:
        # 1. Setați self.activ = False
        # 2. Așteptați ca thread-urile să se termine (join cu timeout)
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# ANALIZOR_DATE
# Scop: Colectează și analizează datele de la senzori
# Transferabil la: Orice sistem de monitorizare cu agregare statistică
# ═══════════════════════════════════════════════════════════════════════════════

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
        
        PREDICȚIE:
        - Ce lungime trebuie să aibă datagrama?
        - Cum extragi locația din bytes (cu sau fără null bytes)?
        - Cum verifici CRC-ul?
        
        Args:
            date: Datagrama brută
        
        Returns:
            CitireSenzor sau None dacă invalid
        """
        # TODO: Implementați parsarea datagramei
        # Indiciu: Inversul funcției _construieste_datagrama
        # 1. Verificați lungimea (23 bytes)
        # 2. Extrageți câmpurile cu struct.unpack
        # 3. Extrageți locația și eliminați padding-ul (\x00)
        # 4. Verificați CRC
        # 5. Returnați CitireSenzor
        pass
    
    def adauga_citire(self, citire: CitireSenzor):
        """
        Adaugă o citire la colecție.
        
        Args:
            citire: Citirea de adăugat
        """
        # TODO: Implementați adăugarea citirii
        # Indiciu: 
        # - Dacă sensor_id nu există în self.citiri, creați o listă nouă
        # - Adăugați citirea la listă
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
        # - statistics.mean() pentru medie
        # - statistics.stdev() pentru deviație standard (necesită minim 2 valori)
        # - min() și max() pentru extreme
        pass
    
    def detecteaza_anomalii(self, sensor_id: int, 
                            prag_deviatie: float = 2.0) -> List[CitireSenzor]:
        """
        Detectează citiri anormale (outliers).
        
        O citire este anormală dacă deviază cu mai mult de
        prag_deviatie * deviatie_standard de la medie.
        
        PREDICȚIE:
        - Câte citiri ai nevoie minim pentru a detecta anomalii?
        - O anomalie e neapărat o eroare?
        
        Args:
            sensor_id: ID-ul senzorului
            prag_deviatie: Pragul în deviații standard
        
        Returns:
            Lista citirilor anormale
        """
        # TODO: Implementați detectarea anomaliilor
        # Indiciu:
        # 1. Calculați statisticile cu calculeaza_statistici
        # 2. Pentru fiecare citire, verificați dacă:
        #    abs(citire.temperatura - medie) > prag * deviatie
        # 3. Returnați lista anomaliilor
        pass
    
    def genereaza_raport(self) -> str:
        """
        Generează un raport text cu toate statisticile.
        
        Returns:
            Raportul formatat
        """
        # TODO: Implementați generarea raportului
        # Indiciu: Formatați frumos statisticile pentru fiecare senzor
        # Exemplu format:
        # """
        # Senzor #1 (Lab1):
        #   Citiri: 100
        #   Temperatură: 22.5°C (min: 20.1°C, max: 24.8°C)
        #   Deviație: ±1.2°C
        #   Anomalii: 2
        # """
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# RECEPTOR_UDP
# Scop: Primește și procesează datagramele UDP de la senzori
# ═══════════════════════════════════════════════════════════════════════════════

class ReceptorUDP:
    """Receptor UDP pentru colectarea datelor de la senzori."""
    
    def __init__(self, port: int = SENZOR_PORT_IMPLICIT, 
                 analizor: Optional[AnalizorDateSenzori] = None):
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
        
        PREDICȚIE:
        - Ce tip de socket folosești pentru UDP? (SOCK_STREAM sau SOCK_DGRAM?)
        - recv() sau recvfrom() pentru UDP? De ce?
        - Ce se întâmplă dacă nu vine nicio datagramă?
        
        Args:
            durata: Durata în secunde (None = infinit)
        """
        # TODO: Implementați recepția UDP
        # Indiciu:
        # 1. Creați socket UDP și legați-l de port (bind)
        # 2. Setați timeout pentru a putea verifica self.activ
        # 3. Primiți datagrame în buclă cu recvfrom()
        # 4. Parsați și adăugați la analizor
        # 5. Respectați durata dacă e specificată
        pass
    
    def opreste(self):
        """Oprește recepția."""
        self.activ = False


# ═══════════════════════════════════════════════════════════════════════════════
# VIZUALIZARE (BONUS)
# ═══════════════════════════════════════════════════════════════════════════════

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
    #     print("Instalare: pip install matplotlib --break-system-packages")
    #     return
    #
    # Pentru fiecare senzor:
    # - plt.plot(timestamps, temperaturi, label=f"Senzor {id}")
    # 
    # plt.xlabel("Timp")
    # plt.ylabel("Temperatură (°C)")
    # plt.legend()
    # plt.show()
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRAȚIE
# ═══════════════════════════════════════════════════════════════════════════════

def demonstratie():
    """Demonstrație a sistemului de senzori."""
    print("=" * 60)
    print("Demonstrație Simulator Rețea Senzori")
    print("=" * 60)
    
    print("\nImplementați demonstrația conform instrucțiunilor!")
    print()
    print("Exemplu de utilizare (după implementare):")
    print("""
    # Creați configurații pentru senzori
    senzori = [
        ConfiguratieSenzor(1, "Lab1", 22.0),
        ConfiguratieSenzor(2, "Lab2", 24.0, variatie=3.0),
        ConfiguratieSenzor(3, "Hol", 20.0, interval=2.0),
    ]
    
    # Creați generatorul și adăugați senzorii
    generator = GeneratorSenzori()
    for s in senzori:
        generator.adauga_senzor(s)
    
    # Creați analizorul și receptorul
    analizor = AnalizorDateSenzori()
    receptor = ReceptorUDP(analizor=analizor)
    
    # Porniți generatorul într-un thread
    generator.porneste()
    
    # Colectați date pentru 10 secunde
    print("Colectare date pentru 10 secunde...")
    receptor.porneste(durata=10)
    
    # Opriți generatorul
    generator.opreste()
    
    # Afișați raportul
    print(analizor.genereaza_raport())
    
    # Detectați anomalii
    for sensor_id in analizor.citiri:
        anomalii = analizor.detecteaza_anomalii(sensor_id)
        if anomalii:
            print(f"Anomalii senzor {sensor_id}: {len(anomalii)}")
    
    # (Bonus) Vizualizați
    vizualizeaza_temperaturi(analizor)
    """)


if __name__ == "__main__":
    demonstratie()
