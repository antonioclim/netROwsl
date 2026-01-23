#!/usr/bin/env python3
"""
================================================================================
Exercițiul 3: Analizor de Pachete (Packet Sniffer)
================================================================================
S13 - IoT și Securitate în Rețelele de Calculatoare

OBIECTIVE PEDAGOGICE:
1. Înțelegerea structurii pachetelor de rețea
2. Utilizarea bibliotecii Scapy pentru captura pachetelor
3. Analiza straturilor protocolare (Ethernet, IP, TCP/UDP)
4. Identificarea protocoalelor la nivel aplicație

AVERTISMENT:
- Necesită privilegii de administrator/root pentru captură
- Utilizați doar în rețele pentru care aveți autorizare

UTILIZARE:
    # Captură de bază (20 pachete)
    sudo python3 ex_13_03_sniffer_pachete.py --numar 20
    
    # Captură cu filtru BPF
    sudo python3 ex_13_03_sniffer_pachete.py --filtru "tcp port 1883" --numar 50
    
    # Salvare în fișier PCAP
    sudo python3 ex_13_03_sniffer_pachete.py --output captura.pcap --numar 100

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
================================================================================
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

try:
    from scapy.all import sniff, wrpcap, IP, TCP, UDP, ICMP, Raw, Ether
    from scapy.layers.http import HTTPRequest, HTTPResponse
except ImportError:
    print("[EROARE] Biblioteca Scapy nu este instalată!")
    print("         Instalați cu: pip install scapy")
    sys.exit(1)


# ==============================================================================
# ==============================================================================
# 🔮 PREDICȚIE - RĂSPUNDE ÎNAINTE DE A RULA CODUL
# ==============================================================================
#
# Înainte de a executa acest sniffer, răspunde la următoarele întrebări:
#
# 1. PROTOCOALE: Ce procent din pachetele capturate vor fi TCP vs UDP?
#    Estimarea ta: TCP ___% / UDP ___%
#    Hint: Gândește-te la serviciile laboratorului (MQTT, HTTP, FTP)
#
# 2. TTL: Ce valoare TTL te aștepți să vezi în pachetele locale?
#    A) 64 (Linux implicit)
#    B) 128 (Windows implicit)
#    C) 255 (maxim teoretic)
#    Răspuns probabil: A sau B, depinde de sursă
#
# 3. PERMISIUNI: De ce sniffer-ul necesită sudo/root?
#    A) Pentru a citi fișiere de configurare
#    B) Pentru a accesa interfețele de rețea în mod promiscuous
#    C) Pentru a scrie în directorul de output
#    Răspuns corect: B
#
# 4. HEADER IP: Câți bytes are cel mai mic header IP valid?
#    Răspuns: ___ bytes (Hint: IHL minim = 5, IHL × 4 = ?)
#
# 5. FLAGS TCP: În handshake-ul TCP, ce flags vei vedea în ordine?
#    Pachet 1: ___
#    Pachet 2: ___
#    Pachet 3: ___
#
# După rulare, verifică predicțiile în output-ul capturat!
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

# Mapare porturi cunoscute la protocoale
PROTOCOALE_PORTURI = {
    20: "FTP-DATE",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    1883: "MQTT",
    2121: "FTP-ALT",
    3306: "MYSQL",
    5432: "POSTGRESQL",
    6200: "BACKDOOR",
    8080: "HTTP-ALT",
    8883: "MQTT-TLS",
}


# ==============================================================================
# FUNCȚII DE ANALIZĂ
# ==============================================================================

class AnalizorPachete:
    """
    Analizor de pachete de rețea.
    
    Capturează și analizează pachetele, identificând protocoalele
    și extragând informații relevante.
    """
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.contor = 0
        self.pachete = []
        self.statistici = {
            'tcp': 0,
            'udp': 0,
            'icmp': 0,
            'altele': 0,
            'total_bytes': 0
        }
    
    def identifica_protocol(self, port_sursa: int, port_dest: int) -> str:
        """
        Identifică protocolul aplicație bazat pe porturi.
        
        Args:
            port_sursa: Portul sursă
            port_dest: Portul destinație
        
        Returns:
            Numele protocolului sau 'NECUNOSCUT'
        """
        # Verifică ambele porturi
        if port_dest in PROTOCOALE_PORTURI:
            return PROTOCOALE_PORTURI[port_dest]
        if port_sursa in PROTOCOALE_PORTURI:
            return PROTOCOALE_PORTURI[port_sursa]
        return "NECUNOSCUT"
    
    def formateaza_flags_tcp(self, flags) -> str:
        """
        Formatează flag-urile TCP într-un format lizibil.
        
        Args:
            flags: Flag-urile TCP din pachet
        
        Returns:
            Șir cu flag-urile (ex: "[SYN,ACK]")
        """
        flag_map = {
            'F': 'FIN',
            'S': 'SYN',
            'R': 'RST',
            'P': 'PSH',
            'A': 'ACK',
            'U': 'URG',
            'E': 'ECE',
            'C': 'CWR'
        }
        
        flags_str = str(flags)
        flags_active = [flag_map.get(f, f) for f in flags_str if f in flag_map]
        
        return f"[{','.join(flags_active)}]" if flags_active else ""
    
    def proceseaza_pachet(self, pachet):
        """
        Callback pentru procesarea fiecărui pachet capturat.
        
        Args:
            pachet: Pachetul Scapy capturat
        """
        self.contor += 1
        self.pachete.append(pachet)
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Calculează dimensiunea
        dimensiune = len(pachet)
        self.statistici['total_bytes'] += dimensiune
        
        # Analizează stratul IP
        if IP in pachet:
            ip_sursa = pachet[IP].src
            ip_dest = pachet[IP].dst
            
            # Analizează stratul transport
            if TCP in pachet:
                self.statistici['tcp'] += 1
                port_sursa = pachet[TCP].sport
                port_dest = pachet[TCP].dport
                flags = self.formateaza_flags_tcp(pachet[TCP].flags)
                protocol = self.identifica_protocol(port_sursa, port_dest)
                
                if self.verbose:
                    culoare = Culori.VERDE if 'SYN' in flags else Culori.CYAN
                    print(f"{culoare}[PKT {self.contor:04d}]{Culori.RESET} "
                          f"TCP {ip_sursa}:{port_sursa} -> {ip_dest}:{port_dest} "
                          f"{flags} [{protocol}] ({dimensiune} bytes)")
                    
                    # Afișează payload dacă există
                    if Raw in pachet and self.verbose:
                        payload = pachet[Raw].load
                        self._afiseaza_payload(payload, protocol)
            
            elif UDP in pachet:
                self.statistici['udp'] += 1
                port_sursa = pachet[UDP].sport
                port_dest = pachet[UDP].dport
                protocol = self.identifica_protocol(port_sursa, port_dest)
                
                if self.verbose:
                    print(f"{Culori.ALBASTRU}[PKT {self.contor:04d}]{Culori.RESET} "
                          f"UDP {ip_sursa}:{port_sursa} -> {ip_dest}:{port_dest} "
                          f"[{protocol}] ({dimensiune} bytes)")
            
            elif ICMP in pachet:
                self.statistici['icmp'] += 1
                tip_icmp = pachet[ICMP].type
                cod_icmp = pachet[ICMP].code
                
                tipuri_icmp = {
                    0: "Echo Reply",
                    8: "Echo Request",
                    3: "Destination Unreachable",
                    11: "Time Exceeded"
                }
                
                tip_str = tipuri_icmp.get(tip_icmp, f"Tip {tip_icmp}")
                
                if self.verbose:
                    print(f"{Culori.GALBEN}[PKT {self.contor:04d}]{Culori.RESET} "
                          f"ICMP {ip_sursa} -> {ip_dest} {tip_str} "
                          f"(cod: {cod_icmp}) ({dimensiune} bytes)")
            
            else:
                self.statistici['altele'] += 1
                if self.verbose:
                    print(f"{Culori.MAGENTA}[PKT {self.contor:04d}]{Culori.RESET} "
                          f"IP {ip_sursa} -> {ip_dest} "
                          f"Protocol: {pachet[IP].proto} ({dimensiune} bytes)")
        
        elif Ether in pachet:
            # Pachete non-IP (ARP, etc.)
            self.statistici['altele'] += 1
            if self.verbose:
                print(f"{Culori.MAGENTA}[PKT {self.contor:04d}]{Culori.RESET} "
                      f"Ethernet {pachet[Ether].src} -> {pachet[Ether].dst} "
                      f"Tip: 0x{pachet[Ether].type:04x} ({dimensiune} bytes)")
    
    def _afiseaza_payload(self, payload: bytes, protocol: str):
        """
        Afișează payload-ul într-un format lizibil.
        
        Args:
            payload: Datele brute din pachet
            protocol: Protocolul identificat
        """
        try:
            text = payload.decode('utf-8', errors='ignore')
            
            # Limitează la prima linie sau primele 100 caractere
            linii = text.split('\n')
            prima_linie = linii[0][:100] if linii else ""
            
            if prima_linie.strip():
                print(f"         {Culori.GALBEN}Payload:{Culori.RESET} {prima_linie}")
                
                # Identifică tipuri specifice de mesaje
                if protocol == "MQTT":
                    self._analizeaza_mqtt(payload)
                elif protocol in ["HTTP", "HTTP-ALT"]:
                    self._analizeaza_http(text)
                elif protocol == "FTP" or protocol == "FTP-ALT":
                    self._analizeaza_ftp(text)
                    
        except Exception:
            # Afișează hex pentru date binare
            hex_str = payload[:32].hex()
            print(f"         {Culori.GALBEN}Hex:{Culori.RESET} {hex_str}...")
    
    def _analizeaza_mqtt(self, payload: bytes):
        """Analizează un pachet MQTT."""
        if len(payload) < 2:
            return
        
        tip_mesaj = (payload[0] & 0xF0) >> 4
        
        tipuri_mqtt = {
            1: "CONNECT",
            2: "CONNACK",
            3: "PUBLISH",
            4: "PUBACK",
            5: "PUBREC",
            6: "PUBREL",
            7: "PUBCOMP",
            8: "SUBSCRIBE",
            9: "SUBACK",
            10: "UNSUBSCRIBE",
            11: "UNSUBACK",
            12: "PINGREQ",
            13: "PINGRESP",
            14: "DISCONNECT"
        }
        
        tip_str = tipuri_mqtt.get(tip_mesaj, f"NECUNOSCUT({tip_mesaj})")
        print(f"         {Culori.CYAN}MQTT:{Culori.RESET} {tip_str}")
    
    def _analizeaza_http(self, text: str):
        """Analizează un request/response HTTP."""
        if text.startswith(('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS')):
            parti = text.split(' ')
            if len(parti) >= 2:
                print(f"         {Culori.CYAN}HTTP Request:{Culori.RESET} {parti[0]} {parti[1]}")
        elif text.startswith('HTTP/'):
            parti = text.split(' ')
            if len(parti) >= 2:
                print(f"         {Culori.CYAN}HTTP Response:{Culori.RESET} {parti[1]}")
    
    def _analizeaza_ftp(self, text: str):
        """Analizează comenzi/răspunsuri FTP."""
        linii = text.strip().split('\n')
        for linie in linii[:3]:  # Primele 3 linii
            linie = linie.strip()
            if linie:
                print(f"         {Culori.CYAN}FTP:{Culori.RESET} {linie[:60]}")
    
    def afiseaza_statistici(self):
        """Afișează statisticile capturii."""
        print("\n" + "=" * 50)
        print(f"{Culori.BOLD}STATISTICI CAPTURĂ{Culori.RESET}")
        print("=" * 50)
        print(f"Total pachete:    {self.contor}")
        print(f"  TCP:            {self.statistici['tcp']}")
        print(f"  UDP:            {self.statistici['udp']}")
        print(f"  ICMP:           {self.statistici['icmp']}")
        print(f"  Altele:         {self.statistici['altele']}")
        print(f"Total bytes:      {self.statistici['total_bytes']:,}")
        print("=" * 50)


def listeaza_interfete():
    """Listează interfețele de rețea disponibile."""
    try:
        from scapy.all import get_if_list, get_if_addr
        
        print("\nInterfețe de rețea disponibile:")
        print("-" * 40)
        
        for iface in get_if_list():
            try:
                addr = get_if_addr(iface)
                print(f"  • {iface:15} ({addr})")
            except Exception:
                print(f"  • {iface}")
        
        print("-" * 40)
    except Exception as e:
        print(f"[EROARE] Nu s-au putut lista interfețele: {e}")


# ==============================================================================
# FUNCȚIA PRINCIPALĂ
# ==============================================================================

def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Analizor de Pachete - Laborator IoT și Securitate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  # Captură simplă
  sudo python ex_13_03_sniffer_pachete.py --numar 20
  
  # Captură trafic MQTT
  sudo python ex_13_03_sniffer_pachete.py --filtru "tcp port 1883" --numar 50
  
  # Captură și salvare în fișier
  sudo python ex_13_03_sniffer_pachete.py --filtru "tcp port 8080" --output captura.pcap --numar 100
  
  # Captură pe interfață specifică
  sudo python ex_13_03_sniffer_pachete.py --interfata eth0 --numar 50

Filtre BPF comune:
  tcp port 1883          - Trafic MQTT
  tcp port 8080          - Trafic HTTP alternativ
  host 10.0.13.11        - Trafic de la/către un host
  tcp and port 80        - Doar TCP pe portul 80

Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix
        """
    )
    
    parser.add_argument("--numar", "-n", type=int, default=20,
                        help="Numărul de pachete de capturat (implicit: 20)")
    parser.add_argument("--filtru", "-f", default="",
                        help="Filtru BPF pentru captură")
    parser.add_argument("--interfata", "-i", default=None,
                        help="Interfața de rețea pentru captură")
    parser.add_argument("--output", "-o",
                        help="Fișier PCAP pentru salvarea capturii")
    parser.add_argument("--timeout", "-t", type=int, default=0,
                        help="Timeout în secunde (0=nelimitat)")
    parser.add_argument("--silentios", "-s", action="store_true",
                        help="Mod silențios (doar statistici)")
    parser.add_argument("--listeaza-interfete", action="store_true",
                        help="Listează interfețele disponibile și iese")
    
    args = parser.parse_args()
    
    if args.listeaza_interfete:
        listeaza_interfete()
        return 0
    
    print("=" * 60)
    print(f"{Culori.BOLD}ANALIZOR PACHETE - LABORATOR SĂPTĂMÂNA 13{Culori.RESET}")
    print("IoT și Securitate în Rețelele de Calculatoare")
    print("=" * 60)
    
    print(f"\n{Culori.GALBEN}⚠️  ATENȚIE: Necesită privilegii de administrator!{Culori.RESET}")
    print(f"{Culori.GALBEN}   Utilizați doar în rețele autorizate!{Culori.RESET}\n")
    
    analizor = AnalizorPachete(verbose=not args.silentios)
    
    print(f"[INFO] Captură: {args.numar} pachete")
    if args.filtru:
        print(f"[INFO] Filtru BPF: {args.filtru}")
    if args.interfata:
        print(f"[INFO] Interfață: {args.interfata}")
    print("-" * 50)
    print("Apăsați Ctrl+C pentru a opri mai devreme\n")
    
    try:
        # Pornește captura
        pachete = sniff(
            count=args.numar,
            filter=args.filtru if args.filtru else None,
            iface=args.interfata,
            timeout=args.timeout if args.timeout > 0 else None,
            prn=analizor.proceseaza_pachet,
            store=True
        )
        
        # Afișează statisticile
        analizor.afiseaza_statistici()
        
        # Salvează în fișier dacă este specificat
        if args.output:
            wrpcap(args.output, pachete)
            print(f"\n{Culori.VERDE}[SALVAT]{Culori.RESET} Captură salvată în: {args.output}")
            print(f"         Analizați cu: wireshark {args.output}")
        
        return 0
        
    except PermissionError:
        print(f"\n{Culori.ROSU}[EROARE]{Culori.RESET} Permisiuni insuficiente!")
        print("         Rulați cu sudo: sudo python ex_13_03_sniffer_pachete.py")
        return 1
    except KeyboardInterrupt:
        print(f"\n{Culori.GALBEN}[INFO]{Culori.RESET} Captură întreruptă de utilizator")
        analizor.afiseaza_statistici()
        return 0
    except Exception as e:
        print(f"\n{Culori.ROSU}[EROARE]{Culori.RESET} {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
