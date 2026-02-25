# 🔑 Azure IAM & RBAC Management

This project demonstrates how to manage users and permissions in **Azure Active Directory (Entra ID)** (equivalent to AWS IAM).

## 📋 Prerequisites
- Azure CLI installed (`az login`)
- PowerShell
- **Permissions**: You must be an "Owner" or "User Access Administrator" in your subscription to assign roles.

## 🚀 Setup
1.  **Find your Domain**:
    Run `az ad signed-in-user show --query userPrincipalName` to see your domain (e.g., `user@mycompany.onmicrosoft.com`).
2.  **Update Script**:
    Edit `deploy.ps1` and replace `$DomainName` with your actual domain (e.g., `mycompany.onmicrosoft.com`).
3.  **Run Deployment**:
    ```powershell
    ./deploy.ps1
    ```

## 🛠️ What it does
1.  Creates a new user in Azure AD (`junior-dev`).
2.  Assigns the **Reader** role to this user for the `AzureFresherProjects` resource group.
3.  This simulates granting limited access to a new team member.
