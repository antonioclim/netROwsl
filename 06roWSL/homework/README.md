# Teme pentru acasă Săptămâna 6

> Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | Laborator Rețele de Calculatoare
>
> de Revolvix

## Prezentare generală

Aceste exerciții pentru acasă extind conceptele explorate în timpul sesiunii de laborator despre NAT/PAT și Rețele Definite prin Software. Completează aceste teme pentru a-ți consolida înțelegerea mecanismelor de traducere a adreselor de rețea și a politicilor de trafic bazate pe OpenFlow.

---

## Tema 1: Analiză extinsă NAT

**Obiectiv:** Analizează comportamentul traducerilor NAT sub diverse modele de trafic.

**Sarcini:**

1. Modifică `topo_nat.py` pentru a adăuga un al patrulea host (h4) în rețeaua privată cu IP 192.168.1.40/24
2. Generează conexiuni TCP simultane de la h1, h2 și h4 către h3 folosind `nat_observer.py`
3. Capturează traficul pe rnat-eth1 (interfața publică) folosind tcpdump
4. Documentează intrările din tabela de traducere PAT observate

**Livrabile:**
- Fișierul de topologie modificat
- Captura de pachete (PCAP) arătând traducerile
- Analiză scrisă (300-500 cuvinte) explicând comportamentul observat

**Criterii de evaluare:**
- Modificarea corectă a topologiei (25%)
- Captura completă de pachete (25%)
- Analiză precisă a comportamentului PAT (50%)

---

## Tema 2: Implementare politici SDN

**Obiectiv:** Proiectează și implementează politici OpenFlow personalizate folosind OS-Ken.

**Sarcini:**

1. Extinde topologia SDN pentru a include un al patrulea host (h4: 10.0.6.14/24)
2. Implementează următoarele reguli de politică:
   - h1 ↔ h2: PERMITE tot traficul
   - h1 ↔ h3: PERMITE doar ICMP, BLOCHEAZĂ TCP/UDP
   - h1 → h4: PERMITE doar TCP portul 80
   - h4 → h1: BLOCHEAZĂ tot traficul (politică asimetrică)
3. Testează fiecare politică cu generatoare de trafic adecvate

**Livrabile:**
- Fișierul de topologie modificat cu h4
- Controller actualizat cu politicile noi
- Script de test demonstrând fiecare politică
- Documentație a intrărilor din tabela de fluxuri

**Criterii de evaluare:**
- Extensia corectă a topologiei (20%)
- Acuratețea implementării politicilor (40%)
- Testare comprehensivă (25%)
- Calitatea documentației (15%)

---

## Tema 3: Analiză comparativă

**Obiectiv:** Compară NAT tradițional cu abordările bazate pe SDN pentru gestionarea adreselor de rețea.

**Sarcini:**

1. Cercetează și documentează cel puțin trei alternative bazate pe SDN la NAT tradițional
2. Implementează un exemplu simplu al unei alternative folosind Mininet/OS-Ken
3. Compară metricile de performanță și complexitate

**Livrabile:**
- Document de cercetare (800-1000 cuvinte)
- Implementare funcțională
- Tabel comparativ cu metrici

**Criterii de evaluare:**
- Profunzimea și acuratețea cercetării (35%)
- Funcționalitatea implementării (40%)
- Calitatea analizei (25%)

---

## Ghid de trimitere

- Trimite toate fișierele ca o singură arhivă ZIP numită `tema6_<id_student>.zip`
- Include un `README.txt` cu numele tău, ID-ul de student și orice instrucțiuni speciale
- Asigură-te că toate fișierele Python au sintaxă validă înainte de trimitere
- Include capturile de pachete în format PCAP (nu capturi de ecran)

**Termen limită:** Consultă calendarul cursului pe portalul universitar

---

## Resurse

- Slide-urile cursului: Componente NAT/PAT și SDN
- Ghidul de laborator: Documentația Săptămânii 6
- RFC 3022: Translator tradițional de adrese de rețea IP (NAT tradițional)
- Specificația OpenFlow 1.3.5

---

*Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
