import connexion
import six
import time

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.product_create_request import ProductCreateRequest  # noqa: E501
from swagger_server.models.product_patch_request import ProductPatchRequest  # noqa: E501
from swagger_server.models.product_response import ProductResponse  # noqa: E501
from swagger_server.models.product_entity import Product
from swagger_server import util
from flask_sqlalchemy import SQLAlchemy

from ..database import db


def api_v1_products_get():  # noqa: E501
    """Returns list of all products

    Returns list of all products # noqa: E501


    :rtype: List[ProductResponse]
    """
    products = db.session.execute(db.select(Product)).scalars()
    product_responses = []
    for product in products:
        product_response = ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            sku=product.sku,
            quantity=product.quantity,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
        product_responses.append(product_response.to_dict())

    return product_responses


def api_v1_products_id_delete(id_):  # noqa: E501
    """Delete product using id

     # noqa: E501

    :param id: Product&#x27;s id
    :type id: int

    :rtype: str
    """
    product = db.get_or_404(Product, id_)
    db.session.delete(product)
    db.session.commit()
    return 200


def api_v1_products_id_get(id_):  # noqa: E501
    """Getting product by id

     # noqa: E501

    :param id: Product&#x27;s id
    :type id: int

    :rtype: ProductResponse
    """
    product = db.get_or_404(Product, id_)
    product_response = ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        sku=product.sku,
        quantity=product.quantity,
        created_at=product.created_at,
        updated_at=product.updated_at
    )

    return product_response.to_dict()


def api_v1_products_id_patch(body, id_):  # noqa: E501
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

    product = db.get_or_404(Product, id_)
    for k, v in body.to_dict().items():
        if v is not None:
            setattr(product, k, v)

    product.updated_at = int(time.time())
    db.session.commit()
    return 'do some magic!'


def api_v1_products_id_put(body, id_):
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

    product = db.get_or_404(Product, id_)
    for k, v in body.to_dict().items():
        setattr(product, k, v)

    product.updated_at = int(time.time())
    db.session.commit()
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
        product = Product(
            name=body.name,
            description=body.description,
            price=body.price,
            quantity=body.quantity,
            sku=body.sku,
            created_at=int(time.time()),
            updated_at=int(time.time())
        )
        db.session.add(product)
        db.session.commit()
    return 'do some magic!'
