import os
from flask import Flask, jsonify
import psycopg2
app = Flask(__name__)
db_user = os.environ.get('DATABASE_USERNAME')
db_password = os.environ.get('DATABASE_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_host = os.getenv('DB_HOST') 
db_port = int(os.getenv('DB_PORT'))


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=5432,
            database=db_name,
            user=db_user,
            password=db_password
        )
        print("Connection successful")
        return conn
    except psycopg2.InterfaceError as e:
        print(f"InterfaceError connecting to the database: {e}")
    except psycopg2.DatabaseError as e:
        print(f"DatabaseError connecting to the database: {e}")
    except Exception as e:
        print("General error connecting to the db{e}")
    return None

def create_table_if_not_exists():
    conn = get_db_connection()
    if conn is None:
        print("Database connection failed")
        return False

    try:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS greetings (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL
        );
        """
        cursor.execute(create_table_query)

        # Insert the initial data if it does not exist
        insert_data_query = """
        INSERT INTO greetings (id, message) VALUES (1, 'Hello World');
        """
        cursor.execute(insert_data_query)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Table created and initial data inserted successfully")
        return True
    except Exception as e:
        print(f"Error creating table or inserting data: {e}")
        return False

#Define Flask routes
@app.route('/greeting/<int:id>', methods=['GET'])
def get_greeting(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        cursor = conn.cursor()
        # Execute the query
        cursor.execute("SELECT message FROM greetings WHERE id = %s", (id,))
        row = cursor.fetchone()

        # Close the connection
        cursor.close()
        conn.close()

        if row:
            return row[0]
        else:
            return 'Greeting not found'
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

if __name__ == '__main__':
    # Create table if it does not exist and insert initial data
    create_table_if_not_exists()
        # Check if the record with id=1 exists before running Flask
    print("Record with id=1 found. Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
