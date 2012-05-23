class Registry(object):

    @classmethod
    def get(cls, key):
        try:
            return cls._registry[key]
        except (AttributeError, KeyError):
            raise LookupError('Not found %r in %s' % (key, cls.__name__))

    @classmethod
    def register(cls, key, obj):
        try:
            cls._registry[key] = obj
        except AttributeError:
            cls._registry = {key: obj}
