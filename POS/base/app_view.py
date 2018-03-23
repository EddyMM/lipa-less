from flask import make_response, jsonify
from flask.views import MethodView


class AppView(MethodView):
    """
        Generic method view to handle responses
    """
    @staticmethod
    def send_response(msg, status):
        return make_response(jsonify(
            msg=msg,
            status=status
        ))
