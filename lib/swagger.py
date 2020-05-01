import yaml
from flask_swagger_ui import get_swaggerui_blueprint


def get_blueprint(swagger_url, swagger_path, app_name):
    with open(swagger_path, "r") as f:
        swagger_yml = yaml.load(f, Loader=yaml.Loader)

    return get_swaggerui_blueprint(swagger_url, swagger_path, config={"spec": swagger_yml, "app_name": app_name})
