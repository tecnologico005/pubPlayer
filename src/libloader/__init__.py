import ctypes
import os
import platform


def _get_arch():
	machine = platform.machine().lower()
	if platform.system() == "Linux" and machine in ("aarch64", "arm64"):
		return "arm64"
	if platform.architecture()[0] == "64bit":
		return "x64"
	return "x86"


def _choose_directory(x86_path=None, x64_path=None, arm64_path=None):
	arch = _get_arch()
	if arch == "arm64" and arm64_path:
		return arm64_path
	if arch == "x64" and x64_path:
		return x64_path
	return x86_path or x64_path or ""


def _extension():
	system = platform.system()
	if system == "Windows":
		return ".dll"
	if system == "Darwin":
		return ".dylib"
	return ".so"


def find_library_path(name, x86_path=None, x64_path=None, arm64_path=None):
	directory = _choose_directory(x86_path, x64_path, arm64_path)
	ext = _extension()
	for file_name in (name + ext, "lib" + name + ext):
		path = os.path.join(directory, file_name)
		if os.path.isfile(path):
			return path
	return name


def load_library(name, x86_path=None, x64_path=None, arm64_path=None, mode=0):
	lib_path = find_library_path(name, x86_path=x86_path, x64_path=x64_path, arm64_path=arm64_path)

	if platform.system() == "Windows":
		lib_dir = os.path.dirname(lib_path)
		if lib_dir and os.path.isdir(lib_dir):
			if hasattr(os, "add_dll_directory"):
				try:
					os.add_dll_directory(lib_dir)
				except OSError:
					pass
			os.environ["PATH"] = lib_dir + os.pathsep + os.environ.get("PATH", "")
		return ctypes.WinDLL(lib_path)
	return ctypes.CDLL(lib_path, mode=mode)


def get_functype():
	if platform.system() == "Windows":
		return ctypes.WINFUNCTYPE
	return ctypes.CFUNCTYPE
