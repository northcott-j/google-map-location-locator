from flask import current_app as app
from flask import request
from functools import wraps
from src.support.exceptions import UnsupportedMapException, InvalidRequestException


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


def check_map_id(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if kwargs.get('map_id') not in app.config['LOCATION_MAPS']:
            raise UnsupportedMapException(kwargs.get('map_id'))
        return f(*args, **kwargs)
    return decorated


def inject_location_collection(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        map_id = kwargs.get('map_id')
        location_collection = app.config.get('LOCATION_MAPS', {}).get(map_id, {})
        kwargs['locations'] = location_collection
        return f(*args, **kwargs)
    return decorated


@parametrized
def inject_request_body(f, **params):
  @wraps(f)
  def decorated(*args, **kwargs):
    data = request.get_json(force=True, silent=True)
    if data is None:
      raise InvalidRequestException('Expected a JSON request body!')

    if 'allowed' in params:
      data = {k:data[k] for k in params['allowed'] if k in data}

    kwargs['data'] = data
    return f(*args, **kwargs)

  return decorated
