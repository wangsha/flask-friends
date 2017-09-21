from flask import Blueprint

from friends.frameworks.flask.utils import load_strategy

friends_blueprint = Blueprint('friends', __name__)


@friends_blueprint.route()
@load_strategy
def