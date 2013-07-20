# JSONRPCService for the CherrPy webserver.
# Copyright (C) 2011 Rene Maurer <renemaur@gmail.com>
# See LICENSE for details.
#
# Time-stamp: <2011-10-10 01:03:52 rene>
#
# Example usage:
#
# import cherrypy
# from pyjs.jsonrpc.cherrypy.jsonrpc import JSONRPCService
#
# class EchoService(JSONRPCService):
#
#     def __init__(self, defaultPage):
#         JSONRPCService.__init__(self, defaultPage)
#         self.add_method(self.echo.__name__, self.echo)    
#
#     def echo(self, msg):
#         return msg
#
# if __name__ == "__main__":
#     service =  EchoService(defaultPage='index.html')
#     configs = {'server.socket_port':8000, 'log.screen':True}
#     cherrypy.quickstart(service, '/', {'global':configs})

import os
import bottle
from pyjs.jsonrpc import JSONRPCServiceBase

class JSONRPCService(JSONRPCServiceBase):

    def __call__(self, extra=None):
        return self.process(bottle.request.body.read())

