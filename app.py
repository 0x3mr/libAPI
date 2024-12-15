from flask import Flask, request, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint
import json
import os

app = Flask(__name__)

SWAGGER_URL = '/api-docs'
API_URL = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "libAPI"}
)

app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

DATA_FILE = 'books.json'


def load_books():
    """
    Load books from JSON file.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []


def save_books(books):
    """
    Save books to the JSON file.
    """
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(books, f, indent=4)
    except IOError as e:
        raise Exception(f"Error saving books: {e}")

@app.route('/', methods=['GET'])
def home():
    """
    Serve the HTML documentation page at the root URL.
    """
    return render_template('index.html')


@app.route('/books', methods=['POST'])
def add_book():
    """
    Add a new book to the library.
    """
    book = request.json

    required_fields = ['title', 'author', 'publishedYear', 'isbn']
    for field in required_fields:
        if field not in book:
            return jsonify({'error': f'{field} is required'}), 400

    books = load_books()

    if any(b['isbn'] == book['isbn'] for b in books):
        return jsonify({'error': 'Book with this ISBN already exists'}), 409

    books.append(book)
    save_books(books)
    return jsonify(book), 201


@app.route('/books', methods=['GET'])
def list_books():
    """
    List all books or filter books.
    """
    books = load_books()

    author = request.args.get('author')
    published_year = request.args.get('publishedYear')
    genre = request.args.get('genre')

    filtered_books = books
    if author:
        filtered_books = [b for b in filtered_books if b['author'].lower() == author.lower()]
    if published_year:
        filtered_books = [b for b in filtered_books if str(b['publishedYear']) == str(published_year)]
    if genre:
        filtered_books = [b for b in filtered_books if b.get('genre', '').lower() == genre.lower()]

    return jsonify(filtered_books)


@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """
    Delete a book by ISBN.
    """
    books = load_books()
    original_length = len(books)
    books = [b for b in books if b['isbn'] != isbn]
    if len(books) == original_length:
        return jsonify({'error': 'Book not found'}), 404
    save_books(books)
    return '', 204


@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    """
    Update book details by ISBN.
    """
    books = load_books()
    book_to_update = None
    book_index = None
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            book_to_update = book
            book_index = i
            break
    if not book_to_update:
        return jsonify({'error': 'Book not found'}), 404

    update_data = request.json
    book_to_update.update(update_data)
    books[book_index] = book_to_update
    save_books(books)
    return jsonify(book_to_update)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
