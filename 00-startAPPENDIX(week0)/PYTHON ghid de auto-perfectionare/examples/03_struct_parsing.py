#!/usr/bin/env python3
"""
Exemplu 3: Parsing binar cu struct
==================================
Demonstrează extragerea datelor din headere de protocol.

Curs: Rețele de Calculatoare - ASE București, CSIE
Autor: ing. dr. Antonio Clim
Versiune: 2.1 — cu subgoal labels și comentarii extinse

💡 ANALOGIE: Pachetele de Rețea ca Scrisori Poștale
---------------------------------------------------
| Element Pachet | Element Scrisoare                    |
|----------------|--------------------------------------|
| Header IP      | Plicul cu adrese (expeditor, dest.)  |
| Header TCP     | Ștampila și numărul de înregistrare  |
| Payload        | Conținutul scrisorii din plic        |
| Checksum       | Sigiliul de ceară (verifică integr.) |
| TTL            | "Returnează după 30 zile dacă nu..."  |

struct.unpack() = deschizi plicul și citești adresele în format standard

Obiective de învățare:
- Înțelegerea formatului binar al headerelor de protocol
- Manipularea bit-ilor și byte-ilor în Python
- Interpretarea câmpurilor unui header IP
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import struct
import socket
import logging
from typing import Optional
from dataclasses import dataclass

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURARE_LOGGING
# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: Logging-ul e esențial pentru debugging în aplicații de rețea
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# STRUCTURI_DE_DATE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class HeaderIP:
    """Reprezentare structurată a unui header IPv4.
    
    NOTE: Dataclass generează automat __init__, __repr__, __eq__ etc.
    Mult mai curat decât un dict sau o clasă manuală.
    
    Attributes:
        version: Versiunea IP (4 pentru IPv4)
        header_length: Lungimea headerului în bytes
        tos: Type of Service / DSCP
        total_length: Lungimea totală a pachetului
        identification: ID pentru fragmentare
        flags: Flags pentru fragmentare (DF, MF)
        fragment_offset: Offset-ul fragmentului
        ttl: Time To Live
        protocol: Protocolul încapsulat (6=TCP, 17=UDP, 1=ICMP)
        checksum: Checksum header (hex)
        src_ip: Adresa IP sursă
        dst_ip: Adresa IP destinație
    """
    version: int
    header_length: int
    tos: int
    total_length: int
    identification: int
    flags: int
    fragment_offset: int
    ttl: int
    protocol: int
    checksum: str
    src_ip: str
    dst_ip: str


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL
# ═══════════════════════════════════════════════════════════════════════════════

# NOTE: Numere protocol din header IP (RFC 790)
PROTOCOL_NAMES: dict[int, str] = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
    47: "GRE",
    50: "ESP",
    51: "AH",
    89: "OSPF",
}

# Format struct pentru header IP
# HACK: !BBHHHBBHII = network byte order, 20 bytes total
# B=1byte, H=2bytes, I=4bytes
IP_HEADER_FORMAT: str = '!BBHHHBBHII'
IP_HEADER_SIZE: int = 20


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_DE_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parseaza_header_ip(data: bytes) -> HeaderIP:
    """Parsează un header IPv4 din date binare.
    
    Extrage toate câmpurile standard dintr-un header IPv4 de 20 bytes.
    
    Args:
        data: Minimum 20 bytes reprezentând headerul IP
        
    Returns:
        HeaderIP cu toate câmpurile populate
        
    Raises:
        TypeError: Dacă data nu este de tip bytes
        ValueError: Dacă data are mai puțin de 20 bytes sau format invalid
        
    Example:
        >>> header = parseaza_header_ip(raw_packet[:20])
        >>> print(header.src_ip)
        '192.168.1.1'
        
    Note:
        Format struct: !BBHHHBBHII
        - ! = network byte order (big-endian)
        - B = unsigned char (1 byte)
        - H = unsigned short (2 bytes)
        - I = unsigned int (4 bytes)
    """
    # ─────────────────────────────────────────────────────────────
    # VALIDARE_INPUT
    # ─────────────────────────────────────────────────────────────
    if not isinstance(data, bytes):
        raise TypeError(
            f"Se așteaptă bytes, primit {type(data).__name__}. "
            f"Dacă ai un string, încearcă data.encode()."
        )
    
    if len(data) < IP_HEADER_SIZE:
        raise ValueError(
            f"Date insuficiente: {len(data)} bytes (minim {IP_HEADER_SIZE} pentru header IP). "
            f"Verifică dacă ai capturat headerul complet."
        )
    
    # ─────────────────────────────────────────────────────────────
    # PARSING_CU_STRUCT
    # ─────────────────────────────────────────────────────────────
    try:
        # NOTE: Format = Version+IHL, TOS, TotalLen, ID, Flags+FragOff, TTL, Proto, Checksum, SrcIP, DstIP
        fields = struct.unpack(IP_HEADER_FORMAT, data[:IP_HEADER_SIZE])
        logger.debug(f"Câmpuri raw: {fields}")
        
    except struct.error as e:
        raise ValueError(
            f"Format binar invalid: {e}. "
            f"Bytes-ii nu corespund formatului header IP."
        ) from e
    
    # ─────────────────────────────────────────────────────────────
    # EXTRAGERE_VERSION_IHL
    # ─────────────────────────────────────────────────────────────
    # NOTE: Primul byte conține 2 câmpuri de 4 biți fiecare
    # HACK: Folosim operații pe biți pentru a le separa
    version_ihl: int = fields[0]
    version: int = version_ihl >> 4  # Primii 4 biți (shift right)
    ihl: int = (version_ihl & 0x0F)  # Ultimii 4 biți (mask)
    header_length: int = ihl * 4     # IHL e în unități de 4 bytes
    
    # WARNING: Verificare versiune — alertează dacă nu e IPv4
    if version != 4:
        logger.warning(f"Versiune IP neașteptată: {version} (așteptat 4)")
    
    # ─────────────────────────────────────────────────────────────
    # EXTRAGERE_FLAGS_FRAGMENT
    # ─────────────────────────────────────────────────────────────
    # NOTE: Bytes 6-7 conțin flags (3 biți) și fragment offset (13 biți)
    flags_frag: int = fields[4]
    flags: int = flags_frag >> 13           # Primii 3 biți
    fragment_offset: int = flags_frag & 0x1FFF  # Ultimii 13 biți
    
    # ─────────────────────────────────────────────────────────────
    # CONVERSIE_ADRESE_IP
    # ─────────────────────────────────────────────────────────────
    # NOTE: Adresele IP sunt stocate ca unsigned int (4 bytes)
    # inet_ntoa le convertește în format string (dotted decimal)
    try:
        src_ip: str = socket.inet_ntoa(struct.pack('!I', fields[8]))
        dst_ip: str = socket.inet_ntoa(struct.pack('!I', fields[9]))
    except (socket.error, struct.error) as e:
        logger.error(f"Eroare la conversia adreselor IP: {e}")
        src_ip = f"invalid:{fields[8]:08x}"
        dst_ip = f"invalid:{fields[9]:08x}"
    
    # ─────────────────────────────────────────────────────────────
    # CONSTRUIRE_REZULTAT
    # ─────────────────────────────────────────────────────────────
    return HeaderIP(
        version=version,
        header_length=header_length,
        tos=fields[1],
        total_length=fields[2],
        identification=fields[3],
        flags=flags,
        fragment_offset=fragment_offset,
        ttl=fields[5],
        protocol=fields[6],
        checksum=f"0x{fields[7]:04x}",
        src_ip=src_ip,
        dst_ip=dst_ip,
    )


def get_protocol_name(protocol_num: int) -> str:
    """Returnează numele protocolului pentru un număr dat.
    
    Args:
        protocol_num: Numărul protocolului din header IP
        
    Returns:
        Numele protocolului sau "Unknown (N)" dacă nu e cunoscut
        
    Example:
        >>> get_protocol_name(6)
        'TCP'
    """
    return PROTOCOL_NAMES.get(protocol_num, f"Unknown ({protocol_num})")


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_DE_AFISARE
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_header(header: HeaderIP) -> None:
    """Afișează un header IP într-un format citibil.
    
    Args:
        header: Obiect HeaderIP de afișat
        
    Returns:
        None. Afișează la consolă.
    """
    protocol_name: str = get_protocol_name(header.protocol)
    
    # NOTE: Interpretare flags — biții au semnificații specifice
    flags_str: list[str] = []
    if header.flags & 0x4:
        flags_str.append("Reserved")
    if header.flags & 0x2:
        flags_str.append("DF (Don't Fragment)")
    if header.flags & 0x1:
        flags_str.append("MF (More Fragments)")
    flags_display: str = ", ".join(flags_str) if flags_str else "None"
    
    print(f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                         HEADER IPv4 PARSAT                            ║
╠═══════════════════════════════════════════════════════════════════════╣
║  Versiune:         {header.version:<10} (IPv{header.version})                          ║
║  Header Length:    {header.header_length:<10} bytes                                ║
║  Type of Service:  {header.tos:<10} (0x{header.tos:02x})                            ║
║  Total Length:     {header.total_length:<10} bytes                                ║
║  Identification:   {header.identification:<10} (0x{header.identification:04x})                          ║
║  Flags:            {flags_display:<45}║
║  Fragment Offset:  {header.fragment_offset:<10}                                    ║
║  TTL:              {header.ttl:<10} hops                                ║
║  Protocol:         {header.protocol:<10} ({protocol_name})                          ║
║  Header Checksum:  {header.checksum:<10}                                    ║
╠═══════════════════════════════════════════════════════════════════════╣
║  Source IP:        {header.src_ip:<20}                         ║
║  Destination IP:   {header.dst_ip:<20}                         ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRATIE
# ═══════════════════════════════════════════════════════════════════════════════

def demo() -> None:
    """Demonstrație completă a parsing-ului de header IP.
    
    Generează un header IP valid, îl parsează și afișează rezultatul.
    Include și demonstrații de gestionare a erorilor.
    
    Returns:
        None. Afișează output la consolă.
    """
    print("=" * 70)
    print("DEMONSTRAȚIE: Parsing Header IP cu struct")
    print("=" * 70)
    
    # ─────────────────────────────────────────────────────────────
    # PARTEA_1_GENERARE_HEADER
    # ─────────────────────────────────────────────────────────────
    print("\n📦 PARTEA 1: Generare header IP de test")
    print("-" * 50)
    
    # NOTE: Construim un header IP valid manual
    # Asta simulează ce ai primi de la un packet capture
    header_bytes: bytes = struct.pack(IP_HEADER_FORMAT,
        0x45,           # Version (4) + IHL (5) = 20 bytes header
        0x00,           # TOS (0 = normal)
        40,             # Total length (20 header + 20 TCP)
        0x1234,         # Identification
        0x4000,         # Flags (Don't Fragment) + Frag offset (0)
        64,             # TTL (64 hops - standard Linux)
        6,              # Protocol (6 = TCP)
        0x0000,         # Checksum (0 = nu calculăm)
        0xC0A80101,     # Source: 192.168.1.1
        0x08080808,     # Dest: 8.8.8.8 (Google DNS)
    )
    
    print(f"Header generat ({len(header_bytes)} bytes):")
    print(f"  Raw bytes: {header_bytes}")
    print(f"  Hex: {header_bytes.hex()}")
    
    # HACK: Afișare hex formatată (ca în Wireshark)
    print(f"  Wireshark view:")
    hex_str: str = header_bytes.hex()
    for i in range(0, len(hex_str), 4):
        chunk: str = hex_str[i:i+4]
        if i > 0 and i % 32 == 0:
            print()
        print(f"  {chunk}", end=" ")
    print()
    
    # ─────────────────────────────────────────────────────────────
    # PARTEA_2_PARSING
    # ─────────────────────────────────────────────────────────────
    print("\n🔍 PARTEA 2: Parsing header")
    print("-" * 50)
    
    try:
        header: HeaderIP = parseaza_header_ip(header_bytes)
        afiseaza_header(header)
        logger.info(f"Header parsat cu succes: {header.src_ip} → {header.dst_ip}")
        
    except (TypeError, ValueError) as e:
        logger.error(f"Eroare la parsing: {e}")
        print(f"❌ Eroare: {e}")
        return
    
    # ─────────────────────────────────────────────────────────────
    # PARTEA_3_GESTIONARE_ERORI
    # ─────────────────────────────────────────────────────────────
    print("\n⚠️  PARTEA 3: Gestionare erori")
    print("-" * 50)
    
    # Test 1: Date insuficiente
    print("\nTest 1: Date insuficiente (10 bytes în loc de 20)")
    try:
        parseaza_header_ip(b'\x45\x00\x00\x28\x12\x34\x40\x00\x40\x06')
    except ValueError as e:
        print(f"  ✅ Eroare așteptată: {e}")
    
    # Test 2: Tip greșit
    print("\nTest 2: Tip greșit (string în loc de bytes)")
    try:
        parseaza_header_ip("not bytes")  # type: ignore
    except TypeError as e:
        print(f"  ✅ Eroare așteptată: {e}")
    
    print("\n✅ Demonstrație completată!")


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_INTERACTIV
# ═══════════════════════════════════════════════════════════════════════════════

def quiz_struct() -> None:
    """Quiz pentru verificarea înțelegerii struct."""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║  🗳️  QUIZ: struct.unpack                                              ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  🔮 PREDICȚIE: Ce returnează acest cod?                               ║
║                                                                       ║
║      data = b'\\x00\\x50'  # 2 bytes                                    ║
║      port, = struct.unpack('!H', data)                                ║
║      print(port)                                                      ║
║                                                                       ║
║  Opțiuni:                                                             ║
║    A) 80                                                              ║
║    B) 20480                                                           ║
║    C) "\\x00\\x50"                                                      ║
║    D) (80,)                                                           ║
║                                                                       ║
║  Răspuns: A                                                           ║
║                                                                       ║
║  Explicație:                                                          ║
║  - '!H' = network byte order, unsigned short (2 bytes)                ║
║  - 0x0050 în big-endian = 80 în decimal                               ║
║  - Virgula după 'port' extrage valoarea din tuplu                     ║
║  - B ar fi corect dacă era '<H' (little-endian)                       ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        demo()
        quiz_struct()
        
    except KeyboardInterrupt:
        print("\n\n👋 Întrerupt de utilizator")
    except Exception as e:
        logger.exception(f"Eroare neașteptată: {e}")
        print(f"\n❌ Eroare neașteptată: {e}")
