"""OpenPack plugin entry point."""

import re
import shutil
import subprocess
import sys

VERSION = "0.1.0"

def register(registry):
    """Register commands with Command++.

    Expected registry interface:
    - register_command(name: str, handler: callable, help_text: str | None)
    """
    if registry is None:
        return

    def _split_args(args):
        if args is None:
            return []
        if isinstance(args, (list, tuple)):
            return [str(a) for a in args]
        return str(args).split()

    def _winget_available():
        if sys.platform != "win32":
            return False
        return shutil.which("winget") is not None

    def _run_winget(args):
        if not _winget_available():
            return "winget is not available on this system."
        cmd = ["winget"] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception as e:
            return f"Failed to run winget: {e}"

        output = (result.stdout or "") + (result.stderr or "")
        output = output.strip()
        if not output:
            output = "Done."
        return output

    def _run_winget_install(name_or_id):
        if not _winget_available():
            return "winget is not available on this system."
        cmd = [
            "winget",
            "install",
            "--exact",
            "--id",
            name_or_id,
            "--accept-source-agreements",
            "--accept-package-agreements",
        ]
        last_pct = None
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
        except Exception as e:
            return f"Failed to run winget: {e}"

        if proc.stdout:
            for line in proc.stdout:
                m = re.search(r"(\\d{1,3})%", line)
                if m:
                    last_pct = m.group(1)
                    msg = f"[{last_pct}%] Installing {name_or_id}..."
                    sys.stdout.write(msg + "\\n")
                    sys.stdout.flush()

        proc.wait()
        if last_pct is None:
            return f"Installing {name_or_id}..."
        return f"[{last_pct}%] Installing {name_or_id}..."

    def _opkg_cmd(_args=None):
        args = _split_args(_args)
        if not args:
            return (
                "opkg commands:\n"
                "  opkg search <name>\n"
                "  opkg install <id|name>\n"
                "  opkg update\n"
                "  opkg remove <id|name>\n"
                "  opkg version"
            )

        cmd = args[0].lower()
        tail = args[1:]

        if cmd == "version":
            return f"OpenPack version {VERSION}"

        if cmd == "search":
            if not tail:
                return "Usage: opkg search <name>"
            return _run_winget(["search"] + tail)

        if cmd == "install":
            if not tail:
                return "Usage: opkg install <id|name>"
            return _run_winget_install(" ".join(tail))

        if cmd == "update":
            return _run_winget(["source", "update"])

        if cmd == "remove":
            if not tail:
                return "Usage: opkg remove <id|name>"
            return _run_winget(["uninstall"] + tail)

        return "Unknown opkg command. Try: opkg"

    if hasattr(registry, "register_command"):
        registry.register_command("opkg", _opkg_cmd, "OpenPack app installer (winget)")
        registry.register_command("opkg.version", lambda _args=None: f"OpenPack version {VERSION}", "OpenPack plugin version")
