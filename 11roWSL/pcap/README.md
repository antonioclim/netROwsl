# Director pentru Capturi de Pachete

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

## Scop

Acest director stochează fișierele de captură (.pcap) generate în timpul exercițiilor de laborator.

## Metode de Captură

### 1. Script Automat

```powershell
python scripts/capture_traffic.py --interface eth0 --duration 60
```

Fișierul va fi salvat ca `week11_TIMESTAMP.pcap`.

### 2. Wireshark GUI

1. Deschideți Wireshark
2. Selectați interfața corespunzătoare
3. Aplicați filtru de captură: `tcp port 8080`
4. Porniți captura
5. Salvați ca `.pcap` în acest director

### 3. tshark CLI

```bash
tshark -i eth0 -w pcap/captura.pcap -f "tcp port 8080" -a duration:60
```

## Analiză Capturi

### Cu tshark

```bash
# Statistici generale
tshark -r captura.pcap -q -z io,stat,1

# Filtrează HTTP
tshark -r captura.pcap -Y http

# Filtrează DNS
tshark -r captura.pcap -Y dns
```

### Cu Wireshark

1. File → Open → selectați fișierul .pcap
2. Aplicați filtre de afișare (vezi mai jos)
3. Analizați conversațiile: Statistics → Conversations

## Filtre Recomandate

| Filtru | Descriere |
|--------|-----------|
| `tcp.port == 8080 && http` | Trafic HTTP prin echilibror |
| `dns` | Tot traficul DNS |
| `http.request` | Doar cereri HTTP |
| `http.response` | Doar răspunsuri HTTP |
| `tcp.flags.syn == 1` | Conexiuni noi TCP |

## Denumire Fișiere

Convenție recomandată:
```
week11_<exercitiu>_<timestamp>.pcap
```

Exemple:
- `week11_ex2_20250106_143000.pcap`
- `week11_failover_demo.pcap`

## Curățare

Pentru a șterge capturile vechi:

```powershell
python scripts/cleanup.py --full
```

Sau manual:
```powershell
del pcap\*.pcap
```

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
