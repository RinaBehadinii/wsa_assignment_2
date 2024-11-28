from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app) 

db_config = {
    'host': os.getenv('DB_HOST', 'user-db'), 
    'user': os.getenv('DB_USER', 'user_user'),
    'password': os.getenv('DB_PASS', 'user_pass'),
    'database': os.getenv('DB_NAME', 'user_db')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/users', methods=['GET'])
def get_users():
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify({"users": users}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/users', methods=['POST'])
def create_user():
    connection = None
    try:
        data = request.json
        if not data.get('name') or not data.get('email'):
            return jsonify({"error": "Name and Email are required"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(query, (data['name'], data['email']))
        connection.commit()
        return jsonify({"message": "User created successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    connection = None
    try:
        data = request.json
        if not data.get('name') or not data.get('email'):
            return jsonify({"error": "Name and Email are required"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE users SET name = %s, email = %s WHERE id = %s"
        cursor.execute(query, (data['name'], data['email'], user_id))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "User service is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
