#!/usr/bin/env python3
"""
Tema 4.02b: Simulator Rețea Senzori — Partea 2: Analiză
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Implementați receptorul și analizorul de date de la senzori.

CERINȚE:
    1. Recepție datagrame UDP
    2. Parsare și verificare CRC
    3. Calcul statistici (medie, min, max, deviație)
    4. Detectare anomalii
    5. (Bonus) Vizualizare grafică

PREREQUISITE:
    - Finalizați tema_4_02a.py (generatorul)

INSTRUCȚIUNI:
    - Completați funcțiile marcate cu TODO
    - Folosiți generatorul din tema_4_02a pentru testare

PUNCTAJ: 25 puncte (+ 10 puncte bonus pentru vizualizare)
"""

import socket
import struct
import binascii
import statistics
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL
# ═══════════════════════════════════════════════════════════════════════════════

SENZOR_VERSIUNE = 1
SENZOR_DIMENSIUNE_DATAGRAMA = 23
SENZOR_PORT_IMPLICIT = 5402


# ═══════════════════════════════════════════════════════════════════════════════
# STRUCTURI_DATE
# Scop: Definește tipurile de date pentru citiri și statistici
# ═══════════════════════════════════════════════════════════════════════════════

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
# FUNCTII_UTILITARE
# ═══════════════════════════════════════════════════════════════════════════════

def calculeaza_crc32(date: bytes) -> int:
    """Calculează CRC32 pentru un șir de bytes."""
    return binascii.crc32(date) & 0xFFFFFFFF


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
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PARSARE_DATAGRAME
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _parseaza_datagrama(self, date: bytes) -> Optional[CitireSenzor]:
        """
        Parsează o datagramă de senzor.
        
        ---
        PREDICȚIE:
        1. Ce lungime trebuie să aibă datagrama?
        2. Cum extragi locația din bytes (cu sau fără null bytes)?
        3. Cum verifici CRC-ul? Pe câți bytes?
        ---
        
        Args:
            date: Datagrama brută
        
        Returns:
            CitireSenzor sau None dacă invalid
        """
        # TODO: Implementați parsarea datagramei
        # Indiciu: Inversul funcției _construieste_datagrama din tema_4_02a
        # 1. Verificați lungimea (exact 23 bytes)
        # 2. Extrageți versiune, sensor_id, temperatura: struct.unpack('!BHf', date[:7])
        # 3. Extrageți locația: date[7:17].rstrip(b'\x00').decode('utf-8')
        # 4. Extrageți CRC primit: struct.unpack('!I', date[17:21])[0]
        # 5. Calculați CRC peste primii 17 bytes și comparați
        # 6. Returnați CitireSenzor cu timestamp=datetime.now()
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COLECTARE_DATE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def adauga_citire(self, citire: CitireSenzor) -> None:
        """
        Adaugă o citire la colecție.
        
        Args:
            citire: Citirea de adăugat
        """
        # TODO: Implementați adăugarea citirii
        # Indiciu: 
        # - Dacă sensor_id nu există în self.citiri, creați o listă nouă
        # - Adăugați citirea la listă
        # if citire.sensor_id not in self.citiri:
        #     self.citiri[citire.sensor_id] = []
        # self.citiri[citire.sensor_id].append(citire)
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CALCUL_STATISTICI
    # ═══════════════════════════════════════════════════════════════════════════
    
    def calculeaza_statistici(self, sensor_id: int) -> StatisticiSenzor:
        """
        Calculează statistici pentru un senzor.
        
        ---
        PREDICȚIE:
        1. Ce funcție folosești pentru medie? (hint: statistics.mean)
        2. Ce se întâmplă cu stdev dacă ai doar 1 citire?
        3. Cum numeri citirile cu CRC invalid?
        ---
        
        Args:
            sensor_id: ID-ul senzorului
        
        Returns:
            Statistici calculate
        """
        # TODO: Implementați calculul statisticilor
        # Indiciu: Folosiți modulul statistics
        # temperaturi = [c.temperatura for c in self.citiri[sensor_id] if c.crc_valid]
        # stat = StatisticiSenzor(sensor_id)
        # stat.numar_citiri = len(temperaturi)
        # if temperaturi:
        #     stat.temperatura_medie = statistics.mean(temperaturi)
        #     stat.temperatura_min = min(temperaturi)
        #     stat.temperatura_max = max(temperaturi)
        #     if len(temperaturi) >= 2:
        #         stat.deviatie_standard = statistics.stdev(temperaturi)
        # stat.citiri_invalide = sum(1 for c in self.citiri[sensor_id] if not c.crc_valid)
        # return stat
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DETECTARE_ANOMALII
    # ═══════════════════════════════════════════════════════════════════════════
    
    def detecteaza_anomalii(self, sensor_id: int, 
                            prag_deviatie: float = 2.0) -> List[CitireSenzor]:
        """
        Detectează citiri anormale (outliers).
        
        O citire este anormală dacă deviază cu mai mult de
        prag_deviatie * deviatie_standard de la medie.
        
        ---
        PREDICȚIE:
        1. Câte citiri ai nevoie minim pentru a detecta anomalii?
        2. O anomalie e neapărat o eroare?
        3. Ce se întâmplă dacă deviația standard e 0?
        ---
        
        Args:
            sensor_id: ID-ul senzorului
            prag_deviatie: Pragul în deviații standard (implicit 2.0)
        
        Returns:
            Lista citirilor anormale
        """
        # TODO: Implementați detectarea anomaliilor
        # Indiciu:
        # 1. Calculați statisticile cu calculeaza_statistici(sensor_id)
        # 2. Dacă deviația e 0 sau avem prea puține citiri, returnați []
        # 3. Pentru fiecare citire validă, verificați:
        #    abs(citire.temperatura - medie) > prag * deviatie
        # 4. Returnați lista citirilor care depășesc pragul
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GENERARE_RAPORT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def genereaza_raport(self) -> str:
        """
        Generează un raport text cu toate statisticile.
        
        Returns:
            Raportul formatat
        """
        # TODO: Implementați generarea raportului
        # Indiciu: Formatați frumos statisticile pentru fiecare senzor
        # Exemplu output:
        # """
        # ══════════════════════════════════════════
        # RAPORT SENZORI
        # ══════════════════════════════════════════
        # 
        # Senzor #1 (Lab1):
        #   Citiri valide: 100
        #   Citiri invalide: 2
        #   Temperatură medie: 22.5°C
        #   Interval: 20.1°C - 24.8°C
        #   Deviație standard: ±1.2°C
        #   Anomalii detectate: 3
        # 
        # Senzor #2 (Lab2):
        #   ...
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
    
    def porneste(self, durata: Optional[float] = None) -> None:
        """
        Pornește recepția.
        
        ---
        PREDICȚIE:
        1. Ce tip de socket folosești pentru UDP? (SOCK_STREAM sau SOCK_DGRAM?)
        2. recv() sau recvfrom() pentru UDP? De ce?
        3. Ce se întâmplă dacă nu vine nicio datagramă?
        ---
        
        Args:
            durata: Durata în secunde (None = infinit)
        """
        # TODO: Implementați recepția UDP
        # Indiciu:
        # 1. Creați socket UDP: socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 2. Legați de port: self.socket.bind(('0.0.0.0', self.port))
        # 3. Setați timeout pentru a putea verifica self.activ: settimeout(1.0)
        # 4. self.activ = True
        # 5. timp_start = time.time() dacă durata e specificată
        # 6. Buclă while self.activ:
        #    try:
        #        date, adresa = self.socket.recvfrom(SENZOR_DIMENSIUNE_DATAGRAMA)
        #        citire = self.analizor._parseaza_datagrama(date)
        #        if citire:
        #            self.analizor.adauga_citire(citire)
        #    except socket.timeout:
        #        pass  # Normal, verificăm doar self.activ
        #    # Verifică durata dacă e specificată
        # 7. Închideți socket-ul
        pass
    
    def opreste(self) -> None:
        """Oprește recepția."""
        self.activ = False


# ═══════════════════════════════════════════════════════════════════════════════
# VIZUALIZARE (BONUS)
# ═══════════════════════════════════════════════════════════════════════════════

def vizualizeaza_temperaturi(analizor: AnalizorDateSenzori) -> None:
    """
    Vizualizează temperaturile în timp.
    
    BONUS: Implementați această funcție pentru 10 puncte extra.
    
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
    # plt.figure(figsize=(12, 6))
    # 
    # for sensor_id, citiri in analizor.citiri.items():
    #     timestamps = [c.timestamp for c in citiri if c.crc_valid]
    #     temperaturi = [c.temperatura for c in citiri if c.crc_valid]
    #     locatie = citiri[0].locatie if citiri else f"Senzor {sensor_id}"
    #     plt.plot(timestamps, temperaturi, label=f"{locatie} (#{sensor_id})", marker='.')
    # 
    # plt.xlabel("Timp")
    # plt.ylabel("Temperatură (°C)")
    # plt.title("Monitorizare Temperatură Senzori")
    # plt.legend()
    # plt.grid(True, alpha=0.3)
    # plt.tight_layout()
    # plt.show()
    print("Funcția de vizualizare nu este implementată (BONUS)")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRAȚIE
# ═══════════════════════════════════════════════════════════════════════════════

def demonstratie():
    """Demonstrație a sistemului de analiză."""
    print("=" * 60)
    print("Demonstrație Analizor Senzori (Partea 2)")
    print("=" * 60)
    
    print("\nAceastă temă necesită generatorul din tema_4_02a.py!")
    print()
    print("Exemplu de utilizare completă (după implementarea ambelor părți):")
    print("""
    from tema_4_02a import GeneratorSenzori, ConfiguratieSenzor
    from tema_4_02b import AnalizorDateSenzori, ReceptorUDP, vizualizeaza_temperaturi
    import threading
    import time
    
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
    
    # Porniți generatorul
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


# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-EVALUARE (completează înainte de predare)
# ═══════════════════════════════════════════════════════════════════════════════
# □ Funcția _parseaza_datagrama() parsează corect toate câmpurile
# □ CRC-ul se verifică corect (comparație cu CRC calculat)
# □ Locația se extrage corect (eliminare null padding)
# □ Statisticile se calculează corect (medie, min, max, stdev)
# □ Detectarea anomaliilor funcționează cu prag configurabil
# □ Raportul e formatat clar și lizibil
# □ Receptorul UDP primește datagrame și le procesează
# □ Am testat cu generatorul din tema_4_02a
# □ (Bonus) Vizualizarea afișează grafic corect
# ═══════════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    demonstratie()
