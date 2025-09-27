import csv
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_customer_data(num_records=1000):
    """Generate dummy customer data with the specified structure."""
    customers = []
    used_emails = set()

    for customer_id in range(1, num_records + 1):
        # Generate unique email
        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)

        # Generate registration date (within last 2 years)
        start_date = datetime.now() - timedelta(days=730)
        end_date = datetime.now()
        registration_date = fake.date_between(start_date=start_date, end_date=end_date)

        customer = {
            'customer_id': customer_id,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': email,
            'phone': fake.phone_number(),
            'city': fake.city(),
            'registration_date': registration_date.strftime('%Y-%m-%d'),
            'customer_type': random.choice(['Regular', 'Premium', 'VIP'])
        }

        customers.append(customer)

    return customers

def save_to_csv(customers, filename='customer_data.csv'):
    """Save customer data to CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['customer_id', 'first_name', 'last_name', 'email', 'phone', 'city', 'registration_date', 'customer_type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for customer in customers:
            writer.writerow(customer)

if __name__ == "__main__":
    # Generate 1000 customer records
    num_records = 1000
    print(f"Generating {num_records} customer records...")

    customers = generate_customer_data(num_records)

    # Save to CSV
    filename = 'customer_data.csv'
    save_to_csv(customers, filename)

    print(f"Data saved to {filename}")
    print(f"Generated {len(customers)} customer records")

    # Display first 5 records as sample
    print("\nSample records:")
    for i, customer in enumerate(customers[:5]):
        print(f"{i+1}. ID: {customer['customer_id']}, Name: {customer['first_name']} {customer['last_name']}, "
              f"Email: {customer['email']}, Type: {customer['customer_type']}")
