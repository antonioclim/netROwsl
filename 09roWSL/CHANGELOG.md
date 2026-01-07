# Istoric Modificări

Toate modificările notabile ale acestui proiect vor fi documentate în acest fișier.

Formatul se bazează pe [Keep a Changelog](https://keepachangelog.com/ro/1.0.0/).

## [1.0.0] - 2026-01-07

### Adăugat
- Configurație inițială Docker Compose pentru mediul de laborator FTP
- Scripturi Python pentru gestionarea laboratorului (pornire, oprire, curățare)
- Exerciții pentru nivelul Sesiune (L5) și nivelul Prezentare (L6)
- Demonstrație endianness cu comparație big-endian / little-endian
- Implementare server pseudo-FTP cu gestiunea sesiunii
- Client de test FTP cu suport pentru mod pasiv
- Suite de teste pentru validarea mediului și exercițiilor
- Documentație completă în limba română
- Teme pentru acasă cu specificații detaliate
- Ghid de depanare pentru probleme frecvente
- Fișă de referință rapidă pentru comenzi

### Caracteristici Tehnice
- Suport Docker Compose v2 cu fallback la v1
- Verificare automată a sănătății serviciilor
- Rețea izolată pentru containere (172.29.9.0/24)
- Porturi passive FTP pre-configurate (60000-60010)
- Jurnalizare colorată în terminal
- Mod dry-run pentru operațiuni de curățare

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
