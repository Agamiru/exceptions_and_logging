from rest_framework.views import exception_handler, set_rollback, Response
from .exceptions import ApplicationErrors


def app_exception_handler(exc, context):

    if isinstance(exc, ApplicationErrors):
        kwargs = exc._extra_kwargs()
        logger = exc.get_logger()
        logger.exception(exc.message, exc_info=True, extra=kwargs)
        data = exc.err_dict()
        set_rollback()
        return Response(data, status=exc.status_code)

    response = exception_handler(exc, context)

    return response



