from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure MySQL database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'clockedin'
}


@app.route('/api/login', methods=['POST'])
def login():
    try:

        data = request.json
        print("Received request", data)
        email = data['email']
        password = data['password']

        # Sanitize the input
        sanitized_email = email
        sanitized_password = password

        # Establish MySQL connection
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()


        # Query the database
        query = "SELECT COUNT(*) as count FROM staff_users WHERE email = %s AND password = %s"
        cursor.execute(query, (sanitized_email, sanitized_password))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result[0] > 0:
            print("Sending success")
            return jsonify({'message': 'grantaccess'})
        else:
            print("Sending block")
            return jsonify({'message': 'blockaccess'})
    except Exception as e:
        return jsonify({'error': str(e)})


#####REGISTRATION
@app.route('/api/registration', methods=['POST'])
def register_user():
    try:
        # Extract data from the request
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        picture = request.files['picture']

        print("Receive registration:" + firstname)
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert data into the users table
        insert_query = "INSERT INTO users (firstname, lastname, email, picture) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (firstname, lastname, email, picture.read()))

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return jsonify({"message": "Registration successful"}), 200
    except Exception as e:
        return jsonify({"error": "Registration error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)  # Change host and port as needed
