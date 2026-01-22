# Întrebări Peer Instruction — Săptămâna 6

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim

Folosește aceste întrebări pentru votare în clasă (Think-Pair-Share).

**Protocol recomandat:**
1. Prezintă scenariul (1 min)
2. Vot individual în liniște (1 min)
3. Discuție în perechi (2-3 min)
4. Re-vot (30 sec)
5. Explicație instructor (2 min)

---

## PI-1: Port Mapping NAT

### Scenariu

Un host intern (192.168.1.10) se conectează la un server extern (8.8.8.8:443).
Routerul NAT are IP-ul public 203.0.113.1.

### Întrebare

Ce adresă IP sursă vede serverul extern în pachetul primit?

### Opțiuni

| Cod | Răspuns | Explicație (pentru instructor) |
|-----|---------|-------------------------------|
| **A** | 192.168.1.10 — IP-ul original al clientului | Misconceptie: crede că NAT nu modifică sursa |
| **B** | 203.0.113.1 — IP-ul public al routerului NAT | **CORECT** |
| **C** | 8.8.8.8 — IP-ul serverului (reflectat) | Confuzie totală despre direcția traficului |
| **D** | 127.0.0.1 — localhost | Nu înțelege conceptul de adresare |

### Note instructor

- **Răspuns corect:** B
- **Țintă vot inițial:** ~60% corect
- **După discuție:** Desenează fluxul pachetului cu traducerea pe tablă
- **Demonstrație:** Rulează `nat_observer.py` și arată output-ul

---

## PI-2: Comunicare Container Docker

### Scenariu

```yaml
services:
  frontend:
    networks: [webnet]
  backend:
    networks: [webnet, dbnet]
  database:
    networks: [dbnet]
```

### Întrebare

Poate `frontend` să comunice direct cu `database`?

### Opțiuni

| Cod | Răspuns | Explicație (pentru instructor) |
|-----|---------|-------------------------------|
| **A** | Da, sunt în același fișier docker-compose | Misconceptie: crede că compose = conectivitate |
| **B** | Da, dar doar prin IP, nu prin nume | Misconceptie parțială despre DNS Docker |
| **C** | Nu, sunt pe rețele izolate fără suprapunere | **CORECT** |
| **D** | Nu, containerele nu pot comunica niciodată între ele | Înțelegere incompletă a rețelelor Docker |

### Note instructor

- **Răspuns corect:** C
- **Țintă vot inițial:** ~40% corect
- **Concept cheie:** Izolarea rețelelor Docker
- **Diagramă:** Desenează frontend ↔ backend ↔ database (dar NU frontend ↔ database)
- **Followup:** "Cum ar putea comunica frontend cu database?" (răspuns: prin backend ca proxy)

---

## PI-3: Prioritate Fluxuri OpenFlow

### Scenariu

Switch-ul OVS s1 are aceste reguli instalate:

```
priority=100: match=ip_dst=10.0.6.13 → actions=drop
priority=50:  match=ip_proto=icmp → actions=output:3
priority=10:  match=* → actions=controller
```

### Întrebare

Ce se întâmplă cu un pachet ICMP destinat adresei 10.0.6.13?

### Opțiuni

| Cod | Răspuns | Explicație (pentru instructor) |
|-----|---------|-------------------------------|
| **A** | Este trimis pe portul 3 (regula ICMP) | Misconceptie: crede că ordinea în fișier contează |
| **B** | Este aruncat (regula drop pentru .13) | **CORECT** — prioritate 100 > 50 |
| **C** | Este trimis la controller | Misconceptie: crede că ultima regulă câștigă |
| **D** | Este procesat de toate cele 3 reguli în ordine | Nu înțelege match-ul exclusiv |

### Note instructor

- **Răspuns corect:** B
- **Țintă vot inițial:** ~50% corect
- **Concept cheie:** Prioritatea determină ordinea, NU ordinea definirii
- **Demonstrație:** `ovs-ofctl dump-flows s1 --rsort=priority`
- **Analogie:** "Agentul de circulație verifică regulile după numărul paginii, nu după ordinea scrierii"

---

## PI-4: Conntrack și NAT

### Scenariu

3 hosturi interne (h1, h2, h4) fac conexiuni TCP simultane către același server extern (h3:5000).
Routerul NAT are o singură adresă IP publică (203.0.113.1).

### Întrebare

Cum diferențiază routerul NAT răspunsurile pentru fiecare host intern?

### Opțiuni

| Cod | Răspuns | Explicație (pentru instructor) |
|-----|---------|-------------------------------|
| **A** | Prin adresa MAC a fiecărui host intern | MAC-urile nu traversează routerul |
| **B** | Prin portul sursă unic alocat fiecărei conexiuni | **CORECT** — esența PAT |
| **C** | Prin TTL-ul diferit al pachetelor | TTL nu e folosit pentru identificare |
| **D** | Nu poate — de aceea NAT limitează conexiunile | Înțelegere incompletă a PAT |

### Note instructor

- **Răspuns corect:** B
- **Țintă vot inițial:** ~55% corect
- **Concept cheie:** PAT = Port Address Translation = multiplexare prin porturi
- **Demonstrație:** `conntrack -L` după exercițiul NAT cu multiple conexiuni
- **Followup:** "De ce routerul alocă porturi diferite chiar dacă h1 și h2 folosesc același port local?"

---

## PI-5: Traducere NAT Bidirecțională

### Scenariu

Output din `conntrack -L` pe routerul NAT:

```
tcp ESTABLISHED src=192.168.1.10 dst=203.0.113.2 sport=45678 dport=5000 
                src=203.0.113.2 dst=203.0.113.1 sport=5000 dport=50001
```

### Întrebare

Ce port sursă vede serverul h3 (203.0.113.2) în pachetele primite de la h1?

### Opțiuni

| Cod | Răspuns | Explicație (pentru instructor) |
|-----|---------|-------------------------------|
| **A** | 45678 — portul original folosit de h1 | Misconceptie: crede că NAT păstrează portul |
| **B** | 5000 — portul pe care ascultă serverul | Confuzie sursă/destinație |
| **C** | 50001 — portul tradus de routerul NAT | **CORECT** |
| **D** | 9000 — portul Portainer | Răspuns random/neatent |

### Note instructor

- **Răspuns corect:** C
- **Țintă vot inițial:** ~45% corect
- **Concept cheie:** Citirea tabelei conntrack (linia 1 = client→server, linia 2 = server→client tradus)
- **Demonstrație vizuală:** Desenează cele două perspective pe tablă

---

## Ghid de utilizare

### Când să folosești Peer Instruction

- După prezentarea unui concept nou (NAT, SDN, OpenFlow)
- Înainte de un exercițiu practic
- Pentru a verifica înțelegerea înainte de a avansa

### Semne că întrebarea funcționează bine

- Vot inițial distribuit (nu 90% corect, nu 90% greșit)
- Discuții animate în perechi
- Schimbare semnificativă între vot 1 și vot 2
- Întrebări de clarificare după explicație

### Dacă >80% răspund corect la primul vot

- Întrebarea e prea ușoară pentru acest grup
- Treci la următoarea întrebare sau la exercițiu

### Dacă <20% răspund corect la primul vot

- Conceptul nu a fost înțeles
- Re-explică înainte de discuția în perechi
- Consideră o demonstrație live

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim*
