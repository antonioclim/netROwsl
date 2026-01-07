#!/usr/bin/env python3
"""
Exercițiul 1: Dialog SMTP Manual
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

INSTRUCȚIUNI:
=============

1. Deschideți un terminal și conectați-vă la serverul SMTP:
   
   nc localhost 1025
   
   Sau pe Windows:
   
   telnet localhost 1025

2. Observați banner-ul de salut al serverului (răspuns 220)

3. Trimiteți comanda HELO pentru a vă identifica:
   
   HELO client.local
   
   Așteptați răspunsul 250

4. Inițiați o tranzacție de email:
   
   MAIL FROM:<expeditor@exemplu.ro>
   RCPT TO:<destinatar@exemplu.ro>
   DATA

5. Introduceți conținutul mesajului:
   
   Subject: Test SMTP din Laborator
   From: expeditor@exemplu.ro
   To: destinatar@exemplu.ro
   
   Acesta este corpul mesajului de test.
   .

   (Terminați cu o linie conținând doar un punct)

6. Verificați mesajele stocate:
   
   LIST

7. Încheiați sesiunea:
   
   QUIT

CAPTURĂ DE TRAFIC:
==================

Înainte de a începe dialogul, porniți captura în alt terminal:

python scripts/captura_trafic.py --port 1025 --output pcap/smtp_dialog.pcap --durata 120

FILTRE WIRESHARK:
=================

tcp.port == 1025
smtp
smtp.req.command == "MAIL"

VERIFICARE:
===========

python tests/test_exercitii.py --exercitiu 1
"""

print(__doc__)
