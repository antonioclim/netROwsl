#!/usr/bin/env python3
"""
Tema 4.02a: Simulator Rețea Senzori — Partea 1: Generator
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Implementați generatorul de senzori virtuali care trimite date prin UDP.

CERINȚE:
    1. Construirea corectă a datagramelor de 23 bytes
    2. Generarea de temperaturi realiste
    3. Trimiterea periodică prin UDP

INSTRUCȚIUNI:
    - Completați funcțiile marcate cu TODO
    - Consultați docs/theory_summary.md pentru structura datagramei
    - Testați cu serverul din container: localhost:5402

PUNCTAJ: 25 puncte

CONTINUARE: După finalizare, treceți la tema_4_02b.py pentru analiză.
"""

import socket
import struct
import binascii
import random
import time
import threading
from typing import Dict, List
from dataclasses import dataclass

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
# Scop: Definește tipurile de date pentru configurare
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ConfiguratieSenzor:
    """Configurația unui senzor virtual."""
    sensor_id: int
    locatie: str
    temperatura_baza: float
    variatie: float = 2.0  # ±°C variație maximă
    interval: float = 1.0  # secunde între citiri


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_UTILITARE
# Scop: Funcții helper pentru construcția datagramelor
# ═══════════════════════════════════════════════════════════════════════════════

def calculeaza_crc32(date: bytes) -> int:
    """
    Calculează CRC32 pentru un șir de bytes.
    
    Args:
        date: Datele pentru care se calculează CRC
        
    Returns:
        Valoarea CRC32 ca întreg pozitiv pe 32 biți
    """
    return binascii.crc32(date) & 0xFFFFFFFF


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
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GESTIONARE_SENZORI
    # ═══════════════════════════════════════════════════════════════════════════
    
    def adauga_senzor(self, config: ConfiguratieSenzor) -> None:
        """
        Adaugă un senzor la rețea.
        
        ---
        PREDICȚIE:
        1. Ce se întâmplă dacă adaugi un senzor cu ID duplicat?
        2. Poți adăuga senzori după ce rețeaua a pornit?
        ---
        
        Args:
            config: Configurația senzorului
        """
        # TODO: Implementați adăugarea senzorului
        # Indiciu: Stocați configurația în self.senzori folosind sensor_id ca cheie
        # self.senzori[config.sensor_id] = config
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CONSTRUIRE_DATAGRAME
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _construieste_datagrama(self, sensor_id: int, temperatura: float, 
                                 locatie: str) -> bytes:
        """
        Construiește o datagramă de senzor.
        
        ---
        PREDICȚIE:
        1. Care e ordinea octeților pentru float în rețea? (little/big-endian?)
        2. Dacă locația are 5 caractere, cu ce umpli restul până la 10?
        3. CRC se calculează ÎNAINTE sau DUPĂ adăugarea câmpurilor rezervate?
        ---
        
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
        # 2. Împachetați versiunea, ID, temperatura cu struct.pack('!BHf', ...)
        # 3. Concatenați cu loc_padded pentru a obține primii 17 bytes
        # 4. Calculați CRC32 pentru cei 17 bytes
        # 5. Adăugați CRC și bytes rezervați (2 x \x00)
        # 6. Verificați că rezultatul are exact 23 bytes
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GENERARE_DATE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _genereaza_temperatura(self, config: ConfiguratieSenzor) -> float:
        """
        Generează o temperatură realistă pentru un senzor.
        
        ---
        PREDICȚIE:
        1. Ce distribuție statistică e mai realistă: uniformă sau normală?
        2. Cum simulezi variația pe parcursul zilei?
        ---
        
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
        # return config.temperatura_baza + random.gauss(0, config.variatie / 3)
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CICLU_TRIMITERE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _ciclu_senzor(self, config: ConfiguratieSenzor) -> None:
        """
        Ciclu de execuție pentru un senzor individual.
        
        Rulează într-un thread separat și trimite date periodic.
        
        Args:
            config: Configurația senzorului
        """
        # TODO: Implementați ciclul de execuție
        # Indiciu:
        # 1. Creați un socket UDP: socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 2. Cât timp self.activ:
        #    - Generați temperatura cu _genereaza_temperatura(config)
        #    - Construiți datagrama cu _construieste_datagrama(...)
        #    - Trimiteți prin UDP: sock.sendto(datagrama, (self.host, self.port))
        #    - Așteptați config.interval secunde: time.sleep(config.interval)
        # 3. Închideți socket-ul la final: sock.close()
        pass
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CONTROL_GENERATOR
    # ═══════════════════════════════════════════════════════════════════════════
    
    def porneste(self) -> None:
        """
        Pornește toți senzorii.
        
        ---
        PREDICȚIE:
        1. Ce se întâmplă dacă apelezi porneste() de două ori?
        2. Thread-urile sunt daemon sau nu? De ce contează?
        ---
        """
        # TODO: Implementați pornirea senzorilor
        # Indiciu: 
        # 1. Verificați dacă e deja activ (evitați pornire dublă)
        # 2. Setați self.activ = True
        # 3. Pentru fiecare senzor din self.senzori.values():
        #    - Creați un thread cu target=self._ciclu_senzor și args=(config,)
        #    - Setați daemon=True pentru oprire automată la închiderea programului
        #    - Porniți thread-ul și adăugați-l la self.thread_uri
        pass
    
    def opreste(self) -> None:
        """Oprește toți senzorii."""
        # TODO: Implementați oprirea senzorilor
        # Indiciu:
        # 1. Setați self.activ = False
        # 2. Opțional: așteptați ca thread-urile să se termine cu join(timeout=2)
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRAȚIE
# ═══════════════════════════════════════════════════════════════════════════════

def demonstratie():
    """Demonstrație a generatorului de senzori."""
    print("=" * 60)
    print("Demonstrație Generator Senzori (Partea 1)")
    print("=" * 60)
    
    print("\nImplementați funcțiile TODO și apoi rulați acest test!")
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
    
    # Porniți generatorul
    generator.porneste()
    
    # Trimite date pentru 10 secunde
    print("Trimit date pentru 10 secunde...")
    time.sleep(10)
    
    # Opriți generatorul
    generator.opreste()
    print("Generator oprit!")
    """)
    
    print("\nVerificare structură datagramă:")
    print("  - Total: 23 bytes")
    print("  - [0]: Versiune (1 byte)")
    print("  - [1-2]: Sensor ID (2 bytes, big-endian)")
    print("  - [3-6]: Temperatură (4 bytes, float big-endian)")
    print("  - [7-16]: Locație (10 bytes, null-padded)")
    print("  - [17-20]: CRC32 (4 bytes, big-endian)")
    print("  - [21-22]: Rezervat (2 bytes, zeros)")


# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-EVALUARE (completează înainte de predare)
# ═══════════════════════════════════════════════════════════════════════════════
# □ Funcția adauga_senzor() stochează configurația corect
# □ Funcția _construieste_datagrama() returnează exact 23 bytes
# □ Locația e padding-uită corect cu null bytes
# □ CRC32 se calculează peste primii 17 bytes (fără CRC și rezervat)
# □ Folosesc '!' în struct.pack pentru network byte order
# □ Generatorul trimite date la intervalul specificat
# □ Thread-urile sunt daemon=True
# □ Am testat cu serverul UDP (port 5402)
# □ Am verificat datagrama în Wireshark
# ═══════════════════════════════════════════════════════════════════════════════


if __name__ == "__main__":
    demonstratie()
