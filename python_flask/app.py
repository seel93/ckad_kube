from flask import Flask
from logging.config import dictConfig
import mysql.connector
from pymongo import MongoClient

config = {
    'user': 'root',
    'password': 'mysecretpassword',
    'host': 'mysql',
    'database': 'mydatabase'
}


cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Example query
query = "SHOW TABLES"
cursor.execute(query)

# Print results
for result in cursor:
    print(result)

# Clean up
cursor.close()
cnx.close()

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)


@app.route('/')
def hello_geek():
    app.logger.info("request has been made")
    return '<h1>Hello from Flask rolling updated, Docker and kubernetes </h2>'


@app.route('/test')
def test_endpoint():
    app.logger.info("request to another endpoint has been made")
    return '<h1>This is another endpoint </h2>'


@app.route('/health')
def db_health_check():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        create_table = """
            CREATE TABLE IF NOT EXISTS customers (
                id INT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100)
            )
        """

        # Execute the SQL statement
        cursor.execute(create_table)

        # Commit the changes to the database
        cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()
        return "Query complete"
    except mysql.connector.Error as err:
        return "Database is not healthy: {}".format(err)



@app.route('/query')
def get_customer_by_id():
    # Establish a connection to the MySQL server
    cnx = mysql.connector.connect(**config)

    # Create a cursor object
    cursor = cnx.cursor()

    # Define the SQL statement
    query = "SELECT * FROM customers"

    # Execute the SQL statement with the customer_id parameter
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Return the result
    return str(result)


@app.route('/mongo')
def create_collection():
    # Create a MongoClient instance
    client = MongoClient('mongodb://mongodb:27017')


    # Access the database
    db = client["my_db"]

    # Create a collection
    collection = db["users"]


    documents = [
        {"name": "Jane", "age": 25, "email": "jane@example.com"},
        {"name": "Bob", "age": 35, "email": "bob@example.com"},
        {"name": "Alice", "age": 40, "email": "alice@example.com"}
    ]

    # Insert the documents into the collection
    if isinstance(documents, dict):
        # Insert a single document
        result = collection.insert_one(documents)
        app.logger.info("Inserted document with ID:", result.inserted_id)
    elif isinstance(documents, list):
        # Insert multiple documents
        result = collection.insert_many(documents)
        app.logger.info("Inserted", len(result.inserted_ids), "documents")
    else:
        app.logger.info("Invalid input: documents must be a dictionary or a list of dictionaries")
    
    return "done with mongo"


@app.route('/qmongo')
def run_mongodb_query():
    # Connect to MongoDB
    client = MongoClient('mongodb://mongodb:27017')
    
    # Access the specified database and collection
       # Access the database
    db = client["my_db"]

    # Create a collection
    collection = db["users"]
    
    # Execute the query
    result = collection.find({ 'name': 'Bob' })
    app.logger.info(result)
    
    # Close the MongoDB connection
    client.close()

    return result



if __name__ == "__main__":
    app.run(debug=True)
