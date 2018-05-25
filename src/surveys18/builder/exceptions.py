class SignError(Exception):
    def __init__(self, **kwargs):

        self.sign = kwargs.get('sign')

        Exception.__init__(self, "{0} Sign Length Is Not Valid {0}".format(self.sign))


