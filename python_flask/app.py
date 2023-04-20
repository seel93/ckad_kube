from flask import Flask
from logging.config import dictConfig
import mysql.connector

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
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result[0] == 1:
            return "Database is healthy"
        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        return "Database is not healthy: {}".format(err)
    return "Unknown error"



if __name__ == "__main__":
    app.run(debug=True)