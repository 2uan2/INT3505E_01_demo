import unittest

from flask import json

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_books_get(self):
        """Test case for books_get

        Returns list of books
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_isbn_borrow_patch(self):
        """Test case for books_isbn_borrow_patch

        Borrow a book using isbn
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{isbn}/borrow'.format(isbn=56),
            method='PATCH',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_isbn_delete(self):
        """Test case for books_isbn_delete

        Delete book using isbn
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{isbn}'.format(isbn=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_isbn_get(self):
        """Test case for books_isbn_get

        Getting book by isbn
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{isbn}'.format(isbn=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_isbn_put(self):
        """Test case for books_isbn_put

        Editing a book using isbn
        """
        book = {"author":"author","isbn":0,"title":"title","borrowed":True}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books/{isbn}'.format(isbn=56),
            method='PUT',
            headers=headers,
            data=json.dumps(book),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_isbn_return_patch(self):
        """Test case for books_isbn_return_patch

        Return a borrowed book using isbn
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/books/{isbn}/return'.format(isbn=56),
            method='PATCH',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_books_post(self):
        """Test case for books_post

        Creates a new book
        """
        book = {"author":"author","isbn":0,"title":"title","borrowed":True}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/books',
            method='POST',
            headers=headers,
            data=json.dumps(book),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_root_get(self):
        """Test case for root_get

        Returns '<h1>Hello world</h1>'
        """
        headers = { 
            'Accept': 'text/html',
        }
        response = self.client.open(
            '/',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
