#!/usr/bin/env python3
"""
Teste Unitare - Săptămâna 12
============================
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Rulare: python -m pytest tests/test_unitare.py -v
"""

import pytest
from typing import Dict, Any, List


class TestSMTPProtocol:
    """Teste pentru validarea comenzilor și răspunsurilor SMTP."""
    
    @pytest.mark.parametrize("cod,clasa_asteptata", [
        (220, "succes"), (250, "succes"), (354, "intermediar"),
        (450, "eroare_temporara"), (550, "eroare_permanenta"),
    ])
    def test_clasificare_coduri_raspuns(self, cod: int, clasa_asteptata: str):
        prima_cifra = cod // 100
        if prima_cifra == 2:
            clasa_reala = "succes"
        elif prima_cifra == 3:
            clasa_reala = "intermediar"
        elif prima_cifra == 4:
            clasa_reala = "eroare_temporara"
        elif prima_cifra == 5:
            clasa_reala = "eroare_permanenta"
        else:
            clasa_reala = "necunoscut"
        assert clasa_reala == clasa_asteptata
    
    def test_ordinea_comenzilor_smtp(self):
        ordine_corecta = ["HELO", "MAIL FROM", "RCPT TO", "DATA", "QUIT"]
        assert ordine_corecta.index("MAIL FROM") < ordine_corecta.index("RCPT TO")
        assert ordine_corecta.index("RCPT TO") < ordine_corecta.index("DATA")


class TestJSONRPCProtocol:
    """Teste pentru validarea protocolului JSON-RPC 2.0."""
    
    def test_cerere_valida_cu_params_array(self):
        cerere = {"jsonrpc": "2.0", "method": "add", "params": [10, 20], "id": 1}
        assert cerere["jsonrpc"] == "2.0"
        assert isinstance(cerere["params"], list)
    
    def test_notificare_fara_id(self):
        cerere = {"jsonrpc": "2.0", "method": "log", "params": ["mesaj"]}
        assert "id" not in cerere
    
    def test_batch_valid(self):
        batch = [
            {"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1},
            {"jsonrpc": "2.0", "method": "multiply", "params": [3, 4], "id": 2},
        ]
        assert isinstance(batch, list)
        assert len(batch) > 0
    
    @pytest.mark.parametrize("cod,nume", [
        (-32700, "Parse error"), (-32601, "Method not found"),
        (-32602, "Invalid params"), (-32603, "Internal error"),
    ])
    def test_coduri_eroare_standard(self, cod: int, nume: str):
        assert cod < 0
        assert -32700 <= cod <= -32600


class TestProtobufSerialization:
    """Teste pentru compararea dimensiunilor de serializare."""
    
    def test_json_vs_protobuf_size(self):
        json_payload = '{"jsonrpc":"2.0","method":"add","params":[10,20],"id":1}'
        json_size = len(json_payload.encode('utf-8'))
        protobuf_size = 4
        assert protobuf_size < json_size
        assert json_size / protobuf_size > 10


class TestComparatieProtocolae:
    """Teste pentru compararea caracteristicilor protocoalelor."""
    
    def test_suport_batch(self):
        suport_batch = {"JSON-RPC": True, "XML-RPC": False, "gRPC": True}
        assert suport_batch["JSON-RPC"] is True
        assert suport_batch["XML-RPC"] is False
    
    def test_format_date(self):
        formate = {"JSON-RPC": "JSON", "XML-RPC": "XML", "gRPC": "Protocol Buffers"}
        assert formate["gRPC"] == "Protocol Buffers"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
