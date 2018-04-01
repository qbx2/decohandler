import functools
from collections import defaultdict


# noinspection PyPep8Naming
class handles:
    def __init__(self, opcode):
        self.opcode = opcode
        self.func = None

    def __get__(self, instance, owner):
        if instance is not None:
            return functools.partial(self.func, instance)
        return self

    def __call__(self, func):
        self.func = func
        return self

    def __repr__(self):
        return f'<handles: {hex(self.opcode)} is handled by {self.func}>'


class BaseHandler:
    def __init__(self):
        handlers = defaultdict(list)
        class_ = self.__class__
        attrs = \
            map(lambda k: (getattr(class_, k), getattr(self, k)), dir(class_))

        for class_attr, instance_attr in attrs:
            if isinstance(class_attr, handles):
                handlers[class_attr.opcode] += [instance_attr]

        self.handlers = handlers

    def handle(self, opcode):
        return [handler() for handler in self.handlers[opcode]]


class ServerHandler(BaseHandler):
    @handles(0x12)
    def handle_hello(self):
        return 'hello'

    @handles(0x12)
    def handle_hello2(self):
        return 'hello2'

    @handles(0x34)
    def handle_bye(self):
        return 'bye'


class Client:
    def __init__(self):
        super().__init__()

        self.server = ServerHandler()

    def _request(self, opcode):
        return self.server.handle(opcode)

    def hello(self):
        print(self._request(0x12))

    def bye(self):
        print(self._request(0x34))


client = Client()
client.hello()
client.hello()
client.bye()
client.bye()
