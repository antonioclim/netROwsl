# Teme pentru Acasă - Săptămâna 14

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest director conține exercițiile de realizat individual pentru consolidarea cunoștințelor din laboratorul Săptămânii 14.

---

## Cerințe Generale

- **Termen limită:** Consultați platforma de curs pentru date exacte
- **Livrare:** Arhivă ZIP cu codul sursă și documentația
- **Limbaj:** Python 3.11+
- **Documentare:** Fiecare temă trebuie să includă un README cu instrucțiuni de rulare

---

## Tema 1: Protocol Echo Îmbunătățit

**Fișier:** `exercises/tema_14_01_echo_avansat.py`

### Obiectiv

Extindeți serverul TCP echo pentru a suporta comenzi multiple, transformându-l într-un server de protocol simplu.

### Cerințe

1. Implementați un parser de comenzi care recunoaște diferite tipuri de mesaje
2. Suportați cel puțin 4 comenzi:
   - `ECHO <mesaj>` - Returnează mesajul (comportament existent)
   - `TIME` - Returnează timestamp-ul curent al serverului
   - `CALC <expresie>` - Evaluează aritmetică simplă (ex: `CALC 2+3*4`)
   - `QUIT` - Închide conexiunea grațios
   - `HELP` - Listează comenzile disponibile

3. Gestionați comenzile malformate în mod grațios
4. Mențineți compatibilitatea retroactivă cu echo simplu

### Exemplu Sesiune

```
Client: ECHO Salut Lume
Server: ECHO: Salut Lume

Client: TIME
Server: TIME: 2026-01-07T12:30:45Z

Client: CALC 10+5*2
Server: CALC: 20

Client: HELP
Server: HELP: Comenzi disponibile: ECHO, TIME, CALC, QUIT, HELP

Client: QUIT
Server: QUIT: La revedere!
[conexiune închisă]
```

### Livrabile

1. `tema_14_01_server.py` - Implementarea serverului echo îmbunătățit
2. `tema_14_01_client.py` - Client interactiv pentru testare
3. `tema_14_01_test.py` - Suite de teste pentru toate comenzile
4. `tema_14_01_raport.md` - Scurt raport despre deciziile de proiectare

### Criterii de Evaluare

- Corectitudinea parsării comenzilor (30%)
- Gestionarea erorilor și cazuri limită (25%)
- Calitatea codului și documentare (20%)
- Acoperire teste (15%)
- Compatibilitate retroactivă (10%)

---

## Tema 2: Load Balancer cu Ponderi

**Fișier:** `exercises/tema_14_02_lb_ponderat.py`

### Obiectiv

Extindeți load balancer-ul pentru a suporta distribuție round-robin ponderată și implementați algoritmi addiționali de echilibrare.

### Cerințe

1. Implementați algoritmul round-robin ponderat:
   - Fiecare backend are o pondere (1-10)
   - Pondere mai mare = mai multe cereri
   - Exemplu: app1(pondere=3), app2(pondere=1) → app1 primește 75% din cereri

2. Adăugați suport pentru algoritmul least-connections:
   - Rutează către backend-ul cu cele mai puține conexiuni active
   - Urmăriți numărul de conexiuni per backend

3. Implementați configurare ponderi prin API:
   ```
   GET  /backends          - Lista backend-urilor cu ponderi
   POST /backends          - Adaugă backend nou
   PUT  /backends/<host>/weight - Actualizează ponderea
   GET  /stats             - Statistici în timp real
   PUT  /algorithm         - Schimbă algoritmul
   ```

### Livrabile

1. `tema_14_02_lb.py` - Implementarea load balancer-ului îmbunătățit
2. `tema_14_02_config.json` - Fișier de configurare exemplu
3. `tema_14_02_test.py` - Suite de teste pentru toți algoritmii
4. `tema_14_02_raport.md` - Analiză a performanței algoritmilor

### Criterii de Evaluare

- Corectitudinea algoritmilor (30%)
- Implementarea API-ului (25%)
- Acuratețea statisticilor (20%)
- Calitatea codului (15%)
- Testare exhaustivă (10%)

---

## Tema 3: Analizator PCAP Automat

**Fișier:** `exercises/tema_14_03_analizator_pcap.py`

### Obiectiv

Dezvoltați un instrument Python pentru analiza automată a fișierelor PCAP cu generare de rapoarte.

### Cerințe

1. Parsați fișiere PCAP folosind scapy sau pyshark
2. Extrageți și rezumați statistici de protocol:
   - Număr pachete per protocol (TCP, UDP, ICMP, etc.)
   - Bytes transferați per protocol
   - Ierarhie protocoale

3. Implementați analiză de conversații TCP:
   - Urmăriți stream-uri TCP (SYN -> date -> FIN)
   - Calculați durata conexiunilor
   - Numărați retransmisii per stream
   - Identificați handshake-uri incomplete

4. Detectați anomalii:
   - Semnalizați retransmisii TCP (> prag)
   - Detectați pachete RST
   - Identificați potențiale scanări de porturi

5. Generați rapoarte în format JSON și Markdown

### Format Raport

```json
{
    "sumar": {
        "fisier": "captura.pcap",
        "durata_secunde": 120.5,
        "total_pachete": 15000,
        "total_bytes": 1234567
    },
    "protocoale": {
        "TCP": {"pachete": 12000, "bytes": 1000000},
        "UDP": {"pachete": 2500, "bytes": 200000}
    },
    "conversatii_tcp": [...],
    "anomalii": [...]
}
```

### Livrabile

1. `tema_14_03_analizator.py` - Instrumentul principal de analiză
2. `tema_14_03_raport.py` - Modul de generare rapoarte
3. `tema_14_03_test.py` - Suite de teste cu PCAP-uri exemplu
4. `tema_14_03_raport_exemplu.md` - Raport generat exemplu

### Criterii de Evaluare

- Acuratețea analizei (30%)
- Calitatea detectării anomaliilor (25%)
- Claritate și completitudine raport (20%)
- Calitatea codului și documentare (15%)
- Performanță pe capturi mari (10%)

---

## Structura Directorului

```
homework/
├── README.md                    # Acest fișier
├── exercises/
│   ├── tema_14_01_echo_avansat.py    # Starter cod tema 1
│   ├── tema_14_02_lb_ponderat.py     # Starter cod tema 2
│   └── tema_14_03_analizator_pcap.py # Starter cod tema 3
└── solutions/
    └── .gitkeep                 # Rezervat pentru soluții
```

---

## Resurse Utile

- [Documentație Python socket](https://docs.python.org/3/library/socket.html)
- [Documentație Scapy](https://scapy.readthedocs.io/)
- [RFC 793 - TCP](https://datatracker.ietf.org/doc/html/rfc793)
- [RFC 7230 - HTTP/1.1](https://datatracker.ietf.org/doc/html/rfc7230)

---

## Întrebări Frecvente

**Î: Pot folosi biblioteci externe?**
R: Da, atâta timp cât sunt listate în requirements.txt și documentate.

**Î: Cum testez fără infrastructura Docker?**
R: Puteți crea servere mock sau folosi capturi PCAP pre-generate.

**Î: Pot lucra în echipă?**
R: Consultați regulamentul cursului. În mod normal, temele sunt individuale.

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
