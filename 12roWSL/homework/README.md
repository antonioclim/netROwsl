# Teme pentru Acasă - Săptămâna 12

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

## Prezentare Generală

Acest director conține exercițiile de lucru individual pentru Săptămâna 12. Temele sunt concepute pentru a consolida înțelegerea protocoalelor de email (SMTP) și a mecanismelor de apel de procedură la distanță (RPC).

**Termen limită:** Consultați platforma de cursuri pentru data exactă.

**Modalitate de predare:** Arhivă ZIP conținând codul sursă, capturile de pachete și documentația.

---

## Tema 1: Client SMTP cu Atașamente MIME

### Obiectiv

Implementați un client SMTP în Python capabil să trimită emailuri cu atașamente binare folosind codificarea MIME (Multipurpose Internet Mail Extensions).

### Cerințe Funcționale

1. **Conectare SMTP**
   - Stabiliți conexiune la serverul SMTP de laborator (localhost:1025)
   - Implementați secvența completă HELO → MAIL FROM → RCPT TO → DATA → QUIT

2. **Suport MIME**
   - Creați mesaje multipart (text + atașamente)
   - Implementați codificarea Base64 pentru fișiere binare
   - Setați corect anteturile Content-Type și Content-Transfer-Encoding

3. **Funcționalități**
   - Suport pentru mai mulți destinatari (TO, CC, BCC)
   - Atașare a cel puțin 2 tipuri de fișiere (ex: .txt, .png, .pdf)
   - Afișarea progresului transmisiei

### Cerințe Tehnice

- Utilizați numai biblioteca `socket` pentru comunicația SMTP (nu `smtplib`)
- Biblioteca `email` poate fi folosită pentru construcția mesajelor MIME
- Codul trebuie să fie modular și bine documentat
- Includeți tratarea erorilor pentru scenarii comune

### Criterii de Evaluare

| Criteriu | Puncte |
|----------|--------|
| Conexiune SMTP funcțională | 20 |
| Implementare MIME corectă | 25 |
| Codificare Base64 | 15 |
| Suport destinatari multipli | 15 |
| Tratarea erorilor | 10 |
| Documentație și cod curat | 15 |
| **Total** | **100** |

---

## Tema 2: Metodă JSON-RPC Personalizată

### Obiectiv

Extindeți serverul JSON-RPC cu o metodă nouă `statistici_text` care analizează un șir de caractere și returnează diverse statistici.

### Cerințe Funcționale

1. **Metoda `statistici_text`**
   
   Rezultat așteptat (obiect JSON):
   ```json
   {
     "lungime": 42,
     "numar_cuvinte": 8,
     "numar_propozitii": 2,
     "frecventa_caractere": {"a": 5, "e": 3},
     "este_palindrom": false,
     "cuvant_cel_mai_lung": "exemplu",
     "vocale": 15,
     "consoane": 20
   }
   ```

2. **Comparație XML-RPC**
   - Implementați aceeași metodă și în serverul XML-RPC
   - Documentați diferențele de implementare

### Criterii de Evaluare

| Criteriu | Puncte |
|----------|--------|
| Implementare JSON-RPC corectă | 25 |
| Implementare XML-RPC corectă | 20 |
| Calcul statistici corect | 20 |
| Tratarea erorilor | 15 |
| Teste unitare | 10 |
| Documentație | 10 |
| **Total** | **100** |

---

## Tema 3: Raport de Analiză a Protocoalelor

### Obiectiv

Realizați o analiză comparativă detaliată a protocoalelor SMTP, JSON-RPC, XML-RPC și gRPC folosind capturi de pachete și măsurători de performanță.

### Cerințe

1. **Capturi Wireshark** pentru fiecare protocol
2. **Analiză Overhead** - dimensiuni anteturi vs payload
3. **Măsurători de Latență** - 100 cereri consecutive
4. **Analiză Calitativă** - comparație lizibilitate și cazuri de utilizare

### Criterii de Evaluare

| Criteriu | Puncte |
|----------|--------|
| Capturi Wireshark complete | 20 |
| Măsurători cantitative | 20 |
| Grafice și vizualizări | 15 |
| Analiză și interpretare | 25 |
| Calitatea redactării | 10 |
| Formatare și prezentare | 10 |
| **Total** | **100** |

**Lungime minimă raport:** 1500 cuvinte

---

## Instrucțiuni de Predare

1. Arhivă ZIP: `Nume_Prenume_Grupa_Saptamana12.zip`
2. Includeți toate fișierele sursă, capturile și documentația
3. Asigurați-vă că codul rulează fără erori

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
