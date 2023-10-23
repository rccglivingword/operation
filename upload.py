import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
# Load the env variables
load_dotenv()

uri = os.getenv('DATABASE_URI')


# Define the db details

db_name = 'member'
collection_name = 'registers'

# CSV file path
csv_file = 'data.csv'  # Change this to your CSV file path

# Connect to MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[db_name]
collection = db[collection_name]

# Load CSV data into a Pandas DataFrame
df = pd.read_csv(csv_file)

# Convert the DataFrame to a list of dictionaries (one dictionary per row)
data = df.to_dict(orient='records')

# Insert the data into the MongoDB collection
collection.insert_many(data)

# Close the MongoDB connection
client.close()

print(f'Loaded {len(data)} documents into the {collection_name} collection in the {db_name} database.')
