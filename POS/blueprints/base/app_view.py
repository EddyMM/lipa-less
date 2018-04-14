from flask import make_response, jsonify
from flask.views import MethodView


class AppView(MethodView):
    """
        Generic method view to handle responses
    """
    @staticmethod
    def send_response(msg, status, **kwargs):
        response_body = dict(msg=msg)

        if kwargs:
            response_body.update(kwargs)

        response = make_response(
            jsonify(response_body)
        )
        response.headers["code"] = status

        return response
