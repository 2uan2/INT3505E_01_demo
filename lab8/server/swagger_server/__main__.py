#!/usr/bin/env python3

import connexion
from .database import db

from . import encoder 
from .models.product_entity import Product


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    flask_app = app.app

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.sqlite3"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =  False

    db.init_app(flask_app)
    app.add_api('swagger.yaml', arguments={'title': 'Product API'}, pythonic_params=True)

    with app.app.app_context():
        db.create_all()

    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
