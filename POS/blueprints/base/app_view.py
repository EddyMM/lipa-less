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

    @staticmethod
    def error_in_request_response():
        return AppView.send_response(
            msg="Problem with request type or structure",
            status=400
        )

    @staticmethod
    def validation_error_response():
        return AppView.send_response(
            msg="Missing fields or values",
            status=400
        )

    @staticmethod
    def error_in_processing_request():
        return AppView.send_response(
            msg="Problem processing your request, we will fix it soon, kindly be patient",
            status=500
        )
