import boto3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY

# Initialize AWS client for Cost Explorer
client = boto3.client(
    'ce',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def get_cost_data(start_date, end_date):
    """Fetch cost and usage data from AWS Cost Explorer."""
    try:
        response = client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )
        return response['ResultsByTime']
    except Exception as e:
        print(f"Error fetching cost data: {e}")
        return []

def process_cost_data(cost_data):
    """Process and structure cost data for analysis."""
    records = []
    for day in cost_data:
        date = day['TimePeriod']['Start']
        amount = float(day['Total']['UnblendedCost']['Amount'])
        records.append({'Date': date, 'Cost': amount})
    return pd.DataFrame(records)

def plot_cost_data(dataframe):
    """Plot cost data to visualize spending trends."""
    plt.figure(figsize=(10, 6))
    plt.plot(dataframe['Date'], dataframe['Cost'], marker='o')
    plt.title('AWS Daily Cost Analysis', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cost (USD)', fontsize=12)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Define date range for the cost analysis
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    print(f"Fetching cost data from {start_date} to {end_date}...")
    cost_data = get_cost_data(start_date, end_date)
    
    if cost_data:
        df = process_cost_data(cost_data)
        print(df)
        plot_cost_data(df)
    else:
        print("No cost data available.")

