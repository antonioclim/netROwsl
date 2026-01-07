# Director Capturi de Pachete

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest director stochează fișierele de captură de pachete (.pcap) generate în timpul sesiunilor de laborator.

## Utilizare

### Generare Captură

```powershell
python scripts/captura_trafic.py --durata 30 --iesire pcap/demo.pcap
```

### Vizualizare în Wireshark

```powershell
& "C:\Program Files\Wireshark\Wireshark.exe" pcap/demo.pcap
```

### Analiză cu tshark

```bash
tshark -r pcap/demo.pcap -Y "http"
tshark -r pcap/demo.pcap -q -z conv,tcp
```

## Fișiere Generate

Capturele vor fi salvate aici cu nume descriptive:
- `demo.pcap` - Captură din demonstrație
- `http_trafic.pcap` - Trafic HTTP
- `echo_sesiune.pcap` - Sesiune TCP echo

## Curățare

Fișierele din acest director sunt curățate automat cu:

```powershell
python scripts/curata.py --complet
```

---

*Laborator Rețele de Calculatoare - ASE | by Revolvix*
