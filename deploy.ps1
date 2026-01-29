# Terraform Deployment Script
# Usage: ./deploy.ps1

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Terraform Deployment..." -ForegroundColor Cyan

# Check if Terraform is installed
if (-not (Get-Command "terraform" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Terraform is not installed. Please install it first."
    Write-Host "Download: https://www.terraform.io/downloads"
    exit 1
}

# Check for SSH Key (required by main.tf)
if (-not (Test-Path "~/.ssh/id_rsa.pub")) {
    Write-Host "⚠️ SSH Key not found. Generating one..." -ForegroundColor Yellow
    mkdir -p ~/.ssh
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
}

# 1. Initialize
Write-Host "Initializing Terraform..."
terraform init

# 2. Plan
Write-Host "Planning Deployment..."
terraform plan -out=tfplan

# 3. Apply
Write-Host "Applying Deployment (this will create resources)..."
terraform apply tfplan

Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "To destroy resources, run: terraform destroy -auto-approve"

# --- Frontend Deployment ---
# To run the frontend locally:
# cd frontend
# npm install
# npm run dev
