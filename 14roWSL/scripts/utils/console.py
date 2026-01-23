#!/usr/bin/env python3
"""
Console output utilities with ANSI colors.

NETWORKING class - ASE, Informatics | by Revolvix

This module provides consistent terminal output formatting across all scripts.
"""

from typing import Optional
import sys


class Colors:
    """ANSI color codes for terminal output."""
    
    # Standard colors
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    
    # Formatting
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Reset
    END = '\033[0m'
    
    @classmethod
    def strip(cls, text: str) -> str:
        """Remove all ANSI codes from text."""
        import re
        return re.sub(r'\033\[[0-9;]*m', '', text)
    
    @classmethod
    def supports_color(cls) -> bool:
        """Check if terminal supports color."""
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


# Convenience aliases
C = Colors


def info(msg: str, prefix: str = "INFO") -> None:
    """Print info message in cyan."""
    print(f"{C.CYAN}[{prefix}]{C.END} {msg}")


def success(msg: str, prefix: str = "OK") -> None:
    """Print success message in green."""
    print(f"{C.GREEN}[{prefix}]{C.END} {msg}")


def warning(msg: str, prefix: str = "ATENȚIE") -> None:
    """Print warning message in yellow."""
    print(f"{C.YELLOW}[{prefix}]{C.END} {msg}")


def error(msg: str, prefix: str = "EROARE") -> None:
    """Print error message in red."""
    print(f"{C.RED}[{prefix}]{C.END} {msg}")


def header(title: str, width: int = 60) -> None:
    """Print a formatted header."""
    print()
    print(f"{C.BOLD}{'=' * width}{C.END}")
    print(f"{C.BOLD}{title}{C.END}")
    print(f"{C.BOLD}{'=' * width}{C.END}")


def subheader(title: str, width: int = 50) -> None:
    """Print a formatted subheader."""
    print()
    print(f"{C.BOLD}{title}{C.END}")
    print("-" * width)


def status_line(name: str, status: bool, details: Optional[str] = None) -> None:
    """Print a status line with checkmark or X."""
    symbol = f"{C.GREEN}✓{C.END}" if status else f"{C.RED}✗{C.END}"
    detail_str = f" - {details}" if details else ""
    print(f"  {symbol} {name}{detail_str}")


def progress(current: int, total: int, prefix: str = "", width: int = 30) -> None:
    """Print a progress bar."""
    filled = int(width * current / total)
    bar = '█' * filled + '░' * (width - filled)
    percent = 100 * current / total
    print(f"\r{prefix}[{bar}] {percent:.1f}%", end='', flush=True)
    if current >= total:
        print()


# Romanian aliases for compatibility
def afiseaza_info(msg: str) -> None:
    """Alias for info() - Romanian."""
    info(msg)


def afiseaza_succes(msg: str) -> None:
    """Alias for success() - Romanian."""
    success(msg)


def afiseaza_avertisment(msg: str) -> None:
    """Alias for warning() - Romanian."""
    warning(msg)


def afiseaza_eroare(msg: str) -> None:
    """Alias for error() - Romanian."""
    error(msg)


if __name__ == "__main__":
    # Demo
    header("Console Utilities Demo")
    info("This is an info message")
    success("Operation completed successfully")
    warning("This might need attention")
    error("Something went wrong")
    
    subheader("Status Examples")
    status_line("Docker running", True)
    status_line("Portainer accessible", True, "http://localhost:9000")
    status_line("Backend unhealthy", False, "Connection refused")
    
    print("\nProgress bar demo:")
    import time
    for i in range(101):
        progress(i, 100, "Loading: ")
        time.sleep(0.02)
