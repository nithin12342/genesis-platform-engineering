# 💰 Cost Optimization & Monitoring Tool (Azure Cost Management)

This project demonstrates how to programmatically query the **Azure Cost Management API** using Python to analyze cloud spending.

## 📋 Prerequisites
- Azure CLI
- Python 3.x
- Subscription ID (`AZURE_SUBSCRIPTION_ID`)

## 🚀 Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Analysis
Run the script to fetch the accumulated cost for the current month, grouped by Resource Group.
```bash
python cost_analysis.py
```

## 🛠️ What it does
1.  **Authentication**: Uses `DefaultAzureCredential` to authenticate.
2.  **API Query**: Sends a query to the Azure Cost Management API.
3.  **Aggregation**: Aggregates costs by **Resource Group** for the current month.
4.  **Reporting**: Prints a simple text-based report to the console.

## 💡 Use Case
This script can be extended to:
-   Send email alerts if spending exceeds a budget.
-   Identify unused resources (e.g., unattached disks).
-   Generate weekly cost reports for management.
