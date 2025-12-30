param(
  [Parameter(Mandatory=$true)]
  [string]$ProjectId,

  [Parameter(Mandatory=$true)]
  [string]$Location
)

$ErrorActionPreference = "Stop"

Write-Host "== Ops Engine POC: Running DDLs ==" -ForegroundColor Cyan
Write-Host "Project: $ProjectId"
Write-Host "Location: $Location"
Write-Host ""

# Helper to run a SQL file in BigQuery
function Invoke-BqSqlFile {
  param(
    [Parameter(Mandatory=$true)][string]$SqlPath
  )

  if (!(Test-Path $SqlPath)) {
    throw "SQL file not found: $SqlPath"
  }

  Write-Host "Running: $SqlPath" -ForegroundColor Yellow

  bq query `
    --project_id=$ProjectId `
    --location=$Location `
    --use_legacy_sql=false `
    --quiet `
    < $SqlPath

  Write-Host "OK: $SqlPath" -ForegroundColor Green
}

# Run REF DDLs
$refDir = "C:\aj-ops-engine-poc\bigquery\ddl\ref"
$goldDir = "C:\aj-ops-engine-poc\bigquery\ddl\gold"

Write-Host "`n-- REF DDLs --" -ForegroundColor Cyan
Get-ChildItem "$refDir\*.sql" | Sort-Object Name | ForEach-Object {
  Invoke-BqSqlFile $_.FullName
}

Write-Host "`n-- GOLD DDLs --" -ForegroundColor Cyan
Get-ChildItem "$goldDir\*.sql" | Sort-Object Name | ForEach-Object {
  Invoke-BqSqlFile $_.FullName
}

Write-Host "`nAll DDLs executed successfully." -ForegroundColor Green
