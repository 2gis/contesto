# coding: utf-8
import sys
import json
import os

from datetime import datetime
from functools import wraps
from traceback import format_exc

from contesto import config
from contesto.globals import current_test
from contesto.utils.log import log


class ContestoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj.to_json()
        except AttributeError:
            return super(ContestoJSONEncoder, self).encode(obj)


def get_filename_base():
    date_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    return '%s%s' % (str(current_test), date_time)


def get_path_for_metadata():
    path = config.utils.get('metadata_path', None)
    if path is None:
        log.info("No 'metadata_path' provided in config. "
                 "Defaulting to '.test_metadata'")
        path = '.test_metadata'
    path = path.rstrip(os.path.sep)
    return path


def _collect_error_details():
    _meta = current_test._meta_info
    _meta['stack_trace'] = format_exc()
    _meta['message'] = str(sys.exc_info()[1])


def report_to_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(
            obj=current_test._meta_info,
            cls=ContestoJSONEncoder,
            ensure_ascii=False)
        )


def _collect():
    _collect_error_details()

    path = get_path_for_metadata()
    file = os.path.join(path, '%s.json' % get_filename_base())

    try:
        report_to_file(file)
    except Exception as e:
        log.warn('Error reporting test metadata to file: %s', e)


def collect_on_error(func):
    if hasattr(func, "__will_collect_metadata__"):
        return func

    setattr(func, "__will_collect_metadata__", True)

    @wraps(func)
    def wrapper(test, *args, **kwargs):
        try:
            return func(test, *args, **kwargs)
        except:
            _collect()
            raise

    return wrapper
