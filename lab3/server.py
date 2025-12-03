from flask import Flask, jsonify, request, url_for, redirect
from flask_cors import CORS

def create_app():
    from v1.routes import v1_bp
    from v2.routes import v2_bp

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(v1_bp, url_prefix='/v1')
    app.register_blueprint(v2_bp, url_prefix='/v2')

    return app


books = [
    {"isbn": 100, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 101, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 102, "title": "The", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 110, "title": "Thet", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 200, "title": "1984", "author": "George Orwell", "borrowed": False},
    {"isbn": 300, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 400, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 500, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 600, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 700, "title": "The", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 800, "title": "Thet", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 900, "title": "1984", "author": "George Orwell", "borrowed": False},
    {"isbn": 1000, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 1100, "title": "The", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 1200, "title": "Thet", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 1300, "title": "1984", "author": "George Orwell", "borrowed": False},
    {"isbn": 1400, "title": "The Hobbit", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 1500, "title": "The", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 1600, "title": "Thet", "author": "J.R.R. Tolkien", "borrowed": True},
    {"isbn": 1700, "title": "1984", "author": "George Orwell", "borrowed": False},

]



if __name__ == '__main__':
    from v1.routes import get_books_v1
    from v2.routes import get_books_v2
    app = create_app()

    @app.route('/')
    def home():
        return '<div>Welcome to somewhere INT3505E_01</div>'

    @app.route('/books')
    def xapi():
        version = int(request.headers.get("X-API-Version"))
        print(version)
        if version == 1:
            return get_books_v1()
        elif version == 2:
            return get_books_v2()
        else:
            return get_books_v2()


    app.run(host="0.0.0.0", debug=True)
