# OpenPack (opkg)

OpenPack (opkg) is a Command++ plugin for installing apps. Think of it like `choco` or `scoop`, but cleaner and focused on a simple, readable workflow.

Goals:
- Clean commands that are easy to remember.
- Minimal noise, clear output, and deterministic installs.
- Simple metadata format so packages stay understandable.

Planned commands:
- `opkg search <name>`: find apps.
- `opkg install <name>`: install apps.
- `opkg update`: refresh indexes.
- `opkg remove <name>`: uninstall apps.

Status:
- Early scaffold. Behavior will evolve as Command++ grows.

Files:
- opkg.cmdpp: plugin definition
- opkg/main.py: entry point
