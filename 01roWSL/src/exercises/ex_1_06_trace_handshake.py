#!/usr/bin/env python3
"""
Exercițiul 1.06: Trace TCP Handshake (FĂRĂ COD DE SCRIS)
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest exercițiu NU implică scrierea de cod.
Vei analiza o captură PCAP existentă și vei răspunde la întrebări.

Nivel Bloom: ANALYSE
Durată: 15 minute

Obiective:
- Să interpretezi capturile de pachete în Wireshark
- Să identifici fazele handshake-ului TCP
- Să extragi informații relevante din headere
"""

from __future__ import annotations

import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

VERDE = "\033[92m"
GALBEN = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


# ═══════════════════════════════════════════════════════════════════════════════
# INSTRUCTIUNI_EXERCITIU
# ═══════════════════════════════════════════════════════════════════════════════

INSTRUCTIUNI = f"""
{BOLD}╔════════════════════════════════════════════════════════════════════════════╗
║  EXERCIȚIU DE TRACE - ANALIZA TCP HANDSHAKE (FĂRĂ CODING)                  ║
╚════════════════════════════════════════════════════════════════════════════╝{RESET}

{CYAN}CONTEXT:{RESET}
Acest exercițiu dezvoltă abilitatea de a citi și interpreta capturi de pachete.
În lumea reală, debugging-ul problemelor de rețea începe aproape mereu cu
"hai să vedem ce se întâmplă în Wireshark".

{CYAN}PREGĂTIRE:{RESET}
1. Ai nevoie de o captură PCAP cu trafic TCP
   - Folosește captura din Exercițiul 4: /work/pcap/captura_tcp.pcap
   - SAU generează una nouă (vezi mai jos)

2. Deschide captura în Wireshark (pe Windows) sau cu tshark (în container)

{CYAN}GENERARE CAPTURĂ NOUĂ (dacă nu ai deja):{RESET}
   
   Terminal 1:
   $ tcpdump -i lo -w /work/pcap/handshake_demo.pcap port 9095 &
   
   Terminal 2:
   $ nc -l -p 9095
   
   Terminal 3:
   $ echo "test" | nc localhost 9095
   
   Terminal 1:
   $ pkill tcpdump

{BOLD}═══════════════════════════════════════════════════════════════════════════════{RESET}
{BOLD}                              ÎNTREBĂRI                                        {RESET}
{BOLD}═══════════════════════════════════════════════════════════════════════════════{RESET}

{GALBEN}PASUL 1:{RESET} Deschide fișierul PCAP și aplică filtrul: {BOLD}tcp{RESET}

{GALBEN}PASUL 2:{RESET} Identifică pachetele handshake-ului

┌─────────────────────────────────────────────────────────────────────────────┐
│  {BOLD}ÎNTREBAREA 1:{RESET} Care este primul pachet din handshake?                       │
│                                                                             │
│  Ce flag-uri TCP are setate? (Hint: coloana "Info" din Wireshark)          │
│                                                                             │
│  Răspunsul tău: _________________________________________________          │
│                                                                             │
│  {CYAN}Verificare:{RESET} Ar trebui să vezi [SYN] în coloana Info                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  {BOLD}ÎNTREBAREA 2:{RESET} Care este sequence number inițial al clientului?            │
│                                                                             │
│  (Click pe pachetul SYN → expandează "Transmission Control Protocol"       │
│   → caută "Sequence Number")                                               │
│                                                                             │
│  Răspunsul tău: _________________________________________________          │
│                                                                             │
│  {CYAN}Notă:{RESET} Wireshark poate arăta "relative sequence number" (0) sau           │
│        valoarea reală (un număr mare). Ambele sunt corecte.                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  {BOLD}ÎNTREBAREA 3:{RESET} Câte milisecunde durează întregul handshake?                │
│                                                                             │
│  Calculează diferența de timp între:                                       │
│  - Timestamp-ul pachetului SYN (primul)                                    │
│  - Timestamp-ul pachetului ACK final (al treilea)                          │
│                                                                             │
│  Răspunsul tău: ______________ ms                                          │
│                                                                             │
│  {CYAN}Hint:{RESET} Pentru loopback, ar trebui să fie sub 1ms                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  {BOLD}ÎNTREBAREA 4:{RESET} Dacă handshake-ul ar dura >100ms, ce ar putea indica?       │
│                                                                             │
│  Gândește-te la tipurile de întârziere din teorie:                         │
│  - Întârziere de transmisie                                                │
│  - Întârziere de propagare                                                 │
│  - Întârziere de procesare                                                 │
│  - Întârziere de așteptare (queuing)                                       │
│                                                                             │
│  Răspunsul tău: _________________________________________________          │
│                 _________________________________________________          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  {BOLD}ÎNTREBAREA 5 (BONUS):{RESET} Care este Window Size anunțat de server?            │
│                                                                             │
│  (În pachetul SYN-ACK, câmpul "Window")                                    │
│                                                                             │
│  Răspunsul tău: ______________ bytes                                       │
│                                                                             │
│  {CYAN}Context:{RESET} Window Size controlează cât de multe date pot fi "în zbor"      │
│           înainte de a primi ACK. Un window mare = throughput mai bun.     │
└─────────────────────────────────────────────────────────────────────────────┘

{BOLD}═══════════════════════════════════════════════════════════════════════════════{RESET}
{BOLD}                            VERIFICARE                                         {RESET}
{BOLD}═══════════════════════════════════════════════════════════════════════════════{RESET}

{GALBEN}PASUL 3:{RESET} Verifică răspunsurile

Nu există "răspuns corect" universal — depinde de captura ta.
Important e să înțelegi CE vezi și DE CE.

{VERDE}Criterii de auto-evaluare:{RESET}
□ Am identificat corect cele 3 pachete ale handshake-ului
□ Știu diferența între SYN, SYN-ACK și ACK
□ Pot explica de ce handshake-ul durează cât durează
□ Înțeleg ce reprezintă sequence number

{GALBEN}PASUL 4:{RESET} Discută cu colegul de bancă
- Ați obținut valori similare?
- Dacă nu, de ce? (capturi diferite? interpretări diferite?)

{BOLD}═══════════════════════════════════════════════════════════════════════════════{RESET}

{CYAN}COMANDĂ UTILĂ PENTRU VERIFICARE RAPIDĂ:{RESET}

   tshark -r /work/pcap/captura_tcp.pcap -Y "tcp.flags.syn==1" \\
          -T fields -e frame.number -e ip.src -e ip.dst \\
          -e tcp.seq -e tcp.ack -e tcp.flags.str

Aceasta afișează doar pachetele cu flag SYN setat (SYN și SYN-ACK).

{BOLD}═══════════════════════════════════════════════════════════════════════════════{RESET}
"""


def main() -> int:
    """Afișează instrucțiunile exercițiului."""
    print(INSTRUCTIUNI)
    
    # Verifică dacă există o captură
    pcap_path = Path("/work/pcap")
    if pcap_path.exists():
        pcap_files = list(pcap_path.glob("*.pcap"))
        if pcap_files:
            print(f"{VERDE}Capturi găsite în /work/pcap/:{RESET}")
            for f in pcap_files:
                size_kb = f.stat().st_size / 1024
                print(f"  - {f.name} ({size_kb:.1f} KB)")
            print()
        else:
            print(f"{GALBEN}Nu există capturi în /work/pcap/ — generează una nouă.{RESET}")
            print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
