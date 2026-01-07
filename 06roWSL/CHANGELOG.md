# Jurnal de modificări

Toate modificările notabile la Kit-ul WSL Săptămâna 6 vor fi documentate în acest fișier.

Formatul se bazează pe [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
iar acest proiect aderă la [Versionare Semantică](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-2026

### Adăugate

- Mediu de laborator complet compatibil WSL2 pentru Săptămâna 6
- Configurare Docker Compose cu suport pentru containere privilegiate
- Scripturi de gestionare bazate pe Python (start_lab.py, stop_lab.py, cleanup.py)
- Topologie NAT/PAT cu demonstrație MASQUERADE
- Topologie SDN cu politici OpenFlow 1.3
- Aplicații echo TCP/UDP pentru testarea conectivității
- Aplicație observator NAT pentru vizualizarea traducerii PAT
- Implementare controller politici SDN (OS-Ken)
- README comprehensiv cu obiective de învățare și exerciții
- Teste automate rapide și verificare exerciții
- Documentație de depanare

### Infrastructură

- Dockerfile cu bază Ubuntu 22.04
- Integrare Mininet și Open vSwitch
- Suport Portainer pentru administrarea containerelor
- Integrare Wireshark pentru capturarea pachetelor

### Documentație

- Sumar teoretic pentru concepte NAT/PAT și SDN
- Fișă de comenzi pentru operațiuni comune
- Documentație pentru output-urile așteptate
- Referințe pentru lectură suplimentară

---

Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix
