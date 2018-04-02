import types
from collections import defaultdict


# noinspection PyPep8Naming
class handles:
    def __init__(self, opcode):
        self.opcode = opcode
        self.func = None

    def __get__(self, instance, owner):
        if instance is not None:
            return types.MethodType(self.func, instance)
        return self

    def __call__(self, func):
        self.func = func
        return self

    def __repr__(self):
        return f'<handles: {hex(self.opcode)} is handled by {self.func}>'


class BaseHandler:
    def __init__(self):
        handlers = defaultdict(list)

        for k, v in vars(type(self)).items():
            if isinstance(v, handles):
                handlers[v.opcode] += [getattr(self, k)]

        self.handlers = handlers

    def handle(self, opcode):
        return [handler() for handler in self.handlers[opcode]]
