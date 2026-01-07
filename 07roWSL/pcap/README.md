# Director pentru Capturi de Pachete

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest director stochează capturile de pachete (.pcap) generate în timpul exercițiilor de laborator.

## Convenții de Denumire

Folosiți următorul format pentru numele fișierelor:

```
saptamana7_ex<NUMAR>_<DESCRIERE>.pcap
```

Exemple:
- `saptamana7_ex1_referinta.pcap` - Captură de bază fără filtrare
- `saptamana7_ex2_tcp_reject.pcap` - Captură cu REJECT pe TCP
- `saptamana7_ex3_udp_drop.pcap` - Captură cu DROP pe UDP
- `saptamana7_ex4_filtru_aplicatie.pcap` - Captură cu filtrare la nivel aplicație
- `saptamana7_ex5_sondare_porturi.pcap` - Captură sondare porturi

## Comenzi Utile

### Capturare cu tcpdump

```bash
# Captură pe toate interfețele, portul 9090
tcpdump -i any port 9090 -w saptamana7_captura.pcap

# Captură cu filtru complex
tcpdump -i eth0 'port 9090 or port 9091' -w saptamana7_multi.pcap

# Captură cu limit de pachete
tcpdump -i any -c 1000 port 9090 -w saptamana7_limitat.pcap
```

### Capturare cu tshark

```bash
# Captură cu durată limitată
tshark -i eth0 -a duration:60 -w saptamana7_60s.pcap

# Captură doar TCP SYN
tshark -i eth0 -f "tcp[tcpflags] & (tcp-syn) != 0" -w saptamana7_syn.pcap
```

### Analiza Capturilor

```bash
# Statistici despre captură
capinfos saptamana7_ex1_referinta.pcap

# Afișare pachete cu tshark
tshark -r saptamana7_ex1_referinta.pcap

# Filtrare la citire
tshark -r captura.pcap -Y "tcp.port == 9090"
```

## Filtre Wireshark Recomandate

### Filtre de Bază

```
# Trafic TCP pe portul echo
tcp.port == 9090

# Trafic UDP pe portul receptor
udp.port == 9091

# Tot traficul relevant pentru laborator
tcp.port == 9090 or udp.port == 9091 or tcp.port == 8888
```

### Filtre pentru Analiza Handshake

```
# Doar pachete SYN (începuturi de conexiune)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Pachete SYN-ACK
tcp.flags.syn == 1 && tcp.flags.ack == 1

# Pachete RST (reset-uri)
tcp.flags.reset == 1
```

### Filtre pentru Analiza Filtrării

```
# Mesaje ICMP de eroare
icmp.type == 3

# ICMP Port Unreachable
icmp.type == 3 && icmp.code == 3

# Toate erorile ICMP
icmp.type >= 3 && icmp.type <= 5
```

### Filtre pentru Comparație REJECT vs DROP

```
# Pentru REJECT - căutați RST sau ICMP
tcp.flags.reset == 1 or icmp

# Pentru DROP - verificați retransmisii TCP
tcp.analysis.retransmission
```

## Sfaturi de Analiză

1. **Verificați timestamp-urile**
   - REJECT: Răspuns în milisecunde
   - DROP: Timeout de secunde

2. **Urmăriți secvența de pachete**
   - Folosiți "Follow TCP Stream" pentru conversații complete

3. **Comparați capturi**
   - Deschideți două instanțe Wireshark pentru comparație

4. **Exportați statistici**
   - Statistics → Protocol Hierarchy
   - Statistics → Conversations

## Structura Așteptată

După finalizarea exercițiilor, ar trebui să aveți:

```
pcap/
├── saptamana7_ex1_referinta.pcap
├── saptamana7_ex2_tcp_reject.pcap
├── saptamana7_ex3_udp_drop.pcap
├── saptamana7_ex4_filtru_aplicatie.pcap
└── saptamana7_ex5_sondare_porturi.pcap
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
