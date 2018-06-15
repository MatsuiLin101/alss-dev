import logging
import traceback
from .models import ReviewLog


class ReviewLogHandler(logging.Handler):
    def emit(self, record):

        trace = None

        if record.exc_info:
            trace = traceback.format_exc()

        msg = record.getMessage()
        user = record.__dict__.get('user')
        content_type = record.__dict__.get('content_type')
        object_id = record.__dict__.get('object_id')
        initial_errors = record.__dict__.get('initial_errors')
        current_errors = record.__dict__.get('current_errors')

        kwargs = {
            'logger_name': record.name,
            'level': record.levelno,
            'msg': msg,
            'trace': trace,
            'user': user,
            'content_type': content_type,
            'object_id': object_id,
            'initial_errors': initial_errors,
            'current_errors': current_errors,
        }
        logging.debug(msg)
        ReviewLog.objects.create(**kwargs)