# Tema 2: Plan de Migrare la IPv6

> Laborator Rețele de Calculatoare – Săptămâna 5
> ASE, Informatică Economică | realizat de Revolvix

## Obiective

- Înțelegerea structurii adreselor IPv6
- Proiectarea unei scheme de adresare IPv6
- Planificarea unei strategii de migrare dual-stack

## Scenariu

O companie de dimensiuni medii cu rețea IPv4 existentă primește o alocare IPv6 `/48` de la ISP:

**Prefix alocat:** `2001:db8:cafe::/48`

Rețeaua curentă IPv4 are următoarea structură:

| Segment | Descriere | VLAN | IPv4 Actual |
|---------|-----------|------|-------------|
| Utilizatori | Stații de lucru | 10 | 192.168.10.0/24 |
| Servere | Centru de date | 20 | 192.168.20.0/24 |
| Management | Echipamente rețea | 30 | 192.168.30.0/24 |
| Vizitatori | Wi-Fi public | 40 | 192.168.40.0/24 |
| DMZ | Servere publice | 50 | 10.0.50.0/24 |
| VoIP | Telefonie | 60 | 10.0.60.0/24 |

## Cerințe

### Partea A: Schema de Adresare IPv6 (30 puncte)

1. Proiectați o schemă de adresare IPv6 pentru toate cele 6 segmente
2. Folosiți subrețele `/64` pentru fiecare segment
3. Documentați logica de numerotare a subrețelelor

**Format tabel:**

| Segment | VLAN | Subrețea IPv6 | Gateway IPv6 |
|---------|------|---------------|--------------|
| | | | |

### Partea B: Strategia de Migrare (30 puncte)

Descrieți strategia de migrare dual-stack răspunzând la următoarele:

1. **Faza 1 - Pregătire** (Ce trebuie verificat/actualizat?)
   - Compatibilitate echipamente
   - Actualizări software necesare
   - Training personal IT

2. **Faza 2 - Implementare Dual-Stack** (Cum coexistă IPv4 și IPv6?)
   - Ordinea implementării pe segmente
   - Configurare servere DNS (AAAA records)
   - Testare conectivitate

3. **Faza 3 - Tranziție** (Cum se face trecerea completă?)
   - Criterii pentru dezactivarea IPv4
   - Plan de rollback în caz de probleme

### Partea C: Autoconfigurare și DHCPv6 (20 puncte)

1. Explicați diferența între SLAAC și DHCPv6 Stateful
2. Pentru fiecare segment, recomandați metoda de configurare a adreselor și justificați alegerea:

| Segment | Metodă recomandată | Justificare |
|---------|-------------------|-------------|
| Utilizatori | | |
| Servere | | |
| ... | | |

### Partea D: Securitate IPv6 (20 puncte)

Identificați și descrieți:

1. **3 amenințări specifice IPv6** care nu există în IPv4
2. **3 măsuri de securitate** recomandate pentru rețeaua IPv6

## Format Livrabil

- Fișier PDF sau Word cu toate răspunsurile
- Numele fișierului: `Tema2_NumePrenume_Grupa.pdf`
- Includeți diagrame unde este relevant

## Criterii de Evaluare

| Criteriu | Punctaj |
|----------|---------|
| Schema de adresare corectă și logică | 30 |
| Strategie de migrare detaliată | 30 |
| Analiza SLAAC vs DHCPv6 | 20 |
| Considerații de securitate | 15 |
| Formatare și prezentare | 5 |
| **Total** | **100** |

## Indicații

### Structura Prefixului /48

```
2001:db8:cafe:XXXX::/64
               │
               └── ID Subrețea (16 biți = 65.536 subrețele posibile)
```

### Exemplu de numerotare logică

```
2001:db8:cafe:0010::/64  → VLAN 10 (Utilizatori)
2001:db8:cafe:0020::/64  → VLAN 20 (Servere)
...
```

### Verificare cu scripturile din kit

```powershell
# Generează subrețele IPv6
python src/exercises/ex_5_02_vlsm_ipv6.py subretele-ipv6 "2001:db8:cafe::/48" --numar 6

# Comprimare adresă
python src/exercises/ex_5_02_vlsm_ipv6.py ipv6-comprimare "2001:0db8:cafe:0010:0000:0000:0000:0001"
```

## Resurse Suplimentare

- RFC 8200 - Internet Protocol, Version 6 (IPv6)
- RFC 4862 - IPv6 Stateless Address Autoconfiguration
- RFC 8415 - Dynamic Host Configuration Protocol for IPv6 (DHCPv6)

---

*Termen de predare: Conform indicațiilor de la seminar*
