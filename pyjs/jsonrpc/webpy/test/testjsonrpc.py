import jsonrpclib

s = jsonrpclib.ServerProxy("http://127.0.0.1:8000/json", verbose=1)
reply = s.upper("foo bar")
print reply

reply = s.lower("foo R bar")
print reply
