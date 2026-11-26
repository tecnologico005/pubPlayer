import os
import platform
import sys

# Directory that holds the bundled BASS libraries (sound_lib/lib).
if getattr(sys, "frozen", False):
    # Frozen apps (PyInstaller) unpack bundled data next to the executable.
    _data_root = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    _lib_root = os.path.join(_data_root, "sound_lib", "lib")
else:
    _lib_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib")

# 32-bit ARM Linux (ARMv6/ARMv7). libloader looks in x86_path for 32-bit
# Python interpreters, so on these systems that slot points at armhf.
_is_armhf = platform.system() == "Linux" and platform.machine().lower() in (
    "armv6l",
    "armv7l",
    "armv8l",
)

x64_path = os.path.join(_lib_root, "x64")
x86_path = os.path.join(_lib_root, "armhf") if _is_armhf else x64_path
# 64-bit ARM Linux (aarch64). None elsewhere, so Windows and macOS keep using x64_path.
arm64_path = os.path.join(_lib_root, "arm64") if platform.system() == "Linux" else None
