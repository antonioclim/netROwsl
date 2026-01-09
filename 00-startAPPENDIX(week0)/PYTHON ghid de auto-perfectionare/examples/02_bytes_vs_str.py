#!/usr/bin/env python3
"""
Exemplu 2: Diferența dintre bytes și str
Demonstrează conversia între text și date binare.
"""

def demonstreaza_conversie():
    # String (text pentru oameni)
    text = "Salut, Rețele!"
    print(f"String: {text}")
    print(f"Tip: {type(text)}")
    
    # Conversie la bytes (pentru trimitere pe rețea)
    octeti = text.encode('utf-8')
    print(f"\nBytes: {octeti}")
    print(f"Tip: {type(octeti)}")
    print(f"Lungime în bytes: {len(octeti)}")
    
    # Conversie înapoi la string
    text_decodat = octeti.decode('utf-8')
    print(f"\nDecodat: {text_decodat}")
    
    # Bytes literal (folosit des în networking)
    http_request = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
    print(f"\nHTTP Request (bytes):\n{http_request}")
    
    # Reprezentarea hexadecimală
    ip_bytes = b'\xC0\xA8\x01\x01'  # 192.168.1.1
    print(f"\nIP ca bytes: {ip_bytes}")
    print(f"Hex: {ip_bytes.hex()}")

if __name__ == "__main__":
    demonstreaza_conversie()
