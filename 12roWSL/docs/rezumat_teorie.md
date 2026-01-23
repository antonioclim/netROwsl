# Rezumat Teoretic - Săptămâna 12

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

## Analogii pentru Înțelegere (CPA)

| Concept | CONCRET (din viața de zi cu zi) | PICTORIAL | ABSTRACT (tehnic) |
|---------|--------------------------------|-----------|-------------------|
| **SMTP** | Oficiu poștal: depui scrisoarea, poștașul o duce | Client → Server → Inbox | MAIL FROM → RCPT TO → DATA → QUIT |
| **Coduri SMTP** | Răspunsuri la ghișeu: "OK", "Revino mâine", "Nu avem" | 2xx=verde, 4xx=galben, 5xx=roșu | 250, 450, 550 |
| **RPC** | Telecomandă TV: apeși buton local, TV-ul execută | Stub → Rețea → Stub → Funcție | proxy.add(10, 20) |
| **JSON-RPC** | Comandă la restaurant în română (citibil) | JSON cu nume de câmpuri | {"method":"add","params":[10,20]} |
| **XML-RPC** | Formular oficial cu toate câmpurile | XML verbose cu tag-uri | <methodCall><methodName>add |
| **gRPC/Protobuf** | Cod secret între spioni (dicționar necesar) | Bytes: 08 0A 10 14 | Schema .proto compilată |
| **Serializare** | Împachetare bagaje pentru avion | Obiect → Bytes → Obiect | marshal / unmarshal |

## Protocolul SMTP

SMTP (Simple Mail Transfer Protocol, RFC 5321) - protocol pentru transmisia poștei electronice.

### Comenzi Fundamentale

| Comandă | Descriere |
|---------|-----------|
| HELO/EHLO | Identificare client |
| MAIL FROM | Specifică expeditorul |
| RCPT TO | Specifică destinatarul |
| DATA | Începe corpul mesajului |
| QUIT | Închide conexiunea |

### Coduri de Răspuns

| Clasă | Semnificație |
|-------|--------------|
| 2xx | Succes |
| 3xx | Date suplimentare necesare |
| 4xx | Eroare temporară |
| 5xx | Eroare permanentă |

## Remote Procedure Call (RPC)

RPC e un mecanism de comunicare care permite unui program să execute o procedură pe alt sistem ca și cum ar fi locală.

### Comparație Protocoale

| Aspect | JSON-RPC | XML-RPC | gRPC |
|--------|----------|---------|------|
| Format date | JSON | XML | Protocol Buffers |
| Transport | HTTP/1.1 | HTTP/1.1 | HTTP/2 |
| Dimensiune | Mic | Mare | Foarte mic |
| Citibil | Da | Da | Nu |
| Streaming | Nu | Nu | Da |
| Batch | Da | Nu | Da |

### Criterii de Selecție

**JSON-RPC:** Simplitate, browsere web, debugging ușor
**XML-RPC:** Sisteme legacy, introspecție nativă
**gRPC:** Performanță, microservicii, streaming

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
