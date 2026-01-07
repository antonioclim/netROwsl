# Jurnal de Modificări

Toate modificările notabile ale acestui proiect sunt documentate în acest fișier.

Formatul se bazează pe [Keep a Changelog](https://keepachangelog.com/ro/1.0.0/).

## [1.0.0] - 2025-01-06

### Adăugat
- Structură inițială a kit-ului pentru Săptămâna 2
- Server TCP concurent cu suport pentru moduri threaded și iterativ
- Server UDP cu protocol personalizat (ping, upper, lower, reverse, echo, time)
- Scripturi de management: start_lab.py, stop_lab.py, cleanup.py
- Demonstrații automate pentru prezentări la curs
- Script de captură trafic cu integrare Wireshark
- Documentație completă în limba română
- Teste de funcționalitate și smoke tests
- Configurație Docker cu Portainer CE
- Teme pentru acasă cu cerințe detaliate

### Configurație Docker
- Container `week2_lab` bazat pe Python 3.11-slim-bookworm
- Portainer CE pentru management vizual
- Rețea dedicată `week2_network` (10.0.2.0/24)
- Porturi expuse: 9090/TCP, 9091/UDP, 9443/HTTPS (Portainer)

### Instrumente Incluse
- tcpdump pentru captură pachete din container
- tshark pentru analiză în linia de comandă
- netcat pentru testare rapidă conexiuni
- iproute2 pentru configurare rețea

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
