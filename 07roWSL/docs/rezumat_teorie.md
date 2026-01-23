# Rezumat Teoretic - Săptămâna 7

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## Interceptarea Pachetelor

### Ce Este Interceptarea Pachetelor?

Interceptarea pachetelor (packet sniffing) reprezintă procesul de captare
și analiză a pachetelor de date care traversează o rețea. Această tehnică
este fundamentală pentru:

- **Diagnosticarea problemelor de rețea** - identificarea punctelor de eșec
- **Analiza securității** - detectarea traficului suspect
- **Dezvoltarea aplicațiilor** - verificarea implementării protocoalelor
- **Educație** - înțelegerea funcționării rețelelor

### 💡 Analogie: Camere de Supraveghere

Imaginează-ți o clădire de birouri cu sistem de securitate:

| Concept Tehnic | Analogie |
|----------------|----------|
| **Interceptarea pachetelor** | Camerele video înregistrează tot ce se întâmplă |
| **Wireshark** | Monitorul de securitate unde vizualizezi filmările |
| **Filtrele de captură** | Setarea camerelor să filmeze doar anumite zone |
| **Filtrele de afișare** | Căutarea în arhivă pentru o persoană sau interval |
| **Fișier PCAP** | Caseta video salvată ca probă |

Așa cum securitatea poate revizui filmările pentru a investiga un incident, tu poți analiza capturile pentru a diagnostica probleme de rețea.

### 💡 Analogie Alternativă: Detectivul și Scrisorile

Gândește-te la interceptarea pachetelor ca la un detectiv care monitorizează corespondența:

| Pas | În Lumea Reală | În Rețelistică |
|-----|----------------|----------------|
| 1 | Detectivul se așază la oficiul poștal | Wireshark ascultă pe interfață |
| 2 | Notează expeditorul și destinatarul fiecărei scrisori | Înregistrează IP sursă, IP destinație |
| 3 | Notează tipul coletului (plic, pachet, recomandat) | Notează protocolul (TCP, UDP, ICMP) |
| 4 | Salvează totul într-un dosar | Salvează în fișier .pcap |
| 5 | Mai târziu caută "toate scrisorile de la Ion" | Aplică filtru: `ip.src == 10.0.7.100` |

### Instrumente de Captare

**Wireshark** - Analizor grafic de protocoale
- Captură în timp real
- Filtre puternice de afișare
- Decodare automată a protocoalelor
- Export în multiple formate

**tcpdump** - Instrument linie de comandă
- Ușor și rapid
- Ideal pentru servere fără interfață grafică
- Filtre BPF (Berkeley Packet Filter)

**tshark** - Versiunea CLI a Wireshark
- Funcționalitate similară cu Wireshark
- Potrivit pentru scripturi automatizate

### Filtre de Captare vs. Filtre de Afișare

**Filtre de captare (BPF)**
- Aplicate în timpul capturii
- Reduc volumul de date capturate
- Sintaxă: `tcp port 80`, `host 192.168.1.1`

**Filtre de afișare (Wireshark)**
- Aplicate pe datele deja capturate
- Mai flexibile și expresive
- Sintaxă: `tcp.port == 80`, `ip.addr == 192.168.1.1`

---

## Filtrarea Pachetelor cu iptables

### Arhitectura Netfilter

Netfilter este framework-ul de filtrare a pachetelor în kernelul Linux.
iptables este instrumentul de configurare pentru Netfilter.

### 💡 Analogie: Poarta cu Paznic

Imaginează-ți intrarea într-un campus universitar:

| Regulă Firewall | Echivalent Campus |
|-----------------|-------------------|
| **ACCEPT** | Paznicul verifică legitimația și te lasă să intri |
| **DROP** | Paznicul te ignoră complet, ca și cum nu exiști |
| **REJECT** | Paznicul îți spune "Accesul interzis!" și te trimite înapoi |
| **Lanțul INPUT** | Verificarea la intrare în campus |
| **Lanțul OUTPUT** | Verificarea la ieșire din campus |
| **Lanțul FORWARD** | Tranzitul prin campus către altă clădire |

**Lanțuri principale:**
- **INPUT** - pachete destinate sistemului local
- **OUTPUT** - pachete generate de sistemul local
- **FORWARD** - pachete care tranzitează sistemul

**Tabele:**
- **filter** - filtrarea pachetelor (implicit)
- **nat** - traducerea adreselor de rețea
- **mangle** - modificarea pachetelor
- **raw** - excepții de la urmărirea conexiunilor

### Structura unei Reguli

```
iptables -t TABLE -A CHAIN -p PROTOCOL --dport PORT -j TARGET
```

**Componente:**
- `-t TABLE` - tabela (filter implicit)
- `-A CHAIN` - adaugă regulă la lanț
- `-p PROTOCOL` - protocolul (tcp, udp, icmp)
- `--dport PORT` - portul destinație
- `-j TARGET` - acțiunea (ACCEPT, DROP, REJECT)

---

## Semantica REJECT vs DROP

### 💡 Analogie: Apel Telefonic Refuzat

| Scenariu Telefon | Echivalent Firewall |
|------------------|---------------------|
| Sună ocupat imediat | **REJECT** — răspuns clar, eșec rapid |
| Sună la infinit, nimeni nu răspunde | **DROP** — tăcere, trebuie să aștepți |
| "Numărul format nu există" | **REJECT cu ICMP** — mesaj explicit |

**De reținut:**
- REJECT = politicos dar informativ (atacatorul știe că exiști)
- DROP = tăcut dar frustrant (nimeni nu știe ce s-a întâmplat)

### Acțiunea REJECT

Când un pachet este respins cu REJECT:
1. Firewall-ul trimite un răspuns explicit
2. Pentru TCP: pachet RST (reset)
3. Pentru alte protocoale: mesaj ICMP de eroare
4. Conexiunea eșuează **imediat**

**Avantaje:**
- Experiență utilizator mai bună (eroare clară)
- Depanare mai ușoară
- Aplicațiile primesc feedback rapid

**Dezavantaje:**
- Dezvăluie prezența firewall-ului
- Consumă resurse pentru generarea răspunsului

### Acțiunea DROP

Când un pachet este eliminat cu DROP:
1. Pachetul este eliminat silențios
2. **Niciun răspuns** nu este trimis
3. Conexiunea expiră după timeout

**Avantaje:**
- Mai discret ("stealth")
- Nu dezvăluie configurația firewall-ului
- Atacatorul trebuie să aștepte timeout

**Dezavantaje:**
- Experiență utilizator slabă
- Depanare dificilă
- Indistinguibil de pierderea pachetelor

### Când să Folosiți Fiecare

| Scenariu | Recomandare |
|----------|-------------|
| Rețea internă | REJECT |
| Servicii publice | DROP |
| Depanare | REJECT |
| Producție cu cerințe de securitate | DROP |
| Aplicații cu timeout scurt | REJECT |

---

## Filtrarea la Nivel Aplicație

### 💡 Analogie: Controlul la Aeroport

| Etapă Aeroport | Echivalent Rețea |
|----------------|------------------|
| Check-in reușit | Handshake TCP complet |
| Bagajele trec prin scanner | Inspecția conținutului la nivel aplicație |
| "Obiect interzis în bagaj!" | 403 Forbidden — cerere blocată |
| "Puteți îmbarca" | 200 OK — cerere acceptată |

**Diferența cheie:** 
- Firewall rețea (iptables) = bariera de la intrarea în aeroport
- Firewall aplicație (proxy) = scanner-ul de bagaje

Poți trece de barieră (conexiune TCP) dar tot să fii oprit la scanner (conținut blocat).

### Diferențe față de Filtrarea la Nivel Rețea

**Filtrare la nivel rețea (iptables):**
- Operează la nivelurile 3-4 OSI
- Decizii bazate pe: IP, port, protocol
- Blocarea se întâmplă înainte de stabilirea conexiunii
- Nu "vede" conținutul aplicației

**Filtrare la nivel aplicație (proxy):**
- Operează la nivelul 7 OSI
- Decizii bazate pe conținutul cererilor
- Conexiunea TCP se stabilește cu succes
- Poate inspecta și modifica conținutul

### Cazuri de Utilizare

**Firewall aplicație web (WAF):**
- Detectarea atacurilor SQL injection
- Prevenirea cross-site scripting (XSS)
- Validarea inputului

**Proxy de conținut:**
- Filtrarea URL-urilor
- Blocarea tipurilor de fișiere
- Inspecția SSL/TLS

---

## Sondarea Defensivă a Porturilor

### Ce Este Sondarea Porturilor?

Tehnica de identificare a serviciilor active pe un sistem prin
trimiterea de cereri către diferite porturi și analiza răspunsurilor.

### 💡 Analogie: Bătutul la Uși

Imaginează-ți că verifici care apartamente sunt ocupate într-un bloc:

| Răspuns la Ușă | Stare Port | Ce înseamnă |
|----------------|------------|-------------|
| "Cine e?" | **DESCHIS** | Cineva locuiește aici și răspunde |
| "Apartament gol" (de la administrator) | **ÎNCHIS** | Nimeni nu stă, dar clădirea confirmă |
| Tăcere completă | **FILTRAT** | Nu știi — e gol? e ascuns? e interfon defect? |

**De ce contează pentru securitate:**
- Sondarea identifică ce servicii rulează
- FILTRAT (DROP) face mai greu de cartografiat rețeaua
- ÎNCHIS (RST) confirmă că sistemul există

### Tipuri de Sondare TCP

**SYN Scan (Half-open)**
- Trimite SYN, analizează răspunsul
- Nu finalizează handshake-ul
- Mai discret decât conexiunea completă

**Connect Scan**
- Conexiune TCP completă
- Mai ușor de detectat
- Nu necesită privilegii speciale

### Interpretarea Răspunsurilor

| Răspuns | Interpretare |
|---------|--------------|
| SYN-ACK | Port DESCHIS - serviciu activ |
| RST | Port ÎNCHIS - niciun serviciu |
| Niciun răspuns | Port FILTRAT - DROP activ |
| ICMP unreachable | Port FILTRAT - REJECT activ |

### Utilizare Etică

Sondarea porturilor este o tehnică legitimă pentru:
- Audit de securitate propriu
- Verificarea configurației firewall
- Inventarierea serviciilor

**Important:** Sondarea sistemelor fără autorizație este ilegală!

---

## Formatul Capturilor PCAP

### Structura Fișierului PCAP

```
┌────────────────────────────────────┐
│         Global Header             │
│  (magic, version, snaplen, etc.)  │
├────────────────────────────────────┤
│         Packet Header #1          │
│  (timestamp, captured len, etc.)  │
├────────────────────────────────────┤
│         Packet Data #1            │
│  (frame, headers, payload)        │
├────────────────────────────────────┤
│         Packet Header #2          │
├────────────────────────────────────┤
│         Packet Data #2            │
├────────────────────────────────────┤
│              ...                  │
└────────────────────────────────────┘
```

### Utilitate ca Probă

Capturile PCAP servesc ca:
- Evidență obiectivă a evenimentelor de rețea
- Probă în investigații de securitate
- Documentație pentru audit
- Material pentru analiza post-incident

---

## Concepte Cheie de Reținut

1. **Interceptarea** permite observarea directă a traficului de rețea
2. **REJECT** trimite răspuns, **DROP** elimină silențios
3. **Filtrarea nivel aplicație** vede conținutul, nu doar headerele
4. **Sondarea porturilor** identifică servicii și configurații firewall
5. **PCAP** este formatul standard pentru stocarea capturilor

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
