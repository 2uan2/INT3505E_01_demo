import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.product_create_request import ProductCreateRequest  # noqa: E501
from swagger_server.models.product_patch_request import ProductPatchRequest  # noqa: E501
from swagger_server.models.product_response import ProductResponse  # noqa: E501
from swagger_server import util


def api_v1_products_get():  # noqa: E501
    """Returns list of all products

    Returns list of all products # noqa: E501


    :rtype: List[ProductResponse]
    """
    return 'do some magic!'


def api_v1_products_id_delete(id):  # noqa: E501
    """Delete product using id

     # noqa: E501

    :param id: Product&#x27;s id
    :type id: int

    :rtype: str
    """
    return 'do some magic!'


def api_v1_products_id_get(id):  # noqa: E501
    """Getting product by id

     # noqa: E501

    :param id: Product&#x27;s id
    :type id: int

    :rtype: ProductResponse
    """
    return 'do some magic!'


def api_v1_products_id_patch(body, id):  # noqa: E501
    """Edit a product using id

     # noqa: E501

    :param body: Describe product to be edited
    :type body: dict | bytes
    :param id: Product&#x27;s id
    :type id: int

    :rtype: ProductResponse
    """
    if connexion.request.is_json:
        body = ProductPatchRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def api_v1_products_id_put(body, id):  # noqa: E501
    """Edit a product using id

     # noqa: E501

    :param body: Describe product to be edited
    :type body: dict | bytes
    :param id: Product&#x27;s id
    :type id: int

    :rtype: ProductResponse
    """
    if connexion.request.is_json:
        body = ProductCreateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def api_v1_products_post(body):  # noqa: E501
    """Creates a new product

     # noqa: E501

    :param body: Parameters for new product
    :type body: dict | bytes

    :rtype: ProductResponse
    """
    if connexion.request.is_json:
        body = ProductCreateRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
