# Rezultate Așteptate pentru Exerciții

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest document prezintă rezultatele așteptate pentru fiecare exercițiu de laborator.

---

## Exercițiul 1: Explorare Serviciu HTTP

### Cerere și Răspuns HTTP

```bash
$ curl -v http://localhost:8000/
*   Trying 127.0.0.1:8000...
* Connected to localhost (127.0.0.1) port 8000
> GET / HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/8.0.1
> Accept: */*
>
< HTTP/1.0 200 OK
< Server: SimpleHTTP/0.6 Python/3.11.7
< Content-type: text/html; charset=utf-8
< Content-Length: 4523
```

### Cerere HEAD

```bash
$ curl -I http://localhost:8000/hello.txt
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.7
Content-type: text/plain
Content-Length: 173
```

---

## Exercițiul 2: Rezoluție DNS

### Interogare DNS Reușită

```bash
$ dig @localhost -p 5353 web.lab.local

;; QUESTION SECTION:
;web.lab.local.                 IN      A

;; ANSWER SECTION:
web.lab.local.          300     IN      A       172.20.0.10
```

### Interogare NXDOMAIN

```bash
$ dig @localhost -p 5353 inexistent.lab.local

;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 12345

;; QUESTION SECTION:
;inexistent.lab.local.          IN      A
```

---

## Exercițiul 3: Comunicație SSH

### Conectare SSH Reușită

```bash
$ ssh -p 2222 labuser@localhost
The authenticity of host '[localhost]:2222 ([127.0.0.1]:2222)' can't be established.
ED25519 key fingerprint is SHA256:xxxxx...
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
labuser@localhost's password: labpass

labuser@ssh-server:~$ whoami
labuser
labuser@ssh-server:~$ hostname
ssh-server
```

### Ieșire Paramiko

```
========================================
  CLIENT SSH PARAMIKO - DEMONSTRAȚIE
========================================

  Conectare la labuser@ssh-server:22...
  ✓ Conectat cu succes!

  Informații conexiune:
    Cipher: aes256-ctr
    MAC: hmac-sha2-256

  $ whoami
    labuser
  $ hostname
    ssh-server

  ✓ Demonstrație finalizată cu succes!
```

---

## Exercițiul 4: Protocol FTP

### Conectare FTP

```bash
$ ftp localhost 2121
Connected to localhost.
220 Bine ați venit pe serverul FTP de laborator! (by Revolvix)
Name (localhost:user): labftp
331 Username ok, send password.
Password: labftp
230 Login successful.

ftp> pwd
257 "/" is the current directory.

ftp> ls
227 Entering passive mode (172,20,0,21,117,48).
150 File status okay. About to open data connection.
drwxr-xr-x    2 1000     1000          4096 Jan 07 12:00 download
drwxr-xr-x    2 1000     1000          4096 Jan 07 12:00 upload
-rw-r--r--    1 1000     1000            36 Jan 07 12:00 bun_venit.txt
226 Transfer complete.
```

---

## Exercițiul 5: HTTPS cu TLS

### Răspuns HTTPS

```bash
$ curl -k https://localhost:4443/
{
  "mesaj": "Bine ați venit la serverul HTTPS!",
  "versiune": "1.0",
  "endpoints": [
    "GET /api/resurse - Listează toate resursele",
    ...
  ]
}
```

### Operații CRUD

```bash
# CREATE
$ curl -k -X POST -H "Content-Type: application/json" \
  -d '{"nume": "Test", "valoare": 42}' \
  https://localhost:4443/api/resurse

{
  "mesaj": "Resursă creată cu succes",
  "resursa": {
    "id": 1,
    "nume": "Test",
    "valoare": 42,
    "creat_la": "2024-01-07 12:00:00"
  }
}

# READ
$ curl -k https://localhost:4443/api/resurse
{
  "total": 1,
  "resurse": [...]
}

# DELETE
$ curl -k -X DELETE https://localhost:4443/api/resurse/1
{
  "mesaj": "Resursă ștearsă"
}
```

---

## Exercițiul 6: Niveluri REST

### Nivelul 0 (RPC)

```bash
$ curl -X POST -H "Content-Type: application/json" \
  -d '{"actiune": "listeaza"}' \
  http://localhost:5000/api/nivel0

{
  "succes": true,
  "rezultat": []
}
```

### Nivelul 2 (Verbe HTTP)

```bash
$ curl http://localhost:5000/api/nivel2/produse
{
  "produse": []
}

$ curl -X POST -H "Content-Type: application/json" \
  -d '{"nume": "Laptop"}' \
  http://localhost:5000/api/nivel2/produse

{
  "produs": {
    "id": 1,
    "nume": "Laptop",
    "creat_la": "2024-01-07 12:00:00"
  }
}
```

### Nivelul 3 (HATEOAS)

```bash
$ curl http://localhost:5000/api/nivel3/produse
{
  "produse": [
    {
      "id": 1,
      "nume": "Laptop",
      "_linkuri": {
        "self": "/api/nivel3/produse/1",
        "actualizeaza": {
          "href": "/api/nivel3/produse/1",
          "metoda": "PUT"
        },
        "sterge": {
          "href": "/api/nivel3/produse/1",
          "metoda": "DELETE"
        },
        "colectie": "/api/nivel3/produse"
      }
    }
  ],
  "_linkuri": {
    "self": "/api/nivel3/produse",
    "creeaza": {
      "href": "/api/nivel3/produse",
      "metoda": "POST",
      "corpNecesar": {"nume": "string", "pret": "number"}
    }
  }
}
```

---

## Verificări Automate

### Test Rapid (Smoke Test)

```
====================================
  TEST RAPID (SMOKE TEST)
====================================

  [1/5] Verificare Docker... ✓
  [2/5] Verificare HTTP (port 8000)... ✓
  [3/5] Verificare DNS (port 5353)... ✓
  [4/5] Verificare SSH (port 2222)... ✓
  [5/5] Verificare FTP (port 2121)... ✓

──────────────────────────────────────
  ✓ Toate verificările trecute (2.3s)
  Mediul de laborator este pregătit!
```

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
