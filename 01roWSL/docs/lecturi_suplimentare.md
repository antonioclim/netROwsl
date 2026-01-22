# Lecturi Suplimentare - Săptămâna 1

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

---

## Cărți Recomandate

### Nivel Introductiv

**Computer Networking: A Top-Down Approach** — Kurose & Ross
- Pornește de la aplicații și coboară spre hardware
- Bună pentru primii pași în networking
- Ediția 7 sau 8 preferată
- Capitolele relevante pentru Săpt. 1: 1-3

**TCP/IP Illustrated, Volume 1** — W. Richard Stevens
- Clasic absolut pentru înțelegerea protocoalelor
- Multe diagrame și exemple practice
- Referință pentru stiva TCP/IP

### Nivel Avansat

**Computer Networks** — Tanenbaum & Wetherall: Acoperire completă de la Layer 1 la Layer 7. Mai academic, dar extrem de solid ca fundament teoretic.

**Unix Network Programming** — Stevens, Fenner, Rudoff: Biblia programării socket-urilor. Exemple extinse în C, dar conceptele se aplică și în Python.

---

## Documentație Online

### RFC-uri Esențiale

| RFC | Titlu | Relevant Pentru |
|-----|-------|-----------------|
| 791 | Internet Protocol | Structura pachetelor IP |
| 793 | Transmission Control Protocol | Stări, handshake, control flux |
| 768 | User Datagram Protocol | Protocol simplu, fără conexiune |
| 1918 | Private Addresses | Adrese IP private (172.20.x.x din lab) |

Link: https://www.rfc-editor.org/

**Cum să citești un RFC:** Nu citi de la cap la coadă. Sari la secțiunea relevantă (ex: pentru handshake, caută "Connection Establishment" în RFC 793).

### Tutoriale Practice

**Wireshark Documentation** — https://www.wireshark.org/docs/
- Ghid utilizator complet pentru începători
- Display filters reference (salvează-l ca bookmark!)

**Docker Networking** — https://docs.docker.com/network/
- Bridge, host, overlay networks
- Troubleshooting connectivity

**Python Socket Programming** — https://docs.python.org/3/library/socket.html

**Vezi și:** `fisa_comenzi.md` pentru comenzile practice din laborator

---

## Cursuri Video Gratuite

**Stanford CS144 - Introduction to Computer Networking**
- Gratuit pe YouTube
- Acoperire solidă a fundamentelor
- Laboratoare practice asemănătoare cu ale noastre

**MIT OCW 6.829 - Computer Networks** — Nivel mai avansat, focus pe cercetare și optimizare. Recomandat după ce termini cursul nostru.

---

## Instrumente de Învățare

### Simulatoare

**Packet Tracer** (Cisco) — Simulare rețele complete. Gratuit pentru studiu, interfață vizuală intuitivă. Ideal pentru a vedea cum circulă pachetele.

**GNS3** — Emulare echipamente reale. Mai complex decât Packet Tracer, dar mai realist pentru scenarii avansate.

### Laboratoare Online

**TryHackMe** — Network Fundamentals Path: Exerciții interactive, nivel începător-intermediar.

**Hack The Box** — Starting Point: Provocări practice cu focus pe securitate.

---

## Resurse pentru Examen

### Concepte de Revizuit

Acestea sunt conceptele esențiale pe care le vei întâlni în evaluări:

1. **Modelul TCP/IP** — cele 4 straturi și funcțiile lor
2. **Adresare IP** — notație CIDR, subnetting, adrese private vs. publice
3. **TCP vs UDP** — când folosești fiecare și de ce
4. **Handshake TCP** — cei 3 pași, sequence numbers, de ce sunt necesari
5. **Socket Programming** — bind, listen, accept, connect
6. **Analiza traficului** — interpretarea capturilor Wireshark/tcpdump

**Vezi și:** `intrebari_peer_instruction.md` pentru întrebări de auto-evaluare

### Exerciții Recomandate pentru Practică

- Calculează adrese de subrețea manual (cel puțin 5 exemple)
- Desenează diagrama handshake-ului TCP din memorie
- Scrie un server echo TCP în Python fără a te uita la documentație
- Analizează o captură PCAP: identifică handshake-ul, datele, închiderea

**Vezi și:** `README.md` Exercițiul 5 (trace) pentru practică de analiză

---

## Comunități și Forumuri

- **r/networking** — Reddit, comunitate activă pentru întrebări
- **Network Engineering Stack Exchange** — Q&A tehnic
- **Server Fault** — pentru întrebări de administrare sisteme

**Sfat:** Înainte de a pune o întrebare, caută dacă nu a mai fost răspunsă. 90% din întrebările începătorilor au deja răspunsuri excelente.

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix | 2025*
