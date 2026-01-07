#!/usr/bin/env python3
"""
Exercițiul 2-4: Apeluri RPC (JSON-RPC, XML-RPC, gRPC)
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

EXERCIȚIUL 2: JSON-RPC 2.0
==========================

1. Testați un apel simplu folosind curl:

   curl -X POST http://localhost:6200 \\
     -H "Content-Type: application/json" \\
     -d '{"jsonrpc":"2.0","method":"add","params":[10,20],"id":1}'

2. Testați apeluri cu parametri numiți:

   curl -X POST http://localhost:6200 \\
     -H "Content-Type: application/json" \\
     -d '{"jsonrpc":"2.0","method":"subtract","params":{"a":100,"b":42},"id":2}'

3. Executați un apel în lot (batch):

   curl -X POST http://localhost:6200 \\
     -H "Content-Type: application/json" \\
     -d '[
       {"jsonrpc":"2.0","method":"add","params":[1,2],"id":1},
       {"jsonrpc":"2.0","method":"multiply","params":[3,4],"id":2}
     ]'

EXERCIȚIUL 3: XML-RPC
=====================

1. Listați metodele disponibile (introspecție):

   curl -X POST http://localhost:6201 \\
     -H "Content-Type: text/xml" \\
     -d '<?xml version="1.0"?>
     <methodCall>
       <methodName>system.listMethods</methodName>
     </methodCall>'

2. Efectuați un apel de calcul:

   curl -X POST http://localhost:6201 \\
     -H "Content-Type: text/xml" \\
     -d '<?xml version="1.0"?>
     <methodCall>
       <methodName>multiply</methodName>
       <params>
         <param><value><int>7</int></value></param>
         <param><value><int>8</int></value></param>
       </params>
     </methodCall>'

EXERCIȚIUL 4: gRPC
==================

1. Rulați clientul gRPC:

   python src/apps/rpc/grpc/grpc_client.py

2. Observați diferența de dimensiune a payload-ului în Wireshark:

   tcp.port == 6251

COMPARAȚIE PROTOCOALE:
======================

Observați diferențele între:
- Dimensiunea cererii/răspunsului
- Lizibilitatea datelor
- Timpii de răspuns

VERIFICARE:
===========

python tests/test_exercitii.py --exercitiu 2
python tests/test_exercitii.py --exercitiu 3
python tests/test_exercitii.py --exercitiu 4
"""

print(__doc__)
