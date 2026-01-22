# Întrebări Peer Instruction - Săptămâna 3

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

---

## Instrucțiuni pentru Instructor

**Metoda Peer Instruction (Mazur):**

1. **Afișează întrebarea** (1 min) - studenții citesc individual
2. **Primul vot** (1 min) - fără discuții, răspuns individual
3. **Discuție în perechi** (3 min) - studenții își explică reciproc alegerea
4. **Al doilea vot** (30 sec) - după discuție
5. **Explicație și debrief** (2 min) - instructorul clarifică

**Țintă:** ~50% răspunsuri corecte la primul vot. Dacă >80% corect, întrebarea e prea ușoară. Dacă <30% corect, conceptul necesită re-predare.

**Distractorii** sunt construiți pe baza misconceptiilor comune documentate în literatura de specialitate.

---

## 🗳️ Întrebarea 1: Adresa de Bind pentru Broadcast

### Scenariu

Un student scrie următorul cod pentru un receptor broadcast:

```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('192.168.1.50', 5007))  # IP-ul mașinii locale
data, addr = sock.recvfrom(1024)
```

### Întrebare

Receptorul va primi mesajele broadcast trimise la 255.255.255.255:5007?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | Da, pentru că portul 5007 este corect |
| **B** | Nu, pentru că trebuie să faci bind la '0.0.0.0' |
| **C** | Da, dar doar dacă SO_BROADCAST este activat pe receptor |
| **D** | Nu, pentru că broadcast-ul nu funcționează cu socket-uri UDP |

---

### Răspuns Corect: **B**

<details>
<summary>Explicație detaliată (pentru după vot)</summary>

**B este corect.** Pentru a primi broadcast, receptorul TREBUIE să facă bind la `0.0.0.0` (INADDR_ANY), nu la o adresă IP specifică.

**Analiza distractorilor:**

| Opțiune | De ce e greșită | Misconceptie vizată |
|---------|-----------------|---------------------|
| **A** | Portul corect nu e suficient - adresa de bind contează | Ignorarea adresei de bind |
| **C** | SO_BROADCAST e pentru EMIȚĂTOR, nu receptor | Confuzie emițător/receptor |
| **D** | Broadcast funcționează perfect cu UDP | Confuzie TCP/UDP |

**Cod corect:**
```python
sock.bind(('0.0.0.0', 5007))  # INADDR_ANY
```

**Întrebare de follow-up:** De ce nu merge cu IP-ul specific?
- Kernelul livrează pachetele broadcast doar la socket-urile bound la INADDR_ANY sau la adresa de broadcast.

</details>

---

## 🗳️ Întrebarea 2: IGMP și Recepția Multicast

### Scenariu

Un emițător multicast funcțional trimite la grupul 239.0.0.1:5008.
Receptorul execută:

```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 5008))
# ... lipsește ceva aici? ...
data, addr = sock.recvfrom(1024)
```

### Întrebare

Receptorul va primi mesajele multicast?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | Da, bind-ul la portul 5008 este suficient |
| **B** | Nu, lipsește IP_ADD_MEMBERSHIP pentru a se înscrie în grup |
| **C** | Da, dar doar dacă emițătorul are TTL > 1 |
| **D** | Nu, trebuie să facă bind direct la adresa 239.0.0.1 |

---

### Răspuns Corect: **B**

<details>
<summary>Explicație detaliată (pentru după vot)</summary>

**B este corect.** Pentru multicast, receptorul TREBUIE să se înscrie explicit în grupul multicast folosind `IP_ADD_MEMBERSHIP`. Aceasta trimite un mesaj IGMP Membership Report către router.

**Analiza distractorilor:**

| Opțiune | De ce e greșită | Misconceptie vizată |
|---------|-----------------|---------------------|
| **A** | Bind deschide socket-ul, dar NU înscrie în grup | Confuzie bind vs join |
| **C** | TTL controlează propagarea, nu recepția locală | Neînțelegerea TTL |
| **D** | Bind la grupul multicast funcționează pe unele OS-uri, dar nu e portabil și nu e suficient | Dependență de OS |

**Cod corect:**
```python
import struct
mreq = struct.pack('4s4s', 
    socket.inet_aton('239.0.0.1'),    # Grup
    socket.inet_aton('0.0.0.0'))       # Interfață
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
```

**Întrebare de follow-up:** Ce mesaj IGMP se trimite când apelezi IP_ADD_MEMBERSHIP?
- IGMP Membership Report (Type 0x16)

</details>

---

## 🗳️ Întrebarea 3: Conexiuni în Tunel TCP

### Scenariu

Arhitectura laboratorului:
```
Client (172.20.0.100) → Tunel (172.20.0.254:9090) → Server Echo (172.20.0.10:8080)
```

Clientul trimite "Hello" prin tunel. Serverul răspunde cu "ECHO: Hello".

### Întrebare

Câte conexiuni TCP sunt active în total în timpul acestui schimb?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | 1 conexiune (client → server, tunelul e transparent) |
| **B** | 2 conexiuni (client → tunel, tunel → server) |
| **C** | 3 conexiuni (client → tunel → router → server) |
| **D** | 0 conexiuni (tunelul convertește la UDP intern) |

---

### Răspuns Corect: **B**

<details>
<summary>Explicație detaliată (pentru după vot)</summary>

**B este corect.** Un tunel TCP menține DOUĂ conexiuni TCP separate:

```
Client ←──Conn 1──→ Tunel ←──Conn 2──→ Server
         TCP #1              TCP #2
```

**Vizualizare în Wireshark:**
- Vei vedea 2× SYN (unul pentru fiecare conexiune)
- 2× handshake-uri TCP complete
- 2× FIN la închidere

**Analiza distractorilor:**

| Opțiune | De ce e greșită | Misconceptie vizată |
|---------|-----------------|---------------------|
| **A** | TCP nu poate "traversa" transparent un intermediar la Layer 4 | Confuzie cu NAT |
| **C** | "Router" în context e tunelul, nu un hop suplimentar | Confuzie terminologie |
| **D** | Tunelul TCP rămâne TCP end-to-end | Inventare protocol |

**Întrebare de follow-up:** Ce IP sursă vede serverul?
- IP-ul tunelului (172.20.0.254), NU IP-ul clientului

</details>

---

## 🗳️ Întrebarea 4: Eficiență Broadcast vs Multicast

### Scenariu

O companie are 100 de dispozitive în rețea. Vrea să trimită actualizări de stoc către 10 aplicații de trading.

### Întrebare

Care abordare generează MAI PUȚIN trafic procesat inutil de dispozitivele neinteresate?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | Broadcast - un singur pachet ajunge oricum la toți |
| **B** | Multicast cu IGMP snooping pe switch |
| **C** | Sunt echivalente în rețeaua locală |
| **D** | 10 conexiuni TCP unicast separate |

---

### Răspuns Corect: **B**

<details>
<summary>Explicație detaliată (pentru după vot)</summary>

**B este corect.** Cu IGMP snooping, switch-ul învață ce porturi au membri multicast și livrează pachetele DOAR acolo.

**Comparație:**

| Metodă | Pachete trimise | Dispozitive care procesează | Overhead |
|--------|-----------------|----------------------------|----------|
| Broadcast | 1 | 100 (toate) | 90 ignoră |
| Multicast + IGMP snooping | 1 | 10 (doar membrii) | 0 |
| Multicast fără snooping | 1 | 100 (ca broadcast) | 90 ignoră |
| 10× Unicast | 10 | 10 | 0, dar 10× trafic |

**Analiza distractorilor:**

| Opțiune | De ce e greșită | Misconceptie vizată |
|---------|-----------------|---------------------|
| **A** | "Un pachet" nu înseamnă "procesare minimă" | Ignorare overhead CPU |
| **C** | Cu IGMP snooping, multicast e superior | Ignorare capabilități switch |
| **D** | Corect că ajunge doar la 10, dar generează 10× trafic pe rețea | Trade-off trafic vs procesare |

**Notă pentru instructor:** Dacă switch-ul NU are IGMP snooping, multicast se comportă ca broadcast la Layer 2.

</details>

---

## 🗳️ Întrebarea 5: TTL și Propagare Multicast

### Scenariu

Un dezvoltator setează TTL=0 pentru pachetele multicast:

```python
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 0)
sock.sendto(b"Test", ('239.0.0.1', 5008))
```

### Întrebare

Cine va primi acest pachet?

### Opțiuni

| | Răspuns |
|---|---------|
| **A** | Toți membrii grupului din rețeaua locală |
| **B** | Nimeni, pachetul e invalid |
| **C** | Doar procesele de pe aceeași mașină (localhost) |
| **D** | Doar primul router |

---

### Răspuns Corect: **C**

<details>
<summary>Explicație detaliată (pentru după vot)</summary>

**C este corect.** TTL=0 înseamnă că pachetul NU părăsește mașina locală. E livrat doar proceselor locale înscrise în grupul multicast.

**Tabel TTL:**

| TTL | Scop | Cine primește |
|-----|------|---------------|
| 0 | Doar localhost | Procese locale |
| 1 | Rețea locală | Segment L2, fără routere |
| 2-31 | Site/Campus | Traversează routere locale |
| 32 | Organizație | Routere organizaționale |
| 255 | Nelimitat | Tot internetul (teoretic) |

**Analiza distractorilor:**

| Opțiune | De ce e greșită | Misconceptie vizată |
|---------|-----------------|---------------------|
| **A** | TTL=0 nu ajunge în rețea | Ignorare TTL |
| **B** | E valid, doar că nu iese din mașină | Confuzie validitate |
| **D** | TTL=0 înseamnă "0 hopuri", adică nu traversează nimic | Confuzie decrementare |

**Use case TTL=0:** Testing local, când vrei să verifici că aplicația ta multicast funcționează fără a polua rețeaua.

</details>

---

## Sumar Misconceptii Vizate

| # | Misconceptie | Întrebarea |
|---|--------------|------------|
| 1 | Bind la IP specific primește broadcast | Q1 |
| 2 | SO_BROADCAST e pentru receptor | Q1 |
| 3 | Bind la port e suficient pentru multicast | Q2 |
| 4 | Tunelul TCP e transparent la Layer 4 | Q3 |
| 5 | Broadcast și multicast sunt echivalente | Q4 |
| 6 | TTL=0 e invalid | Q5 |

---

## Note pentru Instructor

**Timing total:** ~35 minute pentru toate cele 5 întrebări

**Ordine recomandată:**
1. Q1 (Broadcast bind) - fundamentală
2. Q2 (IGMP membership) - esențială pentru laborator
3. Q5 (TTL) - complementară la Q2
4. Q4 (Eficiență) - conceptuală, bună pentru discuție
5. Q3 (Tunel conexiuni) - finalizare

**Materiale necesare:**
- Proiector pentru afișare întrebări
- Sistem de vot (mâini ridicate, Mentimeter, Kahoot, sau hârtii A/B/C/D)
- Wireshark pregătit pentru demonstrații post-vot

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
