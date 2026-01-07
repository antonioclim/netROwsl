# Director Capturi de Pachete

> Stocați aici capturile de trafic pentru analiză
> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Convenții de Denumire

Folosiți următorul format pentru fișierele de captură:

```
saptamana9_<descriere>_<data>.pcap
```

Exemple:
- `saptamana9_ftp_sesiune_20260107.pcap`
- `saptamana9_mod_pasiv_20260107.pcap`
- `saptamana9_multi_client_20260107.pcap`

## Filtre Wireshark Recomandate

### FTP Control
```
ftp
tcp.port == 2121
```

### FTP Data
```
ftp-data
tcp.port >= 60000 and tcp.port <= 60010
```

### Autentificare
```
ftp.request.command == "USER" or ftp.request.command == "PASS"
```

## Note

- Fișierele din acest director sunt ignorate de Git (prin .gitkeep)
- Salvați capturile importante în altă locație
- Acest director se curăță la fiecare `python scripts/curata.py --complet`

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
