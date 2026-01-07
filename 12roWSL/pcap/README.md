# Director pentru Capturi de Pachete

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

## Descriere

Acest director este destinat stocării capturilor de pachete realizate în timpul sesiunilor de laborator.

## Convenții de Denumire

```
week12_<protocol>_<descriere>_<timestamp>.pcap
```

## Metode de Captură

### Folosind scriptul inclus
```bash
python scripts/captura_trafic.py --protocol smtp --durata 60
```

### Filtre Wireshark

```
# SMTP
tcp.port == 1025

# JSON-RPC / XML-RPC
tcp.port == 6200 or tcp.port == 6201

# gRPC
tcp.port == 6251
```

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
