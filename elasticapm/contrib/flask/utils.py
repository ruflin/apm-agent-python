try:
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib import urlencode

from elasticapm.utils import get_url_dict
from elasticapm.utils.wsgi import get_environ, get_headers


def get_data_from_request(request):
    body = None
    if request.data:
        body = request.data
    elif request.form:
        body = urlencode(request.form)

    result = {
        'body': body,
        'env': dict(get_environ(request.environ)),
        'headers': dict(
            get_headers(request.environ),
        ),
        'method': request.method,
        'socket': {
            'remote_address': request.environ.get('REMOTE_ADDR'),
            'encrypted': request.is_secure
        },
        'cookies': request.cookies,
    }

    result['url'] = get_url_dict(request.url)

    return result
