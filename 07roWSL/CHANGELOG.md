# Changelog

All notable changes to the Week 7 WSL Starter Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-22

### Added
- Peer Instruction questions (4 MCQ cu distractori bazați pe misconceptii)
- Prediction prompts în toate cele 5 exerciții de laborator
- Analogii CPA (Concret-Pictorial-Abstract) pentru toate conceptele cheie
- Glosar de termeni (`docs/glosar.md`)
- Modul constante centralizat (`src/constants.py`)
- Rubrici detaliate de evaluare pentru teme
- Subgoal labels în scripturile de management

### Changed
- Îmbunătățire documentație cu analogii intuitive
- Restructurare scripturi cu etichete clare pentru pași

### Fixed
- Eliminare vocabular AI-sounding din documentație

## [1.0.0] - 2026-01-07

### Added
- Initial release of WEEK7_WSLkit
- Complete Docker Compose environment for TCP/UDP traffic experiments
- Python-based laboratory management scripts (start_lab.py, stop_lab.py, cleanup.py)
- Packet filter proxy implementation for application-layer filtering
- Defensive port probe utility
- Firewall profile management with JSON-based configuration
- Five structured laboratory exercises with verification tests
- Documentație completă: rezumat teoretic și referință comenzi rapide
- Homework assignments with solution stubs
- Automated demonstration scripts for instructor use
- Wireshark and tcpdump integration for traffic capture
- Portainer CE support for container management

### Infrastructure
- WSL2-optimised Docker configuration
- Bridge network with configurable addressing
- Volume mounts for artifact persistence
- Graceful shutdown and cleanup procedures

### Documentation
- README.md with complete quick-start guide
- Theory summary covering packet capture evidence and filtering semantics
- Troubleshooting guide for common WSL2/Docker issues
- Commands cheatsheet for tcpdump, tshark and iptables

---

*NETWORKING class - ASE, Informatics | by Revolvix*
