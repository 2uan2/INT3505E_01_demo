from flask import Blueprint
from server import books

v1_bp = Blueprint("v1", __name__)

@v1_bp.route("/books")
def get_books_v1():
    return books

