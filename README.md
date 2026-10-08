# Linux Security Audit Tool

A Python-based Linux security auditing tool designed to collect and assess key security information from a Linux system.

## Overview

This project uses Python and Linux system commands to perform a basic security audit of a Linux machine.

The tool checks system configuration, security settings, user privileges, system updates, disk usage, network services and failed login attempts.

It then produces a security score and overall security status.

## Features

- Displays the current Linux user
- Detects the operating system
- Detects the Linux kernel version
- Checks firewall status
- Checks whether SSH is installed
- Lists system users
- Checks available system updates
- Checks disk usage
- Detects listening network sockets
- Counts failed login attempts
- Identifies users with sudo privileges
- Calculates a security score
- Generates an audit report

## Technologies Used

- Python 3
- Linux / Ubuntu
- Bash
- Python subprocess module
- Linux system commands
- Git / GitHub

## Security Checks

The tool currently assesses several areas of system security:

| Check | Purpose |
|---|---|
| Firewall | Determines whether the firewall is enabled |
| SSH | Checks whether an SSH server is installed |
| Updates | Detects available system updates |
| Disk Usage | Checks available storage capacity |
| Failed Logins | Detects failed authentication attempts |
| Sudo Users | Identifies users with administrative privileges |
| Network Services | Detects listening network sockets |

## Security Score

The tool calculates a security score based on successful checks.

Each successful check contributes to the overall score.

The tool also categorises the system as:

- `GOOD`
- `MODERATE`
- `NEEDS ATTENTION`

## Example

Example output:

```text
LINUX SECURITY AUDIT

Current User: lennox
Operating System: Ubuntu
Kernel: Linux

[WARN] Firewall is disabled
[INFO] SSH server is not installed

System Updates:
[WARN] System updates are available

Disk Usage:
[PASS] Disk usage is within limits

Failed Login Attempts:
[WARN] Failed login attempts detected

Administrative Users:
[INFO] Users with sudo privileges detected

Security Score: 40/100
Security Status: NEEDS ATTENTION
