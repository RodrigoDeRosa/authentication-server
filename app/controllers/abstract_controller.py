from http import HTTPStatus

from flask import make_response, jsonify
from flask_restful import Resource

from app.model.errors.application_error import ApplicationError
from app.utils.logging.logger import Logger


class AbstractController(Resource):
    """
    This controller allows us to avoid having to define the HTTP verb methods
    in every other controller and only keep the methods that actually DO stuff.
    """

    INTERNAL_SERVER_ERROR_MESSAGE = 'Internal Server Error. ' \
                                    'Our best engineers were [probably] notified ' \
                                    'and are [probably] running to fix it.'

    _post_method = None
    _get_method = None
    _patch_method = None
    _put_method = None
    _delete_method = None

    __logger = Logger('AbstractController')

    def post(self, **kwargs):
        return self.handle_request(self._post_method, 'POST', **kwargs)

    def get(self, **kwargs):
        return self.handle_request(self._get_method, 'GET', **kwargs)

    def patch(self, **kwargs):
        return self.handle_request(self._patch_method, 'PATCH', **kwargs)

    def put(self, **kwargs):
        return self.handle_request(self._put_method, 'PUT', **kwargs)

    def delete(self, **kwargs):
        return self.handle_request(self._delete_method, 'DELETE', **kwargs)

    def handle_request(self, method, name, **kwargs):
        if not method:
            return self.build_exception(message=f'Invalid {name} request.', status=HTTPStatus.METHOD_NOT_ALLOWED)
        return self.wrap_handling(method, **kwargs)

    @classmethod
    def wrap_handling(cls, method, **kwargs):
        try:
            return method(**kwargs)
        except ApplicationError as ae:
            cls.__logger.error(ae.message)
            return cls.build_exception(ae.message, ae.status)
        except Exception as e:
            cls.__logger.error(e)
            return cls.build_exception(cls.INTERNAL_SERVER_ERROR_MESSAGE, HTTPStatus.INTERNAL_SERVER_ERROR)

    @classmethod
    def build_response(cls, body: dict = None, status: int = HTTPStatus.OK):
        return make_response(cls._to_json(body) if body is not None else '', status)

    @classmethod
    def build_exception(cls, message: str, status: int = HTTPStatus.INTERNAL_SERVER_ERROR):
        body = {'message': message, 'status': status}
        return make_response(cls._to_json(body), status)

    @classmethod
    def _to_json(cls, body: dict):
        return '' if body is None else jsonify(body)