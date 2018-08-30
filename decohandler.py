import logging
from collections import defaultdict

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        handlers = defaultdict(list)
        registered = set()

        for cls in type(self).mro():
            for k, v in vars(cls).items():
                if k not in registered and isinstance(v, handles):
                    logger.debug(v)
                    registered.add(k)
                    handlers[v.opcode] += [getattr(self, k)]

        self.handlers = dict(handlers)

    def get_handlers(self, opcode):
        try:
            return self.handlers[opcode]
        except KeyError:
            raise NotImplementedError(
                'There is no handler implemented for {}'.format(opcode))

    def handle(self, opcode, *args, **kwargs):
        return [handler(*args, **kwargs) for handler in self.get_handlers(opcode)]
