import os
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, QueryTimePeriod, QueryDataset, QueryAggregation, QueryGrouping

# Configuration
SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")

def get_cost_report():
    if not SUBSCRIPTION_ID:
        print("❌ Please set AZURE_SUBSCRIPTION_ID environment variable.")
        return

    print(f"💰 Fetching Cost Data for Subscription: {SUBSCRIPTION_ID}...")
    
    credential = DefaultAzureCredential()
    client = CostManagementClient(credential)
    
    # Define Time Period (Current Month)
    end_date = datetime.now()
    start_date = end_date.replace(day=1)
    time_period = QueryTimePeriod(from_property=start_date, to=end_date)
    
    # Define Query
    query = QueryDefinition(
        type="Usage",
        timeframe="Custom",
        time_period=time_period,
        dataset=QueryDataset(
            granularity="None",
            aggregation={
                "totalCost": QueryAggregation(name="Cost", function="Sum")
            },
            grouping=[
                QueryGrouping(type="Dimension", name="ResourceGroup")
            ]
        )
    )

    # Execute Query
    scope = f"/subscriptions/{SUBSCRIPTION_ID}"
    result = client.query.usage(scope, query)
    
    print("\n📊 Cost by Resource Group (Current Month):")
    print("-" * 40)
    
    total_cost = 0.0
    for row in result.rows:
        cost = row[0]
        rg_name = row[1]
        currency = "USD" # Default assumption or fetch from metadata
        print(f"{rg_name:<30} : {cost:.2f} {currency}")
        total_cost += cost
        
    print("-" * 40)
    print(f"Total Estimated Cost: {total_cost:.2f} {currency}")

if __name__ == "__main__":
    get_cost_report()
