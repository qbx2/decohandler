from collections import defaultdict


# noinspection PyPep8Naming
class handles:
    def __init__(self, opcode):
        self.opcode = opcode
        self.__func__ = None

    def __get__(self, instance=None, owner=None):
        return self.__func__.__get__(instance, owner)

    def __call__(self, func):
        self.__func__ = func
        return self

    def __repr__(self):
        return '<{} handles opcode {}>'.format(self.__func__, self.opcode)


class BaseHandler:
    def __init__(self):
        handlers = defaultdict(list)

        for k, v in vars(type(self)).items():
            if isinstance(v, handles):
                handlers[v.opcode] += [getattr(self, k)]

        self.handlers = dict(handlers)

    def handle(self, opcode, *args, **kwargs):
        try:
            return [handler(*args, **kwargs) for handler in self.handlers[opcode]]
        except KeyError:
            raise NotImplementedError(
                'There is no handler implemented for {}'.format(opcode))
