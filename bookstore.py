from flask import Flask, request, jsonify, json, abort

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello World!<h1>"

with open('books.json') as json_data:
    books_data = json.load(json_data)['books']

@app.route('/isbns', methods=['GET'])
def get_isbns():
    isbns = [book['isbn'] for book in books_data]
    return jsonify(isbns)

@app.route('/isbns/<isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
    book = next((b for b in books_data if b['isbn'] == isbn), None)
    if book:
        return jsonify(book)
    else:
        abort(404)

@app.route('/authors/<expression>', methods=['GET'])
def get_authors_by_title(expression):
    authors = [book['author'] for book in books_data if expression in book['title']]
    return jsonify(authors)


@app.route('/books/<isbn>', methods=['GET','PUT'])
def update_publisher(isbn):
    new_publisher = request.args.get('publisher')

    for book in books_data:
        if book['isbn'] == isbn:
            book['publisher'] = new_publisher
            return jsonify(
                {"message": f"Zaktualizowano wydawce ksiazki o numerze ISBN {isbn} na {new_publisher}."}), 200

    return jsonify({"error": f"Nie znaleziono ksiazki o numerze ISBN {isbn}."}), 404