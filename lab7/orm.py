from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import logging
import time

# --- Configuration ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nplus1_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Query Logging Utility ---
# Configure logging to capture SQLAlchemy queries
logging.basicConfig()
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.INFO)

# Global counter for queries executed in a request
query_counter = 0

with app.app_context():
    @event.listens_for(db.engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        global query_counter
        query_counter += 1
        # print(f"--- Query {query_counter}: {statement}")

    @app.before_request
    def reset_query_counter():
        global query_counter
        query_counter = 0
        app.logger.info("--- STARTING NEW REQUEST ---")
        app.logger.info(f"Initial query count reset to: {query_counter}")

    @app.after_request
    def log_query_count(response):
        app.logger.info(f"--- TOTAL QUERIES EXECUTED: {query_counter} ---")
        return response

# --- Database Models ---
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<Author {self.name}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'

# --- Utility to initialize data ---
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        author1 = Author(name='Alice')
        author2 = Author(name='Bob')
        author3 = Author(name='Charlie')
        db.session.add_all([author1, author2, author3])
        db.session.commit()

        # Posts for Alice
        db.session.add_all([
            Post(title='Alice Post 1', author=author1),
            Post(title='Alice Post 2', author=author1)
        ])
        # Posts for Bob
        db.session.add_all([
            Post(title='Bob Post 1', author=author2),
            Post(title='Bob Post 2', author=author2),
            Post(title='Bob Post 3', author=author2)
        ])
        # Post for Charlie
        db.session.add(Post(title='Charlie Post 1', author=author3))
        
        db.session.commit()
        app.logger.info("Database initialized with 3 authors and 6 posts.")

# --- N+1 Demonstration Route (The Problem) ---
@app.route('/nplus1')
def nplus1_problem():
    # Query 1: Retrieve all authors
    authors = db.session.execute(db.select(Author)).scalars().all()
    
    start_time = time.time()
    
    # N Queries: Loop through authors, accessing 'posts' relationship, which triggers 
    # a new query for each author if not already loaded (Lazy Loading)
    output = "<h1>N+1 Problem (Lazy Loading)</h1>"
    for author in authors:
        output += f"<h2>Author: {author.name}</h2>"
        # Accessing author.posts triggers a separate query for each author
        # In this case, 3 authors = 3 extra queries. Total: 1 (authors) + 3 (posts) = 4 queries
        output += "<ul>"
        for post in author.posts.all(): # .all() is necessary because lazy='dynamic'
            output += f"<li>{post.title}</li>"
        output += "</ul>"

    end_time = time.time()
    elapsed = end_time - start_time
    
    output += f"<p>Time elapsed: {elapsed:.4f}s</p>"
    output += f"<p>Total queries executed (Check console for count): **{query_counter}**</p>"
    output += "<hr>"
    output += "<a href='/eager'>View Solution (Eager Loading)</a>"
    return render_template_string(output)

# --- Eager Loading Solution Route (The Fix) ---
@app.route('/eager')
def eager_loading_solution():
    # Use joinedload to pre-load the 'posts' relationship in the initial query.
    # This executes a single, efficient JOIN query.
    # Total: 1 query
    authors = db.session.execute(
        db.select(Author).options(db.joinedload(Author.posts))
    ).scalars().all()

    start_time = time.time()

    # 0 Queries: Accessing 'posts' now uses the data pre-loaded by the join.
    output = "<h1>Eager Loading Solution (Joined Loading)</h1>"
    for author in authors:
        output += f"<h2>Author: {author.name}</h2>"
        # No extra query is executed here
        output += "<ul>"
        for post in author.posts.all(): # .all() is necessary because lazy='dynamic'
            output += f"<li>{post.title}</li>"
        output += "</ul>"
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    output += f"<p>Time elapsed: {elapsed:.4f}s</p>"
    output += f"<p>Total queries executed (Check console for count): **{query_counter}**</p>"
    output += "<hr>"
    output += "<a href='/nplus1'>View Problem (N+1)</a>"
    return render_template_string(output)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
