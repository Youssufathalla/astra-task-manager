"""Program entry point.

Run this file to start the Astra task manager.
"""

try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

from app import run_app


if __name__ == "__main__":
    run_app()
