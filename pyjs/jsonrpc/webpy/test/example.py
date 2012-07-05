import web
from jsonrpc import JSONRPCService, jsonremote

svc = JSONRPCService()

@jsonremote(svc)
def upper(arg):
    return arg.upper()

@jsonremote(svc)
def lower(arg):
    return arg.lower()

urls = (
'/json', 'svc'
)
app = web.application(urls, globals())

if __name__ == "__main__":
  app.run()
