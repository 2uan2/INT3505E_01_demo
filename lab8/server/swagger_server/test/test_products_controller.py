# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.product_create_request import ProductCreateRequest  # noqa: E501
from swagger_server.models.product_patch_request import ProductPatchRequest  # noqa: E501
from swagger_server.models.product_response import ProductResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProductsController(BaseTestCase):
    """ProductsController integration test stubs"""

    def test_api_v1_products_get(self):
        """Test case for api_v1_products_get

        Returns list of all products
        """
        response = self.client.open(
            '/api/v1/products',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_products_id_delete(self):
        """Test case for api_v1_products_id_delete

        Delete product using id
        """
        response = self.client.open(
            '/api/v1/products/{id}'.format(id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_products_id_get(self):
        """Test case for api_v1_products_id_get

        Getting product by id
        """
        response = self.client.open(
            '/api/v1/products/{id}'.format(id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_products_id_patch(self):
        """Test case for api_v1_products_id_patch

        Edit a product using id
        """
        body = ProductPatchRequest()
        response = self.client.open(
            '/api/v1/products/{id}'.format(id=789),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_products_id_put(self):
        """Test case for api_v1_products_id_put

        Edit a product using id
        """
        body = ProductCreateRequest()
        response = self.client.open(
            '/api/v1/products/{id}'.format(id=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_v1_products_post(self):
        """Test case for api_v1_products_post

        Creates a new product
        """
        body = ProductCreateRequest()
        response = self.client.open(
            '/api/v1/products',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
