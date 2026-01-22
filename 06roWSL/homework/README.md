# Teme pentru acasă Săptămâna 6

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim

## Prezentare generală

Aceste exerciții extind conceptele explorate în timpul sesiunii de laborator despre NAT/PAT și Rețele Definite prin Software.

---

## Tema 1: Analiză extinsă NAT

**Nivel Bloom:** APPLY + ANALYSE  
**Durată estimată:** 2 ore  
**Punctaj:** 15%

### Obiectiv

Analizează comportamentul traducerilor NAT sub diverse modele de trafic.

### Sarcini

1. Modifică `topo_nat.py` pentru a adăuga un al patrulea host (h4) în rețeaua privată
2. Generează conexiuni TCP simultane de la h1, h2 și h4 către h3
3. Capturează traficul pe rnat-eth1 folosind tcpdump
4. Documentează intrările din tabela de traducere PAT

### Livrabile

- Fișierul de topologie modificat
- Captura de pachete (PCAP)
- Analiză scrisă (300-500 cuvinte)

### Rubrică auto-evaluare Tema 1

| Criteriu | Punctaj | Verificare |
|----------|---------|------------|
| Topologia modificată funcționează | 5p | □ `pingall` trece pentru toate hosturile |
| Captura PCAP conține traduceri | 4p | □ Văd IP-uri traduse în Wireshark |
| Analiza identifică pattern-ul PAT | 4p | □ Am explicat alocarea porturilor |
| Documentație clară | 2p | □ README include pașii de reproducere |
| **Total** | **15p** | |

---

## Tema 2: Implementare politici SDN personalizate

**Nivel Bloom:** APPLY + ANALYSE  
**Durată estimată:** 2-3 ore  
**Punctaj:** 15%

### Obiectiv

Proiectează și implementează politici OpenFlow personalizate.

### Sarcini

1. Extinde topologia SDN pentru a include un al patrulea host (h4: 10.0.6.14/24)
2. Implementează regulile:
   - h1 ↔ h2: PERMITE tot traficul
   - h1 ↔ h3: PERMITE doar ICMP
   - h1 → h4: PERMITE doar TCP portul 80
   - h4 → h1: BLOCHEAZĂ tot traficul
3. Testează fiecare politică

### Livrabile

- Fișierul de topologie modificat
- Controller actualizat
- Script de test
- Documentație

### Rubrică auto-evaluare Tema 2

| Criteriu | Punctaj | Verificare |
|----------|---------|------------|
| Topologia cu h4 pornește | 3p | □ `nodes` arată 4 hosturi |
| Politica h1↔h2 funcționează | 3p | □ `h1 ping h2` OK |
| Politica h1↔h3 (doar ICMP) | 3p | □ ping OK, TCP blocat |
| Politica h1→h4 (doar TCP:80) | 3p | □ HTTP OK, restul blocat |
| Documentație completă | 3p | □ Explică fiecare regulă |
| **Total** | **15p** | |

---

## Tema 3: Analiză comparativă

**Nivel Bloom:** ANALYSE  
**Durată estimată:** 3 ore  
**Punctaj:** 15%

### Obiectiv

Compară NAT tradițional cu abordările bazate pe SDN.

### Sarcini

1. Cercetează cel puțin trei alternative bazate pe SDN la NAT tradițional
2. Implementează un exemplu simplu folosind Mininet/OS-Ken
3. Compară metricile de performanță și complexitate

### Livrabile

- Document de cercetare (800-1000 cuvinte)
- Implementare funcțională
- Tabel comparativ

### Rubrică auto-evaluare Tema 3

| Criteriu | Punctaj | Verificare |
|----------|---------|------------|
| 3+ alternative cercetate | 4p | □ Surse academice citate |
| Implementare funcțională | 5p | □ Codul rulează fără erori |
| Tabel comparativ complet | 3p | □ Min. 5 criterii comparate |
| Analiză critică | 3p | □ Pro/contra pentru fiecare |
| **Total** | **15p** | |

---

## Tema 4: Evaluare Critică NAT vs SDN-NAT

**Nivel Bloom:** EVALUATE  
**Durată estimată:** 2-3 ore  
**Punctaj:** 15%

### Context

O companie mică (50 angajați) trebuie să aleagă între:
- **Opțiunea A:** Router Linux cu iptables NAT
- **Opțiunea B:** Switch OpenFlow cu controller SDN care implementează NAT

### Sarcini

**1. Completează tabelul de evaluare (40%)**

| Criteriu | NAT Tradițional | SDN-NAT | Câștigător |
|----------|-----------------|---------|------------|
| Cost hardware inițial | | | |
| Complexitate configurare | | | |
| Scalabilitate (50→500 users) | | | |
| Vizibilitate trafic | | | |
| Flexibilitate politici | | | |
| Single point of failure | | | |
| Latență per-pachet | | | |
| Expertiză necesară | | | |

**2. Scrie recomandarea (35%)**

200-300 cuvinte cu cel puțin 3 argumente tehnice.

**3. Scenariu alternativ (25%)**

50-100 cuvinte despre când alegerea opusă ar fi mai bună.

### Livrabil

`homework/exercises/hw_6_04_evaluare_nat_sdn.md`

### Rubrică auto-evaluare Tema 4

| Criteriu | Punctaj | Verificare |
|----------|---------|------------|
| Tabel complet (8 criterii) | 6p | □ Toate celulele completate |
| Recomandare cu 3+ argumente | 5p | □ Argumente tehnice, nu opinii |
| Scenariu alternativ logic | 4p | □ Justificare coerentă |
| **Total** | **15p** | |

---

## Tema 5: Proiectare Topologie Campus Hibridă

**Nivel Bloom:** CREATE  
**Durată estimată:** 4-5 ore  
**Punctaj:** 20%

### Context

Proiectează arhitectura de rețea pentru un campus universitar cu:
- 3 clădiri cu câte 100 utilizatori fiecare
- 1 datacenter central
- Acces internet printr-un singur punct de ieșire
- Izolare între departamente

### Cerințe funcționale

1. Izolare inter-departamente
2. Acces la datacenter pentru toate departamentele
3. Acces extern la serverele web
4. NAT pentru ieșire

### Livrabile

**1. Diagrama topologiei (20%)**

**2. Fișier topologie Mininet (35%)**
- Minim 3 switch-uri OpenFlow
- 1 router NAT
- Comentarii explicative

**3. Controller SDN (30%)**
- Politici de izolare
- Logging pentru pachetele blocate

**4. Documentație (15%)**
- 300-500 cuvinte
- Justificarea deciziilor arhitecturale
- Cum s-ar scala soluția

### Bonus (până la +10%)

- Implementare failover
- Dashboard de monitorizare
- Teste automate

### Rubrică auto-evaluare Tema 5

| Criteriu | Punctaj | Verificare |
|----------|---------|------------|
| Diagrama completă și lizibilă | 4p | □ Include toate cele 3 clădiri + datacenter |
| Topologia Mininet pornește | 7p | □ `sudo python3 topo_campus.py` OK |
| Politicile SDN funcționează | 6p | □ Izolarea inter-departamente verificată |
| Documentația justifică deciziile | 3p | □ Explică "de ce", nu doar "ce" |
| **Total** | **20p** | |

| Bonus | Punctaj extra | Verificare |
|-------|---------------|------------|
| Failover implementat | +4p | □ Un switch cade, rețeaua funcționează |
| Dashboard monitorizare | +3p | □ Interfață web cu statistici |
| Teste automate | +3p | □ Script care verifică toate politicile |

---

## Ghid de trimitere

- Trimite toate fișierele ca o singură arhivă ZIP: `tema6_<id_student>.zip`
- Include un `README.txt` cu numele și ID-ul de student
- Asigură-te că fișierele Python au sintaxă validă
- Include capturile în format PCAP

**Termen limită:** Consultă calendarul cursului

---

## Checklist pre-trimitere

Înainte de a trimite, verifică:

```bash
# 1. Sintaxa Python este validă
python3 -m py_compile *.py

# 2. Topologiile pornesc
sudo python3 topo_*.py --test

# 3. Documentația există
ls *.md README.txt

# 4. Arhiva este completă
unzip -l tema6_<id>.zip
```

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de ing. dr. Antonio Clim*
