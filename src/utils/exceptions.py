from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Model
from rest_framework import exceptions as rest_exceptions


class ErrorHandlerMixin:
    model: Model = None

    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied,
        ObjectDoesNotExist: rest_exceptions.NotFound
    }

    def handle_exception(self, exc):
        self._add_model_does_not_exist()

        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))
            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)

    def _add_model_does_not_exist(self):
        if self.model is not None:
            self.expected_exceptions[
                self.model.DoesNotExist
            ] = rest_exceptions.NotFound


def get_error_message(exc):
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default
