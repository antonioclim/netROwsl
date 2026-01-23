#!/usr/bin/env python3
"""
Server JSON-RPC 2.0 - Săptămâna 12
==================================
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI
# ═══════════════════════════════════════════════════════════════════════════════
import argparse, datetime, hashlib, json, logging, sys, threading
from collections import defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_PROTOCOL
# ═══════════════════════════════════════════════════════════════════════════════
JSONRPC_VERSION = "2.0"
ERROR_PARSE, ERROR_INVALID_REQUEST = -32700, -32600
ERROR_METHOD_NOT_FOUND, ERROR_INVALID_PARAMS, ERROR_INTERNAL = -32601, -32602, -32603

_stats_lock = threading.Lock()
_call_counts: Dict[str, int] = defaultdict(int)
_start_time = datetime.datetime.now()

def _count(method: str) -> None:
    with _stats_lock:
        _call_counts[method] += 1

# ═══════════════════════════════════════════════════════════════════════════════
# PARSARE_PARAMETRI
# ═══════════════════════════════════════════════════════════════════════════════
def _need2(pos: List[Any], named: Dict[str, Any]) -> tuple:
    if pos and len(pos) >= 2:
        return pos[0], pos[1]
    if "a" in named and "b" in named:
        return named["a"], named["b"]
    raise ValueError("Necesari doi parametri: a și b")

# ═══════════════════════════════════════════════════════════════════════════════
# DISPATCH_METODE
# ═══════════════════════════════════════════════════════════════════════════════
def _dispatch(method: str, pos: List[Any], named: Dict[str, Any]) -> Any:
    method = method.strip()
    if method == "add":
        _count("add"); a, b = _need2(pos, named); return a + b
    if method == "subtract":
        _count("subtract"); a, b = _need2(pos, named); return a - b
    if method == "multiply":
        _count("multiply"); a, b = _need2(pos, named); return a * b
    if method == "divide":
        _count("divide"); a, b = _need2(pos, named)
        if b == 0: raise ZeroDivisionError("Împărțire la zero")
        return a / b
    if method == "echo":
        _count("echo"); return str(pos[0]) if pos else str(named.get("message", ""))
    if method == "get_time":
        _count("get_time"); return datetime.datetime.now().isoformat()
    if method == "sha256":
        _count("sha256"); s = str(pos[0]) if pos else str(named.get("data", ""))
        return hashlib.sha256(s.encode()).hexdigest()
    if method == "get_stats":
        _count("get_stats")
        with _stats_lock:
            return {"uptime": (datetime.datetime.now() - _start_time).total_seconds(),
                    "calls": dict(_call_counts)}
    raise KeyError(f"Metodă necunoscută: {method}")

# ═══════════════════════════════════════════════════════════════════════════════
# PROCESARE_CERERE
# ═══════════════════════════════════════════════════════════════════════════════
def _make_error(code: int, message: str, req_id: Any = None) -> Dict:
    return {"jsonrpc": JSONRPC_VERSION, "error": {"code": code, "message": message}, "id": req_id}

def _make_result(result: Any, req_id: Any) -> Dict:
    return {"jsonrpc": JSONRPC_VERSION, "result": result, "id": req_id}

def _process_single(obj: Dict) -> Optional[Dict]:
    if not isinstance(obj, dict):
        return _make_error(ERROR_INVALID_REQUEST, "Cerere invalidă")
    req_id = obj.get("id")
    if obj.get("jsonrpc") != JSONRPC_VERSION:
        return _make_error(ERROR_INVALID_REQUEST, "jsonrpc trebuie să fie '2.0'", req_id)
    method = obj.get("method")
    if not method or not isinstance(method, str):
        return _make_error(ERROR_INVALID_REQUEST, "method invalid", req_id)
    
    params = obj.get("params", [])
    pos, named = (params, {}) if isinstance(params, list) else ([], params if isinstance(params, dict) else [])
    
    try:
        result = _dispatch(method, pos, named)
        return None if req_id is None else _make_result(result, req_id)
    except KeyError as e:
        return _make_error(ERROR_METHOD_NOT_FOUND, str(e), req_id)
    except (ValueError, TypeError, ZeroDivisionError) as e:
        return _make_error(ERROR_INVALID_PARAMS, str(e), req_id)
    except Exception as e:
        return _make_error(ERROR_INTERNAL, str(e), req_id)

def process_request(raw_body: bytes) -> bytes:
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return json.dumps(_make_error(ERROR_PARSE, f"Parse error: {e}")).encode()
    
    if isinstance(payload, list):
        responses = [r for r in (_process_single(item) for item in payload) if r]
        return json.dumps(responses).encode() if responses else b""
    else:
        resp = _process_single(payload)
        return json.dumps(resp).encode() if resp else b""

# ═══════════════════════════════════════════════════════════════════════════════
# HANDLER_HTTP
# ═══════════════════════════════════════════════════════════════════════════════
class JSONRPCHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        logger.debug(f"{self.address_string()} - {format % args}")
    
    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length else b""
        response_body = process_request(raw_body)
        
        self.send_response(200 if response_body else 204)
        if response_body:
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if response_body:
            self.wfile.write(response_body)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    ap = argparse.ArgumentParser(description="Server JSON-RPC 2.0")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=6200)
    args = ap.parse_args()
    
    httpd = HTTPServer((args.host, args.port), JSONRPCHandler)
    logger.info(f"Server JSON-RPC pe http://{args.host}:{args.port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Oprire...")
    finally:
        httpd.server_close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
