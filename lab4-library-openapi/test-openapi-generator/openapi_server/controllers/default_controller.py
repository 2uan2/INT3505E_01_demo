import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server import util


def books_get():  # noqa: E501
    """Returns list of books

    Returns list of books # noqa: E501


    :rtype: Union[List[Book], Tuple[List[Book], int], Tuple[List[Book], int, Dict[str, str]]
    """
    return 'do some magic!'


def books_isbn_borrow_patch(isbn):  # noqa: E501
    """Borrow a book using isbn

     # noqa: E501

    :param isbn: Book&#39;s isbn
    :type isbn: int

    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_isbn_delete(isbn):  # noqa: E501
    """Delete book using isbn

     # noqa: E501

    :param isbn: Book&#39;s isbn
    :type isbn: int

    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_isbn_get(isbn):  # noqa: E501
    """Getting book by isbn

     # noqa: E501

    :param isbn: Book&#39;s isbn
    :type isbn: int

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_isbn_put(isbn, body):  # noqa: E501
    """Editing a book using isbn

     # noqa: E501

    :param isbn: Book&#39;s isbn
    :type isbn: int
    :param book: Describe book to be created
    :type book: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book = body
    if connexion.request.is_json:
        book = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def books_isbn_return_patch(isbn):  # noqa: E501
    """Return a borrowed book using isbn

     # noqa: E501

    :param isbn: Book&#39;s isbn
    :type isbn: int

    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    return 'do some magic!'


def books_post(body):  # noqa: E501
    """Creates a new book

     # noqa: E501

    :param book: Parameters for new book
    :type book: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    book = body
    if connexion.request.is_json:
        book = Book.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def root_get():  # noqa: E501
    """Returns &#39;&lt;h1&gt;Hello world&lt;/h1&gt;&#39;

     # noqa: E501


    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    return 'do some magic!'
