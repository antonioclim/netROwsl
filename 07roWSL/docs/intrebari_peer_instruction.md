# Întrebări Peer Instruction - Săptămâna 7

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix
>
> Aceste întrebări sunt proiectate pentru metoda Peer Instruction (Mazur).
> Timing recomandat: Prezentare (1 min) → Vot individual (1 min) → Discuție în perechi (3 min) → Revot (30 sec) → Explicație (2 min)

---

## Întrebarea 1: Comportamentul DROP

### Scenariu

Ai configurat următoarea regulă pe un server Linux:
```bash
iptables -A INPUT -p tcp --dport 9090 -j DROP
```

Un client încearcă să se conecteze la portul 9090 de pe acest server.

### Întrebare

Ce va vedea clientul în Wireshark?

### Opțiuni

| | Opțiune |
|---|---------|
| **A** | SYN → RST (eșec instant, "Connection refused") |
| **B** | SYN → SYN-ACK → ACK (conexiune reușită) |
| **C** | SYN → [pauză 3s] → SYN → [pauză 6s] → SYN → ... (retransmisii până la timeout) |
| **D** | SYN → ICMP "Destination Port Unreachable" |

---

### Răspuns Corect: **C**

### Explicație Post-Vot

- **A** — Aceasta ar fi comportamentul **REJECT**, nu DROP. REJECT trimite RST.
- **B** — Ar însemna că nu există nicio regulă de blocare.
- **C** ✅ — **DROP elimină silențios pachetul**. Clientul nu primește niciun răspuns, așa că retransmite SYN-ul (backup exponențial: 3s, 6s, 12s...) până la timeout (~30-60s).
- **D** — Aceasta ar fi `REJECT --reject-with icmp-port-unreachable`.

### Note Instructor

**Misconceptie vizată:** Mulți studenți confundă DROP cu REJECT și cred că DROP trimite RST.

**Demonstrație practică:**
```bash
# Aplică DROP și observă în Wireshark cu filtrul: tcp.port == 9090
sudo iptables -A INPUT -p tcp --dport 9090 -j DROP
# Din alt terminal: nc -zv localhost 9090
# Vei vedea multiple SYN fără răspuns
```

**Întrebare de follow-up:** "De ce ar alege cineva DROP în loc de REJECT?"
- Răspuns: DROP nu dezvăluie prezența firewall-ului (stealth), dar REJECT oferă experiență mai bună utilizatorilor legitimi.

---

## Întrebarea 2: REJECT vs DROP - Timp de Răspuns

### Scenariu

Ai două servere identice. Pe Server A ai configurat:
```bash
iptables -A INPUT -p tcp --dport 80 -j REJECT
```

Pe Server B ai configurat:
```bash
iptables -A INPUT -p tcp --dport 80 -j DROP
```

Un client încearcă să se conecteze la portul 80 pe ambele servere.

### Întrebare

Care server va raporta eroarea mai rapid clientului?

### Opțiuni

| | Opțiune |
|---|---------|
| **A** | Server A (REJECT) - eroare în milisecunde |
| **B** | Server B (DROP) - eroare în milisecunde |
| **C** | Ambele raportează eroarea în același timp |
| **D** | Niciun server nu raportează eroare, conexiunea reușește |

---

### Răspuns Corect: **A**

### Explicație Post-Vot

- **A** ✅ — **REJECT trimite RST imediat** (milisecunde). Clientul primește "Connection refused" aproape instant.
- **B** — DROP nu trimite nimic. Clientul trebuie să aștepte **timeout-ul TCP** (~30-75 secunde, depinde de SO).
- **C** — Comportamentul este complet diferit.
- **D** — Ambele blochează conexiunea.

### Note Instructor

**Demonstrație timing:**
```bash
# Terminal 1 - REJECT
time nc -zv server_a 80
# Output: ~0.01s

# Terminal 2 - DROP  
time nc -zv server_b 80
# Output: ~30-75s (timeout)
```

**Întrebare de discuție:** "Din perspectiva unui atacator, care comportament e mai informativ?"
- REJECT dezvăluie că sistemul există și are firewall activ
- DROP lasă atacatorul în incertitudine

---

## Întrebarea 3: Filtrare Nivel Aplicație vs Nivel Rețea

### Scenariu

Ai configurat un proxy de filtrare (filtru_pachete.py) care blochează cererile ce conțin cuvântul "attack". Un client trimite:

```
GET /page?q=attack HTTP/1.1
Host: localhost:8888
```

### Întrebare

Ce vei vedea în Wireshark?

### Opțiuni

| | Opțiune |
|---|---------|
| **A** | SYN → RST (conexiune refuzată înainte să se stabilească) |
| **B** | SYN → SYN-ACK → ACK → HTTP Request → HTTP 403 Forbidden → FIN |
| **C** | Niciun pachet (DROP silențios) |
| **D** | SYN → SYN-ACK → ACK → [timeout, niciun răspuns HTTP] |

---

### Răspuns Corect: **B**

### Explicație Post-Vot

- **A** — Ar fi filtrare la nivel **rețea** (iptables REJECT), nu aplicație.
- **B** ✅ — **Filtrarea la nivel aplicație** operează DUPĂ ce conexiunea TCP s-a stabilit. Vedem:
  1. Handshake complet (SYN, SYN-ACK, ACK)
  2. Cererea HTTP trimisă
  3. Răspuns 403 de la proxy
  4. Închidere grațioasă (FIN)
- **C** — Ar fi iptables DROP.
- **D** — Proxy-ul răspunde, nu ignoră cererea.

### Note Instructor

**Concept cheie:** Diferența între nivelurile OSI:
- iptables (L3-L4): Decide pe baza IP/port ÎNAINTE de handshake
- Proxy/WAF (L7): Decide pe baza CONȚINUTULUI DUPĂ handshake

**Analogie:** 
- iptables = paznicul de la intrarea în clădire (verifică legitimația)
- Proxy = scanner-ul de bagaje (verifică conținutul)

Poți trece de paznic dar să fii oprit la scanner!

---

## Întrebarea 4: Sondarea Porturilor - Interpretare Rezultate

### Scenariu

Rulezi o sondare de porturi și observi următoarele răspunsuri:

| Port | Răspuns |
|------|---------|
| 22 | SYN-ACK |
| 80 | RST |
| 443 | [timeout, niciun răspuns] |

### Întrebare

Care este starea fiecărui port?

### Opțiuni

| | Opțiune |
|---|---------|
| **A** | 22: DESCHIS, 80: ÎNCHIS, 443: FILTRAT |
| **B** | 22: DESCHIS, 80: FILTRAT, 443: ÎNCHIS |
| **C** | 22: ÎNCHIS, 80: DESCHIS, 443: FILTRAT |
| **D** | Toate trei sunt FILTRATE |

---

### Răspuns Corect: **A**

### Explicație Post-Vot

| Port | Răspuns | Interpretare |
|------|---------|--------------|
| 22 | SYN-ACK | **DESCHIS** — Serviciu activ, acceptă conexiuni |
| 80 | RST | **ÎNCHIS** — Niciun serviciu, dar sistemul răspunde |
| 443 | timeout | **FILTRAT** — Firewall DROP activ |

- **A** ✅ — Interpretare corectă
- **B** — Confundă RST (închis) cu filtrat
- **C** — Inversează deschis cu închis
- **D** — Ignoră că primim răspunsuri de la 22 și 80

### Note Instructor

**Tabel de referință:**

| Răspuns | Stare Port | Ce înseamnă |
|---------|------------|-------------|
| SYN-ACK | DESCHIS | Serviciu activ |
| RST | ÎNCHIS | Niciun serviciu, niciun firewall |
| Timeout | FILTRAT | Firewall DROP |
| ICMP Unreachable | FILTRAT | Firewall REJECT |

**Discuție:** De ce e importantă distincția pentru un administrator de securitate?

---

## Întrebarea 5: Captură PCAP ca Evidență

### Scenariu

Un utilizator reclamă că "site-ul nu funcționează". Ai capturat traficul și vezi:

```
1. 10:00:00.000  Client → Server  TCP SYN (port 443)
2. 10:00:00.001  Server → Client  TCP SYN-ACK
3. 10:00:00.002  Client → Server  TCP ACK
4. 10:00:00.003  Client → Server  TLS Client Hello
5. 10:00:00.050  Server → Client  TCP RST
```

### Întrebare

Unde este problema cel mai probabil?

### Opțiuni

| | Opțiune |
|---|---------|
| **A** | Firewall-ul blochează portul 443 |
| **B** | Serverul nu are certificat TLS valid sau configurație TLS incompatibilă |
| **C** | Clientul a închis conexiunea |
| **D** | Rețeaua pierde pachete |

---

### Răspuns Corect: **B**

### Explicație Post-Vot

- **A** — Dacă firewall-ul ar bloca, nu am vedea SYN-ACK (pachetele 2-3).
- **B** ✅ — Handshake-ul TCP **reușește** (pașii 1-3), dar serverul trimite RST **după** Client Hello. Aceasta indică o problemă la nivelul TLS (certificat expirat, cipher suite incompatibil, etc.).
- **C** — RST vine de la server, nu de la client.
- **D** — Vedem toate pachetele, nicio pierdere.

### Note Instructor

**Lecție cheie:** Capturile PCAP permit diagnosticarea precisă:
- Handshake TCP OK → problema NU e la nivel rețea
- RST după TLS Hello → problema e la nivel aplicație/TLS

**Exercițiu suplimentar:** Cum ar arăta captura dacă firewall-ul ar avea REJECT pe 443?
- Răspuns: SYN → RST (fără SYN-ACK)

---

## Utilizare în Laborator

### Recomandări de Timing

| Fază | Durată | Activitate |
|------|--------|------------|
| Prezentare | 1 min | Citește scenariul și opțiunile |
| Vot 1 | 1 min | Studenții votează individual (fără discuție) |
| Discuție | 3 min | Perechi discută și argumentează |
| Vot 2 | 30 sec | Revot după discuție |
| Explicație | 2 min | Instructor explică răspunsul corect |

### Ținte de Performanță

| Întrebare | Țintă Vot 1 | Țintă Vot 2 |
|-----------|-------------|-------------|
| 1 (DROP) | 40-60% | 85%+ |
| 2 (Timing) | 50-70% | 90%+ |
| 3 (L7 vs L3) | 30-50% | 80%+ |
| 4 (Sondare) | 40-60% | 85%+ |
| 5 (Diagnostic) | 30-50% | 75%+ |

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
