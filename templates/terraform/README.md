# 🏗️ Infrastructure as Code (Terraform)

This project demonstrates how to use **Terraform** to provision Azure infrastructure (IaC).

## 📋 Prerequisites
- Azure CLI installed (`az login`)
- Terraform installed
- PowerShell

## 🚀 Deployment
Run the deployment script to initialize and apply the Terraform configuration.

```powershell
./deploy.ps1
```

## 🛠️ What it does
1.  **Providers**: Configures the `azurerm` provider.
2.  **Resources**:
    -   Resource Group (`AzureTerraformLab`)
    -   Virtual Network (`myTFVnet`)
    -   Subnet (`myTFSubnet`)
    -   Public IP
    -   Network Interface (NIC)
    -   Linux VM (`myTFVM`)
3.  **Outputs**: Prints the Public IP of the created VM.

## 🧹 Cleanup
To remove all resources created by Terraform:
```bash
terraform destroy -auto-approve
```
