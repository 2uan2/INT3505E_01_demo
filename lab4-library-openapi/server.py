from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/docs'

API_URL = '/openapi.yaml'

swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)

app.register_blueprint(swagger_blueprint)

@app.route('/openapi.yaml')
def get_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml')

books = [
    {"isbn": 100, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 200, "title": "1984", "author": "George Orwell", "borrowed": False}
]

@app.route('/')
def home():
    return '<div>Welcome to uhh, idk, you can checkout the docs at <a href="/docs">docs</a></div>'

@app.route('/books')
def get_books():
    return jsonify(books)

@app.route('/books/<int:isbn>')
def get_book(isbn: int):
    book = [book for book in books if book['isbn'] == isbn]
    print(book)
    return book[0] if book else (jsonify({'error': 'no book with that isbn'}), 404)

@app.route('/books', methods=['POST'])
def create_book():
    try:
        isbn = int(request.json['isbn'])
        title = request.json['title']
        author = request.json['author']
        borrowed = False
    except KeyError:
        return {'error': 'missing required field'}, 400

    if isbn in [book['isbn'] for book in books]:
        return {'error': 'resource with that isbn existed'}, 409
    
    book = {'isbn': isbn, 'title': title, 'author': author, 'borrowed': borrowed}
    books.append(book)
    return book, 201

@app.route("/books/<int:isbn>", methods=['PUT'])
def update_book(isbn: int):
    try:
        title = request.json['title']
        author = request.json['author']
    except KeyError:
        return {'error': 'missing required field'}, 400

    found = False
    for book in books:
        if book['isbn'] == isbn:
            found = True
            book['title'] = title
            book['author'] = author
            return book

    if not found:
        return {'error': 'no book with that isbn lol'}, 404

@app.route("/books/<int:isbn>", methods=["DELETE"])
def delete_book(isbn: int):
    if isbn not in [book['isbn'] for book in books]:
        return "didn't even exist lol", 200

    for id, book in enumerate(books):
        if (book['isbn'] == isbn):
            books.remove(book)

    return 'done', 200

@app.route("/books/<int:isbn>/borrow", methods=['PATCH'])
def borrow_book(isbn: int):
    if isbn not in [book['isbn'] for book in books]:
        return {"error": "didn't even exist lol"}, 404

    for book in books:
        if book['isbn'] == isbn:
            found_book = book

    if found_book['borrowed'] == False:
        found_book['borrowed'] = True
        return "idk here's your book i guess", 200
    else:
        return {'error': "taken bruv"}, 409


@app.route("/books/<int:isbn>/return", methods=['PATCH'])
def return_book(isbn: int):
    if isbn not in [book['isbn'] for book in books]:
        return {"error": "didn't even exist lol"}, 404

    for book in books:
        if book['isbn'] == isbn:
            found_book = book

    if found_book['borrowed'] == True:
        found_book['borrowed'] = False 
        return "very well, no fine for u", 200
    else:
        return {'error': "what? not even taken man"}, 409
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
