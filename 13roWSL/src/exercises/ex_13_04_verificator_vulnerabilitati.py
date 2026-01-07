#!/usr/bin/env python3
"""
================================================================================
Exercițiul 4: Verificator de Vulnerabilități
================================================================================
S13 - IoT și Securitate în Rețelele de Calculatoare

OBIECTIVE PEDAGOGICE:
1. Înțelegerea tehnicilor de evaluare a vulnerabilităților
2. Identificarea configurațiilor nesigure în servicii de rețea
3. Detectarea versiunilor software vulnerabile
4. Generarea rapoartelor de securitate

AVERTISMENT ETIC:
- Utilizați EXCLUSIV pe sisteme pentru care aveți autorizare
- Scopul este educațional - învățarea securității defensive

UTILIZARE:
    # Verificare completă
    python3 ex_13_04_verificator_vulnerabilitati.py --tinta localhost --toate
    
    # Verificare specifică FTP
    python3 ex_13_04_verificator_vulnerabilitati.py --tinta localhost --ftp --port 2121
    
    # Export raport JSON
    python3 ex_13_04_verificator_vulnerabilitati.py --tinta localhost --toate --output raport.json

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
================================================================================
"""

import argparse
import json
import re
import socket
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Dict, Optional

try:
    import requests
except ImportError:
    requests = None


# ==============================================================================
# CONSTANTE ȘI CONFIGURARE
# ==============================================================================

class Culori:
    ROSU = "\033[91m"
    VERDE = "\033[92m"
    GALBEN = "\033[93m"
    ALBASTRU = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# Dezactivează culorile când nu este TTY
try:
    if not sys.stdout.isatty():
        for attr in dir(Culori):
            if not attr.startswith('_'):
                setattr(Culori, attr, "")
except Exception:
    pass


# Niveluri de severitate
class Severitate:
    CRITIC = "CRITIC"
    RIDICAT = "RIDICAT"
    MEDIU = "MEDIU"
    SCAZUT = "SCĂZUT"
    INFO = "INFO"


# Mapare culori pentru severități
CULORI_SEVERITATE = {
    Severitate.CRITIC: Culori.ROSU,
    Severitate.RIDICAT: Culori.MAGENTA,
    Severitate.MEDIU: Culori.GALBEN,
    Severitate.SCAZUT: Culori.ALBASTRU,
    Severitate.INFO: Culori.CYAN
}


# ==============================================================================
# STRUCTURI DE DATE
# ==============================================================================

@dataclass
class Vulnerabilitate:
    """Reprezintă o vulnerabilitate descoperită."""
    serviciu: str
    port: int
    severitate: str
    titlu: str
    descriere: str
    cve: Optional[str] = None
    remediere: Optional[str] = None


@dataclass
class RaportSecuritate:
    """Raport complet de securitate."""
    tinta: str
    data_scanare: str
    durata_secunde: float
    vulnerabilitati: List[Dict] = field(default_factory=list)
    sumar: Dict = field(default_factory=dict)


# ==============================================================================
# VERIFICATORI DE VULNERABILITĂȚI
# ==============================================================================

class VerificatorVulnerabilitati:
    """
    Verificator principal de vulnerabilități.
    
    Oferă metode pentru verificarea diferitelor servicii
    și identificarea problemelor de securitate.
    """
    
    def __init__(self, tinta: str, verbose: bool = True):
        self.tinta = tinta
        self.verbose = verbose
        self.vulnerabilitati: List[Vulnerabilitate] = []
    
    def log(self, mesaj: str, nivel: str = "INFO"):
        """Afișează un mesaj de log."""
        if not self.verbose:
            return
        
        culoare = {
            "INFO": Culori.CYAN,
            "OK": Culori.VERDE,
            "ATENTIE": Culori.GALBEN,
            "EROARE": Culori.ROSU
        }.get(nivel, Culori.RESET)
        
        print(f"{culoare}[{nivel}]{Culori.RESET} {mesaj}")
    
    def adauga_vulnerabilitate(self, vuln: Vulnerabilitate):
        """Adaugă o vulnerabilitate la lista de rezultate."""
        self.vulnerabilitati.append(vuln)
        
        culoare = CULORI_SEVERITATE.get(vuln.severitate, Culori.RESET)
        print(f"\n{culoare}[{vuln.severitate}]{Culori.RESET} {vuln.titlu}")
        print(f"         Serviciu: {vuln.serviciu} (port {vuln.port})")
        if vuln.cve:
            print(f"         CVE: {vuln.cve}")
        print(f"         {vuln.descriere}")
    
    def verifica_port_deschis(self, port: int, timeout: float = 2.0) -> bool:
        """Verifică dacă un port este deschis."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            rezultat = sock.connect_ex((self.tinta, port))
            sock.close()
            return rezultat == 0
        except Exception:
            return False
    
    def obtine_banner(self, port: int, timeout: float = 3.0) -> Optional[str]:
        """Obține banner-ul de la un serviciu."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((self.tinta, port))
            
            sock.settimeout(1.0)
            try:
                banner = sock.recv(1024)
                return banner.decode('utf-8', errors='ignore').strip()
            except socket.timeout:
                return None
        except Exception:
            return None
        finally:
            try:
                sock.close()
            except Exception:
                pass
    
    # ==========================================================================
    # VERIFICĂRI FTP
    # ==========================================================================
    
    def verifica_ftp(self, port: int = 2121):
        """
        Verifică vulnerabilitățile serviciului FTP.
        
        Verificări:
        - Versiune vsftpd 2.3.4 (backdoor CVE-2011-2523)
        - Acces anonim activat
        - Transmisie în text clar
        """
        self.log(f"Verificare FTP pe portul {port}...")
        
        if not self.verifica_port_deschis(port):
            self.log(f"Portul {port} nu este deschis", "INFO")
            return
        
        banner = self.obtine_banner(port)
        
        if banner:
            self.log(f"Banner FTP: {banner}", "INFO")
            
            # Verifică vsftpd 2.3.4 - backdoor cunoscut
            if "vsFTPd 2.3.4" in banner or "vsftpd 2.3.4" in banner.lower():
                self.adauga_vulnerabilitate(Vulnerabilitate(
                    serviciu="FTP",
                    port=port,
                    severitate=Severitate.CRITIC,
                    titlu="vsftpd 2.3.4 - Backdoor în codul sursă",
                    descriere="Această versiune conține un backdoor introdus malițios. "
                             "Autentificarea cu username conținând ':)' deschide un shell pe portul 6200.",
                    cve="CVE-2011-2523",
                    remediere="Actualizați la versiunea 2.3.5 sau mai nouă. "
                             "Verificați integritatea surselor software."
                ))
        
        # Verifică acces anonim
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.tinta, port))
            
            # Citește banner
            sock.recv(1024)
            
            # Încearcă login anonim
            sock.send(b"USER anonymous\r\n")
            raspuns = sock.recv(1024).decode('utf-8', errors='ignore')
            
            if "331" in raspuns:  # Password required
                sock.send(b"PASS anonymous@test.com\r\n")
                raspuns = sock.recv(1024).decode('utf-8', errors='ignore')
                
                if "230" in raspuns:  # Login successful
                    self.adauga_vulnerabilitate(Vulnerabilitate(
                        serviciu="FTP",
                        port=port,
                        severitate=Severitate.RIDICAT,
                        titlu="Acces anonim FTP activat",
                        descriere="Serverul FTP permite autentificare anonimă, "
                                 "ceea ce poate expune fișiere sensibile.",
                        remediere="Dezactivați accesul anonim în configurația vsftpd "
                                 "(anonymous_enable=NO)."
                    ))
            
            sock.close()
        except Exception as e:
            self.log(f"Eroare la verificarea accesului anonim: {e}", "EROARE")
        
        # Verifică transmisie în text clar
        self.adauga_vulnerabilitate(Vulnerabilitate(
            serviciu="FTP",
            port=port,
            severitate=Severitate.MEDIU,
            titlu="FTP transmite date în text clar",
            descriere="Protocolul FTP transmite credențialele și datele necriptat. "
                     "Un atacator pe rețea poate intercepta informațiile.",
            remediere="Migrați la SFTP (SSH File Transfer) sau FTPS (FTP over TLS)."
        ))
    
    def verifica_backdoor_ftp(self, port: int = 6200):
        """Verifică dacă portul de backdoor vsftpd este deschis."""
        self.log(f"Verificare port backdoor {port}...")
        
        if self.verifica_port_deschis(port):
            self.adauga_vulnerabilitate(Vulnerabilitate(
                serviciu="Backdoor",
                port=port,
                severitate=Severitate.CRITIC,
                titlu="Port backdoor vsftpd activ",
                descriere="Portul 6200 este deschis, indicând posibila activare "
                         "a backdoor-ului din vsftpd 2.3.4.",
                cve="CVE-2011-2523",
                remediere="Opriți imediat serviciul vsftpd și actualizați la o versiune sigură."
            ))
        else:
            self.log("Portul backdoor 6200 este închis", "OK")
    
    # ==========================================================================
    # VERIFICĂRI MQTT
    # ==========================================================================
    
    def verifica_mqtt(self, port: int = 1883):
        """
        Verifică vulnerabilitățile broker-ului MQTT.
        
        Verificări:
        - Conexiune fără autentificare
        - Trafic în text clar (fără TLS)
        """
        self.log(f"Verificare MQTT pe portul {port}...")
        
        if not self.verifica_port_deschis(port):
            self.log(f"Portul {port} nu este deschis", "INFO")
            return
        
        # Încearcă conexiune fără autentificare
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.tinta, port))
            
            # Trimite pachet MQTT CONNECT minim
            # Fixed header: CONNECT (0x10), Remaining length
            # Variable header: Protocol name, level, flags, keepalive
            # Payload: Client ID
            
            client_id = b"vuln-check"
            pachet_connect = bytearray([
                0x10,  # CONNECT
                12 + len(client_id),  # Remaining length
                0x00, 0x04,  # Protocol name length
                0x4D, 0x51, 0x54, 0x54,  # "MQTT"
                0x04,  # Protocol level (4 = 3.1.1)
                0x02,  # Connect flags (clean session)
                0x00, 0x3C,  # Keep alive (60 seconds)
                0x00, len(client_id),  # Client ID length
            ]) + client_id
            
            sock.send(bytes(pachet_connect))
            raspuns = sock.recv(4)
            
            if len(raspuns) >= 4 and raspuns[0] == 0x20:  # CONNACK
                cod_retur = raspuns[3]
                if cod_retur == 0:
                    self.adauga_vulnerabilitate(Vulnerabilitate(
                        serviciu="MQTT",
                        port=port,
                        severitate=Severitate.CRITIC,
                        titlu="Broker MQTT fără autentificare",
                        descriere="Broker-ul MQTT acceptă conexiuni fără credențiale. "
                                 "Oricine poate publica/abona la orice topic.",
                        remediere="Configurați autentificarea în mosquitto.conf: "
                                 "allow_anonymous false și password_file."
                    ))
            
            sock.close()
        except Exception as e:
            self.log(f"Eroare la verificarea MQTT: {e}", "EROARE")
        
        # Verifică dacă este text clar (nu TLS)
        if port == 1883:
            self.adauga_vulnerabilitate(Vulnerabilitate(
                serviciu="MQTT",
                port=port,
                severitate=Severitate.MEDIU,
                titlu="MQTT transmite în text clar",
                descriere="Traficul MQTT pe portul 1883 nu este criptat. "
                         "Mesajele pot fi interceptate pe rețea.",
                remediere="Utilizați portul 8883 cu TLS activat."
            ))
    
    # ==========================================================================
    # VERIFICĂRI HTTP/DVWA
    # ==========================================================================
    
    def verifica_http(self, port: int = 8080):
        """
        Verifică vulnerabilitățile serviciului HTTP.
        
        Verificări:
        - Prezența DVWA (Damn Vulnerable Web Application)
        - Headere de securitate lipsă
        """
        self.log(f"Verificare HTTP pe portul {port}...")
        
        if not self.verifica_port_deschis(port):
            self.log(f"Portul {port} nu este deschis", "INFO")
            return
        
        if requests is None:
            self.log("Biblioteca requests nu este disponibilă. Verificare limitată.", "ATENTIE")
            return
        
        try:
            url = f"http://{self.tinta}:{port}"
            raspuns = requests.get(url, timeout=5, allow_redirects=True)
            
            # Verifică dacă este DVWA
            if "dvwa" in raspuns.text.lower() or "damn vulnerable" in raspuns.text.lower():
                self.adauga_vulnerabilitate(Vulnerabilitate(
                    serviciu="HTTP",
                    port=port,
                    severitate=Severitate.CRITIC,
                    titlu="DVWA - Aplicație web intenționat vulnerabilă",
                    descriere="Damn Vulnerable Web Application este detectată. "
                             "Conține vulnerabilități intenționate: SQL Injection, XSS, "
                             "CSRF, File Inclusion, Command Injection, etc.",
                    remediere="Nu expuneți DVWA la internet. Utilizați doar în medii izolate "
                             "pentru învățare."
                ))
            
            # Verifică headere de securitate
            headere_lipsa = []
            headere_importante = [
                ("X-Content-Type-Options", "Previne MIME sniffing"),
                ("X-Frame-Options", "Previne clickjacking"),
                ("X-XSS-Protection", "Protecție XSS browser"),
                ("Content-Security-Policy", "Restricții resurse"),
                ("Strict-Transport-Security", "Forțează HTTPS")
            ]
            
            for header, descriere in headere_importante:
                if header.lower() not in [h.lower() for h in raspuns.headers.keys()]:
                    headere_lipsa.append(f"{header} ({descriere})")
            
            if headere_lipsa:
                self.adauga_vulnerabilitate(Vulnerabilitate(
                    serviciu="HTTP",
                    port=port,
                    severitate=Severitate.SCAZUT,
                    titlu="Headere de securitate HTTP lipsă",
                    descriere=f"Următoarele headere de securitate lipsesc: "
                             f"{', '.join(headere_lipsa[:3])}...",
                    remediere="Configurați serverul web pentru a trimite headerele de securitate."
                ))
            
        except requests.exceptions.RequestException as e:
            self.log(f"Eroare la verificarea HTTP: {e}", "EROARE")
    
    # ==========================================================================
    # RAPORTARE
    # ==========================================================================
    
    def genereaza_raport(self, durata: float) -> RaportSecuritate:
        """Generează raportul final de securitate."""
        sumar = {
            Severitate.CRITIC: 0,
            Severitate.RIDICAT: 0,
            Severitate.MEDIU: 0,
            Severitate.SCAZUT: 0,
            Severitate.INFO: 0
        }
        
        for vuln in self.vulnerabilitati:
            sumar[vuln.severitate] = sumar.get(vuln.severitate, 0) + 1
        
        return RaportSecuritate(
            tinta=self.tinta,
            data_scanare=datetime.now().isoformat(),
            durata_secunde=round(durata, 2),
            vulnerabilitati=[asdict(v) for v in self.vulnerabilitati],
            sumar=sumar
        )
    
    def afiseaza_raport(self, raport: RaportSecuritate):
        """Afișează raportul în format vizual."""
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║" + " " * 15 + "RAPORT VERIFICARE VULNERABILITĂȚI" + " " * 10 + "║")
        print("╠" + "═" * 58 + "╣")
        print(f"║ Țintă: {raport.tinta:50}║")
        print(f"║ Data:  {raport.data_scanare[:19]:50}║")
        print(f"║ Durată: {raport.durata_secunde} secunde" + " " * (41 - len(str(raport.durata_secunde))) + "║")
        print("╠" + "═" * 58 + "╣")
        
        # Sumar
        total = sum(raport.sumar.values())
        print(f"║ Total vulnerabilități: {total:33}║")
        
        for sev, cnt in raport.sumar.items():
            if cnt > 0:
                culoare = CULORI_SEVERITATE.get(sev, "")
                print(f"║   {culoare}{sev:10}{Culori.RESET}: {cnt:42}║")
        
        print("╚" + "═" * 58 + "╝")


# ==============================================================================
# FUNCȚIA PRINCIPALĂ
# ==============================================================================

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Verificator de Vulnerabilități - Laborator IoT și Securitate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  # Verificare completă pe toate serviciile
  python ex_13_04_verificator_vulnerabilitati.py --tinta localhost --toate
  
  # Verificare doar FTP
  python ex_13_04_verificator_vulnerabilitati.py --tinta localhost --ftp --port-ftp 2121
  
  # Verificare MQTT și export raport
  python ex_13_04_verificator_vulnerabilitati.py --tinta localhost --mqtt --output raport.json

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
        """
    )
    
    parser.add_argument("--tinta", "-t", required=True,
                        help="Ținta de verificat (IP sau hostname)")
    parser.add_argument("--toate", "-a", action="store_true",
                        help="Verifică toate serviciile")
    parser.add_argument("--ftp", action="store_true",
                        help="Verifică serviciul FTP")
    parser.add_argument("--mqtt", action="store_true",
                        help="Verifică serviciul MQTT")
    parser.add_argument("--http", action="store_true",
                        help="Verifică serviciul HTTP")
    parser.add_argument("--port-ftp", type=int, default=2121,
                        help="Port FTP (implicit: 2121)")
    parser.add_argument("--port-mqtt", type=int, default=1883,
                        help="Port MQTT (implicit: 1883)")
    parser.add_argument("--port-http", type=int, default=8080,
                        help="Port HTTP (implicit: 8080)")
    parser.add_argument("--output", "-o",
                        help="Fișier JSON pentru salvarea raportului")
    parser.add_argument("--silentios", "-s", action="store_true",
                        help="Mod silențios (doar rezultate)")
    
    args = parser.parse_args()
    
    # Dacă nu e specificat niciun serviciu, verifică toate
    if not (args.ftp or args.mqtt or args.http or args.toate):
        args.toate = True
    
    print("=" * 60)
    print(f"{Culori.BOLD}VERIFICATOR VULNERABILITĂȚI - SĂPTĂMÂNA 13{Culori.RESET}")
    print("IoT și Securitate în Rețelele de Calculatoare")
    print("=" * 60)
    
    print(f"\n{Culori.GALBEN}⚠️  Utilizați doar pe sisteme autorizate!{Culori.RESET}\n")
    
    verificator = VerificatorVulnerabilitati(args.tinta, verbose=not args.silentios)
    
    import time
    timp_start = time.time()
    
    # Rulează verificările selectate
    if args.toate or args.ftp:
        verificator.verifica_ftp(args.port_ftp)
        verificator.verifica_backdoor_ftp(6200)
    
    if args.toate or args.mqtt:
        verificator.verifica_mqtt(args.port_mqtt)
    
    if args.toate or args.http:
        verificator.verifica_http(args.port_http)
    
    durata = time.time() - timp_start
    
    # Generează și afișează raportul
    raport = verificator.genereaza_raport(durata)
    verificator.afiseaza_raport(raport)
    
    # Salvează în JSON dacă este specificat
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(asdict(raport), f, indent=2, ensure_ascii=False)
        print(f"\n{Culori.VERDE}[SALVAT]{Culori.RESET} Raport salvat în: {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
