# Întrebări Peer Instruction - Săptămâna 13

> Laborator IoT și Securitate în Rețelele de Calculatoare
>
> Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

---

## Instrucțiuni pentru Instructor

Aceste întrebări sunt proiectate conform metodologiei Peer Instruction (Mazur, Porter et al.):

1. **Prezentare** (1 min) — Citește scenariul și întrebarea
2. **Vot individual** (1 min) — Studenții votează fără discuție
3. **Discuție în perechi** (3 min) — Studenții își explică reciproc răspunsurile
4. **Revot** (30 sec) — Votează din nou după discuție
5. **Explicație** (2 min) — Instructorul clarifică răspunsul corect

**Țintă:** 40-60% răspunsuri corecte la primul vot (prea ușor = >80%, prea greu = <30%)

---

## 🗳️ PI-13.1: MQTT Quality of Service

### Scenariu

```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883)
client.publish("senzori/temperatura", "23.5", qos=2)
```

Imediat după apelul `publish()`, conexiunea de rețea se întrerupe complet pentru 30 de secunde, apoi revine.

### Întrebare

Ce se întâmplă cu mesajul "23.5"?

### Opțiuni

A) Mesajul este pierdut definitiv — QoS 2 nu poate recupera din deconectări complete

B) Mesajul va ajunge la subscriber EXACT O DATĂ când conexiunea revine

C) Mesajul va ajunge de mai multe ori (duplicat) din cauza retransmisiilor

D) Broker-ul trimite o eroare către publisher și mesajul este anulat

---

### 📋 NOTE INSTRUCTOR

**Răspuns corect:** B

**Țintă primul vot:** ~45% corect

**Analiza distractorilor:**
- **A)** Misconceptie: confuzie cu QoS 0 (fire-and-forget)
- **C)** Misconceptie: confuzie cu QoS 1 (at least once, posibile duplicate)
- **D)** Misconceptie: nu înțeleg că MQTT este asincron și broker-ul păstrează starea

**După discuție:** Desenează pe tablă fluxul celor 4 mesaje din QoS 2:
```
Publisher          Broker
    │──PUBLISH────▶│
    │◀──PUBREC─────│
    │──PUBREL─────▶│
    │◀──PUBCOMP────│
```

**Întrebare de follow-up:** "De ce am folosi QoS 1 în loc de QoS 2 dacă 2 e mai sigur?"
(Răspuns: overhead mai mare, latență crescută)

---

## 🗳️ PI-13.2: Docker Port Mapping

### Scenariu

```yaml
# docker-compose.yml
services:
  mosquitto:
    image: eclipse-mosquitto:2.0
    ports:
      - "1883:1883"
    networks:
      week13net:
        ipv4_address: 10.0.13.100
```

Containerul Mosquitto rulează și ascultă pe portul 1883 intern. IP-ul containerului în rețeaua Docker este 10.0.13.100.

### Întrebare

Din Windows (host), ce adresă și port folosești pentru a te conecta la broker?

### Opțiuni

A) `10.0.13.100:1883` — folosești IP-ul containerului direct

B) `localhost:1883` — folosești localhost cu portul mapat

C) `172.17.0.2:1883` — folosești IP-ul din rețeaua bridge implicită

D) `mosquitto:1883` — folosești numele serviciului ca hostname

---

### 📋 NOTE INSTRUCTOR

**Răspuns corect:** B

**Țintă primul vot:** ~50% corect

**Analiza distractorilor:**
- **A)** Misconceptie: IP-ul 10.0.13.x este intern rețelei Docker, nu accesibil direct din Windows
- **C)** Misconceptie: confuzie între rețeaua bridge implicită și rețeaua custom
- **D)** Misconceptie: numele serviciului se rezolvă doar ÎNTRE containere, nu din host

**După discuție:** Desenează diagrama:
```
Windows (Host)                    Docker Network (week13net)
┌─────────────────┐              ┌─────────────────────────┐
│                 │              │                         │
│  localhost:1883 │──────────────│▶ 10.0.13.100:1883      │
│                 │   port map   │   (mosquitto)           │
└─────────────────┘              └─────────────────────────┘
```

**Demo live:** Arată că `ping 10.0.13.100` din PowerShell NU funcționează, dar `Test-NetConnection localhost -Port 1883` DA.

---

## 🗳️ PI-13.3: TLS și Securitate MQTT

### Scenariu

Ai configurat broker-ul MQTT să accepte conexiuni pe două porturi:
- Port 1883: MQTT text clar
- Port 8883: MQTT cu TLS (certificate auto-semnate)

Un atacator se află pe aceeași rețea WiFi ca tine.

### Întrebare

Ce poate face atacatorul în fiecare caz?

### Opțiuni

A) Port 1883: vede mesajele în clar | Port 8883: nu poate vedea nimic

B) Port 1883: vede mesajele în clar | Port 8883: vede trafic criptat dar nu conținutul

C) Port 1883: vede mesajele în clar | Port 8883: poate decripta dacă are certificatul CA

D) Ambele porturi sunt la fel de vulnerabile dacă atacatorul are acces fizic la rețea

---

### 📋 NOTE INSTRUCTOR

**Răspuns corect:** B

**Țintă primul vot:** ~40% corect

**Analiza distractorilor:**
- **A)** Parțial corect dar incomplet — atacatorul VEDE traficul pe 8883, doar nu-l poate citi
- **C)** Misconceptie: certificatul CA public NU permite decriptarea (confuzie cu cheia privată)
- **D)** Misconceptie: TLS oferă protecție reală chiar și cu acces la rețea

**După discuție:** Demo live în Wireshark:
1. Capturează trafic pe portul 1883 — arată payload-ul vizibil
2. Capturează trafic pe portul 8883 — arată "Application Data" criptat

**Întrebare de follow-up:** "TLS garantează că serverul este de încredere?"
(Răspuns: NU! TLS garantează criptare și identitate verificabilă, nu încredere)

---

## 🗳️ PI-13.4: Tehnici de Scanare Porturi

### Scenariu

Rulezi două tipuri de scanare pe același server:

```bash
# Scanare 1: TCP Connect
python3 ex_13_01_scanner_porturi.py --tinta 10.0.13.11 --porturi 80

# Scanare 2: nmap SYN scan (necesită root)
sudo nmap -sS 10.0.13.11 -p 80
```

### Întrebare

Care este diferența principală între cele două scanări?

### Opțiuni

A) Connect scan este mai rapidă, SYN scan este mai precisă

B) Connect scan completează handshake-ul TCP, SYN scan nu — deci SYN e mai discretă

C) SYN scan funcționează doar pe Linux, Connect scan e cross-platform

D) Nu există diferență practică, ambele detectează portul deschis la fel

---

### 📋 NOTE INSTRUCTOR

**Răspuns corect:** B

**Țintă primul vot:** ~55% corect

**Analiza distractorilor:**
- **A)** Invers: SYN scan e mai rapidă (un pachet mai puțin per port)
- **C)** Fals: SYN scan funcționează pe orice OS cu drepturi root/admin
- **D)** Fals: diferența e în loguri — Connect scan lasă urme, SYN scan nu

**După discuție:** Desenează cele două fluxuri:
```
Connect Scan:              SYN Scan:
─────────────              ─────────
    │──SYN────▶│              │──SYN────▶│
    │◀─SYN/ACK─│              │◀─SYN/ACK─│
    │──ACK────▶│ ← logged     │──RST────▶│ ← NOT logged
    │──RST────▶│              
```

**Demo:** Arată în jurnalele DVWA (`docker logs week13_dvwa`) că Connect scan apare, dar SYN scan nu.

---

## 🗳️ PI-13.5: Vulnerabilitatea Backdoor FTP

### Scenariu

În laborator, containerul `week13_vsftpd` simulează vulnerabilitatea CVE-2011-2523 din vsftpd 2.3.4.

Această vulnerabilitate permitea executarea de comenzi prin trimiterea unui username care conținea caracterul `:)` (smiley).

### Întrebare

De ce folosim o SIMULARE a backdoor-ului în loc de versiunea reală vulnerabilă?

### Opțiuni

A) Versiunea reală nu mai există, codul sursă a fost șters de pe internet

B) Versiunea reală ar fi prea periculoasă — simularea oferă același efect educațional în siguranță

C) Simularea este mai ușor de instalat în Docker decât versiunea originală

D) Nu există nicio diferență, folosim de fapt versiunea reală vsftpd 2.3.4

---

### 📋 NOTE INSTRUCTOR

**Răspuns corect:** B

**Țintă primul vot:** ~60% corect

**Analiza distractorilor:**
- **A)** Fals: codul sursă vulnerabil încă există în arhive
- **C)** Parțial adevărat dar nu motivul principal — securitatea e prioritară
- **D)** Fals și periculos: verifică `docker inspect week13_vsftpd` pentru a confirma

**După discuție:** Explică principiul "safe learning environment":
- Simulăm comportamentul, nu vulnerabilitatea reală
- Backdoor-ul nostru nu oferă acces root real
- Scopul e să înveți DETECTAREA, nu EXPLOATAREA

**Întrebare de follow-up:** "Cum ai detecta un backdoor real într-un server FTP de producție?"
(Răspunsuri posibile: scanare porturi neașteptate, analiza traficului, verificare hash-uri binare)

---

## Resurse Suplimentare

- Mazur, E. (1997). Peer Instruction: A User's Manual
- Porter, L. et al. (2011). Peer Instruction: Do Students Really Learn from Peer Discussion in Computing?
- OWASP IoT Top 10: https://owasp.org/www-project-internet-of-things/

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix*
