#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() {
  printf '[project-memory-bridge] %s\n' "$1"
}

fail() {
  printf '[project-memory-bridge] ERROR: %s\n' "$1" >&2
  exit 1
}

version_ge() {
  local a="$1" b="$2"
  [[ "$(printf '%s\n%s\n' "$a" "$b" | sort -V | head -n1)" == "$b" ]]
}

detect_python() {
  if command -v python3 >/dev/null 2>&1; then
    local version
    version="$(python3 - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
PY
)"
    if version_ge "$version" "3.10.0"; then
      printf '%s\n' "python3"
      return 0
    fi
  fi

  if command -v python >/dev/null 2>&1; then
    local version
    version="$(python - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
PY
)"
    if version_ge "$version" "3.10.0"; then
      printf '%s\n' "python"
      return 0
    fi
  fi

  return 1
}

install_python_macos() {
  command -v brew >/dev/null 2>&1 || fail "Python 3.10+ no está instalado y Homebrew no existe. Instalá Homebrew o Python manualmente."
  log "Python 3.10+ no encontrado. Instalando con Homebrew..."
  brew install python
}

detect_platform() {
  case "$(uname -s)" in
    Darwin) printf '%s\n' "macos" ;;
    Linux) printf '%s\n' "linux" ;;
    *) printf '%s\n' "unknown" ;;
  esac
}

PYTHON_BIN="$(detect_python || true)"

if [[ -z "$PYTHON_BIN" ]]; then
  case "$(detect_platform)" in
    macos)
      install_python_macos
      PYTHON_BIN="$(detect_python || true)"
      ;;
    linux)
      fail "Python 3.10+ no está instalado. En Linux prefiero no adivinar tu package manager. Instalalo y reintentá."
      ;;
    *)
      fail "No se pudo detectar una instalación compatible de Python 3.10+."
      ;;
  esac
fi

[[ -n "$PYTHON_BIN" ]] || fail "No se pudo obtener Python 3.10+ después del intento de instalación."

exec "$PYTHON_BIN" "$SCRIPT_DIR/bootstrap.py" "$@"
