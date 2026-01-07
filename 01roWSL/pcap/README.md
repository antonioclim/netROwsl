# Director Capturi de Rețea (PCAP)

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## Descriere

Acest director este destinat stocării fișierelor de captură de pachete (PCAP).

## Convenții de Denumire

```
<descriere>_<timestamp>.pcap
```

Exemple:
- `tcp_handshake_20250106.pcap`
- `udp_trafic_9091.pcap`
- `icmp_ping_test.pcap`

## Cum să Deschideți Fișierele PCAP

### Wireshark (Recomandat)

1. Deschideți Wireshark
2. File → Open → Selectați fișierul .pcap
3. Aplicați filtre după necesitate

### tshark (Linie de Comandă)

```bash
# Afișare conținut
tshark -r captura.pcap

# Primele 20 de pachete
tshark -r captura.pcap -c 20

# Cu filtru
tshark -r captura.pcap -Y "tcp"
```

### tcpdump (Linie de Comandă)

```bash
# Citire fișier
tcpdump -r captura.pcap

# Cu detalii
tcpdump -r captura.pcap -vv
```

## Curățare

Pentru a șterge toate capturile:

```bash
# Din directorul proiectului
rm -f pcap/*.pcap
```

Sau folosiți scriptul de curățare:

```bash
python scripts/curatare.py --complet
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
