# Ghid Pair Programming - Săptămâna 13

> Laborator IoT și Securitate în Rețelele de Calculatoare
>
> Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

---

## Ce este Pair Programming?

Pair Programming este o tehnică în care doi programatori lucrează împreună la același calculator:
- **Driver** — scrie cod, execută comenzi
- **Navigator** — verifică, sugerează, consultă documentația

Studiile arată că pair programming reduce erorile cu 15% și îmbunătățește învățarea conceptelor noi.

---

## Reguli de Bază

### Roluri și Responsabilități

| Rol | Ce face | Ce NU face |
|-----|---------|-----------|
| **Driver** | Tastează, execută comenzi, explică ce face | NU ia decizii majore singur |
| **Navigator** | Verifică erori, sugerează îmbunătățiri, ține evidența progresului | NU preia tastatura fără permisiune |

### Rotație

- **Schimb la fiecare 10 minute** (folosiți un timer!)
- La schimb, Navigator-ul rezumă în 30 secunde ce s-a făcut
- Dacă Driver-ul e blocat >2 minute, Navigator-ul poate sugera soluții

### Comunicare

- Driver-ul verbalizează ce face: "Acum rulez scanarea pe portul 1883..."
- Navigator-ul pune întrebări: "De ce ai ales timeout 0.5 în loc de 1.0?"
- Ambii discută ÎNAINTE de a face schimbări majore

---

## Exerciții Structurate pentru Perechi

### Exercițiul 1: Scanner Porturi TCP (30 minute)

**Obiectiv:** Înțelegerea scanării de porturi și interpretarea rezultatelor

| Etapă | Timp | Driver face | Navigator verifică |
|-------|------|-------------|-------------------|
| 1 | 5 min | Rulează: `python3 src/exercises/ex_13_01_scanner_porturi.py --tinta localhost --porturi 1883,8883,8080,2121,6200` | Notează porturile raportate ca DESCHISE |
| 2 | 5 min | Modifică timeout la 0.5s și rerulează | Compară timpul total de execuție |
| **SCHIMB** | — | — | — |
| 3 | 5 min | Scanează interval: `--porturi 1-100` | Identifică servicii necunoscute |
| 4 | 5 min | Exportă în JSON: `--output rezultat.json` | Validează structura JSON |
| **SCHIMB** | — | — | — |
| 5 | 5 min | Analizează JSON cu `cat` sau Python | Calculează rata porturi deschise/total |
| 6 | 5 min | Documentează concluziile | Verifică acuratețea notițelor |

**Întrebări de discutat:**
1. De ce unele porturi apar ca "filtrate" în loc de "închise"?
2. Ce s-ar întâmpla dacă am scana un host extern fără autorizare?

---

### Exercițiul 2: Client MQTT (35 minute)

**Obiectiv:** Înțelegerea modelului publish/subscribe și diferențelor TLS

| Etapă | Timp | Driver face | Navigator verifică |
|-------|------|-------------|-------------------|
| 1 | 5 min | Deschide 2 terminale Ubuntu | Confirmă că ambele sunt în folderul corect |
| 2 | 5 min | Terminal 1: `--mod subscribe --topic "test/#"` | Observă mesajul de conectare |
| **SCHIMB** | — | — | — |
| 3 | 5 min | Terminal 2: `--mod publish --topic "test/temp" --mesaj "23.5"` | Verifică că mesajul apare în Terminal 1 |
| 4 | 5 min | Publică 3 mesaje cu QoS diferit (0, 1, 2) | Notează diferențele de confirmare |
| **SCHIMB** | — | — | — |
| 5 | 5 min | Oprește subscribe, reconectează cu `--port 8883 --tls` | Verifică mesajul TLS activat |
| 6 | 5 min | Deschide Wireshark pe `vEthernet (WSL)` | Capturează trafic |
| **SCHIMB** | — | — | — |
| 7 | 5 min | Publică pe 1883 (text clar) și 8883 (TLS) | Compară pachetele în Wireshark |

**Întrebări de discutat:**
1. Ce informații poți vedea în pachetele MQTT necriptate?
2. De ce portul 8883 arată "Application Data" în loc de payload?

---

### Exercițiul 3: Sniffer Pachete (25 minute)

**Obiectiv:** Analiza traficului de rețea la nivel de pachete

| Etapă | Timp | Driver face | Navigator verifică |
|-------|------|-------------|-------------------|
| 1 | 5 min | Rulează: `sudo python3 src/exercises/ex_13_03_sniffer_pachete.py --numar 20` | Notează tipurile de pachete capturate |
| 2 | 5 min | Generează trafic MQTT în alt terminal | Observă pachetele TCP noi |
| **SCHIMB** | — | — | — |
| 3 | 5 min | Filtrează doar TCP: `--filtru "tcp"` | Compară cu captură nefiltrata |
| 4 | 5 min | Salvează în PCAP: `--output captura.pcap` | Verifică că fișierul există |
| **SCHIMB** | — | — | — |
| 5 | 5 min | Deschide `captura.pcap` în Wireshark (Windows) | Compară cu output-ul din terminal |

**Întrebări de discutat:**
1. Ce informații sunt vizibile în header-ul IP?
2. De ce sniffer-ul necesită permisiuni root/sudo?

---

### Exercițiul 4: Verificator Vulnerabilități (30 minute)

**Obiectiv:** Identificarea și raportarea problemelor de securitate

| Etapă | Timp | Driver face | Navigator verifică |
|-------|------|-------------|-------------------|
| 1 | 5 min | Rulează: `python3 src/exercises/ex_13_04_verificator_vulnerabilitati.py --tinta localhost --toate` | Notează vulnerabilitățile găsite |
| 2 | 5 min | Analizează output-ul pe severități | Sortează: CRITIC > RIDICAT > MEDIU |
| **SCHIMB** | — | — | — |
| 3 | 5 min | Testează doar FTP: `--ftp --port 2121` | Verifică detecția backdoor |
| 4 | 5 min | Testează doar MQTT: `--mqtt --port 1883` | Verifică raportul TLS |
| **SCHIMB** | — | — | — |
| 5 | 5 min | Exportă raport: `--output raport.json` | Validează JSON și completitudinea |
| 6 | 5 min | Discută remedierea pentru fiecare vulnerabilitate | Documentează soluțiile propuse |

**Întrebări de discutat:**
1. Care vulnerabilitate are cel mai mare risc real? De ce?
2. Cum ai remedia problema backdoor-ului FTP într-un mediu de producție?

---

## Evaluare Pair Programming

La sfârșitul fiecărui exercițiu, discutați:

### Pentru Driver:
- Am explicat clar ce fac în timp ce tastez?
- Am ascultat sugestiile Navigator-ului?
- Am cedat controlul la schimb fără rezistență?

### Pentru Navigator:
- Am oferit feedback constructiv, nu critic?
- Am evitat să preiau tastatura fără permisiune?
- Am ținut evidența progresului și a timpului?

### Pentru echipă:
- Am învățat ceva nou unul de la altul?
- Am rezolvat blocajele prin comunicare?
- Am terminat exercițiul în timpul alocat?

---

## Probleme Frecvente și Soluții

| Problemă | Soluție |
|----------|---------|
| Driver-ul tastează prea repede | Navigator cere explicații la fiecare pas |
| Navigator-ul preia controlul | Folosiți un obiect fizic (pix) ca "token" — doar cine îl are tastează |
| Unul știe mai mult decât celălalt | Cel avansat explică, cel începător pune întrebări |
| Comunicare deficitară | Stabiliți o regulă: "Nu tastăm nimic fără să spunem ce facem" |
| Dezacord asupra soluției | Încercați ambele variante și comparați rezultatele |

---

## Resurse

- Williams, L. & Kessler, R. (2002). Pair Programming Illuminated
- Cockburn, A. & Williams, L. (2000). The Costs and Benefits of Pair Programming
- Hanks, B. et al. (2011). Pair Programming in Education

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix*
