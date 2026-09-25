[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$GameDirectory)
$ErrorActionPreference = 'Stop'
$targetRoot = (Resolve-Path -LiteralPath $GameDirectory).Path
$destination = [IO.Path]::GetFullPath((Join-Path $targetRoot 'T800HybridR4'))
$receiptPath = Join-Path $destination 't800-install-receipt.json'
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($receipt.schema -ne 1 -or $receipt.destination -ne $destination -or $null -eq $receipt.files -or @($receipt.files).Count -eq 0) { throw 'Invalid installation receipt.' }
function FileDigest([string]$Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
$prefix = $destination.TrimEnd([char[]]@('\','/')) + '\'
$seen = @{}
foreach ($file in $receipt.files) {
    $relative = [string]$file.relative
    if ([string]::IsNullOrWhiteSpace($relative) -or [IO.Path]::IsPathRooted($relative) -or $relative -match '^[A-Za-z]:') { throw "Invalid receipt file path: $relative" }
    if (@($relative -split '[\\/]' | Where-Object { $_ -eq '' -or $_ -eq '.' -or $_ -eq '..' }).Count -ne 0) { throw "Invalid receipt file path: $relative" }
    if ($seen.ContainsKey($relative) -or [string]$file.sha256 -notmatch '^[a-fA-F0-9]{64}$') { throw "Invalid receipt file record: $relative" }
    $seen[$relative] = $true
    $path = [IO.Path]::GetFullPath((Join-Path $destination $relative))
    if (-not $path.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) { throw "Receipt file escapes installation: $relative" }
    if (-not (Test-Path -LiteralPath $path -PathType Leaf) -or (FileDigest $path) -ne $file.sha256) { throw "Changed or missing installed file; launch blocked: $path" }
}
$allowedExe = if ($receipt.game -eq 'jk') { @('JK.EXE','JediKnight.EXE') } elseif ($receipt.game -eq 'mots') { @('JKM.EXE') } else { throw 'Invalid receipt game.' }
$resolvedExe = [IO.Path]::GetFullPath([string]$receipt.executable)
if ($resolvedExe -notin @($allowedExe | ForEach-Object { [IO.Path]::GetFullPath((Join-Path $targetRoot $_)) })) { throw 'Receipt executable is outside the selected game directory.' }
if (-not (Test-Path -LiteralPath $resolvedExe -PathType Leaf)) { throw 'Game executable missing.' }
# This is an intentional interactive launch requested by the user running this script.
Start-Process -FilePath $resolvedExe -ArgumentList @('-path','T800HybridR4') -WorkingDirectory $targetRoot
