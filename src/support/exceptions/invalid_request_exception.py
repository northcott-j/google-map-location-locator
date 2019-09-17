from src.support.exceptions import BECoreException


class InvalidRequestException(BECoreException):
    status_code = 400

    def __init__(self, error):
        message = 'Invalid request: {0}'.format(error)
        BECoreException.__init__(self, message)
