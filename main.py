import os
import boto3
from dotenv import load_dotenv
import csv

load_dotenv()

aws_region = os.getenv('AWS_REGION')
aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
email = os.getenv('EMAIL')


ses_client = boto3.client('ses', region_name=aws_region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

with open('template.html', 'r') as template_file:
    template = template_file.read()

with open('recipients.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)

    email_counter = 0

    for row in reader:
        try:
            ses_client.send_email(
                Destination={
                    'ToAddresses': [row['email']]
                },
                Message={
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': "Subject"
                    },
                    'Body': {
                        'Html': {
                            'Charset': 'UTF-8',
                            'Data': template,
                        }
                    }
                },
                Source = email
            )
            email_counter += 1

            print(f"Email sent successfully to {row['email']}")

        except Exception as e:
            print(f"Error sending email to {row['email']} - {e}")

print(f"Total emails sent: {email_counter}")