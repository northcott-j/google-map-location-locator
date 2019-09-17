from src.support.exceptions import BECoreException


class UnsupportedMapException(BECoreException):
    status_code = 400

    def __init__(self, map_id):
        message = f'Map ID {map_id} not supported by this service.'
        BECoreException.__init__(self, message)
