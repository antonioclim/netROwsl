# Istoric Modificări

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Toate modificările notabile ale acestui proiect vor fi documentate în acest fișier.

Formatul este bazat pe [Keep a Changelog](https://keepachangelog.com/ro/1.0.0/).

---

## [1.0.0] - 2025-01-07

### Adăugat
- Versiunea inițială a kit-ului de laborator pentru Săptămâna 12
- Server SMTP educațional cu suport pentru comanda LIST
- Server JSON-RPC 2.0 cu metode de calcul și statistici
- Server XML-RPC cu introspecție activată
- Server gRPC cu serviciul Calculator
- Script de benchmark pentru compararea protocoalelor RPC
- Configurare Docker Compose pentru toate serviciile
- Portainer CE pentru gestionarea vizuală a containerelor
- Scripturi de gestionare: pornește_lab, oprește_lab, curăță
- Script de captură trafic cu suport pentru filtre predefinite
- Script de demonstrații interactive
- Suite de teste cu pytest
- Documentație completă în limba română:
  - README principal cu ghid de laborator
  - Rezumat teoretic
  - Fișă de comenzi
  - Ghid de depanare
  - Lecturi suplimentare
  - Teme pentru acasă

### Caracteristici Tehnice
- Python 3.11+ cerut
- Docker Compose pentru orchestrare
- Rețea Docker izolată (172.28.12.0/24)
- Porturi: SMTP 1025, JSON-RPC 6200, XML-RPC 6201, gRPC 6251

---

## Versiuni Planificate

### [1.1.0] - Planificat
- Suport pentru STARTTLS în serverul SMTP
- Exemple de autentificare pentru servere RPC
- Tutoriale video integrate

### [1.2.0] - Planificat
- Suport pentru streaming gRPC
- Exerciții suplimentare
- Integrare cu platforma de evaluare

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
