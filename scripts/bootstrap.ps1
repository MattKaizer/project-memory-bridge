param(
  [string]$ProjectRoot = (Get-Location).Path,
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$PassthroughArgs
)

$ErrorActionPreference = 'Stop'

function Write-Log($Message) {
  Write-Host "[project-memory-bridge] $Message"
}

function Get-PythonCommand {
  foreach ($candidate in @('py', 'python')) {
    $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($cmd) {
      try {
        $version = & $candidate -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
        $parts = $version.Trim().Split('.') | ForEach-Object { [int]$_ }
        if ($parts[0] -gt 3 -or ($parts[0] -eq 3 -and $parts[1] -ge 10)) {
          return $candidate
        }
      } catch {}
    }
  }
  return $null
}

$python = Get-PythonCommand

if (-not $python) {
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    Write-Log 'Python 3.10+ no encontrado. Instalando con winget...'
    winget install -e --id Python.Python.3.12
  } elseif (Get-Command scoop -ErrorAction SilentlyContinue) {
    Write-Log 'Python 3.10+ no encontrado. Instalando con scoop...'
    scoop install python
  } else {
    throw '[project-memory-bridge] ERROR: Python 3.10+ no está instalado y no encontré winget ni scoop.'
  }

  $python = Get-PythonCommand
}

if (-not $python) {
  throw '[project-memory-bridge] ERROR: No se pudo obtener Python 3.10+.'
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& $python "$scriptDir/bootstrap.py" --project-root $ProjectRoot @PassthroughArgs
