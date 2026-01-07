# Rezumat Teoretic - Săptămâna 12

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

## Cuprins

1. [Protocolul SMTP](#protocolul-smtp)
2. [Protocolul POP3 vs IMAP](#pop3-vs-imap)
3. [Remote Procedure Call (RPC)](#remote-procedure-call-rpc)
4. [JSON-RPC 2.0](#json-rpc-20)
5. [XML-RPC](#xml-rpc)
6. [gRPC și Protocol Buffers](#grpc-și-protocol-buffers)
7. [Comparație între Protocoale](#comparație-între-protocoale)

---

## Protocolul SMTP

### Prezentare Generală

**SMTP** (Simple Mail Transfer Protocol) este protocolul standard pentru transmisia poștei electronice pe Internet. Definit în RFC 5321, SMTP utilizează un model client-server în care mesajele sunt "împinse" (push) de la client către server.

### Porturi Standard

| Port | Descriere | Securitate |
|------|-----------|------------|
| 25 | SMTP standard (server-to-server) | Fără criptare |
| 587 | SMTP submission (client-to-server) | STARTTLS |
| 465 | SMTPS (depreciat, revitalizat) | TLS implicit |

### Comenzi SMTP Fundamentale

| Comandă | Sintaxă | Descriere |
|---------|---------|-----------|
| HELO | `HELO <domeniu>` | Identificare client (SMTP de bază) |
| EHLO | `EHLO <domeniu>` | Identificare client (ESMTP cu extensii) |
| MAIL FROM | `MAIL FROM:<adresă>` | Specifică expeditorul |
| RCPT TO | `RCPT TO:<adresă>` | Specifică destinatarul |
| DATA | `DATA` | Începe transmisia mesajului |
| QUIT | `QUIT` | Închide conexiunea |
| RSET | `RSET` | Resetează tranzacția curentă |
| VRFY | `VRFY <adresă>` | Verifică o adresă (adesea dezactivat) |
| NOOP | `NOOP` | Operație nulă (keep-alive) |

### Coduri de Răspuns SMTP

| Clasă | Semnificație | Exemple |
|-------|--------------|---------|
| 2xx | Succes | 220 (salut), 250 (OK), 221 (închidere) |
| 3xx | Date suplimentare necesare | 354 (trimite mesajul) |
| 4xx | Eroare temporară | 421 (serviciu indisponibil), 450 (cutie poștală ocupată) |
| 5xx | Eroare permanentă | 550 (cutie inexistentă), 553 (sintaxă invalidă) |

### Fazele unei Tranzacții SMTP

```
1. Conexiune TCP    → Client se conectează la server
2. Banner           ← Server: 220 mail.example.com SMTP ready
3. Identificare     → Client: EHLO client.example.com
                    ← Server: 250-mail.example.com
                              250-SIZE 35882577
                              250 8BITMIME
4. Expeditor        → Client: MAIL FROM:<sender@example.com>
                    ← Server: 250 OK
5. Destinatar       → Client: RCPT TO:<recipient@example.com>
                    ← Server: 250 OK
6. Date             → Client: DATA
                    ← Server: 354 Start mail input
                    → Client: [anteturi și corp mesaj]
                    → Client: .
                    ← Server: 250 OK: message queued
7. Închidere        → Client: QUIT
                    ← Server: 221 Bye
```

---

## POP3 vs IMAP

### POP3 (Post Office Protocol v3)

- **Port:** 110 (sau 995 pentru POP3S)
- **Model:** Descărcare și ștergere
- **Stare:** Fără stare pe server după descărcare
- **Utilizare:** Un singur dispozitiv

### IMAP (Internet Message Access Protocol)

- **Port:** 143 (sau 993 pentru IMAPS)
- **Model:** Acces și sincronizare
- **Stare:** Mesajele rămân pe server
- **Utilizare:** Dispozitive multiple, foldere

### Comparație

| Caracteristică | POP3 | IMAP |
|----------------|------|------|
| Stocare mesaje | Local | Server |
| Acces multi-dispozitiv | Dificil | Nativ |
| Lățime de bandă | Mai mică | Mai mare |
| Spațiu server | Redus | Necesar |
| Funcții avansate | Limitate | Bogate |

---

## Remote Procedure Call (RPC)

### Conceptul RPC

RPC este o paradigmă de comunicare între procese care permite unui program să execute o procedură (subrutină) pe un alt spațiu de adrese (de obicei pe un alt calculator) ca și cum ar fi un apel local.

### Componente RPC

```
┌─────────────────┐                     ┌─────────────────┐
│     CLIENT      │                     │     SERVER      │
│                 │                     │                 │
│  ┌───────────┐  │     Rețea           │  ┌───────────┐  │
│  │ Aplicație │  │  ◄──────────────►   │  │ Serviciu  │  │
│  └─────┬─────┘  │                     │  └─────┬─────┘  │
│        │        │                     │        │        │
│  ┌─────▼─────┐  │                     │  ┌─────▼─────┐  │
│  │Client Stub│  │                     │  │Server Stub│  │
│  └─────┬─────┘  │                     │  └─────┬─────┘  │
│        │        │                     │        │        │
│  ┌─────▼─────┐  │                     │  ┌─────▼─────┐  │
│  │ Transport │  │◄───────────────────►│  │ Transport │  │
│  └───────────┘  │                     │  └───────────┘  │
└─────────────────┘                     └─────────────────┘
```

### Pașii unui Apel RPC

1. **Client:** Apelează stub-ul local
2. **Client Stub:** Serializează parametrii (marshalling)
3. **Transport Client:** Trimite mesajul prin rețea
4. **Transport Server:** Primește mesajul
5. **Server Stub:** Deserializează parametrii (unmarshalling)
6. **Server:** Execută procedura
7. **Server Stub:** Serializează rezultatul
8. **Transport Server:** Trimite răspunsul
9. **Client Stub:** Deserializează rezultatul
10. **Client:** Primește rezultatul ca de la un apel local

---

## JSON-RPC 2.0

### Caracteristici

- Protocol ușor, bazat pe JSON
- Transport-agnostic (HTTP, WebSocket, TCP)
- Suport pentru notificări (fără răspuns)
- Suport pentru apeluri în lot (batch)

### Structura Cererii

```json
{
    "jsonrpc": "2.0",
    "method": "subtract",
    "params": [42, 23],
    "id": 1
}
```

| Câmp | Obligatoriu | Descriere |
|------|-------------|-----------|
| jsonrpc | Da | Versiunea protocolului ("2.0") |
| method | Da | Numele metodei de apelat |
| params | Nu | Parametrii (array sau obiect) |
| id | Nu* | Identificator unic pentru corelare |

*Dacă lipsește `id`, cererea este o notificare (fără răspuns)

### Structura Răspunsului

**Succes:**
```json
{
    "jsonrpc": "2.0",
    "result": 19,
    "id": 1
}
```

**Eroare:**
```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32601,
        "message": "Method not found"
    },
    "id": 1
}
```

### Coduri de Eroare Standard

| Cod | Mesaj | Descriere |
|-----|-------|-----------|
| -32700 | Parse error | JSON invalid |
| -32600 | Invalid Request | Cerere invalidă |
| -32601 | Method not found | Metodă inexistentă |
| -32602 | Invalid params | Parametri invalizi |
| -32603 | Internal error | Eroare internă server |

### Apeluri în Lot (Batch)

```json
[
    {"jsonrpc": "2.0", "method": "add", "params": [1,2], "id": 1},
    {"jsonrpc": "2.0", "method": "subtract", "params": [5,3], "id": 2},
    {"jsonrpc": "2.0", "method": "notify", "params": ["hello"]}
]
```

---

## XML-RPC

### Caracteristici

- Predecesorul SOAP
- Format XML peste HTTP
- Tipuri de date explicite
- Suport pentru introspecție

### Tipuri de Date XML-RPC

| Tip | Exemplu XML |
|-----|-------------|
| int | `<int>42</int>` |
| double | `<double>3.14</double>` |
| string | `<string>Hello</string>` |
| boolean | `<boolean>1</boolean>` |
| dateTime | `<dateTime.iso8601>20240115T12:00:00</dateTime.iso8601>` |
| base64 | `<base64>SGVsbG8=</base64>` |
| array | `<array><data><value>...</value></data></array>` |
| struct | `<struct><member><name>...</name><value>...</value></member></struct>` |

### Exemplu Cerere XML-RPC

```xml
<?xml version="1.0"?>
<methodCall>
    <methodName>add</methodName>
    <params>
        <param><value><int>17</int></value></param>
        <param><value><int>25</int></value></param>
    </params>
</methodCall>
```

### Metode de Introspecție

| Metodă | Descriere |
|--------|-----------|
| system.listMethods | Listează toate metodele disponibile |
| system.methodHelp | Returnează documentația unei metode |
| system.methodSignature | Returnează semnătura unei metode |

---

## gRPC și Protocol Buffers

### Protocol Buffers (protobuf)

Sistem de serializare binară dezvoltat de Google:

```protobuf
syntax = "proto3";

message Person {
    string name = 1;
    int32 age = 2;
    repeated string emails = 3;
}

service Greeter {
    rpc SayHello (HelloRequest) returns (HelloReply);
}
```

### Caracteristici gRPC

- Serializare binară compactă
- HTTP/2 ca transport (multiplexare, compresie)
- Siguranța tipurilor la compilare
- Generare automată de cod pentru multiple limbaje
- Streaming bidirecțional

### Tipuri de Streaming gRPC

| Tip | Descriere |
|-----|-----------|
| Unary | O cerere, un răspuns |
| Server streaming | O cerere, flux de răspunsuri |
| Client streaming | Flux de cereri, un răspuns |
| Bidirectional | Fluxuri în ambele direcții |

---

## Comparație între Protocoale

### Tabel Comparativ

| Aspect | JSON-RPC | XML-RPC | gRPC |
|--------|----------|---------|------|
| **Format date** | JSON | XML | Protocol Buffers |
| **Transport** | HTTP, WS, TCP | HTTP | HTTP/2 |
| **Dimensiune mesaj** | Mic | Mare | Foarte mic |
| **Citibil de om** | Da | Da | Nu |
| **Tipare date** | Dinamic | Static | Static (compilat) |
| **Streaming** | Nu | Nu | Da |
| **Batch** | Da | Nu | Da |
| **Introspecție** | Nu standard | Da | Reflecție |
| **Performanță** | Bună | Moderată | Excelentă |
| **Complexitate** | Mică | Medie | Mare |

### Criterii de Selecție

**Alegeți JSON-RPC când:**
- Aveți nevoie de simplitate și ușurință în implementare
- Clienții sunt browsere web sau aplicații JavaScript
- Debugging-ul uman este important
- Performanța nu este critică

**Alegeți XML-RPC când:**
- Integrați cu sisteme legacy
- Aveți nevoie de introspecție nativă
- Tipurile de date explicite sunt importante
- Interoperabilitatea cu sisteme vechi este necesară

**Alegeți gRPC când:**
- Performanța este critică
- Comunicați între microservicii
- Aveți nevoie de streaming
- Dezvoltați în medii poliglote cu contracte stricte

---

## Referințe

- RFC 5321 - Simple Mail Transfer Protocol
- RFC 2045-2049 - MIME
- JSON-RPC 2.0 Specification
- XML-RPC Specification
- gRPC Documentation (grpc.io)
- Google Protocol Buffers Documentation

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
