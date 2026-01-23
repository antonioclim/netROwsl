# Misconceptii Frecvente - Săptămâna 7

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix
>
> Acest document listează greșelile comune de înțelegere și cum să le corectezi.

---

## Filtrarea Pachetelor (iptables)

### 🚫 Misconceptia 1: "DROP trimite RST"

**GREȘIT:** "Când configurez DROP, firewall-ul trimite un pachet RST pentru a refuza conexiunea."

**CORECT:** DROP elimină pachetul **SILENȚIOS**. Nu trimite absolut nimic.

| Acțiune | Ce trimite | Ce vede clientul |
|---------|-----------|------------------|
| **DROP** | Nimic | Timeout, retransmisii |
| **REJECT** | RST (TCP) sau ICMP | Eroare imediată |

**Verificare practică:**
```bash
# Aplică DROP
sudo iptables -A INPUT -p tcp --dport 9999 -j DROP

# Într-un alt terminal, încearcă conexiunea
nc -zv localhost 9999
# Vei aștepta ~30 secunde până la timeout

# În Wireshark vei vedea: SYN → SYN → SYN (retransmisii fără răspuns)
```

---

### 🚫 Misconceptia 2: "REJECT e mai sigur decât DROP"

**GREȘIT:** "REJECT oferă mai multă securitate pentru că refuză explicit conexiunea."

**CORECT:** E invers! **DROP e considerat mai sigur** din perspectiva securității:

| Aspect | DROP | REJECT |
|--------|------|--------|
| Dezvăluie existența sistemului | Nu | Da |
| Dezvăluie existența firewall-ului | Nu | Da |
| Informații pentru atacator | Minime | Confirmă că portul e monitorizat |
| Experiență utilizator | Slabă (timeout lung) | Bună (eroare rapidă) |

**Recomandare:** DROP pentru perimetru extern, REJECT pentru rețea internă.

---

### 🚫 Misconceptia 3: "Ordinea regulilor nu contează"

**GREȘIT:** "Pot pune regulile iptables în orice ordine, toate se aplică."

**CORECT:** iptables procesează regulile **în ordine** și se oprește la prima potrivire!

```bash
# Ordinea GREȘITĂ - regula 2 nu se aplică niciodată!
iptables -A INPUT -p tcp -j ACCEPT       # Acceptă TOT TCP
iptables -A INPUT -p tcp --dport 22 -j DROP  # Această regulă e ignorată!

# Ordinea CORECTĂ
iptables -A INPUT -p tcp --dport 22 -j DROP  # Mai întâi regula specifică
iptables -A INPUT -p tcp -j ACCEPT           # Apoi regula generală
```

**Regulă de aur:** Regulile specifice ÎNAINTEA regulilor generale.

---

## Interceptarea Pachetelor (Wireshark)

### 🚫 Misconceptia 4: "Filtrele de captură și de afișare sunt identice"

**GREȘIT:** "Pot folosi `tcp.port == 80` ca filtru de captură."

**CORECT:** Sunt sintaxe complet diferite!

| Tip filtru | Sintaxă | Când se aplică | Exemplu |
|------------|---------|----------------|---------|
| **Captură (BPF)** | Simplă | ÎN TIMPUL capturii | `tcp port 80` |
| **Afișare (Wireshark)** | Complexă | DUPĂ captură | `tcp.port == 80` |

**Greșeli frecvente:**
```
# GREȘIT ca filtru de captură:
tcp.port == 80     # Sintaxă de afișare!

# CORECT ca filtru de captură:
tcp port 80        # Sintaxă BPF

# CORECT ca filtru de afișare:
tcp.port == 80     # Sintaxă Wireshark
```

---

### 🚫 Misconceptia 5: "Lipsa pachetelor înseamnă că filtrul e greșit"

**GREȘIT:** "Nu văd pachete în Wireshark, deci filtrul meu e incorect."

**CORECT:** Pot fi mai multe cauze:

| Cauză | Verificare | Soluție |
|-------|------------|---------|
| Interfață greșită | Check interfața selectată | Selectează `vEthernet (WSL)` |
| Trafic negenerat | Verifică dacă ai rulat comanda | Generează trafic ÎN TIMPUL capturii |
| Filtru prea restrictiv | Testează fără filtru | Șterge filtrul și vezi tot traficul |
| DROP activ | Verifică regulile iptables | `iptables -L -n` |

**Procedură de diagnostic:**
1. Oprește captura
2. Șterge filtrul de afișare
3. Repornește captura FĂRĂ filtru
4. Generează trafic
5. Dacă vezi pachete → problema era filtrul
6. Dacă NU vezi pachete → problema e interfața sau traficul

---

## Protocoale de Transport

### 🚫 Misconceptia 6: "UDP nu se poate filtra cu firewall"

**GREȘIT:** "Pentru că UDP e fără conexiune, firewall-ul nu-l poate bloca."

**CORECT:** iptables poate filtra UDP exact ca TCP:

```bash
# Blochează UDP pe portul 9091
sudo iptables -A INPUT -p udp --dport 9091 -j DROP

# Funcționează identic cu TCP:
# - DROP elimină silențios datagrama
# - REJECT trimite ICMP Port Unreachable
```

**Diferența:** Nu există "handshake" de blocat, dar fiecare datagramă individuală poate fi filtrată.

---

### 🚫 Misconceptia 7: "Timeout la UDP înseamnă DROP"

**GREȘIT:** "Dacă nu primesc răspuns UDP, înseamnă că e DROP pe firewall."

**CORECT:** UDP e **fire-and-forget** — lipsa răspunsului poate însemna:

| Cauză posibilă | Cum să diferențiezi |
|----------------|---------------------|
| DROP pe firewall | Verifică `iptables -L -n` |
| Serviciul nu răspunde (by design) | Verifică logurile serviciului |
| Pachetul s-a pierdut în rețea | Trimite mai multe, verifică statistic |
| Aplicația nu implementează răspuns | Citește documentația protocolului |

**Realitate:** Multe protocoale UDP (DNS query, syslog) NU trimit confirmare. Lipsa răspunsului e normală!

---

## Filtrare Nivel Aplicație

### 🚫 Misconceptia 8: "WAF înlocuiește firewall-ul de rețea"

**GREȘIT:** "Dacă am un Web Application Firewall, nu mai am nevoie de iptables."

**CORECT:** Sunt **complementare**, operează la niveluri diferite:

```
          ┌─────────────────────────────────────────┐
          │              INTERNET                   │
          └─────────────────┬───────────────────────┘
                            │
                    ┌───────▼───────┐
                    │   iptables    │  ← Nivel 3-4 (IP, TCP/UDP)
                    │   (L3-L4)     │    Blochează pe bază de IP/port
                    └───────┬───────┘    ÎNAINTE de conexiune
                            │
                    ┌───────▼───────┐
                    │     WAF       │  ← Nivel 7 (HTTP, conținut)
                    │   (L7)        │    Inspectează DUPĂ handshake
                    └───────┬───────┘
                            │
                    ┌───────▼───────┐
                    │   Aplicație   │
                    └───────────────┘
```

**De ce ai nevoie de ambele:**
- iptables: Blochează scanări de porturi, DDoS, IP-uri cunoscute rele
- WAF: Blochează SQL injection, XSS, conținut malițios

---

### 🚫 Misconceptia 9: "403 Forbidden = firewall a blocat"

**GREȘIT:** "Am primit 403, deci firewall-ul m-a blocat."

**CORECT:** 403 e un răspuns **HTTP** de la aplicație, NU de la firewall de rețea!

| Blocare | Ce vezi în Wireshark | Mesaj pentru client |
|---------|---------------------|---------------------|
| iptables DROP | SYN → timeout | Connection timed out |
| iptables REJECT | SYN → RST | Connection refused |
| WAF/Aplicație | Handshake OK → HTTP 403 | 403 Forbidden |

**Indiciu cheie:** Dacă vezi handshake TCP complet (SYN, SYN-ACK, ACK), blocarea NU e la nivel rețea!

---

## Sondarea Porturilor

### 🚫 Misconceptia 10: "Port FILTRAT = port ÎNCHIS"

**GREȘIT:** "Dacă scannerul zice FILTRAT, înseamnă că nu rulează niciun serviciu."

**CORECT:** FILTRAT înseamnă "NU ȘTIU" — firewall-ul blochează, nu putem determina starea reală:

| Stare | Ce s-a întâmplat | Ce înseamnă |
|-------|------------------|-------------|
| **DESCHIS** | Am primit SYN-ACK | Serviciu activ, acceptă conexiuni |
| **ÎNCHIS** | Am primit RST | Niciun serviciu, dar sistemul răspunde |
| **FILTRAT** | Timeout/ICMP filtered | Firewall activ, starea reală necunoscută |

**Implicație practică:** Un port FILTRAT POATE avea un serviciu activ în spate — doar firewall-ul nu ne lasă să verificăm!

---

## Sumar: Tabel de Corecții Rapide

| Misconceptie | Corecție |
|--------------|----------|
| DROP trimite RST | DROP = tăcere absolută |
| REJECT e mai sigur | DROP e mai sigur (stealth) |
| Ordinea regulilor nu contează | Prima potrivire câștigă |
| Filtrele de captură = filtre de afișare | Sintaxe diferite! |
| UDP nu se poate filtra | Se filtrează identic cu TCP |
| Timeout UDP = DROP | UDP nu garantează răspuns oricum |
| WAF înlocuiește iptables | Sunt complementare (L7 vs L3-4) |
| 403 = firewall | 403 = răspuns aplicație |
| FILTRAT = ÎNCHIS | FILTRAT = necunoscut |

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
