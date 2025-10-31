import datetime
from datetime import timedelta
from functools import wraps
from typing import List, Optional

from flask import Flask, jsonify, request, send_from_directory, url_for
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager, get_jwt
from pydantic import BaseModel, ValidationError
from passlib.context import CryptContext

# --- Configuration & Setup ---

# Security & JWT Configuration
# NOTE: Replace these with real, strong secrets in a production environment
SECRET_KEY = "supersecretkey" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
JWT_SECRET_KEY = "library-api-jwt-secret" 

# Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Dummy Data ---

# User Database
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123"),
        "role": "admin",
    },
    "user": {
        "username": "user",
        "hashed_password": pwd_context.hash("user123"),
        "role": "user",
    }
}

# Book Database (using 'isbn' as ID)
books = [
    {"isbn": 100, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 101, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 102, "title": "The", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 110, "title": "Thet", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 200, "title": "1984", "author": "George Orwell", "borrowed": False}
]

# --- Pydantic Models for Data Validation ---

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    role: str

class BookBase(BaseModel):
    isbn: int
    title: str
    author: str
    borrowed: bool = False

class BookCreate(BookBase):
    pass

class Book(BookBase):
    pass

    class Config:
        from_attributes = True

# --- Authentication and Authorization Utilities ---

def verify_password(plain_password, hashed_password):
    """Checks if the plain password matches the hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str) -> Optional[UserInDB]:
    """Retrieves a user from the fake database."""
    if username in db:
        return UserInDB(**db[username])
    return None

def authenticate_user(db, username: str, password: str) -> Optional[UserInDB]:
    """Authenticates a user against the database."""
    user = get_user(db, username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def admin_required():
    """Custom decorator for role-based authorization (requires 'admin' role)."""
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            # Get the claims (payload) from the JWT
            claims = get_jwt()
            user_role = claims.get("role")
            
            if user_role != "admin":
                return jsonify({"detail": "Permission denied. Admin role required."}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


# --- Flask App Setup ---

app = Flask(__name__)
CORS(app)

# JWT Setup
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
jwt = JWTManager(app)

# Swagger UI Setup
SWAGGER_URL = '/docs'
API_URL = '/openapi.yaml'
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_blueprint)

@app.route('/openapi.yaml')
def get_openapi_yaml():
    """Route to serve the OpenAPI spec file."""
    # NOTE: You would need to create an actual openapi.yaml file 
    # describing your API and security scheme for this to fully work.
    return send_from_directory('.', 'openapi.yaml')


# --- Public/Auth Routes ---

@app.route('/')
def home():
    """Root endpoint with docs link."""
    return '<div>Welcome to the Book API. Checkout the docs at <a href="/docs">docs</a></div>'

@app.route("/login", methods=["POST"])
def login():
    """Authenticates user and returns an access token."""
    # Now expecting application/json in the request body
    data = request.get_json()

    if not data:
        return jsonify({"detail": "Missing JSON body"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"detail": "Missing 'username' or 'password' in JSON body"}), 400

    user = authenticate_user(fake_users_db, username, password)

    if not user:
        return jsonify({"detail": "Invalid username or password"}), 401

    # Add role to the JWT claims
    additional_claims = {"role": user.role}
    
    # Create token with username as identity
    access_token = create_access_token(identity=user.username, additional_claims=additional_claims)
    
    # Return the token data
    return Token(access_token=access_token).model_dump()

# --- Book Pagination/Utility Functions (Unchanged from base code) ---

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
    if cursor is None:
        if len(items) <= limit:
            return items, None
        return items[:limit], items[limit]["isbn"]

    idx = next((i for i, b in enumerate(items) if str(b["isbn"]) == str(cursor)), None)
    if idx is None or idx == len(items) - 1:
        return [], None
    
    start = idx + 1
    end = start + limit
    
    # Ensure next_cursor points to a valid item or is None
    next_cursor = items[end - 1]["isbn"] if end <= len(items) else None
    return items[start:end], next_cursor


# --- Secured API Routes (V2) ---

@app.route('/v2/books', methods=['GET'])
@jwt_required()
def get_books():
    """Secured: Allows any logged-in user to retrieve books with pagination."""
    offset = request.args.get("offset", type=int)
    limit = request.args.get("limit", type=int, default=2)
    page = request.args.get("page", type=int)
    size = request.args.get("size", type=int, default=2)
    cursor = request.args.get("cursor")

    if offset is not None:
        paginated = apply_offset_limit(books, offset=offset, limit=limit)
        return jsonify({
            "strategy": "offset/limit",
            "data": paginated
        })
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
    else:
        # Default: first page of cursor-based
        paginated, next_cursor = apply_cursor(books, cursor=None, limit=limit)
        return jsonify({
            "strategy": "cursor (default)",
            "data": paginated,
            "next_cursor": next_cursor
        })

@app.route("/v1/books")
@jwt_required()
def get_books_v1():
    """Secured: Allows any logged-in user to retrieve all books (V1)."""
    return jsonify(books)

@app.route('/v2/books/<int:isbn>', methods=['GET'])
@jwt_required()
def get_book(isbn: int):
    """Secured: Allows any logged-in user to retrieve a specific book."""
    book = [book for book in books if book['isbn'] == isbn]
    return jsonify(book[0]) if book else (jsonify({'error': 'no book with that isbn'}), 404)

@app.route('/v2/books', methods=['POST'])
@admin_required()
def create_book():
    """Secured: Requires admin role to create a book."""
    try:
        # Validate data using Pydantic model
        book_in = BookCreate(**request.get_json())
    except (ValidationError, TypeError, KeyError) as e:
        return jsonify({'error': 'Invalid or missing required fields', 'details': str(e)}), 400

    if book_in.isbn in [book['isbn'] for book in books]:
        return jsonify({'error': f'Resource with ISBN {book_in.isbn} already exists'}), 409
        
    book = book_in.model_dump()
    books.append(book)
    return jsonify(book), 201

@app.route("/v2/books/<int:isbn>", methods=['PUT'])
@admin_required()
def update_book(isbn: int):
    """Secured: Requires admin role to update a book."""
    try:
        # Validate update data structure (we allow partial fields, but Pydantic requires all, 
        # so we'll check fields manually or use a more flexible model if needed for PATCH)
        update_data = request.get_json()
        title = update_data['title']
        author = update_data['author']
    except KeyError:
        return jsonify({'error': 'missing required field (title and author)'}), 400

    found = False
    for book in books:
        if book['isbn'] == isbn:
            found = True
            book['title'] = title
            book['author'] = author
            # We don't change 'borrowed' status via PUT here, only title/author
            return jsonify(book)

    if not found:
        return jsonify({'error': 'no book with that isbn lol'}), 404

@app.route("/v2/books/<int:isbn>", methods=["DELETE"])
@admin_required()
def delete_book(isbn: int):
    """Secured: Requires admin role to delete a book."""
    book_to_delete = next((book for book in books if book['isbn'] == isbn), None)
    
    if not book_to_delete:
        # Return 204 No Content if the resource is already gone, or 404
        return jsonify({"message": "Book not found, nothing to delete."}), 404 

    books.remove(book_to_delete)
    return jsonify({"message": "Book deleted"}), 204 # HTTP 204 No Content

@app.route("/v2/books/<int:isbn>/borrow", methods=['PATCH'])
@jwt_required()
def borrow_book(isbn: int):
    """Secured: Allows any logged-in user to borrow a book."""
    found_book = next((book for book in books if book['isbn'] == isbn), None)
    
    if not found_book:
        return jsonify({"error": "Book with that isbn not found"}), 404

    if found_book['borrowed'] == False:
        found_book['borrowed'] = True
        return jsonify({"message": "Book successfully borrowed"}), 200
    else:
        return jsonify({'error': "Book is already taken"}), 409


@app.route("/v2/books/<int:isbn>/return", methods=['PATCH'])
@jwt_required()
def return_book(isbn: int):
    """Secured: Allows any logged-in user to return a book."""
    found_book = next((book for book in books if book['isbn'] == isbn), None)

    if not found_book:
        return jsonify({"error": "Book with that isbn not found"}), 404

    if found_book['borrowed'] == True:
        found_book['borrowed'] = False
        return jsonify({"message": "Book successfully returned"}), 200
    else:
        return jsonify({'error': "Book was not currently borrowed"}), 409
    
if __name__ == '__main__':
    # Running this will start the server on http://127.0.0.1:5000/
    app.run(host="0.0.0.0", debug=True)
