# coding: utf-8
import sys
import json
import os
from datetime import datetime
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


def _collect_page_source():
    page_source = current_test.driver.page_source
    path_to_file = "%s.page_source.xml" % os.sep.join(
        [get_path_for_metadata(), get_filename_base()]
    )
    page_source_meta_info = {
        "path": path_to_file,
        "name": "page_source",
        "mime_type": "text/plain"
    }
    current_test._meta_info["attachments"].append(page_source_meta_info)
    with open(path_to_file, "w", encoding="utf-8") as f:
        f.write(page_source)


def _collect_error_details():
    _meta = current_test._meta_info
    _meta['stack_trace'] = format_exc()
    _meta['message'] = str(sys.exc_info()[1])
    if config.utils.get('collect_page_source', True):
        try:
            _collect_page_source()
        except:
            log.exception('Error collecting page source')


def report_to_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(
            obj=current_test._meta_info,
            cls=ContestoJSONEncoder,
            ensure_ascii=False)
        )


def _dump_meta_info():
    path = get_path_for_metadata()
    file = os.path.join(path, '%s.json' % get_filename_base())

    try:
        report_to_file(file)
    except:
        log.exception('Error while dump test metadata to file')
