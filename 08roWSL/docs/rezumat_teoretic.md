# Rezumat Teoretic — Săptămâna 8

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix
>
> **Vezi și:** [README principal](../README.md) | [Fișa de comenzi](fisa_comenzi.md) | [Depanare](depanare.md)

---

## Nivelul Transport

Nivelul transport asigură comunicarea logică între procese care rulează pe gazde diferite. Spre deosebire de nivelul rețea care oferă comunicare între gazde, nivelul transport extinde această comunicare la nivel de proces prin intermediul porturilor.

### 💡 De la Concret la Abstract: Porturile

**CONCRET:**
> Imaginează-ți un bloc de birouri (computerul). Adresa blocului e IP-ul. Dar în bloc sunt multe firme (aplicații). Numărul etajului/camerei = portul. Când trimiți un colet, scrii: "Strada X nr. 10 (IP), camera 80 (port)".

**PICTORIAL:**
```
┌─────────────────────────────────────────┐
│         COMPUTER (IP: 192.168.1.5)      │
│                                         │
│   ┌──────────┐  ┌──────────┐            │
│   │ Browser  │  │  Server  │            │
│   │ port:443 │  │ port:80  │            │
│   └──────────┘  └──────────┘            │
│                                         │
│   Datele ajung la IP, apoi portul       │
│   decide CARE aplicație le primește     │
└─────────────────────────────────────────┘
```

**ABSTRACT:**
```
socket.bind(("0.0.0.0", 8080))  # Ascultă pe portul 8080
# Tuple: (IP, PORT) identifică unic un proces în rețea
```

### Servicii Principale

Nivelul transport oferă două tipuri fundamentale de servicii:

**Transfer fără conexiune (UDP)** — Oferă un serviciu simplu, best-effort, fără garanții de livrare. Mesajele pot fi pierdute, duplicate sau livrate în altă ordine.

**Transfer orientat pe conexiune (TCP)** — Oferă un flux de octeți fiabil, ordonat și cu control al erorilor. Garantează livrarea corectă a datelor.

---

## Transmission Control Protocol (TCP)

TCP este un protocol de nivel transport orientat pe conexiune care oferă transfer fiabil de date.

### Caracteristici TCP

TCP asigură multiplexarea și demultiplexarea prin porturile sursă și destinație. Fiecare segment TCP conține numere de secvență și de confirmare pentru a asigura livrarea ordonată și detectarea pierderilor.

**Controlul fluxului** previne supraîncărcarea receptorului prin mecanismul ferestrei glisante. Receptorul anunță dimensiunea bufferului disponibil, iar emițătorul limitează cantitatea de date neconfirmate.

**Controlul congestiei** previne supraîncărcarea rețelei prin algoritmi precum slow start și congestion avoidance. Emițătorul ajustează dinamic rata de transmisie în funcție de condițiile rețelei.

### 💡 De la Concret la Abstract: TCP Reliability

**CONCRET:**
> TCP e ca trimiterea unui pachet prin curier cu confirmare de primire. După ce trimiți, aștepți confirmarea. Dacă nu vine în timp util, retrimiți. Dacă trimiți mai multe pachete, le numerotezi (1, 2, 3...) ca destinatarul să le pună în ordine.

**PICTORIAL:**
```
Emițător                              Receptor
    │                                     │
    │ ──── Segment 1 (seq=100) ─────────► │
    │                                     │ ✓ Primit
    │ ◄──── ACK (ack=101) ─────────────── │
    │                                     │
    │ ──── Segment 2 (seq=101) ────╳      │  (Pierdut!)
    │                                     │
    │     [Timeout - nu vine ACK]         │
    │                                     │
    │ ──── Segment 2 (seq=101) ─────────► │  (Retransmis)
    │ ◄──── ACK (ack=102) ─────────────── │
```

**ABSTRACT:**
```python
# Numărul de secvență = primul octet din segment
# ACK = următorul octet așteptat
# seq=100, len=50 bytes → ACK așteptat = 150
```

### Stabilirea Conexiunii (Three-Way Handshake)

Stabilirea unei conexiuni TCP urmează un protocol în trei pași:

1. **SYN:** Clientul trimite un segment SYN cu numărul de secvență inițial
2. **SYN-ACK:** Serverul răspunde cu SYN-ACK, confirmând recepția și trimițând propriul număr de secvență
3. **ACK:** Clientul finalizează cu ACK, confirmând recepția răspunsului serverului

Acest mecanism asigură că ambele părți sunt pregătite pentru comunicare și sincronizează numerele de secvență.

### Diagrama State TCP (Simplificată)

```
                    CLOSED
                       │
            ┌──────────┴──────────┐
            │ (client)            │ (server)
            ▼                     ▼
        SYN_SENT              LISTEN
            │                     │
            │    SYN-ACK          │ SYN
            ├─────────────────────┤
            │                     │
            ▼                     ▼
       ESTABLISHED ◄────────► ESTABLISHED
            │                     │
            │      FIN            │
            ├─────────────────────┤
            │                     │
            ▼                     ▼
      FIN_WAIT / CLOSE_WAIT / TIME_WAIT
            │                     │
            └──────────┬──────────┘
                       ▼
                    CLOSED
```

### Închiderea Conexiunii

Închiderea conexiunii folosește un schimb în patru pași. Oricare parte poate iniția închiderea trimițând FIN. Cealaltă parte confirmă cu ACK și poate continua să trimită date. Când este pregătită, trimite propriul FIN, care este confirmat cu ACK.

---

## User Datagram Protocol (UDP)

UDP este un protocol simplu, fără conexiune, care oferă multiplexare și verificare minimă a erorilor.

### Caracteristici UDP

UDP nu oferă garanții de livrare, ordonare sau detectare a duplicatelor. Aplicațiile care folosesc UDP trebuie să implementeze aceste funcționalități dacă sunt necesare.

Avantajul principal este overhead-ul redus, făcându-l potrivit pentru aplicații care tolerează pierderi sau care implementează propriile mecanisme de fiabilitate.

### Cazuri de Utilizare

UDP este preferat pentru:
- **DNS** — interogări scurte, răspunsuri rapide
- **Streaming media** — tolerează pierderi, latența contează
- **Jocuri online** — latență redusă critică
- **VoIP** — comunicare în timp real

---

## 🗳️ PEER INSTRUCTION: TCP vs UDP pentru Aplicații

**Scenariu:**
Dezvolți o aplicație de video-conferință (precum Zoom).

**Întrebare:**
Ce combinație de protocoale ar fi cea mai potrivită?

**Opțiuni:**
- A) TCP pentru tot (video, audio, chat)
- B) UDP pentru video/audio, TCP pentru chat/control
- C) UDP pentru tot
- D) HTTP/3 pentru tot

<details>
<summary>📋 Răspuns</summary>

**Corect: B**

- Video/audio: UDP — tolerează pierderi, latența e critică
- Chat/control: TCP — mesajele trebuie să ajungă complet și în ordine
- Zoom folosește exact această abordare!
</details>

---

## HTTP peste TCP

HTTP folosește TCP ca protocol de transport pentru a beneficia de transferul fiabil de date.

### De Ce TCP pentru HTTP

HTTP necesită livrarea corectă a fiecărui octet din cerere și răspuns. Paginile web, imaginile și alte resurse trebuie să ajungă integre. TCP asigură că datele corupte sau pierdute sunt retransmise.

Ordonarea este critică pentru reconstruirea corectă a conținutului. Antetele HTTP trebuie procesate înainte de corp, iar corpul trebuie să fie complet pentru a fi utilizabil.

### Evoluția HTTP

| Versiune | Transport | Caracteristici |
|----------|-----------|----------------|
| HTTP/1.0 | TCP | O conexiune per cerere |
| HTTP/1.1 | TCP | Conexiuni persistente, pipelining |
| HTTP/2 | TCP | Multiplexare fluxuri, compresie headers |
| HTTP/3 | QUIC/UDP | Elimină head-of-line blocking |

---

## Arhitectura Proxy Invers

Un proxy invers acționează ca intermediar între clienți și servere, acceptând cereri de la clienți și redirecționându-le către serverele backend.

### 💡 De la Concret la Abstract: Load Balancing

**CONCRET:**
> Imaginează-ți casele de marcat la un supermarket mare. Când intri, un angajat (load balancer) te direcționează către casa cu cea mai scurtă coadă. Nu alegi tu casa — ești distribuit eficient.

**PICTORIAL:**
```
   Clienți        Angajat (LB)           Case de marcat
   ┌─────┐                               ┌─────────────┐
   │ 👤  │ ────►  ┌─────────┐  ──1──►   │ Casa 1 ████ │
   │ 👤  │        │ nginx   │            │ Casa 2 ██   │
   │ 👤  │ ◄────  │ :8080   │  ──2──►   │ Casa 3 █    │
   │ 👤  │        └─────────┘            └─────────────┘
   └─────┘                               
                  Algoritmi:
                  - round-robin (pe rând)
                  - least-conn (mai puțin ocupat)
                  - weighted (cu ponderi)
```

**ABSTRACT:**
```nginx
upstream backend {
    least_conn;  # sau: round-robin, ip_hash
    server backend1:8080 weight=5;
    server backend2:8080 weight=3;
    server backend3:8080 weight=1;
}
```

### Beneficii

- **Echilibrarea încărcării** — distribuie traficul între multiple servere
- **Terminarea TLS** — descarcă criptografia de la backend-uri
- **Cache** — reduce încărcarea pentru conținut static
- **Securitate** — ascunde infrastructura internă

### Antetele de Proxy

Când un proxy redirecționează cereri, informația despre clientul original poate fi pierdută. Antetele speciale păstrează această informație:

| Antet | Scop | Exemplu |
|-------|------|---------|
| `X-Forwarded-For` | IP-ul original al clientului | `192.168.1.100, 10.0.0.1` |
| `X-Forwarded-Proto` | Protocolul original | `https` |
| `X-Forwarded-Host` | Hostname-ul original | `www.example.com` |

---

## TLS (Transport Layer Security)

TLS oferă securitate pentru comunicațiile de rețea prin criptare, autentificare și integritate.

### Obiective de Securitate

- **Confidențialitate** — doar părțile autorizate pot citi datele
- **Autentificare** — verifică identitatea serverului (și opțional a clientului)
- **Integritate** — detectează orice modificare a datelor în tranzit

### Handshake TLS (Simplificat)

```
Client                                  Server
   │                                       │
   │ ──── ClientHello ───────────────────► │
   │      (versiuni suportate, cipher)     │
   │                                       │
   │ ◄──── ServerHello + Certificate ───── │
   │       (versiune aleasă, certificat)   │
   │                                       │
   │ ──── Key Exchange ──────────────────► │
   │      (material pentru cheie)          │
   │                                       │
   │ ◄──── Finished ─────────────────────► │
   │                                       │
   │ ════════ COMUNICARE CRIPTATĂ ═════════│
```

TLS 1.3 a simplificat handshake-ul la un singur round-trip în cazul optim.

---

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson.
- RFC 793 — Transmission Control Protocol
- RFC 768 — User Datagram Protocol
- RFC 9110 — HTTP Semantics
- RFC 8446 — Transport Layer Security 1.3

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
