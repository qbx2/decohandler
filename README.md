# Decorator for Implementing Handlers in Python
## Easy
```python
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
```
