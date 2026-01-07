# Stocare capturi de pachete

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Scop

Acest director stochează capturile de pachete (fișiere PCAP) generate în timpul exercițiilor de laborator și demonstrațiilor.

## Convenție de denumire

Folosește următorul format pentru fișierele de captură:

```
sapt6_<exercitiu>_<timestamp>.pcap
```

Exemple:
- `sapt6_demo_nat_20250107_1430.pcap`
- `sapt6_politici_sdn_20250107_1445.pcap`
- `sapt6_traducere_pat_20250107_1500.pcap`

## Capturarea traficului

### Din interiorul topologiei Mininet

```bash
# Pe un host specific
mininet> h1 tcpdump -i h1-eth0 -w /pcap/captura.pcap &

# Pe interfața publică a routerului NAT
mininet> rnat tcpdump -i rnat-eth1 -w /pcap/nat_public.pcap &
```

### Folosind scriptul de captură

```powershell
python scripts/capture_traffic.py --interface eth0 --output pcap/sapt6_captura.pcap
```

### Folosind Wireshark (Windows)

1. Deschide Wireshark
2. Selectează interfața de rețea Docker
3. Pornește captura
4. Salvează în acest director când e completă

## Sfaturi pentru analiză

### Filtre Wireshark utile pentru Săptămâna 6

```
# Analiză NAT
ip.addr == 203.0.113.0/24        # Trafic rețea publică
ip.addr == 192.168.1.0/24        # Trafic rețea privată
tcp.port == 5000                  # Trafic observator NAT

# Analiză SDN
ip.addr == 10.0.6.0/24           # Subrețea SDN
openflow_v4                       # Mesaje OpenFlow
tcp.port == 6633 || tcp.port == 6653  # Trafic controller

# Specific protocolului
icmp                              # Trafic ping
tcp.flags.syn == 1               # Încercări de conexiune TCP
```

## Curățare

Înainte de următoarea sesiune de laborator:

```powershell
python scripts/cleanup.py --full
```

Aceasta elimină toate fișierele PCAP din acest director.

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
