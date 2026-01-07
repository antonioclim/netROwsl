# Director Capturi de Pachete

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

## Scop

Acest director este destinat stocării fișierelor de captură de pachete (.pcap, .pcapng) 
generate în timpul laboratorului.

## Denumire Fișiere

Convențiile de denumire recomandate:

```
<protocol>_<descriere>_<data>.pcap
```

Exemple:
- `text_proto_ping_20240115.pcap` - Captură PING pe protocolul TEXT
- `binary_proto_set_get_20240115.pcap` - Captură SET/GET pe protocolul BINAR  
- `udp_sensor_burst_20240115.pcap` - Captură rafală senzori UDP

## Cum se Capturează

### Cu Wireshark (GUI)

1. Deschideți Wireshark
2. Selectați interfața "Loopback" sau "Npcap Loopback Adapter"
3. Aplicați filtrul de capturare: `port 5400 or port 5401 or port 5402`
4. Porniți capturarea
5. Executați exercițiul
6. Opriți capturarea
7. Salvați: File → Save As → `nume_descriptiv.pcap`

### Cu tcpdump (CLI)

```bash
# Capturare pe toate interfețele, porturi laborator
sudo tcpdump -i any port 5400 or port 5401 or port 5402 -w captura.pcap

# Capturare cu limită de timp (60 secunde)
sudo tcpdump -i any port 5400 -w captura.pcap -G 60 -W 1

# Capturare cu limită de pachete (100)
sudo tcpdump -i any port 5400 -w captura.pcap -c 100
```

### Cu tshark (CLI)

```bash
# Capturare simplă
tshark -i any -f "port 5400" -w captura.pcap

# Capturare cu durată
tshark -i any -f "port 5400" -a duration:60 -w captura.pcap
```

## Cum se Analizează

### Cu Wireshark

1. Deschideți fișierul .pcap
2. Aplicați filtre de afișare:
   - Protocol TEXT: `tcp.port == 5400`
   - Protocol BINAR: `tcp.port == 5401`
   - Senzori UDP: `udp.port == 5402`

3. Urmăriți fluxul TCP: Click dreapta → Follow → TCP Stream

### Cu tshark

```bash
# Afișare text
tshark -r captura.pcap

# Extragere câmpuri specifice
tshark -r captura.pcap -T fields -e ip.src -e ip.dst -e tcp.port

# Statistici conversații
tshark -r captura.pcap -q -z conv,tcp

# Urmărire flux
tshark -r captura.pcap -z follow,tcp,ascii,0
```

## Capturi de Referință

După completarea fiecărui exercițiu, salvați capturile pentru referință:

| Fișier | Descriere |
|--------|-----------|
| `ex1_text_ping.pcap` | PING/PONG pe protocolul TEXT |
| `ex1_text_set_get.pcap` | Operațiuni SET/GET |
| `ex2_binary_messages.pcap` | Diverse mesaje binare |
| `ex3_udp_sensors.pcap` | Datagrame senzori |
| `ex4_crc_corrupt.pcap` | Mesaje cu CRC corupt |

## Note

- Fișierele .pcap pot deveni mari rapid. Limitați capturările la ce este necesar.
- Acest director este în .gitignore (dacă se folosește Git).
- Capturile pot conține date sensibile - nu le partajați public.

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
