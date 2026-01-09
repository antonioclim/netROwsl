#!/usr/bin/env python3
"""
Exemplu 3: Parsing binar cu struct
Demonstrează extragerea datelor din headere de protocol.
"""
import struct
import socket

def parseaza_header_ip(data: bytes) -> dict:
    """Parsează un header IP (primii 20 bytes)."""
    if len(data) < 20:
        raise ValueError("Date insuficiente pentru header IP")
    
    # Format: !BBHHHBBHII
    # B = unsigned char (1 byte)
    # H = unsigned short (2 bytes)
    # I = unsigned int (4 bytes)
    fields = struct.unpack('!BBHHHBBHII', data[:20])
    
    version_ihl = fields[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0x0F) * 4
    
    return {
        'version': version,
        'header_length': ihl,
        'tos': fields[1],
        'total_length': fields[2],
        'identification': fields[3],
        'ttl': fields[5],
        'protocol': fields[6],
        'checksum': hex(fields[7]),
        'src_ip': socket.inet_ntoa(struct.pack('!I', fields[8])),
        'dst_ip': socket.inet_ntoa(struct.pack('!I', fields[9])),
    }

def demo():
    # Simulăm un header IP
    header = struct.pack('!BBHHHBBHII',
        0x45,           # Version (4) + IHL (5) = 20 bytes
        0x00,           # TOS
        40,             # Total length
        0x1234,         # Identification
        0x4000,         # Flags + Fragment offset
        64,             # TTL
        6,              # Protocol (TCP)
        0x0000,         # Checksum
        0xC0A80101,     # Source: 192.168.1.1
        0x08080808,     # Dest: 8.8.8.8
    )
    
    print("Header IP generat:")
    print(f"Hex: {header.hex()}")
    print(f"\nParsare:")
    
    result = parseaza_header_ip(header)
    for key, value in result.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    demo()
