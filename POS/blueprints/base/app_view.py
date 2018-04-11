from flask import make_response, jsonify
from flask.views import MethodView


class AppView(MethodView):
    """
        Generic method view to handle responses
    """
    @staticmethod
    def send_response(**kwargs):
        if kwargs is not None:
            return make_response(
                jsonify(kwargs)
            )
