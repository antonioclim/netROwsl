# Glosar de Termeni - Săptămâna 12

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

## Termeni SMTP și Email

| Termen | Definiție | Exemplu/Context |
|--------|-----------|-----------------|
| **SMTP** | Simple Mail Transfer Protocol - protocol pentru trimiterea email-urilor între servere | Port 25 (server-to-server), 587 (submission) |
| **MTA** | Mail Transfer Agent - server care primește și retransmite email | Postfix, Sendmail, Microsoft Exchange |
| **MUA** | Mail User Agent - aplicație client de email | Outlook, Thunderbird, Gmail web |
| **MDA** | Mail Delivery Agent - livrează email-ul în cutia poștală | Dovecot, procmail |
| **Envelope** | Adresele MAIL FROM/RCPT TO (pot diferi de headerele mesajului) | Expeditor real vs. afișat în "From:" |
| **HELO/EHLO** | Comenzi de identificare a clientului | EHLO activează extensiile SMTP |
| **MIME** | Multipurpose Internet Mail Extensions - standard pentru atașamente | Content-Type: multipart/mixed |
| **Relay** | Trimiterea email-ului către alt server pentru livrare | Open relay = risc de spam |
| **Bounce** | Mesaj de eroare returnat când livrarea eșuează | 550 User unknown |
| **Spool** | Director unde email-urile așteaptă procesarea | /var/spool/mail |

## Coduri de Răspuns SMTP

| Cod | Categorie | Semnificație | Exemplu |
|-----|-----------|--------------|---------|
| **220** | 2xx - Succes | Serviciu pregătit | 220 mail.example.com SMTP ready |
| **250** | 2xx - Succes | Comandă acceptată | 250 OK |
| **354** | 3xx - Continuare | Trimite datele | 354 Start mail input |
| **421** | 4xx - Eroare temporară | Serviciu indisponibil | Încearcă mai târziu |
| **450** | 4xx - Eroare temporară | Cutie poștală ocupată | Încearcă mai târziu |
| **550** | 5xx - Eroare permanentă | Cutie inexistentă | Nu reîncerca |
| **553** | 5xx - Eroare permanentă | Sintaxă invalidă | Verifică adresa |

## Termeni RPC

| Termen | Definiție | Exemplu/Context |
|--------|-----------|-----------------|
| **RPC** | Remote Procedure Call - apel de funcție pe alt calculator | proxy.add(10, 20) executat remote |
| **Stub** | Cod generat care face serializarea și comunicația | Client stub, server stub |
| **Marshalling** | Serializarea parametrilor pentru transmisie | Object → Bytes |
| **Unmarshalling** | Deserializarea răspunsului | Bytes → Object |
| **Proxy** | Obiect local care reprezintă serviciul remote | ServerProxy("http://...") |
| **Endpoint** | Adresa serviciului (URL + port) | http://localhost:6200 |
| **Introspection** | Capacitatea de a descoperi metodele disponibile | system.listMethods() |
| **Batch** | Trimiterea mai multor cereri într-un singur mesaj | [{...}, {...}, {...}] |
| **Notification** | Cerere fără răspuns așteptat | JSON-RPC fără câmpul "id" |
| **IDL** | Interface Definition Language | .proto pentru gRPC |

## Termeni JSON-RPC

| Termen | Definiție | Exemplu |
|--------|-----------|---------|
| **jsonrpc** | Câmp obligatoriu cu versiunea | "jsonrpc": "2.0" |
| **method** | Numele metodei de apelat | "method": "add" |
| **params** | Parametrii (array sau obiect) | "params": [10, 20] sau {"a": 10} |
| **id** | Identificator pentru corelarea răspunsului | "id": 1 |
| **result** | Rezultatul în caz de succes | "result": 30 |
| **error** | Obiect de eroare în caz de eșec | "error": {"code": -32601} |

### Coduri de Eroare JSON-RPC Standard

| Cod | Mesaj | Când apare |
|-----|-------|------------|
| -32700 | Parse error | JSON invalid |
| -32600 | Invalid Request | Cerere malformată |
| -32601 | Method not found | Metoda nu există |
| -32602 | Invalid params | Parametri greșiți |
| -32603 | Internal error | Eroare server |
| -32000 to -32099 | Server error | Erori specifice aplicației |

## Termeni gRPC și Protocol Buffers

| Termen | Definiție | Exemplu |
|--------|-----------|---------|
| **gRPC** | Google Remote Procedure Call - framework RPC modern | HTTP/2 + Protobuf |
| **Protobuf** | Protocol Buffers - format de serializare binară | Mai compact decât JSON |
| **.proto** | Fișier cu definiția schemei | message Person { string name = 1; } |
| **Service** | Colecție de metode RPC | service Calculator { rpc Add(...) } |
| **Message** | Structură de date în Protobuf | Similar cu struct/class |
| **Field number** | Identificator numeric pentru câmp | string name = 1; (1 e field number) |
| **Varint** | Codificare variabilă pentru întregi | Numere mici = mai puțini bytes |
| **Channel** | Conexiunea către server | grpc.insecure_channel(...) |
| **Stub** | Client generat din .proto | CalculatorStub(channel) |
| **Streaming** | Flux continuu de mesaje | Unary, server-stream, client-stream, bidi |

### Tipuri de Streaming gRPC

| Tip | Client | Server | Exemplu |
|-----|--------|--------|---------|
| **Unary** | 1 mesaj | 1 mesaj | Add(a, b) → result |
| **Server streaming** | 1 mesaj | N mesaje | GetLogs(filter) → stream of logs |
| **Client streaming** | N mesaje | 1 mesaj | UploadChunks(chunks) → status |
| **Bidirectional** | N mesaje | N mesaje | Chat în timp real |

## Acronime

| Acronim | Expansiune |
|---------|------------|
| SMTP | Simple Mail Transfer Protocol |
| POP3 | Post Office Protocol version 3 |
| IMAP | Internet Message Access Protocol |
| MIME | Multipurpose Internet Mail Extensions |
| RPC | Remote Procedure Call |
| JSON | JavaScript Object Notation |
| XML | eXtensible Markup Language |
| gRPC | Google Remote Procedure Call |
| HTTP | HyperText Transfer Protocol |
| TCP | Transmission Control Protocol |
| TLS | Transport Layer Security |
| IDL | Interface Definition Language |
| API | Application Programming Interface |

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
