# Director pentru Capturi de Pachete

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Descriere

Acest director este destinat stocării fișierelor de captură de pachete (format `.pcap`) generate în timpul sesiunilor de laborator.

## Convenție de Denumire

Fișierele sunt generate automat cu formatul:
```
week2_YYYYMMDD_HHMMSS.pcap
```

Exemplu: `week2_20250106_143022.pcap`

## Capturi Recomandate

Pentru a înțelege mai bine protocoalele TCP și UDP, vă recomandăm să capturați:

### TCP (portul 9090)
1. **Handshake-ul în trei pași**
   - Filtru: `tcp.port == 9090 && tcp.flags.syn == 1`
   - Observați: SYN → SYN-ACK → ACK

2. **Schimbul de date**
   - Filtru: `tcp.port == 9090 && tcp.len > 0`
   - Observați: PSH, ACK, numerele de secvență

3. **Terminarea conexiunii**
   - Filtru: `tcp.port == 9090 && tcp.flags.fin == 1`
   - Observați: FIN → ACK → FIN → ACK

### UDP (portul 9091)
1. **Cerere-Răspuns simplu**
   - Filtru: `udp.port == 9091`
   - Observați: Absența handshake-ului, datagrame independente

## Filtre Wireshark Utile

```
# Tot traficul laboratorului
tcp.port == 9090 || udp.port == 9091

# Doar handshake TCP
tcp.flags.syn == 1

# Doar date (exclude handshake/terminare)
tcp.len > 0

# Retransmisii (probleme de rețea)
tcp.analysis.retransmission

# Pachete cu erori
tcp.analysis.flags

# UDP timeout/fără răspuns
udp.port == 9091 && !udp.srcport == 9091
```

## Deschiderea Capturilor

### Din Windows
```powershell
# Deschideți cu Wireshark
& "C:\Program Files\Wireshark\Wireshark.exe" pcap\week2_capture.pcap
```

### Din Container
```bash
# Analiză rapidă cu tshark
docker exec week2_lab tshark -r /app/pcap/week2_capture.pcap -Y "tcp.port == 9090"
```

## Note

- Fișierele `.pcap` pot fi mari; curățați periodic acest director
- Nu includeți capturi în controlul versiunilor (sunt în `.gitignore`)
- Pentru capturi sensibile, criptați înainte de stocare

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
