from flask import Flask, jsonify, request, send_from_directory, url_for
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
    {"isbn": 101, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 102, "title": "The", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 110, "title": "Thet", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 200, "title": "1984", "author": "George Orwell", "borrowed": False}
]

@app.route('/')
def home():
    return '<div>Welcome to uhh, idk, you can checkout the docs at <a href="/docs">docs</a></div>'

@app.route('/books')
def get_books():
    # offset = request.args.get("offset", type=int, default=0)
    # limit = request.args.get("limit", type=int, default=len(books))
    # returned_books = []
    # for i in range(limit):
    #     returned_books.append(books[offset+i])
    # return returned_books, 200
    # return books
    offset = request.args.get("offset", type=int)
    limit = request.args.get("limit", type=int, default=2)
    page = request.args.get("page", type=int)
    size = request.args.get("size", type=int, default=2)
    cursor = request.args.get("cursor")

    # Strategy 1: Offset/Limit
    if offset is not None:
        paginated = apply_offset_limit(books, offset=offset, limit=limit)
        return jsonify({
            "strategy": "offset/limit",
            "data": paginated
        })

    # Strategy 2: Page/Size
    elif page is not None:
        paginated = apply_page(books, page=page, size=size)
        total_pages = (len(books) + size - 1) // size
        return jsonify({
            "strategy": "page/size",
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "data": paginated
        })

    # Strategy 3: Cursor-based
    elif cursor is not None:
        paginated, next_cursor = apply_cursor(books, cursor=cursor, limit=limit)
        response = {
            "strategy": "cursor",
            "data": paginated,
            "next_cursor": next_cursor
        }
        if next_cursor:
            response["next_url"] = url_for("get_books", cursor=next_cursor, limit=limit, _external=True)
        return jsonify(response)

    # Default: first page of cursor-based or all books
    else:
        paginated, next_cursor = apply_cursor(books, cursor=None, limit=limit)
        return jsonify({
            "strategy": "cursor (default)",
            "data": paginated,
            "next_cursor": next_cursor
        })

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
    
# @app.route("/books")
# def get_offseted_books(offset: int, limit: int):
#     print("limit is: ", limit)
#     print("offset is: ", offset)
#     returned_books = []
#     for i in range(limit):
#         returned_books.append(books[offset+i])
#     return returned_books, 200

def apply_offset_limit(items, offset=0, limit=None):
    if limit is None:
        return items[offset:]
    return items[offset:offset + limit]

def apply_page(items, page=1, size=10):
    start = (page - 1) * size
    end = start + size
    return items[start:end]

def apply_cursor(items, cursor=None, limit=2):
    """Cursor-based pagination using ISBN as cursor."""
    # If no cursor, start at beginning
    if cursor is None:
        return items[:limit], items[limit]["isbn"] if len(items) > limit else None
    
    # Find cursor index
    idx = next((i for i, b in enumerate(items) if str(b["isbn"]) == str(cursor)), None)
    if idx is None:
        return [], None

    start = idx + 1
    end = start + limit
    next_cursor = items[end - 1]["isbn"] if end < len(items) else None
    return items[start:end], next_cursor

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
