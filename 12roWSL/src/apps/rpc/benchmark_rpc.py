#!/usr/bin/env python3
"""
Benchmark RPC (Săptămâna 12) — JSON-RPC vs XML-RPC vs gRPC
==========================================================
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Utilizare: python benchmark_rpc.py --calls 1000
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import time
import urllib.parse
import http.client
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, List
import xmlrpc.client

# ═══════════════════════════════════════════════════════════════════════════════
# STRUCTURI_DATE
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class BenchResult:
    name: str
    calls: int
    seconds: float
    success: bool = True
    error_message: Optional[str] = None

    @property
    def calls_per_second(self) -> float:
        return self.calls / self.seconds if self.success and self.seconds > 0 else 0.0

    @property
    def avg_ms(self) -> float:
        return (self.seconds / self.calls) * 1000 if self.success and self.calls > 0 else 0.0

# ═══════════════════════════════════════════════════════════════════════════════
# BENCHMARK_JSONRPC
# ═══════════════════════════════════════════════════════════════════════════════
def bench_jsonrpc(url: str, calls: int, warmup: int = 10) -> BenchResult:
    try:
        parsed = urllib.parse.urlparse(url)
        conn = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=5)
        path = parsed.path or "/"
        
        for i in range(warmup):
            payload = json.dumps({"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": i})
            conn.request("POST", path, payload.encode(), {"Content-Type": "application/json"})
            conn.getresponse().read()
        
        start = time.perf_counter()
        for i in range(calls):
            payload = json.dumps({"jsonrpc": "2.0", "method": "add", "params": [10, 32], "id": i})
            conn.request("POST", path, payload.encode(), {"Content-Type": "application/json"})
            conn.getresponse().read()
        end = time.perf_counter()
        
        conn.close()
        return BenchResult(name="JSON-RPC", calls=calls, seconds=end - start)
    except Exception as e:
        return BenchResult(name="JSON-RPC", calls=0, seconds=0, success=False, error_message=str(e))

# ═══════════════════════════════════════════════════════════════════════════════
# BENCHMARK_XMLRPC
# ═══════════════════════════════════════════════════════════════════════════════
def bench_xmlrpc(url: str, calls: int, warmup: int = 10) -> BenchResult:
    try:
        proxy = xmlrpc.client.ServerProxy(url)
        for _ in range(warmup):
            proxy.add(1, 2)
        
        start = time.perf_counter()
        for _ in range(calls):
            proxy.add(10, 32)
        end = time.perf_counter()
        
        return BenchResult(name="XML-RPC", calls=calls, seconds=end - start)
    except Exception as e:
        return BenchResult(name="XML-RPC", calls=0, seconds=0, success=False, error_message=str(e))

# ═══════════════════════════════════════════════════════════════════════════════
# BENCHMARK_GRPC
# ═══════════════════════════════════════════════════════════════════════════════
def bench_grpc(host: str, port: int, calls: int, warmup: int = 10) -> BenchResult:
    try:
        import grpc
        grpc_path = Path(__file__).parent / "grpc"
        sys.path.insert(0, str(grpc_path))
        import calculator_pb2, calculator_pb2_grpc
        
        channel = grpc.insecure_channel(f"{host}:{port}")
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        
        for _ in range(warmup):
            stub.Add(calculator_pb2.CalcRequest(a=1, b=2))
        
        start = time.perf_counter()
        for _ in range(calls):
            stub.Add(calculator_pb2.CalcRequest(a=10, b=32))
        end = time.perf_counter()
        
        channel.close()
        return BenchResult(name="gRPC", calls=calls, seconds=end - start)
    except ImportError as e:
        return BenchResult(name="gRPC", calls=0, seconds=0, success=False, error_message=f"Import: {e}")
    except Exception as e:
        return BenchResult(name="gRPC", calls=0, seconds=0, success=False, error_message=str(e))

# ═══════════════════════════════════════════════════════════════════════════════
# AFISARE_REZULTATE
# ═══════════════════════════════════════════════════════════════════════════════
def afiseaza_rezultate(rezultate: List[BenchResult]) -> None:
    print("\n" + "=" * 60)
    print("REZULTATE BENCHMARK RPC")
    print("=" * 60 + "\n")
    
    for r in rezultate:
        if r.success:
            print(f"📊 {r.name}: {r.calls_per_second:.1f} cereri/s, {r.avg_ms:.3f} ms/cerere")
        else:
            print(f"❌ {r.name}: EROARE - {r.error_message}")
    
    valide = [r for r in rezultate if r.success]
    if len(valide) >= 2:
        fastest = min(valide, key=lambda x: x.seconds)
        print(f"\n🥇 Cel mai rapid: {fastest.name}")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    ap = argparse.ArgumentParser(description="Benchmark JSON-RPC vs XML-RPC vs gRPC")
    ap.add_argument("--jsonrpc-url", default="http://127.0.0.1:6200")
    ap.add_argument("--xmlrpc-url", default="http://127.0.0.1:6201")
    ap.add_argument("--grpc-host", default="127.0.0.1")
    ap.add_argument("--grpc-port", type=int, default=6251)
    ap.add_argument("--calls", type=int, default=1000)
    ap.add_argument("--skip-grpc", action="store_true")
    args = ap.parse_args()
    
    print(f"Rulare benchmark cu {args.calls} apeluri per protocol...")
    
    rezultate = [
        bench_jsonrpc(args.jsonrpc_url, args.calls),
        bench_xmlrpc(args.xmlrpc_url, args.calls),
    ]
    if not args.skip_grpc:
        rezultate.append(bench_grpc(args.grpc_host, args.grpc_port, args.calls))
    
    afiseaza_rezultate(rezultate)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
