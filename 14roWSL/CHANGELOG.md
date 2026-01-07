# Jurnal de Modificări

Toate modificările notabile ale acestui proiect vor fi documentate în acest fișier.

Formatul se bazează pe [Keep a Changelog](https://keepachangelog.com/ro/1.0.0/).

## [1.0.0] - 2026-01-07

### Adăugat
- Structură inițială pentru laboratorul Săptămânii 14
- Infrastructură Docker cu 5 servicii (app1, app2, lb, echo, client)
- Scripturi Python pentru management: porneste_lab.py, opreste_lab.py, curata.py
- Scripturi de captură trafic și demonstrații
- Documentație completă în limba română
- 4 exerciții de laborator cu verificare automată
- 3 teme pentru acasă cu cod de pornire
- Ghid de depanare cuprinzător
- Rezumat teoretic al conceptelor din curs

### Infrastructură
- Rețea frontend (172.21.0.0/24) pentru client și load balancer
- Rețea backend (172.20.0.0/24) pentru serviciile interne
- Load balancer cu algoritm round-robin
- Health checks pentru monitorizarea sănătății
- Server TCP echo pentru testare protocol

### Documentație
- README.md cu instrucțiuni complete
- Rezumat teoretic (rezumat_teoretic.md)
- Ghid de depanare (depanare.md)
- Rezultate așteptate pentru teste

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
