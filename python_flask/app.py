from flask import Flask, jsonify
import os
from logging.config import dictConfig
import mysql.connector
from pymongo import MongoClient

config = {
    'user': 'root',
    'password': 'mysecretpassword',
    'host': 'mysql',
    'database': 'mydatabase'
}


try:
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
except Error as e:
    print(e)


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
        from flask import Flask, jsonify
        app.logger.info("Inserted", len(result.inserted_ids), "documents")
    else:
        app.logger.info(
            "Invalid input: documents must be a dictionary or a list of dictionaries")

    return "done with mongo"


@app.route('/qmongo')
def run_mongodb_query():
    # Connect to MongoDB
    client = MongoClient('mongodb://mongodb:27017')
    app.logger.info("init client")
    # Access the specified database and collection
    # Access the database
    db = client["my_db"]

    # Create a collection
    collection = db["users"]

    # Execute the query
    result = collection.find({'name': 'Bob'})
    app.logger.info(result)

    # Close the MongoDB connection
    client.close()

    return result


@app.route('/listdir/<path:dir_path>', methods=['GET'])
def list_directory_contents(dir_path):
    try:
        # Note: be careful here. Allowing users to specify arbitrary directory
        # paths can be a security risk. You may want to add checks to make sure
        # they can only access directories they should be able to.
        files = os.listdir(dir_path)
        pwd = os.listdir(os.getcwd())
        files_in_directory = os.listdir(os.getcwd())
        return jsonify(files)
    except FileNotFoundError:
        return jsonify({
            "ls": f"{list(files_in_directory)}",
            "pwd": f"{pwd}",    
            "error": f"The directory {dir_path} does not exist."
        }), 404
    except NotADirectoryError:
        return jsonify({
            "ls": f"{list(files_in_directory)}",
            "pwd": f"{pwd}",
            "error": f"{dir_path} is not a directory."
        }), 400
    except PermissionError:
        return jsonify({"error": f"You do not have permissions to access the directory {dir_path}."}), 403


if __name__ == "__main__":
    app.run(debug=True)
