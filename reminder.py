import pymongo
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # MongoDB connection details
    mongo_host = 'localhost'
    mongo_port = 27017
    mongo_db = 'your_database'
    mongo_collection = 'your_collection'

    # SMTP server details
    smtp_host = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_username'
    smtp_password = 'your_password'

    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client[mongo_db]
    collection = db[mongo_collection]

    # Retrieve birthday dates
    birthdays = collection.find()

    # Send reminder emails
    for birthday in birthdays:
        name = birthday['name']
        email = birthday['email']
        date = birthday['date']

        # Calculate the difference between the birthday and today's date
        today = datetime.now().date()
        birthday_date = datetime.strptime(date, '%Y-%m-%d').date()
        days_until_birthday = (birthday_date - today).days

        # Check if the birthday is in 5 days
        if days_until_birthday == 5:
            # Compose email message
            message = f"Hi {name},\n\nJust a reminder that your birthday is in 5 days, on {date}!\n\nBest regards,\nYour Name"

            # Create email
            msg = MIMEText(message)
            msg['Subject'] = 'Birthday Reminder'
            msg['From'] = smtp_username
            msg['To'] = email

            # Send email
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
                print(f"Reminder email sent to {name} at {email}")
