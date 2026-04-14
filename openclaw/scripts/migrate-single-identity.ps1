param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$canonicalUserId = "edgar"
$canonicalAgentId = "agent"
$repoRoot = Split-Path -Parent $PSScriptRoot
$backupDir = Join-Path $repoRoot "migration-backups"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupPath = Join-Path $backupDir "mem0-pre-single-identity-$timestamp.json"

function Get-Mem0Key {
  $candidates = @(
    "D:\01_projects_staging\龍蝦專案\Edgars_secret\from mem0 import MemoryClient.txt",
    "D:\01_projects_staging\龍蝦專案\Edgars_secret\memo控制台api.txt"
  )

  foreach ($path in $candidates) {
    if (-not (Test-Path -LiteralPath $path)) { continue }
    $raw = Get-Content -LiteralPath $path -Raw
    $match = [regex]::Match($raw, "m0-[A-Za-z0-9_-]+")
    if ($match.Success) {
      return $match.Value
    }
  }

  throw "Mem0 API key not found in Edgars_secret."
}

function Invoke-Mem0Json {
  param(
    [Parameter(Mandatory = $true)][string]$Method,
    [Parameter(Mandatory = $true)][string]$Uri,
    [hashtable]$Headers,
    [object]$Body
  )

  if ($null -ne $Body) {
    return Invoke-RestMethod -Method $Method -Uri $Uri -Headers $Headers -Body ($Body | ConvertTo-Json -Depth 10)
  }

  return Invoke-RestMethod -Method $Method -Uri $Uri -Headers $Headers
}

function Get-MemoriesForUser {
  param(
    [Parameter(Mandatory = $true)][string]$UserId,
    [hashtable]$Headers
  )

  $response = Invoke-Mem0Json -Method POST -Uri "https://api.mem0.ai/v2/memories/?page=1&page_size=1000" -Headers $Headers -Body @{
    filters = @{
      user_id = $UserId
    }
    page_size = 1000
  }

  @($response.results) | Where-Object {
    $agentProp = $_.PSObject.Properties["agent_id"]
    -not $agentProp -or [string]::IsNullOrWhiteSpace([string]$agentProp.Value)
  }
}

function Get-MemoriesForCanonicalAgent {
  param([hashtable]$Headers)

  $response = Invoke-Mem0Json -Method POST -Uri "https://api.mem0.ai/v2/memories/?page=1&page_size=1000" -Headers $Headers -Body @{
    filters = @{
      AND = @(
        @{ user_id = $canonicalUserId },
        @{ agent_id = $canonicalAgentId }
      )
    }
    page_size = 1000
  }

  @($response.results)
}

function Add-CanonicalMemory {
  param(
    [Parameter(Mandatory = $true)][string]$Text,
    [Parameter(Mandatory = $true)][string]$SourceUser,
    [Parameter(Mandatory = $true)][string]$SourceId,
    [hashtable]$Headers
  )

  Invoke-Mem0Json -Method POST -Uri "https://api.mem0.ai/v1/memories/" -Headers $Headers -Body @{
    messages = @(
      @{
        role = "user"
        content = $Text
      }
    )
    user_id = $canonicalUserId
    agent_id = $canonicalAgentId
    infer = $false
    metadata = @{
      migrated_from_user = $SourceUser
      migrated_from_memory_id = $SourceId
      migration_kind = "single_identity_consolidation"
      migrated_at = (Get-Date).ToString("o")
    }
  }
}

function Remove-MemoryById {
  param(
    [Parameter(Mandatory = $true)][string]$MemoryId,
    [hashtable]$Headers
  )

  Invoke-Mem0Json -Method DELETE -Uri "https://api.mem0.ai/v1/memories/$MemoryId/" -Headers $Headers | Out-Null
}

function Remove-EntityIfExists {
  param(
    [Parameter(Mandatory = $true)][ValidateSet("user", "agent", "run", "app")][string]$Type,
    [Parameter(Mandatory = $true)][string]$Name,
    [hashtable]$Headers
  )

  try {
    Invoke-Mem0Json -Method DELETE -Uri "https://api.mem0.ai/v2/entities/$Type/$Name/" -Headers $Headers | Out-Null
    return $true
  } catch {
    return $false
  }
}

$apiKey = Get-Mem0Key
$headers = @{
  Authorization = "Token $apiKey"
  "Content-Type" = "application/json"
}

$legacyUsers = @("edgar", "mem0-mcp")
$legacyItems = foreach ($user in $legacyUsers) {
  Get-MemoriesForUser -UserId $user -Headers $headers
}

$legacyItems = @($legacyItems)

if (-not (Test-Path -LiteralPath $backupDir)) {
  New-Item -ItemType Directory -Path $backupDir | Out-Null
}

[pscustomobject]@{
  exportedAt = (Get-Date).ToString("o")
  canonicalUserId = $canonicalUserId
  canonicalAgentId = $canonicalAgentId
  legacyItems = $legacyItems
} | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $backupPath -Encoding UTF8

$existingCanonicalTexts = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
foreach ($item in Get-MemoriesForCanonicalAgent -Headers $headers) {
  $memoryText = ""
  if ($null -ne $item.memory) {
    $memoryText = [string]$item.memory
  }
  $null = $existingCanonicalTexts.Add($memoryText.Trim())
}

$migrated = New-Object System.Collections.Generic.List[object]
$skipped = New-Object System.Collections.Generic.List[object]
$failures = New-Object System.Collections.Generic.List[object]

foreach ($item in $legacyItems) {
  $text = ""
  if ($null -ne $item.memory) {
    $text = [string]$item.memory
  }
  $text = $text.Trim()
  if ([string]::IsNullOrWhiteSpace($text)) {
    $skipped.Add([pscustomobject]@{ id = $item.id; reason = "empty_memory" }) | Out-Null
    continue
  }

  if ($existingCanonicalTexts.Contains($text)) {
    $skipped.Add([pscustomobject]@{ id = $item.id; reason = "duplicate_text" }) | Out-Null
    continue
  }

  try {
    Add-CanonicalMemory -Text $text -SourceUser $item.user_id -SourceId $item.id -Headers $headers | Out-Null
    $null = $existingCanonicalTexts.Add($text)
    $migrated.Add([pscustomobject]@{ id = $item.id; user_id = $item.user_id }) | Out-Null
  } catch {
    $failures.Add([pscustomobject]@{ id = $item.id; user_id = $item.user_id; error = $_.Exception.Message }) | Out-Null
  }
}

if ($failures.Count -gt 0) {
  Write-Output "Migration aborted before deletion because some adds failed."
  Write-Output "Backup: $backupPath"
  $failures | Format-Table -AutoSize
  exit 1
}

foreach ($item in $legacyItems) {
  Remove-MemoryById -MemoryId $item.id -Headers $headers
}

$oldAgents = @(
  "haodai",
  "channel-fast",
  "mem0-lab",
  "codex",
  "claude-desktop",
  "claude-code",
  "github-copilot",
  "ollama",
  "perplexity-computer",
  "mini-agent"
)

$removedEntities = New-Object System.Collections.Generic.List[string]

foreach ($agent in $oldAgents) {
  if (Remove-EntityIfExists -Type agent -Name $agent -Headers $headers) {
    $removedEntities.Add("agent:$agent") | Out-Null
  }
}

if (Remove-EntityIfExists -Type user -Name "mem0-mcp" -Headers $headers) {
  $removedEntities.Add("user:mem0-mcp") | Out-Null
}

[pscustomobject]@{
  backup = $backupPath
  migrated = $migrated.Count
  skipped = $skipped.Count
  removed_entities = @($removedEntities)
} | Format-List
