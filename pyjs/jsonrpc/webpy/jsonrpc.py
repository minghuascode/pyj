from pyjs.jsonrpc import JSONRPCServiceBase, jsonremote
import web


class JSONRPCService(JSONRPCServiceBase):

    def POST(self):
        web.header("Content-Type","text/plain")
        return self.process(web.data())

    def __call__(self, func=None):
        if func is None:
            return self # webpy insistence on setup using class names
        self.methods[func.__name__] = func
        return func

