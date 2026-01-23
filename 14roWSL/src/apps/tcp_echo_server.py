#!/usr/bin/env python3
"""tcp_echo_server.py — Simple TCP echo server for demonstrations.

This server implements the Echo Protocol (RFC 862) over TCP.
It accepts connections and returns any data received unchanged.

Features:
  - Multi-threaded: handles multiple clients concurrently
  - Graceful shutdown on SIGINT (Ctrl+C)
  - Detailed logging with timestamps

Usage:
  python3 tcp_echo_server.py --host 0.0.0.0 --port 9090

Testing:
  echo "Hello" | nc localhost 9090
  # Expected: Hello

Architecture:
  Main Thread: accept() loop
       │
       ├──► Client Thread 1: recv/send loop
       ├──► Client Thread 2: recv/send loop
       └──► ...
"""

from __future__ import annotations

import argparse
import socket
import threading
from datetime import datetime
from typing import Tuple


def log(msg: str, level: str = "INFO") -> None:
    """
    Log message with timestamp and level.
    
    Args:
        msg: Message to log
        level: Log level (INFO, ERROR, DEBUG)
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{ts}] [echo-server] [{level}] {msg}")


def handle_client(client_socket: socket.socket, client_addr: Tuple[str, int]) -> None:
    """
    Process a single client connection in a dedicated thread.
    
    Implements the echo loop: receive data, send it back unchanged.
    Continues until client disconnects or error occurs.
    
    Args:
        client_socket: Connected socket to client
        client_addr: Tuple of (ip_address, port)
    """
    addr_str = f"{client_addr[0]}:{client_addr[1]}"
    log(f"Connection established: {addr_str}")
    
    bytes_received = 0
    bytes_sent = 0
    
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                # Client closed connection gracefully
                break
            
            bytes_received += len(data)
            log(f"← Received from {addr_str}: {len(data)} bytes", "DEBUG")
            
            client_socket.sendall(data)
            bytes_sent += len(data)
            log(f"→ Echoed to {addr_str}: {len(data)} bytes", "DEBUG")
            
    except (ConnectionResetError, BrokenPipeError) as e:
        log(f"Connection reset by {addr_str}: {e}", "ERROR")
    except Exception as e:
        log(f"Unexpected error with {addr_str}: {e}", "ERROR")
    finally:
        client_socket.close()
        log(f"Connection closed: {addr_str} (rx={bytes_received}, tx={bytes_sent})")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="TCP Echo Server (RFC 862)",
        epilog="NETWORKING class - ASE, Informatics | by Revolvix"
    )
    parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Bind address (default: 0.0.0.0 = all interfaces)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=9090, 
        help="Listening port (default: 9090)"
    )
    parser.add_argument(
        "--backlog",
        type=int,
        default=5,
        help="Listen queue size (default: 5)"
    )
    return parser.parse_args()


def main() -> int:
    """
    Main entry point.
    
    Creates server socket, binds, and enters accept loop.
    Each client is handled in a separate daemon thread.
    
    Returns:
        0 on clean shutdown, 1 on error
    """
    args = parse_args()
    
    # Create and configure server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((args.host, args.port))
    except OSError as e:
        log(f"Cannot bind to {args.host}:{args.port}: {e}", "ERROR")
        return 1
    
    server_socket.listen(args.backlog)
    
    log(f"TCP Echo Server listening on {args.host}:{args.port}")
    log(f"Test with: echo 'Hello' | nc localhost {args.port}")
    
    try:
        while True:
            client_socket, client_addr = server_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_addr),
                daemon=True,
                name=f"client-{client_addr[0]}:{client_addr[1]}"
            )
            thread.start()
    except KeyboardInterrupt:
        log("Shutdown requested (Ctrl+C)")
    finally:
        server_socket.close()
        log("Server stopped")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
