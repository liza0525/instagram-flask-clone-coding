import os
import warnings

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

docs = FlaskApiSpec()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
api = Api()

config_path = os.path.join(os.getcwd(), 'instagram', 'instagram.json')


def create_app(config_path=config_path):
    app = Flask(__name__)
    app.config.from_pyfile(config_path)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Instagram Clone Coding',
            version='0.0.1',
            openapi_version='2.0',
            plugins=[FlaskPlugin(), MarshmallowPlugin()]
        ),
        'APISPEC_SWAGGER_URL': '/docs.json',
        'APISPEC_SWAGGER_UI_URL': '/docs/'
    })

    # Register Extensions
    docs.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True, compare_server_default=True)
    cors.init_app(app)
    api.init_app(app)

    # suppress marshmallow schema name warnings
    warnings.filterwarnings(
        'ignore',
        message='Multiple schemas resolved to the name ',
    )

    with app.app_context():
        # migration model import

        # Blueprint

        # NOTE: blueprint 등록 후 주석 해제
        # blueprints = []
        # for bp in blueprints:
        #     app.register_blueprint(bp)

        # docs.register_existing_resources()

        # 스웨거에서 options 제거
        for key, value in docs.spec._paths.items():
            docs.spec._paths[key] = {
                inner_key: inner_value for inner_key, inner_value in value.items() if inner_key != 'options'
            }

    return app