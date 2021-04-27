#!/usr/bin/env python3

import connexion

from openapi_server import encoder
from .database import db_session


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'EasyMarket Server'},
                pythonic_params=True)

    app.run(port=8080)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()    


if __name__ == '__main__':
    main()
