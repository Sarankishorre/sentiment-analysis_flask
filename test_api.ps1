# PowerShell script to test the Flask API

$url = "http://localhost:5000/predict"
$headers = @{"Content-Type" = "application/json"}

# Test 1: Single positive text
$body = @{"text" = "I love this product, it is great!"} | ConvertTo-Json
Write-Host "Test 1 - Positive sentiment:"
Write-Host "Request: $body"
$response = Invoke-WebRequest -Uri $url -Method Post -Headers $headers -Body $body
Write-Host "Response: $($response.Content)"
Write-Host ""

# Test 2: Single negative text
$body = @{"text" = "This is terrible, I hate it"} | ConvertTo-Json
Write-Host "Test 2 - Negative sentiment:"
Write-Host "Request: $body"
$response = Invoke-WebRequest -Uri $url -Method Post -Headers $headers -Body $body
Write-Host "Response: $($response.Content)"
Write-Host ""

# Test 3: Batch texts
$body = @{"texts" = @("I love it", "This is awful", "Not bad")} | ConvertTo-Json
Write-Host "Test 3 - Batch predictions:"
Write-Host "Request: $body"
$response = Invoke-WebRequest -Uri $url -Method Post -Headers $headers -Body $body
Write-Host "Response: $($response.Content)"
Write-Host ""

# Test 4: Health check
$healthUrl = "http://localhost:5000/health"
Write-Host "Test 4 - Health check:"
$response = Invoke-WebRequest -Uri $healthUrl -Method Get
Write-Host "Response: $($response.Content)"
