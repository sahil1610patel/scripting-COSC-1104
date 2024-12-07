# Author: Sahil Patel , id:100991127
# Date: 2024/12/06
# Description: This code Fetches, processes, and visualizes AWS cost data, sends alerts for budget breaches, and stops idle EC2 instances to optimize resource usage.

import boto3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, SENDER_EMAIL, RECEIVER_EMAIL, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD, BUDGET_THRESHOLD, FORECAST_DAYS

# Initialize AWS Cost Explorer client
client = boto3.client('ce',
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY,
                      region_name=AWS_REGION)

# Initialize EC2 client
ec2_client = boto3.client('ec2', 
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY,
                          region_name=AWS_REGION)

# Initialize CloudWatch client
cloudwatch_client = boto3.client('cloudwatch',
                                 aws_access_key_id=AWS_ACCESS_KEY,
                                 aws_secret_access_key=AWS_SECRET_KEY,
                                 region_name=AWS_REGION)

def fetch_cost_data():
    # Fetch cost data from AWS Cost Explorer
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': '2024-11-01',  # Change as needed
            'End': '2024-11-30'
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )
    return response

def process_data(response):
    # Process the response into a Pandas DataFrame
    cost_data = []
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            cost_data.append([service, cost])
    
    df = pd.DataFrame(cost_data, columns=['Service', 'Cost'])
    return df

def visualize_costs(df):
    # Visualize the costs with a bar plot
    plt.figure(figsize=(10, 6))  # Resize the plot for better visibility
    sns.barplot(x='Service', y='Cost', data=df)
    plt.title('AWS Cost Breakdown by Service')
    plt.xlabel('Service')
    plt.ylabel('Cost (USD)')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to avoid clipping
    plt.show()

def save_to_csv(df, filename="aws_cost_data.csv"):
    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def send_email_alert(subject, body):
    # Send an email alert if spending exceeds threshold
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

def check_spending_alert(df):
    total_cost = df['Cost'].sum()
    if total_cost > BUDGET_THRESHOLD:
        subject = "AWS Spending Alert: Budget Exceeded"
        body = f"Your AWS spending has exceeded the budget of ${BUDGET_THRESHOLD}. Total cost is ${total_cost}."
        send_email_alert(subject, body)

def forecast_budget(df):
    # Simple forecast based on past data (for illustration)
    total_cost = df['Cost'].sum()
    forecasted_cost = total_cost * (FORECAST_DAYS / 30)  # Assume linear growth
    return forecasted_cost

def check_ec2_idle_and_stop():
    # Check the CPU utilization of EC2 instances and stop if idle
    response = cloudwatch_client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'cpuUtilization',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': 'CPUUtilization',
                        'Dimensions': [{'Name': 'InstanceId', 'Value': 'your-instance-id'}],  # Replace with your EC2 instance ID
                    },
                    'Period': 300,
                    'Stat': 'Average',
                },
                'ReturnData': True,
            },
        ],
        StartTime='2024-12-05T00:00:00Z',  # Change as needed
        EndTime='2024-12-06T00:00:00Z',  # Change as needed
    )

    cpu_utilization = response['MetricDataResults'][0]['Values']
    
    if not cpu_utilization:
        print("No CPU utilization data available")
        return

    avg_cpu = sum(cpu_utilization) / len(cpu_utilization)
    print(f"Average CPU Utilization: {avg_cpu}%")

    if avg_cpu < 10:  # If CPU utilization is below 10%, consider it idle
        print("EC2 instance is idle, stopping it...")
        ec2_client.stop_instances(InstanceIds=['your-instance-id'])  # Replace with your EC2 instance ID

def main():
    # Fetch, process, and visualize AWS cost data
    response = fetch_cost_data()
    df = process_data(response)
    
    # Visualize the cost breakdown
    visualize_costs(df)
    
    # Check if spending exceeds the budget and send alerts
    check_spending_alert(df)
    
    # Forecast the budget for the next 30 days
    forecasted_cost = forecast_budget(df)
    print(f"Forecasted spending for the next {FORECAST_DAYS} days: ${forecasted_cost:.2f}")
    
    # Save the data to CSV
    save_to_csv(df)  # This will save the processed data to a CSV file
    
    # Check EC2 instances' idle status and stop if necessary
    check_ec2_idle_and_stop()

if __name__ == "__main__":
    main()
