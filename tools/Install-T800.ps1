[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$GameDirectory,
    [ValidateSet('jk','mots')][string]$Game,
    [ValidateSet('original','holding-curl')][string]$Pose = 'original',
    [ValidateSet('indexed','rgb565')][string]$Materials = 'indexed',
    [switch]$Uninstall
)
$ErrorActionPreference = 'Stop'
$builder = Join-Path $PSScriptRoot 't800.py'
if ($Uninstall) {
    & python $builder uninstall --game-directory $GameDirectory
} else {
    if (-not $Game) { throw 'Specify -Game jk or -Game mots.' }
    & python $builder install --game $Game --game-directory $GameDirectory --pose $Pose --materials $Materials
}
if ($LASTEXITCODE -ne 0) { throw "T800 installer stopped with exit code $LASTEXITCODE." }
