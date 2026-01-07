# Rezultate Așteptate - Săptămâna 7

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest document descrie rezultatele așteptate pentru fiecare exercițiu,
ajutându-vă să verificați că ați finalizat corect fiecare pas.

## Exercițiul 1: Conectivitate de Bază

### Rezultat Așteptat în Consolă

```
[2024-01-15 10:30:45] Începere secvență de testare

[2024-01-15 10:30:45] FAZA 1: Testare TCP Echo
[2024-01-15 10:30:45] Test TCP Echo: localhost:9090
[2024-01-15 10:30:45]   Mesaj: 'Salut de la exercitiul 7.01'
[2024-01-15 10:30:45]   Inițiere conexiune (SYN)...
[2024-01-15 10:30:45]   Conexiune stabilită (handshake complet)
[2024-01-15 10:30:46]   Trimitere date: 28 octeți
[2024-01-15 10:30:46]   Așteptare răspuns...
[2024-01-15 10:30:46]   Răspuns primit: 'Salut de la exercitiul 7.01'
[2024-01-15 10:30:47]   Închidere conexiune (FIN)...
[2024-01-15 10:30:47]   [OK] Test TCP reușit
```

### Observații Wireshark

**Trafic TCP (port 9090):**
| Nr. | Sursă | Destinație | Protocol | Info |
|-----|-------|------------|----------|------|
| 1 | Client | Server | TCP | SYN |
| 2 | Server | Client | TCP | SYN, ACK |
| 3 | Client | Server | TCP | ACK |
| 4 | Client | Server | TCP | PSH, ACK (date) |
| 5 | Server | Client | TCP | PSH, ACK (echo) |
| 6 | Client | Server | TCP | FIN, ACK |
| 7 | Server | Client | TCP | FIN, ACK |

**Trafic UDP (port 9091):**
| Nr. | Sursă | Destinație | Protocol | Info |
|-----|-------|------------|----------|------|
| 1 | Client | Server | UDP | Date aplicație |
| 2 | Client | Server | UDP | Date aplicație |
| 3 | Client | Server | UDP | Date aplicație |

*Notă: Nu există handshake pentru UDP!*

---

## Exercițiul 2: Filtrare TCP cu REJECT

### Comportament Așteptat

Când profilul `blocare_tcp_9090` este activ:

1. Clientul trimite pachet SYN
2. Serverul (firewall) răspunde imediat cu RST sau ICMP Port Unreachable
3. Conexiunea eșuează **instant** (milisecunde)

### Observații Wireshark

| Nr. | Sursă | Destinație | Protocol | Info |
|-----|-------|------------|----------|------|
| 1 | Client | Server | TCP | SYN |
| 2 | Server | Client | TCP | RST, ACK |

Sau cu ICMP:

| Nr. | Sursă | Destinație | Protocol | Info |
|-----|-------|------------|----------|------|
| 1 | Client | Server | TCP | SYN |
| 2 | Server | Client | ICMP | Destination unreachable (Port unreachable) |

### Mesaj în Consolă

```
[2024-01-15 10:35:00] Test conexiune TCP (port 9090):
[2024-01-15 10:35:00]   [OK] Conexiune refuzată în 0.003s
[2024-01-15 10:35:00]       Aceasta este comportamentul REJECT tipic
```

---

## Exercițiul 3: Filtrare UDP cu DROP

### Comportament Așteptat

Când profilul `blocare_udp_9091` este activ:

1. Clientul trimite datagramă UDP
2. **Niciun răspuns** - pachetul este eliminat silențios
3. Clientul așteaptă timeout

### Observații Wireshark

| Nr. | Sursă | Destinație | Protocol | Info |
|-----|-------|------------|----------|------|
| 1 | Client | Server | UDP | Date aplicație |

*Notă: Niciun pachet de răspuns! Aceasta este diferența față de REJECT.*

### Mesaj în Consolă

```
[2024-01-15 10:40:00] Test trimitere UDP (port 9091):
[2024-01-15 10:40:02]   [OK] Niciun răspuns primit (posibil DROP)
[2024-01-15 10:40:02]       Aceasta este comportamentul DROP - niciun răspuns!
```

---

## Exercițiul 4: Filtru Nivel Aplicație

### Comportament Așteptat

**Cerere cu conținut permis:**
- Conexiune TCP se stabilește (SYN-SYN/ACK-ACK)
- Date trimise și primite
- Răspuns HTTP 200 OK

**Cerere cu conținut blocat (ex: "malware"):**
- Conexiune TCP se stabilește (handshake complet!)
- Date trimise
- Răspuns HTTP 403 Forbidden

### Diferența Cheie

Spre deosebire de filtrarea la nivel rețea (iptables), filtrarea la nivel
aplicație permite stabilirea conexiunii TCP. Blocarea se face după ce 
conținutul este analizat.

### Observații Wireshark

Ambele tipuri de cereri arată identic la nivel TCP:

| Nr. | Sursă | Destinație | Protocol | Info |
|-----|-------|------------|----------|------|
| 1 | Client | Proxy | TCP | SYN |
| 2 | Proxy | Client | TCP | SYN, ACK |
| 3 | Client | Proxy | TCP | ACK |
| 4 | Client | Proxy | TCP | PSH, ACK (cerere) |
| 5 | Proxy | Client | TCP | PSH, ACK (răspuns 200/403) |

---

## Exercițiul 5: Sondare Porturi

### Rezultate Așteptate

```
[2024-01-15 10:45:00] Începere sondare: localhost porturi 9085-9095
[2024-01-15 10:45:00] Total porturi: 11, Timeout: 1.0s per port

  Port 9085: închis
  Port 9086: închis
  ...
  Port 9090: DESCHIS
  Port 9091: închis (UDP nu răspunde la sondare TCP)
  ...
  Port 9095: închis

SUMAR SONDARE
═════════════════════════════════════════
  Porturi deschise:  1
    9090
  Porturi închise:   9
  Porturi filtrate:  1
```

### Interpretare Stări

| Stare | Răspuns | Interpretare |
|-------|---------|--------------|
| DESCHIS | SYN-ACK | Serviciu activ, acceptă conexiuni |
| ÎNCHIS | RST | Niciun serviciu, dar portul accesibil |
| FILTRAT | Timeout | Regulă DROP activă sau host inaccesibil |

---

## Comparație REJECT vs DROP

### Tabel Rezumat

| Aspect | REJECT | DROP |
|--------|--------|------|
| Răspuns trimis | Da (RST/ICMP) | Nu |
| Timp până la eșec | Instant (~ms) | Timeout (secunde) |
| Informează atacatorul | Da - arată că există firewall | Nu - pare problemă de rețea |
| Experiență utilizator | Eșec rapid, clar | Așteptare lungă, confuz |
| Consum resurse atacator | Scăzut | Ridicat (trebuie să aștepte) |
| Recomandare | Rețele interne, debug | Servicii publice, securitate |

### Output Test Rapid

```
╔══════════════════════════════════════════════════════════╗
║   TEST RAPID - Săptămâna 7                               ║
║   Curs REȚELE DE CALCULATOARE - ASE, Informatică         ║
╚══════════════════════════════════════════════════════════╝

[10:50:00] [OK] Docker rulează
[10:50:01] [OK]   Server TCP rulează
[10:50:01] [OK]   Receptor UDP rulează
[10:50:02] [OK]   Port 9090/tcp (Server TCP Echo) accesibil
[10:50:02] [OK]   Port 9091/udp (Receptor UDP) accesibil
[10:50:02] [OK]   Python 3.11

═════════════════════════════════════════════════════════════
  REZULTAT: Mediul este pregătit pentru laborator!
═════════════════════════════════════════════════════════════
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
