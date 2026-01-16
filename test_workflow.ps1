# Complete workflow test script

Write-Host "`n=================================================" -ForegroundColor Cyan
Write-Host "TESTING COMPLETE A2A WORKFLOW" -ForegroundColor Cyan
Write-Host "=================================================`n" -ForegroundColor Cyan

# Step 1: Build images
Write-Host "[1/5] Building Docker images..." -ForegroundColor Yellow
docker-compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Build failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Images built successfully`n" -ForegroundColor Green

# Step 2: Start purple agent
Write-Host "[2/5] Starting purple agent..." -ForegroundColor Yellow
docker-compose up -d purple-agent
Start-Sleep -Seconds 10

# Check if healthy
$health = docker inspect sentiment-purple --format='{{.State.Health.Status}}'
if ($health -ne "healthy") {
    Write-Host "✗ Purple agent not healthy: $health" -ForegroundColor Red
    docker-compose logs purple-agent
    docker-compose down
    exit 1
}
Write-Host "✓ Purple agent running and healthy`n" -ForegroundColor Green

# Step 3: Test purple agent directly
Write-Host "[3/5] Testing purple agent..." -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri http://localhost:8000/health -Method Get
if ($response.status -eq "healthy") {
    Write-Host "✓ Health check passed" -ForegroundColor Green
} else {
    Write-Host "✗ Health check failed" -ForegroundColor Red
    docker-compose down
    exit 1
}

# Test assessment endpoint
$body = @{
    task = "Analyze sentiment for: iPhone 16"
} | ConvertTo-Json

try {
    $assessResponse = Invoke-RestMethod -Uri http://localhost:8000/assess -Method Post -Body $body -ContentType "application/json"
    if ($assessResponse.success) {
        Write-Host "✓ Assessment endpoint working" -ForegroundColor Green
        Write-Host "  Sentiment: $($assessResponse.result.sentiment)" -ForegroundColor Cyan
    } else {
        Write-Host "✗ Assessment failed: $($assessResponse.error)" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Assessment request failed: $_" -ForegroundColor Red
}

Write-Host ""

# Step 4: Run green agent
Write-Host "[4/5] Running green agent assessment..." -ForegroundColor Yellow
docker-compose up green-agent
Write-Host "✓ Assessment complete`n" -ForegroundColor Green

# Step 5: Check results
Write-Host "[5/5] Checking results..." -ForegroundColor Yellow
if (Test-Path "data/assessment_results.json") {
    $results = Get-Content "data/assessment_results.json" | ConvertFrom-Json
    Write-Host "✓ Results file generated" -ForegroundColor Green
    Write-Host "`nSummary:" -ForegroundColor Cyan
    Write-Host "  Accuracy: $($results.results[0].details.summary.accuracy * 100)%" -ForegroundColor White
    Write-Host "  Average score: $([math]::Round($results.results[0].details.summary.average_score, 2))" -ForegroundColor White
} else {
    Write-Host "✗ Results file not found" -ForegroundColor Red
}

# Cleanup
Write-Host "`nCleaning up..." -ForegroundColor Yellow
docker-compose down
Write-Host "✓ Cleanup complete" -ForegroundColor Green

Write-Host "`n=================================================" -ForegroundColor Cyan
Write-Host "✅ WORKFLOW TEST COMPLETE" -ForegroundColor Green
Write-Host "=================================================`n" -ForegroundColor Cyan