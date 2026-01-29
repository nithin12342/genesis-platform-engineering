# Azure Entra ID (IAM) Management Script
# Usage: ./deploy.ps1 -ResourceGroup "AzureFresherProjects" -NewUserName "junior-dev"

param (
    [string]$ResourceGroup = "AzureFresherProjects",
    [string]$NewUserName = "junior-dev",
    [string]$DomainName = "example.onmicrosoft.com" # You must change this to your actual Azure AD domain!
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Managing Azure Entra ID (IAM)..." -ForegroundColor Cyan

# 0. Check for Domain Name
if ($DomainName -eq "example.onmicrosoft.com") {
    Write-Host "⚠️ PLEASE UPDATE THE SCRIPT WITH YOUR ACTUAL AZURE AD DOMAIN NAME." -ForegroundColor Red
    Write-Host "Run 'az ad signed-in-user show --query userPrincipalName' to see your domain."
    exit 1
}

$UserPrincipalName = "$NewUserName@$DomainName"
$Password = "ChangeMe123!$" # In production, generate this securely

# 1. Create Resource Group (if needed)
az group create --name $ResourceGroup --location eastus

# 2. Create New User
Write-Host "Creating User: $UserPrincipalName..."
try {
    az ad user create `
        --display-name "Junior Developer" `
        --user-principal-name $UserPrincipalName `
        --password $Password `
        --force-change-password-next-sign-in false
}
catch {
    Write-Host "User might already exist. Continuing..." -ForegroundColor Yellow
}

# 3. Get User Object ID
$UserId = az ad user show --id $UserPrincipalName --query id --output tsv

# 4. Assign 'Reader' Role to Resource Group
Write-Host "Assigning 'Reader' role to Resource Group..."
$Scope = "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$ResourceGroup"

az role assignment create `
    --assignee $UserId `
    --role "Reader" `
    --scope $Scope

Write-Host "✅ User Created and Role Assigned!" -ForegroundColor Green
Write-Host "User: $UserPrincipalName"
Write-Host "Role: Reader"
Write-Host "Scope: $ResourceGroup"

# --- Frontend Deployment ---
# To run the frontend locally:
# cd frontend
# npm install
# npm run dev
