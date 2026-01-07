# Teme pentru Acasă - Săptămâna 10

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Instrucțiuni Generale

1. Temele sunt individuale
2. Codul sursă trebuie să fie bine documentat cu comentarii în română
3. Includeți un fișier README.md cu instrucțiuni de rulare
4. Termenul limită: săptămâna viitoare la începutul laboratorului

---

## Tema 1: Server DNS Extins (Dificultate: Medie)

### Obiectiv
Extindeți serverul DNS din laborator pentru a suporta tipuri suplimentare de înregistrări.

### Cerințe

1. **Înregistrări MX (Mail Exchange)**
   - Adăugați suport pentru înregistrări de tip MX
   - Exemplu: `mail.lab.local` → `smtp.lab.local` cu prioritate 10

2. **Înregistrări CNAME (Alias)**
   - Adăugați suport pentru alias-uri de domenii
   - Exemplu: `www.lab.local` → `web.lab.local`

3. **Înregistrări TXT**
   - Adăugați suport pentru înregistrări text
   - Exemplu: verificări SPF pentru domeniu

### Punctaj
- Implementare MX: 3 puncte
- Implementare CNAME: 3 puncte
- Implementare TXT: 2 puncte
- Documentație și teste: 2 puncte

### Fișiere de predat
- `dns_server_extins.py` - Serverul modificat
- `test_dns.py` - Script de testare
- `README.md` - Documentație

---

## Tema 2: Client REST Complet (Dificultate: Medie)

### Obiectiv
Implementați un client Python care interacționează cu API-ul REST din laborator.

### Cerințe

1. **Client pentru toate nivelurile**
   - Implementați metode pentru Nivelul 0 (RPC)
   - Implementați metode pentru Nivelul 2 (Verbe HTTP)
   - Implementați metode pentru Nivelul 3 (HATEOAS)

2. **Navigare HATEOAS**
   - Clientul să poată naviga folosind linkurile din răspunsuri
   - Să nu hardcodeze URL-uri

3. **Interfață utilizator**
   - Meniu interactiv pentru operații CRUD
   - Afișare frumoasă a răspunsurilor JSON

### Punctaj
- Client Nivelul 0: 2 puncte
- Client Nivelul 2: 3 puncte
- Client Nivelul 3 cu navigare: 3 puncte
- Interfață utilizator: 2 puncte

### Fișiere de predat
- `client_rest.py` - Clientul implementat
- `README.md` - Documentație cu exemple de utilizare

---

## Tema 3: Analizor de Trafic HTTP (Dificultate: Ridicată)

### Obiectiv
Creați un script care analizează capturile de trafic HTTP.

### Cerințe

1. **Parsare PCAP**
   - Citiți fișiere .pcap folosind scapy sau pyshark
   - Extrageți pachetele HTTP

2. **Analiză statistică**
   - Număr de cereri per metodă (GET, POST, etc.)
   - Distribuția codurilor de stare
   - Top 10 URI-uri solicitate

3. **Raport**
   - Generați un raport în format Markdown sau HTML
   - Includeți grafice (opțional, bonus)

### Punctaj
- Parsare PCAP: 3 puncte
- Analiză statistică: 4 puncte
- Raport generat: 3 puncte
- Grafice (bonus): +2 puncte

### Fișiere de predat
- `analizor_http.py` - Scriptul de analiză
- `exemplu_raport.md` - Exemplu de raport generat
- `README.md` - Documentație

---

## Resurse Utile

- [RFC 2616 - HTTP/1.1](https://tools.ietf.org/html/rfc2616)
- [RFC 1035 - DNS](https://tools.ietf.org/html/rfc1035)
- [dnslib Documentation](https://github.com/paulc/dnslib)
- [Requests Library](https://docs.python-requests.org/)
- [Scapy Documentation](https://scapy.readthedocs.io/)

---

## Notare

| Componentă | Punctaj Maxim |
|------------|---------------|
| Funcționalitate | 7 puncte |
| Documentație | 2 puncte |
| Cod curat și comentat | 1 punct |
| **Total** | **10 puncte** |

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
