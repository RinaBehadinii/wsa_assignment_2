from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

db_config = {
    'host': os.getenv('DB_HOST', 'catalog-db'),
    'user': os.getenv('DB_USER', 'catalog_user'),
    'password': os.getenv('DB_PASS', 'catalog_pass'),
    'database': os.getenv('DB_NAME', 'catalog_db')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/catalog', methods=['GET'])
def get_books():
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        return jsonify({"books": books}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/catalog', methods=['POST'])
def add_book():
    connection = None
    try:
        data = request.json
        if not data or not all(k in data for k in ("title", "author", "published_year")):
            return jsonify({"error": "Missing title, author, or published_year"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO books (title, author, published_year) VALUES (%s, %s, %s)
        """
        cursor.execute(query, (data['title'], data['author'], data['published_year']))
        connection.commit()
        return jsonify({"message": "Book added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/catalog/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    connection = None
    try:
        data = request.json
        if not data or not all(k in data for k in ("title", "author", "published_year")):
            return jsonify({"error": "Missing title, author, or published_year"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            UPDATE books
            SET title = %s, author = %s, published_year = %s
            WHERE id = %s
        """
        cursor.execute(query, (data['title'], data['author'], data['published_year'], book_id))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Book not found"}), 404

        return jsonify({"message": "Book updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/catalog/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "DELETE FROM books WHERE id = %s"
        cursor.execute(query, (book_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Book not found"}), 404

        return jsonify({"message": "Book deleted successfully"}), 200
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
    """Health check endpoint to verify service availability."""
    return jsonify({"status": "Catalog service is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
