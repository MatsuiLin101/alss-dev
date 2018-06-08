class SignError(Exception):
    def __init__(self, **kwargs):
        sign = kwargs.get('sign')
        Exception.__init__(self, "{0} Sign Length Is Not Valid".format(sign))


class StringLengthError(Exception):
    def __init__(self, **kwargs):
        model = kwargs.get('target')
        msg = kwargs.get('msg')
        Exception.__init__(self, "{0} String Length Is Not Valid: {1}".format(model, msg))


class CreateModelError(Exception):
    def __init__(self, msg):
        model = kwargs.get('target')
        msg = kwargs.get('msg')
        Exception.__init__(self, "{0} Create Model Is Error: {1}".format(model, msg))


